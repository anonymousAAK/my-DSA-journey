#!/usr/bin/env python3
"""
verify_credential.py — Public verifier for DSA Journey credentials.

Anyone with the signing secret can confirm a credential JSON was
issued by the repo's certification flow.  Usage:

    JOURNEY_CERT_SECRET=<shared-secret> \
        python3 scripts/verify_credential.py credential.json

Exit codes:

    0  signature is valid and payload looks well-formed
    1  signature is invalid OR payload is malformed
    2  usage error (e.g. missing secret, unreadable file)

Stdlib-only — uses ``hmac.compare_digest`` for constant-time comparison.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path


REQUIRED_FIELDS = {
    "learner",
    "issued",
    "weeks_completed",
    "capstones_completed",
    "level",
    "schema",
}
ALLOWED_LEVELS = {"Foundation", "Practitioner", "Master"}
ALLOWED_SCHEMAS = {"dsa-journey-credential-v1"}


def canonical_payload(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify(credential: dict, secret: str) -> tuple[bool, str]:
    if "payload" not in credential or "signature" not in credential:
        return False, "credential missing 'payload' or 'signature' fields"

    algo = credential.get("algorithm", "HMAC-SHA256")
    if algo != "HMAC-SHA256":
        return False, f"unsupported algorithm: {algo!r}"

    payload = credential["payload"]
    missing = REQUIRED_FIELDS - set(payload)
    if missing:
        return False, f"payload missing required fields: {sorted(missing)}"

    if payload["schema"] not in ALLOWED_SCHEMAS:
        return False, f"unknown schema: {payload['schema']!r}"
    if payload["level"] not in ALLOWED_LEVELS:
        return False, f"unknown level: {payload['level']!r}"

    expected = hmac.new(
        secret.encode("utf-8"), canonical_payload(payload), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(expected, credential["signature"]):
        return False, "signature does not match payload"

    return True, "signature valid"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify a DSA Journey credential JSON (HMAC-SHA256).",
    )
    parser.add_argument("credential", type=Path,
                        help="Path to credential.json")
    parser.add_argument("--secret-env", default="JOURNEY_CERT_SECRET",
                        help="Env var holding the verification secret (default: JOURNEY_CERT_SECRET)")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress payload summary; only print PASS/FAIL.")
    args = parser.parse_args(argv)

    secret = os.environ.get(args.secret_env)
    if not secret:
        print(f"error: ${args.secret_env} is not set.", file=sys.stderr)
        return 2

    try:
        with args.credential.open("r", encoding="utf-8") as fh:
            credential = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: cannot read credential: {exc}", file=sys.stderr)
        return 2

    ok, reason = verify(credential, secret)

    if not ok:
        print(f"INVALID: {reason}")
        return 1

    print("VALID: signature verified")
    if not args.quiet:
        p = credential["payload"]
        print(f"  learner          : {p['learner']}")
        print(f"  level            : {p['level']}")
        print(f"  issued           : {p['issued']}")
        print(f"  weeks_completed  : {len(p['weeks_completed'])} weeks")
        print(f"  capstones        : {len(p['capstones_completed'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
