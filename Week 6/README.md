# Week 6

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | ReturnArraySum | `java/1.ReturnArraySum.java` | `python/1.return_array_sum.py` | `cpp/1.return_array_sum.cpp` | `rust/s01_return_array_sum.rs` | `web/1.return_array_sum.html` |
| 2 | LinearSearch | `java/2.LinearSearch.java` | `python/2.linear_search.py` | `cpp/2.linear_search.cpp` | `rust/s02_linear_search.rs` | `web/2.linear_search.html` |
| 3 | ArrayReverseAndRotate | `java/3.ArrayReverseAndRotate.java` | `python/3.array_reverse_and_rotate.py` | `cpp/3.array_reverse_and_rotate.cpp` | `rust/s03_array_reverse_and_rotate.rs` | `web/3.array_reverse_and_rotate.html` |
| 4 | PrefixSumAndKadane | `java/4.PrefixSumAndKadane.java` | `python/4.prefix_sum_and_kadane.py` | `cpp/4.prefix_sum_and_kadane.cpp` | `rust/s04_prefix_sum_and_kadane.rs` | `web/4.prefix_sum_and_kadane.html` |
| 5 | DutchNationalFlagAndMissing | `java/5.DutchNationalFlagAndMissing.java` | `python/5.dutch_national_flag_and_missing.py` | `cpp/5.dutch_national_flag_and_missing.cpp` | `rust/s05_dutch_national_flag_and_missing.rs` | `web/5.dutch_national_flag_and_missing.html` |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Arrays | — | `python/arrays.py` | `cpp/arrays.cpp` | `rust/arrays.rs` | — |
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

- **1. ReturnArraySum**
- **2. LinearSearch**
- **3. ArrayReverseAndRotate**
- **4. PrefixSumAndKadane**
- **5. DutchNationalFlagAndMissing**
