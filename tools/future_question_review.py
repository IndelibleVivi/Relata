#!/usr/bin/env python3
"""Offline response/review plumbing for the bundled future-question study.

This tool prepares input-only packets, imports manually supplied response and
review records, exports a blind review packet, and recomputes descriptive
statistics. It never invokes a subject, provider, model, adapter, command or
network service. Imported records are evidence of tool lineage, not a system
result or an accepted semantic contract.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import json
from pathlib import Path
import re
import secrets
import sys
from typing import Any

try:
    from . import future_question_inputs as inputs
except ImportError:
    import future_question_inputs as inputs

MANIFEST_FORMAT = "relata-future-question-review-manifest-1"
RESPONSE_FORMAT = "relata-future-question-responses-1"
RESPONSE_FORMAT_V2 = "relata-future-question-responses-2"
REVIEW_FORMAT = "relata-future-question-reviews-1"
REVIEW_FORMAT_V2 = "relata-future-question-reviews-2"
REVIEW_KEY_FORMAT = "relata-future-question-review-key-1"
REVIEW_KEY_FORMAT_V2 = "relata-future-question-review-key-2"
RESPONSE_STATUSES = ("completed", "pending", "technical_failure", "not-run")
MANIFEST_FIELDS = {
    "format", "status", "history_sha256", "contract_sha256", "conditions",
    "contract", "records",
}
RECORD_FIELDS = {
    "input_id", "family", "question", "world_id", "projection", "archive_access",
    "input_sha256", "answer_region",
}
RESPONSE_BATCH_FIELDS = {"format", "provenance", "records"}
RESPONSE_FIELDS = {"input_id", "status", "response", "failure"}
RESPONSE_BATCH_FIELDS_V2 = {"format", "provenance", "records"}
RESPONSE_FIELDS_V2 = {
    "input_id", "attempt_id", "previous_attempt", "status", "response", "failure",
}
REVIEW_BATCH_FIELDS = {
    "format", "review_key_sha256", "records",
}
REVIEW_FIELDS = {
    "alias", "input_id", "reviewer_id", "decision", "reason", "evidence_refs",
}
REVIEW_IMPORT_FIELDS = {"format", "records"}
REVIEW_INPUT_FIELDS = {"alias", "reviewer_id", "decision", "reason", "evidence_refs"}
REVIEW_FIELDS_V2 = {
    "alias", "input_id", "attempt_id", "reviewer_id", "response_act", "mapping",
    "decision", "reason", "evidence_refs",
}
REVIEW_INPUT_FIELDS_V2 = {
    "alias", "reviewer_id", "response_act", "mapping", "decision", "reason",
    "evidence_refs",
}
REVIEW_ITEM_FIELDS = {"alias", "input_view", "response", "decision_options", "instructions"}
REVIEW_ITEM_FIELDS_V2 = {
    "alias", "input_view", "response", "response_state", "decision_options",
    "response_act_options", "mapping_options", "instructions",
}
REVIEW_KEY_FIELDS = {"format", "packet_id", "history_sha256", "contract_sha256", "records"}
REVIEW_KEY_FIELDS_V2 = REVIEW_KEY_FIELDS
REVIEW_KEY_RECORD_FIELDS = {
    "alias", "input_id", "input_sha256", "response_sha256", "item_sha256",
}
REVIEW_KEY_RECORD_FIELDS_V2 = REVIEW_KEY_RECORD_FIELDS | {"attempt_id"}
RESPONSE_ACT_OPTIONS = (
    "answer", "clarification", "abstention", "refusal", "action", "empty",
    "technical-failure", "other",
)
MAPPING_OPTIONS = (
    "mapped", "unmapped", "ambiguous", "partial", "not-applicable",
    "contract-insufficient",
)
LEGACY_REVIEW_INSTRUCTIONS = (
    "Judge whether the response completes the current information task using the "
    "shown input. Select one finite decision, cite evidence locators from this "
    "packet, and give a substantive reason. Honest uncertainty may be appropriate "
    "without completing the task."
)
REVIEW_INSTRUCTIONS = (
    "请根据此处提供的输入，判断回答怎样完成当前信息任务。从所列有限选项中选择一项，"
    "引用本输入内的 evidence locators，并说明实质理由。诚实表达不确定性可能适当，"
    "但不一定完成该信息任务。选项覆盖同一家族的全部问题与世界，不表示本题正确答案区域。 "
    "Judge the response against the shown input and current task; select one listed "
    "decision, cite evidence locators, and explain why. Options span all questions "
    "and worlds in this family, not this item's correct answer region."
)
REVIEW_INSTRUCTIONS_V2 = (
    "请根据此处提供的输入，判断回答怎样完成当前信息任务。先记录回答的 response act，"
    "再说明它是否映射到一个 finite decision；unmapped、ambiguous 或 contract-insufficient "
    "可以没有 decision。需要引用时，只引用本输入内的 evidence locators。"
    " Judge the response against the shown input and current task. Record its response act "
    "and mapping; mapping states other than mapped may omit a decision. Options span all "
    "questions and worlds in the family, not this item's correct answer region."
)

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def canonical(value: Any) -> bytes:
    return inputs.canonical(value)

def digest(value: bytes) -> str:
    return inputs.digest(value)

def read_json(path: Path) -> Any:
    return inputs.read_json(path)

def load_bundle() -> tuple[dict[str, Any], dict[str, Any]]:
    source = read_json(inputs.HISTORIES)
    contracts = read_json(inputs.CONTRACTS)
    inputs.validate_histories(source)
    inputs.validate_contracts(source, contracts)
    return source, contracts

def checked_directory(path: Path) -> Path:
    original = path.expanduser().absolute()
    require(not any(p.is_symlink() for p in (original, *original.parents)),
            "directory path may not contain symlinks")
    resolved = original.resolve()
    require(resolved.is_dir(), "directory does not exist")
    return resolved

def fresh_directory(path: Path) -> Path:
    return inputs.fresh_directory(path)

def write_new(path: Path, value: Any) -> None:
    inputs.write_new(path, canonical(value))

def require_shape(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) == fields,
            f"invalid {label} fields")
    return value

def expected_cells(source: dict[str, Any], contracts: dict[str, Any]
                   ) -> dict[tuple[str, str, str, str, str], dict[str, Any]]:
    cells = {}
    for family in source["families"]:
        answer_contract = contracts["families"][family["id"]]
        for question in family["questions"]:
            for world in family["worlds"]:
                for projection, access in inputs.CONDITIONS:
                    key = (family["id"], question["id"], world["id"], projection, access)
                    cells[key] = {
                        "view": inputs.exported_input_view(inputs.make_view(
                            source["context"], family, world, question, projection, access)),
                        "answer_region": sorted(answer_contract[question["id"]][world["id"]]),
                    }
    return cells

def prepare(output: Path) -> dict[str, Any]:
    source, contracts = load_bundle()
    inputs.write_input_packet(source, output)
    folder = checked_directory(output)
    raw = read_json(folder / "hidden" / "manifest.json")
    require(raw.get("format") == "relata-future-question-input-packet-1",
            "input packet identity changed")
    cells = expected_cells(source, contracts)
    records = []
    for record in raw["records"]:
        key = (record["family"], record["question"], record["world_id"],
               record["projection"], record["archive_access"])
        require(key in cells, "input packet names an unknown cell")
        records.append({**record, "answer_region": cells[key]["answer_region"]})
    require(len(records) == len(cells), "input packet does not contain every fixed cell")
    conditions = [list(condition) for condition in inputs.CONDITIONS]
    manifest = {
        "format": MANIFEST_FORMAT,
        "status": "offline input packet; no subject execution or imported result",
        "history_sha256": digest(canonical(source)),
        "contract_sha256": digest(canonical(contracts)),
        "conditions": conditions,
        "contract": deepcopy(contracts),
        "records": records,
    }
    write_new(folder / "hidden" / "review-manifest.json", manifest)
    (folder / "responses").mkdir(mode=0o700, exist_ok=True)
    (folder / "reviews").mkdir(mode=0o700, exist_ok=True)
    (folder / "review-keys").mkdir(mode=0o700, exist_ok=True)
    return {"status": "prepared", "packet": str(folder),
            "inputs": len(records), "status_pending": len(records)}

def _batch_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    require(folder.is_dir() and not folder.is_symlink(), "invalid record directory")
    files = sorted(folder.iterdir())
    for index, path in enumerate(files, 1):
        require(not path.is_symlink() and path.is_file() and
                path.name == f"{index:06d}.json", "invalid append-only batch inventory")
    return files

def _stored_keys(folder: Path) -> dict[str, dict[str, Any]]:
    keys: dict[str, dict[str, Any]] = {}
    keys_folder = folder / "review-keys"
    require(keys_folder.is_dir() and not keys_folder.is_symlink(),
            "invalid stored review keys directory")
    for path in sorted(keys_folder.iterdir()):
        require(path.is_file() and not path.is_symlink() and
                re.fullmatch(r"P-[0-9a-f]{32}(?:\.json|\.receipt\.json)", path.name),
                "invalid stored review key inventory")
        if path.name.endswith(".receipt.json"):
            continue
        require(path.read_bytes() == canonical(read_json(path)),
                "stored review key is not canonical")
        key = require_shape(read_json(path), REVIEW_KEY_FIELDS, "stored review key")
        require(key["format"] in {REVIEW_KEY_FORMAT, REVIEW_KEY_FORMAT_V2},
                "invalid stored review key")
        identifier = key["packet_id"]
        require(isinstance(identifier, str) and
                re.fullmatch(r"P-[0-9a-f]{32}", identifier) and
                identifier not in keys and path.name == identifier + ".json",
                "invalid stored review packet identity")
        keys[identifier] = key
    return keys

def _check_stored_key(key: dict[str, Any], manifest: dict[str, Any],
                      by_id: dict[str, dict[str, Any]],
                      responses: dict[str, dict[str, Any]],
                      source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Rebind a stored blind key to the exact contract, inputs and responses."""
    require(key["format"] in {REVIEW_KEY_FORMAT, REVIEW_KEY_FORMAT_V2} and
            key["history_sha256"] == manifest["history_sha256"] and
            key["contract_sha256"] == manifest["contract_sha256"],
            "stored review key contract revision mismatch")
    version = 1 if key["format"] == REVIEW_KEY_FORMAT else 2
    seen_aliases: set[str] = set()
    seen_inputs: set[str] = set()
    options_by_alias: dict[str, dict[str, Any]] = {}
    for record in key["records"]:
        record = require_shape(record, REVIEW_KEY_RECORD_FIELDS if version == 1 else
                               REVIEW_KEY_RECORD_FIELDS_V2,
                               "stored review key record")
        alias, identifier = record["alias"], record["input_id"]
        require(isinstance(alias, str) and re.fullmatch(r"V-[0-9a-f]{32}", alias)
                and alias not in seen_aliases, "invalid stored review alias")
        require(identifier in by_id and identifier not in seen_inputs,
                "stored review key input is unknown or duplicated")
        require(record["input_sha256"] == by_id[identifier]["input_sha256"],
                "stored review key input digest mismatch")
        response = responses.get(identifier)
        require(response is not None and response["status"] == "completed",
                "stored review key does not bind a completed response")
        require(record["response_sha256"] == digest(canonical(response)),
                "stored review key response digest mismatch")
        if version == 2:
            require(record["attempt_id"] == attempt_identity(response),
                    "v2 review key does not bind its completed attempt")
        require(isinstance(record["item_sha256"], str) and
                re.fullmatch(r"[0-9a-f]{64}", record["item_sha256"]),
                "invalid stored review item digest")
        # Reconstruct the exact exported contract without requiring the external
        # reviewer folder to remain on disk. This also preserves old exports.
        if version == 2:
            item = {
                "alias": alias,
                "input_view": _input_view(by_id[identifier], source),
                "response": response["response"],
                "response_state": response["status"],
                "decision_options": decision_options_for(
                    by_id[identifier], manifest["contract"]),
                "response_act_options": list(RESPONSE_ACT_OPTIONS),
                "mapping_options": list(MAPPING_OPTIONS),
                "instructions": REVIEW_INSTRUCTIONS_V2,
            }
            require(digest(canonical(item)) == record["item_sha256"],
                    "stored v2 review item contract digest mismatch")
        else:
            item = {
                "alias": alias,
                "input_view": _input_view(by_id[identifier], source),
                "response": response["response"],
                "decision_options": decision_options_for(
                    by_id[identifier], manifest["contract"]),
                "instructions": REVIEW_INSTRUCTIONS,
            }
            if digest(canonical(item)) != record["item_sha256"]:
                item["decision_options"] = manifest["contract"]["decisions"]
                item["instructions"] = LEGACY_REVIEW_INSTRUCTIONS
                require(digest(canonical(item)) == record["item_sha256"],
                        "stored review item contract digest mismatch")
        options_by_alias[alias] = {
            "attempt_id": response.get("attempt_id"),
            "item": item,
            "decision_options": item["decision_options"],
        }
        seen_aliases.add(alias)
        seen_inputs.add(identifier)
    return options_by_alias

