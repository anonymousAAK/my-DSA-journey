"""
WEEK 5 - PYTHON FUNCTIONS & RECURSION
Topic: Fibonacci -- Recursion, Memoisation, Iteration
File: 4.fibonacci_recursion.py

CONCEPT:
Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, ...
Three approaches with very different time complexities:
  1. Naive recursion: O(2^n) -- recomputes overlapping subproblems
  2. Memoisation: O(n) -- cache subproblem results
  3. Iterative bottom-up: O(n) time, O(1) space

KEY POINTS:
 - Naive recursion DEMONSTRATES exponential blow-up; never use for n > 35.
 - functools.lru_cache decorator gives free memoisation.
 - Iterative bottom-up uses two rolling variables -- cleanest, fastest.

SYNTAX:
 @functools.lru_cache(maxsize=None)
 def fib_memo(n): ...

DRY RUN (n=5):
 fib_naive(5):
   fib(4) + fib(3)
   = (fib(3) + fib(2)) + (fib(2) + fib(1))
   = ... 9 calls total
 fib_memo(5): 5 unique calls; 4 cache hits
 fib_iter(5): 5 loop iterations
"""

import sys
import functools


def fib_naive(n: int) -> int:
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


@functools.lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)


def fib_iterative(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# Helper to count naive recursion calls
def count_calls(n: int) -> int:
    calls = [0]
    def helper(n: int) -> int:
        calls[0] += 1
        if n <= 1:
            return n
        return helper(n - 1) + helper(n - 2)
    helper(n)
    return calls[0]


def main() -> None:
    print("First 10 Fibonacci numbers:", end=' ')
    for i in range(10):
        print(fib_iterative(i), end=' ')
    print()

    n = 10
    print(f"\nfib({n}):")
    print(f"  Naive    : {fib_naive(n)}")
    print(f"  Memo     : {fib_memo(n)}")
    print(f"  Iterative: {fib_iterative(n)}")

    big = 45
    print(f"\nfib({big}) iterative = {fib_iterative(big)}")
    print(f"fib({big}) memoised = {fib_memo(big)}")

    print(f"\nKEY INSIGHT: fib_naive(5) makes {count_calls(5)} recursive calls")
    print(f"          fib_naive(10) makes {count_calls(10)} recursive calls")

    # Python ints are arbitrary-precision -- huge fib values are exact
    print(f"\nfib(200) = {fib_iterative(200)}")
    sys.setrecursionlimit(5000)


if __name__ == "__main__":
    main()


# NOTES:
# - functools.lru_cache turns a recursive function into a memoised one with one decorator.
# - For O(log n), use matrix exponentiation or fast doubling.
# - Python's int is arbitrary precision -> no overflow at any n.
# - Watch out for recursion depth on n > 1000 even with memoisation.
