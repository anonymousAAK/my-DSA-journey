#!/usr/bin/env python3
"""
verify_certification.py — Validate a learner's progress.json + capstone
submissions and (if everything checks out) issue a signed credential.

Usage
-----

    python3 scripts/verify_certification.py \
        --progress path/to/progress.json \
        --user <github-username> \
        --capstone https://github.com/<user>/<fork>/pull/123 \
        --capstone https://github.com/<user>/<fork>/pull/124 \
        --capstone https://github.com/<user>/<fork>/pull/125 \
        [--output-dir ./out]

Outputs (written to ``--output-dir``, default ``.``):

    credential.json   machine-readable signed credential
    credential.txt    human-readable summary

The credential is signed with HMAC-SHA256 using the secret in the
``JOURNEY_CERT_SECRET`` environment variable.  This script ships with
**no** secret embedded — you supply your own when running it.  The
companion ``verify_credential.py`` script can validate the signature
given the same secret.

Stdlib-only.  See ``docs/CERTIFICATION.md`` for the full flow and
``docs/CERTIFICATION_LEVELS.md`` for the level rubric.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path


PASS_THRESHOLD = 80
TOTAL_WEEKS = 30

# Mirrors docs/CERTIFICATION_LEVELS.md.  Order matters: highest first.
LEVELS = [
    {
        "name": "Master",
        "weeks_required": list(range(1, 31)),
        "capstones_min": 4,
        "notes": "All 30 weeks at >=80% + 4 capstones (any) or capstones 1-3 + showcase.",
    },
    {
        "name": "Practitioner",
        "weeks_required": list(range(1, 21)),
        "capstones_min": 2,
        "notes": "Weeks 1-20 at >=80% + 2 capstones.",
    },
    {
        "name": "Foundation",
        "weeks_required": list(range(1, 11)),
        "capstones_min": 1,
        "notes": "Weeks 1-10 at >=80% + 1 capstone.",
    },
]


# ---------------------------------------------------------------------------
# Loading & validation
# ---------------------------------------------------------------------------

def load_progress(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if "weeks" not in data or not isinstance(data["weeks"], dict):
        raise ValueError("progress.json: missing or invalid 'weeks' object")
    return data


def passing_weeks(progress: dict) -> set[int]:
    """Return the set of week numbers passed at >=80%."""
    out: set[int] = set()
    for k, rec in (progress.get("weeks") or {}).items():
        if not str(k).isdigit() or not rec:
            continue
        rate = float(rec.get("rate", 0) or 0)
        if rate >= PASS_THRESHOLD:
            out.add(int(k))
    return out


def failing_weeks_for(level: dict, passed: set[int]) -> list[int]:
    return sorted(w for w in level["weeks_required"] if w not in passed)


def determine_level(passed: set[int], n_capstones: int) -> tuple[dict | None, list[str]]:
    """Return (level_dict_or_None, list_of_blockers_for_each_level_tried)."""
    blockers: list[str] = []
    for level in LEVELS:
        missing_weeks = failing_weeks_for(level, passed)
        ok_weeks = not missing_weeks
        ok_capstones = n_capstones >= level["capstones_min"]
        if ok_weeks and ok_capstones:
            return level, blockers
        if not ok_weeks:
            blockers.append(
                f"{level['name']}: missing weeks {missing_weeks}"
                + (f" and {level['capstones_min'] - n_capstones} capstone(s)"
                   if not ok_capstones else "")
            )
        elif not ok_capstones:
            blockers.append(
                f"{level['name']}: need {level['capstones_min']} capstones, got {n_capstones}"
            )
    return None, blockers


# ---------------------------------------------------------------------------
# Signing
# ---------------------------------------------------------------------------

def canonical_payload(payload: dict) -> bytes:
    """Stable serialization so signatures are reproducible."""
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sign(payload: dict, secret: str) -> str:
    mac = hmac.new(secret.encode("utf-8"), canonical_payload(payload), hashlib.sha256)
    return mac.hexdigest()


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def render_text(credential: dict) -> str:
    p = credential["payload"]
    lines = [
        "DSA Journey — Credential",
        "=" * 32,
        f"Learner          : {p['learner']}",
        f"Level            : {p['level']}",
        f"Issued (UTC)     : {p['issued']}",
        f"Weeks completed  : {len(p['weeks_completed'])} "
        f"({_format_range(p['weeks_completed'])})",
        f"Capstones        : {len(p['capstones_completed'])}",
    ]
    for c in p["capstones_completed"]:
        lines.append(f"   - {c}")
    lines.append("")
    lines.append(f"Signature (HMAC-SHA256): {credential['signature']}")
    lines.append("")
    lines.append("Anyone can verify this credential by running:")
    lines.append("  python3 scripts/verify_credential.py credential.json")
    lines.append("(with the same JOURNEY_CERT_SECRET set in the environment).")
    return "\n".join(lines) + "\n"


def _format_range(weeks: list[int]) -> str:
    if not weeks:
        return "-"
    weeks = sorted(weeks)
    runs: list[str] = []
    start = prev = weeks[0]
    for w in weeks[1:]:
        if w == prev + 1:
            prev = w
            continue
        runs.append(f"{start}" if start == prev else f"{start}-{prev}")
        start = prev = w
    runs.append(f"{start}" if start == prev else f"{start}-{prev}")
    return ",".join(runs)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify progress.json + capstones and issue a signed credential.",
    )
    parser.add_argument("--progress", type=Path, required=True,
                        help="Path to the learner's progress.json")
    parser.add_argument("--user", required=True,
                        help="GitHub username of the learner")
    parser.add_argument("--capstone", action="append", default=[],
                        help="Capstone PR URL (repeat for each, at least 3 for any level >= Practitioner)")
    parser.add_argument("--output-dir", type=Path, default=Path("."),
                        help="Where to write credential.json / credential.txt")
    parser.add_argument("--secret-env", default="JOURNEY_CERT_SECRET",
                        help="Env var holding the signing secret (default: JOURNEY_CERT_SECRET)")
    args = parser.parse_args(argv)

    secret = os.environ.get(args.secret_env)
    if not secret:
        print(
            f"error: ${args.secret_env} is not set.  Refusing to issue an "
            "unsigned credential.\n"
            "Set a secret for local testing, e.g.:\n"
            f"    export {args.secret_env}=$(python3 -c 'import secrets; print(secrets.token_hex(32))')",
            file=sys.stderr,
        )
        return 2

    try:
        progress = load_progress(args.progress)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: failed to load progress file: {exc}", file=sys.stderr)
        return 2

    passed = passing_weeks(progress)
    capstones = list(args.capstone)
    level, blockers = determine_level(passed, len(capstones))

    if level is None:
        print("Verification FAILED — no certification level reached.", file=sys.stderr)
        for b in blockers:
            print(f"  - {b}", file=sys.stderr)
        return 1

    issued = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()
    payload = {
        "learner": args.user,
        "issued": issued,
        "weeks_completed": sorted(passed),
        "capstones_completed": capstones,
        "level": level["name"],
        "schema": "dsa-journey-credential-v1",
    }
    signature = sign(payload, secret)
    credential = {
        "payload": payload,
        "signature": signature,
        "algorithm": "HMAC-SHA256",
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "credential.json"
    txt_path = args.output_dir / "credential.txt"
    with json_path.open("w", encoding="utf-8") as fh:
        json.dump(credential, fh, indent=2, sort_keys=True)
        fh.write("\n")
    with txt_path.open("w", encoding="utf-8") as fh:
        fh.write(render_text(credential))

    print(f"OK — issued {level['name']} credential for @{args.user}")
    print(f"  wrote {json_path}")
    print(f"  wrote {txt_path}")
    print()
    print(f"  weeks_completed : {_format_range(payload['weeks_completed'])}")
    print(f"  capstones       : {len(capstones)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
