"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: Character Case Detection via ASCII Values
File: 3.find_character_case.py

PROBLEM:
Given a single character print:
  1  -> if the character is an UPPERCASE letter (A-Z)
  0  -> if the character is a LOWERCASE letter (a-z)
 -1  -> otherwise

CONCEPT:
Use the ASCII (Unicode) code point of the character. In Python `ord(ch)`
returns the int code point of a length-1 string. ASCII ranges:
  uppercase 'A'-'Z' -> 65-90
  lowercase 'a'-'z' -> 97-122

KEY POINTS:
 - `ord(ch)` -> int code point.
 - Chained comparisons make range tests pleasant: `'A' <= ch <= 'Z'`.
 - You can also use `str.isupper()`, `str.islower()`, `str.isalpha()`.

SYNTAX:
 if 'A' <= ch <= 'Z': ...
 if ch.isupper(): ...

DRY RUN:
 ch = 'q' -> ord = 113 -> in 97..122 -> print 0
 ch = 'A' -> ord = 65  -> in 65..90  -> print 1
 ch = '7' -> ord = 55  -> neither    -> print -1

COMPLEXITY: O(1).
"""

import sys


def classify(ch: str) -> int:
    """Return 1 for uppercase, 0 for lowercase, -1 otherwise."""
    if not ch:
        return -1
    # Prefer the readable, idiomatic test:
    if ch.isupper():
        return 1
    if ch.islower():
        return 0
    return -1

    # Equivalent ASCII-range test (kept for clarity):
    # if 'A' <= ch <= 'Z': return 1
    # if 'a' <= ch <= 'z': return 0
    # return -1


def main() -> None:
    if sys.stdin.isatty():
        # Demo path with a few hard-coded cases when no input is piped
        for c in ("Q", "q", "7", "!"):
            print(f"{c!r} -> {classify(c)}")
        return

    raw = sys.stdin.read().strip()
    ch = raw[0] if raw else ""
    print(classify(ch))


if __name__ == "__main__":
    main()


# NOTES:
# - Java has `Character.isUpperCase(ch)` etc.; Python's str methods are the equivalent.
# - Python strings are Unicode -- isalpha() returns True for letters beyond ASCII too.
# - Chained comparison `'A' <= ch <= 'Z'` is unique to Python (and a few other langs).
# - `ord('A') == 65`, `chr(65) == 'A'` -- bidirectional helpers.
