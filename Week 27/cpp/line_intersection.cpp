/*
 * WEEK 27 - C++ ADVANCED TOPICS
 * Topic: Line Segment Intersection
 * File: line_intersection.cpp
 *
 * CONCEPT:
 *   Two segments AB and CD intersect when their endpoints "straddle" each
 *   other, captured by the cross-product orientation test:
 *     ccw(p,q,r) = sign((q-p) x (r-p)).
 *   A proper crossing happens when ccw(A,B,C) and ccw(A,B,D) differ in sign
 *   AND ccw(C,D,A) and ccw(C,D,B) differ in sign. Special cases handle
 *   collinear endpoints lying on the opposite segment.
 *
 * KEY POINTS:
 *   - O(1) per query.
 *   - Returns intersection point for non-parallel infinite lines via solving
 *     a 2x2 linear system using cross-product ratios.
 *
 * ALGORITHM / APPROACH:
 *   compute o1..o4 (orientations)
 *   if signs differ on both pairs -> intersect
 *   else handle 4 collinear endpoint cases
 *
 * C++-SPECIFIC NOTES:
 *   - Use long long for the cross product to avoid overflow.
 *   - Return std::optional<Point> for the intersection point.
 *
 * DRY RUN / EXAMPLE:
 *   AB = (0,0)-(4,4), CD = (0,4)-(4,0): proper crossing at (2,2).
 *
 * COMPLEXITY:
 *   Time O(1). Space O(1).
 */

#include <iostream>
#include <optional>
#include <algorithm>

using namespace std;

struct Point { double x, y; };

long long sgn(long long x) { return (x > 0) - (x < 0); }

long long ccw(const Point& a, const Point& b, const Point& c) {
    long double v = (long double)(b.x - a.x) * (c.y - a.y)
                  - (long double)(b.y - a.y) * (c.x - a.x);
    if (v > 0) return 1;
    if (v < 0) return -1;
    return 0;
}

bool onSegment(const Point& p, const Point& q, const Point& r) {
    return min(p.x, q.x) <= r.x && r.x <= max(p.x, q.x) &&
           min(p.y, q.y) <= r.y && r.y <= max(p.y, q.y);
}

bool segmentsIntersect(const Point& a, const Point& b, const Point& c, const Point& d) {
    long long o1 = ccw(a, b, c), o2 = ccw(a, b, d);
    long long o3 = ccw(c, d, a), o4 = ccw(c, d, b);
    if (o1 != o2 && o3 != o4) return true;
    if (o1 == 0 && onSegment(a, b, c)) return true;
    if (o2 == 0 && onSegment(a, b, d)) return true;
    if (o3 == 0 && onSegment(c, d, a)) return true;
    if (o4 == 0 && onSegment(c, d, b)) return true;
    return false;
}

optional<Point> lineIntersection(const Point& a, const Point& b, const Point& c, const Point& d) {
    double denom = (a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x);
    if (denom == 0.0) return nullopt;
    double t = ((a.x - c.x) * (c.y - d.y) - (a.y - c.y) * (c.x - d.x)) / denom;
    return Point{a.x + t * (b.x - a.x), a.y + t * (b.y - a.y)};
}

int main() {
    Point a{0,0}, b{4,4}, c{0,4}, d{4,0};
    cout << "Segments intersect: " << boolalpha << segmentsIntersect(a,b,c,d) << "\n";
    if (auto p = lineIntersection(a,b,c,d)) cout << "Point: (" << p->x << "," << p->y << ")\n";

    Point e{0,0}, f{5,0}, g{0,1}, h{5,1};
    cout << "Parallel intersect: " << boolalpha << segmentsIntersect(e,f,g,h) << "\n";
    cout << "Lines parallel: " << boolalpha << !lineIntersection(e,f,g,h).has_value() << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - Java's geometry.java does not include segment intersection; this file
 *     adds it.
 *   - std::optional<Point> represents "no intersection" cleanly.
 *   - long double in ccw guards against overflow on large coordinates.
 */
