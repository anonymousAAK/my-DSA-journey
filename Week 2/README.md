# Week 2

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | Data Types review | `java/1.Data_Types_review.java` | `python/1.data_types_review.py` | `cpp/1.data_types_review.cpp` | `rust/s01_data_types_review.rs` | `web/1.data_types_review.html` |
| 2 | If else | `java/2.If_else.java` | `python/2.if_else.py` | `cpp/2.if_else.cpp` | `rust/s02_if_else.rs` | `web/2.if_else.html` |
| 3 | Find Character Case | `java/3.Find_Character_Case.java` | `python/3.find_character_case.py` | `cpp/3.find_character_case.cpp` | `rust/s03_find_character_case.rs` | `web/3.find_character_case.html` |
| 4 | While Loop | `java/4.While_Loop.java` | `python/4.while_loop.py` | `cpp/4.while_loop.cpp` | `rust/s04_while_loop.rs` | `web/4.while_loop.html` |
| 5 | Infinite Loop | `java/5.Infinite_Loop.java` | `python/5.infinite_loop.py` | `cpp/5.infinite_loop.cpp` | `rust/s05_infinite_loop.rs` | `web/5.infinite_loop.html` |
| 6 | Fahrenheit to Celsius Table | `java/6.Fahrenheit_to_Celsius_Table.java` | `python/6.fahrenheit_to_celsius_table.py` | `cpp/6.fahrenheit_to_celsius_table.cpp` | `rust/s06_fahrenheit_to_celsius_table.rs` | `web/6.fahrenheit_to_celsius_table.html` |
| 7 | Total Salary | `java/7.Total_Salary.java` | `python/7.total_salary.py` | `cpp/7.total_salary.cpp` | `rust/s07_total_salary.rs` | `web/7.total_salary.html` |
| 8 | Multiplication Table | `java/8.Multiplication_Table.java` | `python/8.multiplication_table.py` | `cpp/8.multiplication_table.cpp` | `rust/s08_multiplication_table.rs` | `web/8.multiplication_table.html` |
| 9 | Sum of Even Odd | `java/9.Sum_of_Even_Odd.java` | `python/9.sum_of_even_odd.py` | `cpp/9.sum_of_even_odd.cpp` | `rust/s09_sum_of_even_odd.rs` | `web/9.sum_of_even_odd.html` |
| 10 | Factors | `java/10.Factors.java` | `python/10.factors.py` | `cpp/10.factors.cpp` | `rust/s10_factors.rs` | `web/10.factors.html` |
| 11 | Find Power | `java/11.Find_Power.java` | `python/11.find_power.py` | `cpp/11.find_power.cpp` | `rust/s11_find_power.rs` | `web/11.find_power.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Control Flow | — | `python/control_flow.py` | `cpp/control_flow.cpp` | `rust/control_flow.rs` | — |
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

- **1. Data Types review**
- **2. If else**
- **3. Find Character Case**
- **4. While Loop**
- **5. Infinite Loop**
- **6. Fahrenheit to Celsius Table**
- **7. Total Salary**
- **8. Multiplication Table**
- **9. Sum of Even Odd**
- **10. Factors**
- **11. Find Power**

## Tradeoff Matrix

Flagship topic: computing `a^b` (Find_Power).

| Approach | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| Repeated multiplication (`for i in 1..b`) | O(b) | O(1) | Low | Tiny exponents, learning loops |
| `Math.pow(a, b)` | O(1) amortized | O(1) | Lowest | When `double` precision is acceptable |
| Fast exponentiation (binary) | O(log b) | O(1) iterative / O(log b) recursive | Medium | Large `b`, modular exponentiation |
| Lookup table | O(1) | O(range) | Low | Fixed small domain (e.g. powers of 2 up to 30) |

## Anti-patterns to avoid

- **Using `Math.pow` for integer answers** — it returns `double`, and `(int) Math.pow(10, 18)` will give you a wrong, off-by-a-few value because doubles only carry ~15 significant digits. Roll your own loop or use `BigInteger.pow`.
- **Infinite `while` loops because the update is missing or wrong-signed** — `while (n > 0)` with `n--` works; `while (n > 0)` with `n++` runs forever. Always read your loop body and ask "does this make progress toward the exit condition?".
- **Off-by-one in `for (int i = 0; i <= n; i++)` vs `i < n`** — running one iteration too many is the single most common arithmetic bug. Decide whether `n` is inclusive or exclusive *before* you write the loop.
- **Using `if (x = 0)` instead of `==`** — Java will reject this for booleans but it still trips C-trained brains. Read the condition aloud: "if x equals zero", not "if x is zero".
- **Treating `char` as a string** — `'A'` is not `"A"`. They behave differently in concatenation and switch statements.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach `if/else` vs `while` in one sentence, what would you say?
- Did your loops ever run one too many or one too few times? How did you debug it?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
