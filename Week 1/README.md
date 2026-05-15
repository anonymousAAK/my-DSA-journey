# Week 1

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | Java Installation | `java/1.Java Installation` | `python/1.installation.py` | `cpp/1.installation.cpp` | `rust/s01_installation.rs` | `web/1.installation.html` |
| 2 | hello world | `java/2.hello_world.java` | `python/2.hello_world.py` | `cpp/2.hello_world.cpp` | `rust/s02_hello_world.rs` | `web/2.hello_world.html` |
| 3 | Better Hello World | `java/3.Better_Hello_World.java` | `python/3.better_hello_world.py` | `cpp/3.better_hello_world.cpp` | `rust/s03_better_hello_world.rs` | `web/3.better_hello_world.html` |
| 4 | Add two numbers | `java/4.Add_two_numbers.java` | `python/4.add_two_numbers.py` | `cpp/4.add_two_numbers.cpp` | `rust/s04_add_two_numbers.rs` | `web/4.add_two_numbers.html` |
| 5 | Arithmetic Operation | `java/5.Arithmetic_Operation.java` | `python/5.arithmetic_operation.py` | `cpp/5.arithmetic_operation.cpp` | `rust/s05_arithmetic_operation.rs` | `web/5.arithmetic_operation.html` |
| 6 | Taking Input | `java/6.Taking_Input.java` | `python/6.taking_input.py` | `cpp/6.taking_input.cpp` | `rust/s06_taking_input.rs` | `web/6.taking_input.html` |
| 7 | Taking Input all | `java/7.Taking_Input_all.java` | `python/7.taking_input_all.py` | `cpp/7.taking_input_all.cpp` | `rust/s07_taking_input_all.rs` | `web/7.taking_input_all.html` |
| 8 | Add two number better | `java/8.Add_two_number_better.java` | `python/8.add_two_number_better.py` | `cpp/8.add_two_number_better.cpp` | `rust/s08_add_two_number_better.rs` | `web/8.add_two_number_better.html` |
| 9 | Data Types | `java/9.Data_Types.java` | `python/9.data_types.py` | `cpp/9.data_types.cpp` | `rust/s09_data_types.rs` | `web/9.data_types.html` |
| 10 | Multiple input | `java/10.Multiple_input.java` | `python/10.multiple_input.py` | `cpp/10.multiple_input.cpp` | `rust/s10_multiple_input.rs` | `web/10.multiple_input.html` |
| 11 | Integer and String | `java/11.Integer_and_String.java` | `python/11.integer_and_string.py` | `cpp/11.integer_and_string.cpp` | `rust/s11_integer_and_string.rs` | `web/11.integer_and_string.html` |
| 12 | Average of two numbers | `java/12.Average_of_two_numbers.java` | `python/12.average_of_two_numbers.py` | `cpp/12.average_of_two_numbers.cpp` | `rust/s12_average_of_two_numbers.rs` | `web/12.average_of_two_numbers.html` |
| 13 | How Integer is Stored | `java/13.How Integer is Stored.java` | `python/13.how_integer_is_stored.py` | `cpp/13.how_integer_is_stored.cpp` | `rust/s13_how_integer_is_stored.rs` | `web/13.how_integer_is_stored.html` |
| 14 | How other datatype are stores | `java/14. How other datatype are stores.java` | `python/14.how_other_datatypes_are_stored.py` | `cpp/14.how_other_datatypes_are_stored.cpp` | `rust/s14_how_other_datatypes_are_stored.rs` | `web/14.how_other_datatypes_are_stored.html` |
| 15 | Typecasting | `java/15.Typecasting.java` | `python/15.typecasting.py` | `cpp/15.typecasting.cpp` | `rust/s15_typecasting.rs` | `web/15.typecasting.html` |
| 16 | Operators in java | `java/16.Operators_in_java` | `python/16.operators.py` | `cpp/16.operators.cpp` | `rust/s16_operators.rs` | `web/16.operators.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Fundamentals | — | `python/fundamentals.py` | `cpp/fundamentals.cpp` | `rust/fundamentals.rs` | — |
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

- **1. Java Installation**
- **2. hello world**
- **3. Better Hello World**
- **4. Add two numbers**
- **5. Arithmetic Operation**
- **6. Taking Input**
- **7. Taking Input all**
- **8. Add two number better**
- **9. Data Types**
- **10. Multiple input**
- **11. Integer and String**
- **12. Average of two numbers**
- **13. How Integer is Stored**
- **14. How other datatype are stores**
- **15. Typecasting**
- **16. Operators in java**

## Tradeoff Matrix

Flagship topic: reading input and printing output (Scanner vs BufferedReader vs args).

| Approach | Time | Space | Code complexity | When to prefer |
|----------|------|-------|-----------------|----------------|
| `System.out.println` + `Scanner` | O(N) I/O | O(1) extra | Low | Tiny programs (< 10⁴ tokens), tutorials |
| `BufferedReader` + `StringTokenizer` | O(N) I/O, ~5–10× faster | O(line) | Medium | Competitive programming, large inputs |
| `DataInputStream` byte reader | O(N), fastest | O(buf) | High | Hot loops with 10⁶+ tokens |
| Command-line `args[]` | O(args) | O(1) | Low | Fixed-size config, scripts driven by shell |

## Anti-patterns to avoid

- **Calling `sc.nextInt()` then `sc.nextLine()` and being surprised the second returns empty** — `nextInt` leaves the trailing newline in the buffer; either consume it with an extra `nextLine()` or use `nextLine()` + `Integer.parseInt` consistently.
- **Reusing one `Scanner` and closing it inside a helper** — closing a `Scanner` over `System.in` closes `System.in` itself, so later reads silently fail. Don't close stdin scanners.
- **Mixing `int` and `double` in arithmetic and expecting fractional results** — `5/2` is `2`, not `2.5`. Cast one operand to `double` first, or use a `double` literal.
- **Comparing strings with `==`** — `==` checks reference identity, not content. Use `.equals()`. This bites people on day one and never fully stops biting.
- **Believing `int` can hold any number** — Java `int` overflows silently past 2³¹−1. Use `long` for products, factorials, or anything that could exceed ~2·10⁹.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach a beginner how Java stores an `int` in one minute, what's the one sentence you'd use?
- Did you hit any silent type-conversion bugs (e.g. integer division)? How did you spot them?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
