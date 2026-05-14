"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: While Loop Basics
File: 4.while_loop.py

CONCEPT:
A `while` loop repeats as long as the condition is truthy. Python does NOT
support assignment inside an expression the way Java does (`(x = 5) == y`),
because `=` is a STATEMENT, not an expression. PEP 572 introduced the
"walrus operator" `:=` for assignment expressions (Python 3.8+).

KEY POINTS:
 - Syntax: `while cond: body`
 - There is NO do-while in Python; emulate with `while True: ... if not cond: break`.
 - `else` clause on a while: runs when the loop exits NORMALLY (without break).
 - Walrus `:=` lets you assign and test in one expression, but it is rarely
   needed and never appears in beginner code.

SYNTAX:
 while x < y:
     x += 1

 while (line := input()):
     ...  # walrus assignment

DRY RUN (Java equivalent (x=5)==y):
 In Java, `(x = 5) == y` ASSIGNS 5 to x, then compares with y. Python:
   `x = 5; while x == y:` — the assignment is OUTSIDE the condition.
   That's why we discuss the Java behaviour and SHOW the Python translation.
 Step:
   x = 5; y = 5
   Iteration 1: x == y -> True -> print "Hello"; x = 6; y = 6
   Iteration 2: x == y -> True -> infinite loop!  (We break after 5 iters.)

COMPLEXITY: depends on the loop body and condition.
"""


def java_style_assignment_loop() -> None:
    """Translation of Java's `while ((x=5) == y)` quirk to clear Python."""
    print("--- Java semantics translated to Python ---")
    x = 5
    y = 5
    iterations = 0
    # Re-create the Java semantics by reassigning x at the top of each iteration
    while True:
        x = 5           # mimic the assignment in Java's condition
        if x != y:       # condition test
            break
        print("Hello")
        x += 1
        y += 1
        iterations += 1
        if iterations > 5:  # safety cap (don't loop forever)
            break
    print(f"(loop body ran {iterations} time(s))")


def plain_while_with_break() -> None:
    """Demonstrate a clean while loop with safe termination."""
    print("\n--- Plain while loop ---")
    i = 1
    while i <= 5:
        print(i)
        i += 1
    else:
        print("loop completed without break")


def walrus_demo() -> None:
    """Use the walrus operator for the closest analogue to Java's quirk."""
    print("\n--- Walrus operator demo (Python 3.8+) ---")
    nums = iter([1, 2, 3, 4, 5])
    while (n := next(nums, None)) is not None:
        print(f"got {n}")


def main() -> None:
    java_style_assignment_loop()
    plain_while_with_break()
    walrus_demo()


if __name__ == "__main__":
    main()


# NOTES:
# - Python forbids `if (x = 5):` — assignment is a statement, not expression.
# - Walrus `:=` (PEP 572) is the closest equivalent and is mostly used in loops.
# - `while...else` runs after a NORMAL exit (not after break) — useful for "search" loops.
