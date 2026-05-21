> 本文档是英文原版的翻译。如有不清楚之处，请参考[英文原版](../../docs/diagnostic.md)。

# Diagnostic —— 你应该从哪里开始？

跨越课程的 15 道题。诚实作答。结束时我们把你的答案映射到推荐的起始周。

**做题时不要查任何资料。目的是校准，不是打分。** 时间预算：~25 分钟。如果一题花了两分钟以上，写下你的最佳猜测继续。

准备一张简单的答题卡：`Q1: C`、`Q2: ...` 等。在回答完所有 15 题之后再展开底部的答案 key。

---

## Section 1: Foundations & Complexity (Q1–Q3)

### Q1. 下面这段 Python 代码的时间复杂度是？

```python
def f(n):
    result = []
    for i in range(n):
        for j in range(i, n):
            result.append(i * j)
    return result
```

- A) O(N)
- B) O(N log N)
- C) O(N²)
- D) O(N³)

### Q2. 你有一个算法，N = 1,000 时跑 1 秒。假设算法是 O(N log N)，N = 1,000,000 时大约跑多久？

- A) 约 1,000 秒（~17 分钟）
- B) 约 2,000 秒（~33 分钟）
- C) 约 1,000,000 秒（~12 天）
- D) 约 10 秒

### Q3. 简答。一个题的约束是 `1 ≤ N ≤ 20`。在不知道更多信息的情况下，在这个小 N 下*开启*了什么算法类，而在 N = 10⁵ 时不可行？用一两个词回答。

---

## Section 2: Arrays & Strings (Q4–Q5)

### Q4. 给定一个由不同整数构成的有序数组和一个 target，找两个下标其值之和等于 target。最干净的方法是？

- A) Hash map：对每个 `x`，查找 `target - x`。O(N) 时间，O(N) 空间。
- B) 从两端开始的 two pointers，根据当前 sum 向内移动。O(N) 时间，O(1) 空间。
- C) 对每个元素的 complement 做 binary search。O(N log N) 时间，O(1) 空间。
- D) 检查每一对的 nested loop。O(N²) 时间，O(1) 空间。

> 多个选项"能 pass"是*正确*的。选那个最大化利用输入**结构**的。

### Q5. 你在处理一段字符流，在每个位置想知道以当前字符结尾、无重复字符的最长子串长度。用什么技巧？

- A) 对 substring 排序后去重。
- B) 用 hash set 的 sliding window：right 扩张，window 内有 duplicate 时 left 收缩。
- C) DP，始终 `dp[i] = dp[i-1] + 1`。
- D) Suffix array。

---

## Section 3: Hash Maps & Data Structures (Q6–Q8)

### Q6. 在一个 average-case 下大小合适的 hash table 中，`insert`、`lookup`、`delete` 的时间复杂度是？

- A) 三个都是 O(log N)。
- B) 三个都是 O(1) amortized average。
- C) Insert O(N)，lookup O(1)，delete O(N)。
- D) Insert O(1)，lookup O(N)，delete O(N)。

### Q7. 你需要一个数据结构，支持 `get(key)` 和 `put(key, value)` 在 O(1) average，并在超出容量时驱逐 least-recently-used key。你组合哪两个结构？

- A) 两个 stack。
- B) Hash map + 平衡 BST。
- C) Hash map + doubly linked list。
- D) Min-heap + hash set。

### Q8. 简答。一句话：何时你会为存一组字符串选 **trie** 而不是 **hash map**？

---

## Section 4: Trees, Recursion & Graphs (Q9–Q11)

### Q9. 给定二叉树 root，你写 `depth(root) = 1 + max(depth(left), depth(right))`，base case `depth(None) = 0`。这是正确且 idiomatic 的实现。其时间与空间复杂度是？（空间 = 递归栈），其中 `N` 是节点数，`H` 是树高。

- A) Time O(N log N), space O(N)。
- B) Time O(N), space O(H)。
- C) Time O(H), space O(1)。
- D) Time O(N²), space O(N)。

### Q10. 在**无权无向**图中求 `s` 到 `t` 的最短路径（以边数计）。用哪个遍历，为什么？

