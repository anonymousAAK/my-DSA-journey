# Week 4

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | Square Pattern | `java/1.Square_Pattern.java` | `python/1.square_pattern.py` | `cpp/1.square_pattern.cpp` | `rust/s01_square_pattern.rs` | `web/1.square_pattern.html` |
| 2 | Tri Star Pattern | `java/2.Tri_Star_Pattern.java` | `python/2.tri_star_pattern.py` | `cpp/2.tri_star_pattern.cpp` | `rust/s02_tri_star_pattern.rs` | `web/2.tri_star_pattern.html` |
| 3 | Tri No pattern | `java/3.Tri_No_pattern.java` | `python/3.tri_no_pattern.py` | `cpp/3.tri_no_pattern.cpp` | `rust/s03_tri_no_pattern.rs` | `web/3.tri_no_pattern.html` |
| 4 | Reverse Num Pattern | `java/4.Reverse_Num_Pattern.java` | `python/4.reverse_num_pattern.py` | `cpp/4.reverse_num_pattern.cpp` | `rust/s04_reverse_num_pattern.rs` | `web/4.reverse_num_pattern.html` |
| 5 | Alpha Pattern | `java/5.Alpha_Pattern.java` | `python/5.alpha_pattern.py` | `cpp/5.alpha_pattern.cpp` | `rust/s05_alpha_pattern.rs` | `web/5.alpha_pattern.html` |
| 6 | Char Pattern | `java/6.Char_Pattern.java` | `python/6.char_pattern.py` | `cpp/6.char_pattern.cpp` | `rust/s06_char_pattern.rs` | `web/6.char_pattern.html` |
| 7 | Interesting Alphabet | `java/7.Interesting_Alphabet.java` | `python/7.interesting_alphabet.py` | `cpp/7.interesting_alphabet.cpp` | `rust/s07_interesting_alphabet.rs` | `web/7.interesting_alphabet.html` |
| 8 | Mirror Image | `java/8.Mirror_Image.java` | `python/8.mirror_image.py` | `cpp/8.mirror_image.cpp` | `rust/s08_mirror_image.rs` | `web/8.mirror_image.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Patterns | — | `python/patterns.py` | `cpp/patterns.cpp` | `rust/patterns.rs` | — |
| Interactive index | — | — | — | — | `web/index.html` |

## How to run a topic file

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

## Topic roadmap

- **1. Square Pattern**
- **2. Tri Star Pattern**
- **3. Tri No pattern**
- **4. Reverse Num Pattern**
- **5. Alpha Pattern**
- **6. Char Pattern**
- **7. Interesting Alphabet**
- **8. Mirror Image**

## Tradeoff Matrix

Flagship topic: printing 2-D patterns (triangle / pyramid / mirror).

| Approach | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Nested `for` loops, one print per cell | O(rows × cols) | O(1) | Low | Default for any pattern |
| Build each row into a `StringBuilder`, print once | O(rows × cols) | O(cols) | Medium | When I/O latency dominates (many rows) |
| Compute symmetry once, mirror | O(rows × cols/2) | O(1) | Medium | Palindromic / mirror patterns |
| Recursive row printer | O(rows × cols) | O(rows) stack | Medium | When recursion is the lesson, not the goal |

## Anti-patterns to avoid

- **Reaching for `String += ch` in a hot loop** — `String` is immutable in Java; every `+=` allocates a new object, turning an O(n) pattern into O(n²). Use `StringBuilder`.
- **Computing the row count and the spaces independently** — they're linked. Express spaces as `total - row` (or similar) in one place; don't maintain two counters that must agree.
- **Hard-coding the pattern for n=5 and hoping it generalizes** — always parameterize by `n` from the start. Patterns that only work for one size are a sign you haven't found the invariant.
- **Mixing `print` and `println` inconsistently** — forgetting a single newline shifts everything below it and makes the bug look like an off-by-one in the loop. Print exactly one `\n` at the end of each row.
- **Confusing row index with row width** — in an inverted pyramid, the printed character count *decreases* with row index. Draw two rows on paper before coding to confirm direction.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach nested loops in one minute, what's the one sentence you'd use?
- Did you find yourself drawing the pattern on paper before coding? Did it help?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
