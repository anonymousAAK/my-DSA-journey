"""
WEEK 2 — Python: Control Flow & Loops
Covers: if/elif/else, while loops, for loops, range(), break/continue
Equivalent to Java Week 2.
"""

# --- If / Elif / Else ---
# Python uses elif (not else if), and indentation defines blocks
x = 42
if x > 100:
    print("Big")
elif x > 10:
    print("Medium")  # this runs
else:
    print("Small")

# Ternary expression
status = "even" if x % 2 == 0 else "odd"
print(f"{x} is {status}")

# --- While Loop ---
print("\n--- While Loop: Multiplication Table ---")
n, i = 7, 1
while i <= 10:
    print(f"{n} x {i} = {n * i}")
    i += 1  # Python has no ++ operator

# --- For Loop with range() ---
# range(start, stop, step) — stop is exclusive
print("\n--- For Loop ---")
print("range(5):", list(range(5)))          # [0, 1, 2, 3, 4]
print("range(2,8):", list(range(2, 8)))     # [2, 3, 4, 5, 6, 7]
print("range(0,10,2):", list(range(0, 10, 2)))  # [0, 2, 4, 6, 8]
print("range(5,0,-1):", list(range(5, 0, -1)))  # [5, 4, 3, 2, 1]

# --- Sum of Even and Odd Digits ---
def sum_even_odd_digits(n: int) -> tuple[int, int]:
    """
    Sum even and odd digits of a number separately.
    Time: O(d) where d = number of digits
    Space: O(1)
    """
    even_sum, odd_sum = 0, 0
    n = abs(n)
    while n > 0:
        digit = n % 10
        if digit % 2 == 0:
            even_sum += digit
        else:
            odd_sum += digit
        n //= 10
    return even_sum, odd_sum

print("\n--- Sum of Even/Odd Digits ---")
for num in [1234, 9876, 555]:
    e, o = sum_even_odd_digits(num)
    print(f"{num}: even_sum={e}, odd_sum={o}")

# --- Factors of a Number ---
def factors(n: int) -> list[int]:
    """Find all factors of n. Time: O(sqrt(n))"""
    result = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            result.append(i)
            if i != n // i:
                result.append(n // i)
    return sorted(result)

print("\n--- Factors ---")
for num in [12, 28, 7]:
    print(f"Factors of {num}: {factors(num)}")

# --- Find Power: x^n ---
def power(x: int, n: int) -> int:
    """
    Compute x^n iteratively.
    Time: O(n)  — See Week 5 for O(log n) fast exponentiation
    """
    result = 1
    for _ in range(n):
        result *= x
    return result

print("\n--- Power ---")
print(f"2^10 = {power(2, 10)}")
print(f"3^5 = {power(3, 5)}")
# Python also has built-in: 2**10 = 1024

# --- Fahrenheit to Celsius Table ---
print("\n--- Fahrenheit to Celsius ---")
print(f"{'F':>5} | {'C':>8}")
print("-" * 16)
for f in range(32, 213, 20):
    c = (f - 32) * 5 / 9
    print(f"{f:>5} | {c:>8.2f}")

# --- Break and Continue ---
print("\n--- Break: first prime after 20 ---")
for n in range(21, 100):
    is_prime = n > 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            is_prime = False
            break
    if is_prime:
        print(f"First prime after 20: {n}")
        break

print("\n--- Continue: skip multiples of 3 ---")
print("Non-multiples of 3 from 1-15:", end=" ")
for i in range(1, 16):
    if i % 3 == 0:
        continue
    print(i, end=" ")
print()

# --- Python-specific: List Comprehensions (powerful shorthand for loops) ---
print("\n--- List Comprehensions ---")
squares = [x**2 for x in range(10)]
print(f"Squares: {squares}")

evens = [x for x in range(20) if x % 2 == 0]
print(f"Evens: {evens}")

# Nested comprehension: multiplication table
table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
print(f"5x5 table: {table}")
