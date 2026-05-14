"""
WEEK 4 - PYTHON PATTERN PROBLEMS
Topic: Square Pattern
File: 1.square_pattern.py

PATTERN (N=4):
4444
4444
4444
4444

CONCEPT:
Print an N x N grid where every cell is the digit N. Outer loop = rows
(1..N); inner loop = columns (1..N); print N at every cell.

KEY POINTS:
 - Two nested loops, both 1..N inclusive.
 - The cell value is constant N (not i, not j).
 - Pythonic alternative: `print((str(n) * n + "\\n") * n, end="")`.

SYNTAX:
 for i in range(n):
     for j in range(n):
         print(n, end="")
     print()

DRY RUN (N=3):
 row 1 -> "333"
 row 2 -> "333"
 row 3 -> "333"

COMPLEXITY: O(N^2).
"""

import sys


def square_loops(n: int) -> None:
    for _ in range(n):
        for _ in range(n):
            print(n, end="")
        print()


def square_oneliner(n: int) -> None:
    """Pythonic one-liner: build the whole grid as a single string."""
    print((str(n) * n + "\n") * n, end="")


def main() -> None:
    if sys.stdin.isatty():
        n = 4
    else:
        n = int(sys.stdin.read().split()[0])
    square_loops(n)
    print("--- one-liner ---")
    square_oneliner(n)


if __name__ == "__main__":
    main()


# NOTES:
# - String multiplication (`"abc" * 3 == "abcabcabc"`) makes pattern code
#   SHORTER but obscures the loop structure -- great for show, not for learning.
# - Use sys.stdout.write for one massive write to avoid per-line flushing.
# - Patterns are an excellent way to internalise nested-loop indices.
