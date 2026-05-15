# Week 4 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which printing/loop-nesting pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given `n`, print a right-aligned triangle of `#` with height `n`. Row i (1-indexed) has `i` characters preceded by `n-i` spaces.
Pattern: ______
Why: ______

### 2. Print an `n × n` hollow square of `*` (only the border filled, interior spaces).
Pattern: ______
Why: ______

### 3. Print a centered diamond of `*` with width `2n-1`. n up to 50.
Pattern: ______
Why: ______

### 4. Print Pascal's triangle up to row `n` (n ≤ 20), each row centered.
Pattern: ______
Why: ______

### 5. Given `n`, print a triangle where row `i` contains the numbers `1 2 ... i` separated by spaces.
Pattern: ______
Why: ______

### 6. Print a "Floyd's triangle" — successive integers in row major form, row `i` containing `i` numbers.
Pattern: ______
Why: ______

### 7. Print a multiplication table from 1×1 up to n×n, padded so columns line up.
Pattern: ______
Why: ______

### 8. Distractor: Given a 2D character grid stored in memory, print it. (Why is this *not* a Week 4 pattern drill?)
Pattern: ______
Why: ______

### 9. Print an inverted triangle of digits where row `i` (starting from 1 at the top) has `n-i+1` columns showing `i, i+1, ..., i+(n-i)`.
Pattern: ______
Why: ______

### 10. Print a "butterfly" pattern of `*`: two right triangles back-to-back forming an hourglass, with width `n` at the widest point.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Nested loops — outer over rows, two inner over spaces then chars. **Why**: classic two-phase row construction.
2. **Pattern**: Border condition inside nested loop. **Why**: print `*` iff `i==1 || i==n || j==1 || j==n`, else space.
3. **Pattern**: Two stacked triangles (upper widens, lower narrows). **Why**: split into two loops, share the spaces+stars formula.
4. **Pattern**: Nested loop with running binomial coefficient `C(i,j) = C(i,j-1)*(i-j+1)/j`. **Why**: avoids recomputing factorials; centering via leading spaces.
5. **Pattern**: Nested loop — outer rows, inner prints `1..i`. **Why**: direct mapping from row index to column count.
6. **Pattern**: Nested loop with an external running counter. **Why**: counter increments across rows, decoupled from `i, j`.
7. **Pattern**: Nested loop + `printf("%4d", i*j)`. **Why**: column alignment is just format-width control.
8. **Pattern**: Distractor — Week 4 is about *generating* patterns with loops, not iterating stored 2D data (Week 10 / matrix traversal).
9. **Pattern**: Nested loop with arithmetic on row index. **Why**: each row prints `n-i+1` numbers starting at `i`; trim count + base value.
10. **Pattern**: Two-phase nested loops (top narrows then bottom widens). **Why**: hourglass = inverted triangle stacked on upright triangle.

</details>
