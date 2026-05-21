> 本文档是英文原版的翻译。如有不清楚之处，请参考[英文原版](../../PROBLEM_SOLVING.md)。

# 问题求解 — 思维方式宣言

> 一个 30 周的 DSA 课程可以教你算法*是什么*。这份文档讲的是当一个你从未见过的问题出现在屏幕上时，*该如何思考*。读一遍。在第 10 周后再读一遍。在第 20 周后再读一遍。

> **在投入 30 周之前，想先在实践中感受一下吗？** 花 4 小时跟着 [Quickstart](QUICKSTART.md) —— 八道精选题目，带你走一遍下面描述的完整循环。或者做一下 [Diagnostic](diagnostic.md)，找出你在课程中真正应该从哪里开始。

---

## 为什么有这份文档

这个仓库教数据结构和算法。这与教问题求解不是同一回事。

一个**写代码的人**知道语法、标准库以及一份命名算法的目录。给他一个带正确关键词的问题（"sorted array" → binary search），他就能交付。

一个**解题者**则不同。他坐在一个陌生的题目前不会慌张。他不断改写题目，直到它不再滑溜。他用手算一个小例子。他写一个明知道太慢的暴力解，*故意*这么做，因为那个解暴露了问题的结构。然后他问那一个驱动着计算机科学几乎所有优化的问题：*哪些功夫被浪费了？* 他的答案就是算法。

你来这里不是为了背 200 个 LeetCode 模板。你来这里是为了成为这样一个人：当面对一个无人解过的题时，仍然能向前推进。模板只是脚手架。心态才是真正的东西。

---

## Polya 的四步

George Polya 的 *How to Solve It*（1945）比你阅读清单里任何一本教材都老，但比大多数都更有用。四步：

### 1. 理解问题（Understand the problem）
读两遍。再读三遍。用自己的话写下：
- 输入是什么？（类型、范围、是否有序、是否有重复、是否可能为空）
- 输出是什么？（一个值、一个结构、所有合法配置）
- 这里的"合法"或"最佳"是什么意思？
- 题目*没有*说什么？（这往往是最重要的问题）

**例子。** "Find the longest substring with at most K distinct characters."（找出最多含 K 个不同字符的最长子串。）在做任何事情之前：K 保证 ≥ 1 吗？字符是 ASCII 还是 Unicode？如果字符串为空，答案是 0 还是未定义？"substring"是连续的（按惯例是），还是"subsequence"（不连续）？跳过这一步，你会解错题目，而且二十分钟里不会察觉。

### 2. 制定计划（Devise a plan）
在写一行代码之前，用中文（或英文）把方法讲清楚。"我会用一个 sliding window，right 指针扩张直到窗口里有 K+1 个不同字符，然后 left 指针收缩直到回到 K 个；过程中追踪最大长度。"如果你不能用两句话讲清楚，那就还没有计划。

这也是把新题与旧题连接起来的地方。"这感觉像 minimum window substring。" "这就是 implicit graph 上的 BFS。" 模式识别是一种规划能力，不是记忆能力。

### 3. 执行计划（Carry out the plan）
现在写代码。从计划到代码的翻译应该是机械的。如果你在敲键盘时仍在做大决策，停下 —— 你跳过了第 2 步。

### 4. 回头看（Look back）
每个人都跳过的一步。在题目通过之后：
- 我能推出更紧的复杂度上界吗？
- 我能简化代码吗？（重命名变量、合并特殊情况、删除未用的分支）
- *关键洞见*是什么？用一句话写下。这句话是会迁移到下一题的东西。
- 这属于哪一类问题？把它加入你的心智索引。

