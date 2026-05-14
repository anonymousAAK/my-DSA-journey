/*
 * WEEK 19 - C++ DSA
 * Topic: Greedy Algorithms — Paradigm + Classic Problems
 * File: 1.GreedyAlgorithms.cpp
 *
 * CONCEPT:
 *     Greedy algorithms always pick the locally optimal choice. They work
 *     when the problem has greedy-choice property + optimal substructure.
 *     Greedy is fast (typically O(n log n) for the sort) but only correct
 *     on certain problems.
 *
 * KEY POINTS:
 *     - Sort + scan is the most common pattern.
 *     - std::priority_queue is C++'s heap (max-heap by default; pass
 *       std::greater<> for a min-heap).
 *     - Use exchange-argument proofs to verify greediness.
 *
 * ALGORITHM / APPROACH:
 *     Five canonical problems:
 *         1. Activity Selection         (sort by end; pick non-overlapping)
 *         2. Fractional Knapsack        (sort by value/weight desc)
 *         3. Min Coins (canonical)      (always take largest coin)
 *         4. Merge Intervals            (sort by start; merge overlaps)
 *         5. Min Meeting Rooms          (sort + min-heap of end times)
 *
 * C++-SPECIFIC NOTES:
 *     - std::sort with lambda comparator.
 *     - std::priority_queue<int, vector<int>, std::greater<>> = min-heap.
 *     - Use std::pair for (start, end) intervals or a small struct.
 *     - LinkedHashMap-style insertion-ordered map: std::vector<pair<...>>.
 *
 * DRY RUN:
 *     Activity Selection on
 *         start = {1, 3, 0, 5, 8, 5}
 *         end   = {2, 4, 6, 7, 9, 9}
 *     Sorting indices by end gives [0,1,3,2,4,5] -> ends [2,4,7,6,9,9].
 *     Pick 0 (end 2); 1 starts at 3>=2 pick; 3 starts at 5>=4 pick;
 *     2 starts at 0<7 skip; 4 starts at 8>=7 pick; 5 starts at 5<9 skip.
 *     Result = 4.
 *
 *     Min Meeting Rooms [[0,30],[5,10],[15,20]]
 *         heap=[30]; (5,10): 5<30 push 10 -> heap=[10,30];
 *         (15,20): 15>=10 pop 10 push 20 -> heap=[20,30].
 *         Answer = heap.size() = 2.
 *
 * COMPLEXITY:
 *     activitySelection      O(n log n)
 *     fractionalKnapsack     O(n log n)
 *     minCoinsGreedy         O(c log c)
 *     mergeIntervals         O(n log n)
 *     minMeetingRooms        O(n log n)
 */

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <utility>
#include <map>

using std::vector;
using std::pair;

// 1. ACTIVITY SELECTION
int activitySelection(const vector<int>& start, const vector<int>& end) {
    int n = (int)start.size();
    if (n == 0) return 0;
    vector<int> idx(n);
    for (int i = 0; i < n; ++i) idx[i] = i;
    std::sort(idx.begin(), idx.end(),
              [&](int a, int b){ return end[a] < end[b]; });
    int count = 1, lastEnd = end[idx[0]];
    for (int k = 1; k < n; ++k) {
        if (start[idx[k]] >= lastEnd) {
            ++count;
            lastEnd = end[idx[k]];
        }
    }
    return count;
}

// 2. FRACTIONAL KNAPSACK
double fractionalKnapsack(const vector<int>& weights, const vector<int>& values, int W) {
    int n = (int)weights.size();
    vector<int> idx(n);
    for (int i = 0; i < n; ++i) idx[i] = i;
    std::sort(idx.begin(), idx.end(), [&](int a, int b) {
        return (double)values[a] / weights[a] > (double)values[b] / weights[b];
    });
    double total = 0.0;
    int remaining = W;
    for (int i : idx) {
        if (remaining <= 0) break;
        int take = std::min(weights[i], remaining);
        total += take * (double)values[i] / weights[i];
        remaining -= take;
    }
    return total;
}