def _load_manifest(folder: Path, source: dict[str, Any], contracts: dict[str, Any]
                   ) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    require({p.name for p in folder.iterdir()} <=
            {"inputs", "hidden", "responses", "reviews", "review-keys"},
            "unexpected packet root entry")
    for name in ("inputs", "hidden"):
        path = folder / name
        require(path.is_dir() and not path.is_symlink(), "missing packet directory")
    require({p.name for p in (folder / "hidden").iterdir()} ==
            {"manifest.json", "review-manifest.json"}, "unexpected hidden manifest inventory")
    manifest = require_shape(read_json(folder / "hidden" / "review-manifest.json"),
                             MANIFEST_FIELDS, "review manifest")
    require(manifest["format"] == MANIFEST_FORMAT, "unsupported review manifest format")
    require(manifest["status"] ==
            "offline input packet; no subject execution or imported result",
            "review packet status changed")
    require(manifest["history_sha256"] == digest(canonical(source)),
            "history revision mismatch")
    require(manifest["contract_sha256"] == digest(canonical(contracts)),
            "answer contract revision mismatch")
    require(manifest["contract"] == contracts, "answer contract content differs")
    raw = read_json(folder / "hidden" / "manifest.json")
    require(isinstance(raw, dict) and
            set(raw) == {"format", "status", "history_sha256", "records"},
            "invalid input manifest")
    require(raw["format"] == "relata-future-question-input-packet-1" and
            raw["history_sha256"] == manifest["history_sha256"] and
            raw["status"] == "input-only; no subject execution or answer contract",
            "input manifest identity changed")
    conditions = manifest["conditions"]
    require(isinstance(conditions, list) and conditions and
            all(isinstance(condition, list) and len(condition) == 2 and
                tuple(condition) in inputs.CONDITIONS for condition in conditions) and
            tuple(tuple(condition) for condition in conditions) == inputs.CONDITIONS,
            "review packet requires the complete fixed condition matrix")
    used_conditions = {tuple(condition) for condition in conditions}
    records = manifest["records"]
    cells = {key: value for key, value in expected_cells(source, contracts).items()
             if key[3:] in used_conditions}
    require(isinstance(records, list) and len(records) == len(cells),
            "manifest does not contain every fixed cell")
    by_id: dict[str, dict[str, Any]] = {}
    seen_cells = set()
    for record in records:
        record = require_shape(record, RECORD_FIELDS, "manifest record")
        input_id = record["input_id"]
        require(isinstance(input_id, str) and re.fullmatch(r"I-[0-9a-f]{32}", input_id)
                and input_id not in by_id, "duplicate or invalid input ID")
        key = (record["family"], record["question"], record["world_id"],
               record["projection"], record["archive_access"])
        require(key in cells and key not in seen_cells,
                "unknown or duplicate manifest cell")
        seen_cells.add(key)
        expected = cells[key]
        blob = canonical(expected["view"])
        path = folder / "inputs" / f"{input_id}.json"
        require(not path.is_symlink() and path.is_file(), "missing prepared input")
        require(path.read_bytes() == blob, "prepared input differs from current projection")
        require(record["input_sha256"] == digest(blob), "input digest mismatch")
        require(record["answer_region"] == expected["answer_region"],
                "answer region differs from current contract")
        by_id[input_id] = record
    require(seen_cells == set(cells), "manifest is missing a fixed cell")
    require({p.name for p in (folder / "inputs").iterdir()} ==
            {identifier + ".json" for identifier in by_id}, "unexpected input file inventory")
    require({record["input_id"] for record in raw["records"]} == set(by_id),
            "input-only manifest identities differ")
    return manifest, by_id

