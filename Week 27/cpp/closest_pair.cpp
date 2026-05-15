/*
 * WEEK 27 - C++ ADVANCED TOPICS
 * Topic: Closest Pair of Points
 * File: closest_pair.cpp
 *
 * CONCEPT:
 *   Divide-and-conquer for the smallest pair distance among n points. Sort
 *   by x; recurse on each half; combine across the dividing line by
 *   examining only points within distance d of it, sorted by y.
 *
 * KEY POINTS:
 *   - Strip combine: each point compares with at most ~7 successors.
 *   - Base case: <= 3 points -> brute force.
 *   - O(n log n) total.
 *
 * ALGORITHM / APPROACH:
 *   sort by x
 *   solve(l, r):
 *     if small -> brute force
 *     d = min(solve(left), solve(right))
 *     build strip; sort by y; scan adjacent pairs while dy < d
 *     return d
 *
 * C++-SPECIFIC NOTES:
 *   - struct Point { double x, y; }
 *   - Use std::hypot for distance.
 *   - sort with lambda by x.
 *
 * DRY RUN / EXAMPLE:
 *   pts = {(2,3),(12,30),(40,50),(5,1),(12,10),(3,4)} -> ~1.4142 (between
 *   (2,3) and (3,4)).
 *
 * COMPLEXITY:
 *   Time O(n log n)   Space O(n)
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <climits>

using namespace std;

struct Point { double x, y; };

double dist(const Point& a, const Point& b) {
    return hypot(a.x - b.x, a.y - b.y);
}

double solve(vector<Point>& pts, int l, int r) {
    if (r - l < 3) {
        double best = 1e18;
        for (int i = l; i <= r; ++i)
            for (int j = i + 1; j <= r; ++j)
                best = min(best, dist(pts[i], pts[j]));
        return best;
    }
    int mid = (l + r) / 2;
    double midX = pts[mid].x;
    double d = min(solve(pts, l, mid), solve(pts, mid + 1, r));
    vector<Point> strip;
    for (int i = l; i <= r; ++i)
        if (fabs(pts[i].x - midX) < d) strip.push_back(pts[i]);
    sort(strip.begin(), strip.end(), [](auto& a, auto& b) { return a.y < b.y; });
    for (int i = 0; i < (int)strip.size(); ++i)
        for (int j = i + 1; j < (int)strip.size() && strip[j].y - strip[i].y < d; ++j)
            d = min(d, dist(strip[i], strip[j]));
    return d;
}

double closestPair(vector<Point> pts) {
    if (pts.size() < 2) return 1e18;
    sort(pts.begin(), pts.end(), [](auto& a, auto& b) { return a.x < b.x; });
    return solve(pts, 0, (int)pts.size() - 1);
}

double closestPairBrute(const vector<Point>& pts) {
    double best = 1e18;
    for (int i = 0; i < (int)pts.size(); ++i)
        for (int j = i + 1; j < (int)pts.size(); ++j)
            best = min(best, dist(pts[i], pts[j]));
    return best;
}

int main() {
    vector<Point> pts = {{2,3},{12,30},{40,50},{5,1},{12,10},{3,4}};
    printf("Closest pair (D&C):       %.4f\n", closestPair(pts));
    printf("Closest pair (brute force): %.4f\n", closestPairBrute(pts));
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - C++ uses struct Point with doubles instead of int[].
 *   - std::hypot provides numerically stable Euclidean distance.
 *   - Brute-force baseline included for self-check.
 */
