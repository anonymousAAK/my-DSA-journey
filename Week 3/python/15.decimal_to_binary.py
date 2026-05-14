"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Decimal to Binary Conversion
File: 15.decimal_to_binary.py

PROBLEM:
Read decimal N and output its binary representation as an integer
(e.g. 12 -> 1100).

CONCEPT:
Repeatedly take N % 2 (the next bit), prepend to result. The original Java
code stores the binary digits as DECIMAL place values (1, 10, 100, ...) so
that the final integer "looks like" the binary representation.

KEY POINTS:
 - `bit = n % 2`
 - `binary += bit * pow`; `pow *= 10`
 - `n //= 2`
 - Built-in: `bin(n)` -> "0b1100"; `format(n, 'b')` -> "1100"

SYNTAX:
 binary = 0; pow = 1
 while n:
     binary += (n % 2) * pow
     pow *= 10
     n //= 2

DRY RUN (n=12):
 n=12 bit=0 -> binary=0;   n=6,  pow=10
 n=6  bit=0 -> binary=0;   n=3,  pow=100
 n=3  bit=1 -> binary=100; n=1,  pow=1000
 n=1  bit=1 -> binary=1100; n=0  STOP
 print 1100

COMPLEXITY: O(log n).
"""

import sys


def decimal_to_binary_int(n: int) -> int:
    """Mirror Java approach -- returns integer whose decimal digits ARE the binary."""
    if n == 0:
        return 0
    binary = 0
    pow_ = 1
    while n > 0:
        binary += (n % 2) * pow_
        pow_ *= 10
        n //= 2
    return binary


def main() -> None:
    if sys.stdin.isatty():
        for n in (0, 1, 2, 12, 255, 1024):
            print(f"{n:>5} -> {decimal_to_binary_int(n):>11}  [bin(): {bin(n)}]")
        return
    n = int(sys.stdin.read().split()[0])
    print(decimal_to_binary_int(n))


if __name__ == "__main__":
    main()


# NOTES:
# - In Python the built-in `bin(n)` or f"{n:b}" returns a STRING -- cleaner
#   when you just need the binary representation.
# - Storing the binary as a "decimal-encoded" int is cute but limits you to
#   values whose binary form fits in an int (Python is unbounded; Java needed long).
# - For negative N, decide on a fixed bit width and emit two's complement.
