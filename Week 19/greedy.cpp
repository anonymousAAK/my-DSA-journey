/*
 * =============================================================================
 * Week 19 — Greedy Algorithms  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. Activity Selection  (max non-overlapping activities)
 *   2. Fractional Knapsack
 *   3. Merge Intervals
 *   4. Minimum Meeting Rooms  (priority_queue)
 *   5. Job Sequencing with Deadlines
 *
 * Complexity cheat-sheet
 * ----------------------
 *   activity_selection     O(n log n)  |  Space O(n)
 *   fractional_knapsack    O(n log n)  |  Space O(n)
 *   merge_intervals        O(n log n)  |  Space O(n)
 *   min_meeting_rooms      O(n log n)  |  Space O(n)
 *   job_sequencing         O(n^2)      |  Space O(n)  (can be O(n log n) with DSU)
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o greedy greedy.cpp && ./greedy
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <cassert>
#include <sstream>
#include <numeric>
#include <iomanip>

// ---------------------------------------------------------------------------
// Helper
// ---------------------------------------------------------------------------
template <typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) oss << ", ";
        oss << v[i];
    }
    oss << "]";
    return oss.str();
}

std::string interval_str(const std::vector<std::pair<int,int>>& iv) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < iv.size(); ++i) {
        if (i) oss << ", ";
        oss << "[" << iv[i].first << "," << iv[i].second << "]";
    }
    oss << "]";
    return oss.str();
}

// ---------------------------------------------------------------------------
// 1. Activity Selection — select max non-overlapping activities
// ---------------------------------------------------------------------------
// Greedy choice: always pick the activity that finishes earliest.
// Complexity:  Time O(n log n)  |  Space O(n)
std::vector<std::pair<int,int>> activity_selection(std::vector<std::pair<int,int>> activities) {
    // Sort by finish time.
    std::sort(activities.begin(), activities.end(),
              [](const auto& a, const auto& b) { return a.second < b.second; });

    std::vector<std::pair<int,int>> selected;
    int last_finish = -1;

    for (const auto& [start, finish] : activities) {
        if (start >= last_finish) {
            selected.emplace_back(start, finish);
            last_finish = finish;
        }
    }
    return selected;
}

// ---------------------------------------------------------------------------
// 2. Fractional Knapsack
// ---------------------------------------------------------------------------
// Greedy choice: take items with highest value/weight ratio first.
// Complexity:  Time O(n log n)  |  Space O(n)
double fractional_knapsack(std::vector<std::pair<double,double>> items, double capacity) {
    // items[i] = {weight, value}
    // Sort by value/weight ratio descending.
    std::sort(items.begin(), items.end(), [](const auto& a, const auto& b) {
        return (a.second / a.first) > (b.second / b.first);
    });

    double total_value = 0.0;
    for (const auto& [w, v] : items) {
        if (capacity <= 0) break;
        double take = std::min(capacity, w);
        total_value += take * (v / w);
        capacity -= take;
    }
    return total_value;
}

// ---------------------------------------------------------------------------
// 3. Merge Intervals
// ---------------------------------------------------------------------------
// Complexity:  Time O(n log n)  |  Space O(n)
std::vector<std::pair<int,int>> merge_intervals(std::vector<std::pair<int,int>> intervals) {
    if (intervals.empty()) return {};

    std::sort(intervals.begin(), intervals.end());
    std::vector<std::pair<int,int>> merged;
    merged.push_back(intervals[0]);

    for (std::size_t i = 1; i < intervals.size(); ++i) {
        auto& back = merged.back();
        if (intervals[i].first <= back.second) {
            back.second = std::max(back.second, intervals[i].second);
        } else {
            merged.push_back(intervals[i]);
        }
    }
    return merged;
}

// ---------------------------------------------------------------------------
// 4. Minimum Meeting Rooms — sweep line with priority_queue
// ---------------------------------------------------------------------------
// Complexity:  Time O(n log n)  |  Space O(n)
int min_meeting_rooms(std::vector<std::pair<int,int>> meetings) {
    if (meetings.empty()) return 0;

    std::sort(meetings.begin(), meetings.end());

    // Min-heap of end times: tracks when each room becomes free.
    std::priority_queue<int, std::vector<int>, std::greater<>> pq;
    pq.push(meetings[0].second);

    for (std::size_t i = 1; i < meetings.size(); ++i) {
        // If earliest-ending meeting finishes before this one starts, reuse room.
        if (pq.top() <= meetings[i].first) {
            pq.pop();
        }
        pq.push(meetings[i].second);
    }
    return static_cast<int>(pq.size());
}

// ---------------------------------------------------------------------------
// 5. Job Sequencing with Deadlines
// ---------------------------------------------------------------------------
// Each job has (id, deadline, profit). Maximize profit; each job takes 1 unit.
// Greedy: sort by profit descending, assign to latest available slot.
// Complexity:  Time O(n^2)  |  Space O(n)
struct Job {
    char id;
    int deadline;
    int profit;
};

std::pair<int, std::string> job_sequencing(std::vector<Job> jobs) {
    // Sort by profit descending.
    std::sort(jobs.begin(), jobs.end(),
              [](const Job& a, const Job& b) { return a.profit > b.profit; });

    int max_deadline = 0;
    for (const auto& j : jobs) max_deadline = std::max(max_deadline, j.deadline);

    // slot[t] = '\0' means slot t is free (1-indexed).
    std::vector<char> slot(max_deadline + 1, '\0');
    int total_profit = 0;

    for (const auto& j : jobs) {
        // Find the latest free slot at or before j.deadline.
        for (int t = j.deadline; t >= 1; --t) {
            if (slot[t] == '\0') {
                slot[t] = j.id;
                total_profit += j.profit;
                break;
            }
        }
    }

    std::string sequence;
    for (int t = 1; t <= max_deadline; ++t) {
        if (slot[t] != '\0') sequence.push_back(slot[t]);
    }
    return {total_profit, sequence};
}

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 19: Greedy Algorithms ===\n\n";

    // 1. Activity Selection
    {
        std::cout << "-- Activity Selection --\n";
        std::vector<std::pair<int,int>> acts = {{1,4}, {3,5}, {0,6}, {5,7}, {3,9}, {5,9}, {6,10}, {8,11}, {8,12}, {2,14}, {12,16}};
        auto sel = activity_selection(acts);
        std::cout << "  selected: " << interval_str(sel) << "\n";
        assert(sel.size() == 4);  // e.g. (1,4), (5,7), (8,11), (12,16)
        std::cout << "  count=" << sel.size() << "\n\n";
    }

    // 2. Fractional Knapsack
    {
        std::cout << "-- Fractional Knapsack --\n";
        // {weight, value}
        std::vector<std::pair<double,double>> items = {{10, 60}, {20, 100}, {30, 120}};
        double cap = 50.0;
        double val = fractional_knapsack(items, cap);
        std::cout << std::fixed << std::setprecision(2);
        std::cout << "  max value = " << val << "  (capacity=" << cap << ")\n";
        assert(val >= 239.99 && val <= 240.01);  // 60 + 100 + 80 = 240
        std::cout << "\n";
    }

    // 3. Merge Intervals
    {
        std::cout << "-- Merge Intervals --\n";
        std::vector<std::pair<int,int>> iv = {{1,3}, {2,6}, {8,10}, {15,18}};
        auto merged = merge_intervals(iv);
        std::cout << "  input:  " << interval_str(iv) << "\n";
        std::cout << "  merged: " << interval_str(merged) << "\n";
        assert(merged.size() == 3);
        assert(merged[0] == std::make_pair(1, 6));
        std::cout << "\n";
    }

    // 4. Minimum Meeting Rooms
    {
        std::cout << "-- Minimum Meeting Rooms --\n";
        std::vector<std::pair<int,int>> meets = {{0,30}, {5,10}, {15,20}};
        int rooms = min_meeting_rooms(meets);
        assert(rooms == 2);
        std::cout << "  meetings: " << interval_str(meets) << "\n";
        std::cout << "  rooms needed: " << rooms << "\n\n";
    }

    // 5. Job Sequencing
    {
        std::cout << "-- Job Sequencing --\n";
        std::vector<Job> jobs = {
            {'a', 2, 100}, {'b', 1, 19}, {'c', 2, 27},
            {'d', 1, 25},  {'e', 3, 15}
        };
        auto [profit, seq] = job_sequencing(jobs);
        std::cout << "  max profit = " << profit << "  sequence = " << seq << "\n";
        assert(profit == 142);  // a(100) + c(27) + e(15) = 142
    }

    std::cout << "\nAll Week 19 tests passed.\n";
    return 0;
}
