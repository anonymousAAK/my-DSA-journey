# Git's Commit Graph as a DAG, Why Topological Sort Matters

## The problem

Git tracks the history of a codebase. Every commit references its parent commit(s), forming a graph. That graph is a **directed acyclic graph** — directed (commits point to their parents, time flows one way), and acyclic (you can't be your own ancestor). Almost every interesting Git operation is a graph-algorithm query on this DAG: "Is commit A an ancestor of commit B?" "What's the most recent common ancestor of these two branches?" "List all commits between these two tags in a sensible order."

This works at the scale of small toys (10 commits) the same way it works on the Linux kernel (~1.4M commits, 80k+ files). The same algorithms, just bigger.

## Why the obvious approach didn't work

Early version-control systems (CVS, Subversion) treated history as a *linear* sequence of revisions. That model breaks the moment two people branch and merge — there's no single "order." Subversion punted: it tracked file revisions but had no first-class notion of branches as graph operations. Merges were lossy.

Linus's insight when designing Git: **history is fundamentally a DAG**, not a sequence. Each commit has zero, one (a normal commit), or two+ (a merge) parents. Once you commit to the DAG model, the right algorithms practically suggest themselves — they're all standard graph traversals.

The naïve implementation: store each commit as a record on disk, walk the graph live for every query. This works for small repos but falls over on huge ones. `git log` on the Linux kernel naively would walk 1.4M commits to render the first page.

## What they actually use

Git's core graph operations are textbook DAG algorithms, with industrial-strength optimizations:

1. **`git log`** is a topological-sort-flavored traversal. Start from HEAD, walk backwards via parent pointers, output commits. To get them in a sensible order across merged branches, it does a topological sort (Week 17): emit a commit only after all its children have been emitted. This is Kahn's algorithm in production.

2. **`git merge-base A B`** finds the **lowest common ancestor** of two commits — the most recent commit that is an ancestor of both. This is the LCA problem on a DAG (not a tree, because merges create multiple parents). Git uses a BFS from both A and B simultaneously, marking nodes as visited from each side, and the first node reached from both sides is a merge base. There may be multiple incomparable merge bases (a fact that complicates `git merge`'s "criss-cross" handling).

3. **`git rebase`** topologically replays commits from one branch onto another. The "what commits to replay" question is "what's reachable from HEAD but not from the target?" — a graph reachability problem.

4. **`git bisect`** is a binary search **on the DAG**. Given a known-good commit and a known-bad commit, find the first bad commit. Because the history is a graph not a line, "binary search" means halving by *reachability* — pick a midpoint by counting commits reachable from bad-but-not-good and halving the candidate set. This is graph-aware binary search (Week 20-ish material), and it's beautiful.

5. **Performance**: Git stores **commit-graph files** (a packed, indexed representation of the DAG, with generation numbers — basically per-node topological-distance labels) so that reachability and ancestor queries can avoid walking the whole graph. Generation numbers convert "is A an ancestor of B?" from a BFS into "is gen(A) ≤ gen(B), and a focused BFS confirming." On the kernel repo this is the difference between minutes and milliseconds.

## The tradeoff

Storing the DAG as objects on disk (one file per commit) gives **infinite history without needing to load anything** — Git can be lazy. The tradeoff is that for fast queries, you need *additional* structure (the commit-graph file, packed object indexes) that has to be maintained as new commits arrive. Git used to be slow on huge repos because that auxiliary structure didn't exist yet; it was added in Git 2.18+ and made operations like `git log --graph` viable on enormous histories.

The other tradeoff is **immutability**. Because the DAG is content-addressed (each commit's ID is a hash of its contents including parent IDs), you can never "edit" a commit — only create new ones. This makes the DAG monotonically growing, simplifies caching enormously, and is also why `git rebase` is "rewriting history" by creating new commits, not modifying old ones.

## You can implement a toy version of this using Week 17

- Week 17 (graph traversal, topological sort) — implement Kahn's algorithm on a small DAG. That's `git log --topo-order` in 30 lines.
- Implement LCA on a DAG via two-source BFS. Test it on a hand-built DAG with a merge (A → B → D, A → C → D, find LCA of B and C). That's `git merge-base`.
- Build a toy "mini-git": a `commit` command that creates a new commit (with parent = current HEAD), a `branch` command, a `merge` command. Store commits as JSON files. Now implement `log` and `merge-base` against your own DAG. You will discover all the same problems Git did — and the same solutions feel natural.

A stretch: implement `bisect`. Given a graph and a marked "good" and "bad" commit, find a midpoint and partition. Run it interactively on your toy repo. You'll feel why this algorithm is so satisfying — and why it's the secret weapon of every long-time Git user.

The lesson: Git's *user interface* feels procedural ("commit, branch, merge") but its *substrate* is a graph algorithm library hiding behind a CLI. Once you see the DAG, every command becomes obvious. Once you don't, every command feels like magic.
