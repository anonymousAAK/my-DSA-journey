# Week 2 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which conditional pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given a year, decide if it is a leap year. A year is a leap year if it is divisible by 4, except centuries which must be divisible by 400.
Pattern: ______
Why: ______

### 2. Read an integer score 0–100 and print the letter grade: A (>=90), B (>=80), C (>=70), D (>=60), F otherwise.
Pattern: ______
Why: ______

### 3. Read three integers representing the sides of a possible triangle. Print "equilateral", "isosceles", "scalene", or "not a triangle".
Pattern: ______
Why: ______

### 4. Read a single character. Print "vowel" if it is one of a/e/i/o/u (any case), "consonant" if it is any other letter, "digit" if it is 0–9, "other" otherwise.
Pattern: ______
Why: ______

### 5. Given hour (0–23) and minute (0–59), decide whether a shop is open. Hours: Mon–Fri 9:00–17:00, Sat 10:00–14:00, closed Sun. Assume you also have a `dayOfWeek` int.
Pattern: ______
Why: ______

### 6. Compute the absolute value of an integer without using `Math.abs`.
Pattern: ______
Why: ______

### 7. Given a temperature in Celsius and a wind speed, print one of: "freezing", "cold", "mild", "hot". The breakpoints depend on wind speed (wind chill table).
Pattern: ______
Why: ______

### 8. Distractor: Read 10 numbers and print the largest. (Why is this Week 3, not Week 2?)
Pattern: ______
Why: ______

### 9. Given three numbers, print them sorted in ascending order on one line. You may compare and swap, but no arrays or loops.
Pattern: ______
Why: ______

### 10. Given an integer between 1 and 7, print the corresponding day name ("Monday"..."Sunday"). Compare a `switch` vs `if-else` chain — which is clearer?
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Nested `if` on modulo. **Why**: `y%400==0 || (y%4==0 && y%100!=0)` — short-circuit logic.
2. **Pattern**: Cascading `if-else if` ladder. **Why**: ordered thresholds, exactly one branch fires.
3. **Pattern**: Validity guard + categorical `if`. **Why**: first reject invalid triangles, then classify by equality count.
4. **Pattern**: Character classification — `switch` or `if` chain. **Why**: discrete categories on `char` value; `Character.isDigit` etc. help.
5. **Pattern**: Combined boolean expression. **Why**: condition on (day, hour) pair; build the open-window predicate.
6. **Pattern**: Single `if` returning negation. **Why**: `x<0 ? -x : x` — ternary or one-armed `if`.
7. **Pattern**: 2-D decision table via nested `if`. **Why**: two variables drive the category — outer switches on wind, inner on temperature.
8. **Pattern**: Distractor — requires a loop. **Why**: "read 10 numbers" implies iteration, which is Week 3. Conditionals alone can't generalize.
9. **Pattern**: Pairwise compare-and-swap. **Why**: 3 comparisons fully sort 3 elements — classic sorting network of size 3.
10. **Pattern**: `switch` on small integer. **Why**: dense 1–7 case set — `switch` is the canonical fit; `if` chain works but is noisier.

</details>
