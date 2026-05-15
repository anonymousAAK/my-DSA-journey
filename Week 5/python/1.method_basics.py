"""
WEEK 5 - PYTHON FUNCTIONS & RECURSION
Topic: Function Basics
File: 1.method_basics.py

CONCEPT:
Python uses `def name(params): body` to declare a function. Functions are
FIRST-CLASS objects -- you can pass them around, store them in variables,
return them from other functions. There is no separate `static` concept;
methods on classes need a `@staticmethod` or `@classmethod` decorator.

KEY POINTS:
 - `def f(a, b): return a + b`
 - Default arguments: `def f(x, n=10): ...`
 - Keyword arguments: `f(x=1, n=5)`
 - Variable args: `*args` (tuple), `**kwargs` (dict)
 - Type hints (PEP 484) are documentation, not enforced
 - All Python arguments are PASSED BY OBJECT REFERENCE
   (looks like value for immutables; like reference for mutables)
 - `return` returns a value; missing return -> implicit `return None`

SYNTAX:
 def add(a: int, b: int) -> int:
     return a + b

 def greet(name: str = "world") -> None:
     print(f"Hello, {name}!")

DRY RUN:
 add(5, 6) -> 11
 try_to_change(42) -- mutates LOCAL n only; outer x stays 42
"""


def greet() -> None:
    print("Hello from a function!")


def print_sum(a: int, b: int) -> None:
    print(f"Sum of {a} and {b} = {a + b}")


def add(a: int, b: int) -> int:
    return a + b


def multiply(x: int, y: int) -> int:
    result = x * y       # local variable
    return result


def try_to_change(n: int) -> None:
    """Reassigning a parameter only affects the LOCAL binding."""
    n = 999
    print(f"  inside try_to_change: n = {n}")


def mutate_list(lst: list[int]) -> None:
    """Mutating a list reflects OUTSIDE the function (lists are mutable)."""
    lst.append(99)


def main() -> None:
    greet()
    print_sum(3, 7)
    print(f"add(5, 6) = {add(5, 6)}")
    print(f"multiply(4, 3) = {multiply(4, 3)}")

    # Pass-by-(object)-reference: int is immutable -> looks like value
    x = 42
    try_to_change(x)
    print(f"after try_to_change: x = {x}   # still 42")

    # But mutable objects ARE shared
    nums = [1, 2, 3]
    mutate_list(nums)
    print(f"after mutate_list: nums = {nums}")  # contains 99

    # Default & keyword arguments
    def power(base: int, exp: int = 2) -> int:
        return base ** exp
    print(f"power(5)        = {power(5)}")     # 25 (default exp=2)
    print(f"power(5, 3)     = {power(5, 3)}")  # 125
    print(f"power(exp=4, base=2) = {power(exp=4, base=2)}")  # 16


if __name__ == "__main__":
    main()


# NOTES:
# - Python has no `void` keyword; functions that don't return anything implicitly return None.
# - All args are passed as OBJECT REFERENCES; immutability of int/str/tuple makes
#   them feel value-like, while list/dict/set are mutable.
# - `**kwargs` packs keyword args into a dict; useful for forwarding.
# - Functions are first-class objects -- assign to vars, pass around, etc.