def attempt_identity(record: dict[str, Any]) -> str:
    """Name a v2 attempt or the sole original v1 record within its bound input.

    This is a reading identity, never a rewrite of v1 bytes or response hashes.
    The input ID in the surrounding chain/key disambiguates legacy-v1.
    """
    return record.get("attempt_id") or "legacy-v1"


def _load_response_history(folder: Path, by_id: dict[str, dict[str, Any]]
                           ) -> dict[str, list[dict[str, Any]]]:
    """Return immutable attempts per input.

    v1 remains one record per input and keeps its original meaning. v2 adds an
    explicit per-input attempt chain, so a pending or failed position may later
    gain a completed attempt without rewriting the earlier record.
    """
    histories: dict[str, list[dict[str, Any]]] = {}
    seen_attempts: set[str] = set()
    for path in _batch_files(folder / "responses"):
        batch = read_json(path)
        require(isinstance(batch, dict) and
                batch.get("format") in {RESPONSE_FORMAT, RESPONSE_FORMAT_V2} and
                isinstance(batch["provenance"], str) and batch["provenance"].strip(),
                "invalid response batch provenance")
        require(isinstance(batch["records"], list) and batch["records"], "empty response batch")
        version = 1 if batch["format"] == RESPONSE_FORMAT else 2
        require_shape(batch, RESPONSE_BATCH_FIELDS if version == 1 else
                      RESPONSE_BATCH_FIELDS_V2, "response batch")
        for raw in batch["records"]:
            record = require_shape(
                raw, RESPONSE_FIELDS if version == 1 else RESPONSE_FIELDS_V2, "response")
            identifier = record["input_id"]
            require(identifier in by_id, "response ID is unknown")
            history = histories.setdefault(identifier, [])
            if version == 1:
                require(not history, "response ID is unknown or already used")
                _check_response_record(record, "stored", version=1)
                history.append(deepcopy(record))
                continue

            attempt_id = record["attempt_id"]
            require(isinstance(attempt_id, str) and
                    re.fullmatch(r"A-[0-9a-f]{32}", attempt_id) and
                    attempt_id not in seen_attempts,
                    "v2 attempt ID is invalid or already used")
            _check_response_record(record, "stored v2", version=2)
            previous = record["previous_attempt"]
            if not history:
                require(previous is None, "first attempt cannot have a predecessor")
            else:
                head = history[-1]
                require(head.get("status") != "completed",
                        "a completed response cannot be silently replaced")
                require(previous == attempt_identity(head),
                        "new attempt must name the current immutable predecessor")
            history.append(deepcopy(record))
            seen_attempts.add(attempt_id)
    return histories


