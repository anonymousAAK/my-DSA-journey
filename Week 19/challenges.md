# Week 19 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Job Sequencing With Deadlines and Profits

**Spec**:
Read `n` and `n` triples `(id, deadline, profit)`. Each job takes exactly 1 unit of time. Schedule a subset of jobs (each at some time slot `<=` its deadline, one job per slot) to maximize total profit. Print total profit and the schedule. Greedy: sort by profit descending; for each job, place it in the latest available slot `<=` deadline. Use a DSU/union-find on slots for O(n α(n)) instead of O(n^2) slot scanning.

**Constraints**:
- `1 <= n <= 10^5`, deadlines up to `10^5`, profits up to `10^4`
- Time: O(n α(n)) with DSU; O(n^2) acceptable for partial credit
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=4 / (a,4,20)(b,1,10)(c,1,40)(d,1,30)` | profit `60`, schedule `c a` |
| `n=5 / (a,2,100)(b,1,19)(c,2,27)(d,1,25)(e,3,15)` | profit `142`, schedule `a c e` |
| `n=1 / (x,1,5)` | `5`, `x` |

**Stretch**: Each job takes variable processing time `p_i` (no longer unit). Now NP-hard; design a heuristic.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Minimum Platforms (Activity Scheduling Variant)

**Spec**:
Read `n` and `n` train pairs `(arrival, departure)` (times like `HHMM`, no two trains share both arrival and departure but a train arriving at time `t` and one departing at `t` overlap in platform requirements). Compute the minimum number of platforms required so that no train waits. Greedy: sort arrivals and departures separately, sweep with two pointers.

**Constraints**:
- `1 <= n <= 10^5`, times in `[0000, 2359]`
- Time: O(n log n)
- Memory: O(n)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=6 arr=900 940 950 1100 1500 1800 dep=910 1200 1120 1130 1900 2000` | `3` |
| `n=2 arr=900 1100 dep=1000 1200` | `1` |
| `n=3 arr=900 900 900 dep=1000 1000 1000` | `3` |

**Stretch**: Also output, for each train, which platform number it uses (1-indexed, smallest available).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Huffman Coding Build + Encode + Decode

**Spec**:
Read a string. Build a Huffman tree (greedy via min-heap), compute the canonical prefix-free code for each character, encode the string to a bit string, then decode it back. Print the encoded bit string length, the codebook, and verify decoded string equals the original.

**Constraints**:
- String length up to `10^6`, alphabet up to 256 symbols
- Time: O(L + sigma log sigma)
- Memory: O(sigma + L)

**Test inputs**:
| Input | Expected behavior |
|-------|-------------------|
| `abracadabra` | codes assigned; encoded length < 11 * 8 bits |
| `aaaa` | edge case: only one distinct symbol — handle specially (assign code `0` of length 1) |
| `(empty)` | nothing to do |

**Stretch**: Output canonical Huffman codes (codes derived purely from code lengths, allowing decoder reconstruction from lengths alone).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Gas Station — Single Pass

**Spec**:
Read `n`, then `n` gas amounts, then `n` costs to travel to next station (circular). Find the starting station index from which you can complete the full loop with non-negative tank at every station; print `-1` if impossible. Required O(n) single pass: if total gas < total cost, return -1; otherwise, the unique answer is `start = i + 1` where `i` is the last station at which the running tank went negative.

**Constraints**:
- `1 <= n <= 10^6`
- Time: O(n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 gas=1 2 3 4 5 cost=3 4 5 1 2` | `3` (0-indexed) |
| `n=3 gas=2 3 4 cost=3 4 3` | `-1` |
| `n=1 gas=5 cost=4` | `0` |
| `n=1 gas=4 cost=5` | `-1` |

**Stretch**: If there's a unique solution, prove it (in your journal) and find it. If there can be multiple valid starts, report all of them.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
