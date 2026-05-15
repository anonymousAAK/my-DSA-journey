# How Google Maps Uses Dijkstra (and Why They Also Use Bidirectional A*)

## The problem

You open Maps, type an address, and the app gives you a 47-minute route across a continent in under a second. The road network of the United States alone has ~50 million intersections and ~150 million road segments. Computing the *shortest* path through that graph naively is a textbook Dijkstra problem — but textbook Dijkstra on 50M nodes is hundreds of milliseconds at best, and that's per query, with one CPU core, assuming the graph is in RAM. Maps serves billions of queries a day. The math doesn't work.

## Why the obvious approach didn't work

Plain Dijkstra explores nodes in order of distance from the source. On a continental graph, by the time you've reached the destination 3,000 miles away, you've explored a vast disk of nodes covering everything within that radius — *including all the directions you weren't going*. That's hundreds of millions of node-relaxations, most of them wasted.

Worse: edge weights aren't constant. They depend on time of day (traffic), road type (highway vs. residential), turn restrictions, current construction. Storing one weight per edge isn't enough.

## What they actually use

The real production system is a pipeline of techniques:

1. **A\* search with a good heuristic.** Straight-line "as-the-crow-flies" distance is an admissible heuristic for shortest-time queries when speed is bounded. A* focuses exploration toward the goal instead of expanding a full disk. On road graphs this typically reduces explored nodes by 10-100x.

2. **Bidirectional search.** Run two searches in parallel — one forward from source, one backward from destination — and stop when they meet. Geometrically, two radius-r/2 disks have ~half the area of one radius-r disk, so this halves the work alone. Combined with A*, it's a multiplicative win.

3. **Contraction hierarchies (CH)** or **Customizable Route Planning (CRP)** for the heavy lifting. The road graph is preprocessed offline into a hierarchy: small back-roads are "contracted" into shortcut edges between major intersections. At query time, the search walks "up" the hierarchy from both endpoints — going from your driveway up to a highway exit, across the highway via long shortcut edges, and back down to the destination's neighborhood. A continental query becomes thousands of node visits, not millions.

4. **Periodic re-preprocessing** for live traffic. CH was rigid — recomputing the hierarchy took hours. Google moved to CRP, which separates the hierarchy structure (slow to compute) from edge weights (fast to update). Traffic updates re-cost edges in seconds, not hours.

## The tradeoff

Preprocessing time and memory in exchange for query latency. CRP and CH preprocess a continental graph in hours and consume tens of GB, but queries drop from "hundreds of ms" to "single-digit ms." For an app serving billions of queries, that tradeoff is a no-brainer — the preprocessing cost is amortized over an astronomical number of queries.

The other tradeoff is **answer quality**. Some routing systems use heuristics that aren't strictly optimal but are 99% as good and 100x faster. Maps will sometimes show you "two routes within 2 minutes of each other" — and the "fastest" claim is best-effort, not provable optimum, because of live data.

## You can implement a toy version of this using Week 16-18

- Week 16 (BFS and graph representation) — start by routing on a small grid graph using BFS.
- Week 17 (Dijkstra) — generalize BFS to weighted edges. Run it on a small extracted OpenStreetMap region (a single city is ~100k nodes — manageable).
- Week 18 (A*) — add a straight-line-distance heuristic, measure the speedup vs. plain Dijkstra. You'll see a real 5-10x reduction in explored nodes on a city graph.
- A weekend project: download a city's OSM data with `osmnx`, build the graph, run Dijkstra and A*, and visualize the explored regions overlaid on the map. You'll *see* the heuristic focus the search toward the goal, and the same visualization makes the value of bidirectional search obvious.

Contraction hierarchies are a stretch goal — they're written up in detail in Geisberger et al. (2008) and there are Python libraries (`graph-tool`, `RoutingKit`) that implement them. But you don't need CH to feel the *idea* of preprocessing-for-fast-queries; even simple landmark-based heuristics (ALT — A*, Landmarks, Triangle inequality) give a nice taste in a Week 18 afternoon.