// 3. MIN COINS (canonical systems only)
std::vector<pair<int,int>> minCoinsGreedy(vector<int> coins, int target) {
    std::sort(coins.begin(), coins.end(), std::greater<int>());
    std::vector<pair<int,int>> result;
    for (int c : coins) {
        if (target <= 0) break;
        if (c <= target) {
            int count = target / c;
            result.emplace_back(c, count);
            target -= c * count;
        }
    }
    return result;
}

// 4. MERGE INTERVALS
vector<pair<int,int>> mergeIntervals(vector<pair<int,int>> intervals) {
    if (intervals.size() <= 1) return intervals;
    std::sort(intervals.begin(), intervals.end(),
              [](const pair<int,int>& a, const pair<int,int>& b){ return a.first < b.first; });
    vector<pair<int,int>> merged;
    merged.push_back(intervals[0]);
    for (size_t i = 1; i < intervals.size(); ++i) {
        auto& last = merged.back();
        if (intervals[i].first <= last.second) {
            last.second = std::max(last.second, intervals[i].second);
        } else {
            merged.push_back(intervals[i]);
        }
    }
    return merged;
}

// 5. MIN MEETING ROOMS
int minMeetingRooms(vector<pair<int,int>> intervals) {
    if (intervals.empty()) return 0;
    std::sort(intervals.begin(), intervals.end(),
              [](const pair<int,int>& a, const pair<int,int>& b){ return a.first < b.first; });
    std::priority_queue<int, vector<int>, std::greater<int>> ends;       // min-heap
    ends.push(intervals[0].second);
    for (size_t i = 1; i < intervals.size(); ++i) {
        if (intervals[i].first >= ends.top()) ends.pop();                 // room frees
        ends.push(intervals[i].second);
    }
    return (int)ends.size();
}

int main() {
    std::cout << "=== Activity Selection ===\n";
    vector<int> start{1, 3, 0, 5, 8, 5};
    vector<int> end{2, 4, 6, 7, 9, 9};
    std::cout << "Max activities: " << activitySelection(start, end) << "\n"; // 4

    std::cout << "\n=== Fractional Knapsack ===\n";
    std::cout.setf(std::ios::fixed); std::cout.precision(2);
    std::cout << "Max value: " <<
        fractionalKnapsack({10, 20, 30}, {60, 100, 120}, 50) << "\n";        // 240.00

    std::cout << "\n=== Min Coins (US denominations) ===\n";
    auto print_coins = [](const std::vector<pair<int,int>>& v) {
        std::cout << "{";
        for (size_t i = 0; i < v.size(); ++i)
            std::cout << v[i].first << "x" << v[i].second
                      << (i+1<v.size() ? ", " : "");
        std::cout << "}\n";
    };
    std::cout << "Change for 87: "; print_coins(minCoinsGreedy({1,5,10,25,50,100}, 87));
    std::cout << "Change for 30: "; print_coins(minCoinsGreedy({1,5,10,25,50,100}, 30));

    std::cout << "\n=== Merge Intervals ===\n";
    auto merged = mergeIntervals({{1,3},{2,6},{8,10},{15,18}});
    std::cout << "Merged: ";
    for (auto& p : merged) std::cout << "[" << p.first << "," << p.second << "] ";
    std::cout << "\n";

    std::cout << "\n=== Min Meeting Rooms ===\n";
    std::cout << "Rooms needed: " << minMeetingRooms({{0,30},{5,10},{15,20}}) << "\n"; // 2
    std::cout << "Rooms needed: " << minMeetingRooms({{7,10},{2,4}}) << "\n";          // 1
}

/*
 * NOTES (C++ vs Java):
 *   - Java requires Integer[] for sorting indices via Comparator; in C++ we
 *     just sort a vector<int> with a lambda referencing the underlying arrays.
 *   - std::priority_queue defaults to max-heap; pass std::greater<int> as
 *     the third template argument for a min-heap.
 *   - std::pair<int,int> is the lightweight (start,end) interval; for clarity
 *     in larger code, define a small struct.
 *   - merging modifies the back element in place — OK because we copied the
 *     interval into the result vector.
 *   - For canonical coin systems greedy is correct; for arbitrary coin sets
 *     fall back to DP (see Week 18).
 */
