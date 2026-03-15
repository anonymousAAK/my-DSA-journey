"""
WEEK 3 — Python: Advanced Loops & Number Theory Basics
Covers: Fibonacci, primes, binary/decimal conversion, bitwise operators.
Equivalent to Java Week 3.
"""

# --- Fibonacci ---
def fibonacci(n: int) -> int:
    """
    Return the Nth Fibonacci number (0-indexed).
    Time: O(n), Space: O(1)
    """
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

print("--- Fibonacci ---")
print("First 10:", [fibonacci(i) for i in range(10)])

# --- Prime Numbers ---
def is_prime(n: int) -> bool:
    """Check if n is prime. Time: O(sqrt(n))"""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def sieve_of_eratosthenes(limit: int) -> list[int]:
    """
    Find all primes up to limit.
    Time: O(n log log n), Space: O(n)
    Much faster than checking each number individually.
    """
    if limit < 2:
        return []
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, limit + 1, i):
                is_p[j] = False
    return [i for i, v in enumerate(is_p) if v]

print("\n--- Primes ---")
print("is_prime(17):", is_prime(17))
print("is_prime(20):", is_prime(20))
print("Primes up to 50:", sieve_of_eratosthenes(50))

# --- Reverse a Number ---
def reverse_number(n: int) -> int:
    """Reverse digits of n. Time: O(d), Space: O(1)"""
    neg = n < 0
    n = abs(n)
    rev = 0
    while n > 0:
        rev = rev * 10 + n % 10
        n //= 10
    return -rev if neg else rev

print("\n--- Reverse Number ---")
for num in [1234, -567, 1000]:
    print(f"reverse({num}) = {reverse_number(num)}")

# --- Binary ↔ Decimal ---
def decimal_to_binary(n: int) -> str:
    """Convert decimal to binary string. Time: O(log n)"""
    if n == 0:
        return "0"
    bits = []
    neg = n < 0
    n = abs(n)
    while n > 0:
        bits.append(str(n % 2))
        n //= 2
    return ("-" if neg else "") + "".join(reversed(bits))

def binary_to_decimal(s: str) -> int:
    """Convert binary string to decimal. Time: O(len(s))"""
    result = 0
    for bit in s:
        result = result * 2 + int(bit)
    return result

print("\n--- Binary Conversion ---")
for num in [0, 5, 10, 42, 255]:
    b = decimal_to_binary(num)
    back = binary_to_decimal(b)
    print(f"{num} → {b} → {back}")
    # Python also has built-in: bin(42) = '0b101010', int('101010', 2) = 42

# --- Bitwise Operators ---
print("\n--- Bitwise Operators ---")
a, b = 12, 10  # 1100, 1010
print(f"a = {a} ({bin(a)}), b = {b} ({bin(b)})")
print(f"a & b  = {a & b}  ({bin(a & b)})")   # AND: 1000 = 8
print(f"a | b  = {a | b}  ({bin(a | b)})")   # OR:  1110 = 14
print(f"a ^ b  = {a ^ b}  ({bin(a ^ b)})")   # XOR: 0110 = 6
print(f"~a     = {~a}")                        # NOT: -13
print(f"a << 2 = {a << 2}")                    # Left shift: 48
print(f"a >> 2 = {a >> 2}")                    # Right shift: 3

# Useful bit tricks
print("\n--- Bit Tricks ---")
n = 20
print(f"Check if {n} is power of 2: {n > 0 and (n & (n-1)) == 0}")
n = 16
print(f"Check if {n} is power of 2: {n > 0 and (n & (n-1)) == 0}")

# Count set bits
def count_set_bits(n: int) -> int:
    count = 0
    while n:
        n &= n - 1  # clear lowest set bit
        count += 1
    return count

print(f"Set bits in 13 (1101): {count_set_bits(13)}")  # 3
print(f"Set bits in 255 (11111111): {count_set_bits(255)}")  # 8

# --- Check Sequence (from Java Week 3) ---
def is_valley_sequence(arr: list[int]) -> bool:
    """
    Check if sequence strictly decreases then strictly increases (valley shape).
    Time: O(n), Space: O(1)
    """
    n = len(arr)
    if n < 3:
        return False
    i = 0
    # Decreasing part
    while i < n - 1 and arr[i] > arr[i + 1]:
        i += 1
    if i == 0 or i == n - 1:  # must have both parts
        return False
    # Increasing part
    while i < n - 1 and arr[i] < arr[i + 1]:
        i += 1
    return i == n - 1

print("\n--- Valley Sequence ---")
print(is_valley_sequence([5, 3, 1, 2, 4]))   # True
print(is_valley_sequence([1, 2, 3]))           # False (only increasing)
print(is_valley_sequence([3, 2, 1]))           # False (only decreasing)
