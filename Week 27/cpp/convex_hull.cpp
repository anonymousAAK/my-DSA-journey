/*
 * WEEK 27 - C++ ADVANCED TOPICS
 * Topic: Convex Hull (Andrew's Monotone Chain)
 * File: convex_hull.cpp
 *
 * CONCEPT:
 *   Smallest convex polygon containing all input points. Andrew's monotone
 *   chain sorts points lex (x then y) and walks them left-to-right (lower
 *   hull) and right-to-left (upper hull) using a cross-product orientation
 *   test on the running stack.
 *
 * KEY POINTS:
 *   - Cross product (a-o)x(b-o) > 0 means counter-clockwise turn.
 *   - Pop while the last triple is non-CCW (<=0) for a strict CCW hull.
 *   - O(n log n) total work, dominated by the sort.
 *
 * ALGORITHM / APPROACH:
 *   sort(points)
 *   build lower hull
 *   build upper hull (reverse iteration)
 *   concatenate, dropping the duplicated end-points
 *
 * C++-SPECIFIC NOTES:
 *   - Use `struct Point { long long x, y; }` to avoid floating-point error.
 *   - Cross product as long long since (a-o)x(b-o) can grow.
 *   - std::sort with a comparator handles lex ordering.
 *
 * DRY RUN / EXAMPLE:
 *   pts = {(0,0),(1,1),(2,2),(3,1),(0,3),(2,4)}
 *   Hull -> {(0,0),(3,1),(2,4),(0,3)} (CCW order).
 *
 * COMPLEXITY:
 *   Time: O(n log n)   Space: O(n)
 */

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

struct Point {
    long long x, y;
    bool operator<(const Point& o) const {
        return x != o.x ? x < o.x : y < o.y;
    }
    bool operator==(const Point& o) const { return x == o.x && y == o.y; }
};

long long cross(const Point& o, const Point& a, const Point& b) {
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);
}

vector<Point> convexHull(vector<Point> pts) {
    sort(pts.begin(), pts.end());
    pts.erase(unique(pts.begin(), pts.end()), pts.end());
    int n = (int)pts.size();
    if (n < 2) return pts;
    vector<Point> hull;
    // Lower hull
    for (const auto& p : pts) {
        while (hull.size() >= 2 && cross(hull[hull.size()-2], hull.back(), p) <= 0)
            hull.pop_back();
        hull.push_back(p);
    }
    // Upper hull
    int lower = (int)hull.size() + 1;
    for (int i = n - 2; i >= 0; --i) {
        while ((int)hull.size() >= lower &&
               cross(hull[hull.size()-2], hull.back(), pts[i]) <= 0)
            hull.pop_back();
        hull.push_back(pts[i]);
    }
    hull.pop_back();
    return hull;
}

int main() {
    vector<Point> pts = {{0,0},{1,1},{2,2},{3,1},{0,3},{2,4}};
    auto hull = convexHull(pts);
    cout << "Convex hull:";
    for (auto& p : hull) cout << " (" << p.x << "," << p.y << ")";
    cout << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - C++ uses a struct Point with long long coords; Java's geometry.java
 *     used int[] arrays.
 *   - We deduplicate with sort+unique which guards against degenerate input.
 *   - The "lower" sentinel is `hull.size()+1` after the lower hull is built
 *     so we never pop into the lower hull during the upper-hull pass.
 */
