# Week 14 — Trees

> Self-check: `./scripts/journey quiz 14`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/2.BinarySearchTree.py`](python/2.BinarySearchTree.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_14/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify bst_validate workbook/week_14/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 14`

If you got stuck: open [`python/2.BinarySearchTree.py`](python/2.BinarySearchTree.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Trees**. You'll touch: BinaryTree, BinarySearchTree. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | BinaryTree | `java/1.BinaryTree.java` | `python/1.BinaryTree.py` | `cpp/1.BinaryTree.cpp` | `rust/s01_BinaryTree.rs` | `web/1.BinaryTree.html` |
| 2 | BinarySearchTree | `java/2.BinarySearchTree.java` | `python/2.BinarySearchTree.py` | `cpp/2.BinarySearchTree.cpp` | `rust/s02_BinarySearchTree.rs` | `web/2.BinarySearchTree.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Trees | — | `python/trees.py` | `cpp/trees.cpp` | `rust/trees.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. BinaryTree**
- **2. BinarySearchTree**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: Binary Trees and Binary Search Trees.

| Approach (tree traversal) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Recursive DFS (pre/in/post) | O(N) | O(h) stack | Low | Default for balanced or moderate trees |
| Iterative DFS with explicit stack | O(N) | O(h) | Medium | Skewed trees where recursion blows the stack |
| Level-order BFS (queue) | O(N) | O(width) | Low | Level-by-level problems, shortest path in tree |
| Morris traversal (threaded) | O(N) | O(1) | High | Constant-space requirement; modifies tree temporarily |

| Approach (BST search/insert) | Time (avg) | Time (worst) | When to prefer |
|----------|------|------|----------------|
| Plain BST | O(log N) | O(N) | Random or shuffled inserts |
| Self-balancing (AVL, Red-Black) | O(log N) | O(log N) | Worst-case guarantees needed |
| `TreeMap` / `TreeSet` | O(log N) | O(log N) | Use the JDK — Red-Black under the hood |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Checking BST validity by comparing each node to only its parent** — a node can satisfy `parent < left ≤ parent < right` locally yet violate global ordering with a grandparent. Pass down `(min, max)` bounds, or do in-order traversal and verify it's strictly increasing.
- **Building a BST from a sorted array by inserting in order** — produces a fully-skewed tree (a linked list). Use the recursive midpoint construction to get a balanced tree.
- **Deleting a BST node by setting it to `null`** — only works if it has zero children. For one child, splice; for two children, replace with the in-order successor (or predecessor) and recurse.
- **Computing tree height with `1 + max(left, right)` but forgetting the null base case** — returns wrong values or NPEs. The null subtree has height -1 (or 0, depending on convention); pick one and stay consistent.
- **Recursing without considering skewed trees** — a 10⁶-deep right-skewed tree blows the default JVM stack (~10⁴ frames). Convert to iterative, or run on a `Thread` with a larger stack.

</details>

## Reference: how to run a topic file

<details>
<summary>Java / Python / C++ / Rust / Web one-liners</summary>


From the week's directory:

```bash
# Java
javac java/<file>.java && java -cp java <ClassName>

# Python
python3 python/<file>.py

# C++
g++ -std=c++17 cpp/<file>.cpp -o /tmp/a && /tmp/a

# Rust
rustc --edition 2021 rust/<file>.rs -o /tmp/a && /tmp/a

# Web — open in a browser
open web/<file>.html   # macOS
xdg-open web/<file>.html   # Linux
```

</details>

## Reflection prompts


- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach the difference between BFS and DFS on a tree in one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
