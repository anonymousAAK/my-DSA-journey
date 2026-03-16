// Week 27: Computational Geometry
// Convex Hull O(n log n), Closest Pair O(n log n)

#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
using namespace std;

struct Point { double x, y; };

double cross(Point o, Point a, Point b) {
    return (a.x-o.x)*(b.y-o.y) - (a.y-o.y)*(b.x-o.x);
}

// === Convex Hull (Andrew's Monotone Chain) ===
vector<Point> convexHull(vector<Point> pts) {
    int n = pts.size();
    if (n < 2) return pts;
    sort(pts.begin(), pts.end(), [](auto& a, auto& b) {
        return a.x < b.x || (a.x == b.x && a.y < b.y);
    });
    vector<Point> hull;
    for (auto& p : pts) {
        while (hull.size() >= 2 && cross(hull[hull.size()-2], hull.back(), p) <= 0)
            hull.pop_back();
        hull.push_back(p);
    }
    int lower = hull.size() + 1;
    for (int i = n-2; i >= 0; i--) {
        while ((int)hull.size() >= lower && cross(hull[hull.size()-2], hull.back(), pts[i]) <= 0)
            hull.pop_back();
        hull.push_back(pts[i]);
    }
    hull.pop_back();
    return hull;
}

// === Closest Pair ===
double dist(Point a, Point b) {
    return sqrt((a.x-b.x)*(a.x-b.x) + (a.y-b.y)*(a.y-b.y));
}

double closestPair(vector<Point>& pts, int l, int r) {
    if (r - l < 3) {
        double best = 1e18;
        for (int i = l; i <= r; i++)
            for (int j = i+1; j <= r; j++)
                best = min(best, dist(pts[i], pts[j]));
        return best;
    }
    int mid = (l+r)/2;
    double midX = pts[mid].x;
    double d = min(closestPair(pts, l, mid), closestPair(pts, mid+1, r));
    vector<Point> strip;
    for (int i = l; i <= r; i++)
        if (abs(pts[i].x - midX) < d) strip.push_back(pts[i]);
    sort(strip.begin(), strip.end(), [](auto& a, auto& b) { return a.y < b.y; });
    for (int i = 0; i < (int)strip.size(); i++)
        for (int j = i+1; j < (int)strip.size() && strip[j].y - strip[i].y < d; j++)
            d = min(d, dist(strip[i], strip[j]));
    return d;
}

int main() {
    vector<Point> pts = {{0,0},{1,1},{2,2},{3,1},{0,3},{2,4}};
    auto hull = convexHull(pts);
    cout << "Convex Hull: ";
    for (auto& p : hull) cout << "(" << p.x << "," << p.y << ") ";
    cout << endl;

    vector<Point> pts2 = {{2,3},{12,30},{40,50},{5,1},{12,10},{3,4}};
    sort(pts2.begin(), pts2.end(), [](auto& a, auto& b) { return a.x < b.x; });
    printf("Closest pair: %.4f\n", closestPair(pts2, 0, pts2.size()-1));
}
