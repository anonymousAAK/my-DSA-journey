# Capstone — Phase 3: Interactive Visualizer for Trees, Heaps, and Linked Lists

**Time estimate**: 12-15 hours over 2 weekends.
**Prerequisite weeks**: 11-15 (linked lists, trees, BSTs, heaps, basic tree balancing concepts).
**Skill checked**: You can build a tool that *teaches you back* — a visualizer is the single best way to lock in tree-and-heap intuition, and writing one forces you to confront every edge case of the underlying data structure.

## The Goal
Build a single-page HTML app (no framework required — vanilla JS is fine, and if you reach for React keep it minimal) that renders three data structures and lets the user perform live operations on them with visual updates:
1. A **binary search tree** with insert, delete, search, and one rotation (left or right) you can invoke manually.
2. A **min-heap** with insert and extract-min, with the sift-up and sift-down steps animated step by step.
3. A **singly linked list** with insert-at-position, delete-at-position, and reverse, with the pointer hand-offs visible.

This is the project you'll show people. It's also the one that turns "I read about heaps" into "I actually feel them."

## Functional Requirements
- Three independent panels for BST, heap, and linked list. Tabs or columns — your call.
- Each panel has input controls (a number input and operation buttons).
- BST renders nodes with their values and edges between parent and child; new nodes appear at the correct slot; deletes show the successor-replacement step (the trickiest part of BST delete).
- Heap renders as a binary tree (use the index/2 parent trick) AND as the underlying array beneath it, so the learner sees both views. Sift-up and sift-down highlight the swapping pair at each step before the next step fires.
- Linked list renders as a horizontal chain with explicit `next` arrows. Insert-at-k animates the pointer rewiring so it's obvious which `next` is being reassigned and in what order.
- Should reject invalid inputs (non-numeric, duplicate insert into BST if you treat BST as unique-key) with a visible inline error.

## Non-functional Requirements
- Performance: a 100-node tree must render and animate without lag. You're not building a 100k-node tool.
- Memory: no leaks across many operations — clean up old DOM/SVG nodes when redrawing.
- Code quality: separate the *data structure logic* from the *rendering*. The BST file must be testable in isolation without touching the DOM. This is the single most important architectural rule of this capstone — it's how real frontend code is structured.
- Tests: at least 20 tests on the data structure logic (no DOM). Snapshot tests of the rendered output are a nice-to-have but not required.

## Architecture Sketch

```
+-----------------------------+
|  index.html (controls UI)   |
+------+-----------+----------+
       |           |
       v           v
+-------------+   +------------------+
| bst.js      |   | renderers/bst.js |
| heap.js     |   | renderers/heap.js|
| linked.js   |   | renderers/list.js|
| (pure logic)|   | (SVG / DOM only) |
+-------------+   +------------------+
        \                 /
         \  event bus    /
          +-------+-----+
                  v
        +--------------------+
        | animation/runner.js|
        | step queue + delay |
        +--------------------+
```

The event bus is the contract: data-structure modules emit events like `{type: 'swap', i: 3, j: 7}` for heap, or `{type: 'pointer-assign', node: 4, field: 'next', target: 9}` for the linked list. Renderers subscribe and animate. This decoupling is what lets you test the logic in isolation.

## Implementation Roadmap

1. **Day 1 (3h) — Skeleton + linked list.**
   Get the page layout and event bus working. Linked list is the simplest data structure, so implement it end-to-end first to validate the architecture. Each `next` reassignment emits a `pointer-assign` event; the renderer draws an arrow and fades the old one. Get reverse to look gorgeous — three pointers (`prev`, `cur`, `next`) shown explicitly is a perfect teaching moment.

2. **Day 2 (4h) — BST.**
   Implement insert (easy), search (easy), delete (the only hard one — three cases: leaf, one child, two children with successor lookup), and a single rotation. Render the tree with a tidy-tree layout — Reingold-Tilford is the textbook algorithm, but for small trees a simple "x = inorder index × spacing" works. Delete-with-two-children is the moment you'll learn the most: emit a sequence of events (find successor → copy value → delete successor node) and watch them animate.

3. **Day 3 (3-4h) — Heap.**
   Render both views (tree + array). Insert: append to array end, sift up. Extract-min: swap root and last, remove last, sift down. Each swap emits an event; the renderer highlights the two cells in red, pauses 300ms, then swaps. The pause is what turns a heap from a black box into a thing you understand.

4. **Day 4 (2-3h) — Polish + write-up.**
   Add a "speed" slider for animations. Add tooltips on each operation that explain what's happening ("Sifting up: the new element is bubbling toward the root because it's smaller than its parent."). Write a one-page README explaining how to use it and one paragraph on what each operation taught you while you were debugging.

## Stretch Goals
- AVL or red-black tree with auto-rotation: show the rebalance step by step.
- Drag-to-rearrange nodes (purely cosmetic) so users can lay out the tree how they want before animating an operation.
- A "challenge mode" — show a tree, ask the user "what does extract-min produce next?" and grade their answer.
- Persist state via `localStorage` so a reload keeps the tree.
- A timeline scrubber: replay the last 20 operations forward and backward.

## Self-grading rubric
| Criterion | Points | What you're checking |
|-----------|--------|----------------------|
| Correctness on basic inputs | 30 | All operations on all three structures produce mathematically correct state |
| Handles edge cases | 20 | Empty structure operations, BST delete of a two-child root, sift on a single-element heap |
| Algorithm choice is justified (commit message or README) | 15 | Why event bus over direct render calls; why the tree layout algorithm you picked |
| Code is readable (function size, naming) | 15 | Logic modules contain zero DOM references; renderers contain zero data-structure logic |
| Tests pass (≥80% coverage on core logic) | 10 | Logic modules are 100% testable from Node/Jest without a browser |
| Stretch goal implemented | 10 | AVL is the meatiest; timeline scrubber is the most useful for users |

## When you're done
- Push to a separate repo (or branch) and host on GitHub Pages, Vercel, or Netlify. Link from your portfolio. **This is the one capstone where hosting it matters** — recruiters will click.
- Write a reflection essay in your `SOLUTION_JOURNAL.md`: where did decoupling logic from rendering save you, where did it cost you?
- Compare your final architecture to a real product that does the same thing (see `case_studies/real_world/`). VisuAlgo and the "USFCA Data Structure Visualizations" site are the inspirations — read their source if you can find it.
