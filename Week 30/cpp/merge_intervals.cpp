/*
 * WEEK 30 - C++ ADVANCED TOPICS
 * Topic: Merge Intervals Pattern
 * File: merge_intervals.cpp
 *
 * CONCEPT:
 *   A family of interval problems: merge overlapping intervals, insert a
 *   new interval, count meeting rooms needed, etc. Sort by start, then a
 *   single pass.
 *
 * KEY POINTS:
 *   - Sort by start; merge if next.start <= last.end.
 *   - For insertion when input is sorted: 3 passes (before/overlap/after).
 *   - For meeting rooms: sorted starts/ends two-pointer trick.
 *
 * ALGORITHM / APPROACH:
 *   MERGE: sort; push first; for each iv extend or push.
 *   INSERT: 3-pass linear scan.
 *   ROOMS:  scan sorted starts vs sorted ends.
 *
 * C++-SPECIFIC NOTES:
 *   - vector<pair<int,int>> or vector<vector<int>> for intervals.
 *   - std::sort with default tuple/pair comparator.
 *
 * DRY RUN / EXAMPLE:
 *   merge {{1,3},{2,6},{8,10},{15,18}} -> {{1,6},{8,10},{15,18}}.
 *   insert {{1,3},{6,9}} with {2,5} -> {{1,5},{6,9}}.
 *   meeting rooms {{0,30},{5,10},{15,20}} -> 2.
 *
 * COMPLEXITY:
 *   Merge / Rooms O(n log n). Insert O(n).
 */

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

vector<vector<int>> mergeIntervals(vector<vector<int>> intervals) {
    if (intervals.empty()) return {};
    sort(intervals.begin(), intervals.end(),
         [](auto& a, auto& b) { return a[0] < b[0]; });
    vector<vector<int>> out{intervals[0]};
    for (int i = 1; i < (int)intervals.size(); ++i) {
        auto& last = out.back();
        if (intervals[i][0] <= last[1]) last[1] = max(last[1], intervals[i][1]);
        else out.push_back(intervals[i]);
    }
    return out;
}

vector<vector<int>> insertInterval(const vector<vector<int>>& intervals, vector<int> newIv) {
    vector<vector<int>> out;
    int n = (int)intervals.size(), i = 0;
    while (i < n && intervals[i][1] < newIv[0]) out.push_back(intervals[i++]);
    while (i < n && intervals[i][0] <= newIv[1]) {
        newIv[0] = min(newIv[0], intervals[i][0]);
        newIv[1] = max(newIv[1], intervals[i][1]);
        ++i;
    }
    out.push_back(newIv);
    while (i < n) out.push_back(intervals[i++]);
    return out;
}

int minMeetingRooms(vector<vector<int>> intervals) {
    if (intervals.empty()) return 0;
    int n = (int)intervals.size();
    vector<int> starts(n), ends(n);
    for (int i = 0; i < n; ++i) { starts[i] = intervals[i][0]; ends[i] = intervals[i][1]; }
    sort(starts.begin(), starts.end());
    sort(ends.begin(), ends.end());
    int rooms = 0, busiest = 0, j = 0;
    for (int s : starts) {
        if (s < ends[j]) { ++rooms; busiest = max(busiest, rooms); }
        else ++j;
    }
    return busiest;
}

bool canAttendAll(vector<vector<int>> intervals) {
    sort(intervals.begin(), intervals.end());
    for (int i = 1; i < (int)intervals.size(); ++i)
        if (intervals[i][0] < intervals[i-1][1]) return false;
    return true;
}

int main() {
    auto m = mergeIntervals({{1,3},{2,6},{8,10},{15,18}});
    cout << "Merged:";
    for (auto& iv : m) cout << " [" << iv[0] << "," << iv[1] << "]";
    cout << "\n";

    auto ins = insertInterval({{1,3},{6,9}}, {2,5});
    cout << "Inserted:";
    for (auto& iv : ins) cout << " [" << iv[0] << "," << iv[1] << "]";
    cout << "\n";

    cout << "Min meeting rooms: " << minMeetingRooms({{0,30},{5,10},{15,20}}) << "\n";
    cout << "Can attend all: " << boolalpha
         << canAttendAll({{0,30},{5,10},{15,20}}) << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - vector<vector<int>> for intervals.
 *   - Adds minMeetingRooms (LC 253) and canAttendAll (LC 252) on top of
 *     Java's mergeIntervals/insertInterval.
 */
