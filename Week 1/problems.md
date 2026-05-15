# Week 1 — Practice Problems

Topics covered this week: Java fundamentals, input/output, primitive datatypes, variables, basic arithmetic, type casting.

## Curated Problems

| # | Problem | Difficulty | Topic | Link |
|---|---------|------------|-------|------|
| 1 | Two Sum | Easy | Array / Hashing | https://leetcode.com/problems/two-sum/ |
| 2 | Palindrome Number | Easy | Math / Digits | https://leetcode.com/problems/palindrome-number/ |
| 3 | Reverse Integer | Easy | Math / Overflow | https://leetcode.com/problems/reverse-integer/ |
| 4 | Fizz Buzz | Easy | Conditionals | https://leetcode.com/problems/fizz-buzz/ |
| 5 | Add Digits | Easy | Math / Digit manipulation | https://leetcode.com/problems/add-digits/ |
| 6 | Plus One | Easy | Array / Math | https://leetcode.com/problems/plus-one/ |
| 7 | Number of 1 Bits | Easy | Bit basics (preview) | https://leetcode.com/problems/number-of-1-bits/ |
| 8 | Running Sum of 1d Array | Easy | Array iteration | https://leetcode.com/problems/running-sum-of-1d-array/ |

## Stretch Problems

Bonus problems for deeper practice:

- [Excel Sheet Column Number](https://leetcode.com/problems/excel-sheet-column-number/) — builds confidence parsing characters and using simple loops.
- [Sqrt(x)](https://leetcode.com/problems/sqrtx/) — teaches integer math and overflow awareness.
- [Convert Integer to Roman](https://leetcode.com/problems/integer-to-roman/) — practice with conditionals and lookup tables.

## Patterns to Master This Week

- I/O with `Scanner` / `BufferedReader`: when speed matters prefer `BufferedReader`; complexity is O(n) for reads. Common pitfall: forgetting to close streams or mixing `nextInt()` with `nextLine()`.
- Primitive type ranges & casting: `int` overflows at ~2.1B — promote to `long` before multiplying. Pitfall: silent overflow producing wrong answers.
- Digit extraction loop (`n % 10`, `n /= 10`): O(log10 n). Pitfall: handle `n == 0` and negative numbers explicitly.
