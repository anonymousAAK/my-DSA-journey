# Algorithm Visualizations

A self-contained, framework-free collection of interactive visualizations for the algorithms covered in this curriculum. Each page is a single HTML file with vanilla JS + Canvas. No build step, no dependencies — open any file directly in a browser.

## Pages

| File | Algorithm | Linked from |
|------|-----------|-------------|
| [`index.html`](index.html) | Landing page (thumbnails) | — |
| [`sorts.html`](sorts.html) | Bubble / Selection / Insertion / Merge / Quick sort, side-by-side | Week 9 |
| [`binary_search.html`](binary_search.html) | Binary search with lo / mid / hi pointer animation | Week 8 |
| [`bfs_dfs.html`](bfs_dfs.html) | BFS frontier expansion vs DFS stack on a grid graph | Week 17 |
| [`dijkstra.html`](dijkstra.html) | Dijkstra relaxation on a weighted graph, with priority-queue contents | Week 22 |
| [`segment_tree.html`](segment_tree.html) | Segment tree built from an array, range-sum query highlighted | Week 21 |
| [`recursion_tree.html`](recursion_tree.html) | Recursion tree for naive Fibonacci or Tower of Hanoi | Week 5 |
| [`dp_table.html`](dp_table.html) | 0/1 Knapsack or LCS DP table filling cell by cell | Week 18 |

## Conventions

Every viz follows the same shape so they feel like one toolkit:

- **Dark theme**, matching the rest of the site (`--bg #0d1117`, `--card #161b22`, `--blue #58a6ff`, `--green #3fb950`, `--yellow #d29922`, `--red #f85149`).
- **Controls bar** at the top with at least: `Step`, `Play`, `Pause`, `Reset`, and a speed slider. Inputs (array, target, source node, etc.) sit alongside.
- **Two-column layout**: visualization canvas on the left, pseudocode panel on the right.
- **Active line highlighting** in the pseudocode mirrors the algorithm's current operation.
- **Stats counter**: comparisons, ops, queue/stack contents, visited nodes — whichever is relevant.
- **Step / Play / Pause / Reset** all work on a precomputed list of "states" produced by a planner function, so the animation is deterministic and you can replay.

## File anatomy

Each viz file is ~250–400 lines and contains:

1. `<style>` — embedded CSS (same palette across all files; not factored out so each file works standalone).
2. The control bar + canvas/pseudocode panels.
3. JS:
   - **`LINES`** — the pseudocode shown on the right, one entry per line.
   - **A planner function** (often called `plan*` or `build*`) — walks the algorithm and pushes a `{line, ...stateDelta}` object for each step into a `steps` array.
   - **`step()`** — advances by one entry from `steps`, mutates a "live state", and calls `render()`.
   - **`render()`** — re-draws the canvas from the live state and re-highlights pseudocode.
   - **`play()` / `pause()`** — drive `step()` on a timer whose delay comes from the speed slider.

## Adding a new visualization

1. Copy any existing file (e.g. `binary_search.html`) as a starting skeleton.
2. Replace the `LINES` constant with your pseudocode.
3. Write a planner that records each step. The state delta should include `line` (which pseudocode line is active) plus whatever fields your `render()` needs (e.g. `lo`, `hi`, `mid`, `cur`, `q`, etc.).
4. Implement `render()` — at minimum re-draw the canvas, re-render pseudocode with `.line.active` set, and update the stats panel.
5. Wire up the controls (`apply`, `step`, `play`, `pause`, `reset`, speed slider). Most of the wiring can be copy-pasted unchanged.
6. Add an entry to `index.html`'s `.grid` and to the table above.
7. (Optional) Add a `🎨 Visualize` link to the relevant Week's `web/index.html`, inside the `#practice-reflect` section.

## Design choices

- **No frameworks.** Vanilla JS + Canvas. We're showing how algorithms work, not how to set up Webpack.
- **No build step.** `file://` URL works. Self-contained files are easier to fork into a gist or share.
- **Pre-planned steps.** Each viz computes all the steps up front, then animates by walking the array. This lets the user step forward without races, and we could later add step-back without restructuring.
- **One pseudocode line per `step()` event.** Keeps the highlight changes feeling tight, even when an algorithm does several things at once internally.

## Not a teaching replacement

These visualizations show *what happens*, but the *why* lives in the Week N READMEs, the patterns/challenges files, and `PROBLEM_SOLVING.md`. Treat the viz as a sanity check after reading, or as a debugger when intuition slips.
