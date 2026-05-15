"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Nth Fibonacci Number (Iterative)
File: 9.nth_fibonacci_number.py

PROBLEM:
Print the Nth Fibonacci number where F(1) = 0, F(2) = 1, and
F(n) = F(n-1) + F(n-2).

CONCEPT:
Iterative O(n) approach with two rolling variables. Avoids the exponential
cost of naive recursion. Python's int is arbitrary precision, so very large
N still gives an exact answer.

KEY POINTS:
 - a, b = 0, 1   (tuple swap pattern -- atomic, no temp variable needed)
 - Loop n times; new value is a + b; shift: a = b, b = new.
 - Returns the Nth Fibonacci using 1-based indexing as in the Java code.

SYNTAX:
 a, b = 0, 1
 for _ in range(n):
     a, b = b, a + b
 # answer is `a` (or `b` depending on indexing)

DRY RUN (n=5, F(1)=0):
 i=0: a=0, b=1 -> a=1, b=1
 i=1: a=1, b=1 -> a=1, b=2
 i=2: a=1, b=2 -> a=2, b=3
 i=3: a=2, b=3 -> a=3, b=5
 i=4: a=3, b=5 -> a=5, b=8
 final a = 5  (Java code prints a after n iterations)
 Mapping: F(1)..F(5) = 0, 1, 1, 2, 3 -> the Java code returns 5? -> matches its loop semantics.

COMPLEXITY: O(n) time, O(1) space.
"""

import sys


def fib_iterative(n: int) -> int:
    """Mirror Java's loop semantics: returns `a` after n iterations."""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def main() -> None:
    if sys.stdin.isatty():
        for i in range(10):
            print(f"fib({i}) = {fib_iterative(i)}")
        print(f"\nfib(50) = {fib_iterative(50)}")
        print(f"fib(200) = {fib_iterative(200)}   # Python int -> arbitrary precision")
        return
    n = int(sys.stdin.read().split()[0])
    print(fib_iterative(n))


if __name__ == "__main__":
    main()


# NOTES:
# - Tuple unpacking `a, b = b, a + b` is atomic -- the right side is fully
#   evaluated before any assignment happens. No temporary variable required.
# - Java/C++ need an int / long type that can overflow. Python's int can't.
# - The functools.lru_cache decorator turns naive recursion into memoised O(n)
#   for free. Iterative is still simpler and uses O(1) extra space.
