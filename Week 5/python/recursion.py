"""
Week 5 — Functions & Recursion
================================
Topics covered:
  - Factorial: iterative, recursive, tail-recursive (accumulator)
  - Fibonacci: naive recursive, memoized (@lru_cache), iterative
  - Tower of Hanoi
  - Power: naive O(n) and fast exponentiation O(log n)
  - Recursion patterns: reverse string, digit sum, palindrome check,
    generate all subsets (power set)

Each function includes time/space complexity analysis in its docstring.
"""

from __future__ import annotations

from functools import lru_cache
from typing import List


# ---------------------------------------------------------------------------
# Factorial
# ---------------------------------------------------------------------------

def factorial_iterative(n: int) -> int:
    """Return n! using a simple loop.

    Time:  O(n)
    Space: O(1)
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def factorial_recursive(n: int) -> int:
    """Return n! using head recursion.

    Time:  O(n)
    Space: O(n)  — call-stack depth
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return 1
    return n * factorial_recursive(n - 1)


def factorial_tail(n: int, accumulator: int = 1) -> int:
    """Return n! using tail recursion via an accumulator.

    Python does not optimize tail calls, but the pattern is still valuable
    for understanding the concept and porting to languages that do.

    Time:  O(n)
    Space: O(n)  — in CPython (no TCO); O(1) in a TCO-capable runtime
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n <= 1:
        return accumulator
    return factorial_tail(n - 1, n * accumulator)


# ---------------------------------------------------------------------------
# Fibonacci
# ---------------------------------------------------------------------------

def fibonacci_naive(n: int) -> int:
    """Return the n-th Fibonacci number (0-indexed) via naive recursion.

    fib(0) = 0, fib(1) = 1, fib(n) = fib(n-1) + fib(n-2)

    Time:  O(2^n)  — exponential due to repeated sub-problems
    Space: O(n)    — recursion depth
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)


@lru_cache(maxsize=None)
def fibonacci_memo(n: int) -> int:
    """Return fib(n) with automatic memoization via @lru_cache.

    Time:  O(n)  — each sub-problem computed once
    Space: O(n)  — cache + recursion depth
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return fibonacci_memo(n - 1) + fibonacci_memo(n - 2)


def fibonacci_iterative(n: int) -> int:
    """Return fib(n) iteratively — the most efficient approach.

    Time:  O(n)
    Space: O(1)
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


# ---------------------------------------------------------------------------
# Tower of Hanoi
# ---------------------------------------------------------------------------

def tower_of_hanoi(
    n: int,
    source: str = "A",
    auxiliary: str = "B",
    destination: str = "C",
    moves: list[str] | None = None,
) -> list[str]:
    """Solve the Tower of Hanoi for *n* disks and return the list of moves.

    Time:  O(2^n - 1) moves — optimal
    Space: O(n)  — recursion depth; O(2^n) for the moves list
    """
    if moves is None:
        moves = []
    if n == 1:
        moves.append(f"Move disk 1 from {source} to {destination}")
        return moves
    tower_of_hanoi(n - 1, source, destination, auxiliary, moves)
    moves.append(f"Move disk {n} from {source} to {destination}")
    tower_of_hanoi(n - 1, auxiliary, source, destination, moves)
    return moves


# ---------------------------------------------------------------------------
# Power / Exponentiation
# ---------------------------------------------------------------------------

def power_naive(base: float, exp: int) -> float:
    """Compute base^exp by multiplying *exp* times.

    Time:  O(n)   where n = |exp|
    Space: O(1)
    """
    if exp < 0:
        return 1.0 / power_naive(base, -exp)
    result = 1.0
    for _ in range(exp):
        result *= base
    return result


def power_fast(base: float, exp: int) -> float:
    """Compute base^exp via fast (binary) exponentiation.

    Also known as exponentiation by squaring.

    Time:  O(log n)
    Space: O(log n)  — recursion depth
    """
    if exp < 0:
        return 1.0 / power_fast(base, -exp)
    if exp == 0:
        return 1.0
    if exp % 2 == 0:
        half = power_fast(base, exp // 2)
        return half * half
    return base * power_fast(base, exp - 1)


# ---------------------------------------------------------------------------
# Recursion Patterns
# ---------------------------------------------------------------------------

def reverse_string(s: str) -> str:
    """Reverse a string recursively.

    Time:  O(n)
    Space: O(n)  — recursion depth + string copies
    """
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]


def digit_sum(n: int) -> int:
    """Return the sum of digits of a non-negative integer, recursively.

    Time:  O(d) where d = number of digits
    Space: O(d)
    """
    n = abs(n)
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


def is_palindrome(s: str) -> bool:
    """Check whether *s* is a palindrome, recursively.

    Time:  O(n)
    Space: O(n)  — recursion depth
    """
    if len(s) <= 1:
        return True
    if s[0] != s[-1]:
        return False
    return is_palindrome(s[1:-1])


def generate_subsets(nums: List[int]) -> List[List[int]]:
    """Generate all subsets (the power set) of *nums* using recursion.

    For each element we make two choices: include it or exclude it.

    Time:  O(n * 2^n)  — 2^n subsets, each copied in O(n)
    Space: O(n * 2^n)  — storing all subsets
    """
    result: List[List[int]] = []

    def backtrack(index: int, current: List[int]) -> None:
        if index == len(nums):
            result.append(current[:])  # copy current subset
            return
        # Exclude nums[index]
        backtrack(index + 1, current)
        # Include nums[index]
        current.append(nums[index])
        backtrack(index + 1, current)
        current.pop()  # undo choice (backtrack)

    backtrack(0, [])
    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # ---- Factorial ----
    for fn in (factorial_iterative, factorial_recursive, factorial_tail):
        assert fn(0) == 1
        assert fn(1) == 1
        assert fn(5) == 120
        assert fn(10) == 3628800
    print("[PASS] Factorial — all three variants")

    # ---- Fibonacci ----
    expected_fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    for fn in (fibonacci_naive, fibonacci_memo, fibonacci_iterative):
        for i, val in enumerate(expected_fib):
            assert fn(i) == val, f"{fn.__name__}({i}) failed"
    print("[PASS] Fibonacci — naive, memo, iterative")

    # ---- Tower of Hanoi ----
    moves = tower_of_hanoi(3)
    assert len(moves) == 7  # 2^3 - 1
    print(f"[PASS] Tower of Hanoi (3 disks) — {len(moves)} moves")

    # ---- Power ----
    assert power_naive(2, 10) == 1024
    assert power_fast(2, 10) == 1024
    assert abs(power_fast(2, -2) - 0.25) < 1e-9
    assert power_fast(3, 0) == 1.0
    print("[PASS] Power — naive & fast exponentiation")

    # ---- Recursion Patterns ----
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert digit_sum(12345) == 15
    assert digit_sum(0) == 0
    assert is_palindrome("racecar") is True
    assert is_palindrome("hello") is False
    assert is_palindrome("") is True

    subsets = generate_subsets([1, 2, 3])
    assert len(subsets) == 8  # 2^3
    # Verify every subset is present
    for s in [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]:
        assert s in subsets, f"Missing subset {s}"
    print("[PASS] Recursion patterns — reverse, digit_sum, palindrome, subsets")

    print("\nAll Week 5 tests passed!")
