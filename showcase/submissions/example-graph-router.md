---
name: "MiniMaps — A 10k-Node Dijkstra Router"
capstone: "Phase 1 — Mini Graph Router"
repo_url: "https://github.com/example-handle/minimaps"
github_handle: "example-handle"
demo_url: "https://asciinema.org/a/example"
languages: ["Python"]
date_finished: "2026-03-14"
---

# MiniMaps — A 10k-Node Dijkstra Router

> This is an example/fake submission to illustrate the format. Don't pattern-match on the content.

A toy shortest-path service that ingests an OpenStreetMap extract for a small city (~10,000 intersections), builds an in-memory graph, and answers route queries in under 50ms over HTTP. Built as Phase 1 of the curriculum's "Mini Graph Router" capstone.

## Capstone phase

Phase 1 — Mini Graph Router. I stayed within scope; the only extension was a `/route?format=geojson` endpoint so I could view results in Leaflet.

## Stack

- Language: Python 3.12
- Notable libraries: `heapq` (stdlib), `aiohttp`, `osmread`
- How to run it: `python -m minimaps.server --osm city.osm.pbf --port 8080`

## What was hardest

The hardest part wasn't Dijkstra — it was the graph build. OpenStreetMap data is messy: ways aren't pre-decomposed into edges, one-ways aren't always tagged, and ~5% of intersections are "phantom" nodes that exist only to mark a curve in the road. My first naive build had a 40MB heap and routing was twice the latency it should've been, because I was traversing all those phantom nodes.

Fixing this meant a preprocessing pass that contracts degree-2 nodes — essentially a one-step shortcut for every two-segment straight road. That cut the node count by 60% and dropped query time from 110ms to 28ms.

The second-hardest part was bidirectional Dijkstra. I'd assumed it was Dijkstra-with-two-priority-queues. It is, but the *termination condition* (stop when the sum of the two frontiers' best-so-far exceeds the meeting node's tentative distance) is much subtler than it sounds, and I shipped a wrong version twice before reading the textbook proof.

## What you learned

- Real-world graphs are 90% data plumbing and 10% algorithms. I'd assumed it would be the reverse.
- Profilers lie to you about the cost of heap operations because they aggregate across millions of tiny ones — write your own counter if you really want to know what's expensive.
- The textbook "explore neighbors" abstraction is fine when you own the data; with OSM you discover that "what is a neighbor" is itself a research question.

## What you'd do differently

I'd build the preprocessor first, *then* the routing engine. I built them in the opposite order and had to refactor the data structures when the preprocessor needed to mutate the graph.

## Screenshots / demo

```
$ curl 'http://localhost:8080/route?from=42.36,-71.06&to=42.40,-71.10'
{"distance_m": 7421, "time_s": 612, "nodes_explored": 1843, "ms": 28}
```
