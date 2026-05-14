"""
WEEK 1 — Python Fundamentals
Equivalent to Java Week 1: hello world, variables, data types, operators, input/output.

Python is dynamically typed — no need to declare variable types.
Python uses indentation instead of braces {} for blocks.
"""

# --- Hello World ---
print("Hello, World!")

# --- Variables (no type declaration needed) ---
name = "Alice"           # str
age = 25                 # int
height = 5.9             # float
is_student = True        # bool
grade = 'A'              # str (Python has no char type)

print(f"Name: {name}, Age: {age}, Height: {height}, Student: {is_student}")

# --- Data Types ---
# Python's basic types: int (arbitrary precision!), float (64-bit), str, bool, None
# Unlike Java: no byte, short, long — int handles ALL integer sizes
# Unlike Java: strings are immutable sequences of characters (no char type)

print(f"\nType of 42:        {type(42)}")        # <class 'int'>
print(f"Type of 3.14:      {type(3.14)}")        # <class 'float'>
print(f"Type of 'hello':   {type('hello')}")     # <class 'str'>
print(f"Type of True:      {type(True)}")        # <class 'bool'>
print(f"Type of None:      {type(None)}")        # <class 'NoneType'>

# Big integers — Python handles them natively (no overflow!)
big = 2 ** 100
print(f"\n2^100 = {big}")  # Works! Java would overflow with int/long.

# --- Type Casting ---
x = int(3.7)        # 3 (truncates, not rounds)
y = float(5)         # 5.0
z = str(42)          # "42"
w = int("123")       # 123
print(f"\nint(3.7) = {x}, float(5) = {y}, str(42) = '{z}', int('123') = {w}")

# --- Arithmetic Operators ---
a, b = 17, 5
print(f"\n--- Arithmetic ({a} and {b}) ---")
print(f"a + b  = {a + b}")     # 22
print(f"a - b  = {a - b}")     # 12
print(f"a * b  = {a * b}")     # 85
print(f"a / b  = {a / b}")     # 3.4  (true division — always float!)
print(f"a // b = {a // b}")    # 3    (floor division — integer result)
print(f"a % b  = {a % b}")     # 2    (modulo)
print(f"a ** b = {a ** b}")    # 1419857 (power — no Math.pow needed)

# --- Comparison & Logical Operators ---
print(f"\n--- Comparison ---")
print(f"5 == 5: {5 == 5}")     # True
print(f"5 != 3: {5 != 3}")     # True
print(f"5 > 3:  {5 > 3}")      # True
print(f"5 <= 5: {5 <= 5}")     # True

print(f"\n--- Logical ---")
print(f"True and False: {True and False}")  # False
print(f"True or False:  {True or False}")   # True
print(f"not True:       {not True}")        # False

# --- User Input ---
# In Python, input() always returns a string. Cast to int/float as needed.
try:
    user_input = input("\nEnter your name: ")
    print(f"Hello, {user_input}!")

    num = int(input("Enter a number: "))
    print(f"Double of {num} is {num * 2}")
except EOFError:
    print("(No input available — running non-interactively)")

# --- String Operations ---
s = "Hello, Python!"
print(f"\n--- String Operations ---")
print(f"Length:         {len(s)}")
print(f"Upper:          {s.upper()}")
print(f"Lower:          {s.lower()}")
print(f"Slice [0:5]:    {s[0:5]}")       # "Hello"
print(f"Reverse [::-1]: {s[::-1]}")       # "!nohtyP ,olleH"
print(f"Split:          {s.split(', ')}") # ["Hello", "Python!"]
print(f"Replace:        {s.replace('Python', 'World')}")
print(f"f-string:       {f'{name} is {age} years old'}")

# --- Collections Preview (Python's built-in data structures) ---
my_list = [1, 2, 3, 4, 5]        # mutable ordered sequence (like ArrayList)
my_tuple = (1, 2, 3)              # immutable ordered sequence
my_dict = {"a": 1, "b": 2}       # hash map (like HashMap)
my_set = {1, 2, 3, 3, 3}         # unique elements (like HashSet)
print(f"\nList:  {my_list}")
print(f"Tuple: {my_tuple}")
print(f"Dict:  {my_dict}")
print(f"Set:   {my_set}")  # {1, 2, 3}
