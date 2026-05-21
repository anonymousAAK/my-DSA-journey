# Week 2 — Practice Problems

Topics covered this week: if/else branching, ternary operator, while loops, do-while loops, basic control flow.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Power of Two | Easy | Conditionals / Loops | https://leetcode.com/problems/power-of-two/ | Google, Amazon, Apple |
| 2 | Power of Three | Easy | Loops | https://leetcode.com/problems/power-of-three/ | Google, Microsoft, Common |
| 3 | Climbing Stairs | Easy | Iterative DP | https://leetcode.com/problems/climbing-stairs/ | Amazon, Apple, Google, Adobe |
| 4 | Excel Sheet Column Number | Easy | Loop + Math | https://leetcode.com/problems/excel-sheet-column-number/ | Amazon, Microsoft, Common |
| 5 | Add Digits | Easy | Repeated reduction | https://leetcode.com/problems/add-digits/ | Common |
| 6 | Happy Number | Easy | Loop with cycle detection | https://leetcode.com/problems/happy-number/ | Google, Amazon, Microsoft |
| 7 | Sum of Digits in Base K | Easy | Base conversion loop | https://leetcode.com/problems/sum-of-digits-in-base-k/ | Common |
| 8 | Count Primes | Medium | Loops / Sieve | https://leetcode.com/problems/count-primes/ | Amazon, Microsoft, Google |
| 9 | Ugly Number | Easy | While loop with division | https://leetcode.com/problems/ugly-number/ | Common |

## Stretch Problems

Bonus problems for deeper practice:

- [Perfect Number](https://leetcode.com/problems/perfect-number/) — divisor enumeration with `i*i <= n` trick.
- [Self Dividing Numbers](https://leetcode.com/problems/self-dividing-numbers/) — combine digit loop with condition.
- [Ugly Number II](https://leetcode.com/problems/ugly-number-ii/) — bridges to DP later.

## Patterns to Master This Week

- While-loop with termination invariant: shrink `n` each iteration. Pitfall: infinite loops if you forget to mutate the loop variable.
- Ternary `cond ? a : b` for compact branching: keeps code readable but avoid nesting more than 2 deep.
- Cycle detection by visited-set or Floyd's tortoise/hare for `O(1)` space — common pitfall: forgetting that 1 is a base/terminating value.
