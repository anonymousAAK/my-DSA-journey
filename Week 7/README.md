# Week 7 — Strings

> Self-check: `./scripts/journey quiz 7`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/2.palindrome_and_anagram.py`](python/2.palindrome_and_anagram.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_07/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify palindrome_check workbook/week_07/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 7`

If you got stuck: open [`python/2.palindrome_and_anagram.py`](python/2.palindrome_and_anagram.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **Strings**. You'll touch: StringBasics, PalindromeAndAnagram, KMPSearch. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | StringBasics | `java/1.StringBasics.java` | `python/1.string_basics.py` | `cpp/1.string_basics.cpp` | `rust/s01_string_basics.rs` | `web/1.string_basics.html` |
| 2 | PalindromeAndAnagram | `java/2.PalindromeAndAnagram.java` | `python/2.palindrome_and_anagram.py` | `cpp/2.palindrome_and_anagram.cpp` | `rust/s02_palindrome_and_anagram.rs` | `web/2.palindrome_and_anagram.html` |
| 3 | KMPSearch | `java/3.KMPSearch.java` | `python/3.kmp_search.py` | `cpp/3.kmp_search.cpp` | `rust/s03_kmp_search.rs` | `web/3.kmp_search.html` |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Strings | — | `python/strings.py` | `cpp/strings.cpp` | `rust/strings.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. StringBasics**
- **2. PalindromeAndAnagram**
- **3. KMPSearch**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: substring search (covered in KMPSearch).

| Approach | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Naive `indexOf` loop | O(N·M) | O(1) | Low | Small patterns / texts, one-off scripts |
| KMP (failure function) | O(N + M) | O(M) | Medium | Single pattern, worst-case guarantees needed |
| Rabin–Karp (rolling hash) | O(N + M) avg, O(N·M) worst | O(1) | Medium | Multiple patterns of same length, plagiarism-style checks |
| Z-algorithm | O(N + M) | O(N + M) | Medium | When you need all match positions and prefix info |
| Suffix automaton / Aho–Corasick | O(N + M) | O(M·Σ) | High | Many patterns at once |

| Approach (palindrome check) | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Reverse and compare | O(N) | O(N) | Low | Quick prototype |
| Two pointers from ends | O(N) | O(1) | Low | Default |
| Recursion | O(N) | O(N) stack | Medium | Pedagogy |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Comparing Strings with `==`** — `"abc" == "abc"` can be `true` due to interning, but `s1 == s2` where one was built dynamically is almost always `false`. Use `.equals()` or `.equalsIgnoreCase()`.
- **Building strings with `+=` inside a loop** — O(N²) due to immutability. Use `StringBuilder` for anything beyond a handful of concatenations.
- **Checking anagrams with `Arrays.sort(s.toCharArray())` and comparing toString** — `.toString()` on a `char[]` gives you the address, not the contents. Use `new String(arr)` or `Arrays.equals`.
- **Implementing KMP and reusing `i` for both text and pattern indices** — KMP needs two distinct indices that advance differently on mismatch. Conflating them produces an algorithm that works on examples but fails on patterns with repeated prefixes (the whole point of KMP).
- **Forgetting Unicode** — `s.length()` returns code units, not code points. Emoji and surrogate pairs will break a naive palindrome check; use `codePointAt` or `Character.toChars` for full Unicode correctness.

</details>

## Reference: how to run a topic file

<details>
<summary>Java / Python / C++ / Rust / Web one-liners</summary>


From the week's directory:

```bash
# Java
javac java/<file>.java && java -cp java <ClassName>

# Python
python3 python/<file>.py

# C++
g++ -std=c++17 cpp/<file>.cpp -o /tmp/a && /tmp/a

# Rust
rustc --edition 2021 rust/<file>.rs -o /tmp/a && /tmp/a

# Web — open in a browser
open web/<file>.html   # macOS
xdg-open web/<file>.html   # Linux
```

</details>

## Reflection prompts


- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach KMP's failure function to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
