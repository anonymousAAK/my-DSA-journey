"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Reverse the Digits of an Integer
File: 13.reverse.py

PROBLEM:
Read N, output the integer obtained by reversing its digits. Trailing zeros
in the original become leading zeros in the reversed number and are
dropped (10400 -> 401).

CONCEPT:
Standard digit-extraction loop:
  rev = rev * 10 + last_digit
  n  //= 10
Repeat until n == 0.

KEY POINTS:
 - Handle negative numbers: reverse abs(n), preserve sign.
 - Or: int(str(abs(n))[::-1]) -- string-based one-liner.
 - For 32-bit overflow check (LeetCode-style), validate against 2^31-1.

SYNTAX:
 rev = 0
 while n:
     rev = rev * 10 + n % 10
     n //= 10

DRY RUN (n=1234):
 rev=0; n=1234 -> rev=4,  n=123
 rev=4;          -> rev=43, n=12
 rev=43;         -> rev=432,n=1
 rev=432;        -> rev=4321,n=0
 print 4321

COMPLEXITY: O(d) where d = number of digits.
"""

import sys


def reverse_int(n: int) -> int:
    sign = -1 if n < 0 else 1
    n = abs(n)
    rev = 0
    while n > 0:
        rev = rev * 10 + n % 10
        n //= 10
    return sign * rev


def reverse_via_string(n: int) -> int:
    """One-liner via string slicing -- often the most Pythonic."""
    sign = -1 if n < 0 else 1
    return sign * int(str(abs(n))[::-1])


def main() -> None:
    if sys.stdin.isatty():
        for n in (1234, 10400, 7, -42):
            print(f"reverse({n:>6}) = {reverse_int(n)}    str-slice: {reverse_via_string(n)}")
        return
    n = int(sys.stdin.read().split()[0])
    print(reverse_int(n))


if __name__ == "__main__":
    main()


# NOTES:
# - String slicing `s[::-1]` is the Pythonic way to reverse any sequence.
# - For Java/C++, the digit-extraction loop is the only sane option (no easy reverse).
# - Mind the sign and trailing zeros.