- A) DFS，因为它先深入探索。
- B) BFS，因为它按距源 edge-distance 的非递减序访问节点。
- C) Dijkstra，因为它是通用的最短路径算法。
- D) 拓扑排序，因为它给出顺序。

### Q11. 简答。要求你在**有向**图中检测 cycle。你决定用 DFS。除了 "visited" 集合外，你还需要什么辅助状态，为什么？一句话。

---

## Section 5: DP & Advanced (Q12–Q15)

### Q12. 下面哪一题用 DP *最干净*（相对于 greedy、brute force 或单次扫描）？

- A) 给定硬币面额和一个金额，返回凑出该金额的硬币的**最少**数量。面额任意（如 `[1, 3, 4]`，金额 `6` → `2`，不是 `3`）。
- B) 给定一组区间，求互不重叠区间的最大数量。
- C) 给定数组，返回其和。
- D) 给定两个字符串，判断它们是否是 anagram。

### Q13. 你看到"求多少种不同方式"，recurrence 形如 `f(n) = f(n-1) + f(n-2)`，约束到 `N ≤ 10⁵`。信号是？

- A) Greedy：在每个 `n` 上取局部最佳。
- B) DP：memoize recurrence（或 tabulate）。注意 overlapping subproblems。
- C) Backtracking：枚举所有配置。
- D) 记录已见 `n` 的 hash map。

### Q14. **Segment tree** 比 prefix-sum array 擅长的是？

- A) 在 array **静态**时，O(N) 预处理后 O(1) 答 "sum of `a[l..r]`"。
- B) 在点更新 `a[i] = x` 与查询交错的情形下，二者都在 O(log N) 内答 "sum of `a[l..r]`"。
- C) 在 O(N log N) 内排序。
- D) 找 stream 的中位数。

### Q15. 简答。一句话解释 **network flow**（max-flow / min-cut）能建模的、普通 BFS/DFS 不能的*问题类型*。不用担心算法名 —— 只说*问题的种类*。

---

## 到此为止。回答完 15 题再打分。

<details>
<summary><b>点击展开 答案 key + placement</b></summary>

### 答案 key

- **Q1: C** —— 外层 N 次；内层从 `i` 到 `n`，总 ops = N + (N-1) + ... + 1 = N(N+1)/2 ≈ N²/2。O(N²)。
- **Q2: B** —— N log N 按 `(N₂/N₁) · (log N₂ / log N₁) = 1000 · (20/10) ≈ 2000` 放大。约 2,000 秒。C 是 O(N³)；A 是 O(N²)。
- **Q3** —— **Bitmask DP**（或"subset enumeration / 2^N brute force / 指数搜索"）。N ≤ 20 意味 2^N ≤ ~10⁶，一秒内可行。Week 23 覆盖。
- **Q4: B** —— two pointers 利用了**有序**结构，达到 O(N) 时间和 O(1) 空间。A 能 pass 但浪费 O(N) 空间；C 多了 log；D 忽略了有序。问题的要点：选最大化利用输入*结构*的技巧。
- **Q5: B** —— 经典 sliding window，用 hash set / last-seen-index map。C 错，因为 `dp[i]` **不**总是 `dp[i-1] + 1` —— 取决于 `s[i]` 是否已在当前 window 里。
- **Q6: B** —— 三者都是 O(1) amortized average。最坏 O(N)（所有 key 哈希到同 bucket），但题问的是平均。
- **Q7: C** —— hash map 提供 O(1) lookup，doubly linked list 在每次访问时 O(1) 重排。这是标准 **LRU cache** 结构，Weeks 11、16、29 覆盖。
- **Q8** —— 当你需要 **prefix queries**（autocomplete、"是否有以 `pre` 开头的串"），或大量串共享长 prefix（节省内存）。Hash map 把 key 当作不透明；trie 利用共享 prefix 结构。
- **Q9: B** —— 每节点访问一次 → O(N) 时间。递归深度 = 树高 → O(H) 空间。平衡树 H = O(log N)；退化（链状）H = N。
- **Q10: B** —— BFS。逐层扩张保证你第一次到达某节点时用的边数最少。Dijkstra 也行，但对无权图是大材小用（且多了无谓 log）。
- **Q11** —— 除了 "fully-visited"（black）集合外，还需要 **"当前在递归栈上"（即 "gray" 或 "in-progress"）** 集合。指向 gray 节点的 back edge 是 cycle。仅用 visited 无法在 DAG 中区分 cross/forward edge 和真正的 back edge。
- **Q12: A** —— 任意面额的 coin change 是经典 DP（greedy 对 `[1, 3, 4]`、金额 `6` 会选 `4 + 1 + 1`；DP 找到 `3 + 3`）。B 是 greedy（interval scheduling）。C、D 一遍扫描即可。
- **Q13: B** —— DP。Fibonacci 形的 recurrence + overlapping subproblems 是教科书 DP 信号。N ≤ 10⁵，naive 递归指数级；memoize 或 tabulate。
- **Q14: B** —— segment tree 在 **点更新 + 区间查询** 都是 O(log N)。Prefix-sum array 在 range-sum 上是 O(1)，但每次更新 O(N)；只在静态时占优。
- **Q15** —— Network flow 建模**带容量约束的路由**：每条边可送 `c(u,v)` 单位，求 source 到 sink 的最大总吞吐。Equivalently（min-cut 对偶），它解决"用最少几条边把 `s` 和 `t` 断开"的问题。普通 BFS/DFS 只讲可达性或最短路径，不推理*容量*或*聚合流量*。许多表面无关的问题（bipartite matching、图像分割、project selection）都可归约到 max-flow。

