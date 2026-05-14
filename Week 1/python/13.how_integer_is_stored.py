"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: How Integers Are Stored in Memory
File: 13.how_integer_is_stored.py

CONCEPT:
Java stores `int` as a fixed 32-bit two's-complement value. Python's `int`
is conceptually a sign + an arbitrary-length sequence of "digits" (CPython
uses a 30-bit base internally). Despite this difference, Python lets you
INSPECT and SIMULATE two's-complement representations using `bin()`,
`int.to_bytes()`, and bit-mask tricks.

KEY POINTS:
- Python ints have arbitrary precision -> NO overflow.
- For positive n: `bin(n)` -> "0b..." binary string.
- For negative n: `bin(-4)` returns "-0b100" (sign-magnitude).
- To see the 32-bit two's-complement form: mask with `0xFFFFFFFF`.
- `int.to_bytes(length, byteorder, signed=True)` returns raw bytes.
- `int.from_bytes(b, byteorder, signed=True)` reads them back.

SYNTAX:
bin(4)                 # '0b100'
bin(-4 & 0xFFFFFFFF)    # '0b11111111111111111111111111111100'  (32-bit two's-complement of -4)
(-4).to_bytes(4, 'big', signed=True)  # b'\\xff\\xff\\xff\\xfc'

DRY RUN — two's-complement of -4 in 32 bits:
1. abs(-4) = 4 -> 0000_0000_0000_0000_0000_0000_0000_0100
2. invert  -> 1111_1111_1111_1111_1111_1111_1111_1011  (1's complement)
3. add 1   -> 1111_1111_1111_1111_1111_1111_1111_1100  (2's complement)
   -> hex 0xFFFFFFFC

COMPLEXITY: O(width) for bit/byte conversions.
"""


def to_twos_complement(n: int, bits: int = 32) -> str:
    """Return the `bits`-wide two's-complement binary string for n."""
    mask = (1 << bits) - 1                  # e.g. 0xFFFFFFFF for 32 bits
    val = n & mask                           # negative numbers wrap correctly
    return format(val, f"0{bits}b")          # zero-padded binary string


def main() -> None:
    print("=== Positive number: 4 ===")
    print(f"bin(4)            = {bin(4)}")
    print(f"32-bit form       = {to_twos_complement(4)}")
    print(f"bytes (4 BE,signed)= {(4).to_bytes(4, 'big', signed=True).hex()}")

    print("\n=== Negative number: -4 ===")
    print(f"bin(-4)           = {bin(-4)}                  (Python sign-magnitude form)")
    print(f"32-bit two's comp = {to_twos_complement(-4)}")
    print(f"bytes (4 BE,signed)= {(-4).to_bytes(4, 'big', signed=True).hex()}")

    print("\n=== Step-by-step derivation of -4 ===")
    pos_bin = to_twos_complement(4)
    print(f"step 1) +4 binary       = {pos_bin}")
    inverted = "".join("1" if b == "0" else "0" for b in pos_bin)
    print(f"step 2) invert all bits = {inverted}")
    plus_one = format(int(inverted, 2) + 1, "032b")
    print(f"step 3) add 1            = {plus_one}")
    print(f"matches to_twos_complement(-4)? {plus_one == to_twos_complement(-4)}")

    print("\n=== Python has NO int overflow ===")
    huge = 1 << 200
    print(f"1 << 200 = {huge}")
    print(f"bit length = {huge.bit_length()}")


if __name__ == "__main__":
    main()


# NOTES:
# - Java's int silently wraps around on overflow (`Integer.MAX_VALUE + 1` -> MIN).
#   Python ints simply grow as needed.
# - To DEMAND fixed-width arithmetic in Python, use `numpy.int32`, `ctypes.c_int`,
#   or apply masks manually as shown above.
# - Bit operators `& | ^ << >> ~` work on Python ints just like in Java.
