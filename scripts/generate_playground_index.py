#!/usr/bin/env python3
"""Generate playground/file_index.json from the Week N/python/*.py files.

The output JSON has the shape:

    {
      "generated_at": "...",
      "weeks": [
        {
          "week": 1,
          "title": "Week 1",
          "files": [
            {"name": "2.hello_world.py", "path": "Week 1/python/2.hello_world.py"},
            ...
          ]
        },
        ...
      ]
    }

The "path" field is repo-relative so the static playground can fetch it via
`fetch('../<path>')` when the site is served from the repo root.

Usage:
    python3 scripts/generate_playground_index.py
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "playground" / "file_index.json"

_FNAME_NUM = re.compile(r"^(\d+)")


def _file_sort_key(name: str) -> tuple[int, str]:
    """Sort files numerically by leading number, then alphabetically."""
    m = _FNAME_NUM.match(name)
    return (int(m.group(1)) if m else 10_000, name.lower())


def _week_title(week_dir: Path) -> str:
    readme = week_dir / "README.md"
    if readme.is_file():
        try:
            for line in readme.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
        except OSError:
            pass
    return week_dir.name


def main() -> int:
    weeks = []
    for n in range(1, 31):
        wdir = ROOT / f"Week {n}"
        pydir = wdir / "python"
        if not pydir.is_dir():
            continue
        files = []
        for p in sorted(pydir.iterdir(), key=lambda x: _file_sort_key(x.name)):
            if p.is_file() and p.suffix == ".py" and not p.name.startswith("_"):
                files.append(
                    {
                        "name": p.name,
                        "path": f"Week {n}/python/{p.name}",
                    }
                )
        if not files:
            continue
        weeks.append(
            {
                "week": n,
                "title": _week_title(wdir),
                "files": files,
            }
        )

    payload = {
        "generated_at": _dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "weeks": weeks,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    total = sum(len(w["files"]) for w in weeks)
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(weeks)} weeks, {total} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
