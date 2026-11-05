#!/usr/bin/env python3
"""Validate authored authorization histories and project one writer-visible history.

This fixed-bundle tool performs no subject execution or natural-language
scoring. Default ``check`` compares the source histories to the separate author
oracle and validates detailed trace/reference shape. ``show`` reads only
histories.json and emits an allowlisted, unlabelled writer projection.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
HISTORIES = HERE / "histories.json"
ORACLES = HERE / "history-oracles.json"
FIXTURES = HERE / "fixtures.json"
LIMIT = 2_000_000

FAMILY_IDS = tuple(f"F{i}" for i in range(1, 9))
VARIANT_IDS = tuple(f"V{i}" for i in range(1, 5))
DECISIONS = {"allow", "deny", "unknown"}
TRACE_DECISIONS = DECISIONS | {"not_run"}
SPEAKER_ROLES = {
    "A": "assistant",
    "U": "project-owner",
    "R": "requester",
    "C": "colleague",
    "S": "contributor",
}
HISTORY_FIELDS = {
    "history_id", "background", "candidate_mode",
    "candidate_instruction", "turns", "current_request", "candidate_actions"
}
PROJECTION_FIELDS = HISTORY_FIELDS | {"scene"}
TURN_FIELDS = {"sequence", "turn_id", "speaker", "role", "capability", "text"}
REQUEST_FIELDS = {"speaker", "role", "capability", "text"}
ACTION_FIELDS = {"candidate_id", "step", "text"}
ORACLE_FIELDS = {"format", "status", "relationship_to_fixtures",
                 "trace_semantics", "families"}
ORACLE_FAMILY_FIELDS = {"family_id", "title", "matrix", "fixture_witnesses",
                        "non_equivalence", "variants"}
ORACLE_VARIANT_FIELDS = {
    "variant_id", "label", "history_id", "rationale", "grant_interpretation",
    "citation_anchors", "unknown_conditions", "author_decisions",
}
TRACE_FIELDS = {"step", "candidate_id", "decision", "reason"}
CANDIDATE_MODES = {"independent_eligibility", "ordered_prefix"}

AUTHOR_ONLY_KEYS = {
    "expected", "oracle", "label", "family_id", "variant_id", "rationale",
    "grant_interpretation", "citation_anchors", "unknown_conditions", "trace",
    "fixture_witnesses", "non_equivalence", "answer", "correct",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       indent=2, allow_nan=False) + "\n").encode("utf-8")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON field")
        result[key] = value
    return result


def read_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(),
            f"missing or symlinked bundled file: {path.name}")
    require(path.stat().st_size < LIMIT, f"bundled file too large: {path.name}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"),
                           object_pairs_hook=unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid JSON in {path.name}: {error}") from error
    require(isinstance(value, dict), f"expected JSON object in {path.name}")
    return value


def exact_fields(value: Any, expected: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label} must be an object")
    require(set(value) == expected, f"invalid fields for {label}: {sorted(set(value) ^ expected)}")


def nonempty_text(value: Any, label: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), f"empty {label}")


def validate_history_source(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    exact_fields(source, {"format", "status", "provenance", "scene", "histories"},
                 "history bundle")
    require(source["format"] == "relata-authorization-histories-1",
            "wrong history format")
    require(source["status"] == "authored-offline-unvalidated",
            "history source must remain explicitly unvalidated")
    for field in ("provenance", "scene"):
        nonempty_text(source[field], field)
    histories = source["histories"]
    require(isinstance(histories, list) and len(histories) == 32,
            "expected exactly 32 histories")
    by_id: dict[str, dict[str, Any]] = {}
    for history in histories:
        exact_fields(history, HISTORY_FIELDS, "history")
        history_id = history["history_id"]
        require(isinstance(history_id, str) and
                len(history_id) == 17 and
                history_id.startswith("hist-") and
                all(character in "0123456789abcdef"
                    for character in history_id[5:]),
                "opaque history ID must be hist- plus 12 lowercase hex digits")
        require(history_id not in by_id, f"duplicate history ID: {history_id}")
        by_id[history_id] = history
        nonempty_text(history["background"], f"{history_id} background")
        require(history["candidate_mode"] in CANDIDATE_MODES,
                f"{history_id} invalid candidate mode")
        nonempty_text(history["candidate_instruction"],
                      f"{history_id} candidate instruction")
        if history["candidate_mode"] == "independent_eligibility":
            require("不要执行" in history["candidate_instruction"],
                    f"{history_id} independent instruction must prohibit execution")
        else:
            require("顺序" in history["candidate_instruction"] and
                    "停止" in history["candidate_instruction"],
                    f"{history_id} ordered instruction must state order and stop")
        turns = history["turns"]
        require(isinstance(turns, list) and bool(turns), f"{history_id} has no turns")
        turn_ids: set[str] = set()
        for expected_sequence, turn in enumerate(turns, 1):
            exact_fields(turn, TURN_FIELDS, f"{history_id} turn")
            require(turn["sequence"] == expected_sequence,
                    f"{history_id} turn structural order is not contiguous")
            turn_id = turn["turn_id"]
            require(turn_id == f"t{expected_sequence:02d}",
                    f"{history_id} turn ID does not match structural order")
            require(turn_id not in turn_ids, f"duplicate turn ID in {history_id}")
            turn_ids.add(turn_id)
            require(turn["speaker"] in SPEAKER_ROLES, "unknown speaker")
            require(turn["role"] == SPEAKER_ROLES[turn["speaker"]],
                    f"role does not match speaker in {history_id}/{turn_id}")
            nonempty_text(turn["capability"], f"{history_id}/{turn_id} capability")
            nonempty_text(turn["text"], f"{history_id}/{turn_id} text")
            for key in AUTHOR_ONLY_KEYS:
                require(key not in turn, f"author-only key {key} in writer input")
        request = history["current_request"]
        exact_fields(request, REQUEST_FIELDS, f"{history_id} current request")
        require(request["speaker"] in SPEAKER_ROLES, "unknown requester")
        require(request["role"] == SPEAKER_ROLES[request["speaker"]],
                f"request role does not match speaker in {history_id}")
        nonempty_text(request["capability"], f"{history_id} request capability")
        nonempty_text(request["text"], f"{history_id} request text")
        actions = history["candidate_actions"]
        require(isinstance(actions, list) and bool(actions),
                f"{history_id} has no candidate actions")
        candidate_ids: set[str] = set()
        for expected_step, action in enumerate(actions, 1):
            exact_fields(action, ACTION_FIELDS, f"{history_id} candidate")
            require(action["step"] == expected_step,
                    f"{history_id} candidate structural order is not contiguous")
            require(isinstance(action["candidate_id"], str) and
                    action["candidate_id"].startswith("a") and
                    action["candidate_id"][1:].isdigit() and
                    len(action["candidate_id"]) == 3,
                    "invalid candidate ID")
            require(action["candidate_id"] not in candidate_ids,
                    f"duplicate candidate ID in {history_id}")
            candidate_ids.add(action["candidate_id"])
            nonempty_text(action["text"], f"{history_id} candidate text")
            for key in AUTHOR_ONLY_KEYS:
                require(key not in action,
                        f"author-only key {key} in writer candidate")
        blob = canonical(history)
        for canary in (b"expected", b"oracle", b"rationale",
                       b"grant_interpretation", b"fixture_witnesses",
                       b'"allow"', b'"deny"', b'"unknown"', b'"not_run"'):
            require(canary not in blob,
                    f"author-only content leaked into writer history {history_id}")
    return by_id


def fixture_ids() -> set[str]:
    fixtures = read_json(FIXTURES)
    cases = fixtures.get("cases")
    require(isinstance(cases, list) and len(cases) == 32,
            "state fixture bundle is not the expected fixed bundle")
    ids = {case.get("id") for case in cases}
    require(len(ids) == 32 and all(isinstance(item, str) for item in ids),
            "invalid state fixture IDs")
    return ids


def validate_trace(trace: Any, actions: list[dict[str, Any]],
                   history_id: str, *, require_all: bool = False,
                   stop_after_none: bool = True) -> None:
    require(isinstance(trace, list) and bool(trace), f"{history_id} empty trace")
    require(len(trace) <= len(actions), f"{history_id} trace longer than candidates")
    if require_all:
        require(len(trace) == len(actions),
                f"{history_id} trace must account for every candidate")
    seen_stop = False
    for expected_step, row in enumerate(trace, 1):
        exact_fields(row, TRACE_FIELDS, f"{history_id} trace row")
        action = actions[expected_step - 1]
        require(row["step"] == expected_step and
                row["candidate_id"] == action["candidate_id"],
                f"{history_id} trace does not follow candidate step order")
        require(row["decision"] in TRACE_DECISIONS,
                f"{history_id} invalid trace decision")
        nonempty_text(row["reason"], f"{history_id} trace reason")
        if stop_after_none:
            if seen_stop:
                require(row["decision"] == "not_run",
                        f"{history_id} resumed after a non-allow step")
            else:
                require(row["decision"] != "not_run",
                        f"{history_id} skipped an action before a stop")
                if row["decision"] != "allow":
                    seen_stop = True
    if stop_after_none and any(row["decision"] != "allow" for row in trace):
        stop = next(i for i, row in enumerate(trace)
                    if row["decision"] != "allow")
        require(all(row["decision"] == "not_run" for row in trace[stop + 1:]),
                f"{history_id} later actions are not marked not_run")
    if not stop_after_none:
        require(all(row["decision"] != "not_run" for row in trace),
                f"{history_id} independent eligibility contains not_run")
    require(any(row["decision"] != "not_run" for row in trace),
            f"{history_id} has no evaluated action")


def validate_oracle(oracle: dict[str, Any],
                    histories: dict[str, dict[str, Any]],
                    valid_fixture_ids: set[str]) -> dict[str, Any]:
    exact_fields(oracle, ORACLE_FIELDS, "oracle bundle")
    require(oracle["format"] == "relata-authorization-history-oracles-1",
            "wrong oracle format")
    require(oracle["status"] == "author-authored-unvalidated",
            "oracle must remain explicitly unvalidated")
    require(isinstance(oracle["relationship_to_fixtures"], str) and
            "not" in oracle["relationship_to_fixtures"],
            "missing fixture non-equivalence statement")
    semantics = oracle["trace_semantics"]
    require(isinstance(semantics, list) and len(semantics) == 6,
            "trace semantics must state all six rules")
    require(any("not_run" in text for text in semantics) and
            any("unknown" in text and "deny" in text for text in semantics),
            "trace semantics do not distinguish stop and unknown")
    require(any("independent_eligibility" in text and
                "ordered_prefix" in text for text in semantics),
            "trace semantics do not distinguish candidate modes")
    families = oracle["families"]
    require(isinstance(families, list) and len(families) == 8,
            "expected exactly eight oracle families")
    require(tuple(f["family_id"] for f in families) == FAMILY_IDS,
            "oracle families are not F1-F8 in order")
    used_histories: set[str] = set()
    variant_index: dict[tuple[str, str], dict[str, Any]] = {}
    counts = {"families": 8, "histories": 32, "candidate_positions": 0,
              "evaluated_decisions": 0, "not_run_positions": 0,
              "allow": 0, "deny": 0, "unknown": 0}
    for family in families:
        exact_fields(family, ORACLE_FAMILY_FIELDS, "oracle family")
        fid = family["family_id"]
        for field in ("title", "matrix", "non_equivalence"):
            nonempty_text(family[field], f"{fid} {field}")
        witnesses = family["fixture_witnesses"]
        require(isinstance(witnesses, list) and bool(witnesses),
                f"{fid} has no fixture witnesses")
        for witness in witnesses:
            exact_fields(witness, {"fixture_id", "mechanism"}, f"{fid} witness")
            require(witness["fixture_id"] in valid_fixture_ids,
                    f"{fid} references unknown fixture {witness['fixture_id']}")
            nonempty_text(witness["mechanism"], f"{fid} witness mechanism")
        variants = family["variants"]
        require(isinstance(variants, list) and len(variants) == 4,
                f"{fid} must have four variants")
        require(tuple(v["variant_id"] for v in variants) == VARIANT_IDS,
                f"{fid} variants are not V1-V4 in order")
        for variant in variants:
            exact_fields(variant, ORACLE_VARIANT_FIELDS, "oracle variant")
            key = (fid, variant["variant_id"])
            variant_index[key] = variant
            history_id = variant["history_id"]
            require(history_id in histories,
                    f"{fid}/{variant['variant_id']} has dangling history ID")
            require(history_id not in used_histories,
                    f"history {history_id} is mapped more than once")
            used_histories.add(history_id)
            for field in ("label", "rationale", "grant_interpretation"):
                nonempty_text(variant[field], f"{fid}/{variant['variant_id']} {field}")
            history = histories[history_id]
            anchors = variant["citation_anchors"]
            require(isinstance(anchors, list) and bool(anchors),
                    f"{history_id} has no citation anchors")
            refs = {turn["turn_id"] for turn in history["turns"]}
            refs |= {action["candidate_id"]
                     for action in history["candidate_actions"]}
            require(len(anchors) == len(set(anchors)),
                    f"{history_id} has duplicate citation anchors")
            require(set(anchors) <= refs,
                    f"{history_id} has a dangling citation anchor")
            ordered_refs = [turn["turn_id"] for turn in history["turns"]]
            ordered_refs += [action["candidate_id"]
                             for action in history["candidate_actions"]]
            listed = [ref for ref in ordered_refs if ref in set(anchors)]
            require(anchors == listed,
                    f"{history_id} citation anchors are not in source order")
            unknown_conditions = variant["unknown_conditions"]
            require(isinstance(unknown_conditions, list) and
                    len(unknown_conditions) == len(set(unknown_conditions)),
                    f"{history_id} invalid unknown condition list")
            decisions = variant["author_decisions"]
            validate_trace(
                decisions, history["candidate_actions"], history_id,
                require_all=True,
                stop_after_none=(
                    history["candidate_mode"] == "ordered_prefix"))
            decision_words = [row["decision"] for row in decisions]
            if "unknown" in decision_words:
                require(unknown_conditions,
                        f"{history_id} has unknown decisions without named conditions")
            else:
                require(not unknown_conditions,
                        f"{history_id} names unknown conditions without unknown decision")
            counts["candidate_positions"] += len(history["candidate_actions"])
            counts["evaluated_decisions"] += sum(d in DECISIONS
                                                 for d in decision_words)
            counts["not_run_positions"] += sum(d == "not_run"
                                               for d in decision_words)
            for decision in DECISIONS:
                counts[decision] += decision_words.count(decision)
    expected_histories = set(histories)
    require(used_histories == expected_histories,
            "history/oracle join is not bijective")
    require(len(variant_index) == 32, "oracle family/variant coverage is incomplete")
    require(counts["evaluated_decisions"] ==
            counts["allow"] + counts["deny"] + counts["unknown"],
            "evaluated decisions do not partition")
    require(counts["candidate_positions"] ==
            counts["evaluated_decisions"] + counts["not_run_positions"],
            "candidate positions must equal decisions plus not_run")
    return counts


def check_bundle() -> dict[str, Any]:
    histories = validate_history_source(read_json(HISTORIES))
    counts = validate_oracle(read_json(ORACLES), histories, fixture_ids())
    return {
        "status": "valid-authored-offline-material",
        **counts,
        "note": "Checks establish bundle consistency only; no semantic truth, writer or executor behavior is measured.",
    }


def writer_projection(scene: str, history: dict[str, Any]) -> dict[str, Any]:
    """Return only writer-specified fields from one source history."""
    projection = {
        "scene": scene,
        "history_id": history["history_id"],
        "background": history["background"],
        "candidate_mode": history["candidate_mode"],
        "candidate_instruction": history["candidate_instruction"],
        "turns": [
            {field: turn[field] for field in
             ("sequence", "turn_id", "speaker", "role", "capability", "text")}
            for turn in history["turns"]
        ],
        "current_request": {
            field: history["current_request"][field]
            for field in ("speaker", "role", "capability", "text")
        },
        "candidate_actions": [
            {field: action[field] for field in
             ("candidate_id", "step", "text")}
            for action in history["candidate_actions"]
        ],
    }
    require(set(projection) == PROJECTION_FIELDS, "projection field drift")
    return projection


def show(history_id: str) -> dict[str, Any]:
    source = read_json(HISTORIES)
    histories = validate_history_source(source)
    require(history_id in histories, "unknown history ID")
    return writer_projection(source["scene"], histories[history_id])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("check", help="validate source and author oracle (default)")
    show_parser = sub.add_parser("show", help="emit one writer-visible history")
    show_parser.add_argument("history_id")
    args = parser.parse_args(argv)
    try:
        if args.command == "show":
            sys.stdout.buffer.write(canonical(show(args.history_id)))
        else:
            print(canonical(check_bundle()).decode(), end="")
        return 0
    except (ValueError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
