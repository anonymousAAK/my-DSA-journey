/*
 * WEEK 27 - C++ ADVANCED TOPICS
 * Topic: Sweep Line - Skyline & Max Overlap
 * File: sweep_line.cpp
 *
 * CONCEPT:
 *   Sweep an imaginary vertical line across the plane, processing events in
 *   x order while maintaining an "active set". Two showcase problems:
 *     - Skyline: max-heap of active building heights gives the silhouette.
 *     - Max overlap: counting +1/-1 events finds the maximum simultaneous
 *       active intervals.
 *
 * KEY POINTS:
 *   - Sort events by primary x then a sensible tie-breaker.
 *   - For skyline: use a max-heap (priority_queue<pair<int,int>>) of
 *     (height, end_x); pop expired tops lazily.
 *
 * ALGORITHM / APPROACH:
 *   SKYLINE: events for each building -> (l, h, r) start, (r, 0, 0) end.
 *           sort; max-heap of (h, r); on each event update heap, lazily
 *           drop expired, emit (x, h_max) when h_max changes.
 *   OVERLAP: events (start,+1), (end,-1); sort; running counter -> max.
 *
 * C++-SPECIFIC NOTES:
 *   - priority_queue<pair<int,int>> is a max-heap by default.
 *   - Use INT_MAX as a sentinel "never expires" entry to avoid empty-heap
 *     edge cases.
 *
 * DRY RUN / EXAMPLE:
 *   buildings = {{2,9,10},{3,7,15},{5,12,12},{15,20,10},{19,24,8}}
 *   skyline   = {(2,10),(3,15),(7,12),(12,0),(15,10),(20,8),(24,0)}
 *
 * COMPLEXITY:
 *   Time O(n log n), Space O(n).
 */

#include <iostream>
#include <vector>
#include <queue>
#include <algorithm>
#include <climits>

using namespace std;

vector<pair<int,int>> skyline(vector<tuple<int,int,int>> buildings) {
    // events: (x, height) — height>0 = start, ==0 = end
    vector<tuple<int,int,int>> events; // (x, h, r)
    for (auto& [l, r, h] : buildings) {
        events.emplace_back(l, h, r);     // start
        events.emplace_back(r, 0, 0);     // end
    }
    sort(events.begin(), events.end(), [](auto& a, auto& b) {
        if (get<0>(a) != get<0>(b)) return get<0>(a) < get<0>(b);
        return get<1>(a) > get<1>(b); // taller starts first
    });
    priority_queue<pair<int,int>> heap; // (height, end_x)
    heap.emplace(0, INT_MAX);
    vector<pair<int,int>> result;
    for (auto& [x, h, r] : events) {
        if (h) heap.emplace(h, r);
        while (heap.top().second <= x) heap.pop();
        int curH = heap.top().first;
        if (result.empty() || result.back().second != curH)
            result.emplace_back(x, curH);
    }
    return result;
}

int maxOverlap(vector<pair<int,int>> intervals) {
    vector<pair<int,int>> events;
    for (auto& [s, e] : intervals) {
        events.emplace_back(s, +1);
        events.emplace_back(e, -1);
    }
    sort(events.begin(), events.end(), [](auto& a, auto& b) {
        if (a.first != b.first) return a.first < b.first;
        return a.second > b.second; // opens before closes at same x
    });
    int cur = 0, best = 0;
    for (auto& [x, d] : events) {
        cur += d;
        best = max(best, cur);
    }
    return best;
}

int main() {
    auto sk = skyline({{2,9,10},{3,7,15},{5,12,12},{15,20,10},{19,24,8}});
    cout << "Skyline:";
    for (auto& [x, h] : sk) cout << " (" << x << "," << h << ")";
    cout << "\n";
    cout << "Max overlap: " << maxOverlap({{1,5},{2,6},{3,4},{7,8}}) << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - Java's geometry.java does not include sweep-line algorithms; we add
 *     the skyline and overlap classics for completeness.
 *   - std::priority_queue + lazy deletion (sentinel INT_MAX) avoids the
 *     overhead of a full balanced BST.
 */
