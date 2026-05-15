"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: Factors of a Number (excluding 1 and n)
File: 10.factors.py

PROBLEM:
Given n, print all divisors i (2 <= i <= n/2) such that n % i == 0.

CONCEPT:
A factor of n divides n with NO remainder. No factor other than n itself
can exceed n/2, so we only test up to that limit. For an O(sqrt(n))
improvement we could iterate up to sqrt(n) and pair (i, n/i).

KEY POINTS:
 - `n % i == 0` -> i is a factor.
 - Loop bounds: 2..n//2 inclusive.
 - For large n use the sqrt(n) optimisation.

SYNTAX:
 for i in range(2, n // 2 + 1):
     if n % i == 0: print(i, end=" ")

DRY RUN:
 n = 12 -> factors: 2 3 4 6
 n = 7  -> (prime) no factors printed

COMPLEXITY: O(n/2) = O(n). Optimised: O(sqrt(n)).
"""

import sys
import math


def factors_excluding_extremes(n: int) -> list[int]:
    """Return divisors of n excluding 1 and n itself."""
    result: list[int] = []
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            result.append(i)
    return result


def factors_sqrt(n: int) -> list[int]:
    """O(sqrt n) version for large inputs."""
    result: set[int] = set()
    i = 2
    while i * i <= n:
        if n % i == 0:
            result.add(i)
            if i != n // i:
                result.add(n // i)
        i += 1
    result.discard(n)        # exclude n itself
    return sorted(result)


def main() -> None:
    if sys.stdin.isatty():
        n = 12
    else:
        n = int(sys.stdin.read().split()[0])
    facs = factors_excluding_extremes(n)
    print(" ".join(str(x) for x in facs))

    # Bonus: faster variant
    print(f"# sqrt-version: {factors_sqrt(n)}")


if __name__ == "__main__":
    main()


# NOTES:
# - Java's solution uses a manual `while` loop with `+= 1`. Python prefers `for + range`.
# - For prime testing, the sqrt(n) bound is the standard optimisation.
# - You could also write `[i for i in range(2, n // 2 + 1) if n % i == 0]` as a comprehension.
