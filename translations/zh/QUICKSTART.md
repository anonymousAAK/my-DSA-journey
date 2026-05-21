> 本文档是英文原版的翻译。如有不清楚之处，请参考[英文原版](../../QUICKSTART.md)。

# Quickstart —— 用 4 小时看看这个 Repo 是否适合你

如果 30 周让人望而生畏：别从那里开始。给这条精选路径专注的 4 个小时。结束时你已经在 5 个难度级别的 8 道代表性题目上完整练习过整套方法论。如果这个循环对你有效，长路径不过是同一个循环的更多次重复。

这个循环就是 [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) 里教的那一个：

> 理解 → 计划（brute → better → optimal）→ 执行 → 回头看（journal）。

你今天会做这个循环八次。

---

## 开始之前（10 min）

1. 读 [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) —— 至少略读 **"Polya 的四步"** 和 **"brute → better → optimal 阶梯"** 两节。
2. 把 [`docs/SOLUTION_JOURNAL.md`](../../docs/SOLUTION_JOURNAL.md) 复制到工作目录的 `my_journal.md`（不要 commit）。每道题追加一条 entry。
3. 设一个 4 小时的计时器。如果在任何一题上超出预算 5 分钟以上，停下，瞄一眼参考文件，继续。今天的重点是*循环的覆盖*，不是完美解。
4. 用两个 pane 打开 scratch editor：左边题目，右边 journal。

> **一条规则，不可商量。** 每道题在打开参考文件*之前*尝试。先看答案会把这从训练变成娱乐。

---

## Hour 1 —— Foundations（识别模式）

目标：感受 brute force 和"正确工具"的差别。两道短题，再加一个模式 drill。

### Problem 1: Two Sum (15 min, Easy)
- **参考（只在尝试后看）**：[`Week 16/java/1.HashingAndHashMap.java`](../../Week%2016/java/1.HashingAndHashMap.java) —— 只略读 `twoSum` 函数（line 43 附近）。
- **Spec**：给定 `nums` 和 `target`，返回值之和为 `target` 的两个下标。假设恰好一个解。
- **任务**：用你喜欢的语言，不看答案地解。先写 brute-force `O(N²)`，再写 hash-map `O(N)` 版本。
- **Journal (2 min)**：你用了什么模式？为什么 brute-force 是 `O(N²)`？把*关键洞见*写成一句话 —— 这句话是会迁移的东西。

### Problem 2: Maximum Subarray / Kadane (15 min, Easy)
- **参考**：[`Week 6/python/4.prefix_sum_and_kadane.py`](../../Week%206/python/4.prefix_sum_and_kadane.py) —— Part B, Kadane 算法。
- **Spec**：给定整数数组（值可能为负），找出和最大的连续子数组。返回这个和。
- **任务**：先 brute force（试每个 `(i, j)` 对，O(N²) 或 O(N³)），再推导 Kadane 的 `O(N)` running-best recurrence。两个都写出来之前不要看。
- **Journal (2 min)**：brute force 浪费了什么功夫？Kadane 在每一步维护什么 invariant？

### Problem 3: 模式识别 Drill (10 min)
- 打开 [`Week 6/patterns.md`](../../Week%206/patterns.md)。冷做 **drills 1–5**（不要看文件其余部分或任何 solution）。
- 每个写一行：哪个模式（two pointers / sliding window / prefix sum / Kadane / Dutch flag / hash）和一句话的理由。
- 然后用文件底部的答案 key 自查。

### Hour 1 总结 (5 min)
在 journal 里写 3 句回答：
1. 你在哪里最挣扎 —— 改写问题、选模式，还是写代码？
2. 哪道题事后感觉"显而易见"？开始时为什么不显而易见？
3. 你在 Problem 2 上真的先写了 brute force 吗，还是直接跳到 Kadane？

---

## Hour 2 —— Structures（造对的工具）

目标：看到*选数据结构*往往*就是*算法。

### Problem 4: 合并两个有序链表 (25 min, Medium)
- **参考**：[`Week 11/python/2.MergeSortedListsAndLRU.py`](../../Week%2011/python/2.MergeSortedListsAndLRU.py) —— 只看 merge 函数。还不要读 LRU 部分。
- **Spec**：给定两个有序的 singly linked list，返回一个合并的有序链表。复用节点（不要复制）。
- **任务**：先在纸上画。画两个链表、两个指针，追踪你接下来要 splice 哪个节点。然后写代码。用一个 dummy/sentinel head —— 它消除"第一个节点是特殊的"这种情况。
- **Journal (3 min)**：dummy head 为什么让代码更短？时间和空间复杂度分别是多少，空间花在哪里？

### Problem 5: 二叉树 —— 最大深度 (15 min, Easy–Medium)
- **参考**：[`Week 14/python/1.BinaryTree.py`](../../Week%2014/python/1.BinaryTree.py) —— 找深度 / 高度函数。
- **Spec**：给定二叉树的 root，返回其深度（最长 root-to-leaf 路径上的节点数）。
- **任务**：用三行写递归版本。然后用 queue 写迭代版本（level-order，统计层数）。
- **Journal (2 min)**：用一行写 recurrence：`depth(root) = ...`。这和 DP recurrence 是同一种形状；你还会再见。

