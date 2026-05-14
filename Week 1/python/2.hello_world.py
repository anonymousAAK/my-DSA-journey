"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Hello World - First Python Program
File: 2.hello_world.py

CONCEPT:
The classic "Hello World" program. In Python it is a single line — there is
no class wrapper, no main method, no semicolons. The print() built-in writes
its argument(s) to standard output, followed by a newline.

KEY POINTS:
- print() is a built-in function (no import required)
- A `.py` file is itself a module; statements at module level run top-to-bottom
- No mandatory class, no `main` method
- Strings are delimited by either single or double quotes — both are equivalent
- Each statement ends with a newline (no semicolons needed)
- The optional `if __name__ == "__main__":` guard prevents a script from
  running when the file is imported as a module

SYNTAX:
print("text")               # prints text followed by a newline
print("a", "b")              # prints "a b" (space-separated by default)
print("a", "b", sep="-")     # prints "a-b" (custom separator)
print("no newline", end="")  # suppresses the trailing newline

DRY RUN:
1. Running `python3 2.hello_world.py` prints:
       Hello World
       Hello, World!
       Hello | World
       Same line: A B
2. The line `print()` with no args prints an empty line (just a newline).
"""


def main() -> None:
    # Simplest possible Hello World
    print("Hello World")

    # Strings can use single OR double quotes; both produce identical objects
    print('Hello, World!')

    # Pass multiple arguments — print joins them with a space by default
    print("Hello", "World")

    # Customise the separator with `sep=`
    print("Hello", "World", sep=" | ")

    # Suppress the trailing newline with `end=""`
    print("Same line:", end=" ")
    print("A", end=" ")
    print("B")  # default end="\n"


if __name__ == "__main__":
    main()


# NOTES:
# - Java requires `System.out.println("...")`; Python only needs `print(...)`.
# - Java needs a class + `main` signature; Python runs any top-level code directly.
# - In Java, `print` and `println` are separate methods. In Python, `end=""`
#   makes `print` behave like Java's `print`; default behaviour matches `println`.
# - Python is dynamically typed: no need to declare types for "Hello World" string.
# - Python also has `sys.stdout.write(...)` for low-level writes (no auto-newline).
