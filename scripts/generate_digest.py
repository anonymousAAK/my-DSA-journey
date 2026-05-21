#!/usr/bin/env python3
"""generate_digest.py — weekly digest builder.

Picks one case study, one pattern drill (from a random week's patterns.md),
and one hard-mode challenge (from a random week's challenges.md). The
selections are deterministic on the ISO week number, so two runs in the
same calendar week always produce identical output.

Outputs:
  - WEEKLY.md   (overwritten)
  - feed.xml    (RSS 2.0; latest item prepended, history capped at 52)

Stdlib only.
"""

from __future__ import annotations

import datetime as _dt
import html
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom

REPO_ROOT = Path(__file__).resolve().parent.parent
CASE_STUDIES_DIR = REPO_ROOT / "case_studies" / "real_world"
WEEKLY_PATH = REPO_ROOT / "WEEKLY.md"
FEED_PATH = REPO_ROOT / "feed.xml"
FEED_TITLE = "My DSA Journey — Weekly Digest"
FEED_LINK = "https://github.com/anonymousAAK/my-DSA-journey"
FEED_DESCRIPTION = (
    "Weekly rotation of one real-world case study, one pattern drill, "
    "and one hard-mode challenge from the 30-week DSA Journey."
)
MAX_FEED_ITEMS = 52


# ---------------------------------------------------------------------------
# Discovery helpers
# ---------------------------------------------------------------------------

def list_case_studies() -> list[Path]:
    if not CASE_STUDIES_DIR.exists():
        return []
    return sorted(CASE_STUDIES_DIR.glob("*.md"))


def list_week_files(filename: str) -> list[Path]:
    """Return Week N/<filename> for every week, in week-number order."""
    items: list[tuple[int, Path]] = []
    for entry in REPO_ROOT.iterdir():
        if not entry.is_dir():
            continue
        m = re.match(r"^Week (\d+)$", entry.name)
        if not m:
            continue
        target = entry / filename
        if target.exists():
            items.append((int(m.group(1)), target))
    items.sort()
    return [p for _, p in items]


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def parse_case_study(path: Path) -> dict:
    """Return {title, summary, path}. Summary = first non-empty paragraph
    after the first heading."""
    lines = path.read_text(encoding="utf-8").splitlines()
    title = path.stem.replace("_", " ")
    for ln in lines:
        if ln.startswith("# "):
            title = ln[2:].strip()
            break
    # First paragraph after first heading
    summary_lines: list[str] = []
    started = False
    for ln in lines[1:]:
        s = ln.strip()
        if not started and not s:
            continue
        if s.startswith("#"):
            if summary_lines:
                break
            continue
        if not s:
            if summary_lines:
                break
            continue
        started = True
        summary_lines.append(s)
        if len(" ".join(summary_lines)) > 400:
            break
    summary = " ".join(summary_lines).strip()
    return {"title": title, "summary": summary, "path": path}


_DRILL_RE = re.compile(r"^###\s+(\d+)\.\s+(.*)$")


def parse_drills(path: Path) -> list[dict]:
    """Each drill: `### N. <prose>` followed by Pattern/Why lines."""
    drills: list[dict] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    # Stop reading drills once we hit the "## Answer Key" section.
    end_idx = len(lines)
    for idx, ln in enumerate(lines):
        if ln.strip().lower().startswith("## answer key"):
            end_idx = idx
            break
    while i < end_idx:
        m = _DRILL_RE.match(lines[i])
        if m:
            n = int(m.group(1))
            prose = m.group(2).strip()
            drills.append({"n": n, "prose": prose})
        i += 1
    return drills


_CHALLENGE_RE = re.compile(r"^##\s+Challenge\s+(\d+):\s*(.*)$", re.IGNORECASE)