**工作示例 —— Two Sum。**
1. *理解。* 给定 `nums` 和 `target`，返回两个和为 `target` 的下标。恰有一个解。同一个元素不能用两次。是下标，不是值。
2. *计划。* 暴力 O(n²) 对。更好：对每个 `x`，我们需要 `target - x`。用 hash 查找是 O(1)。走一遍，问 hash 是否已经见过 `target - nums[i]`，否则存 `nums[i] → i`。
3. *执行。* 十行代码。
4. *回头看。* 关键洞见：*我们不需要搜索 pair；我们需要问 complement 是否存在*。这个重述 —— "search → existence query" —— 正是 3Sum、4Sum、two-pointers-on-sorted 等背后的招式。技巧是可迁移的；记住招式，不是代码。

---

## 改写模糊的问题

真实的问题 —— 工作中、研究中、面试中 —— 都是含糊的。练习把它们收紧。

| 模糊的描述 | 收紧后的版本 |
|---|---|
| "找出这个 array 中的重复项。" | "返回出现超过一次的值的集合。顺序不重要。Array 装得下内存。值是 32 位整数。" |
| "安排会议。" | "给定 `(start, end)` 区间的列表，返回最多互不重叠的区间数。仅共享端点的两个区间不算重叠。" |
| "找最短路径。" | "无权无向图，最多 10⁵ 节点；返回 `s` 到 `t` 最短路径的边数，无法到达返回 `-1`。" |
| "压缩这个字符串。" | "把每一段 `k ≥ 2` 个相同字符替换为 `c` 后跟十进制 count。长度为 1 的段不动。输出必须比输入短，否则原样返回。" |
| "找最佳路线。" | "*最佳*按什么标准 —— 距离、时间、油耗、最少换乘？边是否带权？权可以为负吗？图是稠密还是稀疏？" |

注意这个模式：模糊的描述里有**隐含约束**，提问者脑中有，你没有。在约束没有落到纸上之前，问题不是问题 —— 是愿望。

独自工作（没有提问者可质询）时，把问题改写给自己，**锁定约束**。把它们写在草稿文件的顶部。它们现在是规约的一部分。

---

## 识别约束 —— 每一个告诉你*什么*

约束是题面中最被忽视的部分，也是房间里最大声的提示。像编译器读类型那样去读它们。

**输入规模 N。** 这一个数字比任何其他信息都更能缩小你的算法类。

| N 上限 | 可行算法（~1 秒预算） |
|---|---|
| ~10 | 什么都行。O(N!) 暴力都行。Backtracking, permutations。 |
| ~20 | O(2^N) bitmask DP, meet-in-the-middle。 |
| ~500 | O(N³) 可以 —— Floyd-Warshall, interval DP。 |
| ~5,000 | O(N²) 可以 —— quadratic DP, all-pairs scans。 |
| ~10⁵ | O(N log N) —— 排序, segment trees, 带 heap 的 Dijkstra。 |
| ~10⁶ | O(N) 或 O(N log log N) —— 线性扫描, sieves, hashing。 |
| ~10⁸+ | O(log N) 或 O(1) per query —— 预处理、数学、或在 streaming。 |

如果题目说 `N ≤ 20` 而你在想多项式 DP，那是过度思考。如果 `N ≤ 10⁶` 而你的计划是 O(N²)，那是思考不足。

**时间限制。** "2 秒"加上 N 从另一面讲同一个故事。现代机器大约每秒做 10⁸–10⁹ 个简单操作。把 N 乘以 big-O，看乘积是否塞得下。

**内存限制。** 256 MB 大约是 6×10⁷ 个 int。如果题目给 N=10⁶ 还要 N×N 表，你需要 O(N) 或 O(log N) 空间 —— 这把你推向 space-optimized DP、rolling arrays，或 in-place 算法。

**有序性。** "The array is sorted" 是一个巨大闪烁的牌子，写着*binary search, two pointers, or merge*。"The values are distinct" 排除处理重复的边界情况。"The input is a permutation of 1..N" 开启 cycle decomposition 和 counting 技巧之门。

**可变性。** 能修改输入吗？可以的话，in-place 技巧（negative-marking, swap-to-index）就免费了。不行的话，至少需要 O(N) 的辅助空间。

