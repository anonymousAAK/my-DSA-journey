"""
WEEK 7 - PYTHON DSA
Topic: String Basics
File: 1.string_basics.py

CONCEPT:
    Python strings are immutable sequences of Unicode code points.
    Every "modification" produces a new string. For repeated
    construction, build with a list and ''.join() or use io.StringIO.

KEY POINTS:
    - len(s), s[i], s[a:b], s.find(sub), 'sub' in s
    - .lower(), .upper(), .replace(), .strip(), .split()
    - Concatenation with `+` in a loop is O(n^2) like Java — use .join.
    - Strings are immutable; convert to list for in-place edits.

ALGORITHM / APPROACH:
    Common operations in O(1) or O(n):
        s[i]      O(1)
        s[a:b]    O(b-a)  copies into a new string
        s.find    O(n*m)  naive; CPython uses a fast Boyer-Moore variant
        ''.join() O(n)    when given a sequence of strings

PYTHON-SPECIFIC NOTES:
    - String "comparison" with == checks content; `is` checks identity.
    - f-strings (PEP 498) are the modern formatting tool.
    - .split() with no args splits on any whitespace and trims empties.

DRY RUN:
    s = "Hello, World!"
    len(s) = 13
    s[7] = 'W'
    s[7:12] = 'World'
    s.find('o') = 4
    s.lower() = 'hello, world!'
    s.replace('l','r') = 'Herro, Worrd!'

COMPLEXITY:
    See per-operation table above; most are linear in their argument size.
"""


def main() -> None:
    s = "Hello, World!"
    print(f"String: {s}")
    print(f"len: {len(s)}")
    print(f"s[7]: {s[7]}")
    print(f"s[7:12]: {s[7:12]}")
    print(f"s.find('o'): {s.find('o')}")
    print(f"s.rfind('o'): {s.rfind('o')}")
    print(f"'World' in s: {'World' in s}")
    print(f"s.lower(): {s.lower()}")
    print(f"s.upper(): {s.upper()}")
    print(f"s.replace('l','r'): {s.replace('l', 'r')}")
    print(f'  "  hello  ".strip() = "{"  hello  ".strip()}"')

    # --- Comparison ---
    a = "apple"
    b = "apple"
    c = str(["a", "p", "p", "l", "e"])  # different content
    print(f'\n"apple" == "apple": {a == b}')
    print(f'"apple" is "apple" (interned): {a is b}')
    print(f'a == c: {a == c}')

    # Lexicographic compare
    print(f'"apple" < "banana": {"apple" < "banana"}')

    # --- String <-> list ---
    chars = list(s)
    print(f"\nlist(s): {chars}")
    print(f"''.join(chars): {''.join(chars)}")

    # --- Split ---
    csv = "one,two,three,four"
    parts = csv.split(",")
    print("\nSplit by ',':")
    for p in parts:
        print(f"  {p}")

    # --- Build with join (preferred over += in a loop) ---
    pieces: list[str] = []
    for i in range(1, 6):
        pieces.append(str(i))
        if i < 5:
            pieces.append("-")
    print(f"\nBuilt with join: {''.join(pieces)}")

    # Reverse
    print(f"Reversed: {s[::-1]}")
    print(f"Reversed via reversed(): {''.join(reversed(s))}")

    # BAD: O(n^2) loop concat — shown but commented out
    # result = ""
    # for ch in chars: result += ch
    # GOOD: O(n) join
    good = "".join(chars)
    print(f"\nRebuilt string: {good}")


if __name__ == "__main__":
    main()


"""
NOTES — Python vs Java:
    - No StringBuilder; use a list + ''.join() for O(n) building.
    - Strings are sequences, so slicing (s[a:b], s[::-1]) is built in.
    - Unicode is native — len(s) counts code points, not bytes.
    - 'in' operator (`"x" in s`) replaces s.contains("x").
"""
