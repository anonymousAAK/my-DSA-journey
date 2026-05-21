# Week 12 — Practice Problems

Topics covered this week: stacks (array/LL-backed), push/pop/peek, monotonic stacks, expression evaluation, parenthesis matching.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Valid Parentheses | Easy | Bracket matching | https://leetcode.com/problems/valid-parentheses/ | Amazon, Meta, Microsoft, Bloomberg |
| 2 | Min Stack | Medium | Auxiliary stack | https://leetcode.com/problems/min-stack/ | Amazon, Microsoft, Bloomberg, Google |
| 3 | Evaluate Reverse Polish Notation | Medium | Postfix eval | https://leetcode.com/problems/evaluate-reverse-polish-notation/ | Amazon, LinkedIn, Microsoft |
| 4 | Daily Temperatures | Medium | Monotonic stack | https://leetcode.com/problems/daily-temperatures/ | Amazon, Meta, Google |
| 5 | Next Greater Element I | Easy | Monotonic stack | https://leetcode.com/problems/next-greater-element-i/ | Amazon, Bloomberg, Common |
| 6 | Next Greater Element II | Medium | Circular monotonic stack | https://leetcode.com/problems/next-greater-element-ii/ | Common |
| 7 | Largest Rectangle in Histogram | Hard | Monotonic stack | https://leetcode.com/problems/largest-rectangle-in-histogram/ | Amazon, Meta, Google, Microsoft |
| 8 | Asteroid Collision | Medium | Stack simulation | https://leetcode.com/problems/asteroid-collision/ | Amazon, Google, Uber |
| 9 | Decode String | Medium | Stack of contexts | https://leetcode.com/problems/decode-string/ | Amazon, Meta, Google, Bloomberg |
| 10 | Simplify Path | Medium | Stack of tokens | https://leetcode.com/problems/simplify-path/ | Meta, Amazon, Microsoft |
| 11 | Basic Calculator II | Medium | Stack-based parser | https://leetcode.com/problems/basic-calculator-ii/ | Amazon, Microsoft, Google |

## Stretch Problems

Bonus problems for deeper practice:

- [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) — monotonic stack approach.
- [Maximal Rectangle](https://leetcode.com/problems/maximal-rectangle/) — histogram extension on a 2D grid.
- [Remove K Digits](https://leetcode.com/problems/remove-k-digits/) — monotonic-stack greedy.

## Patterns to Master This Week

- Monotonic stack: keep elements in increasing/decreasing order, pop while invariant breaks. O(n) amortized. Pitfall: pushing indices vs values.
- Two-stack min: store minimum-so-far alongside the value. Pitfall: forgetting to pop both stacks together.
- Stack-based parser: defer operators by precedence; flush on closing token. Pitfall: handling unary minus and whitespace.
