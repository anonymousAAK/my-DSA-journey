# Week 13 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Sliding Window Maximum via Monotonic Deque

**Spec**:
Read `n`, `k`, and `n` integers. For every window of size `k`, print the maximum. Required complexity O(n) using a monotonic-decreasing deque of indices. The O(n log k) heap approach is acceptable for stretch credit only; the O(n k) brute force is forbidden.

**Constraints**:
- `1 <= k <= n <= 10^6`
- Time: O(n)
- Memory: O(k)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=8 k=3 / 1 3 -1 -3 5 3 6 7` | `3 3 5 5 6 7` |
| `n=5 k=1 / 5 4 3 2 1` | `5 4 3 2 1` |
| `n=4 k=4 / 1 2 3 4` | `4` |
| `n=5 k=2 / 7 2 4 6 5` | `7 4 6 6` |

**Stretch**: Sliding window median (harder — needs two heaps with lazy deletion).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Queue via Two Stacks With Amortized O(1) Ops

**Spec**:
Implement a queue using **only two stacks**. Operations: `enqueue x` and `dequeue` (prints the dequeued value). Each op must run in O(1) amortized. Prove the amortization in your journal: each element is pushed at most twice and popped at most twice.

**Constraints**:
- Up to `10^6` ops
- Time: amortized O(1) per op
- Memory: O(elements in queue)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `enq 1 / enq 2 / deq / enq 3 / deq / deq` | `1 2 3` |
| `enq 1 / deq / deq` | `1 EMPTY` |
| `enq 5 / enq 6 / enq 7 / deq / deq / deq` | `5 6 7` |

**Stretch**: Same problem but supporting `front` (peek without dequeue) in O(1) worst case.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Circular Buffer With Fixed Capacity

**Spec**:
Implement a ring buffer holding up to `C` integers. Operations:
- `push x`: if full, overwrite the oldest.
- `peekOldest`: print the oldest.
- `peekNewest`: print the newest.
- `dump`: print all elements from oldest to newest.

Use an array of size `C` with two indices (head/tail) and a count, all O(1). No `LinkedList`, no shifting on overflow.

**Constraints**:
- `1 <= C <= 10^6`, up to `10^6` ops
- Time: O(1) per op (except `dump` which is O(C))
- Memory: O(C)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `C=3 / push 1 / push 2 / push 3 / dump / push 4 / dump / peekOldest / peekNewest` | `1 2 3` / `2 3 4` / `2` / `4` |
| `C=1 / push 5 / push 6 / dump` | `6` |

**Stretch**: Add `popOldest` (FIFO behavior) and a "growable" mode that doubles capacity when full.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: First Non-Repeating Character in a Stream

**Spec**:
Process a stream of characters one at a time. After each character, print the first character in the stream so far that has appeared exactly once. If no such character, print `#`. Required: O(1) per character. Technique: queue of candidates + counts. On each new char, increment its count, push to queue, then advance the queue's head past any character whose count is now > 1.

**Constraints**:
- Stream length up to `10^6`, lowercase ASCII
- Time: O(1) amortized per char
- Memory: O(alphabet size)

**Test inputs**:
| Input | Expected output (one per char) |
|-------|--------------------------------|
| `aabc` | `a # b b` |
| `geeksforgeeks` | `g g g k k e e e e g g e e` (verify by hand) |
| `aaaa` | `a # # #` |
| `abc` | `a a a` |

**Stretch**: Maintain the *k*-th non-repeating character for arbitrary `k`.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
