#!/usr/bin/env python3
"""Input-only finite witness study for the bundled future-question examples.

No subject/model is run. Source projection cannot read the separate answer
contract. Archive states alter an actual in-memory source store and permission
set; a successful lookup appends source text, never labels or a success score.
Equality is checked on canonical view bytes. Hashes label groups for inspection
only; they are neither a retrieval method nor part of any emitted source view.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import secrets
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "research" / "future-question-memory"
HISTORIES = STUDY / "histories.zh-CN.json"
CONTRACTS = STUDY / "contracts.zh-CN.json"
RESULT = STUDY / "results.json"
PROJECTIONS = ("retained", "full", "roles-removed")
ACCESS = ("closed", "allowed", "missing", "denied", "stale")
CONDITIONS = (
    ("retained", "closed"), ("full", "closed"),
    ("roles-removed", "closed"), ("retained", "allowed"),
    ("retained", "missing"), ("retained", "denied"),
    ("retained", "stale"),
)
FAMILY_IDS = (
    "A-AUTHORSHIP", "B-CONDITIONAL-USE", "C-DISCARDED-RATIONALE",
    "D-INTENTION-STATUS", "E-MIGRATION-CAPABILITY",
    "F-UNRESOLVED-ACCOUNTS", "G-GLOBAL-INTERSECTION",
)
LIMIT = 1_000_000


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       indent=2, allow_nan=False) + "\n").encode("utf-8")


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def unique_fields(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON field")
        result[key] = value
    return result


def read_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink() and path.stat().st_size < LIMIT,
            "invalid bundled input")
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_fields)
    require(isinstance(value, dict), "expected a JSON object")
    return value


def check_fields(value: Any, expected: set[str], label: str) -> None:
    require(isinstance(value, dict) and set(value) == expected, f"invalid {label} fields")


def check_events(events: Any, scope: str) -> None:
    require(isinstance(events, list) and bool(events), "empty event list")
    for event in events:
        check_fields(event, {"speaker", "scope", "text"}, "event")
        require(event["speaker"] in {"user", "assistant", "tool"}, "invalid speaker")
        require(event["scope"] == scope, "this bounded study does not mix archive scopes")
        require(isinstance(event["text"], str) and bool(event["text"].strip()), "empty event")


def validate_histories(source: dict[str, Any]) -> None:
    """Validate source material without accepting or importing answer labels."""
    check_fields(source, {"format", "provenance", "context", "families"}, "history bundle")
    require(source["format"] == "relata-future-question-histories-1", "wrong history format")
    require(isinstance(source["context"], str) and bool(source["context"]), "missing context")
    require(isinstance(source["families"], list), "invalid families")
    require(tuple(f["id"] for f in source["families"]) == FAMILY_IDS,
            "only the seven bundled authored families are supported")
    for family in source["families"]:
        check_fields(family, {"id", "title", "relationship_to_existing", "scope",
                             "archive_pointer", "retained_positions", "questions",
                             "stale_archive", "worlds"}, "family")
        require(isinstance(family["archive_pointer"], str) and
                family["archive_pointer"].startswith("archive/"), "invalid archive pointer")
        positions = family["retained_positions"]
        require(isinstance(positions, list) and bool(positions) and
                all(type(i) is int and i >= 0 for i in positions) and
                positions == sorted(set(positions)), "invalid retention positions")
        require(isinstance(family["questions"], list) and bool(family["questions"]), "no questions")
        qids: set[str] = set()
        for question in family["questions"]:
            check_fields(question, {"id", "text"}, "question")
            require(question["id"] not in qids and isinstance(question["text"], str)
                    and bool(question["text"]), "invalid question")
            qids.add(question["id"])
        check_events(family["stale_archive"], family["scope"])
        require(isinstance(family["worlds"], list) and len(family["worlds"]) >= 2, "missing worlds")
        world_ids: set[str] = set()
        for world in family["worlds"]:
            check_fields(world, {"id", "events"}, "world")
            require(world["id"] not in world_ids, "duplicate world identity")
            world_ids.add(world["id"])
            check_events(world["events"], family["scope"])
            require(max(positions) < len(world["events"]), "retention position out of range")


def validate_contracts(source: dict[str, Any], contracts: dict[str, Any]) -> None:
    check_fields(contracts, {"format", "status", "interpretation", "decisions", "families"},
                 "contract bundle")
    require(contracts["format"] == "relata-future-question-contracts-1", "wrong contract format")
    require(set(contracts["families"]) == set(FAMILY_IDS), "contract family mismatch")
    decisions = contracts["decisions"]
    require(isinstance(decisions, dict) and bool(decisions), "no decisions")
    for family in source["families"]:
        contract = contracts["families"][family["id"]]
        require(set(contract) == {q["id"] for q in family["questions"]}, "question contract mismatch")
        worlds = {w["id"] for w in family["worlds"]}
        for answers in contract.values():
            require(set(answers) == worlds, "world contract mismatch")
            for choices in answers.values():
                require(isinstance(choices, list) and bool(choices) and
                        len(choices) == len(set(choices)) and set(choices) <= set(decisions),
                        "invalid finite answer region")


def project_events(events: list[dict[str, str]], positions: list[int],
                   projection: str) -> list[dict[str, str]]:
    """The write-time projection has no question, answer contract or world ID."""
    require(projection in PROJECTIONS, "unknown projection")
    chosen = [events[i] for i in positions] if projection == "retained" else events
    keys = ("scope", "text") if projection == "roles-removed" else ("speaker", "scope", "text")
    return [{key: event[key] for key in keys} for event in chosen]


def resolve_archive(pointer: str, store: dict[str, list[dict[str, str]]],
                    readable: set[str], known_stale: set[str]) -> dict[str, Any]:
    """Resolve actual source contents; authorization is checked before existence."""
    if pointer not in readable:
        return {"status": "denied"}
    if pointer not in store:
        return {"status": "missing"}
    return {"status": "known-stale" if pointer in known_stale else "available-current",
            "events": deepcopy(store[pointer])}


def make_view(context: str, family: dict[str, Any], world: dict[str, Any],
              question: dict[str, str], projection: str, access: str) -> dict[str, Any]:
    """Assemble an input view. Nothing here imports or accepts evaluator choices."""
    require(access in ACCESS, "unknown archive access condition")
    pointer = family["archive_pointer"]
    view = {
        "context": context,
        "current": {"scope": family["scope"], "text": question["text"]},
        "memory": project_events(world["events"], family["retained_positions"], projection),
        "archive_pointer": pointer,
        "archive": {"status": "not-requested"},
    }
    if access != "closed":
        # A missing object, inaccessible object and older object are distinct
        # source environments, never precomputed answer/success branches.
        content = family["stale_archive"] if access == "stale" else world["events"]
        store = {} if access == "missing" else {pointer: content}
        readable = set() if access == "denied" else {pointer}
        known_stale = {pointer} if access == "stale" else set()
        view["archive"] = resolve_archive(pointer, store, readable, known_stale)
    return view

INPUT_VIEW_FIELDS = ("context", "current", "memory", "archive_pointer", "archive")

def exported_input_view(view: dict[str, Any]) -> dict[str, Any]:
    """Return only the provider-consumable field allowlist.

    The authored world, family, question, condition and answer contract are
    evaluator material and must not be reachable from this object.
    """
    require(set(view) == set(INPUT_VIEW_FIELDS), "unexpected input view fields")
    return deepcopy({field: view[field] for field in INPUT_VIEW_FIELDS})

def fresh_directory(path: Path) -> Path:
    original = path.expanduser().absolute()
    require(not any(p.is_symlink() for p in (original, *original.parents)),
            "output path may not contain symlinks")
    path = original.resolve()
    require(path.parent.is_dir(), "output parent must already exist")
    path.mkdir(mode=0o700, exist_ok=False)
    return path

def write_new(path: Path, data: bytes) -> None:
    with path.open("xb") as stream:
        stream.write(data)

def write_input_packet(source: dict[str, Any], output: Path) -> dict[str, Any]:
    """Write all fixed-bundle projection cells as opaque input-only files.

    The hidden manifest is a separate file used by offline preparation/review
    tooling. The input files themselves contain no authored identity, labels,
    answers, reviewer material or hashes.
    """
    validate_histories(source)
    folder = fresh_directory(output)
    for name in ("inputs", "hidden"):
        (folder / name).mkdir()
    records = []
    for family in source["families"]:
        for question in family["questions"]:
            for world in family["worlds"]:
                for projection, access in CONDITIONS:
                    input_id = "I-" + secrets.token_hex(16)
                    view = exported_input_view(make_view(
                        source["context"], family, world, question, projection, access))
                    blob = canonical(view)
                    write_new(folder / "inputs" / f"{input_id}.json", blob)
                    records.append({
                        "input_id": input_id, "family": family["id"],
                        "question": question["id"], "world_id": world["id"],
                        "projection": projection, "archive_access": access,
                        "input_sha256": digest(blob),
                    })
    manifest = {
        "format": "relata-future-question-input-packet-1",
        "status": "input-only; no subject execution or answer contract",
        "history_sha256": digest(canonical(source)),
        "records": records,
    }
    write_new(folder / "hidden" / "manifest.json", canonical(manifest))
    return {"format": manifest["format"], "counts": {"inputs": len(records)},
            "history_sha256": manifest["history_sha256"]}


def group_views(views: dict[str, dict[str, Any]],
                answer_regions: dict[str, list[str]],
                priors: dict[str, Fraction] | None = None) -> list[dict[str, Any]]:
    """Intersect ALL answer regions in each identical-view class.

    Nonempty intersections only establish a possible finite lookup assignment;
    they do not show a natural-language reader can infer it. Pairwise overlap is
    reported as a warning diagnostic and never substituted for global overlap.
    A world prior applies only within each identical-view class. The default is
    uniform there; all report values remain exact rationals.
    """
    if priors is None:
        priors = {world: Fraction(1, len(views)) for world in views}
    check_world_prior(views, priors)
    groups: dict[bytes, list[str]] = {}
    for world, view in views.items():
        groups.setdefault(canonical(view), []).append(world)
    result = []
    for material, worlds in groups.items():
        sets = [set(answer_regions[w]) for w in worlds]
        common = set.intersection(*sets)
        pairwise = all(bool(a & b) for a, b in combinations(sets, 2))
        mass = sum((priors[world] for world in worlds), Fraction(0))
        require(mass > 0, "each identical-view class needs positive prior mass")
        world_rows = [{"world_id": world,
                       "probability": rational_text(priors[world] / mass),
                       "answer_region": sorted(answer_regions[world])}
                      for world in worlds]
        scores = {choice: sum((priors[world] / mass for world in worlds
                               if choice in answer_regions[world]), Fraction(0))
                  for choice in set.union(*sets)}
        best = max(scores.values())
        choices = sorted(choice for choice, score in scores.items() if score == best)
        result.append({
            "worlds": worlds,
            "view_sha256": digest(material),
            "view_bytes": len(material),
            "common_choices": sorted(common),
            "pairwise_intersections_nonempty": pairwise,
            "incompatible_answer_contract": not bool(common),
            "witness_kind": "global-only" if not common and pairwise else
                            "pairwise-contrast" if not common else "none",
            "world_prior_mass": rational_text(mass),
            "worlds_with_probability": world_rows,
            "best_choices": choices,
            "max_correct_probability": rational_text(best),
            "mass_weighted_accuracy": rational_text(mass * best),
        })
    return result

def rational_text(value: Fraction) -> str:
    return (str(value.numerator) if value.denominator == 1
            else f"{value.numerator}/{value.denominator}")

def check_world_prior(views: dict[str, Any], priors: dict[str, Fraction]) -> None:
    """Validate an explicit world prior without normalizing away missing worlds."""
    require(set(priors) == set(views), "world prior must name exactly the observed worlds")
    require(all(isinstance(value, Fraction) and value >= 0 for value in priors.values()),
            "world prior values must be non-negative Fractions")
    require(sum(priors.values(), Fraction(0)) == 1, "world prior must sum to 1")

def uniform_prior(worlds: list[dict[str, Any]]) -> dict[str, Fraction]:
    return {world["id"]: Fraction(1, len(worlds)) for world in worlds}


def audit(source: dict[str, Any], contracts: dict[str, Any]) -> dict[str, Any]:
    validate_histories(source)
    validate_contracts(source, contracts)
    cells = []
    for family in source["families"]:
        for question in family["questions"]:
            for projection, access in CONDITIONS:
                views = {world["id"]: make_view(source["context"], family, world,
                                                question, projection, access)
                         for world in family["worlds"]}
                groups = group_views(views, contracts["families"][family["id"]][question["id"]],
                                     uniform_prior(family["worlds"]))
                cells.append({"family": family["id"], "question": question["id"],
                              "projection": projection, "archive_access": access,
                              "lookup_accuracy": rational_text(
                                  sum((Fraction(group["mass_weighted_accuracy"])
                                       for group in groups), Fraction(0))),
                              "groups": groups})
    return {
        "format": "relata-future-question-projection-report-1",
        "evidence_status": "computed authored input-projection witnesses; no subject execution",
        "history_sha256": digest(canonical(source)),
        "contract_sha256": digest(canonical(contracts)),
        "counts": {"families": len(source["families"]),
                   "worlds": sum(len(f["worlds"]) for f in source["families"]),
                   "questions": sum(len(f["questions"]) for f in source["families"]),
                   "cells": len(cells)},
        "interpretation": "Incompatible means no shared task-fulfilling finite choice under an identical view. max_correct_probability is the ideal finite lookup bound under a uniform world prior within each identical-view class, not a model score or general theorem. lookup_accuracy is the world-mass-weighted sum of group bounds, not an unweighted average of groups. Honest requests for more evidence remain legitimate. No collision found is not a semantic-success result. Cells and variants are correlated, not independent trials.",
        "cells": cells,
    }


def summarize(report: dict[str, Any]) -> str:
    counts = report["counts"]
    lines = [f"{counts['families']} authored families / {counts['worlds']} worlds / "
             f"{counts['questions']} questions / {counts['cells']} projection cells",
             "No subject, provider, score or semantic validation is produced."]
    for projection, access in CONDITIONS:
        cells = [c for c in report["cells"] if (c["projection"], c["archive_access"]) == (projection, access)]
        incompatible = [c for c in cells if any(g["incompatible_answer_contract"] for g in c["groups"])]
        global_only = [c for c in cells if any(g["witness_kind"] == "global-only" for g in c["groups"])]
        lines.append(f"{projection}/{access}: {len(incompatible)} incompatible cells; "
                     f"{len(global_only)} require global intersection")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check", help="validate bundled sources and exact regenerated report")
    sub.add_parser("write", help="regenerate only research/future-question-memory/results.json")
    audit_parser = sub.add_parser("audit", help="compute the finite projection diagnostic")
    audit_parser.add_argument("--json", action="store_true", help="emit the full report as JSON")
    export = sub.add_parser("export-inputs", help="write all fixed-bundle input-only cells")
    export.add_argument("--output", type=Path, required=True, help="new directory")
    show = sub.add_parser("show", help="inspect source-only input views; no answer contract is loaded")
    show.add_argument("--family", choices=FAMILY_IDS, required=True)
    show.add_argument("--question", default="later")
    show.add_argument("--projection", choices=PROJECTIONS, default="retained")
    show.add_argument("--access", choices=ACCESS, default="closed")
    args = parser.parse_args(argv)
    try:
        source = read_json(HISTORIES)
        validate_histories(source)
        if args.command == "show":
            family = next(f for f in source["families"] if f["id"] == args.family)
            questions = {q["id"]: q for q in family["questions"]}
            require(args.question in questions, "unknown question for this family")
            packets = [{"authoring_world": w["id"],
                        "input_view": make_view(source["context"], family, w,
                                                questions[args.question], args.projection, args.access)}
                       for w in family["worlds"]]
            sys.stdout.buffer.write(canonical(packets))
            return 0
        if args.command == "export-inputs":
            summary = write_input_packet(source, args.output)
            print(canonical({"status": "input-packet-written",
                             "output": str(args.output), **summary}).decode(), end="")
            return 0
        report = audit(source, read_json(CONTRACTS))
        if args.command == "write":
            require(not RESULT.is_symlink(), "refusing generated-report symlink")
            RESULT.write_bytes(canonical(report))
            print("Regenerated research/future-question-memory/results.json")
        elif args.command == "check":
            require(RESULT.is_file() and not RESULT.is_symlink(), "generated report missing")
            require(RESULT.read_bytes() == canonical(report), "generated report differs; inspect then run write")
            print("Bundled source/contract structure and regenerated report match.")
        elif args.json:
            sys.stdout.buffer.write(canonical(report))
            return 0
        print(summarize(report))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
