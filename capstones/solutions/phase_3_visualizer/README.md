# Phase 3 — Tree & Heap Visualizer (reference implementation)

A single-file HTML page (`visualizer.html`) that animates BST and min-heap operations as SVG. Open it in any modern browser — no server, no build step, no dependencies.

```
$ open visualizer.html        # macOS
$ xdg-open visualizer.html    # Linux
```

## What it shows

- **BST**: insert, delete (with in-order successor swap), pre-loaded demo tree.
- **Min-heap**: insert (sift-up), extract-min (sift-down), `heapifyFrom` on a random 10-element array.
- **Animation steps**: yellow = node touched by an insert/delete; blue = node currently being compared.
- **Speed slider** controls the per-step delay (50–800 ms).
- **Log pane** prints every operation and step count.

## Architecture: event bus + pure renderer

The hard part of any algorithm visualizer is *not* the data structure — it's keeping the visual layer from drowning in the operational details. This implementation uses the standard decoupling:

```
+-----------------+   events list   +------------+   layout obj   +--------------+
| Data structure  | --------------> |  Driver    | -------------> | SVG renderer |
| (BST / MinHeap) |                 | (animator) |                |              |
+-----------------+                 +------------+                +--------------+
```

1. **Data structure** never touches the DOM. Each mutation method returns a *list of events* (`{type: 'compare', id}`, `{type: 'insert', id, value}`, `{type: 'swap', a, b}`, `{type: 'delete', id}`). Pure logic, easy to test by inspecting the event sequence.
2. **Driver (`play`)** iterates the event list and pushes the current snapshot to the renderer with a delay between each step. It's the only piece that knows about time.
3. **Renderer (`render`)** is a pure function: given a *layout* (positions + edges), it wipes the SVG and draws everything from scratch. No diffing, no per-frame state. Idempotent, trivially testable.
4. **Layout** is also a pure function: given the data structure's current shape, return `{positions, edges, columns}`. BST uses in-order x positions; heap uses level-order positions.

The `Bus` module at the top is a hook for future cross-cutting subscribers (e.g. an audit panel that records every operation). It's currently unused by the visualizer but kept in place because it's the natural extension point — wiring a second listener doesn't touch any existing code.

## Why this architecture

The temptation in a visualizer is to update the SVG inline during the BST mutation: "compare node 5 → set its fill to blue → await → recurse left". This couples your data structure to the DOM and makes the logic untestable in node/jest without a browser.

The event-list pattern keeps each layer independently testable:

- BST unit tests: insert values, assert the event sequence.
- Renderer unit tests: pass a synthetic layout, snapshot the SVG output.
- Driver: stub `requestAnimationFrame`/`setTimeout`, assert the renderer is called once per event.

## What the next iteration would add

- **Step-through controls** (next / prev / pause). Easy: the event list is already materialized; just index into it.
- **AVL or red-black**: drop in alongside `BST` with the same event-list API. The renderer doesn't need to know.
- **Save/load**: serialize the data structure to JSON and reload. The shape of `bst.root` and `heap.arr/heap.ids` is already JSON-friendly.
- **Performance HUD**: count comparisons + swaps per op. The events already carry this information.
- **Mobile-friendly**: SVG scales, but the toolbar should wrap on narrow screens.
