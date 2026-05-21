#!/usr/bin/env python3
"""Rewrite competitions/LEADERBOARD.md from a list of score records.

Manual workflow for now: edit ``SCORES`` below (or pipe JSON via stdin with
``--stdin``) and run::

    python3 scripts/update_leaderboard.py
    # or
    cat scores.json | python3 scripts/update_leaderboard.py --stdin

Records have the schema::

    {"username": "octocat", "week": "2026-W21", "score": 87}

Scores are integers in 0..100. The script:

1. Groups by username, sums total score, counts distinct weeks competed.
2. Sorts the overall table by total score (desc), tie-breaking by
   weeks-competed (desc) then username (asc).
3. For each week, finds the top-two scorers (winner + runner-up).
4. Writes the result to ``competitions/LEADERBOARD.md``.

Stdlib only.
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Edit this list when running the script manually. Each entry is one
# submission's final score. Leave the list empty to produce an "empty"
# leaderboard (useful when bootstrapping).
# ---------------------------------------------------------------------------
SCORES: list[dict] = [
    # {"username": "octocat", "week": "2026-W21", "score": 92},
    # {"username": "ada",     "week": "2026-W21", "score": 88},
]

REPO_ROOT = Path(__file__).resolve().parent.parent
LEADERBOARD_PATH = REPO_ROOT / "competitions" / "LEADERBOARD.md"


def _validate(records: list[dict]) -> list[dict]:
    """Reject records that don't match the expected schema."""
    cleaned: list[dict] = []
    for i, r in enumerate(records):
        if not isinstance(r, dict):
            raise ValueError(f"record {i} is not an object: {r!r}")
        missing = {"username", "week", "score"} - r.keys()
        if missing:
            raise ValueError(f"record {i} missing keys: {missing}")
        if not isinstance(r["username"], str) or not r["username"]:
            raise ValueError(f"record {i} has invalid username")
        if not isinstance(r["week"], str) or not r["week"]:
            raise ValueError(f"record {i} has invalid week")
        if not isinstance(r["score"], int) or not (0 <= r["score"] <= 100):
            raise ValueError(f"record {i} has invalid score (want int 0..100)")
        cleaned.append(r)
    return cleaned


def _overall_table(records: list[dict]) -> str:
    totals: dict[str, int] = defaultdict(int)
    weeks: dict[str, set] = defaultdict(set)
    for r in records:
        totals[r["username"]] += r["score"]
        weeks[r["username"]].add(r["week"])

    rows = sorted(
        totals.items(),
        key=lambda kv: (-kv[1], -len(weeks[kv[0]]), kv[0]),
    )
    if not rows:
        return (
            "| Rank | Username | Total score | Weeks competed |\n"
            "| --- | --- | --- | --- |\n"
            "| _(no entries yet)_ | | | |\n"
        )
    lines = [
        "| Rank | Username | Total score | Weeks competed |",
        "| --- | --- | --- | --- |",
    ]
    for rank, (user, total) in enumerate(rows, start=1):
        lines.append(f"| {rank} | {user} | {total} | {len(weeks[user])} |")
    return "\n".join(lines) + "\n"


def _per_week_table(records: list[dict]) -> str:
    by_week: dict[str, list[tuple[str, int]]] = defaultdict(list)
    for r in records:
        by_week[r["week"]].append((r["username"], r["score"]))

    if not by_week:
        return (
            "| Week | Winner | Score | Runner-up | Score |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| _(no entries yet)_ | | | | |\n"
        )

    lines = [
        "| Week | Winner | Score | Runner-up | Score |",
        "| --- | --- | --- | --- | --- |",
    ]
    for week in sorted(by_week):
        ranked = sorted(by_week[week], key=lambda us: (-us[1], us[0]))
        winner, w_score = ranked[0]
        if len(ranked) >= 2:
            runner, r_score = ranked[1]
            lines.append(
                f"| {week} | {winner} | {w_score} | {runner} | {r_score} |"
            )
        else:
            lines.append(f"| {week} | {winner} | {w_score} | — | — |")
    return "\n".join(lines) + "\n"


def render(records: list[dict]) -> str:
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC"
    )
    if not records:
        last_updated = "never (no scores recorded yet)"
    else:
        last_updated = timestamp
    return (
        "# Competition Leaderboard\n"
        "\n"
        "Auto-rewritten by `scripts/update_leaderboard.py`. Do not edit by hand —\n"
        "your changes will be overwritten the next time the script runs.\n"
        "\n"
        f"_Last updated: {last_updated}._\n"
        "\n"
        "## Overall standings\n"
        "\n"
        f"{_overall_table(records)}"
        "\n"
        "## Per-week breakdown\n"
        "\n"
        f"{_per_week_table(records)}"
    )


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--stdin",
        action="store_true",
        help="Read a JSON array of records from stdin instead of using the "
        "in-file SCORES list.",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=LEADERBOARD_PATH,
        help="Override the output path (default: competitions/LEADERBOARD.md).",
    )
    args = p.parse_args(argv)

    if args.stdin:
        raw = sys.stdin.read().strip()
        records = json.loads(raw) if raw else []
    else:
        records = list(SCORES)
    records = _validate(records)
    content = render(records)
    args.out.write_text(content, encoding="utf-8")
    print(f"wrote {args.out} ({len(records)} record(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
