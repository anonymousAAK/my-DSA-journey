# Weekly Digest — 2026-09-14 (ISO 2026-W38)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Graph Coloring in Compilers**

A CPU has a small fixed number of registers (16 general-purpose on x86-64, 31 on ARM64). A program, after the compiler's optimization passes, has hundreds or thousands of "virtual" variables that all want to live in registers because RAM access is 100x slower. The compiler's job: assign each virtual variable to a physical register, while ensuring that two variables which need to hold distinct values at the same time aren't given the same register. When you run out of registers, "spill" some variables to the stack — accepting the slowdown.

Read it in full: [`case_studies/real_world/15_compiler_register_allocation.md`](case_studies/real_world/15_compiler_register_allocation.md)

## Pattern drill
_From Week 19 (drill #9)._

> Distractor: Given arbitrary coin denominations and a target sum, find the minimum number of coins. (Same as 8?)

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 19/patterns.md`](Week 19/patterns.md)

## Hard-mode challenge
### Challenge 3 (Week 19): Huffman Coding Build + Encode + Decode

**Spec**:
Read a string. Build a Huffman tree (greedy via min-heap), compute the canonical prefix-free code for each character, encode the string to a bit string, then decode it back. Print the encoded bit string length, the codebook, and verify decoded string equals the original.

**Constraints**:
- String length up to `10^6`, alphabet up to 256 symbols
- Time: O(L + sigma log sigma)
- Memory: O(sigma + L)

**Test inputs**:
| Input | Expected behavior |
|

Full spec: [`Week 19/challenges.md`](Week 19/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
