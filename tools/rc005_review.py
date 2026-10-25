#!/usr/bin/env python3
"""Offline first-blind-pass RC-005 review workspace; no runtime or provider access."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "case-lab" / "reviews" / "rc005-review-contract.json"
WORKSPACE_FORMAT = "rc005-review-workspace-1"
PRIVATE_BINDING_FORMAT = "rc005-review-private-binding-1"
SNAPSHOT_FORMAT = "rc005-review-source-snapshot-1"
MARKDOWN_FORMAT = "rc005-review-report-markdown-1"
JSON_FORMAT = "rc005-review-report-1"
MAX_CONTRACT_BYTES = 1_000_000

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "experiments"))
import rc005_native as study
from tools import continuity_inputs as continuity


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def exact_bytes(path: Path, label: str, limit: int) -> bytes:
    require(not path.is_symlink() and path.is_file(), f"{label} is missing or is a symlink")
    data = path.read_bytes()
    require(len(data) <= limit, f"{label} exceeds byte limit")
    return data


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decoded_object(data: bytes, label: str) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            require(key not in result, f"{label} contains a duplicate JSON field")
            result[key] = value
        return result

    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=unique)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{label} is not valid UTF-8 JSON") from error
    require(isinstance(value, dict), f"{label} must be a JSON object")
    return value


def field_set(value: Any, fields: list[str] | tuple[str, ...], label: str) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) == set(fields),
            f"{label} has unknown or missing fields")
    return value


def string(value: Any, label: str, maximum: int, *, nonblank: bool = True) -> str:
    require(isinstance(value, str), f"{label} must be text")
    require(len(value) <= maximum, f"{label} exceeds character limit")
    if nonblank:
        require(bool(value.strip()), f"{label} must not be blank")
    return value


def option_values(entries: list[dict[str, Any]]) -> set[str]:
    return {entry["value"] for entry in entries}


def load_contract() -> tuple[dict[str, Any], bytes, str]:
    data = exact_bytes(CONTRACT, "review contract", MAX_CONTRACT_BYTES)
    value = decoded_object(data, "review contract")
    require(value.get("format") == "rc005-review-contract-1", "unsupported review contract")
    require(value.get("revision") == "continuity-development-2026-10-25",
            "unsupported review contract revision")
    require(value.get("status") == "development-worksheet-not-accepted-rubric",
            "review contract status changed")
    require(value.get("review_pass") == "blind", "review contract allows a non-blind pass")
    require(value.get("batch_format") == "rc005-review-batch-1", "batch format changed")
    require(value.get("draft_format") == "rc005-review-draft-1", "draft format changed")
    require(value.get("packet_format") == "review-packet-1", "packet format changed")
    require(value.get("max_packet_bytes") == 8_388_608, "packet byte limit changed")
    dimensions = {item["id"]: item for item in value["dimensions"]}
    require(set(dimensions) == {
        "claims", "current_action", "clarification", "selective_use",
        "confidence_limits", "guessability", "guess_confidence",
    }, "review dimensions changed")
    return value, data, digest(data)


def safe_directory(path: Path, label: str, *, may_be_absent: bool = False) -> Path:
    absolute = path.expanduser().absolute()
    require(not any(parent.is_symlink() for parent in (absolute, *absolute.parents)),
            f"{label} path may not contain symlinks")
    if may_be_absent and not absolute.exists():
        require(absolute.parent.is_dir(), f"{label} parent must exist")
        return absolute
    require(absolute.is_dir(), f"{label} must be a directory")
    return absolute


def owned_new_directory(path: Path) -> Path:
    absolute = path.expanduser().absolute()
    require(not any(parent.is_symlink() for parent in (absolute, *absolute.parents)),
            "output path may not contain symlinks")
    require(absolute.parent.is_dir(), "output parent must already exist")
    require(not absolute.exists(), "output directory already exists")
    absolute.mkdir(mode=0o700)
    return absolute


def write_new(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def packet_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def parse_iso(value: Any) -> None:
    text = string(value, "created_at", 40)
    require(re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z",
                         text) is not None, "created_at must be an ISO UTC timestamp")
    try:
        datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("created_at is not a real UTC timestamp") from error


def validate_packet(value: Any, contract: dict[str, Any], *, practice: bool) -> dict[str, Any]:
    field_set(value, {"format", "review_status", "items"}, "review packet")
    require(value.get("format") == contract["packet_format"], "unsupported review packet format")
    require(value.get("review_status") == "unreviewed", "review packet is not unreviewed")
    require(isinstance(value.get("items"), list) and value["items"],
            "review packet must contain items")
    expected = set(continuity.REVIEW_FIELDS) | {"review_id", "response_state"}
    seen = set()
    for index, item in enumerate(value["items"]):
        field_set(item, sorted(expected), f"packet item {index}")
        review_id = item["review_id"]
        require(isinstance(review_id, str) and
                re.fullmatch(r"[0-9a-f]{32}", review_id), "packet review ID is invalid")
        require(review_id not in seen, "packet review IDs are duplicated")
        seen.add(review_id)
        require(item["review_status"] == "unreviewed", "packet item is not unreviewed")
        state = item["response_state"]
        require(state in {"complete", "technical-failure"}, "packet response state is invalid")
        if state == "complete":
            require(isinstance(item["response"], str), "complete response must be text")
        else:
            require(item["response"] is None,
                    "technical failure must have a null response")
        string(item["context"], "packet context", 65_536)
        string(item["instructions"], "packet instructions", 10_000)
        require(isinstance(item["governing_history"], list), "governing history must be a list")
        for event in item["governing_history"]:
            field_set(event, continuity.HISTORY_FIELDS, "governing history event")
        field_set(item["current"], {"surface", "text"}, "current turn")
        string(item["current"]["surface"], "current surface", 1_000)
        string(item["current"]["text"], "current text", 65_536)
    if not practice:
        require(len(value["items"]) == 144, "native review packet must contain exactly 144 items")
    return value


def packet_items(packet: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["review_id"]: item for item in packet["items"]}


def reviewable(item: dict[str, Any]) -> bool:
    return item["response_state"] == "complete"


def scan_batches(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    require(folder.is_dir() and not folder.is_symlink(), "judgment directory is invalid")
    for path in folder.iterdir():
        if path.name.startswith("."):
            require(path.is_file() and not path.is_symlink(),
                    "judgment temporary residue is invalid")
    paths = sorted(path for path in folder.iterdir()
                   if not path.name.startswith("."))
    for index, path in enumerate(paths, 1):
        require(path.is_file() and not path.is_symlink() and
                path.name == f"{index:06d}.json", "judgment batches are not append-only numbered files")
    return paths


def read_snapshot(workspace: Path) -> dict[str, Any]:
    return decoded_object(exact_bytes(workspace / "source-snapshot.json",
                                     "saved source snapshot", 16_777_216),
                          "saved source snapshot")


def verify_snapshot(value: dict[str, Any], contract_sha: str, packet_sha: str) -> None:
    require(value.get("format") == SNAPSHOT_FORMAT, "source snapshot format changed")
    require(value.get("contract_sha256") == contract_sha, "source snapshot contract changed")
    require(value.get("packet_sha256") == packet_sha, "source snapshot packet changed")
    require(isinstance(value.get("items"), dict) and value["items"], "source snapshot has no items")
    for identifier, item in value["items"].items():
        require(isinstance(identifier, str) and re.fullmatch(r"[0-9a-f]{32}", identifier),
                "source snapshot contains an invalid review ID")
        require(isinstance(item, dict) and isinstance(item.get("body"), dict),
                "source snapshot item is malformed")


def load_workspace(path: Path, *, verify_run: bool = True) -> dict[str, Any]:
    workspace = safe_directory(path, "workspace")
    require({item.name for item in workspace.iterdir()} ==
            {"review-packet.json", "contract.json", "source-snapshot.json", "private-binding.json",
             "drafts", "judgments"},
            "workspace inventory changed")
    contract, _, contract_sha = load_contract()
    saved_contract = exact_bytes(workspace / "contract.json", "saved contract", MAX_CONTRACT_BYTES)
    require(saved_contract == CONTRACT.read_bytes(), "workspace contract differs from shared contract")
    packet_raw = exact_bytes(workspace / "review-packet.json", "review packet",
                             contract["max_packet_bytes"])
    packet_sha = digest(packet_raw)
    packet = decoded_object(packet_raw, "review packet")
    binding = decoded_object(exact_bytes(workspace / "private-binding.json",
                                        "private binding", 1_000_000), "private binding")
    require(binding.get("format") == PRIVATE_BINDING_FORMAT, "private binding format changed")
    require(binding.get("contract_sha256") == contract_sha, "private binding contract changed")
    require(binding.get("packet_sha256") == packet_sha, "private binding packet changed")
    practice = binding.get("practice_only")
    require(isinstance(practice, bool), "private binding practice flag is invalid")
    validate_packet(packet, contract, practice=practice)
    snapshot = read_snapshot(workspace)
    verify_snapshot(snapshot, contract_sha, packet_sha)
    require(binding.get("source_snapshot_sha256") == digest(canonical(snapshot)),
            "private binding source snapshot changed")
    require(set(snapshot["items"]) == set(packet_items(packet)),
            "source snapshot IDs differ from review packet")
    for item in packet["items"]:
        saved = snapshot["items"][item["review_id"]]
        require(saved.get("response_state") == item["response_state"] and
                saved.get("body") == item,
                "source snapshot body differs from review packet")
    if verify_run and not practice:
        run = binding.get("run")
        require(isinstance(run, str) and Path(run).is_absolute() and
                Path(run).resolve().is_dir(), "bound native run is missing")
        try:
            native_packet, native_contract = verify_native_source(Path(run), workspace)
        except Exception as error:
            raise ValueError(f"native run verification failed: {error}") from error
        require(native_packet.read_bytes() == packet_raw, "native packet bytes changed")
        require(native_contract == contract_sha, "native source no longer matches contract")
        # The saved snapshot was tied to each packet item above; the pure
        # native verifier already re-derived the same packet through the
        # original map and operations. Do not read that source a second time.
    return {
        "workspace": workspace, "contract": contract, "contract_sha256": contract_sha,
        "packet": packet, "packet_bytes": packet_raw, "packet_sha256": packet_sha,
        "binding": binding, "snapshot": snapshot, "practice_only": practice,
    }


def verify_native_source(run: Path, workspace: Path | None = None) -> tuple[Path, str]:
    require(run.is_dir() and not run.is_symlink(), "native run is not a directory")
    contract, _, contract_sha = load_contract()
    packet_path = run / "review-packet.json"
    require(packet_path.exists(), "native run has no existing review packet")
    snapshots = study.review_snapshot(run)
    _, expected_packet = study.bind_review_map(snapshots, run)
    packet_raw = exact_bytes(packet_path, "native review packet", contract["max_packet_bytes"])
    require(packet_raw == study.dump(expected_packet).encode("utf-8") + b"\n",
            "native review packet bytes/source differ from the closed run")
    if workspace is not None:
        require((workspace / "review-packet.json").read_bytes() == packet_raw,
                "workspace packet differs from native export")
    return packet_path, contract_sha


def validate_review(record: dict[str, Any], item: dict[str, Any], contract: dict[str, Any],
                    *, reviewer_id: str, rubric_revision: str, review_pass: str,
                    practice_only: bool) -> None:
    limits = contract["limits"]
    string(reviewer_id, "reviewer_id", limits["reviewer_id"])
    require(rubric_revision == contract["revision"], "review rubric changed")
    require(review_pass == "blind", "only blind reviews are accepted")
    require(isinstance(practice_only, bool), "practice flag is not boolean")
    require(reviewable(item), "technical failure and non-complete responses are not reviewable")
    response = item["response"]
    claims = record["claims"]
    require(isinstance(claims, list), "claims must be a list")
    if response.strip():
        require(bool(claims), "nonblank response needs at least one claim")
    else:
        require(not claims, "blank response must have no claims")
    claim_fields = {"quote", "kind", "attribution", "support", "evidence_refs", "rationale"}
    kinds = option_values(contract["claim_kind_options"])
    supports = option_values(contract["claim_support_options"])
    refs_allowed = {"current"} | {f"H{index}" for index in range(1, len(item["governing_history"]) + 1)}
    for claim in claims:
        field_set(claim, claim_fields, "claim")
        quote = string(claim["quote"], "claim quote", limits["quote"])
        require(quote in response, "claim quote is not an exact response substring")
        kind = claim["kind"]
        support = claim["support"]
        require(isinstance(kind, str) and kind in kinds, "claim kind is not allowed")
        require(isinstance(support, str) and support in supports,
                "claim support is not allowed")
        string(claim["attribution"], "claim attribution", limits["attribution"])
        string(claim["rationale"], "claim rationale", limits["claim_rationale"])
        refs = claim["evidence_refs"]
        require(isinstance(refs, list) and
                all(isinstance(ref, str) for ref in refs) and
                len(refs) == len(set(refs)) and set(refs) <= refs_allowed,
                "claim evidence refs are invalid")
        if support in {"supported", "contradicted"}:
            require(bool(refs), "supported or contradicted claim requires evidence refs")
    dimensions = {entry["id"]: entry for entry in contract["dimensions"]}
    for field in ("current_action", "clarification", "selective_use",
                  "confidence_limits", "guessability", "guess_confidence"):
        require(isinstance(record[field], str) and
                record[field] in option_values(dimensions[field]["options"]),
                f"{field} is not an allowed option")
    cue = string(record["guess_cue"], "guess cue", limits["guess_cue"], nonblank=False)
    if record["guessability"] != "cannot-tell":
        require(bool(cue.strip()), "a positive condition guess needs a cue")
    string(record["rationale"], "overall rationale", limits["rationale"])
    string(record["notes"], "notes", limits["notes"], nonblank=False)


def load_reviews(workspace: dict[str, Any]) -> list[dict[str, Any]]:
    records = []
    seen_ids = set()
    contract = workspace["contract"]
    items = packet_items(workspace["packet"])
    for path in scan_batches(workspace["workspace"] / "judgments"):
        raw = exact_bytes(path, "review batch", 16_777_216)
        batch = decoded_object(raw, "review batch")
        field_set(batch, [entry["id"] for entry in contract["batch_fields"]], "review batch")
        require(batch["format"] == contract["batch_format"], "unsupported review batch format")
        require(batch["packet_sha256"] == workspace["packet_sha256"], "review batch packet changed")
        require(batch["contract_sha256"] == workspace["contract_sha256"], "review batch contract changed")
        require(batch["rubric_revision"] == contract["revision"], "review batch rubric changed")
        require(batch["review_pass"] == "blind", "review batch pass changed")
        require(batch["practice_only"] is workspace["practice_only"],
                "review batch practice flag changed")
        string(batch["reviewer_id"], "batch reviewer_id", contract["limits"]["reviewer_id"])
        require(isinstance(batch["records"], list) and batch["records"], "review batch is empty")
        for record in batch["records"]:
            field_set(record, [entry["id"] for entry in contract["record_fields"]], "review record")
            identifier = record["judgment_id"]
            require(isinstance(identifier, str) and re.fullmatch(r"[0-9a-f]{32}", identifier)
                    and identifier not in seen_ids, "judgment ID is invalid or duplicated")
            seen_ids.add(identifier)
            require(record["review_id"] in items, "judgment names an unknown review ID")
            parse_iso(record["created_at"])
            normalized = dict(record, reviewer_id=batch["reviewer_id"],
                              rubric_revision=batch["rubric_revision"],
                              review_pass=batch["review_pass"],
                              practice_only=batch["practice_only"])
            validate_review(
                normalized, items[record["review_id"]], contract,
                reviewer_id=batch["reviewer_id"],
                rubric_revision=batch["rubric_revision"],
                review_pass=batch["review_pass"],
                practice_only=batch["practice_only"],
            )
            records.append(normalized)
    validate_chains(records)
    return records


def validate_chains(records: list[dict[str, Any]]) -> None:
    by_id = {}
    keys = {}
    for record in records:
        identifier = record["judgment_id"]
        require(isinstance(identifier, str) and
                re.fullmatch(r"[0-9a-f]{32}", identifier) and
                identifier not in by_id, "judgment ID is invalid or duplicated")
        by_id[identifier] = record
        keys[identifier] = (record["review_id"], record["reviewer_id"],
                            record["rubric_revision"], record["review_pass"])
    for identifier, record in by_id.items():
        supersedes = record["supersedes"]
        if supersedes is None:
            continue
        require(isinstance(supersedes, str) and supersedes in by_id,
                "judgment supersedes an unknown ID")
        require(keys[supersedes] == keys[identifier],
                "judgment supersedes across item, reviewer, rubric or pass")
    current: dict[tuple[str, str, str, str], str] = {}
    roots: dict[tuple[str, str, str, str], int] = {}
    for record in records:
        identifier = record["judgment_id"]
        key = keys[identifier]
        supersedes = record["supersedes"]
        if supersedes is None:
            roots[key] = roots.get(key, 0) + 1
            require(roots[key] == 1, "judgment chain has multiple roots")
            require(record["amendment_reason"] == "",
                    "first judgment must have an empty amendment reason")
        else:
            require(supersedes == current.get(key),
                    "judgment supersedes a stale or disconnected head")
            string(record["amendment_reason"], "amendment reason",
                   record_contract_limit(record, "rationale"))
        current[key] = identifier
    require(all(roots.get(key) == 1 for key in current),
            "judgment chain has no root")


def record_contract_limit(record: dict[str, Any], field: str) -> int:
    # amendment_reason shares the bounded rationale allowance.
    return 20_000


def private_binding(run: Path | None, packet_raw: bytes, contract_sha: str,
                    snapshot: dict[str, Any], practice: bool) -> dict[str, Any]:
    return {
        "format": PRIVATE_BINDING_FORMAT,
        "practice_only": practice,
        "run": str(run) if run is not None else None,
        "packet_sha256": digest(packet_raw),
        "contract_sha256": contract_sha,
        "source_snapshot_sha256": digest(canonical(snapshot)),
    }


def make_snapshot(packet: dict[str, Any], contract_sha: str, packet_sha: str) -> dict[str, Any]:
    return {
        "format": SNAPSHOT_FORMAT,
        "contract_sha256": contract_sha,
        "packet_sha256": packet_sha,
        "items": {
            item["review_id"]: {
                "body": dict(item), "response_state": item["response_state"],
            }
            for item in packet["items"]
        },
    }


def prepare(run: Path, output: Path) -> dict[str, Any]:
    run = safe_directory(run, "native run")
    contract, contract_raw, contract_sha = load_contract()
    packet_path, _ = verify_native_source(run)
    packet_raw = exact_bytes(packet_path, "native review packet", contract["max_packet_bytes"])
    packet = decoded_object(packet_raw, "native review packet")
    validate_packet(packet, contract, practice=False)
    snapshot = make_snapshot(packet, contract_sha, digest(packet_raw))
    folder = owned_new_directory(output)
    try:
        (folder / "drafts").mkdir(mode=0o700)
        (folder / "judgments").mkdir(mode=0o700)
        write_new(folder / "contract.json", contract_raw)
        write_new(folder / "review-packet.json", packet_raw)
        write_new(folder / "source-snapshot.json", canonical(snapshot))
        write_new(folder / "private-binding.json",
                  canonical(private_binding(run, packet_raw, contract_sha, snapshot, False)))
    except BaseException:
        # Preserve the partial directory for explicit diagnosis; do not advertise it as valid.
        raise
    return {"status": "prepared", "practice_only": False, "workspace": str(folder),
            "packet_sha256": digest(packet_raw), "contract_sha256": contract_sha,
            "items": len(packet["items"])}


def prepare_practice(packet_file: Path, output: Path) -> dict[str, Any]:
    contract, contract_raw, contract_sha = load_contract()
    raw = exact_bytes(packet_file, "practice packet", contract["max_packet_bytes"])
    wrapper = decoded_object(raw, "practice wrapper")
    require(set(wrapper) == {"practice_only", "packet"}, "practice wrapper fields changed")
    require(wrapper["practice_only"] is True, "practice wrapper must be explicitly practice-only")
    packet = validate_packet(wrapper["packet"], contract, practice=True)
    packet_raw = packet_bytes(packet)
    require(len(packet_raw) <= contract["max_packet_bytes"], "practice packet exceeds byte limit")
    snapshot = make_snapshot(packet, contract_sha, digest(packet_raw))
    folder = owned_new_directory(output)
    (folder / "drafts").mkdir(mode=0o700)
    (folder / "judgments").mkdir(mode=0o700)
    write_new(folder / "contract.json", contract_raw)
    write_new(folder / "review-packet.json", packet_raw)
    write_new(folder / "source-snapshot.json", canonical(snapshot))
    write_new(folder / "private-binding.json",
              canonical(private_binding(None, packet_raw, contract_sha, snapshot, True)))
    return {"status": "prepared-practice", "practice_only": True, "workspace": str(folder),
            "packet_sha256": digest(packet_raw), "contract_sha256": contract_sha,
            "items": len(packet["items"]), "warning":
            "authored practice only; not a run, system result, or human calibration"}


def verify(path: Path) -> dict[str, Any]:
    workspace = load_workspace(path)
    reviews = load_reviews(workspace)
    heads = current_heads(reviews)
    return {
        "status": "valid", "practice_only": workspace["practice_only"],
        "packet_sha256": workspace["packet_sha256"],
        "contract_sha256": workspace["contract_sha256"],
        "positions": len(workspace["packet"]["items"]),
        "reviewable": sum(reviewable(item) for item in workspace["packet"]["items"]),
        "judgments": len(reviews), "current_heads": len(heads),
        "warnings": [
            "development worksheet; not an accepted rubric or human calibration",
            "source identity proves only closure to the saved export, not authenticity",
        ],
    }


def current_heads(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    superseded = {record["supersedes"] for record in records if record["supersedes"]}
    return [record for record in records if record["judgment_id"] not in superseded]

def wire_record(record: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    return {entry["id"]: record[entry["id"]]
            for entry in contract["record_fields"]}

def comparable_record(record: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    return dict(wire_record(record, contract), reviewer_id=record["reviewer_id"],
                rubric_revision=record["rubric_revision"],
                review_pass=record["review_pass"])


def import_review(path: Path, source_file: Path) -> dict[str, Any]:
    workspace = load_workspace(path)
    contract = workspace["contract"]
    raw = exact_bytes(source_file, "review import", 16_777_216)
    batch = decoded_object(raw, "review import")
    field_set(batch, [entry["id"] for entry in contract["batch_fields"]], "review import")
    existing = load_reviews(workspace)
    expected = workspace["packet_sha256"]
    require(batch["format"] == contract["batch_format"], "unsupported review batch")
    require(batch["packet_sha256"] == expected, "review batch packet changed")
    require(batch["contract_sha256"] == workspace["contract_sha256"], "review batch contract changed")
    require(batch["rubric_revision"] == contract["revision"], "review batch rubric changed")
    require(batch["review_pass"] == "blind", "review batch pass changed")
    require(batch["practice_only"] is workspace["practice_only"], "batch practice flag changed")
    string(batch["reviewer_id"], "batch reviewer_id", contract["limits"]["reviewer_id"])
    require(isinstance(batch["records"], list) and batch["records"], "empty review batch")
    existing_by_id = {record["judgment_id"]: record for record in existing}
    submitted_ids = set()
    normalized_records = []
    for record in batch["records"]:
        field_set(record, [entry["id"] for entry in contract["record_fields"]], "review record")
        identifier = record["judgment_id"]
        require(isinstance(identifier, str) and
                re.fullmatch(r"[0-9a-f]{32}", identifier) is not None,
                "judgment ID is invalid")
        require(identifier not in submitted_ids, "judgment ID is duplicated in import")
        submitted_ids.add(identifier)
        require(record["review_id"] in packet_items(workspace["packet"]),
                "judgment names unknown review ID")
        parse_iso(record["created_at"])
        normalized = dict(record, reviewer_id=batch["reviewer_id"],
                          rubric_revision=batch["rubric_revision"],
                          review_pass=batch["review_pass"],
                          practice_only=batch["practice_only"])
        validate_review(
            normalized, packet_items(workspace["packet"])[record["review_id"]], contract,
            reviewer_id=batch["reviewer_id"],
            rubric_revision=batch["rubric_revision"],
            review_pass=batch["review_pass"],
            practice_only=batch["practice_only"],
        )
        normalized_records.append(normalized)
    known_records, new_records = [], []
    for record in normalized_records:
        previous = existing_by_id.get(record["judgment_id"])
        if previous is not None:
            require(comparable_record(previous, contract) == comparable_record(record, contract),
                    "known judgment ID changed content or owner")
            known_records.append(record)
        else:
            new_records.append(record)
    # Cumulative browser journals group each item's history together. A new
    # amendment can precede an unchanged record from another item. Existing
    # records are compared, never reordered or rewritten; only new records
    # advance their authoritative per-item chains below.
    validate_chains(existing + new_records)
    if not new_records:
        return {"status": "already-imported", "practice_only": workspace["practice_only"],
                "batch": None, "records": 0, "judgments": len(existing),
                "recognized_records": len(known_records)}
    new_batch = dict(batch, records=[wire_record(record, contract) for record in new_records])
    candidate_raw = canonical(new_batch)
    folder = workspace["workspace"] / "judgments"
    seq = len(scan_batches(folder)) + 1
    target = folder / f"{seq:06d}.json"
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=folder,
                                         prefix=f".{seq:06d}.", suffix=".tmp",
                                         delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(candidate_raw)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, target)
        except FileExistsError as error:
            raise ValueError("numbered judgment batch already exists") from error
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return {"status": "imported", "practice_only": workspace["practice_only"],
            "batch": target.name, "records": len(new_records),
            "judgments": len(existing) + len(new_records)}


def markdown_text(value: str) -> str:
    """Keep reviewer/response text literal when a private report is rendered."""
    escaped = html.escape(value, quote=False)
    escaped = re.sub(r"([\\`*_{}\[\]()!|])", r"\\\1", escaped)
    return escaped.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def report(path: Path, fmt: str) -> tuple[dict[str, Any] | str, str]:
    workspace = load_workspace(path)
    reviews = load_reviews(workspace)
    heads = current_heads(reviews)
    items = workspace["packet"]["items"]
    dimensions = {entry["id"]: entry for entry in workspace["contract"]["dimensions"]}
    completed = sum(item["response_state"] == "complete" for item in items)
    empty = sum(item["response"] == "" for item in items)
    whitespace = sum(bool(item["response"]) and not item["response"].strip()
                     for item in items if item["response_state"] == "complete")
    technical = sum(item["response_state"] == "technical-failure" for item in items)
    reviewed = {record["review_id"] for record in heads if reviewable(packet_items(workspace["packet"])[record["review_id"]])}
    distributions = {}
    for field in ("current_action", "clarification", "selective_use",
                  "confidence_limits", "guessability", "guess_confidence"):
        counts = Counter(record[field] for record in heads)
        distributions[field] = {option["value"]: counts[option["value"]]
                                for option in dimensions[field]["options"]}
    claims = Counter()
    support = Counter()
    reviewer_history = {}
    reviewer_current = {}
    for record in heads:
        for claim in record["claims"]:
            claims[claim["kind"]] += 1
            support[claim["support"]] += 1
    for record in reviews:
        reviewer_history.setdefault(record["reviewer_id"], set()).add(record["review_id"])
    for record in heads:
        reviewer_current.setdefault(record["reviewer_id"], set()).add(record["review_id"])
    groups = {}
    for record in heads:
        groups.setdefault(record["review_id"], []).append(record)
    differences = []
    claim_differences = []
    for review_id, group in sorted(groups.items()):
        if len({record["reviewer_id"] for record in group}) > 1:
            dimensions_group = {
                field: sorted({record[field] for record in group})
                for field in ("current_action", "clarification", "selective_use",
                              "confidence_limits", "guessability", "guess_confidence")
            }
            if any(len(values) > 1 for values in dimensions_group.values()):
                differences.append({
                    "review_id": review_id, "reviewers": sorted(
                        record["reviewer_id"] for record in group),
                    "dimension_values": dimensions_group,
                })
            claim_value = {
                record["reviewer_id"]: [
                    {
                        "quote": claim["quote"], "kind": claim["kind"],
                        "attribution": claim["attribution"],
                        "support": claim["support"],
                        "evidence_refs": claim["evidence_refs"],
                        "rationale": claim["rationale"],
                    }
                    for claim in record["claims"]
                ]
                for record in group
            }
            if len({json.dumps(value, ensure_ascii=False, sort_keys=True)
                    for value in claim_value.values()}) > 1:
                claim_differences.append({
                    "review_id": review_id,
                    "by_reviewer": claim_value,
                })
    current_judgments = [
        {
            "review_id": record["review_id"],
            "reviewer_id": record["reviewer_id"],
            "judgment_id": record["judgment_id"],
            "supersedes": record["supersedes"],
            "amendment_reason": record["amendment_reason"],
            "created_at": record["created_at"],
            "claims": record["claims"],
            "current_action": record["current_action"],
            "clarification": record["clarification"],
            "selective_use": record["selective_use"],
            "confidence_limits": record["confidence_limits"],
            "guessability": record["guessability"],
            "guess_confidence": record["guess_confidence"],
            "guess_cue": record["guess_cue"],
            "rationale": record["rationale"],
            "notes": record["notes"],
        }
        for record in heads
    ]
    historical_judgments = [
        {
            "review_id": record["review_id"],
            "reviewer_id": record["reviewer_id"],
            "judgment_id": record["judgment_id"],
            "supersedes": record["supersedes"],
            "amendment_reason": record["amendment_reason"],
            "created_at": record["created_at"],
            "claims": record["claims"],
            "current_action": record["current_action"],
            "clarification": record["clarification"],
            "selective_use": record["selective_use"],
            "confidence_limits": record["confidence_limits"],
            "guessability": record["guessability"],
            "guess_confidence": record["guess_confidence"],
            "guess_cue": record["guess_cue"],
            "rationale": record["rationale"],
            "notes": record["notes"],
        }
        for record in reviews
    ]
    value = {
        "format": JSON_FORMAT,
        "status": "development-descriptive-report",
        "practice_only": workspace["practice_only"],
        "packet_sha256": workspace["packet_sha256"],
        "contract_sha256": workspace["contract_sha256"],
        "rubric_revision": workspace["contract"]["revision"],
        "review_pass": "blind",
        "source_binding": {
            "kind": "practice-fixture" if workspace["practice_only"] else "native-closed-export",
            "original_run_required": not workspace["practice_only"],
            "authenticity": "not established beyond closed run/export source identity",
        },
        "counts": {
            "positions": len(items), "completed_text": completed,
            "empty_completed": empty, "whitespace_completed": whitespace,
            "technical_failures": technical,
            "reviewable": completed, "reviewed_current": len(reviewed),
            "unreviewed_current": completed - len(reviewed),
            "historical_judgments": len(reviews), "current_judgments": len(heads),
            "reviewers_seen": len(reviewer_history),
            "reviewers_current": len(reviewer_current),
        },
        "distributions": distributions,
        "claims": {"kind": dict(claims), "support": dict(support)},
        "reviewers": {
            reviewer: {
                "historical_positions": len(reviewer_history[reviewer]),
                "current_positions": len(reviewer_current.get(reviewer, set())),
            }
            for reviewer in sorted(reviewer_history)
        },
        "multi_reviewer_differences": differences,
        "claim_interpretation_differences": claim_differences,
        "current_judgments": current_judgments,
        "historical_judgments": historical_judgments,
        "history": [
            {key: record[key] for key in (
                "judgment_id", "review_id", "reviewer_id", "supersedes",
                "amendment_reason", "created_at", "rubric_revision", "review_pass")}
            for record in reviews
        ],
        "limits": [
            "development worksheet judgments; no accepted rubric",
            "technical failures are non-semantic and excluded",
            "raw counts and disagreement only; no accuracy, quality, ranking or calibration",
            "condition guessability is a blinding diagnostic, not quality",
        ],
    }
    if fmt == "json":
        return value, "json"
    require(fmt == "markdown", "report format must be json or markdown")
    lines = [
        "# RC-005 首次盲评描述性报告",
        "",
        f"**状态：** {value['status']}；开发工作表，不是已接受量表或人类校准结论。",
        f"**范围：** {'作者练习，不绑定真实运行' if workspace['practice_only'] else '已关闭原生导出的绑定工作区'}。",
        f"**包字节：** `{value['packet_sha256']}`",
        f"**契约字节：** `{value['contract_sha256']}`",
        "",
        "## 完成与覆盖",
        "",
        "| 指标 | 数量 |",
        "|---|---:|",
    ]
    for key, count in value["counts"].items():
        lines.append(f"| `{key}` | {count} |")
    lines += ["", "## 当前判断分布", ""]
    for field, counts in distributions.items():
        lines.append(f"### `{field}`")
        lines.append("")
        lines.append("| 选项 | 当前判断数 |")
        lines.append("|---|---:|")
        for option in dimensions[field]["options"]:
            lines.append(f"| `{option['value']}` {option['label']} | {counts[option['value']]} |")
        lines.append("")
    lines += ["## 论断检查", "", "| 维度 | 值 | 数量 |", "|---|---|---:|"]
    for kind, count in sorted(claims.items()):
        lines.append(f"| kind | `{kind}` | {count} |")
    for support_value, count in sorted(support.items()):
        lines.append(f"| support | `{support_value}` | {count} |")
    lines += ["", "## 评审者", "",
              "| 评审者代号 | 历史判断位置数 | 当前判断位置数 |", "|---|---:|---:|"]
    for reviewer, counts in sorted(value["reviewers"].items()):
        lines.append(f"| {markdown_text(reviewer)} | {counts['historical_positions']} | "
                     f"{counts['current_positions']} |")
    lines += ["", "## 多评审者差异", ""]
    if not differences:
        lines.append("没有记录到当前判断维度差异。")
    else:
        for difference in differences:
            lines.append(f"- `{difference['review_id']}`：" +
                         "; ".join(f"{field}={values}" for field, values in
                                   difference["dimension_values"].items() if len(values) > 1))
    lines += ["", "## 论断解释差异", ""]
    if not claim_differences:
        lines.append("没有记录到当前 claim 级解释差异。")
    else:
        for difference in claim_differences:
            lines.append(f"### `{difference['review_id']}`")
            for reviewer, claims in sorted(difference["by_reviewer"].items()):
                lines.append(f"- {markdown_text(reviewer)}:")
                for claim in claims:
                    lines.append(
                        f"  - {claim['kind']} / {claim['support']} / "
                        f"{markdown_text(claim['attribution'])} / {markdown_text(claim['quote'])} / "
                        f"{claim['evidence_refs']} / {markdown_text(claim['rationale'])}")
                if not claims:
                    lines.append("  - 无 atomic claim（空白或技术状态之外的空表达）")
    lines += ["", "## 当前完整判断", ""]
    for judgment in value["current_judgments"]:
        lines.append(f"### `{judgment['review_id']}` / {markdown_text(judgment['reviewer_id'])}")
        lines.append("")
        lines.append(f"- judgment: `{judgment['judgment_id']}`")
        lines.append(f"- supersedes: `{judgment['supersedes'] or '—'}`")
        lines.append(f"- action={judgment['current_action']}; "
                     f"clarification={judgment['clarification']}; "
                     f"selective_use={judgment['selective_use']}; "
                     f"confidence_limits={judgment['confidence_limits']}")
        lines.append(f"- guess={judgment['guessability']} / {judgment['guess_confidence']}; "
                     f"cue={markdown_text(judgment['guess_cue'])}")
        lines.append(f"- rationale: {markdown_text(judgment['rationale'])}")
        for claim in judgment["claims"]:
            lines.append(f"- claim {claim['kind']} / {claim['support']} / "
                         f"{markdown_text(claim['attribution'])} / “{markdown_text(claim['quote'])}” / "
                         f"{claim['evidence_refs']} / {markdown_text(claim['rationale'])}")
        if judgment["notes"]:
            lines.append(f"- notes: {markdown_text(judgment['notes'])}")
        lines.append("")
    lines += ["## 历史原始判断", "", "| judgment | reviewer | review | supersedes | amendment |",
              "|---|---|---|---|---|"]
    for judgment in value["historical_judgments"]:
        lines.append(f"| `{judgment['judgment_id']}` | {markdown_text(judgment['reviewer_id'])} | "
                     f"`{judgment['review_id']}` | `{judgment['supersedes'] or '—'}` | "
                     f"{markdown_text(judgment['amendment_reason'])} |")
    lines += ["", "## 修订历史", "", "| judgment | review | reviewer | supersedes |",
              "|---|---|---|---|"]
    for historical in value["history"]:
        lines.append(f"| `{historical['judgment_id']}` | `{historical['review_id']}` | "
                     f"`{historical['reviewer_id']}` | `{historical['supersedes'] or '—'}` |")
    lines += ["", "## 边界", ""]
    lines += [f"- {limit}" for limit in value["limits"]]
    lines.append("")
    return "\n".join(lines), "markdown"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_command = commands.add_parser("prepare", help="copy an existing closed native export")
    prepare_command.add_argument("--run", type=Path, required=True)
    prepare_command.add_argument("--output", type=Path, required=True)
    practice_command = commands.add_parser("prepare-practice",
                                           help="prepare the authored public practice wrapper")
    practice_command.add_argument("--packet", type=Path, required=True)
    practice_command.add_argument("--output", type=Path, required=True)
    verify_command = commands.add_parser("verify", help="verify workspace and run-bound source")
    verify_command.add_argument("--workspace", type=Path, required=True)
    import_command = commands.add_parser("import-review", help="append a fully validated review batch")
    import_command.add_argument("--workspace", type=Path, required=True)
    import_command.add_argument("--input", type=Path, required=True)
    report_command = commands.add_parser("report", help="write descriptive JSON or Markdown")
    report_command.add_argument("--workspace", type=Path, required=True)
    report_command.add_argument("--format", choices=("json", "markdown"), default="json")
    report_command.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare(args.run, args.output)
        elif args.command == "prepare-practice":
            result = prepare_practice(args.packet, args.output)
        elif args.command == "verify":
            result = verify(args.workspace)
        elif args.command == "import-review":
            result = import_review(args.workspace, args.input)
        else:
            value, kind = report(args.workspace, args.format)
            if args.output:
                target = args.output.expanduser().absolute()
                require(not any(parent.is_symlink() for parent in (target, *target.parents)),
                        "report output may not contain symlinks")
                require(target.parent.is_dir(), "report parent must exist")
                output = canonical(value) if kind == "json" else value.encode("utf-8")
                write_new(target, output)
                result = {"status": "report-written", "format": kind, "output": str(target)}
            else:
                result = value
                if kind == "markdown":
                    print(value, end="" if value.endswith("\n") else "\n")
                    return 0
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
