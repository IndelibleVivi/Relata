#!/usr/bin/env python3
"""Offline input preparation for the selected CT-AUTHORSHIP candidate.

This is offline case-validity tooling, not a subject, model, adapter,
scoring contract, or accepted case release. `check` validates the bundled
authored fixture; `build` writes isolated subject inputs plus unanswered reviewer
packets and an evaluator-only preparation key; `verify` re-derives every prepared
item from the current bundled source; `audit` reports literal information-loss
collisions on the selected family only.

The CLI accepts exactly one bundled fixture path and exactly one family. It
creates no model/provider call, external command, corpus import, retry, inference,
score, or case-authority claim. Directory separation is a bound on accidental
early disclosure, NOT a security sandbox.

Projections are literal transformations of authored bytes. Equal projected
inputs erase an authored contrast at this input boundary. Byte-inequality is not
evidence of solvability, recall, good use, reader success, or a model score.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import secrets
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASE_SOURCE = ROOT / "case-lab" / "fixtures" / "ct-authorship.zh-CN.json"
FAMILY_ID = "CT-AUTHORSHIP"
FORMAT = "relata-ct-authorship-preparation-1"
CONDITIONS = ("current-only", "full-history", "source-excerpt")
PROJECTIONS = ("full-history", "without-speaker", "last-two-events", "last-event", "current-only")
# Expected collisions on this selected one-family candidate only; correlated
# checkpoints, NOT three independent cases and NOT a benchmark figure.
EXPECTED_COLLISIONS = {
    "full-history": 0,
    "without-speaker": 3,
    "last-two-events": 2,
    "last-event": 3,
    "current-only": 3,
}
SUBJECT_FIELDS = ("context", "history", "current")
HISTORY_FIELDS = ("session", "role", "surface", "text")
SUBJECT_ROLES = ("user", "assistant", "tool")
REVIEW_FIELDS = ("context", "governing_history", "current", "response", "review_status", "instructions")
REVIEW_STATUS = "pending-no-response"
KEY_RECORD_FIELDS = ("packet_id", "family", "variant", "probe", "condition",
                     "subject_sha256", "reviewer_sha256", "authoring_review_contract")
KEY_FIELDS = ("format", "bundle_id", "source_revision", "id_salt",
              "counts", "records", "status", "warning")
REVIEW_INSTRUCTIONS = (
    "先按完整历史证据判断答复是否回应当前请求，并记录依据与歧义；"
    "不要把字符串出现当作实际采用，不按字数、亲昵程度或文风直接排高低。"
)
KEY_WARNING = (
    "evaluator-only preparation key; public development material, not a sealed "
    "benchmark, not a scored result, and not reviewer calibration"
)
STATUS = "inputs-prepared; no model calls, no scores, candidate semantics still authored-unvalidated"
LIMIT = 1_000_000


def encoded(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                       allow_nan=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_json(path: Path) -> Any:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > LIMIT:
        raise ValueError(f"invalid JSON input: {path.name}")
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON field")
            result[key] = value
        return result
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid JSON input: {path.name}") from error


def load_case(path: Path = CASE_SOURCE) -> dict[str, Any]:
    if path.resolve() != CASE_SOURCE.resolve():
        raise ValueError("the CLI accepts only the bundled ct-authorship fixture")
    bundle = read_json(path)
    require(isinstance(bundle, dict), "invalid fixture object")
    return bundle


def the_family(bundle: dict[str, Any]) -> dict[str, Any]:
    families = bundle["families"]
    require(isinstance(families, list) and len(families) == 1,
            "this preparation accepts exactly one authored family")
    family = families[0]
    require(family["id"] == FAMILY_ID, "unexpected family identity")
    return family


def source_view(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Literal projection of the authored surface: keep session/role/surface/text.

    Drops authoring IDs only, preserves order verbatim, and performs no semantic
    transformation or inference.
    """
    return [{key: event[key] for key in HISTORY_FIELDS} for event in events]


def history_prefix(variant: dict[str, Any], probe: dict[str, Any]) -> list[dict[str, Any]]:
    ids = [event["id"] for event in variant["history"]]
    require(probe["after_event"] in ids, "unknown checkpoint boundary")
    return variant["history"][:ids.index(probe["after_event"]) + 1]


