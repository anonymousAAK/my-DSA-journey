# Graph Coloring in Compilers

## The problem

A CPU has a small fixed number of registers (16 general-purpose on x86-64, 31 on ARM64). A program, after the compiler's optimization passes, has hundreds or thousands of "virtual" variables that all want to live in registers because RAM access is 100x slower. The compiler's job: assign each virtual variable to a physical register, while ensuring that two variables which need to hold distinct values at the same time aren't given the same register. When you run out of registers, "spill" some variables to the stack — accepting the slowdown.

This is one of the oldest classic compiler problems, and the standard solution is a beautiful reduction to **graph coloring** — a problem you can teach in Week 18.

## Why the obvious approach didn't work

The naïve approach: walk the program top to bottom, assigning each variable the first free register. This works for tiny programs but fails immediately because of scope: variable A might be needed in the early part of the function, variable B in the middle, variable C at the end — they're never alive simultaneously, so they can all share one register. A linear scan that doesn't know about lifetimes assigns them three different registers.

A slightly smarter approach: track "liveness" — the set of variables alive at each instruction. Assign each variable to a register and prove no conflict. But how to do that systematically? The breakthrough (Chaitin 1981 at IBM) is to construct an **interference graph**.

## What they actually use

The classic register allocation pipeline:

1. **Liveness analysis.** Compute, for each instruction, the set of variables alive at that point. A variable is alive if its value will be read before being overwritten.

2. **Build the interference graph.** Create a graph where each node is a variable. Add an edge between two variables iff they are alive at the same instruction. Edges mean "these two cannot share a register."

3. **Graph color** the interference graph with K colors, where K = number of physical registers. If a coloring exists, each color corresponds to a register; assign variables accordingly. **Done.**

Graph coloring is **NP-hard in general**, but the structure of real interference graphs (typically planar-ish, with bounded treewidth) makes them tractable in practice. The most-used algorithm is **Chaitin's algorithm**:

- Repeatedly find a node with fewer than K neighbors (a node that can definitely be colored once its neighbors are). Push it on a stack and remove it from the graph.
- If at some point every remaining node has ≥ K neighbors, **spill**: pick one (using a heuristic like "least-used / highest-degree"), spill it to the stack (load/store on each use), remove it from the graph.
- Pop the stack; for each node, assign it a color different from all its already-colored neighbors. Since it had < K neighbors when pushed, a color is guaranteed available.

The result: a register assignment for the non-spilled variables and a small set of spilled variables that pay the cost of memory access. For typical functions, almost everything stays in registers; only edge cases (pathological code with very many simultaneously-live values) spill significantly.

Modern compilers (LLVM, GCC) use refined variants: **iterated register coalescing** (handle MOV instructions by combining their source and destination into one node when safe), **biased coloring** (prefer specific physical registers for specific operations to enable better instruction encoding), and **linear-scan allocation** (a faster, less optimal alternative used in JIT compilers like V8 and HotSpot, where compile time matters more than optimal allocation).

## The tradeoff

The fundamental tradeoff: **compile time vs. code quality**.

- Chaitin-style graph coloring produces high-quality allocations but is slow on large functions (interference graph construction alone can be quadratic in the number of variables).
- Linear-scan allocation is fast (linear in instruction count) but produces lower-quality allocations — more spills. JIT compilers use it because they care about compile time.
- AOT compilers (LLVM/GCC with -O2/-O3) use graph coloring with significant tuning.

Another tradeoff: **which variables to spill**. Spilling a variable used in a tight loop is catastrophic — every iteration pays a memory roundtrip. Heuristics weight by use-frequency, often factoring in loop nesting depth. Get this wrong and your "optimized" code is slower than -O0.

A subtle tradeoff: **register classes**. Real CPUs have multiple register banks (general-purpose, floating point, vector). The interference graph is sometimes split into per-class subgraphs and colored independently, sometimes coupled when registers can cross classes.

## You can implement a toy version of this using Week 18

- Week 18 (graph coloring and related) — implement greedy graph coloring on a small graph. Implement the Welsh-Powell heuristic (color in descending order of degree). On small graphs (n ≤ 20), compare against brute-force optimal coloring.
- Implement Chaitin's algorithm: removal of low-degree nodes onto a stack, then pop and color. ~50 lines.

A weekend project: build a tiny "compiler" that takes a sequence of three-address-code instructions like `t1 = a + b; t2 = t1 * c; t3 = t2 - a; return t3`, computes liveness, builds the interference graph, and colors it with K registers. Print the resulting register assignment. Add spill handling by reserving one register as a "spill scratch" and rewriting instructions to load/store the spilled variable.

Stretch: take a real LLVM IR snippet (LLVM `clang -S -emit-llvm` will produce one from any C function), build the interference graph from it, color, and compare your assignment to what LLVM actually produced. They'll often differ — LLVM does coalescing and biased coloring you didn't implement — but you'll see the same problem in action.

The deep lesson: **modeling a real-world problem as graph coloring is a master move.** Once you do, you've translated a vague compiler problem into a well-studied algorithmic one with known heuristics. The same trick applies to:

- **Scheduling exam timetables**: events = nodes, conflicts (shared students) = edges, color = time slot.
- **Frequency assignment in cellular networks**: cells = nodes, geographic proximity = edges, color = frequency band.
- **Sudoku**: cells = nodes, same-row/column/box = edges, colors = digits 1-9.

The Week 18 graph-coloring unit is the seed. The fruit ranges from compilers to phone networks to puzzle games. The pattern travels — and recognizing the pattern in a new problem is the real skill.
