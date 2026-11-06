#!/usr/bin/env python3
"""Validate and project the fixed authored authorization representations.

Input-only: no extractor, subject, model or provider is executed. ``show``
returns one common task plus H/P/S/R, separately selected O, or one explicitly
selected deliberate control. ``report`` exposes author-side coverage and exact
UTF-8 byte / Unicode codepoint sizes.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
HISTORIES = HERE / "histories.json"
REPRESENTATIONS = HERE / "representations.json"
STATES = HERE / "representation-states.json"
CONTROLS = HERE / "representation-controls.json"
AUDIT = HERE / "representation-audit.json"
CHECK_HISTORIES = HERE / "check_histories.py"

CONDITIONS = ("H", "P", "S", "R")
CONTROL_CONDITIONS = ("goal_rebinding", "flattened_marginals")
STATE_KEYS = {"acceptance", "grants", "environment", "unresolved"}
ACCEPTANCE_KEYS = {"event", "actor", "referent", "status", "missing"}
GRANT_KEYS = {
    "origin", "scope", "conditions", "uses_before", "use_limit", "validity",
    "semantic_dependency", "per_proposal_acceptance_required", "speaker",
    "authority_capable",
}
GRANT_REQUIRED = {
    "origin", "scope", "conditions", "uses_before", "use_limit", "validity",
}
SCOPE_KEYS = {"verb", "object", "purpose", "surface"}
VALIDITY_KEYS = {
    "status", "valid_until", "event", "includes_boundary", "revoked",
}
SEMANTIC_DEPENDENCY_KEYS = {"origin", "speaker", "fact"}
ENVIRONMENT_KEYS = {
    "artifacts", "bridges", "candidate_referents", "clock", "counters",
    "excluded_proposal", "ineffective_revocation_attempt", "later_proposal",
    "non_authoritative_claim", "owner_statement_at_t02", "project_goal",
    "proposal_status",
    "proposals", "resolved_scope", "shared_project",
    "project_membership_is_not_a_scope_row",
}
BRIDGE_KEYS = {
    "origin", "owner", "artifact", "purpose", "surface", "source", "status",
    "preserves_label",
}
REPRESENTATION_FORMAT = "relata-authorization-representations-2"
AUDIT_FORMAT = "relata-authorization-representation-audit-2"
STATE_FORMAT = "relata-authorization-representation-states-2"
CONTROL_FORMAT = "relata-authorization-representation-controls-1"


def load_history_tool() -> Any:
    spec = importlib.util.spec_from_file_location(
        "authorization_history_validator", CHECK_HISTORIES)
    if spec is None or spec.loader is None:
        raise ValueError("cannot load canonical history validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


histories_tool = load_history_tool()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       indent=2, allow_nan=False) + "\n").encode("utf-8")


def read_json(path: Path) -> dict[str, Any]:
    value = histories_tool.read_json(path)
    require(isinstance(value, dict), f"expected JSON object in {path.name}")
    return value


def exact_fields(value: Any, expected: set[str], label: str) -> None:
    require(isinstance(value, dict), f"{label} must be an object")
    require(set(value) == expected,
            f"invalid fields for {label}: {sorted(set(value) ^ expected)}")


def nonempty_text(value: Any, label: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), f"empty {label}")


def text_list(value: Any, label: str) -> None:
    require(isinstance(value, list), f"{label} must be a list")
    for item in value:
        nonempty_text(item, label)


def boolean(value: Any, label: str) -> None:
    require(type(value) is bool, f"{label} must be boolean")


def nullable_text(value: Any, label: str) -> None:
    if value is not None:
        nonempty_text(value, label)


def ordered_rows(rows: Any, field: str, expected: list[str], label: str) -> None:
    require(isinstance(rows, list) and
            all(isinstance(row, dict) for row in rows) and
            [row.get(field) for row in rows] == expected,
            f"{label} coverage or order differs from source")


def source_hash() -> str:
    return hashlib.sha256(HISTORIES.read_bytes()).hexdigest()


def length_metrics(body: str) -> dict[str, int]:
    return {"bytes": len(body.encode("utf-8")), "codepoints": len(body)}


def source_bundle() -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    source = read_json(HISTORIES)
    return source, histories_tool.validate_history_source(source)


def metadata_roster(history: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "turn_id": turn["turn_id"],
            "speaker": turn["speaker"],
            "role": turn["role"],
            "capability": turn["capability"],
        }
        for turn in history["turns"]
    ]


def validate_representations(
    source: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    bundle = read_json(REPRESENTATIONS)
    exact_fields(bundle, {"format", "status", "source_history_sha256",
                          "author_note", "histories"},
                 "representation bundle")
    require(bundle["format"] == REPRESENTATION_FORMAT,
            "wrong representation format")
    require(bundle["status"] == "author-drafted-offline-unvalidated",
            "representations must remain unvalidated")
    require(bundle["source_history_sha256"] == source_hash(),
            "representation source binding is stale")
    rows = bundle["histories"]
    expected = [history["history_id"] for history in source["histories"]]
    ordered_rows(rows, "history_id", expected, "representation")
    by_id: dict[str, dict[str, Any]] = {}
    for row, history in zip(rows, source["histories"]):
        exact_fields(row, {"history_id", "facts"}, "representation history")
        facts = row["facts"]
        require(isinstance(facts, list) and bool(facts), "empty fact list")
        ids: set[str] = set()
        refs = {turn["turn_id"] for turn in history["turns"]}
        for fact in facts:
            exact_fields(fact, {"fact_id", "source_refs", "prose", "relation"},
                         "representation fact")
            nonempty_text(fact["fact_id"], "fact ID")
            require(fact["fact_id"] not in ids, "duplicate fact ID")
            ids.add(fact["fact_id"])
            text_list(fact["source_refs"], "source refs")
            require(bool(fact["source_refs"]), "fact has no source refs")
            require(len(fact["source_refs"]) == len(set(fact["source_refs"])),
                    "duplicate source ref")
            require(set(fact["source_refs"]) <= refs,
                    "fact has dangling source ref")
            nonempty_text(fact["prose"], "P fact")
            nonempty_text(fact["relation"], "R fact")
        by_id[row["history_id"]] = row
    return by_id


def validate_scope(scope: Any, label: str) -> None:
    exact_fields(scope, SCOPE_KEYS, label)
    for key in SCOPE_KEYS:
        nonempty_text(scope[key], f"{label}.{key}")


def validate_environment(value: Any) -> None:
    require(isinstance(value, dict), "O environment must be an object")
    require(set(value) <= ENVIRONMENT_KEYS,
            "O environment has unknown fields")
    for key in ("clock", "excluded_proposal", "owner_statement_at_t02",
                "project_goal", "proposal_status", "resolved_scope"):
        if key in value:
            nonempty_text(value[key], key)
    for key in ("shared_project", "project_membership_is_not_a_scope_row"):
        if key in value:
            boolean(value[key], key)
    for key in ("candidate_referents", "proposals"):
        if key in value:
            text_list(value[key], key)
    if "artifacts" in value:
        require(isinstance(value["artifacts"], dict), "invalid artifacts")
        for artifact, details in value["artifacts"].items():
            nonempty_text(artifact, "artifact ID")
            exact_fields(details, {"labels", "parents", "private_diary_lineage"},
                         "artifact state")
            text_list(details["labels"], "artifact labels")
            text_list(details["parents"], "artifact parents")
            boolean(details["private_diary_lineage"], "private_diary_lineage")
    if "bridges" in value:
        require(isinstance(value["bridges"], list), "invalid bridges")
        for bridge in value["bridges"]:
            exact_fields(bridge, BRIDGE_KEYS, "bridge")
            for key in BRIDGE_KEYS - {"preserves_label"}:
                nonempty_text(bridge[key], f"bridge.{key}")
            boolean(bridge["preserves_label"], "preserves_label")
    if "counters" in value:
        require(isinstance(value["counters"], dict), "invalid counters")
        for counter, details in value["counters"].items():
            nonempty_text(counter, "counter ID")
            exact_fields(details, {"limit", "spent_before"}, counter)
            for key, count in details.items():
                require(type(count) is int and count >= 0,
                        f"invalid counter {key}")
    if "later_proposal" in value:
        proposal = value["later_proposal"]
        exact_fields(proposal, {"id", "accepted"}, "later proposal")
        nonempty_text(proposal["id"], "proposal ID")
        boolean(proposal["accepted"], "proposal accepted")
    for key in ("ineffective_revocation_attempt", "non_authoritative_claim"):
        if key in value:
            exact_fields(value[key], {"origin", "speaker"}, key)
            for field, content in value[key].items():
                nonempty_text(content, f"{key}.{field}")


def validate_states(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    bundle = read_json(STATES)
    exact_fields(bundle, {"format", "status", "source_history_sha256",
                          "author_note", "states"}, "state bundle")
    require(bundle["format"] == STATE_FORMAT, "wrong state format")
    require(bundle["status"] == "author-drafted-offline-unvalidated",
            "O states must remain unvalidated")
    require(bundle["source_history_sha256"] == source_hash(),
            "state source binding is stale")
    rows = bundle["states"]
    expected = [history["history_id"] for history in source["histories"]]
    ordered_rows(rows, "history_id", expected, "O")
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        exact_fields(row, {"history_id", "state"}, "O state row")
        state = row["state"]
        require(isinstance(state, dict), "O state must be an object")
        require(set(state) <= STATE_KEYS, "O state has unknown fields")
        require({"grants", "environment", "unresolved"} <= set(state),
                "O state is incomplete")
        require(isinstance(state["grants"], list), "O grants must be a list")
        text_list(state["unresolved"], "unresolved")
        validate_environment(state["environment"])
        if "acceptance" in state:
            acceptance = state["acceptance"]
            require(isinstance(acceptance, dict), "invalid acceptance")
            require(set(acceptance) <= ACCEPTANCE_KEYS,
                    "acceptance has unknown fields")
            require({"event", "actor", "referent", "status"} <=
                    set(acceptance), "acceptance is incomplete")
            nonempty_text(acceptance["status"], "acceptance status")
            for key in ACCEPTANCE_KEYS - {"status"}:
                if key in acceptance:
                    nullable_text(acceptance[key], f"acceptance.{key}")
        for grant in state["grants"]:
            require(isinstance(grant, dict), "grant must be an object")
            require(set(grant) <= GRANT_KEYS, "grant has unknown fields")
            require(GRANT_REQUIRED <= set(grant), "grant is incomplete")
            text_list(grant["origin"], "grant origin")
            require(bool(grant["origin"]), "grant has no origin")
            text_list(grant["conditions"], "grant conditions")
            if "speaker" in grant:
                nonempty_text(grant["speaker"], "grant speaker")
            if "authority_capable" in grant and grant["authority_capable"] is not None:
                boolean(grant["authority_capable"], "authority_capable")
            if "per_proposal_acceptance_required" in grant:
                boolean(grant["per_proposal_acceptance_required"],
                        "per_proposal_acceptance_required")
            require(type(grant["uses_before"]) is int and
                    grant["uses_before"] >= 0, "invalid uses_before")
            require(grant["use_limit"] is None or
                    type(grant["use_limit"]) is int and grant["use_limit"] >= 0,
                    "invalid use_limit")
            require(isinstance(grant["scope"], list) and grant["scope"],
                    "grant has no scope")
            for scope in grant["scope"]:
                validate_scope(scope, "grant scope")
            validity = grant["validity"]
            require(isinstance(validity, dict) and "status" in validity and
                    set(validity) <= VALIDITY_KEYS, "invalid validity")
            nonempty_text(validity["status"], "validity status")
            for key in ("event", "valid_until"):
                if key in validity:
                    nullable_text(validity[key], f"validity.{key}")
            for key in ("includes_boundary", "revoked"):
                if key in validity:
                    boolean(validity[key], f"validity.{key}")
            if "semantic_dependency" in grant:
                exact_fields(grant["semantic_dependency"],
                             SEMANTIC_DEPENDENCY_KEYS, "semantic dependency")
                for key, content in grant["semantic_dependency"].items():
                    nonempty_text(content, f"semantic dependency.{key}")
        by_id[row["history_id"]] = row
    return by_id


def validate_controls(source: dict[str, Any]) -> dict[str, dict[str, Any]]:
    bundle = read_json(CONTROLS)
    exact_fields(bundle, {"format", "status", "source_history_sha256",
                          "author_note", "controls"}, "control bundle")
    require(bundle["format"] == CONTROL_FORMAT, "wrong controls format")
    require(bundle["status"] == "author-drafted-deliberate-distortion",
            "controls must be deliberate distortions")
    require(bundle["source_history_sha256"] == source_hash(),
            "control source binding is stale")
    controls = bundle["controls"]
    ordered_rows(controls, "control_id", list(CONTROL_CONDITIONS), "control")
    by_id: dict[str, dict[str, Any]] = {}
    for control in controls:
        exact_fields(control, {
            "control_id", "applicable_history_ids", "mechanism", "variants",
            "corruption", "confounds",
        }, "control")
        ids = control["applicable_history_ids"]
        variants = control["variants"]
        text_list(ids, "control IDs")
        require(isinstance(variants, dict) and
                set(ids) == set(variants), "control IDs and variants differ")
        source_ids = {history["history_id"] for history in source["histories"]}
        require(set(ids) <= source_ids, "control has dangling history ID")
        for history_id in ids:
            nonempty_text(variants[history_id], "control memory")
        for field in ("corruption", "confounds"):
            require(isinstance(control[field], list) and control[field],
                    f"control has no {field}")
        by_id[control["control_id"]] = control
    require(by_id["goal_rebinding"]["applicable_history_ids"] ==
            ["hist-ef80f8ff5f05"], "goal_rebinding witness mismatch")
    require(by_id["flattened_marginals"]["applicable_history_ids"] == [
        "hist-2c7f217a3e94", "hist-9c680d06c3b1",
        "hist-79f3ad41ad1f", "hist-a87beb01b97b",
    ], "flattened_marginals witness mismatch")
    return by_id


def validate_audit(source: dict[str, Any],
                   representations: dict[str, dict[str, Any]]) -> None:
    bundle = read_json(AUDIT)
    exact_fields(bundle, {"format", "status", "source_history_sha256",
                          "representation_sha256", "method_note", "histories"},
                 "audit bundle")
    require(bundle["format"] == AUDIT_FORMAT, "wrong audit format")
    require(bundle["status"] == "author-drafted-offline-unvalidated",
            "audit must remain unvalidated")
    require(bundle["source_history_sha256"] == source_hash(),
            "audit source binding is stale")
    require(bundle["representation_sha256"] == hashlib.sha256(
        canonical(list(representations.values()))).hexdigest(),
        "audit representation binding is stale")
    rows = bundle["histories"]
    expected = [history["history_id"] for history in source["histories"]]
    ordered_rows(rows, "history_id", expected, "audit")
    history_by_id = {history["history_id"]: history
                     for history in source["histories"]}
    for row in rows:
        exact_fields(row, {"history_id", "coverage_claim", "facts"},
                     "audit history")
        authored = representations[row["history_id"]]["facts"]
        facts = row["facts"]
        require(isinstance(facts, list) and len(facts) == len(authored),
                "audit fact count differs")
        history = history_by_id[row["history_id"]]
        for audit_fact, fact in zip(facts, authored):
            exact_fields(audit_fact, {
                "fact_id", "source_refs", "source_witnesses",
                "prose_witness", "relation_witness",
            }, "audit fact")
            require(audit_fact["fact_id"] == fact["fact_id"],
                    "audit fact order differs")
            require(audit_fact["source_refs"] == fact["source_refs"],
                    "audit refs differ")
            require(audit_fact["prose_witness"] == fact["prose"],
                    "P witness differs")
            require(audit_fact["relation_witness"] == fact["relation"],
                    "R witness differs")
            witnesses = audit_fact["source_witnesses"]
            require(isinstance(witnesses, list) and
                    all(isinstance(item, dict) for item in witnesses) and
                    [item.get("ref") for item in witnesses] ==
                    fact["source_refs"], "source witness refs differ")
            for witness in witnesses:
                exact_fields(witness, {"ref", "field", "quote"},
                             "source witness")
                require(witness["field"] == "text", "invalid witness field")
                target = next(item for item in history["turns"]
                              if item["turn_id"] == witness["ref"])
                require(target["text"] == witness["quote"],
                        "quote does not match named source ref")


def validate_bundle() -> tuple[dict[str, Any], dict[str, dict[str, Any]],
                               dict[str, dict[str, Any]],
                               dict[str, dict[str, Any]],
                               dict[str, dict[str, Any]]]:
    source, histories = source_bundle()
    representations = validate_representations(source)
    states = validate_states(source)
    controls = validate_controls(source)
    validate_audit(source, representations)
    return source, histories, representations, states, controls


def task_projection(history: dict[str, Any]) -> dict[str, Any]:
    request = history["current_request"]
    return {
        "background": history["background"],
        "metadata": metadata_roster(history),
        "candidate_mode": history["candidate_mode"],
        "candidate_instruction": history["candidate_instruction"],
        "current_request": {
            key: request[key] for key in
            ("speaker", "role", "capability", "text")
        },
        "candidate_actions": [
            {key: action[key] for key in ("candidate_id", "step", "text")}
            for action in history["candidate_actions"]
        ],
    }


def prose(facts: list[dict[str, Any]]) -> str:
    return " ".join(fact["prose"] for fact in facts)


def attribution(facts: list[dict[str, Any]]) -> str:
    return " ".join(
        f"{fact['prose']} [source: {', '.join(fact['source_refs'])}]"
        for fact in facts
    )


def relational(facts: list[dict[str, Any]]) -> str:
    return "\n".join(
        f"{fact['fact_id']} [source: {', '.join(fact['source_refs'])}]: "
        f"{fact['relation']}" for fact in facts
    )


def history_memory(history: dict[str, Any]) -> str:
    lines = [f"Background: {history['background']}"]
    lines.extend(
        f"{turn['turn_id']} {turn['speaker']} / {turn['role']} "
        f"[capability: {turn['capability']}]: {turn['text']}"
        for turn in history["turns"]
    )
    return "\n".join(lines)


def memory_body(condition: str, history: dict[str, Any],
                facts: list[dict[str, Any]]) -> str:
    if condition == "H":
        return history_memory(history)
    if condition == "P":
        return prose(facts)
    if condition == "S":
        return attribution(facts)
    if condition == "R":
        return relational(facts)
    raise ValueError("unknown faithful condition")


def projection(source: dict[str, Any], history: dict[str, Any],
               state_or_body: str, value: Any) -> dict[str, Any]:
    return {
        "scene": source["scene"],
        "task": task_projection(history),
        state_or_body: value,
    }


def show(history_id: str, condition: str) -> dict[str, Any]:
    source, histories = source_bundle()
    require(condition in CONDITIONS + ("O",) + CONTROL_CONDITIONS,
            "unknown condition")
    require(history_id in histories, "unknown history ID")
    history = histories[history_id]
    if condition == "O":
        state = validate_states(source)[history_id]
        return projection(source, history, "state", state["state"])
    if condition in CONTROL_CONDITIONS:
        control = validate_controls(source)[condition]
        require(history_id in control["applicable_history_ids"],
                f"{condition} is not applicable to this history")
        return projection(source, history, "memory_body",
                          control["variants"][history_id])
    facts = validate_representations(source)[history_id]["facts"]
    return projection(source, history, "memory_body",
                      memory_body(condition, history, facts))


def report() -> dict[str, Any]:
    source, histories, representations, states, controls = validate_bundle()
    sizes: dict[str, list[dict[str, Any]]] = {
        condition: [] for condition in CONDITIONS}
    full: dict[str, list[dict[str, Any]]] = {
        condition: [] for condition in CONDITIONS}
    for history_id in histories:
        for condition in CONDITIONS:
            item = show(history_id, condition)
            sizes[condition].append({
                "history_id": history_id,
                "memory": length_metrics(item["memory_body"]),
            })
            full[condition].append({
                "history_id": history_id,
                "projection": length_metrics(canonical(item).decode("utf-8")),
            })
    ratios = []
    for index, history_id in enumerate(histories):
        row: dict[str, Any] = {"history_id": history_id}
        for condition in ("S", "R"):
            row[f"{condition}_to_P"] = {}
            for layer, table in (("memory", sizes), ("projection", full)):
                p = table["P"][index][layer]
                other = table[condition][index][layer]
                row[f"{condition}_to_P"][layer] = {
                    metric: round(other[metric] / p[metric], 6)
                    for metric in ("bytes", "codepoints")
                }
        ratios.append(row)
    o_sizes = []
    for history_id in histories:
        item = show(history_id, "O")
        o_sizes.append({
            "history_id": history_id,
            "memory": length_metrics(
                canonical(states[history_id]["state"]).decode("utf-8")),
            "projection": length_metrics(canonical(item).decode("utf-8")),
        })
    return {
        "status": "valid-authored-representation-preparation",
        "histories": 32,
        "faithful_representations": 96,
        "o_states": 32,
        "controls": {key: len(value["applicable_history_ids"])
                     for key, value in controls.items()},
        "source_history_sha256": source_hash(),
        "sizes": sizes,
        "full_projection": full,
        "paired_S_R_to_P": ratios,
        "O_sizes": o_sizes,
        "control_sizes": {
            key: [
                {"history_id": history_id,
                 "memory": length_metrics(show(history_id, key)["memory_body"]),
                 "projection": length_metrics(
                     canonical(show(history_id, key)).decode("utf-8"))}
                for history_id in control["applicable_history_ids"]
            ] for key, control in controls.items()
        },
        "note": ("UTF-8 bytes and Unicode codepoints only. No tokenizer was "
                 "selected; counts are not tokens or dispatch receipts. "
                 "Semantic equality remains an author claim."),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("check", help="validate fixed inputs (default)")
    show_parser = sub.add_parser("show", help="emit one selected input")
    show_parser.add_argument("history_id")
    show_parser.add_argument("condition", choices=CONDITIONS + ("O",) +
                             CONTROL_CONDITIONS)
    sub.add_parser("report", help="emit author-side observations")
    args = parser.parse_args(argv)
    try:
        if args.command == "show":
            sys.stdout.buffer.write(canonical(show(args.history_id, args.condition)))
        elif args.command == "report":
            sys.stdout.buffer.write(canonical(report()))
        else:
            _, histories, representations, states, controls = validate_bundle()
            sys.stdout.buffer.write(canonical({
                "status": "valid-authored-representation-preparation",
                "histories": len(histories),
                "faithful_representations": len(representations) * 3,
                "o_states": len(states),
                "controls": {key: len(value["applicable_history_ids"])
                             for key, value in controls.items()},
                "source_history_sha256": source_hash(),
                "note": ("Structure and source witnesses only; no semantic "
                         "equivalence or model behavior is established."),
            }))
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
