"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Binary to Decimal Conversion
File: 14.binary_to_decimal.py

PROBLEM:
Read an integer that LOOKS LIKE a binary number (e.g. 1100) and output its
decimal value (e.g. 12).

CONCEPT:
Iterate digits right to left, accumulate digit * 2^position into a sum.
Equivalent to evaluating the polynomial in base 2.

KEY POINTS:
 - `n % 10` -> rightmost "binary" digit (0 or 1)
 - `n //= 10` -> drop the rightmost digit
 - `pow *= 2` -> next position
 - Built-in: `int("1100", 2)` -> 12  (parse string in given base)

SYNTAX:
 dec = 0; pow = 1
 while n:
     dec += (n % 10) * pow
     pow *= 2
     n //= 10

DRY RUN (1100):
 n=1100 last=0 pow=1 -> dec=0;  n=110, pow=2
 n=110  last=0       -> dec=0;  n=11,  pow=4
 n=11   last=1       -> dec=4;  n=1,   pow=8
 n=1    last=1       -> dec=12; n=0    STOP
 -> 12

COMPLEXITY: O(d) where d = number of binary digits.
"""

import sys


def binary_to_decimal(n: int) -> int:
    dec = 0
    pow_ = 1
    while n > 0:
        bit = n % 10
        if bit not in (0, 1):
            raise ValueError(f"non-binary digit: {bit}")
        dec += bit * pow_
        pow_ *= 2
        n //= 10
    return dec


def main() -> None:
    if sys.stdin.isatty():
        for n in (1100, 1, 0, 11111111, 10101010):
            print(f"{n:>10} (binary) -> {binary_to_decimal(n)} (decimal)   "
                  f"[built-in: {int(str(n), 2)}]")
        return
    n = int(sys.stdin.read().split()[0])
    print(binary_to_decimal(n))


if __name__ == "__main__":
    main()


# NOTES:
# - Built-in `int(s, 2)` parses a binary STRING; cleaner than digit math.
# - For 32+ bit binary numbers, you might exceed int range in Java; Python is fine.
# - Conversely, `bin(12)` -> '0b1100' (string with 0b prefix).
