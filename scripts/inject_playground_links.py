#!/usr/bin/env python3
"""Inject 'Try it live' playground links into every Week N/web/index.html.

For each week:
  1. Locate the <section id="live-demos" class="card"> ... </section> block.
  2. Insert a 'Try it live' callout right after the section's intro <p>.
     The callout links to ../../playground/?file=<urlencoded path> for the
     first .py file in that week's python/ directory (the "tour entry point").
  3. Idempotent: if a marker is already present, skip the file.

Run from repo root:

    python3 scripts/inject_playground_links.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent

MARKER = "<!-- playground-try-it-live -->"

# We insert the callout right after the opening intro <p>...</p> in the
# live-demos section. We anchor on the section's opening tag and on the
# first </p> following it.
SECTION_RE = re.compile(
    r'(<section\s+id="live-demos"[^>]*>\s*<h2>[^<]*</h2>\s*<p>[^<]*</p>)',
    re.IGNORECASE | re.DOTALL,
)

_FNAME_NUM = re.compile(r"^(\d+)")


def _entry_file(week_dir: Path) -> str | None:
    pydir = week_dir / "python"
    if not pydir.is_dir():
        return None
    cands = [
        p for p in pydir.iterdir()
        if p.is_file() and p.suffix == ".py" and not p.name.startswith("_")
    ]
    if not cands:
        return None
    cands.sort(
        key=lambda p: (
            int(_FNAME_NUM.match(p.name).group(1)) if _FNAME_NUM.match(p.name) else 10_000,
            p.name.lower(),
        )
    )
    return cands[0].name


def _callout_html(week_n: int, fname: str) -> str:
    # repo-relative path used by the playground's file_index.json
    repo_path = f"Week {week_n}/python/{fname}"
    href = "../../playground/?file=" + quote(repo_path, safe="")
    return (
        f"\n  {MARKER}\n"
        f'  <p style="margin:8px 0 16px 0;padding:12px 14px;'
        f'background:rgba(63,185,80,.08);border-left:4px solid #3fb950;'
        f'border-radius:0 8px 8px 0;font-size:.9rem">'
        f'<strong>Try it live:</strong> '
        f'<a href="{href}" target="_blank" rel="noopener">'
        f"Open this week&rsquo;s Python in the browser playground"
        f"</a> — edit and run instantly, no install."
        f"</p>"
    )


def process(week_n: int) -> str:
    wdir = ROOT / f"Week {week_n}"
    html_path = wdir / "web" / "index.html"
    if not html_path.is_file():
        return "no web/index.html"
    text = html_path.read_text(encoding="utf-8")
    if MARKER in text:
        return "already present"
    entry = _entry_file(wdir)
    if not entry:
        return "no .py files"
    callout = _callout_html(week_n, entry)
    new_text, n = SECTION_RE.subn(lambda m: m.group(1) + callout, text, count=1)
    if n == 0:
        return "live-demos section not found"
    html_path.write_text(new_text, encoding="utf-8")
    return f"injected -> {entry}"


def main() -> int:
    print("Injecting 'Try it live' playground links:")
    updated = 0
    for n in range(1, 31):
        status = process(n)
        print(f"  Week {n:>2}: {status}")
        if status.startswith("injected"):
            updated += 1
    print(f"\nUpdated {updated} week(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
