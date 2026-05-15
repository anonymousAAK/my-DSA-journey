# Week 14 — Hard Mode Challenges

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Serialize and Deserialize a Binary Tree

**Spec**:
Design two functions: `serialize(root) -> String` and `deserialize(String) -> root`. The serialized form must be lossless and round-trippable. Choose a format (BFS with `null` markers or DFS preorder with `null` markers) and stick with it. Test: build a tree, serialize, deserialize, serialize again; the two strings must be byte-identical.

**Constraints**:
- Up to `10^5` nodes, values in `[-1000, 1000]`
- Time: O(n) each direction
- Memory: O(n)

**Test inputs**:
| Tree | Round-trip works? |
|------|-------------------|
| `1 / 2 3 / null null 4 5` (LC example) | yes |
| empty tree | yes |
| single node `[7]` | yes |
| left-only chain `1 -> 2 -> 3 -> 4 -> 5` | yes |
| right-only chain | yes |

**Stretch**: Compress the serialization (e.g. for sparse trees, switch to (path, value) pairs).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Lowest Common Ancestor in a BST and in a General Binary Tree

**Spec**:
Implement two LCA functions:
1. For a BST: O(h) using the BST property (descend left/right based on comparisons).
2. For a general binary tree: O(n) using a single recursive postorder pass that returns either the found node or null.

Read the tree (level-order with `null`), then read pairs `(u, v)` and print their LCA value.

**Constraints**:
- Up to `10^5` nodes
- Time: BST O(h), general O(n) per query
- Memory: O(h) recursion

**Test inputs**:
| Tree | Query | Expected |
|------|-------|----------|
| BST `6 / 2 8 / 0 4 7 9 / null null 3 5` | `(2, 8)` | `6` |
| same BST | `(2, 4)` | `2` |
| general `3 / 5 1 / 6 2 0 8 / null null 7 4` | `(5, 1)` | `3` |
| general same | `(5, 4)` | `5` |
| general same | `(7, 4)` | `2` |

**Stretch**: Preprocess in O(n log n) to answer LCA queries in O(log n) using binary lifting (also useful in graphs).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: Recover a BST With Two Swapped Nodes

**Spec**:
A valid BST had exactly two of its node values swapped by mistake. Recover the BST by swapping the correct two node values back. Required: O(1) extra space (Morris traversal) — no recursion stack and no auxiliary array. The O(n) auxiliary inorder array is acceptable for partial credit.

Print the BST in inorder after recovery.

**Constraints**:
- Up to `10^5` nodes
- Time: O(n)
- Memory: O(1) for full credit

**Test inputs**:
| Input (BST with two swaps) | Expected inorder after recovery |
|----------------------------|---------------------------------|
| `1 / 3 null / null 2` | `1 2 3` |
| `3 / 1 4 / null null 2` | `1 2 3 4` |
| `2 / 1 3` with no swap | `1 2 3` |

**Stretch**: Detect *which* two nodes were swapped (return their original positions in the inorder sequence).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Maximum Path Sum in a Binary Tree (Any Node to Any Node)

**Spec**:
A path is any sequence of nodes connected by edges; a path may start and end at any nodes and need not pass through the root. Find the maximum sum of node values along any such path. Node values may be negative. Required complexity O(n) using a single recursive postorder pass that returns the best "down-path" contribution while updating a global max with the "through this node" two-arm combination.

**Constraints**:
- Up to `10^5` nodes, values in `[-10^4, 10^4]`
- Time: O(n)
- Memory: O(h)

**Test inputs**:
| Tree | Expected output |
|------|-----------------|
| `1 / 2 3` | `6` |
| `-10 / 9 20 / null null 15 7` | `42` |
| `-3` | `-3` |
| `2 / -1` | `2` |
| `5 / 4 8 / 11 null 13 4 / 7 2 null null null 1` | `48` |

**Stretch**: Also output the path itself (list of node values from start to end).

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
