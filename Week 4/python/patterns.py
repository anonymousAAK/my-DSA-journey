"""
WEEK 4 — Python: Pattern Printing
Master nested loops by printing various patterns.
Equivalent to Java Week 4.
"""

def square_pattern(n: int):
    """Print NxN square of N's"""
    for _ in range(n):
        print(" ".join([str(n)] * n))

def right_triangle_stars(n: int):
    """
    *
    * *
    * * *
    * * * *
    """
    for i in range(1, n + 1):
        print("* " * i)

def right_triangle_numbers(n: int):
    """
    1
    2 2
    3 3 3
    """
    for i in range(1, n + 1):
        print(f"{i} " * i)

def inverted_triangle(n: int):
    """
    * * * * *
    * * * *
    * * *
    * *
    *
    """
    for i in range(n, 0, -1):
        print("* " * i)

def pyramid(n: int):
    """
        *
       * *
      * * *
     * * * *
    * * * * *
    """
    for i in range(1, n + 1):
        spaces = " " * (n - i)
        stars = "* " * i
        print(spaces + stars)

def diamond(n: int):
    """Full diamond pattern"""
    # Upper half
    for i in range(1, n + 1):
        print(" " * (n - i) + "* " * i)
    # Lower half
    for i in range(n - 1, 0, -1):
        print(" " * (n - i) + "* " * i)

def number_pyramid(n: int):
    """
        1
       1 2
      1 2 3
     1 2 3 4
    1 2 3 4 5
    """
    for i in range(1, n + 1):
        spaces = " " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(spaces + nums)

def alphabet_triangle(n: int):
    """
    A
    B B
    C C C
    D D D D
    """
    for i in range(n):
        ch = chr(ord('A') + i)
        print(f"{ch} " * (i + 1))

def right_aligned_numbers(n: int):
    """
            1
          1 2
        1 2 3
      1 2 3 4
    1 2 3 4 5
    """
    for i in range(1, n + 1):
        spaces = "  " * (n - i)
        nums = " ".join(str(j) for j in range(1, i + 1))
        print(spaces + nums)

def floyd_triangle(n: int):
    """
    1
    2 3
    4 5 6
    7 8 9 10
    """
    num = 1
    for i in range(1, n + 1):
        row = []
        for _ in range(i):
            row.append(str(num))
            num += 1
        print(" ".join(row))

def butterfly(n: int):
    """Butterfly pattern — left side mirrors right side"""
    # Upper half
    for i in range(1, n + 1):
        left = "* " * i
        middle = "  " * (n - i)
        right = "* " * i
        print(left + middle + right)
    # Lower half
    for i in range(n, 0, -1):
        left = "* " * i
        middle = "  " * (n - i)
        right = "* " * i
        print(left + middle + right)

def hollow_rectangle(rows: int, cols: int):
    """Print a hollow rectangle"""
    for i in range(rows):
        for j in range(cols):
            if i == 0 or i == rows - 1 or j == 0 or j == cols - 1:
                print("*", end=" ")
            else:
                print(" ", end=" ")
        print()

if __name__ == "__main__":
    n = 5

    print("=== Square Pattern ===")
    square_pattern(n)

    print("\n=== Right Triangle Stars ===")
    right_triangle_stars(n)

    print("\n=== Right Triangle Numbers ===")
    right_triangle_numbers(n)

    print("\n=== Inverted Triangle ===")
    inverted_triangle(n)

    print("\n=== Pyramid ===")
    pyramid(n)

    print("\n=== Diamond ===")
    diamond(n)

    print("\n=== Number Pyramid ===")
    number_pyramid(n)

    print("\n=== Alphabet Triangle ===")
    alphabet_triangle(n)

    print("\n=== Right Aligned Numbers ===")
    right_aligned_numbers(n)

    print("\n=== Floyd's Triangle ===")
    floyd_triangle(n)

    print("\n=== Butterfly ===")
    butterfly(4)

    print("\n=== Hollow Rectangle 4x6 ===")
    hollow_rectangle(4, 6)

    # Python one-liners for patterns (Pythonic way)
    print("\n=== Pythonic Patterns ===")
    print("Triangle:")
    print("\n".join("*" * i for i in range(1, 6)))

    print("\nPyramid:")
    print("\n".join(("*" * (2*i-1)).center(9) for i in range(1, 6)))