def parse_challenges(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    challenges: list[dict] = []
    current: dict | None = None
    body: list[str] = []
    for ln in lines:
        m = _CHALLENGE_RE.match(ln)
        if m:
            if current is not None:
                current["body"] = "\n".join(body).strip()
                challenges.append(current)
            current = {"n": int(m.group(1)), "title": m.group(2).strip()}
            body = []
        elif current is not None:
            body.append(ln)
    if current is not None:
        current["body"] = "\n".join(body).strip()
        challenges.append(current)
    return challenges


# ---------------------------------------------------------------------------
# Selection logic
# ---------------------------------------------------------------------------

def iso_week_index(today: _dt.date | None = None) -> int:
    """Return a monotonic integer combining ISO year and week, so two runs
    in the same calendar week produce the same value. We hash to a stable
    non-negative integer."""
    if today is None:
        today = _dt.date.today()
    iso_year, iso_week, _ = today.isocalendar()
    return iso_year * 100 + iso_week


def pick_case_study(items: list[Path], idx: int) -> dict | None:
    if not items:
        return None
    chosen = items[idx % len(items)]
    return parse_case_study(chosen)


def pick_pattern_drill(patterns_files: list[Path], idx: int) -> dict | None:
    if not patterns_files:
        return None
    path = patterns_files[idx % len(patterns_files)]
    drills = parse_drills(path)
    if not drills:
        return None
    drill = drills[idx % len(drills)]
    week = _week_num_of(path)
    return {
        "week": week,
        "n": drill["n"],
        "prose": drill["prose"],
        "path": path,
    }


def pick_challenge(challenges_files: list[Path], idx: int) -> dict | None:
    if not challenges_files:
        return None
    path = challenges_files[idx % len(challenges_files)]
    challenges = parse_challenges(path)
    if not challenges:
        return None
    ch = challenges[idx % len(challenges)]
    week = _week_num_of(path)
    return {
        "week": week,
        "n": ch["n"],
        "title": ch["title"],
        "body": ch["body"],
        "path": path,
    }


def _week_num_of(path: Path) -> int:
    m = re.match(r"^Week (\d+)$", path.parent.name)
    return int(m.group(1)) if m else 0


# ---------------------------------------------------------------------------
# Markdown / RSS rendering
# ---------------------------------------------------------------------------

def _rel(p: Path) -> str:
    try:
        return str(p.relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


def _truncate(s: str, limit: int = 600) -> str:
    s = s.strip()
    if len(s) <= limit:
        return s
    cut = s[:limit].rsplit(" ", 1)[0]
    return cut + "..."


def render_markdown(case_study: dict, drill: dict, challenge: dict, today: _dt.date,
                    iso_year: int, iso_week: int) -> str:
    parts: list[str] = []
    parts.append(f"# Weekly Digest — {today.isoformat()} (ISO {iso_year}-W{iso_week:02d})")
    parts.append("")
    parts.append(
        "One case study, one pattern drill, one challenge. Rotated weekly. "
        "Read these in any order; the goal is one bite-sized prompt per week "
        "to keep recognition warm even when you can't sit down for a full session."
    )
    parts.append("")

    parts.append("## Case study")
    if case_study:
        parts.append(f"**{case_study['title']}**")
        parts.append("")
        parts.append(_truncate(case_study["summary"], 700))
        parts.append("")
        parts.append(f"Read it in full: [`{_rel(case_study['path'])}`]({_rel(case_study['path'])})")
    else:
        parts.append("_No case studies found in `case_studies/real_world/`._")
    parts.append("")

    parts.append("## Pattern drill")
    if drill:
        parts.append(f"_From Week {drill['week']} (drill #{drill['n']})._")
        parts.append("")
        parts.append(f"> {drill['prose']}")
        parts.append("")
        parts.append(
            "Name the pattern in one word and justify in one sentence. Do **not** "
            "look at the answer key until you've written your guess down."
        )
        parts.append("")
        parts.append(f"Drill source: [`{_rel(drill['path'])}`]({_rel(drill['path'])})")
    else:
        parts.append("_No drills available._")
    parts.append("")

    parts.append("## Hard-mode challenge")
    if challenge:
        parts.append(f"### Challenge {challenge['n']} (Week {challenge['week']}): {challenge['title']}")
        parts.append("")
        # Take the first ~600 chars of the body
        body = challenge.get("body", "")
        snippet = _truncate(body.split("---")[0], 800)
        parts.append(snippet)
        parts.append("")
        parts.append(f"Full spec: [`{_rel(challenge['path'])}`]({_rel(challenge['path'])})")
    else:
        parts.append("_No challenges available._")
    parts.append("")

    parts.append("---")
    parts.append("")
    parts.append(
        "Subscribe via RSS: point your reader at "
        "`https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. "
        "See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details."
    )
    return "\n".join(parts) + "\n"


def build_item_description(case_study: dict, drill: dict, challenge: dict) -> str:
    """Plain-text-ish description for the RSS item (will be escaped)."""
    parts = []
    if case_study:
        parts.append(f"Case study: {case_study['title']}")
    if drill:
        parts.append(f"Pattern drill (Week {drill['week']}, #{drill['n']}): {drill['prose']}")
    if challenge:
        parts.append(
            f"Challenge {challenge['n']} (Week {challenge['week']}): {challenge['title']}"
        )
    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# RSS handling
# ---------------------------------------------------------------------------

RFC822 = "%a, %d %b %Y %H:%M:%S +0000"


def _rfc822(dt: _dt.datetime) -> str:
    return dt.strftime(RFC822)


def _read_existing_items() -> list[dict]:
    """Return existing <item> blocks from feed.xml as dicts."""
    if not FEED_PATH.exists():
        return []
    try:
        tree = ET.parse(FEED_PATH)
    except ET.ParseError:
        return []
    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        return []
    items: list[dict] = []
    for it in channel.findall("item"):
        items.append({
            "title": (it.findtext("title") or "").strip(),
            "link": (it.findtext("link") or "").strip(),
            "description": (it.findtext("description") or "").strip(),
            "pubDate": (it.findtext("pubDate") or "").strip(),
            "guid": (it.findtext("guid") or "").strip(),
        })
    return items


def _build_feed_xml(items: list[dict]) -> str:
    rss = ET.Element("rss", attrib={"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = FEED_TITLE
    ET.SubElement(channel, "link").text = FEED_LINK
    ET.SubElement(channel, "description").text = FEED_DESCRIPTION
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = _rfc822(
        _dt.datetime.now(_dt.timezone.utc)
    )
    for it in items[:MAX_FEED_ITEMS]:
        i = ET.SubElement(channel, "item")
        ET.SubElement(i, "title").text = it["title"]
        ET.SubElement(i, "link").text = it.get("link") or FEED_LINK
        ET.SubElement(i, "description").text = it["description"]
        ET.SubElement(i, "pubDate").text = it["pubDate"]
        guid = ET.SubElement(i, "guid", attrib={"isPermaLink": "false"})
        guid.text = it.get("guid") or it["title"]
    raw = ET.tostring(rss, encoding="utf-8", xml_declaration=True)
    pretty = minidom.parseString(raw).toprettyxml(indent="  ", encoding="utf-8")
    # Drop blank lines minidom inserts
    return "\n".join(
        line for line in pretty.decode("utf-8").splitlines() if line.strip()
    ) + "\n"


def update_feed(case_study: dict, drill: dict, challenge: dict,
                today: _dt.date, iso_year: int, iso_week: int) -> None:
    existing = _read_existing_items()
    guid = f"weekly-{iso_year}-W{iso_week:02d}"
    # Skip duplicate by guid
    existing = [it for it in existing if it.get("guid") != guid]
    title = f"Weekly Digest {iso_year}-W{iso_week:02d}"
    description = build_item_description(case_study, drill, challenge)
    pub = _rfc822(_dt.datetime(today.year, today.month, today.day, 9, 0, 0,
                               tzinfo=_dt.timezone.utc))
    new_item = {
        "title": title,
        "link": f"{FEED_LINK}/blob/main/WEEKLY.md",
        "description": description,
        "pubDate": pub,
        "guid": guid,
    }
    items = [new_item] + existing
    FEED_PATH.write_text(_build_feed_xml(items), encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    today = _dt.date.today()
    # Allow override for testing: env var DIGEST_DATE=YYYY-MM-DD
    env_date = os.environ.get("DIGEST_DATE")
    if env_date:
        today = _dt.date.fromisoformat(env_date)

    iso_year, iso_week, _ = today.isocalendar()
    idx = iso_week_index(today)

    case_studies = list_case_studies()
    pattern_files = list_week_files("patterns.md")
    challenge_files = list_week_files("challenges.md")

    cs = pick_case_study(case_studies, idx)
    drill = pick_pattern_drill(pattern_files, idx)
    challenge = pick_challenge(challenge_files, idx)

    md = render_markdown(cs or {}, drill or {}, challenge or {}, today, iso_year, iso_week)
    WEEKLY_PATH.write_text(md, encoding="utf-8")
    update_feed(cs or {}, drill or {}, challenge or {}, today, iso_year, iso_week)

    sys.stdout.write(
        f"Wrote {_rel(WEEKLY_PATH)} and {_rel(FEED_PATH)} "
        f"(ISO {iso_year}-W{iso_week:02d}, idx={idx}).\n"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