def governing_events(variant: dict[str, Any], probe: dict[str, Any]) -> list[dict[str, Any]]:
    """Ordered raw subset declared as this probe's source evidence (no sorting)."""
    prefix = history_prefix(variant, probe)
    ids = {event["id"] for event in prefix}
    require(set(probe["review"]["source_event_ids"]) <= ids,
            "source evidence references future or missing events")
    wanted = set(probe["review"]["source_event_ids"])
    return [event for event in prefix if event["id"] in wanted]


def subject_input(bundle: dict[str, Any], variant: dict[str, Any], probe: dict[str, Any],
                  condition: str) -> dict[str, Any]:
    """Subject sees context/history/current only, projected for one input condition."""
    require(condition in CONDITIONS, "unknown input condition")
    prefix = history_prefix(variant, probe)
    if condition == "current-only":
        history = []
    elif condition == "source-excerpt":
        history = governing_events(variant, probe)
    else:
        history = prefix
    return {
        "context": bundle["common_context"],
        "history": source_view(history),
        "current": {"surface": probe["current"]["surface"], "text": probe["current"]["text"]},
    }


def reviewer_packet(bundle: dict[str, Any], variant: dict[str, Any], probe: dict[str, Any]) -> dict[str, Any]:
    """Unanswered first-pass reviewer packet with the complete governing history.

    Carries an explicit null response and pending review state; the authoring
    review contract stays evaluator-only and is not exposed here.
    """
    return {
        "context": bundle["common_context"],
        "governing_history": source_view(history_prefix(variant, probe)),
        "current": {"surface": probe["current"]["surface"], "text": probe["current"]["text"]},
        "response": None,
        "review_status": REVIEW_STATUS,
        "instructions": REVIEW_INSTRUCTIONS,
    }


def project(bundle: dict[str, Any], variant: dict[str, Any], probe: dict[str, Any],
            mode: str) -> dict[str, Any]:
    require(mode in PROJECTIONS, "unknown projection")
    history = source_view(history_prefix(variant, probe))
    if mode == "without-speaker":
        history = [{key: value for key, value in event.items() if key != "role"} for event in history]
    elif mode == "last-two-events":
        history = history[-2:]
    elif mode == "last-event":
        history = history[-1:]
    elif mode == "current-only":
        history = []
    return {
        "context": bundle["common_context"],
        "history": history,
        "current": {"surface": probe["current"]["surface"], "text": probe["current"]["text"]},
    }


def validate(bundle: dict[str, Any]) -> dict[str, int]:
    """Validate authored structure and declared pairing invariants; no result claim."""
    require(isinstance(bundle.get("bundle_id"), str) and bundle["bundle_id"], "missing bundle identity")
    require(bool(bundle.get("common_context")), "missing shared context")
    require(bundle.get("semantic_validation") == "not-run", "semantic status must stay unvalidated")
    require(bundle.get("system_evaluation") == "not-run", "this helper accepts no result claims")
    require(bundle.get("human_review") == "not-run", "review state must remain not-run")
    family = the_family(bundle)
    variants = family["variants"]
    require(len(variants) == 2 and len({v["id"] for v in variants}) == 2,
            "candidate format requires two distinct history variants")
    counts = {
        "histories": len(variants), "checkpoints": 0, "conditions": len(CONDITIONS),
        "contrast_pairs": 0, "invariance_pairs": 0,
        "subject_inputs": 0, "reviewer_packets": 0, "reviewer_packet_bodies": 0,
    }
    for variant in variants:
        events = variant["history"]
        require(bool(events), "empty history")
        ids = [event["id"] for event in events]
        require(len(ids) == len(set(ids)), "duplicate event ID")
        require(all(set(event) >= set(HISTORY_FIELDS) for event in events), "incomplete source event")
        require(all(event["role"] in SUBJECT_ROLES for event in events), "unknown source role")
        sessions = [event["session"] for event in events]
        require(all(isinstance(s, int) and s > 0 for s in sessions), "invalid session index")
        require(sessions == sorted(sessions), "out-of-order sessions")
        require(all(isinstance(e["text"], str) and e["text"].strip() for e in events), "empty source text")
        probes = variant["probes"]
        require(bool(probes), "empty checkpoint list")
        require(len({p["id"] for p in probes}) == len(probes), "duplicate probe ID")
        for probe in probes:
            prefix = history_prefix(variant, probe)
            visible = {event["id"] for event in prefix}
            review = probe["review"]
            refs = review["source_event_ids"]
            require(bool(refs) and len(refs) == len(set(refs)), "invalid source evidence references")
            require(set(refs) <= visible, "future or missing evidence reference")
            require(isinstance(probe["current"].get("text"), str) and probe["current"]["text"].strip(),
                    "empty current request")
            require(bool(review["required_meanings"]), "missing required meanings")
            require(bool(review["prohibited_meanings"]), "missing prohibited meanings")
            require(review.get("semantic_status") == "authored-unvalidated", "unsupported semantic claim")
            counts["checkpoints"] += 1
    left, right = variants
    require([p["id"] for p in left["probes"]] == [p["id"] for p in right["probes"]],
            "mismatched paired checkpoints")
    for a, b in zip(left["probes"], right["probes"]):
        require(a["current"] == b["current"], "current request or scope differs across history twins")
        require(a["after_event"] == b["after_event"], "paired checkpoint boundary differs")
        ra, rb = a["review"], b["review"]
        require(ra["pair_relation"] == rb["pair_relation"], "pair relation mismatch")
        if ra["pair_relation"] == "contrast":
            require(ra["hinge_value"] != rb["hinge_value"], "contrast has identical declared hinges")
            counts["contrast_pairs"] += 1
        elif ra["pair_relation"] == "invariance":
            require(ra["hinge_value"] == rb["hinge_value"], "invariance has different hinges")
            counts["invariance_pairs"] += 1
        else:
            raise ValueError("invalid pair relation")
    counts["subject_inputs"] = counts["checkpoints"] * len(CONDITIONS)
    # One reviewer packet file is written per prepared input; its body depends only
    # on (variant, probe), so distinct bodies are one per checkpoint.
    counts["reviewer_packets"] = counts["subject_inputs"]
    counts["reviewer_packet_bodies"] = counts["checkpoints"]
    return counts


