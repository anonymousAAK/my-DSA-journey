#!/usr/bin/env python3
"""
badge_generator.py — Generate shields.io endpoint-format JSON badges
from a learner's local progress.json.

Reads ``~/.journey/progress.json`` (or a path supplied via ``--input``)
and writes a small set of badge JSON files into ``~/.journey/`` (or the
directory supplied via ``--output-dir``).  Each badge file is a tiny
JSON document in the shape shields.io expects from an endpoint URL::

    {
      "schemaVersion": 1,
      "label": "DSA Journey",
      "message": "Week 18 / 30",
      "color": "blue"
    }

The intended workflow is:

    1. Generate the badge files locally.
    2. Upload them to a public Gist (see ``docs/PUBLIC_BADGES.md``).
    3. Embed in your profile README via
       ``https://img.shields.io/endpoint?url=<raw-gist-url>``.

This script is intentionally stdlib-only — no third-party packages
are required.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path


TOTAL_WEEKS = 30

PROGRESS_DIR_DEFAULT = Path.home() / ".journey"
PROGRESS_FILE_DEFAULT = PROGRESS_DIR_DEFAULT / "progress.json"


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_progress(path: Path) -> dict:
    """Load a progress.json file.  Missing / empty file -> empty shape."""
    if not path.exists():
        return {"weeks": {}, "current_week": 1, "history": []}
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"warning: could not read {path}: {exc}", file=sys.stderr)
        return {"weeks": {}, "current_week": 1, "history": []}
    data.setdefault("weeks", {})
    data.setdefault("current_week", 1)
    data.setdefault("history", [])
    return data


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def compute_summary(progress: dict) -> dict:
    """Compute the headline numbers used by all badge files."""
    weeks = progress.get("weeks", {}) or {}
    current_week = int(progress.get("current_week", 1) or 1)

    attempted_keys = [k for k in weeks.keys() if str(k).isdigit() and weeks[k]]
    weeks_attempted = len(attempted_keys)

    aced = 0
    total_rate = 0.0
    total_skills_passed = 0
    for k in attempted_keys:
        rec = weeks[k] or {}
        rate = float(rec.get("rate", 0) or 0)
        total_rate += rate
        if rate >= 80:
            aced += 1
        total_skills_passed += len(rec.get("passed", []) or [])

    avg_rate = (total_rate / weeks_attempted) if weeks_attempted else 0.0

    streak = compute_streak(progress)

    return {
        "weeks_attempted": weeks_attempted,
        "weeks_aced": aced,
        "current_week": current_week,
        "average_rate": round(avg_rate, 1),
        "total_skills_passed": total_skills_passed,
        "streak_days": streak,
    }


def compute_streak(progress: dict) -> int:
    """Count consecutive days (ending today or yesterday) with any history entry.

    A pragmatic, forgiving definition: if the learner has an entry from today
    or yesterday, we count back day-by-day until a gap appears.
    """
    history = progress.get("history") or []
    if not history:
        return 0

    dates = set()
    for entry in history:
        ts = entry.get("timestamp")
        if not ts:
            continue
        try:
            d = _dt.date.fromisoformat(ts[:10])
        except ValueError:
            continue
        dates.add(d)
    if not dates:
        return 0

    today = _dt.date.today()
    # Start at today if there is an entry today, else yesterday.
    cursor = today if today in dates else today - _dt.timedelta(days=1)
    if cursor not in dates:
        return 0

    streak = 0
    while cursor in dates:
        streak += 1
        cursor -= _dt.timedelta(days=1)
    return streak


# ---------------------------------------------------------------------------
# Badge construction
# ---------------------------------------------------------------------------

def _color_for_rate(rate: float) -> str:
    if rate >= 90:
        return "brightgreen"
    if rate >= 80:
        return "green"
    if rate >= 60:
        return "yellowgreen"
    if rate >= 40:
        return "yellow"
    if rate > 0:
        return "orange"
    return "lightgrey"


def _color_for_progress(done: int, total: int) -> str:
    if total <= 0:
        return "lightgrey"
    pct = 100 * done / total
    return _color_for_rate(pct)


def build_badges(summary: dict) -> dict[str, dict]:
    """Return a mapping of {filename: shields-endpoint-dict}."""
    current = summary["current_week"]
    aced = summary["weeks_aced"]
    skills = summary["total_skills_passed"]
    streak = summary["streak_days"]
    avg = summary["average_rate"]

    badges: dict[str, dict] = {}

    # Headline badge — kept at ``badge.json`` for the simplest gist setup.
    badges["badge.json"] = {
        "schemaVersion": 1,
        "label": "DSA Journey",
        "message": f"Week {current} / {TOTAL_WEEKS}",
        "color": _color_for_progress(current, TOTAL_WEEKS),
    }

    badges["badge_weeks_complete.json"] = {
        "schemaVersion": 1,
        "label": "weeks aced",
        "message": f"{aced} / {TOTAL_WEEKS}",
        "color": _color_for_progress(aced, TOTAL_WEEKS),
    }

    badges["badge_current_week.json"] = {
        "schemaVersion": 1,
        "label": "current week",
        "message": f"Week {current}",
        "color": "blue",
    }

    badges["badge_streak.json"] = {
        "schemaVersion": 1,
        "label": "streak",
        "message": f"{streak} day{'s' if streak != 1 else ''}",
        "color": "blueviolet" if streak >= 7 else ("blue" if streak > 0 else "lightgrey"),
    }

    badges["badge_total_skills.json"] = {
        "schemaVersion": 1,
        "label": "skill checks passed",
        "message": str(skills),
        "color": _color_for_rate(avg) if avg else "lightgrey",
    }

    return badges


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate shields.io endpoint badge JSON from progress.json.",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=PROGRESS_FILE_DEFAULT,
        help=f"Path to progress.json (default: {PROGRESS_FILE_DEFAULT})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROGRESS_DIR_DEFAULT,
        help=f"Directory to write badge files into (default: {PROGRESS_DIR_DEFAULT})",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file output.",
    )
    args = parser.parse_args(argv)

    progress = load_progress(args.input)
    summary = compute_summary(progress)
    badges = build_badges(summary)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    for name, payload in badges.items():
        out_path = args.output_dir / name
        with out_path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
            fh.write("\n")
        if not args.quiet:
            print(f"wrote {out_path}  -> {payload['label']}: {payload['message']}")

    if not args.quiet:
        print()
        print("Summary:")
        print(f"  weeks attempted     : {summary['weeks_attempted']}")
        print(f"  weeks aced (>=80%)  : {summary['weeks_aced']}")
        print(f"  current week        : {summary['current_week']}")
        print(f"  average pass rate   : {summary['average_rate']}%")
        print(f"  total skills passed : {summary['total_skills_passed']}")
        print(f"  current streak      : {summary['streak_days']} day(s)")
        print()
        print("Next: upload these files to a public gist — see docs/PUBLIC_BADGES.md")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
