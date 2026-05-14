"""
WEEK 3 - PYTHON LOOPS & NUMBER THEORY
Topic: Scope of Variables
File: 5.scope_of_variable.py

CONCEPT:
Python's scoping rules differ from Java's. Python uses LEGB:
  L  - Local       (inside the current function)
  E  - Enclosing   (outer function for nested defs)
  G  - Global      (module level)
  B  - Built-in    (e.g., print, len)

Crucially, BLOCKS (if/for/while) DO NOT introduce a new scope. A variable
defined inside a `for` loop body remains in scope after the loop exits!
This is the OPPOSITE of Java/C++.

KEY POINTS:
 - Functions create scopes; if/for/while DO NOT.
 - `global` keyword to assign to a module-level variable from inside a function.
 - `nonlocal` keyword to assign to an enclosing-function variable.
 - List/dict/set comprehensions DO create their own scope (since Python 3).

SYNTAX:
 for i in range(5):
     pass
 print(i)         # 4 -- still in scope!

DRY RUN:
 def f():
     for i in range(3):
         x = i * 2
     print(i, x)   # 2, 4
"""

x_global = "module-level x"


def loop_var_leaks_out() -> None:
    print("--- for variables leak out (unlike Java/C++) ---")
    for i in range(5):
        last = i
    # Both i and last are still accessible here
    print(f"after loop: i={i}, last={last}")


def function_creates_scope() -> None:
    print("\n--- function scope ---")
    def inner():
        local_v = "I live in inner"
        return local_v
    print(inner())
    # print(local_v)  # NameError: defined inside `inner`


def global_keyword_demo() -> None:
    print("\n--- global keyword ---")
    global x_global
    x_global = "rebound to a new value"
    print("inside:", x_global)


def nonlocal_keyword_demo() -> None:
    print("\n--- nonlocal keyword ---")
    counter = 0
    def increment():
        nonlocal counter
        counter += 1
    increment(); increment(); increment()
    print("counter is now:", counter)


def comprehension_scope() -> None:
    """List comprehensions DO have their own scope (since Python 3)."""
    print("\n--- comprehension scope ---")
    squares = [k * k for k in range(5)]   # k only lives inside the comprehension
    print("squares:", squares)
    # print(k)  # NameError in Python 3


def main() -> None:
    loop_var_leaks_out()
    function_creates_scope()
    print(f"\ng_global before func call: {x_global}")
    global_keyword_demo()
    print(f"g_global after func call: {x_global}")
    nonlocal_keyword_demo()
    comprehension_scope()


if __name__ == "__main__":
    main()


# NOTES:
# - Java/C++ `{}` blocks (including for/if) create new scopes; Python does NOT.
# - Loop counters and variables defined inside loops live on after the loop ends.
# - `global` modifies a module-level binding from within a function.
# - `nonlocal` modifies an enclosing-function binding (used in closures).
# - Comprehensions have their own scope so loop var doesn't leak (Python 3+).