def source_revision(bundle: dict[str, Any]) -> str:
    return digest(encoded(bundle))


def packet_id(salt: str, family: str, variant: str, probe: str, condition: str) -> str:
    return hashlib.sha256(f"{salt}:{family}:{variant}:{probe}:{condition}".encode()).hexdigest()[:24]


def write_new(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)


def fresh_directory(path: Path) -> Path:
    # Inspect the caller's path (before symlink resolution) so a symlinked output
    # or parent is rejected even though resolve() would silently follow it.
    original = path.expanduser().absolute()
    require(not any(p.is_symlink() for p in (original, *original.parents)),
            "output path may not contain symlinks")
    path = original.resolve()
    require(path.parent.is_dir(), "output parent must already exist")
    path.mkdir(mode=0o700, exist_ok=False)
    return path


def resolve_directory(path: Path) -> Path:
    """Resolve a relative or absolute CLI directory against the current cwd."""
    original = path.expanduser().absolute()
    require(not any(p.is_symlink() for p in (original, *original.parents)),
            "directory path may not contain symlinks")
    resolved = original.resolve()
    require(resolved.is_dir(), "directory does not exist")
    return resolved


def build(bundle: dict[str, Any], out: Path, salt: str | None = None) -> dict[str, Any]:
    counts = validate(bundle)
    folder = fresh_directory(out)
    for name in ("subjects", "reviewers", "audit"):
        (folder / name).mkdir()
    salt = salt or secrets.token_hex(32)
    records: list[dict[str, Any]] = []
    for variant in the_family(bundle)["variants"]:
        for probe in variant["probes"]:
            reviewer_bytes = encoded(reviewer_packet(bundle, variant, probe))
            for condition in CONDITIONS:
                identifier = packet_id(salt, FAMILY_ID, variant["id"], probe["id"], condition)
                subject_bytes = encoded(subject_input(bundle, variant, probe, condition))
                write_new(folder / "subjects" / f"{identifier}.json", subject_bytes)
                write_new(folder / "reviewers" / f"{identifier}.json", reviewer_bytes)
                records.append({
                    "packet_id": identifier, "family": FAMILY_ID, "variant": variant["id"],
                    "probe": probe["id"], "condition": condition,
                    "subject_sha256": digest(subject_bytes),
                    "reviewer_sha256": digest(reviewer_bytes),
                    "authoring_review_contract": probe["review"],
                })
    key = {
        "format": FORMAT, "bundle_id": bundle["bundle_id"],
        "source_revision": source_revision(bundle),
        "id_salt": salt, "counts": counts, "records": records,
        "status": STATUS, "warning": KEY_WARNING,
    }
    write_new(folder / "audit" / "preparation-key.json", encoded(key))
    return key


