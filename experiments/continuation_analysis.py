"""Offline, receipt-bound descriptive analysis of the fixed ADR-0012 study.

No provider access, pooled development/test estimate, or overall memory score.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from contextlib import closing
import csv
import io
import json
from pathlib import Path
import sqlite3
from statistics import mean

from continuation_api import MODELS, canonical, digest, output_text, private_directory
from continuation_core import judge_payload, reader_payload, validate_judgment

CONDITIONS = ("current", "search", "summary", "notes", "full")
DIMENSIONS = ("progress", "fidelity", "intrusion")
BINARY = {"met": 1.0, "not_met": 0.0}
REVIEW_VERSION = "v4"


def review_payload(history, probe, oracle, answer):
    """Select source lines instead of asking a reviewer to recopy quotations."""
    payload = judge_payload(history, probe, oracle, answer)
    semantic, marker, _ = payload["instructions"].partition("answer_quote须")
    if not marker:
        raise ValueError("base review contract changed; inspect the versioned protocol")
    payload["instructions"] = semantic + (
        "候选答案按原始顺序显示为candidate_answer_lines，每行有line和text。必须阅读整份回答。"
        "每条criterion用answer_line选择一个最能支持判断的原文行号，不自行改写引文。"
        "若判断的是遗漏或不适用，可以用0，reason必须明确说明缺失或不适用之处。"
        "选行只是证据定位，不表示只审查该行；其余依据写在reason中。"
        "evidence_episode_ids只引用实际提供的来源episode。"
        "返回JSON object，criteria是按每个criterion ID键控的object，逐项给出judgment、answer_line、evidence_episode_ids和reason；另给overall_note。"
        "覆盖所有criterion，保留不确定，不计算总分。")
    body = json.loads(payload["input"])
    body.pop("candidate_answer")
    body["candidate_answer_lines"] = [{"line": i, "text": line} for i, line in enumerate(answer.splitlines(), 1)]
    payload["input"] = canonical(body)
    return payload


def review_schema(oracle, answer):
    def obj(properties):
        return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}
    row = obj({"judgment": {"type": "string", "enum": ["met", "not_met", "uncertain", "not_applicable"]},
        "answer_line": {"type": "integer", "minimum": 0, "maximum": len(answer.splitlines())},
        "evidence_episode_ids": {"type": "array", "items": {"type": "string", "enum": [f"E{i}" for i in range(1, 7)]}, "maxItems": 6},
        "reason": {"type": "string"}})
    return obj({"criteria": obj({c["id"]: row for c in oracle["criteria"]}), "overall_note": {"type": "string"}})


def decode_review(value, oracle, answer, history):
    """Materialize the selected literal line, then apply existing evidence checks."""
    if not isinstance(value, dict) or set(value) != {"criteria", "overall_note"}:
        raise ValueError("invalid review root")
    rows = value["criteria"]
    if not isinstance(rows, dict) or set(rows) != {c["id"] for c in oracle["criteria"]}:
        raise ValueError("review must cover every criterion exactly once")
    lines, criteria = answer.splitlines(), []
    for criterion in oracle["criteria"]:
        row = rows[criterion["id"]]
        if not isinstance(row, dict) or set(row) != {"judgment", "answer_line", "evidence_episode_ids", "reason"}:
            raise ValueError("invalid review fields")
        number = row["answer_line"]
        if type(number) is not int or not 0 <= number <= len(lines):
            raise ValueError("answer line outside literal candidate")
        criteria.append({"id": criterion["id"], "judgment": row["judgment"],
            "answer_quote": lines[number-1] if number else "", "evidence_episode_ids": row["evidence_episode_ids"], "reason": row["reason"]})
    return validate_judgment({"criteria": criteria, "overall_note": value["overall_note"]}, oracle, answer, history)


def read_json(path):
    return json.loads(Path(path).read_text())


class Evidence:
    """Read the existing immutable receipts; never create or resume a run."""
    def __init__(self, run_dir, values, split):
        self.root = Path(run_dir).resolve()
        hids = {h["id"] for h in values[0]}
        with closing(sqlite3.connect(self.root.joinpath("dispatch.sqlite").as_uri() + "?mode=ro", uri=True)) as db:
            db.row_factory = sqlite3.Row
            self.operations = defaultdict(list)
            for row in db.execute("SELECT * FROM attempts ORDER BY id"):
                parts = row["operation"].split("/")
                relevant = len(parts) >= 3 and parts[0] in ("formation", "reader", "reviews", "review-audit") and parts[2].split("-")[0] in hids
                if row["state"] == "started" and relevant:
                    raise ValueError("report requires settled requests; collection is still active")
                self.operations[row["operation"]].append(dict(row))
            binding = db.execute("SELECT value FROM meta WHERE key=?", ("binding:source-v1:" + split,)).fetchone()
        expected = [{"schema": "relata.continuation-histories/v1", "histories": values[0]},
                    {"schema": "relata.continuation-probes/v1", "probes": values[1]},
                    {"schema": "relata.continuation-oracles/v1", "oracles": values[2]}]
        if not binding or json.loads(binding[0]) != expected:
            raise ValueError("analysis source differs from the exact frozen run binding")

    def receipt(self, operation):
        rows = self.operations.get(operation, [])
        successful = [r for r in rows if r["state"] == "succeeded"]
        return successful[-1] if successful else (rows[-1] if rows else None)

    def answer(self, history, probe, condition, model):
        path = self.root / "answers" / probe["id"] / condition / (model + ".json")
        receipt = self.receipt(f"reader/v1/{probe['id']}/{condition}/{model}")
        if not path.exists():
            if not receipt and condition in ("summary", "notes") and not (self.root / "memory" / history["id"] / condition / "E6.json").exists():
                return None, "upstream_memory_unavailable"
            return None, "artifact_missing" if receipt else "not_run"
        record = read_json(path)
        identity = (record.get("history_id"), record.get("probe_id"), record.get("condition"), record.get("requested_model"))
        if identity != (history["id"], probe["id"], condition, model) or not receipt:
            raise ValueError("answer identity or receipt mismatch")
        body = json.loads(receipt["request_json"])
        delivered = json.loads(body["input"])
        payload = reader_payload(history, probe, condition, delivered["retained_memory"], record["ranking"])
        if body["model"] != model or body["instructions"] != payload["instructions"] or body["input"] != payload["input"] or record["exposure"] != payload["exposure"]:
            raise ValueError("answer exposure does not match the exact provider input")
        if condition in ("summary", "notes"):
            writer = self.receipt(f"formation/v1/{history['id']}/{condition}/E6")
            if not writer or writer["state"] != "succeeded" or output_text(json.loads(writer["response_text"])) != delivered["retained_memory"]:
                raise ValueError("reader memory is not the recorded final writer output")
        if receipt["state"] == "succeeded":
            response = json.loads(receipt["response_text"])
            try:
                answer, state = output_text(response), "completed"
            except ValueError:
                answer, state = "", "incomplete_or_empty"
            if (record["state"], record["answer"], record["response_id"], record["returned_model"], record["usage"]) != (
                    state, answer, response.get("id"), response.get("model"), response.get("usage")):
                raise ValueError("answer differs from the literal provider receipt")
        elif record["state"] != receipt["state"] or record["answer"] or record["response_id"] is not None:
            raise ValueError("technical outcome was rewritten as a semantic answer")
        return record, record["state"]

    def review(self, history, probe, oracle, condition, model, record, *, audit=False):
        directory = "review-audit" if audit else "reviews"
        path = self.root / directory / REVIEW_VERSION / probe["id"] / condition / (model + ".json")
        if record is None or record["state"] != "completed":
            return None, "answer_unavailable"
        if not path.exists():
            receipt = self.receipt(f"{directory}/{REVIEW_VERSION}/{probe['id']}/{condition}/{model}")
            return None, receipt["state"] if receipt and receipt["state"] != "succeeded" else "review_missing"
        review = read_json(path)
        if review["answer_digest"] != digest(record) or review["oracle_digest"] != digest(oracle):
            raise ValueError("review bound to a different answer or criterion contract")
        receipt = self.receipt(f"{directory}/{REVIEW_VERSION}/{probe['id']}/{condition}/{model}")
        if not receipt or receipt["state"] != "succeeded":
            raise ValueError("review has no successful provider receipt")
        response, body = json.loads(receipt["response_text"]), json.loads(receipt["request_json"])
        payload = review_payload(history, probe, oracle, record["answer"])
        if body["instructions"] != payload["instructions"] or body["input"] != payload["input"] or body.get("text", {}).get("format", {}).get("schema") != review_schema(oracle, record["answer"]):
            raise ValueError("review input differs from its blinded governing material")
        if body["model"] != (MODELS[0] if audit else MODELS[1]) or review["response_id"] != response.get("id"):
            raise ValueError("review model or response identity mismatch")
        try:
            raw = json.loads(output_text(response))
        except ValueError as exc:
            expected = {"response_status": response.get("status"), "validation_error": str(exc)}
            if review["state"] != "invalid_review_response" or review["judgment"] != expected:
                raise ValueError("invalid review response was altered or promoted")
            return None, "invalid_review_response"
        try:
            valid = decode_review(raw, oracle, record["answer"], history)
        except ValueError:
            if review["state"] != "invalid_review" or review["judgment"].get("raw") != raw:
                raise ValueError("invalid review was altered or promoted")
            return None, "invalid_review"
        if review["state"] != "valid" or review["judgment"] != valid:
            raise ValueError("review differs from literal validated judgment")
        return {c["id"]: c for c in valid["criteria"]}, "valid"


def collect(values, root, split):
    histories, probes, oracles = values
    evidence = Evidence(root, values, split)
    hmap = {h["id"]: h for h in histories}
    omap = {o["probe_id"]: o for o in oracles}
    audit_ids = ({f"T{base+i:02d}" for base in (0, 12, 24, 36) for i in (2, 5, 8, 11)}
                 if split == "test" else {"D01", "D04", "D07", "D10"})
    answers, rows = [], []
    identities = []
    for probe in probes:
        history, oracle = hmap[probe["history_id"]], omap[probe["id"]]
        for condition in CONDITIONS:
            for model in MODELS:
                record, state = evidence.answer(history, probe, condition, model)
                judged, review_state = evidence.review(history, probe, oracle, condition, model, record)
                secondary, audit_state = (None, "not_selected")
                if history["id"] in audit_ids:
                    secondary, audit_state = evidence.review(history, probe, oracle, condition, model, record, audit=True)
                base = {"history_id": history["id"], "coverage": history["coverage"], "probe_id": probe["id"],
                        "kind": probe["kind"], "condition": condition, "model": model, "answer_state": state,
                        "review_state": review_state, "audit_state": audit_state}
                answers.append({**base, "input_bytes": record["exposure"]["input_bytes"] if record else None,
                                "usage": record.get("usage") if record else None})
                identities.append({**base, "answer_digest": digest(record) if record else None,
                                   "review_digest": digest(judged), "audit_digest": digest(secondary)})
                for criterion in oracle["criteria"]:
                    primary = judged.get(criterion["id"]) if judged else None
                    other = secondary.get(criterion["id"]) if secondary else None
                    rows.append({**base, "criterion_id": criterion["id"], "dimension": criterion["dimension"],
                        "verdict": primary["judgment"] if primary else review_state,
                        "audit_verdict": other["judgment"] if other else audit_state,
                        "answer_quote": primary["answer_quote"] if primary else "",
                        "reason": primary["reason"] if primary else ""})
    return answers, rows, digest(identities)


def comparisons(rows):
    """Equal weight per probe within a history; complete paired histories only.

    A nonbinary judgment excludes that whole history for this dimension/kind
    contrast. NA is never success, and missingness is never failure.
    """
    results = []
    for model in MODELS:
        for left, right in (("search", "current"), ("summary", "search"), ("notes", "search"), ("full", "search"), ("notes", "summary")):
            for dimension in DIMENSIONS:
                for kind in ("all", "continue", "reconnect", "historical", "unrelated"):
                    relevant = [r for r in rows if r["model"] == model and r["dimension"] == dimension
                                and r["condition"] in (left, right) and (kind == "all" or r["kind"] == kind)]
                    by_history = defaultdict(lambda: defaultdict(dict))
                    for row in relevant:
                        by_history[row["history_id"]][row["condition"]][(row["probe_id"], row["criterion_id"])] = row["verdict"]
                    differences = []
                    for hid, arms in sorted(by_history.items()):
                        a, b = arms[left], arms[right]
                        if not a or a.keys() != b.keys() or any(v not in BINARY for v in [*a.values(), *b.values()]):
                            continue
                        per_probe = defaultdict(list)
                        for key in a:
                            per_probe[key[0]].append(BINARY[a[key]] - BINARY[b[key]])
                        differences.append({"history_id": hid, "difference": mean(mean(x) for x in per_probe.values())})
                    if by_history:
                        vals = [d["difference"] for d in differences]
                        results.append({"model": model, "left": left, "right": right, "dimension": dimension,
                            "contrast_role": "secondary_formulation" if (left, right) == ("notes", "summary") else "primary",
                            "kind": kind, "planned_histories": len(by_history), "paired_histories": len(vals),
                            "excluded_histories": len(by_history) - len(vals),
                            "mean_difference": mean(vals) if vals else None,
                            "better": sum(x > 1e-12 for x in vals), "tie": sum(abs(x) <= 1e-12 for x in vals),
                            "worse": sum(x < -1e-12 for x in vals), "history_differences": differences})
    return results


def summarize(answers, rows, split, evidence_digest):
    groups = defaultdict(Counter)
    for row in rows:
        groups[(row["model"], row["condition"], row["dimension"])][row["verdict"]] += 1
    counts = [{"model": key[0], "condition": key[1], "dimension": key[2], "judgments": dict(value)}
              for key, value in sorted(groups.items())]
    agreement = Counter()
    disagreements = []
    for row in rows:
        if row["review_state"] == row["audit_state"] == "valid":
            same = row["verdict"] == row["audit_verdict"]
            agreement["agree" if same else "disagree"] += 1
            if not same:
                disagreements.append({k: row[k] for k in ("history_id", "probe_id", "condition", "model", "criterion_id", "verdict", "audit_verdict")})
    return {"schema": "relata.continuation-descriptive/v1", "split": split, "review_version": REVIEW_VERSION, "evidence_digest": evidence_digest,
        "planned_histories": len({a["history_id"] for a in answers}), "planned_answer_positions": len(answers),
        "answer_states": dict(Counter(a["answer_state"] for a in answers)),
        "review_states": dict(Counter(a["review_state"] for a in answers)),
        "audit_states": dict(Counter(a["audit_state"] for a in answers)),
        "criterion_counts": counts, "comparisons": comparisons(rows),
        "audit_agreement": dict(agreement), "audit_disagreements": disagreements}


def render_report(data):
    lines = ["# Continuation-use 描述性报告", "",
        f"Split：{data['split']}；review {data['review_version']}；{data['planned_histories']} histories，{data['planned_answer_positions']}个计划回答位置。", "",
        "这是原创合成材料上的 AI-assisted criterion review，不是独立人类校准、response accuracy 或通用 memory score。development 与正式 comparison 分开；同一 history 内的任务及共同作者设计均有关联。", "",
        f"答案状态：`{canonical(data['answer_states'])}`。", f"主评审状态：`{canonical(data['review_states'])}`。",
        f"复核状态：`{canonical(data['audit_states'])}`；有效共同criterion上的一致/分歧：`{canonical(data['audit_agreement'])}`。", "",
        "## 分维度判断分布", "", "| Reader | 条件 | 维度 | criterion 判断数量 |", "| --- | --- | --- | --- |"]
    for row in data["criterion_counts"]:
        lines.append(f"| {row['model']} | {row['condition']} | {row['dimension']} | {canonical(row['judgments'])} |")
    lines += ["", "## 任务推进：按完整 history 配对", "",
        "每题先平均其 progress criteria，再对同一history的三个题等权平均。仅纳入两臂所有相关criteria均为met/not_met的完整history；技术缺失、uncertain、NA不填零。差值为左条件减右条件的作者criterion符合比例，不能解释成关系质量或通用任务准确率。", "",
        "| Reader | 对比 | 纳入/计划 histories | 平均差值 | 正/平/负 histories |", "| --- | --- | --- | --- | --- |"]
    for row in data["comparisons"]:
        if row["dimension"] != "progress" or row["kind"] != "all":
            continue
        delta = "不可计算" if row["mean_difference"] is None else f"{row['mean_difference']:+.3f}"
        lines.append(f"| {row['model']} | {row['left']} − {row['right']} | {row['paired_histories']}/{row['planned_histories']} | {delta} | {row['better']}/{row['tie']}/{row['worse']} |")
    lines += ["", "notes−summary为直接比较两种写法的次要描述性对比，仍用其自身共同有效的history，不能用两个不同complete-case集合的对search差值相减替代。JSON另保留按任务类型/维度的配对分母、每history差值及全部双judge分歧；criterion CSV保留逐条证据。fidelity的NA常与是否提及历史有关，不能把较少历史展示带来的NA当成更忠实。", "",
        "这份自动报告负责证据绑定和描述性统计。Mega Essay/Tilia机制解释需要另读实际来源、生成memory、暴露的检索片段及答案；统计本身不证明 memory 被如何使用。", ""]
    return "\n".join(lines)


def write_report(values, run_dir, split):
    answers, rows, identity = collect(values, run_dir, split)
    data = summarize(answers, rows, split, identity)
    directory = private_directory(Path(run_dir) / "reports" / (split + "-" + digest(data)[:16]))
    table = io.StringIO()
    writer = csv.DictWriter(table, fieldnames=list(rows[0]) if rows else [])
    writer.writeheader()
    writer.writerows(rows)
    outputs = {"report.json": json.dumps(data, ensure_ascii=False, indent=2) + "\n",
               "report.md": render_report(data), "criteria.csv": table.getvalue()}
    for name, content in outputs.items():
        path = directory / name
        if path.exists():
            if path.read_bytes() != content.encode("utf-8"):
                raise ValueError("refusing to rewrite a report snapshot")
        else:
            path.write_text(content)
            path.chmod(0o600)
    return {"report": str(directory / "report.md"), "answer_states": data["answer_states"],
            "review_states": data["review_states"], "planned_histories": data["planned_histories"]}
