"""
WEEK 5 - PYTHON FUNCTIONS & RECURSION
Topic: Recursion Basics
File: 3.recursion_basics.py

CONCEPT:
A recursive function calls itself with a SMALLER instance of the problem.
Every recursion needs:
  1. BASE CASE -- terminates the recursion
  2. RECURSIVE CASE -- progresses toward the base case

KEY POINTS:
 - Python's default RECURSION LIMIT is 1000 (sys.setrecursionlimit to change).
 - No tail-call optimisation -- deep recursion -> RecursionError.
 - For deep recursion, prefer iteration or convert to a stack-based loop.
 - functools.lru_cache memoises results, turning O(2^n) -> O(n).

PROBLEMS COVERED:
 1. Print N down to 1
 2. Print 1 up to N (using post-order)
 3. Factorial
 4. Sum of first N
 5. Power (linear and fast exponentiation)

COMPLEXITY:
 - Linear recursions: O(n) time, O(n) call-stack space
 - Fast power: O(log n) time
"""

import sys


def print_desc(n: int) -> None:
    if n == 0:
        return
    print(n, end=' ')
    print_desc(n - 1)


def print_asc(n: int) -> None:
    if n == 0:
        return
    print_asc(n - 1)
    print(n, end=' ')


def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def sum_n(n: int) -> int:
    if n == 0:
        return 0
    return n + sum_n(n - 1)


def power(base: int, exp: int) -> int:
    if exp == 0:
        return 1
    return base * power(base, exp - 1)


def fast_power(base: int, exp: int) -> int:
    if exp == 0:
        return 1
    if exp % 2 == 0:
        half = fast_power(base, exp // 2)
        return half * half
    return base * fast_power(base, exp - 1)


def main() -> None:
    print("Descending 5..1: ", end='')
    print_desc(5)
    print()

    print("Ascending 1..5: ", end='')
    print_asc(5)
    print()

    print(f"5!  = {factorial(5)}")
    print(f"10! = {factorial(10)}")

    print(f"sum(10) = {sum_n(10)}")

    print(f"2^10 = {power(2, 10)}")
    print(f"2^10 (fast) = {fast_power(2, 10)}")
    print(f"3^20 (fast) = {fast_power(3, 20)}")

    # Demonstrate recursion limit
    sys.setrecursionlimit(2000)
    print(f"sum_n(1500) = {sum_n(1500)}")


if __name__ == "__main__":
    main()


# NOTES:
# - Java/C++ have larger default stack sizes; Python's is only ~1000 frames.
# - For sum/factorial use the closed-form: n*(n+1)//2 / math.factorial(n).
# - Fast power uses exponent-by-squaring -- a fundamental DSA pattern.
# - Convert recursion to a loop or an explicit stack to avoid RecursionError.
