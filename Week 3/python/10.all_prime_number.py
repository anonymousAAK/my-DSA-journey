"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: All Prime Numbers up to N
File: 10.all_prime_number.py

PROBLEM:
Print every prime in [2, N], one per line.

CONCEPT:
A prime is divisible only by 1 and itself. The naive trial-division checks
each i for any divisor in [2, i-1]; the canonical optimisation is [2, sqrt(i)].
For "many primes up to N" use the SIEVE OF ERATOSTHENES, which is O(N log log N).

KEY POINTS:
 - Naive: O(N^2)
 - sqrt optimisation: O(N * sqrt(N))
 - Sieve: O(N log log N) -- fastest for N up to ~10^7

SYNTAX:
 def is_prime(n):
     if n < 2: return False
     for i in range(2, int(n ** 0.5) + 1):
         if n % i == 0: return False
     return True

DRY RUN (N=10):
 2 -> prime
 3 -> prime
 4 = 2*2 -> not
 5 -> prime
 6 = 2*3 -> not
 7 -> prime
 8 = 2*4 -> not
 9 = 3*3 -> not
 10 = 2*5 -> not
 -> 2, 3, 5, 7
"""

import sys


def is_prime_naive(n: int) -> bool:
    if n < 2:
        return False
    for j in range(2, n):
        if n % j == 0:
            return False
    return True


def is_prime_sqrt(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    j = 3
    while j * j <= n:
        if n % j == 0:
            return False
        j += 2
    return True


def sieve(n: int) -> list[int]:
    """Sieve of Eratosthenes -- best for many primes up to N."""
    if n < 2:
        return []
    composite = [False] * (n + 1)
    composite[0] = composite[1] = True
    for i in range(2, int(n ** 0.5) + 1):
        if not composite[i]:
            for j in range(i * i, n + 1, i):
                composite[j] = True
    return [i for i in range(2, n + 1) if not composite[i]]


def main() -> None:
    if sys.stdin.isatty():
        n = 30
    else:
        n = int(sys.stdin.read().split()[0])
    # Mirror the Java approach (one prime per line)
    for i in range(2, n + 1):
        if is_prime_naive(i):
            print(i)
    # Bonus: sieve
    print(f"# sieve up to {n}: {sieve(n)}")


if __name__ == "__main__":
    main()


# NOTES:
# - For competitive-programming-grade prime tests, use Miller-Rabin (probabilistic).
# - Python lists are O(1) random access; the sieve uses a boolean array.
# - For BIG primes (cryptographic), use the `sympy.isprime` function.
