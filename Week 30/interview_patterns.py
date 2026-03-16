# Week 30: Interview Patterns & Mastery
# Two Pointers, Sliding Window, Fast & Slow, Merge Intervals, Top-K

import heapq
from collections import Counter

# === Two Pointers ===
def two_sum_sorted(nums, target):
    """LC 167 - O(n)"""
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target: return [left, right]
        elif s < target: left += 1
        else: right -= 1
    return []

def three_sum(nums):
    """LC 15 - O(n^2)"""
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i-1]: continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s == 0:
                result.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l+1]: l += 1
                while l < r and nums[r] == nums[r-1]: r -= 1
                l += 1; r -= 1
            elif s < 0: l += 1
            else: r -= 1
    return result

# === Sliding Window ===
def length_of_longest_substring(s):
    """LC 3 - O(n)"""
    char_idx = {}
    left = max_len = 0
    for right, ch in enumerate(s):
        if ch in char_idx and char_idx[ch] >= left:
            left = char_idx[ch] + 1
        char_idx[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len

def min_window(s, t):
    """LC 76 - O(n)"""
    need = Counter(t)
    missing = len(t)
    left = 0
    best = (0, float('inf'))
    for right, ch in enumerate(s):
        if need[ch] > 0: missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left < best[1] - best[0]:
                best = (left, right)
            need[s[left]] += 1
            if need[s[left]] > 0: missing += 1
            left += 1
    return "" if best[1] == float('inf') else s[best[0]:best[1]+1]

# === Fast & Slow Pointers ===
def is_happy(n):
    """LC 202 - O(log n)"""
    def next_num(num):
        total = 0
        while num:
            num, d = divmod(num, 10)
            total += d * d
        return total
    slow, fast = n, next_num(n)
    while fast != 1 and slow != fast:
        slow = next_num(slow)
        fast = next_num(next_num(fast))
    return fast == 1

# === Merge Intervals ===
def merge(intervals):
    """LC 56 - O(n log n)"""
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# === Top-K Elements ===
def find_kth_largest(nums, k):
    """LC 215 - O(n log k)"""
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k: heapq.heappop(heap)
    return heap[0]

def top_k_frequent(nums, k):
    """LC 347 - O(n log k)"""
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)

if __name__ == "__main__":
    print(f"Two Sum: {two_sum_sorted([2,7,11,15], 9)}")
    print(f"3Sum: {three_sum([-1,0,1,2,-1,-4])}")
    print(f"Longest substring: {length_of_longest_substring('abcabcbb')}")
    print(f"Min window: {min_window('ADOBECODEBANC', 'ABC')}")
    print(f"Happy 19: {is_happy(19)}")
    print(f"Merge: {merge([[1,3],[2,6],[8,10],[15,18]])}")
    print(f"3rd largest: {find_kth_largest([3,2,1,5,6,4], 3)}")
    print(f"Top 2 frequent: {top_k_frequent([1,1,1,2,2,3], 2)}")
