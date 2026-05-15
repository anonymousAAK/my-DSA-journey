# What grep / ripgrep Actually Do

## The problem

You type `grep "foo" *.log` and a tool scans gigabytes of text looking for matches. You don't think about it — it's instant. But "find substring in a file" is one of the most studied algorithmic problems in computer science, with a rich history of algorithms ranging from "obvious and slow" to "subtle and astonishingly fast." Modern tools (GNU grep, ripgrep, ag) routinely outperform what a naïve implementation could do by 10-100x.

## Why the obvious approach didn't work

The textbook naïve approach: for each position i in the text, check if pattern matches starting at i. That's O(n × m) worst case for text of length n and pattern of length m. On a 1 GB log and a 10-char pattern, that's 10 billion comparisons in the worst case. Still a few seconds in C — but grep manages it in well under a second, and ripgrep is faster yet. Where does the speedup come from?

Three categories of insight, layered:

1. **Don't compare characters you don't have to.** Algorithms like KMP and Boyer-Moore preprocess the pattern to skip ahead intelligently after each mismatch.
2. **Don't process bytes that can't possibly contain the pattern.** Use SIMD / vectorized scans to find the *next plausible candidate position* very fast.
3. **Don't read bytes you don't have to.** Use OS facilities (mmap, parallel I/O) to ingest at maximum throughput.

## What they actually use

### Single-pattern search: Boyer-Moore-Horspool, KMP, and SIMD

For a single pattern, KMP (Knuth-Morris-Pratt, 1977) achieves O(n + m) by preprocessing the pattern into a "failure function" that tells you how far to shift after a mismatch. Boyer-Moore-Horspool is faster in practice for typical text: it scans the pattern *backwards* and can skip multiple characters at a time when a mismatching character isn't in the pattern at all.

Modern grep doesn't just use Boyer-Moore — it uses SIMD instructions to find candidate match positions. For an exact substring search, you can use `memchr` (which uses AVX2 / SSE2 on x86) to find the first occurrence of one byte (say, the first byte of the pattern) at gigabytes-per-second speeds. Then you do a careful comparison only at those candidate positions. ripgrep famously leverages the `memchr` crate and similar tricks.

### Multi-pattern search: Aho-Corasick

When you want to search for *many* patterns at once (e.g., `grep -F -f patterns.txt`), running KMP independently for each pattern is wasteful. Aho-Corasick (1975) builds a single automaton from all patterns and processes the text once in O(n + total_pattern_length + matches). The automaton is a trie of all patterns with "failure links" connecting them — essentially generalized-KMP for multiple patterns at once.

Aho-Corasick is everywhere: in antivirus engines scanning for thousands of malware signatures, in spam filters, in network IDS systems matching packet content against thousands of rules, in `fgrep -f`.

### Regex: NFA + DFA

When the pattern is a regex (not just a literal string), you build a nondeterministic finite automaton (NFA) from the regex (Thompson's construction, 1968), then optionally convert to a deterministic automaton (DFA). Modern grep often does this **lazily**: build NFA, simulate it directly on the text, only construct DFA states as they're needed. Lazy DFA conversion avoids the worst case of "DFA can be 2^m states" for pathological patterns.

ripgrep uses the `regex` Rust crate, which combines lazy DFA, SIMD-accelerated literal prefix searches, and parallelism over files. The "literal prefix search" is the killer: most regex patterns have some literal substring, and finding candidates via that literal (with `memchr`) before running the full regex is a huge win.

### I/O and parallelism

ripgrep parallelizes across files by default (one thread per CPU). GNU grep is single-threaded historically but is fast at I/O. Both use `mmap` or buffered reads to stay close to disk throughput. On modern SSDs, you can saturate read bandwidth (~3-5 GB/s) and the bottleneck shifts entirely to the matching algorithm.

## The tradeoff

Tradeoffs in the algorithm choice:

- **Boyer-Moore** is faster in practice on typical text but has poor worst-case bounds without modifications. **KMP** has clean O(n) worst case but is often slower in practice.
- **Aho-Corasick** is the right call when you have many patterns, but preprocessing time/memory grows with pattern set size; for a single pattern it's overkill.
- **DFA** is fast per-character but can have exponential state explosion; **NFA simulation** is slower per-character but bounded.

The system-level tradeoff: **algorithmic cleverness vs. raw byte throughput**. ripgrep famously beats systems with smarter individual algorithms because it dominates on I/O parallelism, SIMD scanning, and avoiding unnecessary work (e.g., respecting `.gitignore` so it doesn't even look at directories you didn't want). Sometimes the win is the byte you don't process.

## You can implement a toy version of this using Week 21

- Week 21 (advanced strings) — implement KMP from scratch in 30 lines. Build the failure function on a pattern, then run the search. Benchmark against naïve O(nm).
- Implement Aho-Corasick: a trie with failure links. ~100 lines. Useful exercise — the failure-link construction is one of the cleanest algorithmic ideas in CS.

A weekend project: build a "mini-grep" that takes a literal pattern and a directory. Walk all files, search with KMP, print matches with filename and line number. Benchmark on a directory of source code. Then add SIMD-style optimization: scan for the first byte of the pattern with Python's `bytes.find` (or a C extension via `mmap` + `memchr`), then only do full KMP at candidate positions. Watch throughput jump.

Stretch: implement Aho-Corasick and use it to grep for many patterns simultaneously. Try matching 1,000 patterns against a multi-megabyte file. You should see Aho-Corasick handle it in one pass, while running KMP 1,000 times takes 1,000x as long.

The deep lesson: **string matching is a microcosm of algorithm design.** There's no single right algorithm — there's a hierarchy where each level beats the previous when its assumptions hold. The senior-engineer skill is recognizing which assumption fits your problem. The Week 21 string-algorithms unit is the entry point; the rabbit hole is deep, beautiful, and surprisingly practical.
