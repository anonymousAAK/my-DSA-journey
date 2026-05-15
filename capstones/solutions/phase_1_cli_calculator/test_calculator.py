"""Tests for calculator.py. Run: python test_calculator.py"""
from __future__ import annotations

import math
import sys

from calculator import CalcError, evaluate


def expect(expr: str, want: float) -> None:
    got = evaluate(expr)
    assert math.isclose(got, want, rel_tol=1e-9, abs_tol=1e-12), f"{expr} -> {got}, want {want}"


def expect_error(expr: str, fragment: str) -> None:
    try:
        evaluate(expr)
    except CalcError as e:
        assert fragment in e.msg, f"{expr}: error {e.msg!r} missing {fragment!r}"
        return
    raise AssertionError(f"{expr}: expected error containing {fragment!r}")


def main() -> int:
    # Basics
    expect("1+1", 2)
    expect("2*3+4", 10)
    expect("2+3*4", 14)
    expect("(2+3)*4", 20)
    expect("10/2/5", 1)
    expect("10-2-3", 5)  # left-assoc
    expect("3.14", 3.14)
    expect(".5+.5", 1.0)
    expect("2.", 2.0)

    # Unary minus
    expect("-3", -3)
    expect("-3 * -4", 12)
    expect("-3 * (-4 + 5)", -3)
    expect("--5", 5)
    expect("+-+3", -3)

    # Exponent right-assoc
    expect("2^3", 8)
    expect("2^3^2", 512)
    expect("(2^3)^2", 64)
    # In our grammar unary is below factor (factor -> unary ('^' factor)?), so unary binds
    # tighter than '^'. That means -2^2 parses as (-2)^2 = 4. Document and lock the behavior.
    expect("-2^2", 4)
    expect("0 - 2^2", -4)  # the "math convention" form using subtraction

    # Functions
    expect("sqrt(16)", 4)
    expect("sqrt(2)^2", 2)
    expect("abs(-7)", 7)
    expect("min(3, 5)", 3)
    expect("max(min(1,2), 0)", 1)
    expect("max(1, 2) * 10", 20)

    # Parentheses nesting
    expect("((((1+2))))", 3)
    expect("(((1+2)*3)+4)", 13)

    # Errors
    expect_error("1+", "expected")
    expect_error("(1+2", "missing ')'")
    expect_error("1 2", "unexpected")
    expect_error("1/0", "division by zero")
    expect_error("foo(1)", "unknown function")
    expect_error("max(1)", "expects 2")
    expect_error("@", "unexpected character")
    expect_error("3..5", "malformed number")

    # Performance smoke test
    big = "+".join(["1"] * 5000)
    assert evaluate(big) == 5000

    # Deep parens. Each '(' eats ~5 frames (expr->term->factor->unary->primary), so we bump
    # the recursion limit before testing. This documents the depth tradeoff of recursive descent.
    sys.setrecursionlimit(10000)
    depth = 150
    expr = "(" * depth + "1" + ")" * depth
    assert evaluate(expr) == 1

    print("calculator: all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
