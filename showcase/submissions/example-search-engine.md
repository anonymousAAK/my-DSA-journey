---
name: "fts-rs — A 100k-Document Inverted-Index Search Engine"
capstone: "Phase 3 — Mini Search Engine"
repo_url: "https://github.com/example-handle-2/fts-rs"
github_handle: "example-handle-2"
demo_url: ""
languages: ["Rust"]
date_finished: "2026-04-02"
---

# fts-rs — A 100k-Document Inverted-Index Search Engine

> This is an example/fake submission to illustrate the format. Don't pattern-match on the content.

A from-scratch full-text search engine in Rust. Indexes 100,000 Wikipedia abstracts in ~12s, answers BM25-ranked queries in single-digit milliseconds, and persists the index to disk in a binary format I designed (because it sounded fun).

## Capstone phase

Phase 3 — Mini Search Engine. I added a stretch goal: a basic query parser that handles `+required -excluded "exact phrase"` syntax.

## Stack

- Language: Rust (1.75)
- Notable libraries: `serde` for some serialization helpers, `unicode-segmentation` for tokenization. Everything else is stdlib.
- How to run it: `cargo run --release -- index <corpus.jsonl> --out idx.bin && cargo run --release -- query idx.bin "your query"`

## What was hardest

BM25 scoring was conceptually fine — the formula is what it is. The hard part was making it *fast*. My first implementation called `idf(term)` and `tf(doc, term)` inside the inner loop, both of which did a hash lookup. Profiling showed 80% of query time was hashing. Caching `idf` at query start and switching the posting lists to a flat `Vec<(doc_id, tf)>` layout cut latency by ~5x.

The second hard thing was phrase queries. Posting lists store per-document term frequencies but not *positions*; to support phrases I had to add a parallel position-index. I went back and forth on whether to interleave positions into the main posting list or keep them in a sidecar. The sidecar won — it kept the hot path (term-only BM25) unchanged.

## What you learned

- "Algorithmic complexity" and "wall-clock speed" are not the same thing once you care about cache lines. My second implementation had identical big-O to my first and was 5x faster.
- Rust's borrow checker forced me to think about ownership of intermediate scoring buffers in ways I would have hand-waved away in Python. Annoying in the moment, valuable afterwards.
- A binary file format is a *contract* with future-you. I added a version byte at the start and was glad I did the first time I changed a struct layout.

## What you'd do differently

Profile earlier. I spent two days hand-optimizing the tokenizer before realizing it was 2% of query time.

## Screenshots / demo

```
$ ./target/release/fts-rs query idx.bin '"machine learning" +python -java'
1. python (score=14.21)            "Python is a programming language often used for machine learning..."
2. tensorflow (score=12.93)        "TensorFlow is an open-source machine learning library originally..."
3. scikit-learn (score=12.11)      "scikit-learn is a free machine learning library for Python..."
Total: 47 hits in 3.2 ms
```
