# Week 30 — Practice Problems

Topics covered this week: interview-pattern revision — sliding window, two pointers, top-K, intervals, prefix sums, stock problems, and mixed problem recognition.

## Curated Problems

| # | Problem | Difficulty | Topic | Link | Companies |
|---|---------|------------|-------|------|------|
| 1 | Longest Substring Without Repeating Characters | Medium | Sliding window | https://leetcode.com/problems/longest-substring-without-repeating-characters/ | Amazon, Meta, Microsoft, Bloomberg |
| 2 | Sliding Window Maximum | Hard | Monotonic deque | https://leetcode.com/problems/sliding-window-maximum/ | Amazon, Meta, Google, Microsoft |
| 3 | 3Sum | Medium | Sort + two pointers | https://leetcode.com/problems/3sum/ | Amazon, Meta, Google, Microsoft |
| 4 | Container With Most Water | Medium | Two pointers | https://leetcode.com/problems/container-with-most-water/ | Amazon, Meta, Apple, Bloomberg |
| 5 | Trapping Rain Water | Hard | Two pointers / stack | https://leetcode.com/problems/trapping-rain-water/ | Amazon, Meta, Google, Apple |
| 6 | Top K Frequent Elements | Medium | Heap / bucket | https://leetcode.com/problems/top-k-frequent-elements/ | Amazon, Meta, Microsoft, Apple |
| 7 | Best Time to Buy and Sell Stock | Easy | Single-pass min tracking | https://leetcode.com/problems/best-time-to-buy-and-sell-stock/ | Amazon, Meta, Google, Microsoft |
| 8 | Best Time to Buy and Sell Stock III | Hard | State-machine DP | https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/ | Amazon, Meta, Microsoft |
| 9 | Merge Intervals | Medium | Sort + sweep | https://leetcode.com/problems/merge-intervals/ | Amazon, Meta, Microsoft, Bloomberg |
| 10 | Minimum Window Substring | Hard | Sliding window + counts | https://leetcode.com/problems/minimum-window-substring/ | Amazon, Meta, Microsoft, LinkedIn |
| 11 | Word Ladder | Hard | BFS | https://leetcode.com/problems/word-ladder/ | Amazon, Meta, Google, LinkedIn |
| 12 | Median of Two Sorted Arrays | Hard | Partition binary search | https://leetcode.com/problems/median-of-two-sorted-arrays/ | Amazon, Google, Apple, Microsoft |
| 13 | Serialize and Deserialize Binary Tree | Hard | Tree encoding | https://leetcode.com/problems/serialize-and-deserialize-binary-tree/ | Amazon, Meta, LinkedIn, Microsoft |
| 14 | LRU Cache | Medium | HashMap + DLL | https://leetcode.com/problems/lru-cache/ | Amazon, Meta, Microsoft, Google, Apple |
| 15 | Word Break | Medium | DP | https://leetcode.com/problems/word-break/ | Amazon, Meta, Microsoft, Google |

## Stretch Problems

Bonus problems for deeper practice:

- [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) — combines recursion + DP cleanly.
- [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) — two-heap design.
- [Word Search II](https://leetcode.com/problems/word-search-ii/) — trie + backtracking.

## Patterns to Master This Week

- Pattern recognition first, code second. Look for: monotonic property → BS; "best in range" → sliding window / monotonic deque; "k-th" → heap or quickselect.
- Time/space budget: interviewers expect you to state complexity before coding. Pitfall: building over-engineered solutions when O(n^2) clearly fits.
- Practice talking aloud: state the approach, identify edge cases (empty input, all same, overflow), then implement. Pitfall: silent coding hides mistakes from the interviewer's feedback loop.
