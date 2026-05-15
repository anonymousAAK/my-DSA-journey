# Rope Data Structure in VS Code / Sublime

## The problem

A text editor displays a document and lets the user type, delete, paste, and undo. If the document is 10 lines, any data structure works — even a flat string. If it's a 500 MB log file or a 200,000-line generated source file, naïve representations collapse: inserting one character at the beginning of a 500 MB string would require shifting all 500 MB. VS Code, Sublime, Atom, Vim — all face this. How do you represent a giant editable document so every keystroke is fast?

## Why the obvious approach didn't work

### Naïve: a single contiguous string

Inserting at position p in a string of length n is O(n) — you allocate a new string, copy `0..p`, the new char, then `p..n`. For a 500 MB document, that's hundreds of milliseconds per keystroke. Awful.

### Gap buffer (Emacs's classic choice)

Keep the text in a buffer with a "gap" near the cursor. Insertions at the cursor are O(1) (write into the gap). Moving the cursor moves the gap, copying bytes — O(distance moved). Great when edits cluster at one location (most editing). Bad when you jump around (search and replace across the file).

### Array of lines

Each line is a separate string; the document is an array (or list) of lines. Now appending to the middle of a line is O(line length), and inserting a new line is O(lines after insertion point). Works okay for moderate files but suffers when lines are long (think minified JS) or when there are millions of lines.

The fundamental tension: you want **fast random insertions/deletions** *and* **fast traversal / position-to-line-mapping**. No flat structure gives both.

## What they actually use

### Ropes

A **rope** is a balanced binary tree where each leaf holds a chunk of text (say, 64-1024 bytes), and each internal node stores the total length of its left subtree. Concatenating two ropes is O(1) (a new root with two children). Inserting at position p is O(log n): find the leaf containing p (using the cached subtree lengths to navigate), split it, insert the new chunk, rebalance.

Lookups, deletes, and substring extractions are all O(log n + length). Most importantly, **structural sharing**: an "undo" history can keep old versions cheaply, since rope trees can share unchanged subtrees.

Ropes are the data structure behind several text editors and most string-heavy systems (Cap'n Proto, Google Docs's collaborative editing, OT/CRDT implementations). The classic paper is Boehm/Atkinson/Plass 1995.

### Piece tables

Slightly different approach, used by VS Code and historically by Microsoft Word: store the original document immutably, plus an append-only "added" buffer of inserted text. A "piece table" is a list of pieces, each piece a (source: original|added, start: int, length: int) tuple. The document logically is the concatenation of all pieces in order.

Inserting at position p: find the piece containing p, split it into two, insert a new piece pointing to a freshly appended chunk in the "added" buffer. Three pieces from one, O(pieces / log pieces) per edit if you keep the piece table as a balanced tree.

Piece tables shine for undo (each edit's pieces stay forever — undo just truncates the piece list) and for large files (the original buffer is never copied, just sliced). VS Code's implementation uses a piece table with the pieces stored in a balanced tree (red-black) so all operations are O(log n).

### Trees over lines: a "line-indexed" tree

Both ropes and piece tables can be augmented to track **line counts** per subtree. Then "go to line 50,000" is O(log n) instead of O(file size). This is essential — every editor needs to support `:50000` in 10ms.

## The tradeoff

Both ropes and piece tables trade **constant-factor overhead** (tree pointers, per-piece metadata) for **logarithmic-time edits at any position**. For documents under a few thousand lines, a flat string + manual fix-up beats both in raw speed because of constant factors. The crossover happens around tens of thousands of lines.

Other tradeoffs:

- **Ropes** are easier to reason about academically. **Piece tables** are simpler to implement and have better cache behavior because long unchanged regions stay contiguous in memory.
- **Ropes** can fragment over heavy editing (many tiny leaves). VS Code's piece table compacts pieces periodically; ropes can rebalance via standard tree operations.
- **CRDTs / OT** for collaborative editing layer on top of either. A rope's structural sharing makes branching/merging document versions cheap (think Git for text).

The performance lesson: **measure first**. Atom famously hit walls because their original buffer implementation didn't scale to large files, and switching to a rope was a big rewrite. VS Code learned the lesson and used a piece table from early on.

## You can implement a toy version of this using Week 11-12

- Week 11-12 (trees and balanced trees) — implement a simple rope with character-chunked leaves and length-augmented internal nodes. Test: insert 1M characters one at a time at random positions, time it. Compare against a Python string with `s = s[:p] + c + s[p:]`. Rope should win dramatically beyond, say, 100k characters.
- Implement piece-table over a flat read-only "original" + an append-only "added": demonstrate that `insert(p, text)` and `delete(p, length)` are both O(pieces) where pieces grow slowly with edits.

A weekend project: build a tiny line-numbered text editor backend in 300 lines. Support `insert(line, col, text)`, `delete(line, col, length)`, `get_line(n)`. Use a rope or piece table internally. Test on a synthetic 1M-line file. Verify that operations are smooth even as the file grows.

Stretch: add **undo** as a stack of rope-versions (or piece-list-versions). Notice how structural sharing makes undo essentially free — the old version is still in the heap, referenced from the undo stack.

The deep lesson: a text editor *feels* like a simple problem until you go large. Then it becomes a beautiful exercise in choosing a structure that matches the access pattern. The classic Week 11 balanced tree is the substrate; the *augmentation* (length and line counts at each node) is what makes it useful. This is the same "augmented tree" pattern that powers Phase 5's range-sum queries on a leaderboard — the application is different, the technique is identical.
