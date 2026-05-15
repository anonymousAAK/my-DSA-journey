# How "Discover Weekly" is a Graph + Matrix Factorization Problem

## The problem

Every Monday, 500+ million Spotify users get a personalized 30-song playlist. Each playlist needs to feel like it understands you, contain songs you haven't heard before, and *not* repeat across weeks. With a catalog of ~100M tracks and hundreds of millions of users, generating 500M personalized playlists is the algorithmic equivalent of cooking 500M custom meals every week from a kitchen of 100M ingredients.

## Why the obvious approach didn't work

The naïve approach: for each user, look at songs they've liked, find "similar songs," recommend the top 30 they haven't heard. The hard part is "similar."

- **Tag-based similarity** (genre, decade, BPM): too coarse. Two indie-pop songs from 2018 might have nothing in common emotionally.
- **Audio-feature similarity** (extract tempo, key, energy from the waveform): better, but expensive and still misses the *cultural* signal — what the song *means* in context.
- **Editorial curation**: doesn't scale to 500M users.

The breakthrough insight: **the data already tells you which songs are similar — through the playlists users have already made.** If millions of users put songs X and Y in the same playlist, those songs are similar in a way no audio analysis can capture.

## What they actually use

Discover Weekly is built on three intertwined techniques:

1. **Collaborative filtering via matrix factorization.** Build a giant sparse matrix M where M[u, s] = 1 if user u has played song s. Factor it as M ≈ U · S^T where U is a user-by-d matrix and S is a song-by-d matrix, with d ≈ 40-200 latent dimensions. The dot product `U[u] · S[s]` predicts how much user u will like song s. The factorization itself is found via alternating least squares (ALS) or matrix-decomposition variants.

2. **Graph-based co-occurrence**. Treat each user-curated playlist as a small graph: every pair of songs in the same playlist gets an edge (with weight). Aggregating across hundreds of millions of playlists yields a massive song-similarity graph where edge weights encode how often two songs are intentionally grouped together. Random walks on this graph (think PageRank — Phase B real-world #14) yield song-embeddings that capture cultural neighborhoods.

3. **NLP on song reviews and blog posts**. They scrape music journalism and use NLP to extract semantic descriptors per song, then embed those into the same latent space as the collaborative filtering. This is how a brand-new song with no plays can still be recommended — its text-derived embedding sits near its musical neighbors.

The final recommendation is a blend: candidate songs come from collaborative filtering (you'll like what people-like-you like), filtered and re-ranked using the graph similarity and content embeddings, then diversified so the playlist isn't 30 variations of the same song.

## The tradeoff

Matrix factorization captures the wisdom of crowds but suffers the **cold-start problem** — new users with no plays get garbage recommendations, and brand-new songs with no plays can't be recommended at all. The graph and text components are what rescue cold-start. The blend is the engineering: too much CF and new music never surfaces; too much content-based and recommendations feel mechanical.

The other tradeoff is **freshness**: matrix factorization is expensive to retrain. Spotify batches it — the heavy factorization runs nightly, and intra-day signals (a song you just played) feed into a lighter re-ranking layer that adjusts the precomputed candidate set. This is the same pattern that powers most recommender systems at scale.

## You can implement a toy version of this using Week 19-20

- Week 19 (graph traversal, shortest paths, BFS) — build a song-similarity graph from a small public playlist dataset (e.g., the Million Playlist Dataset from Spotify itself, which is public). Run BFS from a seed song to find its k-hop neighborhood.
- Week 20 (DP on graphs / random walks) — implement a random walk with restart. From a seed user's favorite songs, take random steps on the song-similarity graph; songs visited often are good recommendations. This is `Personalized PageRank` in disguise, and it captures the *graph* half of Discover Weekly.
- Stretch goal: implement matrix factorization yourself with NumPy on a small user-song matrix (1k users × 10k songs). ALS in 50 lines of code. Compute predicted ratings, recommend top-k unseen songs per user.

A weekend project: take 10k playlists, build the co-occurrence graph, then for any seed song find its top neighbors. You'll be surprised how *meaningful* the results are — pure graph structure, no audio features, no text. The cultural signal is in the edges.
