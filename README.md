# My DSA Journey — Beginner to Research-Advanced

> A comprehensive, multi-week structured guide to mastering Data Structures and Algorithms — from first principles to research-level topics.

All implementations are in **Java** with detailed comments, complexity analysis, and links to practice problems. Contributions in other languages are welcome!

---

## Table of Contents

- [How to Use This Guide](#how-to-use-this-guide)
- [Curriculum Overview](#curriculum-overview)
- [Week-by-Week Breakdown](#week-by-week-breakdown)
- [Complexity Reference](#complexity-reference)
- [Resources](#resources)
- [Contributing](#contributing)

---

## How to Use This Guide

1. **Beginners**: Start at Week 1 and progress sequentially. Don't skip weeks.
2. **Intermediate**: Jump to Week 8 (Searching) or Week 11 (Linked Lists) depending on your comfort level.
3. **Advanced**: Weeks 18-24 cover DP, advanced graphs, and research-level topics.
4. Each week folder contains numbered `.java` files and concept explanation files.
5. Every file includes: Problem statement → Approach/Pseudocode → Implementation → Complexity Analysis.

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

#### Week 18 — Dynamic Programming (Introduction)
- Memoization vs tabulation
- Fibonacci (DP)
- 0/1 Knapsack
- Longest Common Subsequence (LCS)
- Longest Increasing Subsequence (LIS)
- Coin change problem
- Subset sum
- Partition equal subset sum

#### Week 19 — Greedy Algorithms
- Greedy paradigm & correctness proofs
- Activity selection problem
- Fractional Knapsack
- Huffman coding
- Job sequencing
- Minimum number of coins
- Interval scheduling & merging

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
- Amortized analysis (accounting, potential method)
- NP-completeness: P vs NP, reductions
- Approximation algorithms (vertex cover, TSP, set cover)
- Randomized algorithms (quicksort analysis, hashing)
- Skip lists
- Bloom filters
- Cache-oblivious algorithms
- External memory algorithms
- Streaming algorithms (count-min sketch, reservoir sampling)
- Persistent data structures

---

## Complexity Reference

| Algorithm | Best | Average | Worst | Space |
|-----------|------|---------|-------|-------|
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) |
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) |
| BFS/DFS | O(V+E) | O(V+E) | O(V+E) | O(V) |
| Dijkstra | — | O((V+E) log V) | O((V+E) log V) | O(V) |
| Kruskal | — | O(E log E) | O(E log E) | O(V) |

---

## Resources

### Books
- *Introduction to Algorithms* (CLRS) — Cormen et al. [Essential reference]
- *Algorithm Design* — Kleinberg & Tardos [Excellent explanations]
- *The Algorithm Design Manual* — Skiena [Practical focus]
- *Competitive Programming 3* — Steven Halim
- *Programming Pearls* — Jon Bentley

### Online Platforms
- [LeetCode](https://leetcode.com) — Interview prep & contests
- [Codeforces](https://codeforces.com) — Competitive programming
- [AtCoder](https://atcoder.jp) — High-quality problems
- [CSES Problem Set](https://cses.fi/problemset/) — Structured DP & graph problems
- [CP-Algorithms](https://cp-algorithms.com) — Reference implementations

### Courses
- MIT 6.006 — Introduction to Algorithms (free on MIT OpenCourseWare)
- MIT 6.046J — Design and Analysis of Algorithms
- Stanford's Algorithms Specialization (Coursera)

---

## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/week-X-topic`
3. Follow the file naming convention: `N.TopicName.java`
4. Each file must include:
   - Problem description (comment block)
   - Approach/pseudocode
   - Implementation
   - Time & space complexity
5. Open a pull request

Contributions in languages other than Java are very welcome!

---

> **Note on file numbering**: When files are numbered (e.g., `10.TopicName.java`), `10` comes after `9`, not after `1`. Files are listed in logical learning order.