def _check_key_records(key: dict[str, Any], counts: dict[str, int],
                       expected: dict[str, dict[str, Any]]) -> None:
    """Bind the evaluator-only key records to the current source projections."""
    require(key["counts"] == counts, "preparation counts differ from the current source")
    records = key["records"]
    require(isinstance(records, list) and len(records) == len(expected),
            "preparation record coverage differs")
    seen: set[str] = set()
    for record in records:
        require(isinstance(record, dict) and set(record) == set(KEY_RECORD_FIELDS),
                "invalid preparation record shape")
        identifier = record["packet_id"]
        require(isinstance(identifier, str) and identifier not in seen,
                "duplicate or invalid packet identity")
        seen.add(identifier)
        require(identifier in expected, "preparation key contains an unknown packet")
        require(record == expected[identifier], "preparation key record differs from the current projection")
    require(seen == set(expected), "preparation key is missing a packet")


def verify(folder: Path, bundle: dict[str, Any] | None = None) -> dict[str, Any]:
    """Re-derive every prepared item from the current bundled source.

    Each prepared file must byte-equal its intended projection from the current
    source, so a self-consistent but edited bundle is rejected. The key's
    source revision is compared first, so a real fixture change is reported as a
    named source revision mismatch before generic per-input errors. This scope is
    current preparation inputs only; it does not read future answered review records.
    """
    if bundle is None:
        bundle = load_case()
    counts = validate(bundle)
    folder = resolve_directory(folder)
    key_path = folder / "audit" / "preparation-key.json"
    key = read_json(key_path)
    require(isinstance(key, dict) and set(key) == set(KEY_FIELDS), "invalid preparation key shape")
    if key["source_revision"] != source_revision(bundle):
        raise ValueError("source revision mismatch: bundled candidate changed since preparation")
    require(key["bundle_id"] == bundle["bundle_id"], "preparation key belongs to another candidate")
    require(key["status"] == STATUS and key["warning"] == KEY_WARNING,
            "preparation key declaration changed")
    require(isinstance(key["format"], str) and key["format"] == FORMAT,
            "unsupported preparation format")
    salt = key["id_salt"]
    require(isinstance(salt, str) and len(salt) >= 32, "invalid preparation salt")
    require({p.name for p in folder.iterdir()} == {"subjects", "reviewers", "audit"},
            "unexpected or missing root entry")
    require(all((folder / name).is_dir() and not (folder / name).is_symlink()
                for name in ("subjects", "reviewers", "audit")),
            "missing or invalid preparation subdirectory")
    require({p.name for p in (folder / "audit").iterdir()} == {"preparation-key.json"},
            "unexpected or missing preparation key")
    # Re-derive the intended bytes for every prepared input and reviewer packet.
    expected: dict[str, dict[str, Any]] = {}
    subject_bytes: dict[str, bytes] = {}
    reviewer_bytes: dict[str, bytes] = {}
    for variant in the_family(bundle)["variants"]:
        for probe in variant["probes"]:
            reviewer_blob = encoded(reviewer_packet(bundle, variant, probe))
            for condition in CONDITIONS:
                subject_blob = encoded(subject_input(bundle, variant, probe, condition))
                identifier = packet_id(salt, FAMILY_ID, variant["id"], probe["id"], condition)
                expected[identifier] = {
                    "packet_id": identifier, "family": FAMILY_ID, "variant": variant["id"],
                    "probe": probe["id"], "condition": condition,
                    "subject_sha256": digest(subject_blob),
                    "reviewer_sha256": digest(reviewer_blob),
                    "authoring_review_contract": probe["review"],
                }
                subject_bytes[identifier] = subject_blob
                reviewer_bytes[identifier] = reviewer_blob
    # One expected file per identifier; extra or missing members are rejected before
    # any per-file read, so a missing file is a clean shape error.
    subject_files = sorted(p.name for p in (folder / "subjects").iterdir())
    reviewer_files = sorted(p.name for p in (folder / "reviewers").iterdir())
    expected_names = sorted(identifier + ".json" for identifier in expected)
    require(subject_files == expected_names,
            "subject input set differs from the intended projections")
    require(reviewer_files == expected_names,
            "reviewer packet set differs from the intended projections")
    # Every prepared file must byte-equal its intended projection from the current
    # source; this single comparison covers tampering, re-sealing, and drift.
    for identifier, blob in subject_bytes.items():
        subject_file = folder / "subjects" / (identifier + ".json")
        require(not subject_file.is_symlink(), "prepared input may not be a symlink")
        require(subject_file.read_bytes() == blob,
                f"subject input differs from the current projection: {identifier}")
    for identifier, blob in reviewer_bytes.items():
        reviewer_file = folder / "reviewers" / (identifier + ".json")
        require(not reviewer_file.is_symlink(), "prepared input may not be a symlink")
        require(reviewer_file.read_bytes() == blob,
                f"reviewer packet differs from the current projection: {identifier}")
    _check_key_records(key, counts, expected)
    return {
        "status": "prepared-material-valid", "source_revision": source_revision(bundle),
        "counts": counts, "semantic_status": "authored-unvalidated",
    }


