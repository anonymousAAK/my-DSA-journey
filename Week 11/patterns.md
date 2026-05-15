# Week 11 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which linked-list pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Given the head of a singly linked list of up to 10^5 nodes, detect whether it contains a cycle. O(1) extra space.
Pattern: ______
Why: ______

### 2. Given the head of a singly linked list, reverse it in place. n ≤ 10^5.
Pattern: ______
Why: ______

### 3. Given two sorted linked lists, merge them into one sorted linked list. Total nodes ≤ 10^5.
Pattern: ______
Why: ______

### 4. Given the head of a singly linked list, find the node at the middle. If the list has even length, return the second middle.
Pattern: ______
Why: ______

### 5. Design a data structure supporting `get(key)` and `put(key, value)` in O(1), evicting the least-recently-used entry when capacity is exceeded.
Pattern: ______
Why: ______

### 6. Given the head of a linked list, remove the n-th node from the end in a single pass.
Pattern: ______
Why: ______

### 7. Distractor: Given a *sorted array*, decide whether two elements sum to a target. (Why is this not a linked-list problem even though it looks pointer-y?)
Pattern: ______
Why: ______

### 8. Given the head of a linked list where each node has a `next` and a `random` pointer, deep-copy the list.
Pattern: ______
Why: ______

### 9. Given two singly linked lists, find the node at which they intersect (or return null). O(m+n), O(1).
Pattern: ______
Why: ______

### 10. Given a linked list, decide if it forms a palindrome sequence of values. O(n) time, O(1) extra space.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Floyd's tortoise and hare. **Why**: fast/slow pointers meet inside any cycle — O(1) space.
2. **Pattern**: Iterative pointer reversal with `prev`, `curr`, `next`. **Why**: rewire one edge per step — O(n) / O(1).
3. **Pattern**: Two-pointer merge with dummy head. **Why**: classic merge step from merge sort.
4. **Pattern**: Fast/slow pointer (hare moves 2x). **Why**: when fast hits end, slow is at middle.
5. **Pattern**: Doubly linked list + hashmap. **Why**: hashmap → O(1) lookup of node; DLL → O(1) move-to-front / evict-tail.
6. **Pattern**: Two pointers with n-gap. **Why**: advance one pointer n steps, then walk both till the leader hits null.
7. **Pattern**: Distractor — two pointers on array (Week 6), not a list problem. **Why**: arrays support random access; "pointer" is metaphorical here.
8. **Pattern**: Interleave clones then split, or hashmap original→copy. **Why**: random pointers force two passes — first build the mapping, then wire it up.
9. **Pattern**: Length-difference align, or pointer swap to opposite head. **Why**: walking m+n with swap guarantees both pointers traverse equal total distance.
10. **Pattern**: Find middle (fast/slow) + reverse second half + compare. **Why**: in-place transform → linear compare.

</details>
