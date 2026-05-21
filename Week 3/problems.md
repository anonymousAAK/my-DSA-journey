# Week 3 — Practice Problems

Topics covered this week: for loops, nested loops, bitwise operators (AND/OR/XOR/shift), Fibonacci sequence, prime checks.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Fibonacci Number | Easy | Iterative Fibonacci | https://leetcode.com/problems/fibonacci-number/ | Common |
| 2 | N-th Tribonacci Number | Easy | Sliding sum | https://leetcode.com/problems/n-th-tribonacci-number/ | Common |
| 3 | Counting Bits | Easy | Bitwise / DP | https://leetcode.com/problems/counting-bits/ | Amazon, Apple, Google |
| 4 | Single Number | Easy | XOR trick | https://leetcode.com/problems/single-number/ | Google, Amazon, Microsoft |
| 5 | Hamming Distance | Easy | XOR + popcount | https://leetcode.com/problems/hamming-distance/ | Facebook, Google, Common |
| 6 | Power of Four | Easy | Bitmask | https://leetcode.com/problems/power-of-four/ | Amazon, Apple, Common |
| 7 | Reverse Bits | Easy | Bit shift loop | https://leetcode.com/problems/reverse-bits/ | Apple, Amazon, Microsoft |
| 8 | Missing Number | Easy | XOR / Sum | https://leetcode.com/problems/missing-number/ | Microsoft, Amazon, Apple |
| 9 | Single Number II | Medium | Bit counting | https://leetcode.com/problems/single-number-ii/ | Common |
| 10 | Sum of Two Integers | Medium | XOR + carry | https://leetcode.com/problems/sum-of-two-integers/ | Common |

## Stretch Problems

Bonus problems for deeper practice:

- [Bitwise AND of Numbers Range](https://leetcode.com/problems/bitwise-and-of-numbers-range/) — clever shift-until-equal pattern.
- [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) — revisit using iterative Fibonacci style.
- [Maximum XOR of Two Numbers in an Array](https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/) — preview of trie-bit problems.

## Patterns to Master This Week

- XOR self-cancellation (`a ^ a = 0`, `a ^ 0 = a`): O(n) time / O(1) space for "single number" problems. Pitfall: only works for exact pairs.
- `n & (n-1)` to drop the lowest set bit — fundamental for popcount. Pitfall: works in `O(set-bits)` not `O(log n)`.
- Iterative Fibonacci in O(1) memory using two rolling variables. Pitfall: integer overflow past F(46).
