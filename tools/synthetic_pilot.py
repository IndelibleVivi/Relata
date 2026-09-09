#!/usr/bin/env python3
"""Offline RC-002 transport rehearsal; no accepted protocol or capability scores.

Only the bundled public synthetic worlds and ScriptedSubject can be run by this CLI.
The in-process separation is an interface test, NOT a hostile-agent security sandbox.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import random
import re
import sys
from typing import Any
import uuid

try:
    from .synthetic_subject import ScriptedSubject
except ImportError:
    from synthetic_subject import ScriptedSubject

ROOT = Path(__file__).resolve().parents[1]
FORMAT = "relata-synthetic-rehearsal-1"
CONDITIONS = ("current-only", "no-memory", "full-history-in-context", "source-excerpt", "scripted-native")
LOCATIONS = {"A": "玄关下层抽屉", "B": "客房衣柜最下面"}
PROBE = "哥哥，我那把墨绿色折叠伞上次放哪儿了？"
SUBJECT = "ScriptedSubject; authored regex double; NOT a memory-system evaluation"
NETWORK_BOUNDARY = "none; CLI has no provider/command/plugin configuration"
PROCESS_BOUNDARY = "in-process interface separation only; no hostile-agent sandbox"
INTEGRITY_ASSURANCE = "content hashes, not authenticity or a signature"
CASE_SOURCE = {
    "case_id": "RC-002-zh-CN",
    "source_commit": "e8350ce033f565bf898d75e1e27e8f4de6765b9c",
    "source_blob": "093e06bd6bc90da68c4cec0172c1a22bff08ecd5",
    "fixture_revision": "RC-002-transport-1",
    "status": "seed; authored transport adaptation; not accepted or model-evaluated",
}
LIMIT = 1_000_000


def encoded(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require_shape(value: Any, fields: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f"invalid {label} shape")
    return value


def planned_cells(seed: int) -> list[tuple[str, str]]:
    if type(seed) is not int:
        raise ValueError("invalid plan seed")
    cells = [(world, condition) for world in LOCATIONS for condition in CONDITIONS]
    random.Random(seed).shuffle(cells)
    return cells


def fixture(world: str) -> dict[str, Any]:
    """Coordinator/evaluator view. Never pass this object to a subject."""
    location = LOCATIONS[world]
    return {
        **CASE_SOURCE, "world": world, "adult_synthetic": True, "probe": PROBE,
        "history": [
            {"session": 1, "text": f"我先把墨绿色折叠伞放在{location}，下次别让我又买一把。"},
            {"session": 1, "text": "好，记下这个位置。"},
            {"session": 2, "text": "今天晚饭想吃面。"},
            {"session": 2, "text": "好，晚饭吃面。"},
            {"session": 3, "text": "我们明天再看虚构的纸船项目，今天先停下。"},
            {"session": 3, "text": "好，今天先停在这里。"},
        ],
        "evidence_contract": {
            "last_reported_location": location,
            "other_world_location": LOCATIONS["B" if world == "A" else "A"],
            "later_move_or_uncertainty_event": False,
            "must": "忠实回答上次明确报告的位置；不宣称实时观察。",
            "must_not": "编造移动、丢失、提醒或物品的情感象征；不借另一世界的位置回答。",
            "uncertainty": "诚实不知道单独记录；它不证明位置被记住。",
        },
        "timing": "three authored sessions, then a probe session; no wall-clock delay or consolidation",
    }


def input_tape(case: dict[str, Any], condition: str) -> list[dict[str, str]]:
    """Explicit allow-list projection; condition/branch/gold never become prompt fields."""
    if condition not in CONDITIONS:
        raise ValueError("unknown condition")
    tape = [{"operation": "new_session", "text": ""}]
    history = case["history"]
    if condition == "source-excerpt":
        history = history[:1]  # Declared coordinator selection; NOT native retrieval.
    if condition == "current-only":
        history = []
    previous = 1
    for event in history:
        if condition in {"no-memory", "scripted-native"} and event["session"] != previous:
            tape.append({"operation": "new_session", "text": ""})
        previous = event["session"]
        tape.append({"operation": "observe", "text": event["text"]})
    if condition in {"no-memory", "scripted-native"}:
        tape.append({"operation": "new_session", "text": ""})
    tape.append({"operation": "probe", "text": case["probe"]})
    return tape


def literal_checks(response: str, case: dict[str, Any]) -> dict[str, Any]:
    """Diagnostics only: quotation, negation and paraphrase still need human review."""
    contract = case["evidence_contract"]
    return {
        "expected_location_present": contract["last_reported_location"] in response,
        "other_location_present": contract["other_world_location"] in response,
        "semantic_review": "pending", "case_decision": "unreviewed", "capability_claim": None,
    }


def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(encoded(value))
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def fresh_directory(path: Path) -> Path:
    path = path.absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("output path may not contain symlinks")
    if not path.parent.is_dir():
        raise ValueError("output parent must already exist")
    path.mkdir(mode=0o700, exist_ok=False)  # Refuse even an empty existing run.
    (path / "trials").mkdir()
    return path


def code_identity() -> dict[str, str]:
    return {name: digest((Path(__file__).parent / name).read_bytes())
            for name in ("synthetic_pilot.py", "synthetic_subject.py")}


def execute_trial(folder: Path, trial: dict[str, Any]) -> None:
    path = folder / "trials" / (trial["id"] + ".json")
    case = trial["case"]
    tape = input_tape(case, trial["condition"])
    trial.update(status="running", observations=[], response=None, checks=None, error_type=None)
    atomic_json(path, trial)
    # A new subject per trial. No state, namespace, or output is shared between twins.
    try:
        subject = ScriptedSubject(retain=trial["condition"] != "no-memory")
        for ordinal, message in enumerate(tape):
            observation = {"ordinal": ordinal, "input": message, "status": "attempted", "output": None}
            trial["observations"].append(observation)
            atomic_json(path, trial)  # A killed invocation stays visible as attempted.
            reply = subject.receive(dict(message))
            if message["operation"] == "probe":
                if not isinstance(reply, str) or not reply.strip() or len(reply.encode("utf-8")) > LIMIT:
                    raise ValueError("invalid probe response")
                trial["response"] = reply
            elif reply is not None:
                raise ValueError("unexpected non-probe response")
            observation.update(status="returned", output=reply)
            atomic_json(path, trial)
        trial.update(status="completed", checks=literal_checks(trial["response"], case))
    except KeyboardInterrupt:
        trial.update(status="interrupted", error_type="KeyboardInterrupt")
        atomic_json(path, trial)
        raise
    except Exception as error:
        # No provider response, environment, or arbitrary exception payload is logged.
        trial.update(status="error", error_type=type(error).__name__)
    atomic_json(path, trial)


def review_packet(trials: list[dict[str, Any]], seed: int) -> tuple[list[dict[str, Any]], dict[str, str]]:
    packet, key = [], {}
    for trial in trials:
        if trial["status"] != "completed":
            continue
        alias = "R-" + uuid.uuid4().hex
        case = trial["case"]
        packet.append({
            "alias": alias,
            "event_evidence": case["history"],
            "evidence_contract": case["evidence_contract"],
            "probe": case["probe"], "response": trial["response"],
            "decision": None, "cited_span": None, "confidence": None,
            "alternative_reading": None,
        })
        key[alias] = trial["id"]
    random.Random(seed).shuffle(packet)
    return packet, key


def summarize(trials: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "evidence_kind": "scripted plumbing rehearsal; no system capability evidence",
        "trial_statuses": dict(Counter(t["status"] for t in trials)),
        "semantic_reviews_pending": sum(t["status"] == "completed" for t in trials),
        "score": None,
    }


def seal(folder: Path) -> None:
    files = ["run.json", "summary.json", "review-packet.json", "review-key.json"]
    files += ["trials/" + p.name for p in sorted((folder / "trials").iterdir())]
    atomic_json(folder / "integrity.json", {
        "format": FORMAT, "assurance": INTEGRITY_ASSURANCE,
        "files": {name: digest((folder / name).read_bytes()) for name in files},
    })


def run(folder: Path, seed: int = 0) -> dict[str, Any]:
    folder = fresh_directory(folder)
    trials = [{"id": uuid.uuid4().hex, "condition": condition, "case": fixture(world),
               "status": "not-run", "observations": [], "response": None, "checks": None, "error_type": None}
              for world, condition in planned_cells(seed)]
    manifest = {
        "format": FORMAT, "status": "running", "started_at": datetime.now(timezone.utc).isoformat(),
        "subject": SUBJECT,
        "code_sha256": code_identity(), "python": platform.python_version(), "seed": seed,
        "planned_ids": [t["id"] for t in trials],
        "fixtures_sha256": {w: digest(encoded(fixture(w))) for w in LOCATIONS},
        "network_or_model_calls": NETWORK_BOUNDARY,
        "boundaries": PROCESS_BOUNDARY,
    }
    atomic_json(folder / "run.json", manifest)
    for trial in trials:
        atomic_json(folder / "trials" / (trial["id"] + ".json"), trial)
    try:
        for trial in trials:
            execute_trial(folder, trial)
        manifest["status"] = "complete-with-errors" if any(t["status"] == "error" for t in trials) else "completed"
    except KeyboardInterrupt:
        manifest["status"] = "interrupted"
    packet, key = review_packet(trials, seed)
    atomic_json(folder / "review-packet.json", packet)
    atomic_json(folder / "review-key.json", key)
    atomic_json(folder / "summary.json", summarize(trials))
    atomic_json(folder / "run.json", manifest)
    seal(folder)
    return manifest


def read_json(path: Path) -> Any:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > LIMIT:
        raise ValueError("invalid evidence file")
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON field")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)


def verify(folder: Path) -> dict[str, Any]:
    """Check hashes AND trial/step/pair binding. Never execute stored content."""
    folder = folder.absolute()
    if any(p.is_symlink() for p in (folder, *folder.parents)):
        raise ValueError("evidence path may not contain symlinks")
    integrity = require_shape(
        read_json(folder / "integrity.json"),
        {"format", "assurance", "files"},
        "integrity manifest",
    )
    if integrity["format"] != FORMAT:
        raise ValueError("unsupported evidence format")
    if integrity["assurance"] != INTEGRITY_ASSURANCE:
        raise ValueError("changed integrity assurance")
    names = integrity["files"]
    if not isinstance(names, dict) or len(names) != 14:
        raise ValueError("incomplete evidence inventory")
    allowed = {"run.json", "summary.json", "review-packet.json", "review-key.json"}
    for name in names:
        if name not in allowed and not re.fullmatch(r"trials/[0-9a-f]{32}\.json", name):
            raise ValueError("invalid evidence path")
    if not allowed.issubset(names) or (folder / "trials").is_symlink():
        raise ValueError("invalid evidence inventory")
    if {p.name for p in folder.iterdir()} != allowed | {"integrity.json", "trials"}:
        raise ValueError("unexpected or missing root evidence")
    expected_trials = {n.split("/", 1)[1] for n in names if n.startswith("trials/")}
    if {p.name for p in (folder / "trials").iterdir()} != expected_trials:
        raise ValueError("unexpected or missing trial evidence")
    data = {}
    for name, expected in names.items():
        data[name] = read_json(folder / name)
        if digest((folder / name).read_bytes()) != expected:
            raise ValueError("evidence hash mismatch")
    manifest = require_shape(
        data["run.json"],
        {"format", "status", "started_at", "subject", "code_sha256", "python", "seed",
         "planned_ids", "fixtures_sha256", "network_or_model_calls", "boundaries"},
        "run manifest",
    )
    if manifest["format"] != FORMAT or manifest["code_sha256"] != code_identity():
        raise ValueError("implementation identity differs; use the recorded source revision")
    if manifest["subject"] != SUBJECT or manifest["network_or_model_calls"] != NETWORK_BOUNDARY:
        raise ValueError("scripted subject or network boundary changed")
    if manifest["boundaries"] != PROCESS_BOUNDARY:
        raise ValueError("process boundary changed")
    if not isinstance(manifest["python"], str) or not re.fullmatch(r"\d+\.\d+\.\d+", manifest["python"]):
        raise ValueError("invalid Python provenance")
    if not isinstance(manifest["started_at"], str):
        raise ValueError("invalid start time provenance")
    try:
        started_at = datetime.fromisoformat(manifest["started_at"])
    except ValueError as error:
        raise ValueError("invalid start time provenance") from error
    if started_at.utcoffset() != timezone.utc.utcoffset(None):
        raise ValueError("start time is not UTC")
    if manifest["fixtures_sha256"] != {w: digest(encoded(fixture(w))) for w in LOCATIONS}:
        raise ValueError("fixture identity mismatch")
    planned = manifest["planned_ids"]
    if (not isinstance(planned, list) or len(planned) != 10 or
            any(not isinstance(identity, str) or not re.fullmatch(r"[0-9a-f]{32}", identity)
                for identity in planned) or
            len(set(planned)) != 10 or {identity + ".json" for identity in planned} != expected_trials):
        raise ValueError("planned trial identity mismatch")
    trials = [data["trials/" + identity + ".json"] for identity in planned]
    cells = set()
    for identity, trial in zip(planned, trials):
        trial = require_shape(
            trial,
            {"id", "condition", "case", "status", "observations", "response", "checks", "error_type"},
            "trial",
        )
        world, condition = trial["case"]["world"], trial["condition"]
        if trial["id"] != identity or world not in LOCATIONS or condition not in CONDITIONS:
            raise ValueError("trial identity mismatch")
        if (world, condition) in cells or trial["case"] != fixture(world):
            raise ValueError("duplicate cell or changed case")
        cells.add((world, condition))
        tape, observations = input_tape(trial["case"], condition), trial["observations"]
        status = trial["status"]
        if not isinstance(observations, list):
            raise ValueError("invalid observations")
        if status not in {"completed", "error", "interrupted", "not-run"}:
            raise ValueError("unfinished trial; do not infer an outcome")
        if len(observations) > len(tape):
            raise ValueError("extra observations")
        for ordinal, observation in enumerate(observations):
            observation = require_shape(
                observation, {"ordinal", "input", "status", "output"}, "observation"
            )
            if observation["ordinal"] != ordinal or observation["input"] != tape[ordinal]:
                raise ValueError("observation identity/order mismatch")
            if observation["status"] not in {"attempted", "returned"}:
                raise ValueError("invalid observation state")
            if observation["status"] == "attempted" and (ordinal != len(observations) - 1 or status == "completed"):
                raise ValueError("unresolved observation")
            expected_output = trial["response"] if tape[ordinal]["operation"] == "probe" and observation["status"] == "returned" else None
            if observation["output"] != expected_output:
                raise ValueError("response/observation mismatch")
        if status == "completed":
            if len(observations) != len(tape) or not isinstance(trial["response"], str) or not trial["response"].strip():
                raise ValueError("incomplete response")
            if trial["error_type"] is not None or trial["checks"] != literal_checks(trial["response"], trial["case"]):
                raise ValueError("diagnostic mismatch")
        elif trial["checks"] is not None:
            raise ValueError("uncompleted trial was scored")
        if status == "not-run" and (observations or trial["response"] is not None or trial["error_type"] is not None):
            raise ValueError("not-run trial contains execution evidence")
        if status in {"error", "interrupted"} and not trial["error_type"]:
            raise ValueError("missing execution error")
    if [(trial["case"]["world"], trial["condition"]) for trial in trials] != planned_cells(manifest["seed"]):
        raise ValueError("seed and trial plan differ")
    statuses = {t["status"] for t in trials}
    expected_status = "interrupted" if "interrupted" in statuses else "complete-with-errors" if "error" in statuses else "completed"
    if manifest["status"] != expected_status or ("not-run" in statuses and "interrupted" not in statuses):
        raise ValueError("run completion mismatch")
    if data["summary.json"] != summarize(trials):
        raise ValueError("summary mismatch")
    key, packet = data["review-key.json"], data["review-packet.json"]
    if not isinstance(key, dict) or not isinstance(packet, list):
        raise ValueError("invalid review evidence shape")
    completed = {t["id"]: t for t in trials if t["status"] == "completed"}
    if len(packet) != len(completed) or set(key.values()) != set(completed) or len(key) != len(completed):
        raise ValueError("review coverage mismatch")
    seen = set()
    for entry in packet:
        entry = require_shape(
            entry,
            {"alias", "event_evidence", "evidence_contract", "probe", "response", "decision",
             "cited_span", "confidence", "alternative_reading"},
            "review entry",
        )
        alias = entry["alias"]
        if alias in seen or alias not in key or not re.fullmatch(r"R-[0-9a-f]{32}", alias):
            raise ValueError("review alias mismatch")
        seen.add(alias)
        trial = completed[key[alias]]
        expected = {"alias": alias, "event_evidence": trial["case"]["history"],
                    "evidence_contract": trial["case"]["evidence_contract"],
                    "probe": PROBE, "response": trial["response"], "decision": None,
                    "cited_span": None, "confidence": None, "alternative_reading": None}
        if entry != expected:
            raise ValueError("review evidence changed or identity leaked")
    expected_review_order = [trial["id"] for trial in trials if trial["status"] == "completed"]
    random.Random(manifest["seed"]).shuffle(expected_review_order)
    if [key[entry["alias"]] for entry in packet] != expected_review_order:
        raise ValueError("seed and review plan differ")
    return {"integrity": "valid", "execution": manifest["status"], **summarize(trials)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    execute = commands.add_parser("run", help="run bundled synthetic plumbing double only")
    execute.add_argument("--output", type=Path, required=True, help="new directory; parent must exist")
    execute.add_argument("--seed", type=int, default=0)
    inspect = commands.add_parser("verify", help="offline integrity and evidence-binding checks; never replay code")
    inspect.add_argument("directory", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "verify":
            print(encoded(verify(args.directory)).decode(), end="")
            return 0
        manifest = run(args.output, args.seed)
        print(encoded({"execution": manifest["status"], "evidence": "scripted-only", "output": str(args.output)}).decode(), end="")
        return 0 if manifest["status"] == "completed" else 1
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Rehearsal failed: {type(error).__name__}; evidence is absent, incomplete, incompatible or invalid.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
