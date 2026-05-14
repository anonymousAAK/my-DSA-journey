"""
WEEK 5 - PYTHON FUNCTIONS & RECURSION
Topic: Method Overloading
File: 2.method_overloading.py

CONCEPT:
PYTHON HAS NO METHOD OVERLOADING in the Java sense. Two function definitions
with the same name simply OVERWRITE each other. To dispatch on type or arity,
use:
  - Default / variable arguments
  - Type checks inside the body (if isinstance(x, int): ...)
  - functools.singledispatch decorator (idiomatic; runtime type-dispatch)

KEY POINTS:
 - The LAST definition wins; previous bindings are lost.
 - functools.singledispatch dispatches on the FIRST argument's runtime type.
 - For static (compile-time) dispatch, Python is the wrong language.

SYNTAX:
 from functools import singledispatch
 @singledispatch
 def add(a, b): raise NotImplementedError
 @add.register(int)
 def _(a, b): return a + b
 @add.register(float)
 def _(a, b): return a + b

DRY RUN:
 add(2, 3)        -> int dispatch  -> 5
 add(1.5, 2.5)    -> float dispatch -> 4.0
"""

from functools import singledispatch
from typing import Iterable


# Approach 1: variable arguments
def add_variadic(*nums: float) -> float:
    """Replaces add(a,b), add(a,b,c) etc."""
    return sum(nums)


# Approach 2: singledispatch (runtime type-based dispatch on first arg)
@singledispatch
def double(value):
    """Generic fallback for unknown types."""
    raise NotImplementedError(f"don't know how to double {type(value).__name__}")


@double.register(int)
def _(value: int) -> int:
    print("int branch")
    return value * 2


@double.register(float)
def _(value: float) -> float:
    print("float branch")
    return value * 2


@double.register(str)
def _(value: str) -> str:
    print("str branch")
    return value * 2


# Approach 3: print arrays of various types via duck typing
def print_array(arr: Iterable) -> None:
    """Works for any iterable -- the ultimate "overload"."""
    print("[" + ", ".join(repr(x) for x in arr) + "]")


def main() -> None:
    # Variadic
    print(add_variadic(2, 3))                # 5
    print(add_variadic(1, 2, 3))             # 6
    print(add_variadic(1.5, 2.5))            # 4.0

    # singledispatch
    print(double(5))                          # int branch -> 10
    print(double(2.5))                        # float branch -> 5.0
    print(double("ab"))                       # str branch -> "abab"
    try:
        print(double([1, 2]))
    except NotImplementedError as e:
        print(f"caught: {e}")

    # Duck typing handles any iterable
    print_array([1, 2, 3])
    print_array((1.1, 2.2, 3.3))
    print_array("hello")
    print_array({1, 2, 3})


if __name__ == "__main__":
    main()


# NOTES:
# - Java's compile-time overloading -> Python uses runtime dispatch or duck typing.
# - functools.singledispatch is the standard library way to dispatch on type.
# - For multiple-argument dispatch, use multipledispatch (3rd party) or pattern matching.
# - Default args + isinstance checks cover most cases without extra libraries.