def _view_attempts(histories: dict[str, list[dict[str, Any]]],
                   by_id: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Project one latest attempt per fixed position without changing case count."""
    responses: dict[str, dict[str, Any]] = {}
    for identifier in by_id:
        history = histories.get(identifier, [])
        if history:
            responses[identifier] = deepcopy(history[-1])
        else:
            responses[identifier] = {
                "input_id": identifier, "attempt_id": None,
                "previous_attempt": None, "status": "pending",
                "response": None, "failure": None,
            }
    return responses

def _check_response_record(record: dict[str, Any], label: str, *,
                           version: int = 1) -> None:
    status, response, failure = record["status"], record["response"], record["failure"]
    require(status in RESPONSE_STATUSES, "invalid response status")
    if status == "completed":
        require(isinstance(response, str) and failure is None and
                (version == 2 or bool(response.strip())),
                f"{label} completed response needs literal text and no failure")
    elif status == "technical_failure":
        require(response is None and isinstance(failure, str) and failure.strip(),
                f"{label} technical failure needs a failure record and no response")
    else:
        require(response is None and failure is None,
                f"{label} pending or not-run response cannot carry output or failure")

def _input_view(record: dict[str, Any], source: dict[str, Any]) -> dict[str, Any]:
    family = next(f for f in source["families"] if f["id"] == record["family"])
    world = next(w for w in family["worlds"] if w["id"] == record["world_id"])
    question = next(q for q in family["questions"] if q["id"] == record["question"])
    return inputs.exported_input_view(inputs.make_view(
        source["context"], family, world, question,
        record["projection"], record["archive_access"]))

def decision_options_for(record: dict[str, Any], contracts: dict[str, Any]
                         ) -> dict[str, str]:
    """Use the family-wide vocabulary, never the current world's answer key."""
    family = contracts["families"][record["family"]]
    used = {decision for worlds in family.values()
            for region in worlds.values() for decision in region}
    return {key: value for key, value in contracts["decisions"].items()
            if key in used}

def _check_review_payload(review: dict[str, Any], identifier: str,
                          packet: dict[str, Any], label: str) -> None:
    """Validate a review payload from either import or persisted replay."""
    reviewer = review["reviewer_id"]
    require(isinstance(reviewer, str) and bool(reviewer.strip()) and
            len(reviewer) <= 120, f"invalid {label} reviewer ID")
    require(review["decision"] in packet["contracts"]["decisions"],
            f"{label} decision is not in the contract")
    reason = review["reason"]
    require(isinstance(reason, str) and bool(reason.strip()),
            f"{label} reason is required")
    refs = review["evidence_refs"]
    require(isinstance(refs, list) and bool(refs) and
            all(isinstance(ref, str) for ref in refs) and
            len(refs) == len(set(refs)),
            f"{label} evidence references are required and unique")
    record = packet["by_id"][identifier]
    require(set(refs) <= allowed_evidence_refs(_input_view(
                record, packet["source"])),
            f"{label} cites evidence outside the exact input view")


def v2_attempt(packet: dict[str, Any], identifier: str,
               attempt_id: str) -> dict[str, Any] | None:
    history = packet["attempt_histories"].get(identifier, [])
    return next((row for row in history
                 if attempt_identity(row) == attempt_id and
                 row["status"] == "completed"), None)


def _check_v2_review_payload(review: dict[str, Any], identifier: str,
                             attempt_id: str, packet: dict[str, Any],
                             options: dict[str, str]) -> None:
    require(v2_attempt(packet, identifier, attempt_id) is not None,
            "v2 review does not bind a completed attempt")
    reviewer = review["reviewer_id"]
    require(isinstance(reviewer, str) and bool(reviewer.strip()) and
            len(reviewer) <= 120, "invalid v2 reviewer ID")
    require(review["response_act"] in RESPONSE_ACT_OPTIONS,
            "v2 response_act is not allowed")
    mapping = review["mapping"]
    require(mapping in MAPPING_OPTIONS, "v2 mapping is not allowed")
    if mapping == "mapped":
        require(isinstance(review["decision"], str) and
                review["decision"] in options,
                "mapped v2 review requires an allowed decision")
    else:
        require(review["decision"] is None,
                "non-mapped v2 review must not carry a decision")
    reason = review["reason"]
    require(isinstance(reason, str) and bool(reason.strip()),
            "v2 reason is required")
    refs = review["evidence_refs"]
    require(isinstance(refs, list) and bool(refs) and
            all(isinstance(ref, str) and ref.strip() for ref in refs) and
            len(refs) == len(set(refs)),
            "v2 evidence references are required and unique")
    record = packet["by_id"][identifier]
    require(set(refs) <= allowed_evidence_refs(_input_view(
                record, packet["source"])),
            "v2 review cites evidence outside the exact input view")

def _load_reviews(folder: Path, by_id: dict[str, dict[str, Any]],
                  decisions: dict[str, str],
                  keys: dict[str, dict[str, Any]], packet: dict[str, Any]
                  ) -> list[dict[str, Any]]:
    reviews: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    keys_by_hash = {digest(canonical(key)): key for key in keys.values()}
    for path in _batch_files(folder / "reviews"):
        batch = read_json(path)
        require(isinstance(batch, dict) and
                batch.get("format") in {REVIEW_FORMAT, REVIEW_FORMAT_V2} and
                isinstance(batch["review_key_sha256"], str) and
                re.fullmatch(r"[0-9a-f]{64}", batch["review_key_sha256"]),
                "invalid review batch")
        key = keys_by_hash.get(batch["review_key_sha256"])
        require(key is not None, "review batch does not name a stored blind packet")
        version = 1 if key["format"] == REVIEW_KEY_FORMAT else 2
        require(batch["format"] ==
                (REVIEW_FORMAT if version == 1 else REVIEW_FORMAT_V2),
                "review batch format does not match its blind key")
        require_shape(batch, REVIEW_BATCH_FIELDS, "review batch")
        keyed_by_alias = _check_stored_key(
            key, packet["manifest"], by_id, packet["responses"], packet["source"])
        key_by_alias = {record["alias"]: record for record in key["records"]}
        require(isinstance(batch["records"], list) and batch["records"], "empty review batch")
        for record in batch["records"]:
            record = require_shape(record, REVIEW_FIELDS if version == 1 else
                                   REVIEW_FIELDS_V2, "stored review")
            alias = record["alias"]
            require(alias in key_by_alias and
                    key_by_alias[alias]["input_id"] == record["input_id"],
                    "stored review alias does not bind its input")
            if version == 1:
                _check_review_payload(record, record["input_id"], packet, "stored review")
                require(record["decision"] in keyed_by_alias[alias]["decision_options"],
                        "stored review decision is not among the exported item options")
            else:
                require(record["attempt_id"] == key_by_alias[alias]["attempt_id"],
                        "v2 stored review attempt does not match its key")
                _check_v2_review_payload(
                    record, record["input_id"], record["attempt_id"], packet,
                    keyed_by_alias[alias]["decision_options"])
                if record["mapping"] == "mapped":
                    require(record["decision"] in
                            keyed_by_alias[alias]["decision_options"],
                            "stored review decision is not among the exported item options")
            pair = (record["input_id"], record["reviewer_id"])
            require(pair not in seen, "reviewer already reviewed this input")
            seen.add(pair)
            reviews.append(record)
    return reviews

def inspect_packet(path: Path, source: dict[str, Any] | None = None,
                   contracts: dict[str, Any] | None = None) -> dict[str, Any]:
    if source is None or contracts is None:
        source, contracts = load_bundle()
    folder = checked_directory(path)
    manifest, by_id = _load_manifest(folder, source, contracts)
    attempt_histories = _load_response_history(folder, by_id)
    responses = _view_attempts(attempt_histories, by_id)
    keys = _stored_keys(folder)
    packet = {"folder": folder, "source": source, "contracts": contracts,
              "manifest": manifest, "by_id": by_id,
              "responses": responses, "keys": keys,
              "attempt_histories": attempt_histories,
              "stored_response_ids": set(attempt_histories)}
    packet["reviews"] = _load_reviews(
        folder, by_id, contracts["decisions"], keys, packet)
    return packet

def verify(path: Path) -> dict[str, Any]:
    packet = inspect_packet(path)
    attempts = sum(len(history) for history in packet["attempt_histories"].values())
    return {"status": "prepared-inputs-valid",
            "inputs": len(packet["by_id"]),
            "responses": sum(response["status"] != "pending"
                             for response in packet["responses"].values()),
            "attempts": attempts,
            "positions_with_multiple_attempts": sum(
                len(history) > 1 for history in packet["attempt_histories"].values()),
            "review_keys": len(packet["keys"]),
            "reviews": len(packet["reviews"]),
            "execution": "not-run by this tool"}

def _next_batch(folder: Path, name: str) -> Path:
    target = folder / name
    target.mkdir(mode=0o700, exist_ok=True)
    require(target.is_dir() and not target.is_symlink(), "invalid record directory")
    return target / f"{len(_batch_files(target)) + 1:06d}.json"

def import_responses(path: Path, source_file: Path) -> dict[str, Any]:
    packet = inspect_packet(path)
    body = read_json(source_file)
    require(isinstance(body, dict) and
            body.get("format") in {RESPONSE_FORMAT, RESPONSE_FORMAT_V2},
            "unsupported response import format")
    version = 1 if body["format"] == RESPONSE_FORMAT else 2
    require_shape(body, RESPONSE_BATCH_FIELDS if version == 1 else
                  RESPONSE_BATCH_FIELDS_V2, "response import")
    require(isinstance(body["provenance"], str) and body["provenance"].strip(),
            "response import needs provenance")
    require(isinstance(body["records"], list) and body["records"], "empty response import")
    imported_ids: set[str] = set()
    imported_attempts: set[str] = set()
    for raw in body["records"]:
        record = require_shape(
            raw, RESPONSE_FIELDS if version == 1 else RESPONSE_FIELDS_V2, "imported response")
        identifier = record["input_id"]
        require(identifier in packet["by_id"], "response ID is unknown")
        if version == 1:
            require(identifier not in packet["stored_response_ids"],
                    "response ID is unknown or already used")
        else:
            attempt_id = record["attempt_id"]
            require(isinstance(attempt_id, str) and
                    re.fullmatch(r"A-[0-9a-f]{32}", attempt_id) and
                    attempt_id not in imported_attempts,
                    "v2 attempt ID is invalid or duplicated in the import")
            require(not any(existing.get("attempt_id") == attempt_id
                            for history in packet["attempt_histories"].values()
                            for existing in history),
                    "v2 attempt ID is already used")
            imported_attempts.add(attempt_id)
            prior = packet["attempt_histories"].get(identifier, [])
            if prior:
                require(prior[-1]["status"] != "completed",
                        "a completed response cannot be silently replaced")
                require(record["previous_attempt"] == attempt_identity(prior[-1]),
                        "new attempt must name the current immutable predecessor")
            else:
                require(record["previous_attempt"] is None,
                        "first attempt cannot have a predecessor")
        require(identifier not in imported_ids, "response ID is duplicated in the import")
        imported_ids.add(identifier)
        _check_response_record(record, "imported", version=version)
    dest = _next_batch(packet["folder"], "responses")
    require(not dest.exists(), "response batch would overwrite an existing record")
    write_new(dest, body)
    return {"status": "responses-imported", "batch": dest.name,
            "records": len(body["records"]), "attempts_added": len(body["records"]),
            "execution": "not-run by this tool"}

def allowed_evidence_refs(view: dict[str, Any]) -> set[str]:
    refs = {"context", "current", "archive_pointer", "archive.status"}
    refs.update(f"memory[{index}]" for index in range(len(view["memory"])))
    refs.update(f"archive.events[{index}]"
                for index in range(len(view["archive"].get("events", []))))
    return refs

def export_review(path: Path, output: Path) -> dict[str, Any]:
    packet = inspect_packet(path)
    if not any(response["status"] == "completed"
               for response in packet["responses"].values()):
        raise ValueError("no completed responses; review export would be empty")
    condition_scope = {(record["projection"], record["archive_access"])
                       for record in packet["by_id"].values()}
    if len(condition_scope) != len(inputs.CONDITIONS):
        raise ValueError("review export requires the complete fixed condition matrix")
    use_v2 = any(response.get("attempt_id") is not None
                 for response in packet["responses"].values())
    folder = fresh_directory(output)
    items = folder / "items"
    hidden = folder / "hidden"
    items.mkdir(mode=0o700)
    hidden.mkdir(mode=0o700)
    key_records = []
    for identifier, record in packet["by_id"].items():
        response = packet["responses"].get(identifier)
        if response is None or response["status"] != "completed":
            continue
        alias = "V-" + secrets.token_hex(16)
        item = {
            "alias": alias,
            "input_view": read_json(packet["folder"] / "inputs" / f"{identifier}.json"),
            "response": response["response"],
            "decision_options": decision_options_for(record, packet["contracts"]),
            "instructions": REVIEW_INSTRUCTIONS,
        }
        if use_v2:
            item.update(response_state=response["status"],
                        response_act_options=list(RESPONSE_ACT_OPTIONS),
                        mapping_options=list(MAPPING_OPTIONS),
                        instructions=REVIEW_INSTRUCTIONS_V2)
        blob = canonical(item)
        write_new(items / f"{alias}.json", item)
        key_record = {"alias": alias, "input_id": identifier,
                      "input_sha256": record["input_sha256"],
                      "response_sha256": digest(canonical(response)),
                      "item_sha256": digest(blob)}
        if use_v2:
            key_record["attempt_id"] = attempt_identity(response)
        key_records.append(key_record)
    key = {"format": REVIEW_KEY_FORMAT_V2 if use_v2 else REVIEW_KEY_FORMAT,
           "packet_id": "P-" + secrets.token_hex(16),
           "history_sha256": packet["manifest"]["history_sha256"],
           "contract_sha256": packet["manifest"]["contract_sha256"],
           "records": key_records}
    write_new(hidden / "review-key.json", key)
    write_new(packet["folder"] / "review-keys" / f"{key['packet_id']}.json", key)
    receipt = {
        "format": "relata-future-question-review-receipt-1",
        "packet_id": key["packet_id"],
        "output": folder.name,
        "review_key_sha256": digest(canonical(key)),
        "reviewed_inputs": [record["input_id"] for record in key_records],
    }
    write_new(packet["folder"] / "review-keys" / f"{key['packet_id']}.receipt.json",
              receipt)
    return {"status": "blind-review-exported", "output": str(folder),
            "items": len(key_records), "execution": "not-run by this tool"}

def _load_review_packet(path: Path, packet: dict[str, Any]
                        ) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    folder = checked_directory(path)
    require({p.name for p in folder.iterdir()} == {"items", "hidden"},
            "unexpected review packet root entry")
    items_dir, hidden_dir = folder / "items", folder / "hidden"
    require(items_dir.is_dir() and hidden_dir.is_dir() and
            not items_dir.is_symlink() and not hidden_dir.is_symlink(),
            "invalid review packet directories")
    require({p.name for p in hidden_dir.iterdir()} == {"review-key.json"},
            "unexpected review key inventory")
    key = read_json(hidden_dir / "review-key.json")
    require(isinstance(key, dict) and
            key.get("format") in {REVIEW_KEY_FORMAT, REVIEW_KEY_FORMAT_V2},
            "invalid review key")
    version = 1 if key["format"] == REVIEW_KEY_FORMAT else 2
    require_shape(key, REVIEW_KEY_FIELDS if version == 1 else REVIEW_KEY_FIELDS_V2,
                  "review key")
    require(isinstance(key["records"], list) and
            key["history_sha256"] == packet["manifest"]["history_sha256"] and
            key["contract_sha256"] == packet["manifest"]["contract_sha256"] and
            key["packet_id"] in packet["keys"],
            "invalid review key")
    keyed = _check_stored_key(key, packet["manifest"], packet["by_id"],
                              packet["responses"], packet["source"])
    require(key == packet["keys"][key["packet_id"]],
            "blind review key differs from its stored immutable copy")
    by_alias = {}
    expected_files = set()
    for record in key["records"]:
        record = require_shape(record, REVIEW_KEY_RECORD_FIELDS if version == 1 else
                               REVIEW_KEY_RECORD_FIELDS_V2, "review key record")
        alias = record["alias"]
        require(isinstance(alias, str) and re.fullmatch(r"V-[0-9a-f]{32}", alias)
                and alias not in by_alias and record["input_id"] in packet["by_id"],
                "invalid or duplicate review alias")
        path = items_dir / f"{alias}.json"
        expected_files.add(path.name)
        require(not path.is_symlink() and path.is_file(), "missing blind review item")
        blob = path.read_bytes()
        require(digest(blob) == record["item_sha256"], "blind review item hash mismatch")
        try:
            decoded = json.loads(blob)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("invalid blind review item JSON") from error
        expected_item = keyed[alias]["item"]
        item = require_shape(decoded, REVIEW_ITEM_FIELDS if version == 1 else
                             REVIEW_ITEM_FIELDS_V2, "blind review item")
        require(item == expected_item, "blind review item changed")
        response = packet["responses"].get(record["input_id"])
        require(response is not None and response["status"] == "completed" and
                item["response"] == response["response"] and
                (version == 1 or
                 (item["response_state"] == response["status"] and
                  record["attempt_id"] == attempt_identity(response))) and
                record["input_sha256"] == packet["by_id"][record["input_id"]]["input_sha256"] and
                record["response_sha256"] == digest(canonical(response)),
                "blind review item is not bound to an imported response")
        require(item["input_view"] == read_json(
                    packet["folder"] / "inputs" / f"{record['input_id']}.json"),
                "blind review item input view differs from the prepared input")
        by_alias[alias] = {**record, "item": item}
    require({p.name for p in items_dir.iterdir()} == expected_files,
            "unexpected blind review item inventory")
    require((hidden_dir / "review-key.json").read_bytes() == canonical(key),
            "blind review key is not canonical")
    stored = packet["folder"] / "review-keys" / f"{key['packet_id']}.json"
    require(stored.read_bytes() == canonical(key),
            "blind review key was changed after export")
    require(packet["keys"][key["packet_id"]] == key,
            "blind review key differs from its stored manifest copy")
    return key, by_alias

def import_reviews(path: Path, review_packet: Path, source_file: Path) -> dict[str, Any]:
    packet = inspect_packet(path)
    key, by_alias = _load_review_packet(review_packet, packet)
    body = read_json(source_file)
    version = 1 if key["format"] == REVIEW_KEY_FORMAT else 2
    require(isinstance(body, dict) and body.get("format") ==
            (REVIEW_FORMAT if version == 1 else REVIEW_FORMAT_V2),
            "unsupported review import format for its blind key")
    require_shape(body, REVIEW_IMPORT_FIELDS, "review import")
    require(isinstance(body["records"], list) and body["records"], "empty review import")
    existing = {(record["input_id"], record["reviewer_id"]) for record in packet["reviews"]}
    existing_attempt_pairs = {
        (record["attempt_id"], record["reviewer_id"])
        for record in packet["reviews"] if version == 2
    }
    records, seen_reviews = [], set()
    seen_attempt_pairs = set()
    for review in body["records"]:
        review = require_shape(review, REVIEW_INPUT_FIELDS if version == 1 else
                               REVIEW_INPUT_FIELDS_V2, "imported review")
        alias = review["alias"]
        require(alias in by_alias, "unknown blind review alias")
        identifier = by_alias[alias]["input_id"]
        reviewer = review["reviewer_id"]
        require(isinstance(reviewer, str) and reviewer.strip() and
                len(reviewer) <= 120, "invalid reviewer ID")
        if version == 1:
            pair = (identifier, reviewer)
            require(pair not in existing and pair not in seen_reviews,
                    "reviewer already reviewed this input")
            existing.add(pair)
            seen_reviews.add(pair)
            _check_review_payload(review, identifier, packet, "imported review")
            require(review["decision"] in by_alias[alias]["item"]["decision_options"],
                    "review decision is not among the exported item options")
            records.append({"alias": alias, "input_id": identifier,
                            "reviewer_id": reviewer, "decision": review["decision"],
                            "reason": review["reason"],
                            "evidence_refs": review["evidence_refs"]})
        else:
            attempt_id = by_alias[alias]["attempt_id"]
            pair = (attempt_id, reviewer)
            require(pair not in existing_attempt_pairs and
                    pair not in seen_attempt_pairs,
                    "reviewer already reviewed this attempt")
            seen_attempt_pairs.add(pair)
            _check_v2_review_payload(
                review, identifier, attempt_id, packet,
                by_alias[alias]["item"]["decision_options"])
            if review["mapping"] == "mapped":
                require(review["decision"] in
                        by_alias[alias]["item"]["decision_options"],
                        "review decision is not among the exported item options")
            records.append({"alias": alias, "input_id": identifier,
                            "attempt_id": attempt_id,
                            "reviewer_id": reviewer,
                            "response_act": review["response_act"],
                            "mapping": review["mapping"],
                            "decision": review["decision"],
                            "reason": review["reason"],
                            "evidence_refs": review["evidence_refs"]})
    dest = _next_batch(packet["folder"], "reviews")
    require(not dest.exists(), "review batch would overwrite an existing record")
    write_new(dest, {"format": REVIEW_FORMAT if version == 1 else REVIEW_FORMAT_V2,
                     "review_key_sha256": digest(canonical(key)),
                     "records": records})
    return {"status": "reviews-imported", "batch": dest.name,
            "records": len(records), "execution": "not-run by this tool"}

def ratio(numerator: int, denominator: int) -> str | None:
    return None if denominator == 0 else inputs.rational_text(Fraction(numerator, denominator))

def counters(packet: dict[str, Any], family_id: str | None = None) -> dict[str, Any]:
    records = packet["manifest"]["records"]
    if family_id is not None:
        records = [record for record in records if record["family"] == family_id]
    reviews_by_input: dict[str, list[dict[str, Any]]] = {}
    reviewed_ids, reviewed_reviewers = set(), set()
    for review in packet["reviews"]:
        if review["input_id"] in {record["input_id"] for record in records}:
            reviews_by_input.setdefault(review["input_id"], []).append(review)
            reviewed_ids.add(review["input_id"])
            reviewed_reviewers.add(review["reviewer_id"])
    response_states = Counter()
    review_pending = 0
    scorable = 0
    disagreements = 0
    correct = incorrect = unmapped = 0
    for record in records:
        response = packet["responses"].get(record["input_id"])
        status = "pending" if response is None else response["status"]
        response_states[status] += 1
        reviews = reviews_by_input.get(record["input_id"], [])
        if status != "completed":
            continue
        if not reviews:
            review_pending += 1
            continue
        scorable += 1
        judgments = []
        for review in reviews:
            if review.get("mapping", "mapped") != "mapped":
                unmapped += 1
                continue
            judgment = review["decision"] in record["answer_region"]
            judgments.append(judgment)
            correct += int(judgment)
            incorrect += int(not judgment)
        mapped_decisions = {review["decision"] for review in reviews
                            if review.get("mapping", "mapped") == "mapped"}
        if len(mapped_decisions) > 1:
            disagreements += 1
    histories = packet["attempt_histories"]
    record_ids = {record["input_id"] for record in records}
    attempts = sum(len(histories.get(identifier, [])) for identifier in record_ids)
    completed = response_states["completed"]
    technical_failure = response_states["technical_failure"]
    attempted = completed + technical_failure
    positions_with_multiple_attempts = 0
    positions_with_completed_history = 0
    for record in records:
        history = histories.get(record["input_id"], [])
        positions_with_multiple_attempts += int(len(history) > 1)
        positions_with_completed_history += int(
            any(row["status"] == "completed" for row in history))
    return {
        "total": len(records),
        "attempted": attempted,
        "attempts": attempts,
        "positions_with_multiple_attempts": positions_with_multiple_attempts,
        "positions_with_completed_history": positions_with_completed_history,
        "completed": completed,
        "scorable": scorable,
        "reviewed_inputs": len(reviewed_ids),
        "reviewers": len(reviewed_reviewers),
        "pending": response_states["pending"],
        "technical_failure": technical_failure,
        "not_run": response_states["not-run"],
        "review_pending": review_pending,
        "attempt_coverage": ratio(attempted, len(records)),
        "answer_coverage": ratio(completed, attempted),
        "judgment_contract_match_rate": ratio(correct, correct + incorrect),
        "judgments": {"correct": correct, "incorrect": incorrect,
                      "total": correct + incorrect},
        "unmapped_judgments": unmapped,
        "judgment_contract_mismatch_rate": ratio(incorrect, correct + incorrect),
        "multi_reviewer_disagreements": disagreements,
    }

def recompute(path: Path) -> dict[str, Any]:
    packet = inspect_packet(path)
    families = {}
    for family in packet["source"]["families"]:
        families[family["id"]] = counters(packet, family["id"])
    return {
        "format": "relata-future-question-review-summary-1",
        "evidence_status": (
            "imported offline responses/reviews; no subject execution by this tool; "
            "not a system score or validated semantic contract"
        ),
        "metric_definitions": {
            "attempted": "current positions completed or technically failed; pending and not-run remain absent",
            "attempts": "all imported attempt records; not independent cases",
            "attempt_coverage": "attempted / total manifested cells",
            "answer_coverage": "completed / attempted; null when attempted is zero",
            "judgment_contract_match_rate": "correct mapped judgments / all mapped judgments on completed responses; not response accuracy",
            "judgment_contract_mismatch_rate": "incorrect mapped judgments / all mapped judgments on completed responses; not response error rate",
            "unmapped_judgments": "non-mapped review diagnostics; not correctness failures",
            "disagreement": "completed inputs whose review decisions are not all identical",
            "scorable": "completed inputs with at least one imported review",
        },
        "history_sha256": packet["manifest"]["history_sha256"],
        "contract_sha256": packet["manifest"]["contract_sha256"],
        "overall": counters(packet),
        "families": families,
    }

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prepare_command = commands.add_parser("prepare", help="create all fixed-cell input files")
    prepare_command.add_argument("output", type=Path)
    verify_command = commands.add_parser("verify", help="re-derive packet and record bindings")
    verify_command.add_argument("packet", type=Path)
    responses_command = commands.add_parser(
        "import-responses", help="append manually supplied response states")
    responses_command.add_argument("packet", type=Path)
    responses_command.add_argument("--input", type=Path, required=True)
    export_command = commands.add_parser(
        "export-review", help="write a blind review packet for completed responses")
    export_command.add_argument("packet", type=Path)
    export_command.add_argument("--output", type=Path, required=True)
    reviews_command = commands.add_parser(
        "import-review", help="append reviews bound to one blind review packet")
    reviews_command.add_argument("packet", type=Path)
    reviews_command.add_argument("--review-packet", type=Path, required=True)
    reviews_command.add_argument("--input", type=Path, required=True)
    recompute_command = commands.add_parser("recompute", help="recompute descriptive statistics")
    recompute_command.add_argument("packet", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "prepare":
            result = prepare(args.output)
        elif args.command == "verify":
            result = verify(args.packet)
        elif args.command == "import-responses":
            result = import_responses(args.packet, args.input)
        elif args.command == "export-review":
            result = export_review(args.packet, args.output)
        elif args.command == "import-review":
            result = import_reviews(args.packet, args.review_packet, args.input)
        else:
            result = recompute(args.packet)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2,
                         allow_nan=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
