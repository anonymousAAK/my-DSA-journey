// WEEK 27 - RUST ADVANCED TOPICS
// Topic: Convex Hull (Andrew's Monotone Chain)
// File: convex_hull.rs
//
// CONCEPT:
//   Smallest convex polygon containing all input points. Andrew's monotone
//   chain sorts points lexicographically and builds the lower then upper
//   hull using a cross-product orientation test on the running stack.
//
// KEY POINTS:
//   - Cross product (a-o)x(b-o) > 0 -> CCW turn.
//   - Pop while last triple is non-CCW (<=0) for a strict CCW hull.
//   - O(n log n).
//
// ALGORITHM / APPROACH:
//   sort points
//   walk forward (lower hull), then backward (upper hull)
//   concatenate dropping the duplicated endpoints
//
// RUST-SPECIFIC NOTES:
//   - Use struct Point { x: i64, y: i64 } with Ord/Eq derived for sorting.
//   - i64 cross product avoids overflow for typical contest constraints.
//   - dedup_by uses PartialEq.
//
// DRY RUN / EXAMPLE:
//   pts = [(0,0),(1,1),(2,2),(3,1),(0,3),(2,4)] -> hull
//   [(0,0),(3,1),(2,4),(0,3)].
//
// COMPLEXITY:
//   Time O(n log n)   Space O(n)

#[derive(Copy, Clone, Eq, PartialEq, Debug)]
pub struct Point { pub x: i64, pub y: i64 }

impl Ord for Point {
    fn cmp(&self, o: &Self) -> std::cmp::Ordering {
        self.x.cmp(&o.x).then(self.y.cmp(&o.y))
    }
}
impl PartialOrd for Point {
    fn partial_cmp(&self, o: &Self) -> Option<std::cmp::Ordering> { Some(self.cmp(o)) }
}

fn cross(o: Point, a: Point, b: Point) -> i64 {
    (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)
}

pub fn convex_hull(mut pts: Vec<Point>) -> Vec<Point> {
    pts.sort();
    pts.dedup();
    let n = pts.len();
    if n < 2 { return pts; }
    let mut hull: Vec<Point> = Vec::new();
    // lower hull
    for &p in &pts {
        while hull.len() >= 2 && cross(hull[hull.len()-2], hull[hull.len()-1], p) <= 0 {
            hull.pop();
        }
        hull.push(p);
    }
    let lower = hull.len() + 1;
    // upper hull
    for i in (0..n - 1).rev() {
        let p = pts[i];
        while hull.len() >= lower && cross(hull[hull.len()-2], hull[hull.len()-1], p) <= 0 {
            hull.pop();
        }
        hull.push(p);
    }
    hull.pop();
    hull
}

fn main() {
    let pts = vec![
        Point{x:0,y:0}, Point{x:1,y:1}, Point{x:2,y:2},
        Point{x:3,y:1}, Point{x:0,y:3}, Point{x:2,y:4},
    ];
    let hull = convex_hull(pts);
    print!("Convex hull:");
    for p in &hull { print!(" ({},{})", p.x, p.y); }
    println!();
}

// NOTES
// -----
// Differences from Java:
//   * Rust struct Point with derived Ord/Eq replaces int[] arrays.
//   * dedup() uses PartialEq to drop duplicate points after sort.
//   * i64 arithmetic avoids overflow in cross product for moderate inputs.