### Placement 矩阵

数一下你*完全*答对了多少（简答题，捕捉到相同 idea 就算对，即使措辞不同）。

| 分数 | 推荐起点 |
|---|---|
| **0–3** | 从 **Week 1** 开始。基础是必要的。别跳 —— 会复利。 |
| **4–7** | 略读 Weeks 1–5（如果 Q1–Q3 觉得简单可以跳）。从 **Week 6**（arrays）或 **Week 8**（searching）开始正经做。 |
| **8–11** | 从 **Week 11**（链表）或 **Week 14**（树）开始，取决于你哪里答错。错 Q9–Q11 选 Week 14；错 Q6–Q8 选 Week 16。 |
| **12–15** | 从 **Week 17**（图）开始或直接跳到 advanced（**Weeks 21+**）。如果 Q14–Q15 也答对，直接 Weeks 23–24（高级 DP & research-level）。 |

**Diagnostic 异常 —— 也读一下：**
- **Sections 4–5（Q9–Q15）答得好但 section 1（Q1–Q3）答错**：不常见。你会写算法但不会推理代价。重看 [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) 的复杂度分析 —— 尤其是"识别约束"那节。然后回到 Week 8。
- **Sections 1–3 好但 sections 4–5 差**：经典 profile。基础扎实但算法词汇没建立。跳到 [root README](../../README.md#path-2-interview-prep-8-weeks) 的 **8 周面试备战路径** —— Weeks 6, 8, 11, 14, 16, 17, 18, 30。
- **Q3、Q8、Q11 或 Q15 完全答对（简答）**：你有经验 practitioner 的*词汇*。即使 MCQ 中等，也偏向走 advanced。

### 各 section 测试什么

| Section | 测试 | 涵盖于 |
|---|---|---|
| 1 (Q1–Q3) | 复杂度直觉、big-O scaling、约束阅读 | Weeks 1–5, 8; [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) |
| 2 (Q4–Q5) | Array & string 惯用法 —— two pointers, sliding window | Weeks 6, 7, 10, 30 |
| 3 (Q6–Q8) | Hash maps, 复合数据结构, tries | Weeks 11, 16, 21 |
| 4 (Q9–Q11) | 递归, 树, 图遍历推理 | Weeks 5, 14, 17 |
| 5 (Q12–Q15) | DP 识别, segment trees, network flow | Weeks 18, 21, 23, 26 |

---

> 无论你落在哪一周，把 diagnostic 分数和推荐作为 journal 的第一条 entry 记下。半年后，当你已经忘了那时不会什么，它会是最诚实的起点快照。

</details>

---

## 接下来呢？

- 还不熟悉方法论？先试 [**Quickstart**](QUICKSTART.md) —— 4 小时、8 题、完整循环。
- 准备投入？去 [**root README**](../../README.md) 选一条 learning path。
- 想要课程背后的哲学？读 [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md)。
