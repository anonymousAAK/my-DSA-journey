#!/usr/bin/env python3
"""
quality_check.py — schema and consistency validator for the DSA learning repo.

Catches drift before it lands. Eight checks, stdlib only, exit non-zero on any failure.

Usage:
    python scripts/quality_check.py                  # full check
    python scripts/quality_check.py --check headers  # one check only
    python scripts/quality_check.py --json           # machine-readable output
    python scripts/quality_check.py --quiet          # only print failures, not progress

See scripts/QUALITY_CHECK.md for the philosophy and how to fix common failures.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

# Repo root = parent of this script's directory.
REPO_ROOT = Path(__file__).resolve().parent.parent

# Languages by file extension we care about for header / smart-quote / consistency checks.
CODE_EXTS = {".py", ".cpp", ".rs", ".java", ".html"}

# Numbered-topic filename pattern: starts with "<num>." (e.g., "2.hello_world.py" or
# "13.How Integer is Stored.java"). Rust uses s<NN>_... convention.
NUMBERED_RE = re.compile(r"^\d+[\._]")  # 1.something or 1_something
RUST_NUMBERED_RE = re.compile(r"^s\d{2}_")  # s02_hello_world

# Smart-quote code points: U+2018, U+2019, U+201C, U+201D
SMART_QUOTES = {"‘", "’", "“", "”"}
SMART_QUOTE_RE = re.compile("[" + "".join(SMART_QUOTES) + "]")

# Required header tokens (case-insensitive). Each entry is a list of *acceptable
# alternatives* — at least one must be present. e.g. DRY RUN OR EXAMPLE.
REQUIRED_TOKENS_GROUPS: list[list[str]] = [
    ["CONCEPT"],
    ["KEY POINTS"],
    ["DRY RUN", "EXAMPLE"],
    ["COMPLEXITY"],
    ["NOTES", "NOTE:"],
]

# Per-language header opener patterns. We scan the first ~120 lines.
HEADER_SCAN_LINES = 200

# Fundamentals weeks (1-5) — these contain syntax tutorials where COMPLEXITY
# is genuinely not applicable (e.g. "print hello world", "declare a variable").
TUTORIAL_WEEKS = {1, 2, 3, 4, 5}

# Topic-name fragments identifying tutorial/syntax-demo files for which
# COMPLEXITY analysis does not apply. Match is case-insensitive and substring.
TUTORIAL_TOPIC_PATTERNS = (
    "hello_world", "installation", "data_types", "typecasting", "operators",
    "if_else", "while_loop", "for_loop", "break", "continue",
    "scope_of_variable", "bitwise_operator", "infinite_loop",
    "taking_input", "multiple_input", "integer_and_string",
    "how_integer_is_stored", "how_other_datatype",
    "arithmetic_operation", "increment_decrement",
    "precedence_associativity", "add_two_numbers", "better_hello",
    "find_character_case", "for_loop_variations",
)

# Survey / multi-topic legacy filenames. These files bundle several related
# topics in a single source (e.g. all sorting algorithms in BubbleSelectionInsertion.java).
# They are exempt from the per-topic header schema and from the per-topic
# counterpart check. New per-topic files should NOT be added here — use the
# numbered file convention instead.
SURVEY_TOPIC_STEMS = {
    # Weeks 26-30 cross-cutting surveys
    "network_flow", "geometry", "game_theory", "system_design",
    "interview_patterns", "fundamentals", "arrays", "strings",
    "searching", "sorting", "matrix", "linked_lists", "stacks", "queues",
    "trees", "heaps", "hashing", "graphs", "dp", "greedy", "backtracking",
    "recursion", "control_flow", "string_algorithms",
}

# Path to the known-drift configuration. Files listed there are exempted from
# the header check with a human-readable reason. Format is intentionally
# minimal — one entry per line, "<repo-relative-path>: <reason>".
KNOWN_DRIFT_FILE = ".ci-known-drift.yml"

# Path to the java-skip list (also used by CI for the java compile job).
# Files listed here are pedagogical fragments and are exempt from the header
# check in addition to being skipped by the java compile job.
CI_SKIP_JAVA_FILE = ".ci-skip-java"


def _load_line_set(relpath: str) -> set[str]:
    """Load a simple line-oriented config file: blank lines and `#` comments
    are ignored, otherwise either the bare path before any `:` separator OR
    the entire line is treated as a path. Returns the set of repo-relative
    paths (forward-slash) it lists."""
    p = REPO_ROOT / relpath
    if not p.is_file():
        return set()
    out: set[str] = set()
    for raw in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # `<path>: <reason>` form — take everything before the first colon.
        if ":" in line:
            path = line.split(":", 1)[0].strip()
        else:
            path = line
        if path:
            out.add(path)
    return out


# Lazy-loaded module-level caches.
_SKIP_JAVA_CACHE: set[str] | None = None
_KNOWN_DRIFT_CACHE: set[str] | None = None


def skip_java_paths() -> set[str]:
    global _SKIP_JAVA_CACHE
    if _SKIP_JAVA_CACHE is None:
        _SKIP_JAVA_CACHE = _load_line_set(CI_SKIP_JAVA_FILE)
    return _SKIP_JAVA_CACHE


def known_drift_paths() -> set[str]:
    global _KNOWN_DRIFT_CACHE
    if _KNOWN_DRIFT_CACHE is None:
        _KNOWN_DRIFT_CACHE = _load_line_set(KNOWN_DRIFT_FILE)
    return _KNOWN_DRIFT_CACHE


def is_tutorial_topic(path: Path) -> bool:
    """Return True if this file is a syntax-tutorial / fundamentals demo for
    which COMPLEXITY analysis is genuinely not applicable."""
    # Week-based: weeks 1-5 are fundamentals.
    try:
        wk = int(path.parent.parent.name.split()[1])
        if wk in TUTORIAL_WEEKS:
            return True
    except (ValueError, IndexError):
        pass
    # Topic-name-based: any filename whose normalised stem contains a tutorial keyword.
    stem = path.stem if path.suffix else path.name
    is_rust = path.suffix == ".rs"
    norm = normalize_stem(stem, is_rust=is_rust)
    for kw in TUTORIAL_TOPIC_PATTERNS:
        if kw in norm:
            return True
    return False


def is_survey_file(path: Path) -> bool:
    """Return True if this Java/HTML file is a survey/multi-topic legacy file
    that should be exempt from the per-topic header and counterpart checks."""
    stem = path.stem if path.suffix else path.name
    is_rust = path.suffix == ".rs"
    norm = normalize_stem(stem, is_rust=is_rust)
    return norm in SURVEY_TOPIC_STEMS


# ---------------------------------------------------------------------------
# Issue accumulator
# ---------------------------------------------------------------------------

class Issue:
    __slots__ = ("check", "code", "message", "file", "extra")

    def __init__(self, check: str, code: str, message: str, file: str | None = None, extra: dict | None = None):
        self.check = check
        self.code = code
        self.message = message
        self.file = file
        self.extra = extra or {}

    def render(self) -> str:
        if self.file:
            return f"{self.code} {self.message} file={self.file}"
        return f"{self.code} {self.message}"

    def to_json(self) -> dict:
        return {
            "check": self.check,
            "code": self.code,
            "message": self.message,
            "file": self.file,
            **self.extra,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def week_dirs() -> list[Path]:
    """All `Week N/` directories, sorted numerically."""
    out = []
    for p in REPO_ROOT.iterdir():
        if p.is_dir() and p.name.startswith("Week "):
            try:
                n = int(p.name.split()[1])
            except (ValueError, IndexError):
                continue
            out.append((n, p))
    return [p for _, p in sorted(out)]


def rel(p: Path) -> str:
    """Path relative to repo root, as a forward-slash string."""
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def read_text_safely(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def is_numbered_topic_file(path: Path) -> bool:
    """Return True if this is a per-topic numbered file we should validate."""
    name = path.name
    if path.suffix == ".rs":
        return bool(RUST_NUMBERED_RE.match(name))
    return bool(NUMBERED_RE.match(name))


def normalize_stem(stem: str, *, is_rust: bool = False) -> str:
    """Normalise a filename stem for cross-language equivalence matching.

    Examples:
        "2.Hello_World"           -> "hello_world"
        "2.hello_world"           -> "hello_world"
        "s02_hello_world"         -> "hello_world"
        "14. How other datatype"  -> "how_other_datatype"
        "bipartite_matching"      -> "bipartite_matching"
    """
    s = stem
    if is_rust and s.startswith("s") and len(s) > 3 and s[1:3].isdigit() and s[3] == "_":
        s = s[4:]
    else:
        # Strip leading "N." or "N. " number prefix.
        s = re.sub(r"^\d+\s*\.\s*", "", s)
    # Break CamelCase / PascalCase apart: 'BubbleSelectionInsertion' -> 'Bubble_Selection_Insertion'.
    # Insert an underscore before each capital that follows a lowercase letter or digit,
    # and before a capital that precedes a lowercase letter when preceded by another capital
    # (handles acronyms like 'ZAlgorithm' -> 'Z_Algorithm').
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", s)
    s = re.sub(r"(?<=[A-Z])([A-Z][a-z])", r"_\1", s)
    # Lowercase, replace spaces with underscores, collapse repeats.
    s = s.lower().strip()
    s = re.sub(r"[\s\-]+", "_", s)
    s = re.sub(r"_+", "_", s)
    s = s.strip("_")
    return s


# ---------------------------------------------------------------------------
# CHECK 1 — Code file headers
# ---------------------------------------------------------------------------

def extract_header_text(path: Path, text: str) -> str:
    """Return the header text region (first comment block) we should search for tokens.

    Strategy: take the first HEADER_SCAN_LINES lines as the search window. This
    is permissive: the NOTES block may legitimately appear at the bottom. To
    keep things simple, scan the whole file but cap at HEADER_SCAN_LINES, then
    also append the last 40 lines so trailing NOTES blocks are visible.
    """
    lines = text.splitlines()
    head = "\n".join(lines[:HEADER_SCAN_LINES])
    tail = "\n".join(lines[-40:]) if len(lines) > HEADER_SCAN_LINES else ""
    return head + "\n" + tail


def check_html_header(text: str) -> list[str]:
    """HTML must contain `<!-- WEEK N` (or similar) near the top.

    For survey/multi-topic HTML files that follow a `<head>` -> `<title>` -> `<body>`
    layout (no leading HTML comment), accept a `<title>Week N` element instead —
    that's the equivalent "this file declares its week" signal.
    """
    head = "\n".join(text.splitlines()[:30])
    if re.search(r"<!--[^>]*WEEK\s+\d+", head, flags=re.IGNORECASE):
        return []
    # Also tolerate a `<!--\nWEEK N` on the next line.
    if re.search(r"<!--\s*\n\s*WEEK\s+\d+", head, flags=re.IGNORECASE):
        return []
    # Tolerate `<title>Week N - ...</title>` for survey-style HTML pages.
    if re.search(r"<title>[^<]*WEEK\s+\d+", head, flags=re.IGNORECASE):
        return []
    return ["WEEK N comment header"]


def check_code_header(text: str, *, allow_missing_complexity: bool = False) -> list[str]:
    """Return the list of *missing* token-groups (rendered as the first alternative).

    If `allow_missing_complexity` is True (e.g. for syntax-tutorial files in
    fundamentals weeks), the COMPLEXITY group is not required.
    """
    scan = extract_header_text(Path("."), text)  # path unused
    upper = scan.upper()
    missing: list[str] = []
    for group in REQUIRED_TOKENS_GROUPS:
        if allow_missing_complexity and group == ["COMPLEXITY"]:
            continue
        if not any(tok.upper() in upper for tok in group):
            missing.append(group[0])
    return missing


def run_check_headers() -> tuple[int, list[Issue]]:
    issues: list[Issue] = []
    file_count = 0
    skip_java = skip_java_paths()
    drift = known_drift_paths()
    for wk in week_dirs():
        for lang_dir, ext in [("python", ".py"), ("cpp", ".cpp"), ("rust", ".rs"),
                              ("java", ".java"), ("web", ".html")]:
            d = wk / lang_dir
            if not d.is_dir():
                continue
            for f in sorted(d.iterdir()):
                if not f.is_file():
                    continue
                if f.suffix != ext:
                    continue
                if ext != ".html" and not is_numbered_topic_file(f):
                    # only numbered topic files are required to have headers
                    continue
                if ext == ".html" and not is_numbered_topic_file(f):
                    continue
                relpath = rel(f)
                # Pedagogical Java fragments (also skipped by the java compile
                # job) — these are intentionally not standalone programs and
                # not required to carry the per-topic header schema.
                if ext == ".java" and relpath in skip_java:
                    continue
                # Survey / multi-topic files (e.g. Week N java/web "bundle"
                # files in advanced weeks) use a different header schema and
                # are exempted via .ci-known-drift.yml.
                if relpath in drift:
                    continue
                file_count += 1
                text = read_text_safely(f)
                if text is None:
                    issues.append(Issue("headers", "HEADER_UNREADABLE",
                                        "tokens=[?]", relpath))
                    continue
                if ext == ".html":
                    missing = check_html_header(text)
                else:
                    allow_no_complexity = is_tutorial_topic(f)
                    missing = check_code_header(
                        text, allow_missing_complexity=allow_no_complexity)
                if missing:
                    tokens = ", ".join(missing)
                    issues.append(Issue(
                        "headers", "HEADER_MISSING",
                        f"tokens=[{tokens}]", relpath,
                        extra={"missing": missing},
                    ))
    return file_count, issues


# ---------------------------------------------------------------------------
# CHECK 2 — Patterns.md schema
# ---------------------------------------------------------------------------

DRILL_HEADER_RE = re.compile(r"^###\s+\d+\.\s", flags=re.MULTILINE)
PATTERN_LINE_RE = re.compile(r"^\s*(?:-\s*|\*\s*|\d+\.\s*)?\*?\*?Pattern\*?\*?\s*[:\-]", flags=re.MULTILINE | re.IGNORECASE)
WHY_LINE_RE = re.compile(r"^\s*(?:-\s*|\*\s*|\d+\.\s*)?\*?\*?Why\*?\*?\s*[:\-]", flags=re.MULTILINE | re.IGNORECASE)


def run_check_patterns() -> tuple[int, list[Issue]]:
    issues: list[Issue] = []
    total = 0
    passed = 0
    for wk in week_dirs():
        f = wk / "patterns.md"
        if not f.is_file():
            issues.append(Issue("patterns", "PATTERNS_MISSING", "no patterns.md", rel(f)))
            continue
        total += 1
        text = read_text_safely(f) or ""
        drill_headers = DRILL_HEADER_RE.findall(text)
        local: list[str] = []
        if len(drill_headers) < 10:
            local.append(f"only {len(drill_headers)} numbered drills (need >=10)")
        if "## Answer Key" not in text and "<details>" not in text:
            local.append("missing Answer Key / <details> block")
        pat_count = len(PATTERN_LINE_RE.findall(text))
        why_count = len(WHY_LINE_RE.findall(text))
        if pat_count < 10:
            local.append(f"only {pat_count} Pattern: lines (need >=10)")
        if why_count < 10:
            local.append(f"only {why_count} Why: lines (need >=10)")
        if local:
            issues.append(Issue("patterns", "PATTERNS_SCHEMA",
                                "; ".join(local), rel(f)))
        else:
            passed += 1
    return total, issues


# ---------------------------------------------------------------------------
# CHECK 3 — Challenges.md schema
# ---------------------------------------------------------------------------

CHALLENGE_HEADER_RE = re.compile(r"^##\s+Challenge\s+\d+\s*[:\-]", flags=re.MULTILINE | re.IGNORECASE)


def run_check_challenges() -> tuple[int, list[Issue]]:
    issues: list[Issue] = []
    total = 0
    for wk in week_dirs():
        f = wk / "challenges.md"
        if not f.is_file():
            issues.append(Issue("challenges", "CHALLENGES_MISSING", "no challenges.md", rel(f)))
            continue
        total += 1
        text = read_text_safely(f) or ""
        # Split into per-challenge sections to validate each separately.
        positions = [m.start() for m in CHALLENGE_HEADER_RE.finditer(text)]
        if len(positions) < 3:
            issues.append(Issue("challenges", "CHALLENGES_SCHEMA",
                                f"only {len(positions)} Challenge headers (need >=3)",
                                rel(f)))
            continue
        # Slice sections.
        sections = []
        for i, start in enumerate(positions):
            end = positions[i + 1] if i + 1 < len(positions) else len(text)
            sections.append(text[start:end])
        for i, sec in enumerate(sections, 1):
            missing = []
            if "**Spec**" not in sec and "**Spec:**" not in sec:
                missing.append("**Spec**")
            if "**Constraints**" not in sec and "**Constraints:**" not in sec:
                missing.append("**Constraints**")
            if "**Test inputs**" not in sec and "**Test Inputs**" not in sec and "**Test inputs:**" not in sec:
                missing.append("**Test inputs**")
            # Test-input table: a markdown table with a header row (containing
            # at least two `|`-separated columns), a separator row (`|---|---|`)
            # and at least one data row beneath. We just verify the section
            # contains such a triple after `**Test inputs**`.
            has_table = False
            sec_after_test = sec
            ti_idx = sec.lower().find("**test inputs")
            if ti_idx >= 0:
                sec_after_test = sec[ti_idx:]
            lines = [ln.strip() for ln in sec_after_test.splitlines()]
            for i in range(len(lines) - 2):
                a, b, c = lines[i], lines[i + 1], lines[i + 2]
                if (a.startswith("|") and a.count("|") >= 2
                        and b.startswith("|") and set(b.replace("|", "").strip()) <= set("-: ")
                        and c.startswith("|") and c.count("|") >= 2):
                    has_table = True
                    break
            if not has_table:
                missing.append("test-input table row")
            if missing:
                issues.append(Issue("challenges", "CHALLENGES_SCHEMA",
                                    f"Challenge {i} missing: {', '.join(missing)}",
                                    rel(f),
                                    extra={"challenge_index": i, "missing": missing}))
    return total, issues


# ---------------------------------------------------------------------------
# CHECK 4 — Per-week README sections
# ---------------------------------------------------------------------------

README_REQUIRED = [
    "## Tradeoff Matrix",
    "## Anti-patterns to avoid",
    "## Reflection prompts",
]


def run_check_readmes() -> tuple[int, list[Issue]]:
    issues: list[Issue] = []
    total = 0
    for wk in week_dirs():
        f = wk / "README.md"
        if not f.is_file():
            issues.append(Issue("readme", "README_MISSING", "no README.md", rel(f)))
            continue
        total += 1
        text = read_text_safely(f) or ""
        missing = [h for h in README_REQUIRED if h not in text]
        # Topic-index table: a markdown table whose header row includes the
        # language column names. We look for a header row containing at least
        # three of {Java, Python, C++, Rust, Web}.
        has_topic_table = False
        for line in text.splitlines():
            ls = line.strip()
            if ls.startswith("|"):
                lower = ls.lower()
                hits = sum(1 for lang in ("java", "python", "c++", "cpp", "rust", "web")
                           if lang in lower)
                if hits >= 3:
                    has_topic_table = True
                    break
        if not has_topic_table:
            missing.append("topic-index table (cols for each language)")
        if missing:
            issues.append(Issue("readme", "README_SECTIONS",
                                f"missing: {', '.join(missing)}",
                                rel(f),
                                extra={"missing": missing}))
    return total, issues


# ---------------------------------------------------------------------------
# CHECK 5 — Cross-file consistency
# ---------------------------------------------------------------------------

EXPECTED_EXT_BY_LANG = {
    "java": {".java"},
    "python": {".py"},
    "cpp": {".cpp", ".h", ".hpp"},
    "rust": {".rs"},
    "web": {".html"},
}


def index_lang_dir(d: Path, is_rust: bool) -> dict[str, str]:
    """Map normalised stem -> original filename (rel path)."""
    out: dict[str, str] = {}
    if not d.is_dir():
        return out
    lang = d.name
    expected_exts = EXPECTED_EXT_BY_LANG.get(lang, set())
    for f in d.iterdir():
        if not f.is_file():
            continue
        # Skip files without the expected extension for this language directory.
        # (e.g. extension-less '1.Java Installation' is a tutorial stub, not a
        # source file; doesn't have cross-language counterparts.)
        if expected_exts and f.suffix not in expected_exts:
            continue
        stem = f.stem if f.suffix else f.name
        # For numbered files only (skip survey companions like fundamentals.py /
        # index.html). We DO consider every file in weeks 26-30 (no numeric
        # prefix), and all top-level numbered files in weeks 1-25.
        try:
            week_num = int(d.parent.name.split()[1])
        except (ValueError, IndexError):
            week_num = 0
        if week_num <= 25:
            if is_rust:
                if not RUST_NUMBERED_RE.match(f.name):
                    continue
            else:
                if not NUMBERED_RE.match(f.name):
                    continue
        else:
            # weeks 26-30: skip index.html / fundamentals.* survey companions
            if stem.lower() in {"index", "fundamentals"}:
                continue
        norm = normalize_stem(stem, is_rust=is_rust)
        if norm:
            out[norm] = rel(f)
    return out


def run_check_consistency() -> tuple[int, list[Issue]]:
    issues: list[Issue] = []
    missing_count = 0
    skip_java = skip_java_paths()
    drift = known_drift_paths()
    for wk in week_dirs():
        java_dir = wk / "java"
        if not java_dir.is_dir():
            continue
        java_map = index_lang_dir(java_dir, is_rust=False)
        py_map = index_lang_dir(wk / "python", is_rust=False)
        cpp_map = index_lang_dir(wk / "cpp", is_rust=False)
        rs_map = index_lang_dir(wk / "rust", is_rust=True)
        web_map = index_lang_dir(wk / "web", is_rust=False)
        for norm, jpath in java_map.items():
            # Survey / cross-cutting overview files (e.g. fundamentals.java,
            # network_flow.java) don't have a 1:1 per-topic counterpart by
            # design — they are weekly overviews, not per-topic implementations.
            if norm in SURVEY_TOPIC_STEMS:
                continue
            # Pedagogical fragments (skipped by the java compile job) are not
            # standalone programs and don't have cross-language counterparts.
            if jpath in skip_java or jpath in drift:
                continue
            for lang, m in [("python", py_map), ("cpp", cpp_map),
                            ("rust", rs_map), ("web", web_map)]:
                if norm not in m:
                    missing_count += 1
                    issues.append(Issue(
                        "consistency", "COUNTERPART_MISSING",
                        f"java topic '{norm}' has no {lang} counterpart",
                        jpath,
                        extra={"missing_lang": lang, "stem": norm},
                    ))
    return missing_count, issues


# ---------------------------------------------------------------------------
# CHECK 6 — LeetCode link health
# ---------------------------------------------------------------------------

LEETCODE_URL_RE = re.compile(r"https?://leetcode\.com/problems/([^\s\)\]\>\}\"'`]+)")
VALID_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*/?$")


def run_check_leetcode() -> tuple[int, list[Issue]]:
    issues: list[Issue] = []
    total = 0
    for wk in week_dirs():
        f = wk / "problems.md"
        if not f.is_file():
            continue
        text = read_text_safely(f) or ""
        for m in LEETCODE_URL_RE.finditer(text):
            total += 1
            slug = m.group(1)
            # Strip any trailing punctuation that markdown commonly attaches.
            slug_clean = slug.rstrip(".,;:")
            problems: list[str] = []
            if slug != slug_clean:
                problems.append("trailing punctuation")
            if "//" in slug_clean:
                problems.append("double slash")
            if slug_clean.strip() != slug_clean:
                problems.append("whitespace")
            # Allow optional trailing slash.
            candidate = slug_clean[:-1] if slug_clean.endswith("/") else slug_clean
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", candidate):
                problems.append("malformed slug (must be lowercase hyphenated)")
            if problems:
                issues.append(Issue(
                    "leetcode", "LEETCODE_MALFORMED",
                    f"url=https://leetcode.com/problems/{slug} reasons=[{', '.join(problems)}]",
                    rel(f),
                    extra={"slug": slug, "reasons": problems},
                ))
    return total, issues


# ---------------------------------------------------------------------------
# CHECK 7 — Smart-quote detection
# ---------------------------------------------------------------------------

def run_check_smart_quotes() -> tuple[int, list[Issue]]:
    issues: list[Issue] = []
    scanned = 0
    target_exts = {".java", ".py", ".cpp", ".rs"}
    for wk in week_dirs():
        for sub in ("java", "python", "cpp", "rust"):
            d = wk / sub
            if not d.is_dir():
                continue
            for f in d.iterdir():
                if not f.is_file():
                    continue
                if f.suffix not in target_exts:
                    continue
                scanned += 1
                text = read_text_safely(f)
                if not text:
                    continue
                hits = []
                for lineno, line in enumerate(text.splitlines(), 1):
                    if SMART_QUOTE_RE.search(line):
                        chars = sorted({c for c in line if c in SMART_QUOTES})
                        hits.append((lineno, "".join(chars)))
                if hits:
                    sample = ", ".join(f"L{ln}:{c}" for ln, c in hits[:3])
                    issues.append(Issue(
                        "smart_quotes", "SMART_QUOTE",
                        f"chars=[{sample}] count={len(hits)}",
                        rel(f),
                        extra={"hits": [{"line": ln, "chars": c} for ln, c in hits]},
                    ))
    return scanned, issues


# ---------------------------------------------------------------------------
# CHECK 8 — Required top-level docs
# ---------------------------------------------------------------------------

REQUIRED_DOCS = [
    "PROBLEM_SOLVING.md",
    "LICENSE",
    "README.md",
    "docs/SOLUTION_JOURNAL.md",
    "docs/estimation.md",
    "docs/REVIEW_SCHEDULE.md",
    ".github/workflows/build.yml",
    "scripts/build_all.sh",
]


def run_check_required_docs() -> tuple[int, list[Issue]]:
    issues: list[Issue] = []
    for relpath in REQUIRED_DOCS:
        p = REPO_ROOT / relpath
        if not p.is_file():
            issues.append(Issue("docs", "DOC_MISSING",
                                f"required file not found", relpath))
    return len(REQUIRED_DOCS), issues


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

CHECKS = [
    ("headers", "HEADER CHECK", run_check_headers, "files checked"),
    ("patterns", "PATTERNS SCHEMA", run_check_patterns, "patterns.md checked"),
    ("challenges", "CHALLENGES SCHEMA", run_check_challenges, "challenges.md checked"),
    ("readme", "PER-WEEK README SECTIONS", run_check_readmes, "READMEs checked"),
    ("consistency", "CROSS-FILE CONSISTENCY", run_check_consistency, "missing counterparts"),
    ("leetcode", "LEETCODE LINK HEALTH", run_check_leetcode, "URLs scanned"),
    ("smart_quotes", "SMART-QUOTE DETECTION", run_check_smart_quotes, "files scanned"),
    ("docs", "REQUIRED TOP-LEVEL DOCS", run_check_required_docs, "required docs"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="DSA repo quality checker")
    parser.add_argument("--check", choices=[c[0] for c in CHECKS],
                        help="run only one check")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--quiet", action="store_true",
                        help="only print failures, not progress")
    args = parser.parse_args()

    selected = [c for c in CHECKS if (args.check is None or c[0] == args.check)]
    all_issues: list[Issue] = []
    per_check_summary: list[dict] = []

    total_n = len(selected)
    for idx, (key, title, fn, unit) in enumerate(selected, 1):
        count, issues = fn()
        all_issues.extend(issues)
        summary = {
            "check": key,
            "title": title,
            "count": count,
            "unit": unit,
            "issues": len(issues),
        }
        per_check_summary.append(summary)
        if not args.json and not args.quiet:
            if key == "consistency":
                status = f"{count} missing counterparts"
            elif key == "smart_quotes":
                status = (f"{count} {unit}, clean" if not issues
                          else f"{count} {unit}, {len(issues)} files with smart quotes")
            elif key == "docs":
                status = ("all present" if not issues
                          else f"{len(issues)} missing")
            elif key in ("patterns", "challenges", "readme"):
                passed = count - len(issues)
                status = f"{passed}/{count} pass"
            else:
                status = f"{count} {unit}, {len(issues)} issues"
            print(f"[{idx}/{total_n}] {title} ... {status}")

    if args.json:
        payload = {
            "summary": per_check_summary,
            "total_issues": len(all_issues),
            "issues": [i.to_json() for i in all_issues],
        }
        print(json.dumps(payload, indent=2))
        return 1 if all_issues else 0

    if all_issues:
        if not args.quiet:
            print()
            print(f"{len(all_issues)} issues found.")
            print()
            print("--- issues ---")
        for i in all_issues:
            print(i.render())
    else:
        if not args.quiet:
            print()
            print("0 issues found. All checks clean.")

    return 1 if all_issues else 0


if __name__ == "__main__":
    sys.exit(main())
