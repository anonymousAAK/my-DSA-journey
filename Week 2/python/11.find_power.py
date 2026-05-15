"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: x raised to the power n (linear iteration)
File: 11.find_power.py

PROBLEM:
Compute x^n by multiplying x by itself n times. Convention: 0^0 == 1.

CONCEPT:
Iterative O(n) exponentiation. Multiply `ans` by `x` exactly n times. We
also showcase Python's built-in `pow(x, n)` and the `**` operator, plus the
O(log n) fast-exponentiation algorithm.

KEY POINTS:
 - `**` operator: `x ** n`  (returns int when x and n are int)
 - `pow(x, n)`  : built-in; supports `pow(x, n, mod)` for modular exponentiation
 - Python int has no overflow -- great for big results
 - O(log n) "fast power": exp by squaring (covered in Week 5 too)

SYNTAX:
 ans = 1
 for _ in range(n): ans *= x

 ans = x ** n          # idiomatic
 ans = pow(x, n)        # equivalent
 ans = pow(x, n, mod)   # modular

DRY RUN:
 x=2, n=10
   i=0: ans=2
   i=1: ans=4
   i=2: ans=8
   ...
   i=9: ans=1024

COMPLEXITY: linear O(n); fast version O(log n).
"""

import sys


def power_linear(x: int, n: int) -> int:
    """O(n) iterative exponentiation; mirrors Java's `for` loop."""
    ans = 1
    for _ in range(n):
        ans *= x
    return ans


def fast_pow(x: int, n: int) -> int:
    """O(log n) exponentiation by squaring (recursive)."""
    if n == 0:
        return 1
    if n % 2 == 0:
        half = fast_pow(x, n // 2)
        return half * half
    return x * fast_pow(x, n - 1)


def main() -> None:
    if sys.stdin.isatty():
        x, n = 2, 10
    else:
        toks = sys.stdin.read().split()
        x, n = int(toks[0]), int(toks[1])
    print(f"{x}^{n} = {power_linear(x, n)}  (linear)")
    print(f"{x}^{n} = {x ** n}  (** operator)")
    print(f"{x}^{n} = {pow(x, n)}  (pow)")
    print(f"{x}^{n} = {fast_pow(x, n)}  (fast)")


if __name__ == "__main__":
    main()


# NOTES:
# - Java's int overflows for 2^31 and beyond; Python ints just keep growing.
# - For modular exponentiation (e.g. RSA), use the 3-arg pow(): `pow(x, n, m)`.
# - The "exponent by squaring" pattern is used in many algorithms (matrix power,
#   modular inverses, etc.).