### Hour 2 总结 (5 min)
- 哪个结构让你惊讶 —— 链表还是树？
- 你能用 [`Week 5/python/3.recursion_basics.py`](../../Week%205/python/3.recursion_basics.py) 里同样的递归习惯解 Problem 5 吗？简短地打开确认 —— 递归*就是*主线。

---

## Hour 3 —— Algorithms（挑对的方法）

目标：从"数据结构是什么？"升级到"*技巧*是什么？"

### Problem 6: 最多含 K 个不同字符的最长子串 (25 min, Medium)
- **参考**：[`Week 30/python/sliding_window.py`](../../Week%2030/python/sliding_window.py) —— 可变长 window 模板。
- **Spec**：给定字符串 `s` 和整数 `k`，返回最多含 `k` 个不同字符的最长子串长度。
- **任务**：先 brute force（每个 substring，数 distinct → `O(N²)` 或 `O(N³)`）。然后推导 sliding window：right 扩张，distinct 数超过 `k` 时 left 收缩，记最佳长度。`O(N)`。
- **Journal (3 min)**：window 维护什么 invariant？为什么每个字符最多被访问两次（一次 `right`，一次 `left`）？

### Problem 7a (open challenge 前的热身)：BFS 推理 (15 min, Medium)
- **参考**：[`Week 17/python/1.GraphRepresentations.py`](../../Week%2017/python/1.GraphRepresentations.py) —— BFS 函数。
- **Spec**：给定一个用邻接表表示的无权无向图和两个节点 `s`、`t`，返回最短路径上的边数，无法到达返回 `-1`。
- **任务**：从零写 BFS。用 queue 和 visited set。追踪 depth：要么存 `(node, depth)` tuples，要么按层处理 queue。
- **Journal (2 min)**：BFS 为什么对*无权*图给出最短路径，但对*带权*图不行？（如果不知道，这就是你通往 Week 22 的路标。）

### Hour 3 总结 (5 min)
Sliding window 和 BFS 都是"小心地扩张 frontier"。在 journal 里记下：它们共享什么，又有什么不同（一个沿 1-D array 移动，另一个穿过任意图）。

---

## Hour 4 —— 综合（在模拟压力下完整跑一遍）

目标：在一道没有被喂到嘴边的题上端到端地组合这个循环。

### Problem 8: Open-ended challenge (40 min, Hard)
从 [`Week 8/challenges.md`](../../Week%208/challenges.md) 选**一个** challenge —— 推荐：如果你见过 binary search，选 **Challenge 1 (Closest Element in a Rotated Sorted Array)**；否则选同一文件的 **Challenge 2**。

规则：
1. 用自己的话把 spec 改写在 journal entry 顶端。写下约束。
2. 写代码*之前*用 2 句话勾画思路。
3. 实现。不要看 `Week 8/python/`、`Week 8/java/` 等任何文件。
4. 在 challenge 文件给的输入上测试。
5. 只有在它能跑通之后（或者 40 min 到了，以先到者为准），才把你的解与 canonical 解 diff。你做了什么不同？

### Problem 9: Mock interview 自我复习 (15 min)
读 [`mock_interviews/01_two_sum_warm_up.md`](../../mock_interviews/01_two_sum_warm_up.md) —— Hour 1 第一题完整的 annotated transcript。

- 把你 Hour 1 的思考过程和 transcript 标注的好习惯（callouts）对照。
- *你*做了哪些 transcript 标为 "good" 的事？（比如询问是否有重复、改写问题、说出 tradeoffs。）
- 你跳过了什么？（比如有没有说复杂度？解之前有没有提 brute force？）

### Hour 4 总结 (5 min)
在 journal 里写：
- 你 Hour 4 challenge 的解更接近 brute force、"better"，还是 optimal？为什么？
- 今天你最常跳过 Polya 四步中的哪一步？（大多数学习者跳第 4 步 "Look back"。）
- 下次会做得不一样的是什么？

---

## 接下来呢？

你刚做完整个课程的一个 microcosm。八道题，五个难度级别，循环的每一层。如果有价值：

- **做 diagnostic**（[`docs/diagnostic.md`](../../docs/diagnostic.md)）找出你真正的起点。跳过你已经掌握的周。
- **8 周专注面试备战**：在 root README 里跟 [Learning Path 2 (Interview Prep)](../../README.md#path-2-interview-prep-8-weeks) —— Weeks 6, 8, 11, 14, 16, 17, 18, 30。
- **完整 30 周**：从 Week 1 开始，每题写 journal。能完成的人大多这么做。
- **竞赛编程**：跟 [Path 3](../../README.md#path-3-competitive-programming-10-weeks)。

如果没感觉到价值，在离开之前老实地检查：

- 你真的在偷看之前尝试了每道题吗？
- 你写 journal 了吗，还是只是在读？
- 你在 Problems 2、6、7a 上*先*写了 brute force —— 还是直接跳到聪明解？
- Problem 8 上你把代码和 canonical 版本对比了吗？

大多数"对我没用"的结果都能追溯到一个具体的跳过：journaling 这一步。Journal 才是方法论真正生活的地方。代码是副产品。

---

> 你做了八次循环，你就做了八次。这不是无足轻重的。习惯就是这样开始的。
