# Capstone — Phase 2: Tiny Grep Clone with Prefix-Sum Line Counting

**Time estimate**: 10-15 hours over 1-2 weekends.
**Prerequisite weeks**: 6-10 (sorting, hashing, two pointers, prefix sums, sliding windows, basic pattern matching).
**Skill checked**: You can stream large files efficiently, implement a non-trivial matching algorithm by hand, and use prefix sums to answer range queries in O(1).

## The Goal
Build a small command-line search tool — call it `tgrep` (tiny grep) — that searches a file or directory for lines matching a pattern. Support plain-text matching and a useful subset of glob patterns (`*`, `?`, `[abc]`, `[a-z]`). Also expose a `--range L:R` flag that, after a one-pass preprocessing of the file, answers "how many matching lines are in line range L..R" in O(1) per query — backed by a prefix sum array. This last piece is what makes the project a *DSA* capstone and not just a parsing exercise.

## Functional Requirements
- Must accept a pattern and a path (file or directory).
- Must support plain-text substring matching (default).
- Must support glob matching with `--glob`, including `*`, `?`, `[abc]`, `[a-z]`.
- Must print matching lines with their line numbers, in `file:lineno:content` format (so editor pipelines work).
- Must support `--range L:R` to report the count of matches in a given line-number window. This must run in O(1) *per query* after one O(N) preprocessing pass; you should be able to issue many `--range` queries against the same file without re-scanning.
- Should support `--count` to print only the match count.
- Should support recursive directory search via `-r`.
- Should reject patterns that contain unclosed character classes (`[a-`) with a clean error.

## Non-functional Requirements
- Performance: scan a 100 MB log file in well under 5 seconds on a laptop. (Plain-text matching with Boyer-Moore-Horspool or even Python's `in` is fine; you don't need to beat ripgrep.)
- Memory: stream the file. Do not load it all into RAM. The prefix sum array is the only O(N_lines) structure you keep.
- Code quality: tokenizer-style separation — pattern compiler (turns a glob into a matcher), file scanner (streams lines), and query interface (range queries) are three distinct modules.
- Tests: at least 25 tests across plain-text, glob, range queries, and error cases.

## Architecture Sketch

```
                       +-------------------+
                       |  Pattern compiler |  glob -> matcher fn or DFA
                       +---------+---------+
                                 |
            +--------------------+--------------------+
            |                                         |
            v                                         v
+-----------+-----------+                +------------+-------------+
|     File scanner      |   per-line     |  Match array (1 bit per |
| (streams, calls match)|--------------> |  line, 1 = match)        |
+-----------------------+                +------------+-------------+
                                                      |
                                                      v
                                          +-----------+-----------+
                                          |  Prefix sum builder   |
                                          |  P[i] = #matches in   |
                                          |  lines 0..i-1         |
                                          +-----------+-----------+
                                                      |
                                                      v
                                          range(L,R) = P[R+1] - P[L]
                                          O(1) per query
```

## Implementation Roadmap

1. **Day 1 (3-4h) — Plain-text matching + streaming scanner.**
   Start with the simplest case: substring match using your language's built-in. Implement line-by-line streaming. Get `file:lineno:content` output right. This is the "hello world" baseline you'll build on. Write integration tests using small fixture files in `tests/fixtures/`.

2. **Day 2 (3-4h) — Glob compiler.**
   Translate a glob to one of (a) a regex object, (b) a hand-written NFA/DFA, or (c) a recursive matcher. Pick (c) for the educational value — a 30-line recursive matcher that handles `*` with backtracking is a beautiful little algorithm. Document the worst-case complexity in your README (it's exponential in the worst case for nested `*`; bounded inputs make it fine in practice).

   Test cases that have bitten everyone who's written this:
   - `*.txt` matches `a.txt`, not `a/b.txt` (in single-segment glob mode).
   - `[abc].txt` matches `a.txt`, `b.txt`, `c.txt`.
   - `[a-c]*.txt` — composition.
   - `\*` — escaped literal star.

3. **Day 3 (2-3h) — Prefix sum range queries.**
   This is the DSA part. After the file scan, you have a per-line bit `m[i] ∈ {0,1}`. Build `P[i] = m[0] + m[1] + ... + m[i-1]` so that `P[0] = 0` and the count of matches in `[L, R]` inclusive is `P[R+1] - P[L]`. Wire `--range L:R` to call into this. Add a `--repl` mode that lets you issue many range queries interactively against an already-scanned file — that's where O(1)-per-query pays off.

4. **Day 4 (2-3h) — Recursive search + polish.**
   Implement `-r` with a directory walker (depth-first; respect `.gitignore` is a stretch goal). Write the README with a benchmark section: scan time on a known file, range-query latency.

## Stretch Goals
- `--invert` to print non-matching lines.
- Anchored patterns (`^foo`, `bar$`).
- Multi-pattern search via Aho-Corasick — significantly faster than running plain-text search N times when you have many needles. This pulls Week 9-10 material in.
- `--context N` to print N lines before and after each match.
- Honor `.gitignore` for the recursive search.
- Memory-map the file via `mmap` and compare benchmark numbers.

## Self-grading rubric
| Criterion | Points | What you're checking |
|-----------|--------|----------------------|
| Correctness on basic inputs | 30 | Plain-text and glob matching both work, output format is right |
| Handles edge cases | 20 | Empty file, file ending without newline, unclosed `[`, binary file (graceful skip) |
| Algorithm choice is justified (commit message or README) | 15 | Why recursive glob vs. NFA, why prefix sum is asymptotically right |
| Code is readable (function size, naming) | 15 | Three modules, the recursive matcher is under 40 lines |
| Tests pass (≥80% coverage on core logic) | 10 | Especially the glob compiler — it's where bugs hide |
| Stretch goal implemented | 10 | Aho-Corasick is the meatiest; anchored patterns is the cheapest win |

## When you're done
- Push to a separate repo (or branch) and link it from your portfolio.
- Write a reflection essay in your `SOLUTION_JOURNAL.md` covering: what's slower than you expected, what's faster, where would you go to make it production-quality?
- Compare your final architecture to a real product that does the same thing (see `case_studies/real_world/`). Read the first page of ripgrep's design doc — note how aggressively it parallelizes per file, which you didn't do. Why might that not be worth the complexity for your use case?
