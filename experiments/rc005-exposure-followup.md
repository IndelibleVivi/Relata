# RC-005 P0: fixed-capture reader follow-up

**Status:** accepted bounded follow-up, 2026-10-23, under the maintainer's new Relata × AMS continuation commission and [ADR-0009](../decisions/ADR-0009-exploratory-research-boundary.md). Preparation, dispatch, semantic review and publication are separate states. This packet does not alter the original 144-position study.

## 中文摘要

固定原研究全部 18 个成功 immediate captures（两世界×三检查点×三次重复），每份比较 legacy、full-native、format-only 三种暴露，共 54 个新 reader 请求。只用原生已返回材料，不重新摄入或检索、不补作者答案；三臂均使用 4096 completion 上限。共用原账本，原研究与本次合计仍不超过 300 chat / 500 embedding dispatch。原回答不可覆盖，行为与语义评审未完成时不报准确率。

## English summary

This extension compares three projections of all 18 successful immediate captures from the original RC-005 study, for 54 new reader requests. It performs no ingestion, search or embedding. All arms use the same 4096 completion cap, existing generation entitlement and original bound dispatch ledger. Original outputs remain immutable. A paired response table is exploratory evidence, not calibrated accuracy or benchmark promotion.

## Fixed selection and treatments

Select exactly the original `immediate` native capture for every world A/B, checkpoint p1/p2/p3 and repeat 1/2/3. Selection uses identifiers and completion/binding, not answer quality or measured field effect. All 18 must pass the [offline audit](rc005-exposure-audit.md); otherwise stop this packet rather than silently replacing or dropping a capture. Delayed/recovered captures remain audit observations and are not extra independent units.

For each capture create three fresh reader requests:

- **legacy:** the original historical projection, with its original information loss;
- **full-native:** each complete returned entry, nested to preserve native fields, types, order, missing/null and source role without treating native role as a Chat message role;
- **format-only:** nested/rearranged historical fields, with no new source information or author labels.

Use the same common context, current question, captured candidate order and requested model alias. No full-history or author-contract supplementation. Attribution is an upstream extractor assertion; timestamps are processing timestamps unless independently justified. Full-native also changes length and layout: this first contrast does not isolate attribution alone. Later field ablations or length controls are separate planned diagnostics, not claimed as executed by these 54 calls.

Generate a random interleaving of all 54 requests before the first dispatch and preserve the exact assignment/order locally. Every call is stateless; do not feed responses into another arm. Two worlds, checkpoints and repeats all belong to one authored family. Do not estimate a population effect from 54 rows or three repeats of a capture.

## Resource and request boundary

Use only the already selected gateway DSF generation route; keep its credentials in the existing private runtime mechanism. No new provider/fallback, recharge, embedding, native child, remote state mutation or source upload. Transmit only approved synthetic source content and native results derived from it; no operator paths, state paths, private map, review contract or account data enters a reader request.

All new arms use temperature=0, top_p=1, stream=false, `max_tokens=4096`, including any reasoning budget. Original 1024-cap answers remain historical observations and are not the matched legacy arm. Record actual returned model label, finish reason, content, usage and latency; alias equality is not frozen weights or deterministic service. Keep empty content, length truncation and technical failure distinct.

At most **54** new chat dispatches, **0** embedding dispatches; no automatic or manual retries in this packet. Share the original durable ledger and the original cumulative limits of 300 chat / 500 embedding dispatches. Preflight complete request bodies at 65,536 UTF8 bytes; a returned prompt_tokens value above 32,768 stops subsequent dispatch. Count every attempt/failure before sending. If the remaining ledger budget cannot cover all 54, stop before beginning; do not start a fresh ledger to reset the limit. Opaque downstream retries remain unknown.

The operator executes the fixed finite prepared list privately using the existing HTTP boundary. No general provider adapter or repository runner is introduced. The [offline preparation CLI](rc005-exposure-audit.md) never dispatches; its recorded original request parameters are explicitly transformed to this packet's 4096 cap in the actual request receipt. A prepared payload is not proof of dispatch.

## Observation, review and stopping

Keep bound input, exact actual body, dispatch identity, response/technical status, actual model, usage, latency and capture/arm mapping in a separate private result directory. Retain the original run and prepared packet byte-for-byte; don't overwrite failed or incomplete attempts. If execution stops, retain all assigned rows and their pending/failed/completed status; no quality-based resampling.

For subsequent calibrated review, primary outcomes are supported source attribution and legitimate current arrangements. Use the [review worksheet](../case-lab/reviews/continuity-review-calibration.md), governing history, anonymous IDs and a private condition map. Record unsupported specifics, specific clarification and guessability separately. Preserve reviewer disagreement; do not compute automatic semantic accuracy, use a model judge as human calibration, or reuse original condition-visible filenames as a blind handoff.

Inspect all paired raw answers locally as unreviewed observations. A difference may reflect information, length, formatting or service variation. No difference in a small sample does not prove equivalence. Restored wrong attribution can worsen behavior. The narrow completion claim is a field-loss audit plus a response-pair dataset for this configuration and family. Public result disclosure, formal case acceptance, human recruitment, other experiments and Tilia implementation retain separate boundaries.
