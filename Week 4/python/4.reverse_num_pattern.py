"""
WEEK 4 - PYTHON PATTERN PROBLEMS
Topic: Reverse Number Pattern
File: 4.reverse_num_pattern.py

PATTERN (N=4):
1
21
321
4321

CONCEPT:
Row i contains digits from i down to 1.

KEY POINTS:
 - Inner counter starts at i and decrements to 1.
 - Pythonic: `print(*range(i, 0, -1), sep='')` or string join.

DRY RUN (N=3):
 row 1 -> "1"
 row 2 -> "21"
 row 3 -> "321"

COMPLEXITY: O(N^2).
"""

import sys


def main() -> None:
    n = 4 if sys.stdin.isatty() else int(sys.stdin.read().split()[0])

    # Translation of Java's while-loop
    cur_row = 1
    while cur_row <= n:
        cur_col = cur_row
        while cur_col >= 1:
            print(cur_col, end='')
            cur_col -= 1
        print()
        cur_row += 1

    print("--- pythonic ---")
    for i in range(1, n + 1):
        print(*range(i, 0, -1), sep='')


if __name__ == "__main__":
    main()


# NOTES:
# - `range(i, 0, -1)` -> i, i-1, ..., 1.
# - `print(*iterable, sep='')` unpacks values without spacing.
