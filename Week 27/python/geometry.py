# Week 27: Computational Geometry
# Convex Hull O(n log n), Line Intersection O(1), Closest Pair O(n log n)

def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

# === Convex Hull (Andrew's Monotone Chain) ===
# Time: O(n log n), Space: O(n)
def convex_hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

# === Line Segment Intersection ===
# Time: O(1) per check
def on_segment(p, q, r):
    return (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
            min(p[1], r[1]) <= q[1] <= max(p[1], r[1]))

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0: return 0
    return 1 if val > 0 else 2

def segments_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    if o1 != o2 and o3 != o4: return True
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True
    return False

# === Closest Pair of Points (Divide and Conquer) ===
# Time: O(n log n), Space: O(n)
import math

def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def closest_pair(points):
    pts = sorted(points)
    def solve(pts):
        n = len(pts)
        if n <= 3:
            best = float('inf')
            for i in range(n):
                for j in range(i+1, n):
                    best = min(best, dist(pts[i], pts[j]))
            return best
        mid = n // 2
        mid_x = pts[mid][0]
        d = min(solve(pts[:mid]), solve(pts[mid:]))
        strip = [p for p in pts if abs(p[0] - mid_x) < d]
        strip.sort(key=lambda p: p[1])
        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and strip[j][1] - strip[i][1] < d:
                d = min(d, dist(strip[i], strip[j]))
                j += 1
        return d
    return solve(pts)

if __name__ == "__main__":
    points = [(0,0), (1,1), (2,2), (3,1), (0,3), (2,4)]
    print(f"Convex Hull: {convex_hull(points)}")
    print(f"Segments intersect: {segments_intersect((1,1),(4,4),(1,4),(4,1))}")
    pts = [(2,3),(12,30),(40,50),(5,1),(12,10),(3,4)]
    print(f"Closest pair distance: {closest_pair(pts):.4f}")
