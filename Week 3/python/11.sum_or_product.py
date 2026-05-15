"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Sum or Product of First N Natural Numbers
File: 11.sum_or_product.py

PROBLEM:
Read N and choice C:
  C == 1 -> print sum 1 + 2 + ... + N
  C == 2 -> print product 1 * 2 * ... * N
  else   -> print -1

CONCEPT:
Either iterate and accumulate, or use the closed-form formulas:
  sum(1..N)     = N * (N+1) / 2
  product(1..N) = N! (math.factorial)

KEY POINTS:
 - sum: identity is 0
 - product: identity is 1 (NOT 0; 0 * anything = 0)
 - Python ints don't overflow -- factorial of 1000 is fine.

SYNTAX:
 sum(range(1, N+1))
 math.prod(range(1, N+1))
 math.factorial(N)

DRY RUN:
 N=5, C=1 -> 1+2+3+4+5 = 15
 N=5, C=2 -> 1*2*3*4*5 = 120
"""

import sys
import math


def sum_n(n: int) -> int:
    return n * (n + 1) // 2


def product_n(n: int) -> int:
    return math.factorial(n)


def main() -> None:
    if sys.stdin.isatty():
        n, choice = 5, 1
    else:
        toks = sys.stdin.read().split()
        n, choice = int(toks[0]), int(toks[1])

    if choice == 1:
        print(sum_n(n))
    elif choice == 2:
        print(product_n(n))
    else:
        print(-1)


if __name__ == "__main__":
    main()


# NOTES:
# - Built-ins `sum(range(1, N+1))` and `math.prod(range(1, N+1))` are idiomatic.
# - The closed-form formulas are O(1) (or O(N!) for factorial computation cost).
# - Python's math.factorial uses C-level optimisation -- much faster than a loop.
