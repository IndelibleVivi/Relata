[简体中文](language-policy.zh-CN.md) | **English**
<!-- language: en; mirror: language-policy.zh-CN.md; translation-status: synchronized -->

# Relata R0 Language Policy

## Working languages

Chinese is Relata's primary working and community-participation language during R0. English remains a complete public entrypoint for international researchers, maintainers, source review, and citation.

Code, schemas, field names, IDs, CLI commands, failure codes, artifact filenames, exact quoted source terms, and `AGENTS.md` remain English. Chinese documents explain those identifiers without inventing translated canonical names.

## Stable paired authority

The following stable surfaces use an English `.md` file and a Simplified Chinese `.zh-CN.md` mirror:

- root README, Start Here, Charter, Status, Research Questions, Assumption Register, and Contributing guide;
- working terminology and this language policy;
- Case Lab README, Case Card template, acceptance checklist, and Distinction Atlas;
- System Census README and System Card template;
- stable community clinic, consent, Incident Seed, participation, invitation, and consent-record materials;
- accepted ADRs created or substantively revised under this policy.

Each pair must:

1. contain a reciprocal language link;
2. declare `language`, `mirror`, and `translation-status` in the machine-readable HTML comment at the top;
3. change together when either member's meaning changes; and
4. use `translation-status: synchronized` only after human review confirms that both express the same current authority.

The repository checker validates these structural and Git-change properties. It cannot validate semantic equivalence.

## Summary-bilingual research artifacts

Evidence Cards, System Cards, accepted ADRs, and actively maintained review documents provide both `中文摘要` and `English summary`. Their full bodies may remain in the language that best preserves source or authoring context. Exact quoted source terms stay unchanged.

## Locale-sensitive cases and Incident Seeds

A case or Incident Seed preserves its original locale. Translation may change tone, private language, code-switching, cue strength, tokenization, implied relationship information, or reviewer interpretation. A cross-language version is therefore a provenance-linked adaptation with its own variant identity, not an automatically equivalent mirror.

Example:

```text
RC-002-zh-CN
RC-002-en-adaptation
```

The adaptation records its source variant, adapter/translator, material language changes, and separate review state.

## Historical and technical exceptions

- Target Architecture Draft 0.1 remains in its original language as a non-normative historical object.
- Code and generated artifacts do not receive translated duplicates merely to satisfy documentation symmetry.
- Exact-source objects remain linked or quoted under their original names and terms.
- Private continuity follows the working language useful to its owners and is outside the public pair contract.

## Drift handling

When a stable pair is out of sync:

- mark the affected pair `translation-status: drifted` rather than claiming synchronization;
- identify which file contains the newer authority and what changed;
- repair both files before accepting a release or public authority change; and
- never describe a structural checker PASS as proof of translation quality.

See [`ADR-0004`](../decisions/ADR-0004-r0-bilingual-documentation.md).
