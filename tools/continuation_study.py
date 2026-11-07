#!/usr/bin/env python3
"""Named ADR-0012 study. Its only corpus is research/continuation-use/."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import math
import os
import random
from pathlib import Path
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from continuation_api import StudyAPI, DispatchError, MODELS, canonical, digest, output_text

MATERIAL = ROOT / "research" / "continuation-use"
CONDITIONS = ("current", "search", "summary", "notes", "full")

MATERIAL_INSTRUCTIONS = """你是原创合成研究材料的作者。只创作虚构成年人、虚构对话和资料，不引用真实私人聊天。
所有出现的人，包括配角、活动参与者和观众，都必须是成年人。不要写儿童、小朋友、未成年人；木偶/手工等活动也面向成人。
你的任务是写一段细节充分、自然发展、可供后来重新使用的共同经历，而不是把抽象规则换成人名。
人物、事件、具体物件、原话与中间思考都要真实可读。普通工作、生活与关系可以交错；不要强行把每件事浪漫化。
六个episode，每个220到500个中文字符（所有messages合计），每个至少一条user和一条assistant，允许2到4条message。
要有明确的积极进展、仍有价值的旧材料、未决的问题、一次新理解及至少一个普通支线。不要把每条历史写成撤销权限或更正规则。
assistant可以提出自己的看法，user可以同意、保留不同理解或改变主意；来源事实、解释、已选择与备选自然区分。
三项后续任务有具体可交付的行为，不要只问能否记住姓名日期。continue要求接着做事，reconnect提出未预告的新用途或材料。
第三项按指定kind写：historical问过去某选择的理由/变化；unrelated给完整自足的普通任务、无须借历史回答，例如提供明确时间/物品/数字的整理、计划、短消息写作。避免要求医疗、食物存储安全、法律金融知识或外部实时事实。
当前任务不能把有用历史答案重新全部写给reader。必要局部语境可以给，但不能点明应调用哪一段memory或暴露评分点。
reconnect允许多种有根据的联想与做法，不把作者喜欢的一种解读写成唯一正确答案。
oracle每题3到5条有限criteria，至少一条progress。progress含当前指令的遵守，fidelity仅评价历史来源的忠实使用，intrusion评价不恰当的历史侵入或替人作未定判断。unrelated必须有一条intrusion、其余为progress，不设历史fidelity要求。
expectation表述可观察的回应行为，避免主观赞美或僵硬逐字答案。criteria必须与allowed_alternatives相容，不可一边要求至少两种做法、一边又允许只做一种。允许的其他方案不能被criteria判失败。
每题evidence引用原episode某条message中真实存在的连续原文；exact quote请复制，不要改写。unrelated可用空evidence。
allowed_alternatives给出至少两个有理由的其他合法做法，包括适当的不确定或不显式提旧事。
输出一个JSON object，无Markdown，字段只有history、probes、oracles；所有ID精确按要求。
history={id,split,coverage,title,episodes:[{id:'E1'... 'E6',day:'第1天'等,messages:[{role:'user'或'assistant',text:字符串}]}]}。
probes=[{id:'给定ID-P1'等,history_id:给定ID,kind:指定值,messages:[{role:'user',text:字符串}]}]，最后message必须user。
oracles=[{probe_id:对应probeID,rationale:字符串,evidence:[{episode_id:'E1',quote:原文}],criteria:[{id:'C1'等,dimension:'progress'或'fidelity'或'intrusion',expectation:字符串}],allowed_alternatives:[字符串]}]。
这里的oracle是作者解释而非机器真理。不要生成分数、模型输出、哈希、隐私声明或研究结论。"""


def read_json(path):
    return json.loads(Path(path).read_text())


def save_once(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    encoded = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if path.exists():
        if path.read_text() != encoded:
            raise ValueError("refusing to rewrite immutable artifact: " + str(path))
        return
    # Publish a complete private file atomically, without replacing an existing
    # artifact. A reboot can leave a temporary file, not a half-written receipt.
    fd, temporary = tempfile.mkstemp(prefix=".pending-", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as file:
            file.write(encoded)
            file.flush()
            os.fsync(file.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            if path.read_text() != encoded:
                raise ValueError("conflicting immutable artifact: " + str(path))
    finally:
        os.unlink(temporary)


def save_answer(path, value):
    """Preserve the first ranking receipt across harmless floating-point roundoff.

    The exact provider request is already bound by the ledger. Episode order and
    all other answer/exposure fields must still match; no artifact is rewritten.
    """
    path = Path(path)
    if path.exists():
        old = read_json(path)
        before, after = old.get("ranking", []), value.get("ranking", [])
        same = len(before) == len(after) and all(
            x.get("episode_id") == y.get("episode_id")
            and all(math.isclose(x[k], y[k], rel_tol=1e-12, abs_tol=1e-12)
                    for k in ("dense", "lexical", "rrf"))
            for x, y in zip(before, after))
        if same:
            value = {**value, "ranking": before}
    save_once(path, value)


def runtime(args):
    config = read_json(args.runtime_config)
    if set(config) != {"run_dir", "credential_file"}:
        raise ValueError("runtime config contains only run_dir and credential_file references")
    api = StudyAPI(config["run_dir"], config["credential_file"])
    api.bind("execution-envelope", {"study": "ADR-0012", "generation_cap": 6000,
        "embedding_cap": 300, "usd_ceiling": 120, "models": list(MODELS), "writer": MODELS[0]})
    return api


def seeds(split):
    design = read_json(MATERIAL / "material-design.json")
    prefix = "D" if split == "development" else "T"
    result = []
    for coverage, items in design[split].items():
        for title, direction in items:
            i = len(result) + 1
            result.append({"id": f"{prefix}{i:02d}", "split": split, "coverage": coverage,
                "title": title, "direction": direction,
                "kinds": ["continue", "reconnect", "historical" if i % 2 else "unrelated"],
                "author_model": MODELS[(i - 1) % 2]})
    return result


def select(items, ids):
    if not ids:
        return items
    chosen = set(ids.split(","))
    if not chosen <= {item["id"] for item in items}:
        raise ValueError("IDs are outside the fixed selected split")
    return [item for item in items if item["id"] in chosen]


def parallel(items, fn, workers):
    errors = []
    stopped = threading.Event()
    def guarded(item):
        if stopped.is_set():
            return None
        try:
            return fn(item)
        except Exception:
            stopped.set()
            raise
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(guarded, item): item for item in items}
        for future in as_completed(futures):
            item = futures[future]
            try:
                result = future.result()
                if result is None:
                    continue
                print(canonical({"event": "completed", "item": item.get("id", str(item)), "result": result}), flush=True)
            except Exception as error:
                errors.append({"item": item.get("id", str(item)), "type": type(error).__name__, "error": str(error)})
                print(canonical({"event": "failed", **errors[-1]}), flush=True)
    if errors:
        raise RuntimeError(f"{len(errors)} operations failed; preserve records and inspect before resuming")


def generate_materials(args, api):
    api.bind("material-design-v1", read_json(MATERIAL / "material-design.json"))
    version = material_version(args.split)
    api.bind("material-prompt-" + version, MATERIAL_INSTRUCTIONS)
    items = select(seeds(args.split), args.ids)
    def generate(seed):
        path = api.run_dir / "material-drafts" / version / (seed["id"] + ".json")
        payload = {"instructions": MATERIAL_INSTRUCTIONS,
                   "input": "依照以下原创seed创作完整材料，输出JSON：\n" + canonical(seed)}
        result = api.response("material/" + version + "/" + seed["id"], seed["author_model"], payload, cap=12000,
                              json_output=True, json_schema=material_schema(seed) if version == "v3" else None)
        text = output_text(result)
        value = json.loads(text)
        if set(value) != {"history", "probes", "oracles"}:
            raise ValueError("material must separate history/probes/oracles")
        if value["history"].get("id") != seed["id"]:
            raise ValueError("material identity mismatch")
        save_once(path, value)
        return {"author_model": seed["author_model"], "episodes": len(value["history"].get("episodes", [])),
                "probes": len(value["probes"]), "output_characters": len(text)}
    parallel(items, generate, args.workers)


def draft_path(api, identity):
    revision = api.run_dir / "material-replacements" / (identity + ".json")
    if revision.exists():
        return revision
    version = "v2" if identity.startswith("D") else "v3"
    return api.run_dir / "material-drafts" / version / (identity + ".json")


def replace_lost_material(args, api):
    if not args.ids:
        raise ValueError("explicit missing material IDs required; no automatic replacement")
    items = select(seeds(args.split), args.ids)
    def replace(seed):
        original = "material/" + material_version(args.split) + "/" + seed["id"]
        states = api.operation_states(original)
        if not states or any(row["state"] != "uncertain" for row in states):
            raise ValueError("replacement is only for unobservable authoring drafts, never scored answers")
        instructions = MATERIAL_INSTRUCTIONS + "\n独立创作这一主题的另一份完整作者修订。使用新的虚构人物和具体物件细节；原始草稿没有可用正文，不假设它包含任何内容。"
        payload = {"instructions": instructions, "input": "创作新的完整JSON作者修订：\n" + canonical(seed)}
        response = api.response("material/replacement-v1/" + seed["id"], seed["author_model"], payload,
                                cap=12000, json_schema=material_schema(seed))
        value = json.loads(output_text(response))
        save_once(api.run_dir / "material-replacements" / (seed["id"] + ".json"), value)
        save_once(api.run_dir / "material-replacements" / (seed["id"] + ".provenance.json"),
                  {"original_attempts": states, "original_state": "uncertain, reservation retained",
                   "replacement_response_id": response.get("id"), "purpose": "pre-freeze authored material only"})
        return {"material_revision": seed["id"], "original_receipt_preserved": True}
    parallel(items, replace, args.workers)


def material_version(split):
    return "v2" if split == "development" else "v3"


def material_schema(seed):
    def string(values=None):
        result = {"type": "string"}
        if values is not None:
            result["enum"] = values
        return result
    def obj(properties):
        return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}
    def array(items, lo, hi):
        return {"type": "array", "items": items, "minItems": lo, "maxItems": hi}
    episodes = [f"E{i}" for i in range(1, 7)]
    probes = [seed["id"] + f"-P{i}" for i in range(1, 4)]
    message = obj({"role": string(["user", "assistant"]), "text": string()})
    history = obj({"id": string([seed["id"]]), "split": string([seed["split"]]),
        "coverage": string([seed["coverage"]]), "title": string(),
        "episodes": array(obj({"id": string(episodes), "day": string(), "messages": array(message, 2, 4)}), 6, 6)})
    probe = obj({"id": string(probes), "history_id": string([seed["id"]]), "kind": string(seed["kinds"]),
                 "messages": array(message, 1, 3)})
    oracle = obj({"probe_id": string(probes), "rationale": string(),
        "evidence": array(obj({"episode_id": string(episodes), "quote": string()}), 0, 8),
        "criteria": array(obj({"id": string([f"C{i}" for i in range(1, 6)]),
                               "dimension": string(["progress", "fidelity", "intrusion"]), "expectation": string()}), 3, 5),
        "allowed_alternatives": array(string(), 2, 5)})
    return obj({"history": history, "probes": array(probe, 3, 3), "oracles": array(oracle, 3, 3)})


def check_materials(args, api):
    from continuation_core import validate_bundle
    items = select(seeds(args.split), args.ids)
    histories, probes, oracles = [], [], []
    for seed in items:
        value = read_json(draft_path(api, seed["id"]))
        histories.append(value["history"])
        probes.extend(value["probes"])
        oracles.extend(value["oracles"])
    values = bundle_roots(histories, probes, oracles)
    result = validate_bundle(*values, require_full=False)
    print(canonical({"validation": result}), flush=True)
    for h in histories:
        print(canonical({"id": h["id"], "episode_characters": [sum(len(m["text"]) for m in e["messages"]) for e in h["episodes"]]}), flush=True)


def bundle_roots(histories, probes, oracles):
    return ({"schema": "relata.continuation-histories/v1", "histories": histories},
            {"schema": "relata.continuation-probes/v1", "probes": probes},
            {"schema": "relata.continuation-oracles/v1", "oracles": oracles})


MATERIAL_REVIEW = """你审查一组原创成人合成研究材料，而不是给某个system under study打分。请读完整history、probes与oracles。先确认恰好六个episode E1到E6，且evidence引用的episode与原话实际存在。
检查(1)未来问题有没有直接泄漏本应由过去提供的实质答案；(2)criteria是否有原文依据、是否与allowed_alternatives冲突或把合理回答排除；
(3)source evidence是否把assistant推测当成user事实；(4)六阶段是否有真实可继续的事情和正面收益机会，而不是只有撤回/权限/字词谜题；
(5)是否混入未成年人；(6)unrelated是否自足、不需外部事实、不要求历史fidelity且含不干扰criterion。
不要要求所有任务只有一种答案。把可导致错误实验结论的缺陷标must_fix，真正可选的改善标consider。勿为凑问题找茬。
输出JSON object：{adequate:boolean, issues:[{severity:'must_fix'或'consider',path:准确对象路径,problem:具体问题,suggested_change:最小修改建议}], note:字符串}。
这是AI辅助作者审阅，不是独立人类校准。不要重写材料，不要猜测模型表现或添加拟议实验结果。"""


def review_materials(args, api):
    items = select(seeds(args.split), args.ids)
    version = "v1" if args.split == "development" else "v2"
    instructions = MATERIAL_REVIEW
    if version == "v2":
        instructions += "\n关键：历史中包含后来要用的事实/方法/理由是正常的记忆来源，绝不是答案泄漏。只有当前probe自己已给出所评历史答案才是泄漏。问题提到方法名字但仍要问其原因，不等于提供了原因。reconnect允许不显式提历史，条件性要求‘如果提及就准确’可以合法；不要把它误判成强制历史展示。"
    api.bind("material-review-" + version, instructions)
    def review(seed):
        value = read_json(draft_path(api, seed["id"]))
        reviewer = MODELS[1 - MODELS.index(seed["author_model"])]
        response = api.response("material-review/" + version + "/" + seed["id"], reviewer,
            {"instructions": instructions, "input": "审查以下JSON材料：\n" + canonical(value)}, json_output=True)
        judgment = json.loads(output_text(response))
        if not isinstance(judgment.get("issues"), list) or type(judgment.get("adequate")) is not bool:
            raise ValueError("invalid material review")
        save_once(api.run_dir / "material-reviews" / (seed["id"] + ".json"), judgment)
        return {"reviewer": reviewer, "adequate": judgment["adequate"], "issues": judgment["issues"]}
    parallel(items, review, args.workers)


def source_bundle(split):
    from continuation_core import validate_bundle
    values = [read_json(MATERIAL / name) for name in ("histories.json", "probes.json", "oracles.json")]
    validate_bundle(*values, require_full=(split == "test"))
    histories = [h for h in values[0]["histories"] if h["split"] == split]
    hids = {h["id"] for h in histories}
    probes = [p for p in values[1]["probes"] if p["history_id"] in hids]
    pids = {p["id"] for p in probes}
    oracles = [o for o in values[2]["oracles"] if o["probe_id"] in pids]
    return histories, probes, oracles


def freeze_sources(api, split):
    values = source_bundle(split)
    api.bind("source-v1:" + split, bundle_roots(*values))
    api.bind("core-v1:" + split, {"source_sha256": digest((ROOT / "experiments" / "continuation_core.py").read_text()),
                                "conditions": CONDITIONS, "writer": MODELS[0]})
    return values


def form_memories(args, api):
    from continuation_core import writer_payload
    histories, _, _ = freeze_sources(api, args.split)
    def form(history):
        completed, unavailable = 0, []
        for condition in ("summary", "notes"):
            memory = ""
            for index, episode in enumerate(history["episodes"]):
                payload = writer_payload(history, index, memory, condition)
                key = f"formation/v1/{history['id']}/{condition}/{episode['id']}"
                prior = api.operation_states(key)
                try:
                    response = api.response(key, MODELS[0], payload)
                except DispatchError:
                    if prior and all(row["state"] not in ("started", "succeeded") for row in prior):
                        unavailable.append({"condition": condition, "episode": episode["id"], "state": prior[-1]["state"]})
                        break
                    raise
                try:
                    text = output_text(response)
                    if len(text.encode()) > 6000:
                        raise ValueError("memory exceeds exposure cap")
                except ValueError as exc:
                    unavailable.append({"condition": condition, "episode": episode["id"], "state": "invalid_memory", "reason": str(exc)})
                    break
                save_once(api.run_dir / "memory" / history["id"] / condition / (episode["id"] + ".json"),
                          {"text": text, "response_id": response.get("id"), "model": response.get("model"),
                           "episode_id": episode["id"], "condition": condition, "bytes": len(text.encode())})
                memory = text
            else:
                completed += 1
        return {"writer": MODELS[0], "memory_trajectories": completed,
                "unavailable": unavailable, "episodes": len(history["episodes"])}
    parallel(select(histories, args.ids), form, args.workers)


def retrieval_ranking(api, history, probe, documents, query):
    """Keep the first actual ranking, bound to the exact source/query/vectors.

    Near-equal lexical sums can exchange rank after process restart even when
    their roundoff is tiny. Re-ranking must not change a study's exposure.
    """
    from continuation_core import rank_episodes
    name = "retrieval-v1:" + probe["id"]
    identity = digest({"episodes": history["episodes"], "messages": probe["messages"],
                       "documents": documents, "query": query})
    existing = api.bound(name)
    if existing is not None:
        if existing["input_digest"] != identity:
            raise ValueError("retrieval binding differs from its exact inputs")
        return existing["ranking"]
    fresh = rank_episodes(history, probe, documents, query)
    legacy = []
    for condition in CONDITIONS:
        for model in MODELS:
            path = api.run_dir / "answers" / probe["id"] / condition / (model + ".json")
            if not path.exists():
                continue
            record = read_json(path)
            key = f"reader/v1/{probe['id']}/{condition}/{model}"
            attempts = api.operation_states(key)
            if not attempts or (record["history_id"], record["probe_id"], record["condition"], record["requested_model"]) != (
                    history["id"], probe["id"], condition, model):
                raise ValueError("legacy ranking has no matching answer identity/receipt")
            old = record["ranking"]
            by_id = {r["episode_id"]: r for r in old}
            if len(old) != len(fresh) or set(by_id) != {r["episode_id"] for r in fresh} or not all(
                    math.isclose(by_id[r["episode_id"]][k], r[k], rel_tol=1e-12, abs_tol=1e-12)
                    for r in fresh for k in ("dense", "lexical")):
                raise ValueError("legacy ranking scores differ from exact source embeddings/query")
            legacy.append((min(r["id"] for r in attempts), key, old))
    if legacy:
        first = min(legacy, key=lambda item: item[0])
        if any([(r["episode_id"], r["rrf"]) for r in item[2]] != [(r["episode_id"], r["rrf"]) for r in first[2]] for item in legacy):
            raise ValueError("legacy answers disagree on their original ranking; inspect before recovery")
        ranking, origin = first[2], first[1]
    else:
        ranking, origin = fresh, "first-computation"
    api.bind(name, {"input_digest": identity, "ranking": ranking, "origin": origin})
    return ranking


def read_tasks(args, api):
    from continuation_core import episode_text, reader_payload
    histories, probes, _ = freeze_sources(api, args.split)
    def read(history):
        tasks = [p for p in probes if p["history_id"] == history["id"]]
        texts = [episode_text(e) for e in history["episodes"]] + ["\n".join(m["text"] for m in p["messages"]) for p in tasks]
        vectors = api.embed("index/v1/" + history["id"], texts)
        save_once(api.run_dir / "embeddings" / (history["id"] + ".json"),
                  {"model": "text-embedding-3-small", "dimensions": 1536, "input_digest": digest(texts), "vectors": vectors})
        docs = {e["id"]: v for e, v in zip(history["episodes"], vectors)}
        count, unavailable = 0, 0
        for p_index, probe in enumerate(tasks):
            ranking = retrieval_ranking(api, history, probe, docs, vectors[len(history["episodes"]) + p_index])
            payloads = {}
            for condition in CONDITIONS:
                memory = ""
                if condition in ("summary", "notes"):
                    memory_path = api.run_dir / "memory" / history["id"] / condition / (history["episodes"][-1]["id"] + ".json")
                    if not memory_path.exists():
                        continue
                    memory = read_json(memory_path)["text"]
                payload = reader_payload(history, probe, condition, memory, ranking)
                payloads[condition] = payload
            order = [(condition, model) for condition in CONDITIONS for model in MODELS]
            random.Random("continuation-use-v1:" + probe["id"]).shuffle(order)
            for position, (condition, model) in enumerate(order):
                if condition not in payloads:
                    unavailable += 1
                    continue
                payload = payloads[condition]
                key = f"reader/v1/{probe['id']}/{condition}/{model}"
                try:
                    response = api.response(key, model, payload)
                except DispatchError:
                    attempts = api.operation_states(key)
                    if not attempts or any(row["state"] in ("started", "succeeded") for row in attempts):
                        raise
                    # A settled technical outcome occupies its original position.
                    # Resume may visit other positions, never replace this answer.
                    response, answer = {}, ""
                    state = attempts[-1]["state"]
                else:
                    try:
                        answer = output_text(response)
                        state = "completed"
                    except ValueError:
                        answer, state = "", "incomplete_or_empty"
                save_answer(api.run_dir / "answers" / probe["id"] / condition / (model + ".json"),
                    {"history_id": history["id"], "probe_id": probe["id"], "kind": probe["kind"],
                     "condition": condition, "requested_model": model, "returned_model": response.get("model"),
                     "response_id": response.get("id"), "state": state, "answer": answer,
                     "order_position": position, "order_seed": "continuation-use-v1:" + probe["id"],
                     "exposure": payload["exposure"], "ranking": ranking, "usage": response.get("usage")})
                count += 1
        return {"answer_positions": count, "upstream_memory_unavailable": unavailable}
    parallel(select(histories, args.ids), read, args.workers)


def review_answers(args, api, *, audit=False):
    from continuation_analysis import review_payload, review_schema, decode_review, REVIEW_VERSION
    histories, probes, oracles = freeze_sources(api, args.split)
    hmap = {h["id"]: h for h in histories}
    pmap = {p["id"]: p for p in probes}
    omap = {o["probe_id"]: o for o in oracles}
    selected = {h["id"] for h in select(histories, args.ids)}
    if audit:
        if args.split == "test":
            selected &= {f"T{base + i:02d}" for base in (0, 12, 24, 36) for i in (2, 5, 8, 11)}
        else:
            selected &= {"D01", "D04", "D07", "D10"}
    reviewer = MODELS[0] if audit else MODELS[1]
    directory = "review-audit" if audit else "reviews"
    jobs = []
    for probe in probes:
        if probe["history_id"] in selected:
            for condition in CONDITIONS:
                for model in MODELS:
                    jobs.append({"id": f"{probe['id']}/{condition}/{model}", "probe_id": probe["id"],
                                 "condition": condition, "model": model})
    def review(job):
        probe = pmap[job["probe_id"]]
        history = hmap[probe["history_id"]]
        oracle = omap[probe["id"]]
        path = api.run_dir / "answers" / probe["id"] / job["condition"] / (job["model"] + ".json")
        if not path.exists():
            return {"review": "not_run", "technical_state": "answer_unavailable"}
        record = read_json(path)
        if record["state"] != "completed":
            return {"review": "not_run", "technical_state": record["state"]}
        payload = review_payload(history, probe, oracle, record["answer"])
        api.bind("review-policy:" + REVIEW_VERSION, {"instructions": payload["instructions"], "format": "json_schema/line-selection", "one_answer_per_request": True})
        key = directory + "/" + REVIEW_VERSION + "/" + job["id"]
        prior = api.operation_states(key)
        try:
            response = api.response(key, reviewer, payload, json_schema=review_schema(oracle, record["answer"]))
        except DispatchError:
            if prior and all(row["state"] not in ("started", "succeeded") for row in prior):
                return {"review": "not_run", "technical_state": prior[-1]["state"]}
            raise
        try:
            value = json.loads(output_text(response))
        except ValueError as exc:
            judgment, state = {"response_status": response.get("status"), "validation_error": str(exc)}, "invalid_review_response"
        else:
            try:
                judgment = decode_review(value, oracle, record["answer"], history)
                state = "valid"
            except ValueError as exc:
                judgment, state = {"raw": value, "validation_error": str(exc)}, "invalid_review"
        save_once(api.run_dir / directory / REVIEW_VERSION / probe["id"] / job["condition"] / (job["model"] + ".json"),
                  {"answer_digest": digest(record), "oracle_digest": digest(oracle), "reviewer_model": reviewer,
                   "returned_model": response.get("model"), "response_id": response.get("id"),
                   "state": state, "judgment": judgment})
        return {"review": state}
    parallel(jobs, review, args.workers)


def collect_study(args, api):
    """Compose only this study's fixed stages, sharing per-model dispatch slots."""
    histories, _, _ = freeze_sources(api, args.split)
    def collect(history):
        selected = argparse.Namespace(**{**vars(args), "ids": history["id"], "workers": 1})
        form_memories(selected, api)
        read_tasks(selected, api)
        review_answers(selected, api)
        review_answers(selected, api, audit=True)
        return {"collection_stages_settled": True, "technical_missingness_is_retained": True}
    parallel(select(histories, args.ids), collect, args.workers)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "materials", "material-replace", "material-check", "material-review", "formation", "read", "review", "review-audit", "collect", "report", "status"))
    parser.add_argument("--runtime-config")
    parser.add_argument("--run-dir", help="existing private run directory; offline report only")
    parser.add_argument("--split", choices=("development", "test"), default="development")
    parser.add_argument("--ids", help="comma-separated IDs within the fixed split")
    parser.add_argument("--workers", type=int, default=4, choices=range(1, 9))
    args = parser.parse_args(argv)
    if args.command == "check":
        from continuation_core import validate_bundle
        print(canonical(validate_bundle(*[read_json(MATERIAL / name) for name in ("histories.json", "probes.json", "oracles.json")])))
        return
    if args.command == "report":
        if not args.run_dir or args.runtime_config:
            parser.error("report requires --run-dir and does not accept runtime config")
        from continuation_analysis import write_report
        print(canonical(write_report(source_bundle(args.split), args.run_dir, args.split)), flush=True)
        return
    if args.run_dir:
        parser.error("--run-dir is only for the offline report")
    if not args.runtime_config:
        parser.error("--runtime-config is required for private run operations")
    api = runtime(args)
    if args.command == "materials":
        generate_materials(args, api)
    elif args.command == "material-replace":
        replace_lost_material(args, api)
    elif args.command == "material-check":
        check_materials(args, api)
    elif args.command == "material-review":
        review_materials(args, api)
    elif args.command == "formation":
        form_memories(args, api)
    elif args.command == "read":
        read_tasks(args, api)
    elif args.command == "review":
        review_answers(args, api)
    elif args.command == "review-audit":
        review_answers(args, api, audit=True)
    elif args.command == "collect":
        collect_study(args, api)
    print(canonical(api.status()), flush=True)


if __name__ == "__main__":
    main()
