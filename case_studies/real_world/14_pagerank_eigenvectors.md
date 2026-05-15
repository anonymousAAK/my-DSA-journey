# PageRank as a Graph Algorithm

## The problem

Imagine you've just built the first web crawler, and you have a corpus of millions of pages. A user types "computer science"; thousands of pages match. Which do you show first? The pre-Google search engines (AltaVista, Lycos, Excite) ranked by keyword frequency, page length, and other content-only features. The result was a mess of keyword-stuffed garbage. Sergey Brin and Larry Page's 1998 insight: **use the link structure of the web itself as a quality signal**. If many pages link to a page, it's probably important. If important pages link to it, it's even more important.

Turning that recursive definition ("important = linked-to-by-important") into a concrete number per page is the PageRank algorithm — and it turns out to be an eigenvector computation on the web's adjacency matrix.

## Why the obvious approach didn't work

The naive ranking signals — keyword frequency, title-tag matches — were trivially gameable. Anyone could put `<title>computer science computer science computer science</title>` on a junk page and rank top-3. Search results in 1997 were embarrassingly bad for any commercial keyword.

A first-cut link-based approach: count inbound links per page. Pages with more inbound links rank higher. This is also gameable — set up a thousand junk pages all linking to your spam page. You need a notion of "important link" that itself depends on the importance of the linking page. That's the recursive definition.

## What they actually use

PageRank in its simplest form:

> PR(page) = (1 - d) + d × Σ over all pages p linking to it of (PR(p) / number-of-outgoing-links(p))

where d is a damping factor (typically 0.85), modeling a "random surfer" who follows links 85% of the time and jumps to a random page 15% of the time.

This is a recursive equation, but it has a clean linear-algebra interpretation: PR is the **dominant eigenvector** of the matrix M defined by M[i,j] = (1/out_degree(j)) if j links to i, else 0, modified by the damping. Specifically PR = (1-d) × 1/N + d × M × PR. This is solvable by **power iteration**: start with uniform PR, multiply by the transition matrix, normalize, repeat until convergence.

Each iteration is O(E) where E is the number of edges in the web graph. The web has ~10^11 pages and ~10^12 links. One iteration is a trillion sparse-matrix multiplications. Convergence typically takes 50-100 iterations.

This is impossible on one machine. The PageRank-at-scale paper (Brin & Page 1998) is also one of the founding papers of large-scale distributed graph processing. They used a custom storage layout that streamed edges in order, kept the current PR vector in memory (10^11 floats = 800 GB, sharded), and did each multiplication in a distributed shuffle. This was the precursor to MapReduce.

In production, Google long ago moved beyond pure PageRank — modern ranking combines hundreds of signals (BERT-based content understanding, click models, fresh-content boosts, knowledge graph integration, etc.). But the **link-structure-as-eigenvector** intuition is foundational.

PageRank-style algorithms still live in many places:

- **Twitter's "Who To Follow"** uses Personalized PageRank on the follow graph.
- **Citation networks** in academia rank papers by an eigenvector centrality measure.
- **Bitcoin transaction analysis** uses PageRank-style scoring to identify suspicious clusters.
- **Spotify's Discover Weekly** (#2) uses random walks on the song co-occurrence graph — essentially Personalized PageRank.

## The tradeoff

The big tradeoff: **PageRank assumes a static graph and steady state.** It doesn't model time (fresh content), context (your search query), or user personalization. Modern search systems layer query-dependent scoring (TF-IDF, BM25, BERT) on top of static link-based authority.

Algorithmically: **power iteration is simple and embarrassingly parallel** but has slow convergence (linear in 1/log(λ2/λ1)). Smarter approaches (push-based PageRank, asynchronous iteration, Krylov-subspace methods) can converge faster on real graphs but are more complex.

Another tradeoff: **gameability**. Pure PageRank turned out to be exploitable by link farms (mass-creating sites that link to a target). The dance between SEO spam and Google's defenses (TrustRank, manual penalties, BERT replacing crude content matching) is decades old now.

For a personalized variant: **Personalized PageRank** starts the "random jump" not at a uniform distribution but at a specific seed (e.g., the user's recent searches). This gives a per-user importance ranking — much more powerful, but ~N times more expensive to compute. Approximations like Monte Carlo simulation of random walks make it tractable.

## You can implement a toy version of this using Week 16-17 + a little linear algebra

- Week 16 (graph representation) — represent a small web graph as an adjacency list or sparse matrix.
- Week 17 (graph traversal) — implement a random walk on the graph. Simulate 1M steps starting from each node; the visit frequencies converge to the PageRank vector.
- Pure power iteration in NumPy: `pr = (1-d)/N + d * M @ pr` in a loop. 5 lines. Converges in 50 iterations on a graph of 10k nodes. Trivial.

A weekend project: scrape the link structure of a Wikipedia category subgraph (a few thousand pages). Compute PageRank. The results will be obviously correct — main category pages rank above subcategory pages, which rank above stub articles. You'll *see* the algorithm pulling out the structurally-important nodes.

Stretch: implement Personalized PageRank — instead of teleporting uniformly during damping, teleport to a seed node. Now the PR vector is personalized to that seed. Use it for "pages most similar to article X" recommendations.

Even further: implement push-based PageRank (Andersen-Chung-Lang), which propagates residual "score" lazily through the graph and is much faster for personalized variants. This is the algorithm that makes Personalized PageRank feasible at internet scale.

The deep lesson: **linear algebra and graph theory are two views of the same thing.** An adjacency matrix's eigenvectors encode graph structure; a graph's connectivity gives meaning to its matrix's spectrum. Many of the most powerful "algorithms" in modern systems (PageRank, spectral clustering, graph neural networks) live at this intersection. The Week 17 graph-traversal foundations and a Week 22-ish appreciation for matrix-tree-theorem-style ideas are the on-ramp.
