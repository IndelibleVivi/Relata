"""Read-only registration for existing RC-005 and future-question workspaces.

Compatibility registration deliberately uses the upstream canonical verifier
once, then freezes an exact, finite inventory into Lab artifacts. Reading a
registered source never reruns a fixture, imports judgments, or requires the
original native run.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools import future_question_review as future_review
from tools import rc005_review as rc005_review

FORMAT_PRACTICE = "rc005-practice-workspace-1"
FORMAT_NATIVE = "rc005-native-workspace-1"
FORMAT_FUTURE = "future-question-workspace-1"
FORMATS = {FORMAT_PRACTICE, FORMAT_NATIVE, FORMAT_FUTURE}
SOURCE_FORMAT = "relata-legacy-compat-source-1"
BUNDLE_FORMAT = "relata-legacy-frozen-material-1"
MAX_MEMBER_BYTES = 64 * 1024 * 1024

COMMON_FILES = {
    "review-packet.json", "contract.json", "source-snapshot.json",
    "private-binding.json",
}
FUTURE_DIRS = {
    "inputs", "hidden", "responses", "reviews", "review-keys",
}


def require(condition: bool, message: str, code: str = "compat") -> None:
    if not condition:
        from .core import LabError
        raise LabError(code, message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def _real_directory(path: Path) -> Path:
    absolute = path.expanduser().absolute()
    require(not any(item.is_symlink() for item in (absolute, *absolute.parents)),
            "legacy path may not contain symlinks")
    resolved = absolute.resolve()
    require(resolved.is_dir(), "legacy workspace does not exist")
    return resolved


def _member(path: Path) -> dict[str, Any]:
    require(not path.is_symlink() and path.is_file(), "legacy inventory member is invalid")
    size = path.stat().st_size
    require(size <= MAX_MEMBER_BYTES, "legacy inventory member exceeds size limit")
    data = path.read_bytes()
    return {"name": path.name, "size": size, "sha256": future_review.digest(data),
            "text": data.decode("utf-8"), "media_type": "text/plain; charset=utf-8"}


def _inventory(root: Path, relative: str) -> list[dict[str, Any]]:
    if not relative:
        return [_member(path) for path in sorted(root.iterdir())]
    folder = root / relative
    require(folder.is_dir() and not folder.is_symlink(),
            "legacy inventory directory is invalid")
    return [_member(path) for path in sorted(folder.iterdir())]


def _register(lab, title: str, body: dict[str, Any],
              command_id: str) -> dict[str, Any]:
    payload = {"kind": "source", "title": title, "body": body,
               "refs": [], "visibility": "private"}
    return lab.command("object.create", payload, command_id)


def _freeze_files(lab, files: list[dict[str, Any]], command_id: str,
                  format_id: str) -> dict[str, Any]:
    members = []
    for item in files:
        stored = lab.command(
            "artifact.put",
            {"text": item["text"], "media_type": item["media_type"]},
            command_id + ":" + item["name"])
        require(stored["digest"] == item["sha256"],
                "artifact store did not preserve legacy bytes")
        members.append({"name": item["name"], "media_type": item["media_type"],
                        "size": item["size"], "sha256": item["sha256"],
                        "artifact_digest": stored["digest"]})
    manifest = {"format": BUNDLE_FORMAT, "legacy_format": format_id,
                "files": members}
    stored = lab.command(
        "artifact.put",
        {"text": canonical(manifest).decode("utf-8"),
         "media_type": "application/json"},
        command_id + ":manifest")
    return {"artifact_digest": stored["digest"], "files": members}


def register_legacy(lab, path: Path, format_id: str, command_id: str,
                    native_run: Path | None = None) -> dict[str, Any]:
    """Freeze one known legacy workspace into a private Lab source object."""
    require(format_id in FORMATS, "unsupported legacy format")
    require(isinstance(command_id, str) and command_id,
            "compatibility registration needs a command_id")
    root = _real_directory(Path(path))

    files: list[dict[str, Any]] = []
    verification: dict[str, Any]
    if format_id in {FORMAT_PRACTICE, FORMAT_NATIVE}:
        require({item.name for item in root.iterdir()} ==
                COMMON_FILES | {"drafts", "judgments"},
                "legacy review inventory changed")
        native_binding = format_id == FORMAT_NATIVE
        workspace_verify = rc005_review.load_workspace(
            root, verify_run=False if native_binding else True)
        if native_binding:
            require(not workspace_verify["practice_only"],
                    "native format requires a non-practice binding")
            require(native_run is not None,
                    "native format requires its original run")
            selected_run = _real_directory(Path(native_run))
            bound_run = workspace_verify["binding"].get("run")
            require(isinstance(bound_run, str), "native binding has no original run")
            require(_real_directory(Path(bound_run)) == selected_run,
                    "selected run differs from private-binding run")
            packet_path, native_contract = rc005_review.verify_native_source(
                selected_run, root)
            require(packet_path.read_bytes() == workspace_verify["packet_bytes"],
                    "native packet bytes differ from selected run")
            require(native_contract == workspace_verify["contract_sha256"],
                    "native contract differs from selected run")
        reviews = rc005_review.load_reviews(workspace_verify)
        verification = {
            "canonical_verifier": "tools.rc005_review.load_workspace",
            "native_verifier": (
                "tools.rc005_review.verify_native_source"
                if native_binding else None),
            "review_verifier": "tools.rc005_review.load_reviews",
            "source_binding": "verified-now",
            "native_run_reverified": native_binding,
            "native_run": str(selected_run) if native_binding else None,
            "original_native_binding": (
                "verified-from-private-binding"
                if native_binding
                else "not-applicable"),
        }
        for name in sorted(COMMON_FILES):
            files.append(_member(root / name))
        for name in ("drafts", "judgments"):
            for item in _inventory(root, name):
                item["name"] = name + "/" + item["name"]
                files.append(item)
        frozen_verification = {
            "packet_sha256": workspace_verify["packet_sha256"],
            "contract_sha256": workspace_verify["contract_sha256"],
            "practice_only": workspace_verify["practice_only"],
            "review_judgments": len(reviews),
            "review_heads": len(rc005_review.current_heads(reviews)),
        }
    else:
        require({item.name for item in root.iterdir()} <=
                FUTURE_DIRS | {"hidden"},
                "future-question inventory changed")
        future_review.inspect_packet(root)
        verification = {
            "canonical_verifier": "tools.future_question_review.inspect_packet",
            "source_binding": "verified-now",
            "native_run_reverified": False,
        }
        for name in ("hidden", "inputs", "responses", "reviews", "review-keys"):
            require((root / name).is_dir() and not (root / name).is_symlink(),
                    "future-question inventory directory is invalid")
            for item in _inventory(root, name):
                item["name"] = name + "/" + item["name"]
                files.append(item)
        packet = future_review.inspect_packet(root)
        frozen_verification = {
            "history_sha256": packet["manifest"]["history_sha256"],
            "contract_sha256": packet["manifest"]["contract_sha256"],
            "inputs": len(packet["by_id"]),
        }

    frozen_artifact = _freeze_files(lab, files, command_id, format_id)
    body = {
        "format": SOURCE_FORMAT,
        "legacy_format": format_id,
        "artifact_digest": frozen_artifact["artifact_digest"],
        "verification": verification,
        "frozen_verification": frozen_verification,
        "inventory": [{"name": item["name"], "sha256": item["sha256"],
                       "size": item["size"],
                       "artifact_digest": item["artifact_digest"]}
                      for item in frozen_artifact["files"]],
    }
    source_metadata_sha256 = future_review.digest(canonical({
        key: value for key, value in body.items()
        if key != "artifact_digest"
    }))
    manifest = json.loads(
        lab.read_artifact(frozen_artifact["artifact_digest"]).decode("utf-8"))
    manifest["source_metadata_sha256"] = source_metadata_sha256
    stored = lab.command(
        "artifact.put",
        {"text": canonical(manifest).decode("utf-8"),
         "media_type": "application/json"},
        command_id + ":bound-manifest")
    body["artifact_digest"] = stored["digest"]
    body["source_metadata_sha256"] = source_metadata_sha256
    return _register(lab, "Legacy compatibility source", body,
                     command_id + ":object")


def read_legacy(lab, object_id: str) -> dict[str, Any]:
    """Verify and read frozen materials without consulting a live source."""
    source = lab.get_object(object_id)
    require(source.get("kind") == "source", "legacy source object has wrong kind")
    body = source.get("body")
    require(isinstance(body, dict) and body.get("format") == SOURCE_FORMAT,
            "legacy source format changed")
    digest = body.get("artifact_digest")
    require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest),
            "legacy source has no artifact digest")
    raw = lab.read_artifact(digest)
    frozen = json.loads(raw.decode("utf-8"))
    require(frozen.get("format") == BUNDLE_FORMAT and
            frozen.get("legacy_format") == body.get("legacy_format"),
            "legacy artifact identity changed")
    without_digest = {key: value for key, value in body.items()
                      if key not in {"artifact_digest",
                                     "source_metadata_sha256"}}
    require(frozen.get("source_metadata_sha256") ==
            future_review.digest(canonical(without_digest)) and
            body.get("source_metadata_sha256") ==
            frozen.get("source_metadata_sha256"),
            "legacy source body differs from frozen metadata")
    files = frozen.get("files")
    require(isinstance(files, list) and files, "legacy artifact inventory is empty")
    seen = set()
    for item in files:
        require(isinstance(item, dict) and
                set(item) == {"name", "media_type", "size", "sha256",
                              "artifact_digest"},
                "legacy artifact member is malformed")
        name = item["name"]
        require(isinstance(name, str) and name and not name.startswith("/") and
                ".." not in Path(name).parts and name not in seen,
                "legacy artifact member path is unsafe or duplicated")
        seen.add(name)
        encoded = lab.read_artifact(item["artifact_digest"])
        require(len(encoded) == item["size"] and
                future_review.digest(encoded) == item["sha256"],
                "legacy artifact member digest changed")
    expected = {item["name"]: item["sha256"] for item in body["inventory"]}
    expected_digests = {item["name"]: item["artifact_digest"]
                        for item in body["inventory"]}
    require(expected == {item["name"]: item["sha256"] for item in files} and
            expected_digests == {item["name"]: item["artifact_digest"]
                                 for item in files},
            "legacy artifact inventory differs from its source object")
    return {"format": SOURCE_FORMAT, "legacy_format": body["legacy_format"],
            "verification": body["verification"],
            "frozen_verification": body["frozen_verification"],
            "files": {item["name"]: lab.read_artifact(
                item["artifact_digest"]).decode("utf-8") for item in files}}
