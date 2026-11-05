#!/usr/bin/env python3
"""Finite authorization diagnostics; no model, provider, or external action.

These are deliberately stipulated policy models, not a deployed authorization
service. Fixture roots, scope, clocks, input labels, and policy ownership are
assumed known. The JSON is local research input, not a canonical Relata schema.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import platform

HERE = Path(__file__).resolve().parent
FIELDS = ("verb", "object", "purpose", "surface")
POLICIES = (
    "current_turn_only",
    "origin_purity",
    "goal_only_acceptance",
    "marginal_join",
    "local_tuple_only",
    "witness_and_trace",
)
BASE_HEAD = "5d103c2d9cca473a8726eafd36555d299d228946"


def digest(value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def proposal_digest(proposal):
    # Identity binds the complete operative proposal content, including all
    # alternatives/constraints carried here; authorship is not grant authority.
    return digest({k: proposal[k] for k in ("id", "version", "goal", "permissions", "conditions") if k in proposal})


def root_state(grant, now, policy):
    root = grant["root"]
    authority = root.get("authority_capable")
    if authority is False:
        return "deny", "root_lacks_relevant_authority"
    if authority is not True:
        return "unknown", "root_authority_not_established"
    if grant.get("status", "active") != "active":
        return "deny", "grant_not_active"
    if now < grant.get("valid_from", -10**9):
        return "deny", "grant_not_yet_valid"
    if now >= grant.get("valid_until", 10**9):
        return "deny", "grant_expired"
    if policy == "current_turn_only" and not root.get("current_turn", False):
        return "deny", "older_root_excluded"
    return "allow", "root_valid"


def resolve(grant, case, policy):
    state, why = root_state(grant, case.get("now", 5), policy)
    if state != "allow":
        return state, None, why
    resolved = copy.deepcopy(grant)
    dependencies = list(grant.get("semantic_dependencies", []))
    if grant.get("kind", "direct") == "acceptance":
        proposals = case.get("proposals", [])
        if policy == "goal_only_acceptance":
            candidates = [p for p in proposals if p["goal"] == grant["goal"]]
            proposal = max(candidates, key=lambda p: p["version"]) if candidates else None
        else:
            if grant.get("binding_ambiguous", False):
                return "unknown", None, "acceptance_reference_ambiguous"
            ref = grant["proposal_ref"]
            candidates = [p for p in proposals if p["id"] == ref["id"] and p["version"] == ref["version"]]
            proposal = candidates[0] if len(candidates) == 1 else None
        if proposal is None:
            return "unknown", None, "accepted_proposal_missing_or_nonunique"
        # The goal-only ablation intentionally substitutes a goal-compatible
        # latest proposal for the accepted reference. Other policies bind exact
        # identity. This is a formal error model, not an extraction algorithm.
        if policy != "goal_only_acceptance" and proposal_digest(proposal) != grant["proposal_ref"]["digest"]:
            return "unknown", None, "proposal_identity_mismatch"
        resolved["permissions"] = copy.deepcopy(proposal["permissions"])
        resolved["conditions"] = copy.deepcopy(proposal.get("conditions", [])) + copy.deepcopy(grant.get("conditions", []))
        dependencies.append({"id": f"{proposal['id']}@{proposal['version']}", "authority_capable": proposal.get("authority_capable", False)})
        resolved["resolved_proposal"] = f"{proposal['id']}@{proposal['version']}"
    if policy == "origin_purity":
        if any(d.get("authority_capable") is False for d in dependencies):
            return "deny", None, "non_authoritative_semantic_operand_excluded"
        if any(d.get("authority_capable") is not True for d in dependencies):
            return "unknown", None, "semantic_operand_authority_unknown"
    return "allow", resolved, "resolved"


def matches(permission, action):
    return all(permission[field] == action[field] for field in FIELDS)


def permissions_match(grant, action):
    if not any(matches(p, action) for p in grant.get("permissions", [])):
        return False
    restrictions = grant.get("restrictions")
    return restrictions is None or any(matches(p, action) for p in restrictions)


def bridge_valid(bridge, action, artifact_id, label, case, policy):
    state, _ = root_state(bridge, case.get("now", 5), policy)
    return (
        state == "allow"
        and bridge["artifact_id"] == artifact_id
        and label in bridge["labels"]
        and matches(bridge["permission"], action)
    )


def guard(grant, action, case, state, policy):
    if policy == "local_tuple_only":
        return "allow", "prefix_conditions_ignored"
    limit = grant.get("use_limit")
    if limit is not None and state["uses"].get(grant["id"], 0) >= limit:
        return "deny", "grant_use_limit_exhausted"
    for condition in grant.get("conditions", []):
        if condition["kind"] == "budget":
            pool = condition["pool"]
            available = case["budget_pools"][pool] - state["spent"].get(pool, 0)
            if action.get("cost", 0) > available:
                return "deny", "shared_budget_would_be_exceeded"
        elif condition["kind"] == "input_labels":
            allowed = set(condition["allowed"])
            for artifact_id in action.get("inputs", []):
                if artifact_id not in state["artifacts"]:
                    return "unknown", "input_lineage_missing"
                for label in state["artifacts"][artifact_id]["labels"]:
                    if label in allowed:
                        continue
                    if not any(bridge_valid(b, action, artifact_id, label, case, policy) for b in case.get("bridges", [])):
                        return "deny", "flow_condition_not_satisfied"
        else:
            raise ValueError(f"Unknown condition: {condition['kind']}")
    return "allow", "all_prefix_conditions_hold"


def apply(action, witnesses, state):
    for grant in witnesses:
        state["uses"][grant["id"]] = state["uses"].get(grant["id"], 0) + 1
    pools = {c["pool"] for g in witnesses for c in g.get("conditions", []) if c["kind"] == "budget"}
    for pool in pools:
        state["spent"][pool] = state["spent"].get(pool, 0) + action.get("cost", 0)
    output = action.get("output")
    if output is not None:
        if any(i not in state["artifacts"] for i in action.get("inputs", [])):
            raise ValueError("Cannot propagate absent input lineage")
        labels = sorted({label for i in action.get("inputs", []) for label in state["artifacts"][i]["labels"]})
        state["artifacts"][output] = {"labels": labels, "parents": list(action.get("inputs", []))}


def evaluate(case, policy):
    state = {"spent": dict(case.get("spent", {})), "uses": dict(case.get("uses", {})), "artifacts": copy.deepcopy(case.get("artifacts", {}))}
    resolutions = [resolve(g, case, policy) for g in case.get("grants", [])]
    active = [g for status, g, _ in resolutions if status == "allow"]
    trace = []
    for index, action in enumerate(case["actions"], 1):
        candidates = [[g] for g in active if permissions_match(g, action)]
        if not candidates and policy == "marginal_join":
            # All full tuples remain authentic. Only the association among
            # dimensions is removed. Every supporting grant's conditions are
            # still checked; this ablation does not also erase conditions.
            contributors = []
            for field in FIELDS:
                supports = [g for g in active if any(p[field] == action[field] and permissions_match(g, p) for p in g.get("permissions", []))]
                if not supports:
                    contributors = []
                    break
                for g in supports:
                    if g not in contributors:
                        contributors.append(g)
            if contributors:
                candidates = [contributors]
        observations = []
        for witnesses in candidates:
            guarded = [guard(g, action, case, state, policy) for g in witnesses]
            decision = "deny" if any(s == "deny" for s, _ in guarded) else "unknown" if any(s == "unknown" for s, _ in guarded) else "allow"
            reasons = [reason for s, reason in guarded if s != "allow"]
            observations.append((decision, witnesses, reasons))
        accepted = next((o for o in observations if o[0] == "allow"), None)
        if accepted:
            witnesses = accepted[1]
            trace.append({"step": index, "decision": "allow", "witnesses": [g["id"] for g in witnesses], "resolved_proposals": [g["resolved_proposal"] for g in witnesses if "resolved_proposal" in g], "reasons": []})
            apply(action, witnesses, state)
            continue
        if any(o[0] == "unknown" for o in observations):
            decision = "unknown"
        elif observations:
            decision = "deny"
        elif any(status == "unknown" for status, _, _ in resolutions):
            # Fixtures limit unresolved roots to potentially relevant claims.
            # General relevance/closed-world reasoning is deliberately absent.
            decision = "unknown"
        else:
            decision = "deny"
        reasons = [reason for _, _, rs in observations for reason in rs]
        if not candidates:
            reasons = [why for status, _, why in resolutions if status != "allow"] or ["no_joint_scope_witness"]
        trace.append({"step": index, "decision": decision, "witnesses": [], "resolved_proposals": [], "reasons": sorted(set(reasons))})
        return {"decision": decision, "trace": trace}
    return {"decision": "allow", "trace": trace}


def scope_probe():
    rows = [
        {"verb": "read", "object": "private-notes", "purpose": "planning", "surface": "private-workspace"},
        {"verb": "publish", "object": "public-report", "purpose": "release", "surface": "public-site"},
    ]
    grants = [{"id": f"g{i}", "root": {"id": f"r{i}", "authority_capable": True, "current_turn": True}, "permissions": [row]} for i, row in enumerate(rows)]
    tuples = [dict(zip(FIELDS, values)) for values in itertools.product(*(sorted({row[f] for row in rows}) for f in FIELDS))]
    results = []
    for action in tuples:
        case = {"grants": grants, "actions": [action]}
        expected = "allow" if action in rows else "deny"
        results.append({"action": action, "expected": expected, "witness_and_trace": evaluate(case, "witness_and_trace")["decision"], "marginal_join": evaluate(case, "marginal_join")["decision"]})
    return {"description": "Complete 2x2x2x2 product of the marginals of two authentic full-scope grants.", "count": len(results), "jointly_authorized": sum(r["expected"] == "allow" for r in results), "spurious_marginal_permissions": sum(r["expected"] == "deny" and r["marginal_join"] == "allow" for r in results), "rows": results}


def budget_probe():
    rows = []
    for first, second in itertools.product(range(1, 11), repeat=2):
        actions = [{"verb": "buy", "object": item, "purpose": "project", "surface": "vendor", "cost": cost} for item, cost in (("material-a", first), ("material-b", second))]
        grants = [{"id": f"g{i}", "root": {"id": f"r{i}", "authority_capable": True, "current_turn": True}, "permissions": [{f: action[f] for f in FIELDS}], "conditions": [{"kind": "budget", "pool": "shared"}]} for i, action in enumerate(actions)]
        case = {"grants": grants, "actions": actions, "budget_pools": {"shared": 10}}
        # Each complete grant permits its own action from the fresh state.
        standalone = [evaluate({**case, "actions": [action]}, "witness_and_trace")["decision"] for action in actions]
        expected = "allow" if first + second <= 10 else "deny"
        rows.append({"costs": [first, second], "standalone": standalone, "expected_trace": expected, "witness_and_trace": evaluate(case, "witness_and_trace")["decision"], "local_tuple_only": evaluate(case, "local_tuple_only")["decision"]})
    return {"description": "All ordered cost pairs in {1,...,10}^2 under one authenticated shared cap of 10; both exact grants permit their step in a fresh state.", "count": len(rows), "valid_compositions": sum(r["expected_trace"] == "allow" for r in rows), "invalid_compositions": sum(r["expected_trace"] == "deny" for r in rows), "rows": rows}


def build_results(fixtures):
    cases = []
    for case in fixtures["cases"]:
        outcomes = {p: evaluate(case, p) for p in POLICIES}
        cases.append({"id": case["id"], "family": case["family"], "expected": case["expected"], "rationale": case["rationale"], "outcomes": outcomes})
    totals = {}
    for policy in POLICIES:
        disagreements = [c for c in cases if c["outcomes"][policy]["decision"] != c["expected"]]
        totals[policy] = {
            "case_count": len(cases),
            "agreement_with_stipulated_oracle": len(cases) - len(disagreements),
            "false_permits": sum(c["expected"] == "deny" and c["outcomes"][policy]["decision"] == "allow" for c in cases),
            "blocked_valid_traces": sum(c["expected"] == "allow" and c["outcomes"][policy]["decision"] != "allow" for c in cases),
            "unsupported_permits": sum(c["expected"] == "unknown" and c["outcomes"][policy]["decision"] == "allow" for c in cases),
            "disagreement_case_ids": [c["id"] for c in disagreements],
        }
    scope, budget = scope_probe(), budget_probe()
    checks = {
        "unique_case_ids": len({c["id"] for c in cases}) == len(cases),
        "reference_agrees_with_all_hand_authored_cases": all(c["outcomes"]["witness_and_trace"]["decision"] == c["expected"] for c in cases),
        "all_reference_scope_decisions_match_relation": all(r["witness_and_trace"] == r["expected"] for r in scope["rows"]),
        "scope_14_spurious_combinations": scope["spurious_marginal_permissions"] == 14,
        "all_budget_steps_individually_permitted": all(r["standalone"] == ["allow", "allow"] for r in budget["rows"]),
        "all_reference_budget_decisions_match_sum_condition": all(r["witness_and_trace"] == r["expected_trace"] for r in budget["rows"]),
        "budget_45_valid_55_invalid": budget["valid_compositions"] == 45 and budget["invalid_compositions"] == 55,
        "local_budget_policy_permits_all_100": all(r["local_tuple_only"] == "allow" for r in budget["rows"]),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {"artifact_kind": "executed_synthetic_finite_diagnostic", "date_local": "2026-11-05", "timezone": "Asia/Singapore", "base_commit": BASE_HEAD, "limits": ["No model or provider was called.", "Stipulated authorization, status, time, references and lineage are inputs; there is no natural-language history extractor or event reducer.", "Grant status is resolved once at the fixture clock; no mid-trace revocation is modeled.", "The evaluator consumes the first allowed witness; it is not a complete planner for overlapping grants or alternative resource assignments.", "Policy variants are authored ablations, not implementations attributed to existing products.", "Cases and exhaustive probes are correlated constructions, not independent empirical validation."], "expected_decision_counts": dict(Counter(c["expected"] for c in cases)), "policy_summary": totals, "checks": checks, "cases": cases, "scope_probe": scope, "budget_probe": budget}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write results.json and a new receipt.json")
    args = parser.parse_args()
    fixtures_path = HERE / "fixtures.json"
    result = build_results(json.loads(fixtures_path.read_text()))
    result_text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        (HERE / "results.json").write_text(result_text)
        receipt = {
            "artifact_kind": "synthetic_diagnostic_execution_receipt",
            "executed_at_utc": datetime.now(timezone.utc).isoformat(),
            "local_research_date": "2026-11-05",
            "python": platform.python_version(),
            "base_commit": BASE_HEAD,
            "command": "python3 -B research/authorization-continuity/diagnose.py --write",
            "model_calls": 0,
            "network_calls": 0,
            "external_actions": 0,
            "files": {name: {"sha256": hashlib.sha256((HERE / name).read_bytes()).hexdigest(), "bytes": (HERE / name).stat().st_size} for name in ("diagnose.py", "fixtures.json", "results.json")},
            "all_invariants_passed": True,
        }
        (HERE / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    else:
        recorded = HERE / "results.json"
        if not recorded.exists():
            raise SystemExit("saved results.json is missing; use --write to materialize the diagnostic first")
        if recorded.read_text() != result_text:
            raise SystemExit("Recorded results differ. Review the change before regenerating with --write.")
        receipt_path = HERE / "receipt.json"
        if not receipt_path.exists():
            raise SystemExit("saved receipt.json is missing; artifact integrity cannot be verified")
        receipt = json.loads(receipt_path.read_text())
        for name in ("diagnose.py", "fixtures.json", "results.json"):
            data = (HERE / name).read_bytes()
            expected = receipt.get("files", {}).get(name)
            actual = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
            if expected != actual:
                raise SystemExit(f"Receipt integrity mismatch for {name}; review before regenerating with --write.")
        if receipt.get("base_commit") != BASE_HEAD or receipt.get("all_invariants_passed") is not True:
            raise SystemExit("Receipt metadata does not match this completed diagnostic.")
    print(json.dumps({"case_count": len(result["cases"]), "expected": result["expected_decision_counts"], "policies": result["policy_summary"], "scope": {k: v for k, v in result["scope_probe"].items() if k != "rows"}, "budget": {k: v for k, v in result["budget_probe"].items() if k != "rows"}, "checks": result["checks"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
