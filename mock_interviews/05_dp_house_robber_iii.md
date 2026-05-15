# Mock Interview: House Robber III (DP on Trees)

**Setup**: Principal engineer at a fictional security-research lab, Lattice. Candidate has 2 years of experience, has done easy/medium DP but not on trees.

**Difficulty**: Hard
**Topic**: Weeks 14-15 (DP on trees, recursion, post-order traversal).

---

## Transcript

**Interviewer**: Houses are arranged as a binary tree. You can rob a house, but you can't rob a house and its direct parent in the same plan. Maximize total robbed money.

**Candidate**: Just to confirm — only direct parent-child constraint? Grandparent and grandchild are fine?

**Interviewer**: Correct.

**Candidate**: Tree size? Negative values?

**Interviewer**: Up to ~10^4 nodes. Non-negative values.

**Candidate**: Okay. The shape is a graph DP. The constraint "no two adjacent" on a tree generalizes the classic "no two adjacent in a list" Robber I. There the recurrence is `f(i) = max(f(i-1), f(i-2) + a[i])`. Two states per index suffice: best ending with rob, best ending with skip.

> 🔍 **What's happening here**: The candidate is connecting the new problem to a known one — Robber I — *before* trying to solve it. Pattern transfer is the most valuable single habit in DP interviews.

**Candidate**: For the tree, I'll define for each node a pair `(rob, skip)`:
- `rob(node)` = `node.val + skip(left) + skip(right)` — if I rob this node, both children must be skipped.
- `skip(node)` = `max(rob(left), skip(left)) + max(rob(right), skip(right))` — if I skip this node, each child independently chooses its best.

Answer is `max(rob(root), skip(root))`. Post-order traversal computes it in one pass, O(N) time, O(H) stack.

**Interviewer**: Why two states per node? Why not one?

**Candidate**: Because the optimal value at a node depends not on the parent's value alone but on the parent's *decision*. If I only memoize one value `best(node)`, then when the parent decides "rob me", it can't ask the child for the constrained sub-answer "best given you weren't robbed". Two states encode that branch.

> 🔍 **What's happening here**: The interviewer is fishing for "why is this not 1D DP?" — the same reason "Robber II on a circular list" needs two passes. A confident answer requires you to remember that DP state must capture every transition-relevant thing about the past.

**Interviewer**: Code it.

**Candidate**:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rob_tree(root: TreeNode | None) -> int:
    def dfs(node: TreeNode | None) -> tuple[int, int]:
        # returns (rob_this, skip_this)
        if node is None:
            return (0, 0)
        lr, ls = dfs(node.left)
        rr, rs = dfs(node.right)
        rob_this = node.val + ls + rs
        skip_this = max(lr, ls) + max(rr, rs)
        return (rob_this, skip_this)
    return max(dfs(root))
```

**Candidate**: Dry run on the canonical example
```
        3
       / \
      2   3
       \   \
        3   1
```
Leaves return (3,0) for the lower-left 3, and (1,0) for the lower-right 1. The node with value 2: `rob=2+0=2`, `skip=max(3,0)+0=3` → (2,3). The right-side node with value 3: `rob=3+0=3`, `skip=max(1,0)=1` → (3,1). Root with value 3: `rob=3+3+1=7`, `skip=max(2,3)+max(3,1)=3+3=6` → max is 7. Correct.

> 🔍 **What's happening here**: The candidate ran the small canonical example and surfaced the answer 7. They didn't rush; on Hard problems an error in your manual trace usually points to an error in the code, and trusting either without checking is dangerous.

**Interviewer**: Stack depth?

**Candidate**: Recursion depth is the tree height. Worst case a degenerate chain — 10^4 nodes deep — which blows Python's default 1000 recursion limit. Three options: bump `sys.setrecursionlimit(20000)`, convert to iterative post-order with an explicit stack, or use Morris-style threading. For an interview I'd bump the limit and note the concern. For production I'd write the iterative version.

> 🔍 **What's happening here**: Recursion-depth awareness is one of the small things that separates a passing answer from a strong one on tree DP. Even if not asked, mentioning it costs 10 seconds and earns a tick.

**Interviewer**: What if the tree could have cycles?

**Candidate**: Then it's no longer a tree, it's a general graph and Maximum Independent Set is NP-hard on general graphs. On *bipartite* graphs it reduces to maximum matching via König's theorem — polynomial. On trees specifically, the bipartiteness is automatic and DP works. So: with cycles, no polynomial algorithm in general; with cycles but bipartite, max matching; without cycles, this DP.

> 🔍 **What's happening here**: The candidate didn't bluff. They named the complexity class, named the case where polynomial solutions still exist, and stopped. The interviewer now knows the candidate isn't going to fake-confidently misclassify a problem under pressure.

**Interviewer**: Can the DP be done in O(1) extra state per node beyond what we return?

**Candidate**: We're already there — each frame stores constant extra state. The only overhead is the recursion stack. If you mean "without recursion", iterative post-order with a parent-pointer or two-pass marking achieves O(N) work, O(N) auxiliary for the explicit stack.

**Interviewer**: One more. Negative house values?

**Candidate**: Then the recurrence still works structurally but you'd want `rob_this = max(0, ...)`-style guards if a "negative rob" means *don't rob*. Actually no — the cleanest fix is to also allow `rob_this = max(node.val + ls + rs, skip_this)` to mean "you can choose not to rob even when you can". But that collapses the two states. Let me reconsider: keep the two states, but treat the answer as `max` over both. If values can be negative, the simpler patch is: at the answer site `max(rob(root), skip(root))`, and within `skip_this`, take `max(lr, ls)` and `max(rr, rs)` as before — no change needed, since negative `rob_this` for a leaf is fine and the parent will just prefer the leaf's `skip` (which is 0) anyway.

> 🔍 **What's happening here**: The candidate caught themselves mid-answer ("Let me reconsider"). That's a great move. Walking back is far better than steamrolling a wrong claim — interviewers explicitly grade for it.

---

## Annotation legend

Each 🔍 callout teaches a specific *interview meta-skill*.

---

## What was tested
- Clarifying questions: ✅ adjacency definition, size, sign of values
- Brute force first: ⚠️ partial — went straight to the two-state DP. Could have mentioned the 2^N subset brute force, even briefly, to anchor.
- Complexity-driven optimization: ✅ O(N) time, O(H) space
- Edge cases without prompting: ✅ recursion depth, negative values
- Communication while coding: ✅ named the returned tuple's meaning in a comment
- Handling interviewer hints: ✅ recovered cleanly when reconsidering negatives

## Reflection prompts for the learner
- The candidate said "two states encode that branch." Reformulate the problem so *three* states are needed (hint: what if you can rob a node *and* one of its two children, but not both?). What does that do to the recurrence?
- Convert the recursive DP to iterative post-order with an explicit stack. Where does the per-node tuple live during the traversal?
- The interviewer asked "what if the graph has cycles?" Why does the candidate's answer reference König's theorem? Look it up if you don't recognize it — it connects max-matching and min-vertex-cover and is one of the most beautiful results in combinatorics.