**实数 vs. 整数。** 仅整数开启 counting sort、bitmask、modular arithmetic 和精确比较。Floats 强迫你考虑精度、epsilon 比较和数值稳定的表达。

**Online vs. offline。** Offline 意味着你能一次看到所有查询 —— 可以重排、批处理、sweep。Online 意味着每个查询必须在看到下一个之前回答 —— segment trees、平衡 BST、persistent structures。

**先读约束，后读题面。** 不是笔误。约束往往在你读到问题之前就告诉了你答案的形状。

---

## brute → better → optimal 阶梯

这份文档里最重要的一个习惯。

**第 1 步 —— Brute force。** 写下你能写出的最笨的正确解。试每一对、每一个子集、每一条路径。不要跳过。如果 brute force 慢到敲不出来，把*recurrence*写在纸上。

为什么这很重要：
- 它钉住了"正确"的含义 —— 你现在有了一份参考实现可以对比。
- 它暴露了**结构**。Brute force 的瓶颈就是优化所在。
- 它解除了问题的威慑。你从"我不知道怎么解"变成"我有一个 O(N³) 的可用解，想把它变快"—— 这是两种不同的心理状态。

**第 2 步 —— 问那一个问题。** *Brute force 做了哪些被浪费的功夫？*

这个问题是计算机科学中几乎每一个算法改进的引擎：

| 浪费的功夫 | 由此产生的优化 |
|---|---|
| 反复计算同一个子问题 | Memoization → DP |
| 反复扫描刚扫过的区间 | Prefix sums, sliding window |
| 在已排序数据中线性查找 | Binary search |
| 查找一个本可以索引的值 | Hash map |
| 在移动窗口上反复求 `min` | Monotonic deque |
| 重新遍历刚遍历过的树 | Euler tour, DFS reuse |
| 尝试明显被支配的选择 | Greedy + exchange argument |
| 检查不可能改进答案的边 | Dijkstra's relaxation |

**第 3 步 —— Optimal（或够好）。** 应用优化。在小输入上和 brute force 对比验证。*然后*再担心常数、SIMD 和缓存行为 —— 通常你不需要。

跳过第 1 步是中级程序员最常犯的错误。他们直接奔向聪明解，漏一个 case，然后他们在调试一个他们自己都没完全理解的聪明解。Brute force first。永远。

---

## 何时该放弃 —— 走错路的征兆

你会卡住。卡住没关系。因自我而卡住不行。当前计划已死的信号：

- **30+ 分钟没有可运行的代码，问题也没有缩小。** 不是卡在 bug 上 —— 卡在思路上。换张新纸重来。
- **边界情况不断增多。** 每个修复带来两个新情况。数据结构错了，或者 invariant 错了。
- **复杂度分析合不上。** 你甚至不能在纸上给出界。计划不自洽；你不知道它在做什么。
- **你在打症状的补丁。** 加了 `if (i == 0)`，然后 `if (n == 1)`，然后 `if (arr[i] < 0)`。每个补丁都在说，你的核心逻辑没能从构造上处理一个本该处理的情况。
- **你累了，同一个 bug 一直回来。** 离开十分钟。这不是懒，是 debugging。

**如何不带自我地回退。** 写下 —— 真的写下 —— 你当前思路的所有假设。哪一个最弱？放掉它。往往正确算法就是你试过那个的兄弟，只差一个设计选择（BFS vs. DFS，按 start 还是 end 排序，top-down vs. bottom-up）。

早早放弃是一种能力。第 15 分钟换思路代价很小。第 90 分钟换则是灾难性的。

---

## 常见的认知陷阱

这些是反复出现的失败模式。给它们命名，这样你能在自己身上看到它们。

