# Week 15 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which heap pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given an array of n ≤ 10^6 integers and an integer k, return the k-th largest element.
Pattern: ______
Why: ______

### 2. Given n ≤ 10^6 strings and an integer k, return the k most frequent strings.
Pattern: ______
Why: ______

### 3. Given a stream of integers, after each insertion report the running median. Up to 10^5 insertions.
Pattern: ______
Why: ______

### 4. Given k sorted linked lists, merge them into a single sorted linked list. Total nodes up to 10^5.
Pattern: ______
Why: ______

### 5. Given an array of CPU tasks with cooldown constraints (same task needs ≥ n idle time between consecutive runs), return the minimum total time. Up to 10^4 tasks.
Pattern: ______
Why: ______

### 6. Given n points on a plane, return the k closest to the origin.
Pattern: ______
Why: ______

### 7. Distractor: Given a sorted array, find the k-th smallest. (Why is a heap overkill?)
Pattern: ______
Why: ______

### 8. Implement a priority-aware event scheduler: insert `(time, event)` pairs and repeatedly pop the earliest event.
Pattern: ______
Why: ______

### 9. Given a set of intervals `[s, e]` representing meetings, find the minimum number of conference rooms required. n ≤ 10^5.
Pattern: ______
Why: ______

### 10. Distractor: Given an array, return all elements that appear more than ⌊n/3⌋ times. (Does a heap help?)
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Min-heap of size k (or quickselect). **Why**: keep only the k largest seen so far; heap top is the answer — O(n log k).
2. **Pattern**: Frequency map + min-heap of size k. **Why**: count then keep top k by frequency.
3. **Pattern**: Two heaps (max-heap of lower half + min-heap of upper half). **Why**: balance sizes so tops give median.
4. **Pattern**: Min-heap of list heads. **Why**: always pull smallest among k current heads.
5. **Pattern**: Max-heap of remaining counts + cooldown queue. **Why**: at each tick, take most-frequent remaining task; cool it down.
6. **Pattern**: Max-heap of size k on distance. **Why**: keep the k smallest distances.
7. **Pattern**: Distractor — direct indexing, O(1). **Why**: sorted input makes the k-th smallest trivially `a[k-1]`. The heap is wrong here.
8. **Pattern**: Min-heap keyed on time. **Why**: classic priority queue — earliest deadline first.
9. **Pattern**: Sort starts + min-heap of end times (or sweep-line). **Why**: a meeting can reuse a room if its start ≥ earliest end.
10. **Pattern**: Distractor — Boyer–Moore generalized vote (Week 6). **Why**: at most two candidates can exceed n/3; heap doesn't beat O(n) here.

</details>
