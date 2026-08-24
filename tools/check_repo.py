#!/usr/bin/env python3
"""Lightweight structural and Markdown-link checks for the Relata repository."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "README.zh-CN.md",
    "START_HERE.md",
    "START_HERE.zh-CN.md",
    "STATUS.md",
    "STATUS.zh-CN.md",
    "CHARTER.md",
    "CHARTER.zh-CN.md",
    "RESEARCH_QUESTIONS.md",
    "RESEARCH_QUESTIONS.zh-CN.md",
    "ASSUMPTION_REGISTER.md",
    "ASSUMPTION_REGISTER.zh-CN.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING.zh-CN.md",
    "docs/terminology.md",
    "docs/terminology.zh-CN.md",
    "docs/language-policy.md",
    "docs/language-policy.zh-CN.md",
    "docs/vision/README.md",
    "docs/vision/relata-target-architecture-draft-0.1.md",
    "docs/reviews/target-architecture-draft-0.1-adversarial-review.md",
    "docs/reviews/research-foundation-integration-review.md",
    "research/README.md",
    "research/claim-boundary-study.md",
    "research/claim-boundary-study.zh-CN.md",
    "research/source-map.md",
    "research/evidence-card-template.md",
    "research/evidence-cards/README.md",
    "community/participation-principles.md",
    "community/participation-principles.zh-CN.md",
    "community/consent-levels.md",
    "community/consent-levels.zh-CN.md",
    "community/contribution-consent-record-template.md",
    "community/contribution-consent-record-template.zh-CN.md",
    "community/founding-circle-invitation.md",
    "community/founding-circle-invitation.zh-CN.md",
    "community/incident-seed-template.md",
    "community/incident-seed-template.zh-CN.md",
    "systems/README.md",
    "systems/README.zh-CN.md",
    "systems/system-card-template.md",
    "systems/system-card-template.zh-CN.md",
    "systems/architecture-pressure-map-template.md",
    "case-lab/README.md",
    "case-lab/README.zh-CN.md",
    "case-lab/case-card-template.md",
    "case-lab/case-card-template.zh-CN.md",
    "case-lab/case-review-checklist.md",
    "case-lab/case-review-checklist.zh-CN.md",
    "case-lab/distinction-atlas.md",
    "case-lab/distinction-atlas.zh-CN.md",
    "case-lab/cases/pilot-001-current-state-without-erasure.md",
    "case-lab/cases/seed-002-ordinary-life-location-continuity.zh-CN.md",
    "case-lab/cases/seed-003-project-authority-handoff.zh-CN.md",
    "case-lab/cases/seed-004-private-greeting-public-template.zh-CN.md",
    "case-lab/reviews/RC-001-e0-calibration-pack.zh-CN.md",
    "experiments/README.md",
    "experiments/pilot-record-template.md",
    "experiments/pilots/pilot-001-manual-evaluation-plan.md",
    "governance/public-private-boundary.md",
    "governance/attribution-and-withdrawal.md",
    "governance/licensing-decision.md",
    "decisions/ADR-0001-research-first-bootstrap.md",
    "decisions/ADR-0001-research-first-bootstrap.zh-CN.md",
    "decisions/ADR-0002-vision-doc-is-non-normative.md",
    "decisions/ADR-0002-vision-doc-is-non-normative.zh-CN.md",
    "decisions/ADR-0003-mixed-domain-memory-ecology.md",
    "decisions/ADR-0003-mixed-domain-memory-ecology.zh-CN.md",
    "decisions/ADR-0004-r0-bilingual-documentation.md",
    "decisions/ADR-0004-r0-bilingual-documentation.zh-CN.md",
    "tools/check_repo.py",
]

BILINGUAL_PAIRS = [
    ("README.md", "README.zh-CN.md"),
    ("START_HERE.md", "START_HERE.zh-CN.md"),
    ("STATUS.md", "STATUS.zh-CN.md"),
    ("CHARTER.md", "CHARTER.zh-CN.md"),
    ("RESEARCH_QUESTIONS.md", "RESEARCH_QUESTIONS.zh-CN.md"),
    ("ASSUMPTION_REGISTER.md", "ASSUMPTION_REGISTER.zh-CN.md"),
    ("CONTRIBUTING.md", "CONTRIBUTING.zh-CN.md"),
    ("docs/terminology.md", "docs/terminology.zh-CN.md"),
    ("docs/language-policy.md", "docs/language-policy.zh-CN.md"),
    ("research/claim-boundary-study.md", "research/claim-boundary-study.zh-CN.md"),
    ("case-lab/README.md", "case-lab/README.zh-CN.md"),
    ("case-lab/case-card-template.md", "case-lab/case-card-template.zh-CN.md"),
    ("case-lab/case-review-checklist.md", "case-lab/case-review-checklist.zh-CN.md"),
    ("case-lab/distinction-atlas.md", "case-lab/distinction-atlas.zh-CN.md"),
    ("systems/README.md", "systems/README.zh-CN.md"),
    ("systems/system-card-template.md", "systems/system-card-template.zh-CN.md"),
    ("community/architecture-clinic-guide.md", "community/architecture-clinic-guide.zh-CN.md"),
    ("community/case-clinic-guide.md", "community/case-clinic-guide.zh-CN.md"),
    ("community/consent-levels.md", "community/consent-levels.zh-CN.md"),
    ("community/contribution-consent-record-template.md", "community/contribution-consent-record-template.zh-CN.md"),
    ("community/founding-circle-invitation.md", "community/founding-circle-invitation.zh-CN.md"),
    ("community/incident-seed-template.md", "community/incident-seed-template.zh-CN.md"),
    ("community/participation-principles.md", "community/participation-principles.zh-CN.md"),
    ("decisions/ADR-0001-research-first-bootstrap.md", "decisions/ADR-0001-research-first-bootstrap.zh-CN.md"),
    ("decisions/ADR-0002-vision-doc-is-non-normative.md", "decisions/ADR-0002-vision-doc-is-non-normative.zh-CN.md"),
    ("decisions/ADR-0003-mixed-domain-memory-ecology.md", "decisions/ADR-0003-mixed-domain-memory-ecology.zh-CN.md"),
    ("decisions/ADR-0004-r0-bilingual-documentation.md", "decisions/ADR-0004-r0-bilingual-documentation.zh-CN.md"),
]

CASE_METADATA_MARKERS = (
    "**Locale:**",
    "**Coverage stratum:**",
    "**Content domains:**",
    "**Use domain:**",
    "**Surfaces:**",
    "**Roles:**",
    "**Projects/scopes:**",
    "**Continuity horizon:**",
    "**Primary operation under test:**",
)

PROHIBITED_DIRECTORY_NAMES = {
    "relata-research-foundation",
    "relata-research-bootstrap",
}

PROHIBITED_TOP_LEVEL_IMPLEMENTATION_DIRS = {
    "api",
    "arena",
    "infra",
    "leaderboard",
    "runner",
    "sdk",
    "services",
}

INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_LINK = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


def fail(message: str) -> None:
    print(f"FAIL: {message}")


def markdown_without_fenced_code(text: str) -> str:
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3]
        if fence is None and marker in {"```", "~~~"}:
            fence = marker
            kept.append("")
            continue
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            kept.append("")
            continue
        kept.append(line)
    return "\n".join(kept)


def link_destination(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        return raw[1 : raw.index(">")]
    return raw.split(maxsplit=1)[0] if raw else ""


def github_anchor(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("`", "").strip().lower()
    text = re.sub(r"[^\w\-\s]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", text)


def anchors_for(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    counts: dict[str, int] = defaultdict(int)
    anchors: set[str] = set()
    for heading in HEADING.findall(markdown_without_fenced_code(text)):
        base = github_anchor(heading)
        if not base:
            continue
        index = counts[base]
        anchors.add(base if index == 0 else f"{base}-{index}")
        counts[base] += 1
    return anchors


def resolve_local_link(source: Path, raw_target: str) -> tuple[Path, str] | None:
    target = link_destination(raw_target)
    if not target or target.startswith("//"):
        return None
    parsed = urlsplit(target)
    if parsed.scheme:
        return None

    decoded_path = unquote(parsed.path)
    fragment = unquote(parsed.fragment)
    if decoded_path.startswith("/"):
        raise ValueError("uses an absolute local path")

    candidate = source if not decoded_path else (source.parent / decoded_path).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError as error:
        raise ValueError("escapes the repository") from error
    return candidate, fragment


def check_markdown_links() -> tuple[list[str], int, int]:
    failures: list[str] = []
    markdown_files = sorted(ROOT.rglob("*.md"))
    anchor_cache: dict[Path, set[str]] = {}
    links_checked = 0

    for source in markdown_files:
        if ".git" in source.parts:
            continue
        text = markdown_without_fenced_code(source.read_text(encoding="utf-8"))
        raw_targets = INLINE_LINK.findall(text) + REFERENCE_LINK.findall(text)
        for raw_target in raw_targets:
            try:
                resolved = resolve_local_link(source, raw_target)
            except ValueError as error:
                failures.append(f"{source.relative_to(ROOT)}: {raw_target!r} {error}")
                continue
            if resolved is None:
                continue

            target, fragment = resolved
            links_checked += 1
            if not target.exists():
                failures.append(
                    f"{source.relative_to(ROOT)}: missing link target {raw_target!r}"
                )
                continue
            if fragment and target.is_file() and target.suffix.lower() == ".md":
                anchors = anchor_cache.setdefault(target, anchors_for(target))
                if fragment not in anchors:
                    failures.append(
                        f"{source.relative_to(ROOT)}: missing anchor #{fragment} in "
                        f"{target.relative_to(ROOT)}"
                    )

    return failures, len(markdown_files), links_checked


def git_paths_changed_from_head() -> set[str]:
    tracked = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return set(tracked) | set(untracked)


def last_commit_for(relative: str) -> str:
    return subprocess.run(
        ["git", "log", "-1", "--format=%H", "--", relative],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def check_bilingual_pairs() -> list[str]:
    failures: list[str] = []
    changed = git_paths_changed_from_head()

    for english_relative, chinese_relative in BILINGUAL_PAIRS:
        english = ROOT / english_relative
        chinese = ROOT / chinese_relative
        if not english.is_file() or not chinese.is_file():
            continue

        english_text = english.read_text(encoding="utf-8")
        chinese_text = chinese.read_text(encoding="utf-8")
        expected_english = (
            f"<!-- language: en; mirror: {chinese.name}; "
            "translation-status: synchronized -->"
        )
        expected_chinese = (
            f"<!-- language: zh-CN; mirror: {english.name}; "
            "translation-status: synchronized -->"
        )
        if expected_english not in english_text:
            failures.append(f"{english_relative}: missing synchronized English mirror declaration")
        if expected_chinese not in chinese_text:
            failures.append(f"{chinese_relative}: missing synchronized Chinese mirror declaration")

        english_links = INLINE_LINK.findall(markdown_without_fenced_code(english_text))
        chinese_links = INLINE_LINK.findall(markdown_without_fenced_code(chinese_text))
        if not any(link_destination(target).split("#", 1)[0] == chinese.name for target in english_links):
            failures.append(f"{english_relative}: missing reciprocal link to {chinese.name}")
        if not any(link_destination(target).split("#", 1)[0] == english.name for target in chinese_links):
            failures.append(f"{chinese_relative}: missing reciprocal link to {english.name}")

        english_changed = english_relative in changed
        chinese_changed = chinese_relative in changed
        if english_changed != chinese_changed:
            failures.append(
                f"translation drift: {english_relative} and {chinese_relative} "
                "must change together"
            )
        elif not english_changed and last_commit_for(english_relative) != last_commit_for(chinese_relative):
            failures.append(
                f"translation drift: {english_relative} and {chinese_relative} "
                "were last synchronized in different commits"
            )

    return failures


def main() -> int:
    failures: list[str] = []

    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            failures.append(f"missing required file: {relative}")

    for path in ROOT.rglob("*"):
        if not path.is_dir() or ".git" in path.parts:
            continue
        if path.name.casefold() in PROHIBITED_DIRECTORY_NAMES:
            failures.append(f"prohibited project shell: {path.relative_to(ROOT)}")

    for name in PROHIBITED_TOP_LEVEL_IMPLEMENTATION_DIRS:
        if (ROOT / name).exists():
            failures.append(f"premature implementation directory: {name}/")

    vision = ROOT / "docs/vision/relata-target-architecture-draft-0.1.md"
    if vision.is_file():
        text = vision.read_text(encoding="utf-8")
        if "Authority: Non-normative north-star provocation" not in text:
            failures.append("vision document lacks the non-normative authority banner")

    register = ROOT / "ASSUMPTION_REGISTER.md"
    if register.is_file():
        text = register.read_text(encoding="utf-8")
        ids = {
            int(value)
            for value in re.findall(r"^\|\s*(\d+)\s*\|", text, flags=re.MULTILINE)
        }
        expected = set(range(1, 23))
        if ids != expected:
            failures.append(
                f"assumption register IDs are {sorted(ids)}; expected 1..22"
            )

    pilot = ROOT / "case-lab/cases/pilot-001-current-state-without-erasure.md"
    if pilot.is_file():
        text = pilot.read_text(encoding="utf-8").lower()
        for marker in (
            "counterfactual twins",
            "current-turn-only",
            "no-memory",
            "reference-context",
            "full-history",
            "scope note",
            "narrow shared-relational",
            "system under study",
        ):
            if marker not in text:
                failures.append(f"Pilot 001 is missing required marker: {marker}")

    for case in sorted((ROOT / "case-lab/cases").glob("*.md")):
        text = case.read_text(encoding="utf-8")
        for marker in CASE_METADATA_MARKERS:
            if marker not in text:
                failures.append(f"{case.relative_to(ROOT)} is missing Case Card metadata: {marker}")

    failures.extend(check_bilingual_pairs())

    stale_terms = {
        "tools/check_bootstrap.py": "stale checker path",
        "participant-native": "stale system terminology",
        "oracle-context": "stale case-baseline terminology",
    }
    for path in ROOT.rglob("*.md"):
        if path == vision or ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for term, description in stale_terms.items():
            if term in text:
                failures.append(
                    f"{path.relative_to(ROOT)} contains {description}: {term}"
                )

    link_failures, markdown_count, link_count = check_markdown_links()
    failures.extend(link_failures)

    if failures:
        for message in failures:
            fail(message)
        print(f"\nRelata repository check completed with {len(failures)} failure(s).")
        return 1

    print("Relata repository check: PASS")
    print(f"Root: {ROOT}")
    print(f"Required files checked: {len(REQUIRED)}")
    print(f"Bilingual pairs checked: {len(BILINGUAL_PAIRS)}")
    print(f"Markdown files checked: {markdown_count}")
    print(f"Internal Markdown links checked: {link_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
