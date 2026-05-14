# Week 30: Interview Patterns & Mastery
# Two Pointers, Sliding Window, Fast & Slow Pointers, Merge Intervals, Top-K Elements

import heapq
from collections import Counter, defaultdict
from typing import List, Optional

# =========================================================================
# TWO POINTERS
# =========================================================================

def two_sum_ii(nums: List[int], target: int) -> List[int]:
    """Two Sum II - sorted array (LC 167) - Time: O(n), Space: O(1)"""
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left + 1, right + 1]  # 1-indexed
        elif s < target:
            left += 1
        else:
            right -= 1
    return []

def three_sum(nums: List[int]) -> List[List[int]]:
    """3Sum (LC 15) - Time: O(n^2), Space: O(1) extra"""
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s == 0:
                result.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]: l += 1
                while l < r and nums[r] == nums[r - 1]: r -= 1
                l += 1; r -= 1
            elif s < 0:
                l += 1
            else:
                r -= 1
    return result

def max_area(height: List[int]) -> int:
    """Container With Most Water (LC 11) - Time: O(n), Space: O(1)"""
    l, r = 0, len(height) - 1
    best = 0
    while l < r:
        best = max(best, (r - l) * min(height[l], height[r]))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best

# =========================================================================
# SLIDING WINDOW
# =========================================================================

def length_of_longest_substring(s: str) -> int:
    """Longest Substring Without Repeating Characters (LC 3) - Time: O(n), Space: O(min(n, charset))"""
    char_idx = {}
    left = max_len = 0
    for right, ch in enumerate(s):
        if ch in char_idx and char_idx[ch] >= left:
            left = char_idx[ch] + 1
        char_idx[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len

def min_window(s: str, t: str) -> str:
    """Minimum Window Substring (LC 76) - Time: O(n + m), Space: O(m)"""
    if len(s) < len(t):
        return ""
    need = Counter(t)
    missing = len(t)
    left = 0
    best = (0, float('inf'))
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left < best[1] - best[0]:
                best = (left, right)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best[1] == float('inf') else s[best[0]:best[1] + 1]

# =========================================================================
# FAST & SLOW POINTERS
# =========================================================================

class ListNode:
    def __init__(self, val: int = 0, next: Optional['ListNode'] = None):
        self.val = val
        self.next = next

def has_cycle(head: Optional[ListNode]) -> bool:
    """Linked List Cycle Detection (LC 141) - Time: O(n), Space: O(1)"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False

def detect_cycle_start(head: Optional[ListNode]) -> Optional[ListNode]:
    """Cycle Start Detection (LC 142) - Time: O(n), Space: O(1)"""
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            entry = head
            while entry is not slow:
                entry = entry.next
                slow = slow.next
            return entry
    return None

def is_happy(n: int) -> bool:
    """Happy Number (LC 202) - Time: O(log n), Space: O(1)"""
    def digit_square_sum(x: int) -> int:
        total = 0
        while x:
            x, d = divmod(x, 10)
            total += d * d
        return total

    slow = fast = n
    while True:
        slow = digit_square_sum(slow)
        fast = digit_square_sum(digit_square_sum(fast))
        if slow == fast:
            break
    return slow == 1

# =========================================================================
# MERGE INTERVALS
# =========================================================================

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """Merge Intervals (LC 56) - Time: O(n log n), Space: O(n)"""
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

def insert_interval(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:
    """Insert Interval (LC 57) - Time: O(n), Space: O(n)"""
    result = []
    i, n = 0, len(intervals)

    # Add intervals ending before new_interval starts
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1

    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    result.append(new_interval)

    # Add remaining
    while i < n:
        result.append(intervals[i])
        i += 1
    return result

# =========================================================================
# TOP-K ELEMENTS
# =========================================================================

def find_kth_largest(nums: List[int], k: int) -> int:
    """Kth Largest Element (LC 215) - Time: O(n log k), Space: O(k)"""
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

def top_k_frequent(nums: List[int], k: int) -> List[int]:
    """Top K Frequent Elements (LC 347) - Time: O(n log k), Space: O(n)"""
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)

def top_k_frequent_bucket(nums: List[int], k: int) -> List[int]:
    """Top K Frequent - Bucket Sort (LC 347) - Time: O(n), Space: O(n)"""
    freq = Counter(nums)
    buckets: List[List[int]] = [[] for _ in range(len(nums) + 1)]
    for num, count in freq.items():
        buckets[count].append(num)

    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result

# =========================================================================
# DEMO
# =========================================================================

if __name__ == "__main__":
    print("=== TWO POINTERS ===")
    print(f"Two Sum II [2,7,11,15] t=9: {two_sum_ii([2, 7, 11, 15], 9)}")
    print(f"3Sum [-1,0,1,2,-1,-4]: {three_sum([-1, 0, 1, 2, -1, -4])}")
    print(f"Max Area [1,8,6,2,5,4,8,3,7]: {max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])}")

    print("\n=== SLIDING WINDOW ===")
    print(f"Longest unique 'abcabcbb': {length_of_longest_substring('abcabcbb')}")
    print(f"Min window 'ADOBECODEBANC','ABC': {min_window('ADOBECODEBANC', 'ABC')}")

    print("\n=== FAST & SLOW ===")
    print(f"Happy 19: {is_happy(19)}")
    print(f"Happy 2: {is_happy(2)}")
    a, b, c = ListNode(1), ListNode(2), ListNode(3)
    a.next, b.next, c.next = b, c, b
    print(f"Cycle: {has_cycle(a)}, starts at: {detect_cycle_start(a).val}")

    print("\n=== MERGE INTERVALS ===")
    print(f"Merged: {merge_intervals([[1,3],[2,6],[8,10],[15,18]])}")
    print(f"Inserted: {insert_interval([[1,3],[6,9]], [2,5])}")

    print("\n=== TOP-K ===")
    print(f"Kth largest k=2: {find_kth_largest([3,2,1,5,6,4], 2)}")
    print(f"Top 2 frequent: {top_k_frequent([1,1,1,2,2,3], 2)}")
    print(f"Top 2 bucket: {top_k_frequent_bucket([1,1,1,2,2,3], 2)}")
