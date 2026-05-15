# Phase 2 — tgrep (tiny grep clone, reference implementation)

```
$ python tgrep.py "TODO" -r src/
$ python tgrep.py -i "hello" some.txt
$ python tgrep.py "*.py" filelist.txt   # glob mode (* and ?)
$ python tgrep.py                       # self-demo (no args)
```

## Files

- `tgrep.py` — search engine + CLI in one module.
- `test_tgrep.py` — fixture text files in a temp dir; ~7 assertion groups.

## Design decisions

**No regex.** The capstone spec explicitly says "from scratch," so the matching primitives are:

1. `literal_search(haystack, needle)` — naive O(n·m) substring scan. Returns *all* match offsets, including overlapping ones (e.g. `'aa'` matches three times in `'aaaa'`). Fine for the file sizes a `grep` user touches; if you wanted to scale past a few hundred MB, this is exactly where KMP or Boyer-Moore slot in.
2. `glob_match(text, pattern)` — two-pointer wildcard matcher with `*` backtracking. Handles `*` (any run of chars) and `?` (one char), anchored substring-style. The implementation is the classic "save the `*` position, on mismatch rewind and consume one more char from text" pattern.

**Prefix-sum line index.** Each file produces a `FileIndex` with:

- `line_matches[i]` — 1 if line *i* contains a match, else 0
- `prefix[i]` — `sum(line_matches[:i])`

The prefix sum lets `matches_in_range(lo, hi)` answer in O(1), no matter how many queries you make. This is exactly the use case from Week 6's prefix-sums lesson: build once, query many times. The CLI uses it for the optional `--stats` output, but the real win is when you build the index once and serve repeated range queries (e.g. "matches per 100-line window across the file").

## What scaling this up looks like

The trade-off pyramid for substring search:

| Need | Algorithm | Why |
|------|-----------|-----|
| One small file, one pattern | naive | Code is 6 lines; cache-friendly. |
| Big file, one pattern | KMP / Boyer-Moore | O(n+m); BM skips ahead by pattern length on mismatch. |
| Many patterns, one big text | Aho-Corasick | Builds a trie with failure links; finds all matches in one pass over the text. |
| Many files, repeat queries | Inverted index | Tokenize once, query in log(N). This is what ripgrep + ag stop short of and what Elasticsearch builds. |

**KMP upgrade sketch.** Replace `literal_search` with a function that builds the failure table for `needle` once per pattern, then scans with two pointers and never backs up in `haystack`. The CLI surface stays identical; only the inner loop changes. The test for "all overlapping matches in `'aaaa'`" already covers the trickiest edge case.

**Aho-Corasick upgrade sketch.** If a user passes multiple patterns (a feature not yet implemented), you'd build one AC automaton over all of them and walk each line once. The `FileIndex.line_matches` array becomes a multi-dimensional flag per pattern, but the prefix-sum trick still works.

## Known limits

- Binary files are decoded with `errors="replace"`, so they don't crash but produce garbage matches. Real grep does a heuristic check on the first 8 KB.
- No `--context` (lines before/after match). Trivial to add — the prefix-sum index already tells you where matches are.
- Glob is *anchored to substring*: `q*ck` matches `quick` *inside* a line. Use `^...$` semantics if you want full-line match; that would need an explicit anchor or a flag.
