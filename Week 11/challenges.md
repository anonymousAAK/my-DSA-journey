# Week 11 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Reverse Nodes in K-Group (LC 25)

**Spec**:
Build a singly linked list from a sequence of integers. Given `k`, reverse every contiguous group of `k` nodes. If a final group has fewer than `k` nodes, leave it as-is. Modify pointers in place; do not allocate new nodes. Print the resulting list.

**Constraints**:
- List length: `1 <= n <= 10^6`
- `1 <= k <= n`
- Time: O(n)
- Memory: O(1) extra

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `list=1 2 3 4 5 k=2` | `2 1 4 3 5` |
| `list=1 2 3 4 5 k=3` | `3 2 1 4 5` |
| `list=1 2 3 4 5 k=1` | `1 2 3 4 5` |
| `list=1 2 3 4 5 k=5` | `5 4 3 2 1` |
| `list=1 k=1` | `1` |

**Stretch**: Reverse only the groups whose index is even (1st group unchanged, 2nd reversed, 3rd unchanged, ...).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Detect Cycle Start Node (Floyd's Tortoise and Hare)

**Spec**:
Build a list with a possible cycle (input format: `n m`, then `n` values for the nodes, then `m` = the index where the tail links to, or `-1` if no cycle). Detect whether a cycle exists; if yes, print the value of the node where the cycle begins. Required: O(1) extra memory — use Floyd's algorithm (slow/fast pointer convergence, then reset slow to head).

**Constraints**:
- List length: `1 <= n <= 10^6`
- Time: O(n)
- Memory: O(1)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `n=5 m=2 / 1 2 3 4 5` | cycle starts at node with value `3` |
| `n=3 m=0 / 1 2 3` | `1` |
| `n=1 m=-1 / 1` | `NO_CYCLE` |
| `n=4 m=-1 / 1 2 3 4` | `NO_CYCLE` |

**Stretch**: Also report the cycle's length.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: LRU Cache From Scratch (No Library Containers)

**Spec**:
Implement an LRU cache with capacity `C`. Operations: `put(key, value)` and `get(key)` (returns `-1` if absent). Each op must be O(1) amortized. You may not use a hashmap-of-doubly-linked-list-from-the-standard-library — build the doubly linked list yourself, and you may use only a *plain* hashmap (with no LRU semantics).

Read a sequence of operations from stdin and print the output of each `get`.

**Constraints**:
- `1 <= C <= 10^5`
- Up to `10^6` ops
- Time: O(1) per op
- Memory: O(C)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `C=2 / put 1 1 / put 2 2 / get 1 / put 3 3 / get 2 / put 4 4 / get 1 / get 3 / get 4` | `1 -1 -1 3 4` |
| `C=1 / put 1 1 / put 1 2 / get 1` | `2` |
| `C=2 / get 1` | `-1` |

**Stretch**: Implement LFU (least-frequently-used) eviction with O(1) ops — significantly harder.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Merge K Sorted Linked Lists

**Spec**:
Read `k`, then `k` sorted singly linked lists (one per line, space-separated values). Merge into one sorted list and print it. Required: O(N log k) where N = total nodes. Use a min-heap of size `k` holding the current head of each list — not pairwise merging, which is O(N k).

**Constraints**:
- `1 <= k <= 10^4`, total nodes up to `10^6`
- Time: O(N log k)
- Memory: O(k)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `k=3 / 1 4 5 / 1 3 4 / 2 6` | `1 1 2 3 4 4 5 6` |
| `k=1 / 1 2 3` | `1 2 3` |
| `k=2 / (empty) / 0` | `0` |
| `k=3 / (empty) / (empty) / (empty)` | (empty) |

**Stretch**: Solve via divide-and-conquer (pairwise merge in tournament style) — same O(N log k) but different constants. Compare.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
