"""
WEEK 2 - PYTHON CONTROL FLOW
Topic: Infinite Loop Demonstration
File: 5.infinite_loop.py

CONCEPT:
An infinite loop is one whose terminating condition never becomes false.
Python's idiomatic form is `while True: ...`. We DEMONSTRATE infinity here
by capping the iteration count so the program actually terminates.

KEY POINTS:
 - `while True:` is the canonical infinite loop.
 - Use `break` to exit; `continue` to skip the rest of the iteration.
 - Catching KeyboardInterrupt lets long-running loops respond to Ctrl-C cleanly.

SYNTAX:
 while True:
     ...
     if done: break

DRY RUN:
 x = y = 5
 In Java x and y both increment by 1 each iteration -> x == y FOREVER.
 In Python we add a safety counter so the demo terminates after 5 prints.

COMPLEXITY: theoretically unbounded; we cap at 5 iterations.
"""


def main() -> None:
    x = 5
    y = 5
    safety = 0
    while x == y:
        print("Hello")
        x += 1
        y += 1
        safety += 1
        if safety >= 5:
            print("(safety cap reached -- stopping the demo)")
            break

    # Equivalent canonical infinite-loop pattern:
    print("\n--- canonical pattern ---")
    n = 0
    while True:
        n += 1
        if n >= 3:
            print("breaking out after n =", n)
            break


if __name__ == "__main__":
    main()


# NOTES:
# - In Java the same code runs FOREVER (no safety cap). Always include a break
#   condition or a counter when DEMONSTRATING infinite-loop semantics.
# - Long-running loops should handle KeyboardInterrupt:
#       try: ... while True: ...
#       except KeyboardInterrupt: print("Interrupted")
# - Python has no `goto`; use functions + return for early exits across nested scopes.