def audit(bundle: dict[str, Any] | None = None) -> dict[str, Any]:
    """Literal information-loss diagnostic on the selected one-family candidate."""
    if bundle is None:
        bundle = load_case()
    counts = validate(bundle)
    left, right = the_family(bundle)["variants"]
    projections = []
    for mode in PROJECTIONS:
        collisions = []
        for lp in left["probes"]:
            rp = next(p for p in right["probes"] if p["id"] == lp["id"])
            a = encoded(project(bundle, left, lp, mode))
            b = encoded(project(bundle, right, rp, mode))
            collisions.append({
                "probe": lp["id"], "identical_projected_inputs": a == b,
                "left_sha256": digest(a), "right_sha256": digest(b),
            })
        observed = sum(row["identical_projected_inputs"] for row in collisions)
        projections.append({
            "projection": mode, "contrast_pairs": len(collisions),
            "collisions_on_contrast_pairs": observed,
            "expected_collisions": EXPECTED_COLLISIONS[mode],
            "matches_expected": observed == EXPECTED_COLLISIONS[mode],
            "records": collisions,
        })
    return {
        "status": "executed-offline-input-audit", "bundle_id": bundle["bundle_id"],
        "source_revision": source_revision(bundle), "counts": counts, "projections": projections,
        "interpretation": (
            "Collisions are exact encoded-byte equality after a named literal projection; they erase an "
            "authored contrast at this input boundary. Non-collision is not proof of solvability, recall, "
            "good use, or reader success, and no model or scorer was run."
        ),
        "caveats": [
            "One selected family; the three checkpoints are correlated, not three independent cases.",
            "Expected collision counts are a fixture-invariant check, not a benchmark figure or score.",
            "Projection names denote literal transformations, not commercial systems or architecture classes.",
            "Authored semantic contracts remain unvalidated by human review (authored-unvalidated).",
        ],
    }


def _write_report(path: Path, report: dict[str, Any]) -> None:
    original = path.expanduser().absolute()
    require(not any(p.is_symlink() for p in (original, *original.parents)),
            "report path may not contain symlinks")
    path = original.resolve()
    require(path.parent.is_dir(), "report parent must already exist")
    write_new(path, encoded(report))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="validate the bundled fixture and pairing invariants")
    build_command = commands.add_parser("build", help="write isolated subject inputs and reviewer packets")
    build_command.add_argument("--out", type=Path, required=True, help="new directory; parent must exist")
    verify_command = commands.add_parser("verify", help="re-derive prepared material from the current source")
    verify_command.add_argument("directory", type=Path)
    audit_command = commands.add_parser("audit", help="literal projection collision diagnostic")
    audit_command.add_argument("--out", type=Path, help="new JSON report; never overwrite")
    args = parser.parse_args(argv)
    try:
        bundle = load_case()
        if args.command == "check":
            report = {"structural_check": "passed", **validate(bundle),
                      "semantic_status": "authored-unvalidated", "system_evaluation": "not-run"}
            require(all(projection["matches_expected"] for projection in audit(bundle)["projections"]),
                    "fixture collision invariants changed; rerun audit before use")
            print(encoded(report).decode(), end="")
        elif args.command == "build":
            key = build(bundle, args.out)
            print(encoded({"status": key["status"], **key["counts"]}).decode(), end="")
        elif args.command == "verify":
            print(encoded(verify(args.directory, bundle)).decode(), end="")
        else:
            report = audit(bundle)
            if args.out is not None:
                _write_report(args.out, report)
            print(encoded({"status": report["status"], "projections": [
                {k: row[k] for k in ("projection", "contrast_pairs",
                                     "collisions_on_contrast_pairs", "matches_expected")}
                for row in report["projections"]]}).decode(), end="")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Preparation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
