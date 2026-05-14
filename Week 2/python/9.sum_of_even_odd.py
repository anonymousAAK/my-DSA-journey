"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: Sum of Even / Odd Digits
File: 9.sum_of_even_odd.py

PROBLEM:
Given integer N, compute the sum of its EVEN digits and the sum of its
ODD digits separately. Example: 13245 -> even (2+4) = 6; odd (1+3+5) = 9.

CONCEPT:
Extract digits one at a time using `% 10` and `// 10`. Classify each digit
by parity (`digit % 2`) and accumulate into the appropriate running sum.
Loop terminates when the number reduces to 0.

KEY POINTS:
 - `n % 10` -> rightmost digit.
 - `n //= 10` -> drop the rightmost digit.
 - Negative numbers: in Python `(-13) % 10 == 7` due to floor-mod behaviour.
   For this problem we operate on `abs(n)` to mirror Java.

SYNTAX:
 while n:
     d = n % 10
     ...
     n //= 10

DRY RUN:
 n = 13245
   d=5 odd  -> odd=5;   n=1324
   d=4 even -> even=4;  n=132
   d=2 even -> even=6;  n=13
   d=3 odd  -> odd=8;   n=1
   d=1 odd  -> odd=9;   n=0  STOP
 print "6 9"

COMPLEXITY: O(d) where d = number of digits.
"""

import sys


def sum_even_odd(n: int) -> tuple[int, int]:
    n = abs(n)
    even_sum = 0
    odd_sum  = 0
    while n > 0:
        d = n % 10
        if d % 2 == 0:
            even_sum += d
        else:
            odd_sum += d
        n //= 10
    return even_sum, odd_sum


def main() -> None:
    if sys.stdin.isatty():
        n = 13245
    else:
        n = int(sys.stdin.read().split()[0])
    e, o = sum_even_odd(n)
    print(f"{e} {o}")


if __name__ == "__main__":
    main()


# NOTES:
# - Python's `%` follows the SIGN OF THE DIVISOR, so `(-13)%10 == 7`. Take
#   absolute value first to avoid surprises with negative inputs.
# - You could also stringify: `sum(int(c) for c in str(abs(n)) if int(c)%2==0)`.
# - For very large `n`, arithmetic remains O(d) digits; Python handles big ints natively.