- **过早优化。** 没检查 prefix sum 行不行就奔向 segment tree。正确之前先调常数。纪律：*correct, then clear, then fast*。
- **锚定在第一个想法上。** 你的第一个计划感觉像*那个*计划，因为是你想到的。强迫自己在选定之前至少生成三个思路。比较的过程本身就产生洞见。
- **拒绝写 brute force。** "这太低级了。" "明显太慢。" 还是写。它是参考实现、test oracle、思考辅助。它只花四分钟。
- **怕递归。** 递归是一种记法，不是魔法咒语。能写出 recurrence 就能写出函数。递归太深就转成栈 —— 那是机械变换，不是创造性飞跃。
- **跳过纸笔。** 每道题都装得下一张索引卡。画 array、勾出 tree、用手走前三轮迭代 —— 这些比任何 debugger 更快找出 bug。键盘是用来敲的，不是用来思考的。
- **太早读 solution。** 二十分钟富有成效的挣扎比两小时的阅读教得多。如果非看不可，就只看*想法*（一句话），然后关掉标签页。
- **从一个例子泛化。** 你的代码在 `[1,2,3]` 上能跑。试试 `[]`、`[5]`、`[5,5]`、`[5,4,3,2,1]`、`[-1,-2]` 和最大输入。Edge cases 不是可选的。
- **复杂度读错。** "我排序了，所以是 O(N log N)。" 但内层是 O(N)，所以是 O(N² log N)。有疑问就重算。

---

## 7 个问题原型

大多数面试题和竞赛题都是这些原型之一的伪装。每一个都有一个"气味" —— 暗示底层形状的表面特征。

| 原型 | 气味 | 在本仓库的位置 |
|---|---|---|
| **Search & sort** | "Sorted array", "find the K-th", "smallest such that…" | Weeks 8–9 |
| **Two pointers** | "在 sorted array 里找具有性质 X 的 pair", "in-place rearrange" | Week 30 |
| **Sliding window** | "性质 X 的最长/最短连续子数组" | Weeks 6, 13, 30 |
| **BFS / DFS** | "Reachable", "connected", "无权图最短", "全部探索" | Week 17 |
| **Dynamic programming** | "数有多少种方式", "在选择上 min/max", "有 overlapping 的 optimal substructure" | Weeks 18, 23 |
| **Greedy** | "Schedule", "最少多少个 X", "可以证明局部选择是安全的" | Week 19 |
| **Divide & conquer** | "在两半上递归", "merge 结果", "O(N log N) 合理" | Week 9 (merge/quick sort), Week 27 (closest pair) |

这些会重叠。Sliding window 是 two pointers 的特例。DP 常常源自带 memoization 的 divide & conquer。Greedy 是 DP，当你能证明只有一个选择重要时。边界是模糊的 —— 标签是脚手架，不是真理的范畴。

新题来了，做一次快速分诊：它带哪几种气味？如果是两种，答案大概率是它们的组合。

---

## 收尾阅读清单

- **Polya, *How to Solve It* (1945)。** 短。老。仍是这个主题上最好的书。一年读一次。
- **Skiena, *The Algorithm Design Manual*, 3rd ed.** 第 1–3 章讲解题哲学；"war stories" 是金子。后半的 catalog 是工作程序员的参考。
- **CLRS (Cormen, Leiserson, Rivest, Stein), *Introduction to Algorithms*, 4th ed.**
  - 第 1 章 —— 算法的角色。
  - 第 2 章 —— 起步（insertion sort 作为 Polya 工作示例）。
  - 第 4 章 —— 分治（recurrences, master theorem）。
  - 第 15 章 —— 动态规划（rod-cutting 推导是经典的 brute → better → optimal walkthrough）。
  - 第 16 章 —— Greedy（以及如何证明正确性）。
- **Bentley, *Programming Pearls*.** 第 2 列（"Aha! Algorithms"）和第 8 列（"Algorithm Design Techniques"）对这种心态最有用。
- **Kleinberg & Tardos, *Algorithm Design*.** 第 1 章的 gale-shapley 推导是把模糊问题变精确的大师课。

跟课程一起读，而不是读完后再读。重点不是读完它们 —— 而是卡住时它们是打开的。

---

> 仓库里的算法是工具。*问题求解*是工坊。工坊里待的时间比工具箱里多。
