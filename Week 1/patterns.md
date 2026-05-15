# Week 1 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which primitive/pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. A vending machine accepts a single integer denoting cents. Print the value in dollars and cents formatted as `$D.CC`. Input fits in a 32-bit int; one query.
Pattern: ______
Why: ______

### 2. Given two integer variables `a` and `b`, swap them so that `a` ends up holding the old `b` and vice versa. You may use one extra variable.
Pattern: ______
Why: ______

### 3. Read three doubles representing the sides of a triangle and print the perimeter rounded to two decimal places.
Pattern: ______
Why: ______

### 4. Given a single character, print its ASCII code, and given an integer 0..127, print the corresponding character.
Pattern: ______
Why: ______

### 5. A program receives a `long` storing nanoseconds. Convert it into hours, minutes, seconds, and remaining nanoseconds and print each on its own line.
Pattern: ______
Why: ______

### 6. Read a `float` weight in pounds and convert to kilograms (1 lb = 0.453592 kg). Print with 3 decimals.
Pattern: ______
Why: ______

### 7. You are given a `byte` value that should hold the number `200`. Explain in code what happens when you assign it and how you would store the value losslessly.
Pattern: ______
Why: ______

### 8. The user types one integer per line until EOF. Print the sum. (Distractor: looks like loops, but at this point you're only allowed primitives + `Scanner`.)
Pattern: ______
Why: ______

### 9. Given two ints `a` and `b`, print whichever is larger without using `Math.max` or any branching keyword — only arithmetic and comparison operators.
Pattern: ______
Why: ______

### 10. A bank stores account balances as cents in a `long`. Read two balances and print their sum, but warn if the sum would overflow a signed 64-bit integer.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Integer division + modulo. **Why**: `cents/100` gives dollars, `cents%100` gives remainder cents — fundamental decomposition primitive.
2. **Pattern**: Variable assignment with temp (or arithmetic/XOR swap). **Why**: classic three-statement primitive — `t=a; a=b; b=t;`.
3. **Pattern**: Read + arithmetic + `printf("%.2f", ...)`. **Why**: pure I/O + arithmetic, formatting is the only twist.
4. **Pattern**: Typecasting between `int` and `char`. **Why**: Java widens/narrows automatically; this exercises char ↔ int conversion.
5. **Pattern**: Repeated div/mod on a `long`. **Why**: unit conversion is a chain of `quotient, remainder` splits.
6. **Pattern**: Floating-point arithmetic + `printf` formatting. **Why**: straightforward multiply + format.
7. **Pattern**: Typecasting + range awareness. **Why**: `byte` is signed −128..127, so 200 overflows; need `short`/`int` or `(byte)(200-256)` interpretation.
8. **Pattern**: Distractor — you cannot solve this with Week 1 primitives. **Why**: requires a loop, which is Week 3. Recognizing the gap is the lesson.
9. **Pattern**: Arithmetic max trick. **Why**: `(a+b + Math.abs(a-b))/2` — but `Math.abs` is allowed. Alternative: `a - ((a-b) & ((a-b)>>31))` is bitwise (Week 3). At Week 1, the clean answer is "this needs an `if`, which we don't have yet".
10. **Pattern**: Overflow detection via comparison before addition. **Why**: check `Long.MAX_VALUE - a < b` before summing — exercises awareness of integer limits.

</details>
