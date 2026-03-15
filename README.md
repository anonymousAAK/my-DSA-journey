# My DSA Journey — Beginner to Research-Advanced

![Weeks](https://img.shields.io/badge/Weeks-30-blue)
![Languages](https://img.shields.io/badge/Languages-Java%20%7C%20C%2B%2B%20%7C%20Python%20%7C%20Rust-green)
![Level](https://img.shields.io/badge/Level-Beginner%20to%20Research-orange)
![Interactive](https://img.shields.io/badge/Interactive-HTML%20Pages-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

> A comprehensive, 30-week structured guide to mastering Data Structures and Algorithms — from first principles to research-level topics and interview mastery.

All implementations available in **4 languages**: Java, Python, C++, and Rust — with detailed comments, complexity analysis, and test cases.

---

### Interactive Learning Pages

Every week includes a beautifully designed **interactive HTML page** (`index.html`) that you can open in any browser. No build tools, no dependencies — just open the file!

| Feature | Description |
|---------|-------------|
| **Dark Theme** | Eye-friendly dark UI with gradient accents |
| **Multi-Language Code Viewer** | Tabbed code blocks for Java, C++, Python, and Rust |
| **Copy to Clipboard** | One-click copy for all code snippets |
| **Syntax Highlighting** | Keywords, strings, comments, and functions colored |
| **Line Numbers** | Every code block has line numbers |
| **Sidebar Navigation** | Fixed sidebar with scroll-spy active link highlighting |
| **Scroll Animations** | Cards reveal with smooth fade-in as you scroll |
| **Visual Diagrams** | ASCII art diagrams for algorithm walkthroughs |
| **Complexity Tables** | Side-by-side time & space comparisons |
| **Practice Problems** | Curated LeetCode problems with difficulty badges |
| **Progress Bar** | Reading progress indicator at the top |
| **Responsive** | Mobile-friendly with hamburger menu |
| **Print-Ready** | Clean print styles for offline study |

> Open any `Week N/index.html` in your browser to start learning!

---

### Languages

| Language | File Extension | Notes |
|----------|---------------|-------|
| **Java** | `.java` | Original implementations, numbered by topic |
| **Python** | `.py` | Idiomatic Python with type hints, list comprehensions, `heapq`, `collections` |
| **C++** | `.cpp` | Modern C++17, STL-heavy, competitive programming style |
| **Rust** | `.rs` | Ownership-safe, uses `std::collections`, idiomatic iterators |

Each week folder contains all four languages side by side. Pick your preferred language or study all four to understand trade-offs!

---

## Table of Contents

- [Learning Paths](#learning-paths)
- [How to Use This Guide](#how-to-use-this-guide)
- [Curriculum Overview](#curriculum-overview)
- [Week-by-Week Breakdown](#week-by-week-breakdown)
- [Complexity Reference](#complexity-reference)
- [Data Structure Reference](#data-structure-reference)
- [Problem-Solving Patterns](#problem-solving-patterns)
- [Resources](#resources)
- [FAQ](#faq)
- [Contributing](#contributing)

---

## Learning Paths

Not sure where to start? Choose a path based on your goal:

### Path 1: Complete Beginner (Weeks 1-10)
```
Week 1 → Week 2 → Week 3 → Week 4 → Week 5 → Week 6 → Week 7 → Week 8 → Week 9 → Week 10
  ↓         ↓         ↓         ↓         ↓         ↓         ↓         ↓         ↓         ↓
Java     Control    Loops   Patterns  Recursion  Arrays   Strings  Search   Sorting   Matrix
Basics    Flow     & Math                                                    Algos
```

### Path 2: Interview Prep (8 weeks)
```
Week 6 → Week 8 → Week 11 → Week 14 → Week 16 → Week 17 → Week 18 → Week 30
Arrays   Search    Lists     Trees     Hashing   Graphs     DP      Patterns
```

### Path 3: Competitive Programming (10 weeks)
```
Week 9 → Week 17 → Week 18 → Week 20 → Week 21 → Week 22 → Week 23 → Week 25 → Week 26 → Week 28
Sorting  Graphs     DP      Backtrack  Adv Trees  Adv Graph  Adv DP   Strings   Flows    Game Theory
```

### Path 4: System Design + DSA (6 weeks)
```
Week 16 → Week 14 → Week 21 → Week 22 → Week 24 → Week 29
Hashing   Trees    Adv Trees  Adv Graph  Research  Sys Design
```

---

## How to Use This Guide

1. **Beginners**: Start at Week 1 and progress sequentially. Don't skip weeks.
2. **Intermediate**: Jump to Week 8 (Searching) or Week 11 (Linked Lists) depending on your comfort level.
3. **Advanced**: Weeks 18-24 cover DP, advanced graphs, and research-level topics.
4. **Interview prep**: Follow the Interview Prep learning path above, then do Week 30.
5. Each week folder contains implementations in Java, Python, C++, and Rust.
6. Every file includes: Problem statement → Approach/Pseudocode → Implementation → Complexity Analysis.
7. **Language learners**: Compare implementations across languages to understand design differences.
8. **Open the HTML pages**: Each week has an `index.html` with interactive explanations, diagrams, and code you can copy directly.

---

## Curriculum Overview

| Phase | Weeks | Topics | Level |
|-------|-------|--------|-------|
| **Phase 1: Foundations** | 1–5 | Java basics, control flow, loops, patterns, recursion | Beginner |
| **Phase 2: Core DSA** | 6–10 | Arrays, strings, searching, sorting, 2D arrays | Beginner–Intermediate |
| **Phase 3: Linear Structures** | 11–13 | Linked lists, stacks, queues | Intermediate |
| **Phase 4: Non-Linear Structures** | 14–16 | Trees, heaps, hash tables | Intermediate |
| **Phase 5: Graph Theory** | 17 | Graph representations, BFS, DFS | Intermediate |
| **Phase 6: Algorithmic Paradigms** | 18–20 | Dynamic programming, greedy, backtracking | Advanced |
| **Phase 7: Advanced Topics** | 21–22 | Advanced trees, advanced graphs | Advanced |
| **Phase 8: Research Level** | 23–24 | Advanced DP, NP-completeness, approximation, randomized algorithms | Research |
| **Phase 9: Specialist Topics** | 25–27 | Advanced strings, network flow, computational geometry | Research |
| **Phase 10: Mastery** | 28–30 | Game theory, system design, interview patterns | Expert |

---

## Week-by-Week Breakdown

### Phase 1: Foundations

#### Week 1 — Java Fundamentals
- Installation & setup
- Hello World, comments, data types
- Variables, type casting, input/output
- Arithmetic & logical operators

#### Week 2 — Control Flow
- If-else, nested conditions
- Ternary operator
- While loops, do-while loops
- Real-world problems: salary calc, even/odd, power

#### Week 3 — Loops & Number Theory Basics
- For loops, break & continue
- Variable scope
- Bitwise operators
- Fibonacci, prime numbers, AP sequences
- Binary/decimal conversion

#### Week 4 — Pattern Printing
- Nested loops mastery
- Square, triangle, diamond patterns
- Number & alphabet patterns
- Mirror patterns

#### Week 5 — Functions & Recursion
- Method definition, parameters, return types
- Method overloading
- Call stack & stack frames
- Recursion fundamentals
- Factorial, Fibonacci (recursive)
- Tower of Hanoi
- Tail recursion & optimization

---

### Phase 2: Core DSA

#### Week 6 — Arrays
- Array declaration, initialization, traversal
- Array sum, max, min, average
- Linear search
- Reverse an array
- Rotate an array
- Subarray problems (prefix sum, Kadane's algorithm)
- Dutch National Flag (3-way partition)
- Missing number, duplicates

#### Week 7 — Strings
- String basics in Java (String vs StringBuilder)
- String methods & manipulation
- Palindrome check
- Anagram check
- Reverse words in a string
- String compression / run-length encoding
- Rabin-Karp substring search
- KMP algorithm

#### Week 8 — Searching Algorithms
- Linear Search (review)
- Binary Search (iterative & recursive)
- Binary Search on answer
- Ternary Search
- Exponential Search
- Search in rotated sorted array
- First and last occurrence

#### Week 9 — Sorting Algorithms
- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort (divide & conquer)
- Quick Sort (partition schemes)
- Counting Sort
- Radix Sort
- Heap Sort
- Comparison of all sorts (time & space complexity)

#### Week 10 — 2D Arrays & Matrix
- 2D array declaration & traversal
- Matrix addition & multiplication
- Transpose, rotation
- Spiral traversal
- Diagonal traversal
- Search in sorted matrix
- Pascal's triangle

---

### Phase 3: Linear Structures

#### Week 11 — Linked Lists
- Singly Linked List (CRUD operations)
- Doubly Linked List
- Circular Linked List
- Reverse a linked list (iterative & recursive)
- Detect and remove cycle (Floyd's algorithm)
- Find middle node
- Merge two sorted linked lists
- LRU Cache implementation

#### Week 12 — Stacks
- Stack using arrays & linked list
- Java Stack & Deque
- Balanced parentheses
- Next greater element
- Largest rectangle in histogram
- Min stack
- Stack-based expression evaluation (infix, postfix, prefix)

#### Week 13 — Queues
- Queue using arrays & linked list
- Circular queue
- Deque (double-ended queue)
- Queue using two stacks
- Sliding window maximum (monotonic deque)
- BFS using queue (preview)

---

### Phase 4: Non-Linear Structures

#### Week 14 — Trees
- Binary tree: node structure, traversals (inorder, preorder, postorder)
- Level-order traversal (BFS)
- Height, diameter, mirror of a tree
- Binary Search Tree (BST): insert, delete, search
- Lowest Common Ancestor (LCA)
- Check if BST is valid
- Serialize & deserialize a binary tree

#### Week 15 — Heaps & Priority Queues
- Min-heap & max-heap
- Heapify operations
- Java PriorityQueue
- Heap sort
- Kth largest/smallest element
- Merge K sorted arrays
- Median of a stream

#### Week 16 — Hash Tables & Maps
- Hashing concepts, hash functions
- Collision resolution: chaining, open addressing
- Java HashMap, HashSet, LinkedHashMap
- Two Sum problem
- Subarray with zero sum
- Count distinct elements in a window
- Group anagrams
- Consistent hashing (intro)

---

### Phase 5: Graph Theory

#### Week 17 — Graphs: Fundamentals & Traversals
- Graph representations: adjacency matrix, adjacency list
- Directed vs undirected, weighted vs unweighted
- Depth-First Search (DFS)
- Breadth-First Search (BFS)
- Cycle detection (directed & undirected)
- Topological sort (DFS & Kahn's algorithm)
- Bipartite graph check
- Connected components

---

### Phase 6: Algorithmic Paradigms

#### Week 18 — Dynamic Programming
- Memoization vs tabulation
- Fibonacci (DP), Climbing Stairs
- 0/1 Knapsack (2D and space-optimized)
- Longest Common Subsequence (LCS)
- Longest Increasing Subsequence (LIS)
- Coin change problem
- Subset sum
- Edit Distance
- House Robber, Unique Paths
- DP problem-solving framework

#### Week 19 — Greedy Algorithms
- Greedy paradigm & correctness proofs
- Activity selection problem
- Fractional Knapsack
- Huffman coding
- Job sequencing
- Minimum number of coins
- Interval scheduling & merging
- Jump Game, Gas Station, Task Scheduler
- Greedy vs DP comparison

#### Week 20 — Backtracking
- Backtracking template
- N-Queens problem
- Sudoku solver
- Rat in a maze
- Word search
- Permutations & combinations
- Subset generation
- M-Coloring problem

---

### Phase 7: Advanced Topics

#### Week 21 — Advanced Trees
- AVL Trees (rotations, balancing)
- Red-Black Trees (concepts)
- Segment Trees (range queries, point updates)
- Fenwick Tree / Binary Indexed Tree
- Tries (insert, search, prefix matching)
- Suffix Arrays & suffix trees (intro)

#### Week 22 — Advanced Graph Algorithms
- Dijkstra's shortest path
- Bellman-Ford algorithm
- Floyd-Warshall (all-pairs shortest paths)
- Kruskal's MST (Union-Find / DSU)
- Prim's MST
- Strongly Connected Components (Kosaraju's, Tarjan's)
- Articulation points & bridges
- Euler path & circuit

---

### Phase 8: Research Level

#### Week 23 — Advanced Dynamic Programming
- Bitmask DP
- DP on trees
- DP on intervals
- Digit DP
- Profile DP
- Convex hull trick
- Divide-and-conquer optimization

#### Week 24 — Research-Level Topics
- Amortized analysis (aggregate, accounting, potential method)
- NP-completeness: P vs NP, reductions
- Approximation algorithms (vertex cover, set cover)
- Skip lists
- Bloom filters
- Reservoir sampling
- Streaming algorithms

---

### Phase 9: Specialist Topics

#### Week 25 — Advanced String Algorithms
- Z-Algorithm (pattern matching)
- Rabin-Karp (rolling hash)
- Trie-based pattern matching
- Suffix Array construction
- Manacher's Algorithm (longest palindromic substring)
- String hashing techniques

#### Week 26 — Network Flow & Matching
- Max Flow / Min Cut theorem
- Ford-Fulkerson method
- Edmonds-Karp (BFS-based max flow)
- Bipartite matching
- Hopcroft-Karp algorithm
- Applications: assignment problem, image segmentation

#### Week 27 — Computational Geometry
- Point & line representation
- Cross product & orientation test
- Convex Hull (Graham Scan, Andrew's Monotone Chain)
- Line segment intersection
- Closest pair of points (divide & conquer)
- Polygon area (Shoelace formula)

---

### Phase 10: Mastery

#### Week 28 — Game Theory & Combinatorics
- Nim Game & Sprague-Grundy theorem
- Combinatorics: nCr, Pascal's Triangle
- Catalan numbers & applications
- Inclusion-Exclusion principle
- Matrix exponentiation for recurrences
- Probability in algorithms

#### Week 29 — System Design for Engineers
- Consistent hashing (implementation)
- LRU Cache (HashMap + doubly linked list)
- Rate limiter (Token Bucket / Sliding Window)
- Trie-based autocomplete
- Merkle Tree for data verification
- Min-Heap based task scheduler

#### Week 30 — Interview Patterns & Mastery
- Two Pointers pattern
- Sliding Window pattern
- Fast & Slow Pointers (Floyd's)
- Merge Intervals pattern
- Top-K Elements (heap pattern)
- Monotonic Stack pattern
- Pattern recognition flowchart
- Master roadmap: all 30 weeks at a glance

---

## Complexity Reference

### Searching & Sorting

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n+k) |

### Graph Algorithms

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| BFS/DFS | O(V+E) | O(V) | Traversal |
| Dijkstra | O((V+E) log V) | O(V) | Non-negative weights |
| Bellman-Ford | O(VE) | O(V) | Handles negative weights |
| Floyd-Warshall | O(V³) | O(V²) | All-pairs shortest path |
| Kruskal | O(E log E) | O(V) | MST with Union-Find |
| Prim | O((V+E) log V) | O(V) | MST with priority queue |
| Topological Sort | O(V+E) | O(V) | DAGs only |
| Edmonds-Karp | O(VE²) | O(V²) | Max flow |

### Dynamic Programming (Common Problems)

| Problem | Time | Space | Optimized Space |
|---------|------|-------|-----------------|
| Fibonacci | O(n) | O(n) | O(1) |
| 0/1 Knapsack | O(nW) | O(nW) | O(W) |
| LCS | O(mn) | O(mn) | O(min(m,n)) |
| LIS | O(n log n) | O(n) | — |
| Coin Change | O(n×amount) | O(amount) | — |
| Edit Distance | O(mn) | O(mn) | O(n) |

---

## Data Structure Reference

| Data Structure | Access | Search | Insert | Delete | Space | Notes |
|---------------|--------|--------|--------|--------|-------|-------|
| Array | O(1) | O(n) | O(n) | O(n) | O(n) | Contiguous memory |
| Linked List | O(n) | O(n) | O(1) | O(1) | O(n) | With pointer to position |
| Stack | O(n) | O(n) | O(1) | O(1) | O(n) | LIFO |
| Queue | O(n) | O(n) | O(1) | O(1) | O(n) | FIFO |
| Hash Table | — | O(1)* | O(1)* | O(1)* | O(n) | *Amortized average |
| BST (balanced) | O(log n) | O(log n) | O(log n) | O(log n) | O(n) | AVL / Red-Black |
| Min/Max Heap | O(1)† | O(n) | O(log n) | O(log n) | O(n) | †For min/max only |
| Trie | — | O(L) | O(L) | O(L) | O(ALPHABET×L×n) | L = key length |
| Segment Tree | — | O(log n) | — | O(log n) | O(n) | Range queries |
| Skip List | — | O(log n)* | O(log n)* | O(log n)* | O(n) | *Expected |
| Bloom Filter | — | O(k) | O(k) | — | O(m) bits | Probabilistic |

---

## Problem-Solving Patterns

Use this cheat sheet to identify which technique to apply:

| If you see... | Think... | Week |
|---------------|----------|------|
| "Sorted array" | Binary search | 8 |
| "Top/bottom K elements" | Heap / Priority Queue | 15 |
| "Common substring/subsequence" | Dynamic Programming | 18 |
| "Permutations/combinations" | Backtracking | 20 |
| "Graph with weights" | Dijkstra / Bellman-Ford | 22 |
| "Connected/reachable" | BFS / DFS / Union-Find | 17 |
| "Contiguous subarray" | Sliding Window / Prefix Sum | 6, 30 |
| "Linked list cycle" | Fast & Slow Pointers | 11, 30 |
| "Parentheses/nesting" | Stack | 12 |
| "Frequency count" | HashMap | 16 |
| "Minimum cost/path" | DP or Greedy | 18, 19 |
| "Stream of data" | Reservoir Sampling / Bloom Filter | 24 |
| "Pattern in string" | KMP / Z-Algorithm / Rabin-Karp | 7, 25 |
| "Range query" | Segment Tree / Fenwick Tree | 21 |
| "Scheduling/intervals" | Greedy (sort by end time) | 19 |
| "Game / optimal play" | Sprague-Grundy / Minimax | 28 |

---

## Resources

### Books
- *Introduction to Algorithms* (CLRS) — Cormen et al. [Essential reference]
- *Algorithm Design* — Kleinberg & Tardos [Excellent explanations]
- *The Algorithm Design Manual* — Skiena [Practical focus]
- *Competitive Programming 3* — Steven Halim
- *Programming Pearls* — Jon Bentley
- *Cracking the Coding Interview* — Gayle McDowell [Interview-focused]

### Online Platforms
- [LeetCode](https://leetcode.com) — Interview prep & contests
- [Codeforces](https://codeforces.com) — Competitive programming
- [AtCoder](https://atcoder.jp) — High-quality problems
- [CSES Problem Set](https://cses.fi/problemset/) — Structured DP & graph problems
- [CP-Algorithms](https://cp-algorithms.com) — Reference implementations
- [NeetCode](https://neetcode.io) — Curated problem lists with video explanations
- [Visualgo](https://visualgo.net) — Algorithm visualizations

### Courses
- MIT 6.006 — Introduction to Algorithms (free on MIT OpenCourseWare)
- MIT 6.046J — Design and Analysis of Algorithms
- Stanford's Algorithms Specialization (Coursera)
- Princeton Algorithms I & II (Coursera, by Robert Sedgewick)

### YouTube Channels
- Abdul Bari — Clear algorithm explanations
- William Fiset — Graph theory focus
- Errichto — Competitive programming
- NeetCode — LeetCode problem walkthroughs

---

## FAQ

**Q: What order should I study the languages in?**
A: Start with the language you're most comfortable with. Java is the primary language in this guide, but all four implementations are equivalent. If learning a new language, compare it side-by-side with one you know.

**Q: How long does this guide take to complete?**
A: At the suggested pace (one week per topic, ~8-12 hours/week), the full 30-week curriculum takes about 7-8 months. The interview prep path can be completed in 8 weeks of focused study.

**Q: Do I need to learn all 4 languages?**
A: No! Pick one language and stick with it. The multi-language support is for those who want to compare approaches or learn a new language through familiar algorithms.

**Q: Is this guide sufficient for coding interviews?**
A: Yes. Weeks 1-20 cover all major topics tested in coding interviews at top tech companies. Week 30 specifically covers the most common interview patterns. Supplement with practice on LeetCode.

**Q: What if I already know the basics?**
A: Use the learning paths section above to find a path that matches your level. The Interview Prep path skips foundations and focuses on the most commonly tested topics.

**Q: How do I run the code?**
A: See the [Quick Start](#quick-start) section below. Each file is self-contained with a `main` method/function and test cases.

**Q: Can I contribute?**
A: Absolutely! See the [Contributing](#contributing) section. We welcome implementations in additional languages too.

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/week-X-topic`
3. Follow the file naming conventions:
   - Java: `N.TopicName.java`
   - Python: `topic_name.py`
   - C++: `topic_name.cpp`
   - Rust: `topic_name.rs`
4. Each file must include:
   - Problem description (comment block)
   - Approach/pseudocode
   - Implementation
   - Time & space complexity
   - Test cases in main function
5. Open a pull request

Contributions in **any language** are welcome — Go, TypeScript, Kotlin, C#, etc!

---

> **Note on file numbering**: When files are numbered (e.g., `10.TopicName.java`), `10` comes after `9`, not after `1`. Files are listed in logical learning order.

## Project Structure

```
my-DSA-journey/
├── README.md                    # This file
├── Week 1/
│   ├── index.html               # Interactive learning page (open in browser)
│   ├── 1.TopicName.java         # Java implementation (numbered)
│   ├── 2.AnotherTopic.java
│   ├── topic_name.py            # Python implementation
│   ├── topic_name.cpp           # C++ implementation
│   └── topic_name.rs            # Rust implementation
├── Week 2/
│   ├── index.html
│   └── ...
├── ...
└── Week 30/
    ├── index.html
    └── ...
```

## Quick Start

```bash
# Open interactive learning page
open "Week 1/index.html"    # macOS
xdg-open "Week 1/index.html"  # Linux

# Java
javac "Week 8/1.BinarySearch.java" && java -cp "Week 8" BinarySearch

# Python
python3 "Week 8/searching.py"

# C++
g++ -std=c++17 -O2 "Week 8/searching.cpp" -o searching && ./searching

# Rust
rustc "Week 8/searching.rs" && ./searching
```

---

Made with dedication, one algorithm at a time.
