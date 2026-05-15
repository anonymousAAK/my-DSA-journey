"""tgrep: a tiny from-scratch grep clone.

Features:
- plain literal matching (no regex engine)
- glob wildcards: ``*`` (any chars), ``?`` (one char)
- ``-i`` case-insensitive
- ``-n`` line numbers (default on)
- recursive directory walk
- prefix-sum line-match index for O(1) "matches in line range [lo, hi]" queries.

Run ``python tgrep.py`` for a self-demo against synthetic content.
"""
from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from typing import Iterable


# --- Matchers ----------------------------------------------------------------

def literal_search(haystack: str, needle: str) -> list[int]:
    """Return all start indices of needle in haystack. Naive O(n*m); fine for the spec."""
    if not needle:
        return []
    hits: list[int] = []
    n, m = len(haystack), len(needle)
    i = 0
    while i <= n - m:
        if haystack[i : i + m] == needle:
            hits.append(i)
            i += 1  # overlapping matches like 'aaa' in 'aaaaa' counted naturally
        else:
            i += 1
    return hits


def glob_match(text: str, pattern: str) -> bool:
    """Does `pattern` (with * and ?) match anywhere in `text`?

    Implemented as: anchor-free match. We scan each start position and run an
    iterative '*' / '?' DP from there. For reference simplicity, we use a
    classic two-pointer wildcard match with backtracking on '*'.
    """
    if not pattern:
        return False
    # If pattern has no wildcards, fall back to literal scan.
    if "*" not in pattern and "?" not in pattern:
        return pattern in text

    for start in range(len(text) + 1):
        if _wildcard_match_from(text, start, pattern):
            return True
    return False


def _wildcard_match_from(text: str, start: int, pattern: str) -> bool:
    """Two-pointer wildcard match consuming text starting at `start`. Pattern
    must consume some prefix of text[start:] (not the whole thing — we are
    doing substring-style match)."""
    i, j = start, 0
    star_i = -1
    star_j = -1
    n, m = len(text), len(pattern)
    while i <= n:
        if j < m and pattern[j] == "*":
            star_j = j
            star_i = i
            j += 1
            # '*' matched empty; success when remaining pattern can match empty too
            if j == m:
                return True
        elif j < m and i < n and (pattern[j] == "?" or pattern[j] == text[i]):
            i += 1
            j += 1
        elif j == m:
            return True
        elif star_j != -1 and star_i < n:
            star_i += 1
            i = star_i
            j = star_j + 1
        else:
            return False
    return j == m


# --- Line-match index --------------------------------------------------------

@dataclass
class FileIndex:
    """Per-file index: which lines have matches, and a prefix-sum over them."""

    path: str
    line_matches: list[int]  # 1 if line has >=1 match, else 0
    prefix: list[int]  # prefix[i] = sum(line_matches[:i]); len = len(line_matches)+1

    def matches_in_range(self, lo: int, hi: int) -> int:
        """1-indexed inclusive line range [lo, hi]."""
        lo = max(1, lo)
        hi = min(len(self.line_matches), hi)
        if lo > hi:
            return 0
        return self.prefix[hi] - self.prefix[lo - 1]


def build_index(lines: list[str], pattern: str, use_glob: bool, ignore_case: bool) -> list[int]:
    needle = pattern.lower() if ignore_case else pattern
    flags: list[int] = []
    for line in lines:
        h = line.lower() if ignore_case else line
        if use_glob:
            ok = glob_match(h, needle)
        else:
            ok = len(literal_search(h, needle)) > 0
        flags.append(1 if ok else 0)
    return flags


def prefix_sum(flags: list[int]) -> list[int]:
    out = [0] * (len(flags) + 1)
    for i, v in enumerate(flags):
        out[i + 1] = out[i] + v
    return out


# --- File walking ------------------------------------------------------------

def walk_files(roots: list[str], recursive: bool) -> Iterable[str]:
    for r in roots:
        if os.path.isfile(r):
            yield r
        elif os.path.isdir(r) and recursive:
            for dirpath, _dirs, files in os.walk(r):
                for f in files:
                    yield os.path.join(dirpath, f)
        elif os.path.isdir(r):
            for f in sorted(os.listdir(r)):
                full = os.path.join(r, f)
                if os.path.isfile(full):
                    yield full


def search_file(path: str, pattern: str, *, use_glob: bool, ignore_case: bool) -> FileIndex | None:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return None
    flags = build_index(lines, pattern, use_glob, ignore_case)
    return FileIndex(path=path, line_matches=flags, prefix=prefix_sum(flags))


# --- CLI ---------------------------------------------------------------------

def run(args: argparse.Namespace) -> int:
    use_glob = "*" in args.pattern or "?" in args.pattern
    total = 0
    files_with_hits = 0
    for path in walk_files(args.paths, args.recursive):
        idx = search_file(path, args.pattern, use_glob=use_glob, ignore_case=args.ignore_case)
        if idx is None:
            continue
        hits = idx.prefix[-1]
        if hits == 0:
            continue
        files_with_hits += 1
        total += hits
        # Print matching lines.
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                for lineno, line in enumerate(fh.read().splitlines(), 1):
                    if idx.line_matches[lineno - 1]:
                        prefix = f"{path}:{lineno}:" if args.line_number else f"{path}:"
                        print(f"{prefix}{line}")
        except OSError:
            continue
        if args.stats and idx.line_matches:
            mid = max(1, len(idx.line_matches) // 2)
            print(
                f"  [stats] {path}: {hits} matching lines; "
                f"first half={idx.matches_in_range(1, mid)}, "
                f"second half={idx.matches_in_range(mid + 1, len(idx.line_matches))}",
                file=sys.stderr,
            )
    return 0 if total > 0 else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="tgrep: tiny from-scratch grep clone")
    p.add_argument("pattern")
    p.add_argument("paths", nargs="*", default=["."])
    p.add_argument("-i", "--ignore-case", action="store_true")
    p.add_argument("-r", "--recursive", action="store_true")
    p.add_argument("-n", "--line-number", action="store_true", default=True)
    p.add_argument("--stats", action="store_true", help="print prefix-sum stats per file")
    return p


def main(argv: list[str]) -> int:
    if len(argv) <= 1:
        return _demo()
    parser = build_parser()
    args = parser.parse_args(argv[1:])
    return run(args)


def _demo() -> int:
    import tempfile

    sample = (
        "the quick brown fox\n"
        "jumps over the lazy dog\n"
        "THE QUICK BROWN FOX again\n"
        "nothing to see here\n"
        "another the line\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "sample.txt")
        with open(path, "w") as fh:
            fh.write(sample)

        idx = search_file(path, "the", use_glob=False, ignore_case=False)
        assert idx is not None
        print(f"demo: 'the' (case-sensitive) -> {idx.prefix[-1]} matching lines")
        print(f"  first 3 lines: {idx.matches_in_range(1, 3)} matches")
        print(f"  last 3 lines:  {idx.matches_in_range(3, 5)} matches")

        idx2 = search_file(path, "the", use_glob=False, ignore_case=True)
        assert idx2 is not None
        print(f"demo: 'the' (case-insensitive) -> {idx2.prefix[-1]} matching lines")

        idx3 = search_file(path, "q*ck", use_glob=True, ignore_case=True)
        assert idx3 is not None
        print(f"demo: glob 'q*ck' (-i) -> {idx3.prefix[-1]} matching lines")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
