// WEEK 27 - RUST ADVANCED TOPICS
// Topic: Line Segment Intersection
// File: line_intersection.rs
//
// CONCEPT:
//   Two segments AB and CD intersect when they straddle each other in the
//   sense of cross-product orientation:
//     ccw(p,q,r) = sign((q-p) x (r-p)).
//   Proper crossing happens when ccw(A,B,C) != ccw(A,B,D) AND
//   ccw(C,D,A) != ccw(C,D,B). Special cases handle collinear endpoints.
//
// KEY POINTS:
//   - O(1) per query.
//   - Returns intersection point of infinite lines via cross-ratio formula.
//
// ALGORITHM / APPROACH:
//   compute o1..o4
//   if proper straddling -> intersect
//   else handle four collinear endpoint-on-segment cases
//
// RUST-SPECIFIC NOTES:
//   - Use Point { x: f64, y: f64 } for the line-intersection API.
//   - Return Option<Point> for the line intersection point.
//
// DRY RUN / EXAMPLE:
//   AB=(0,0)-(4,4), CD=(0,4)-(4,0): proper crossing at (2,2).
//
// COMPLEXITY:
//   Time O(1)   Space O(1)

#[derive(Copy, Clone, Debug)]
pub struct Point { pub x: f64, pub y: f64 }

fn ccw(a: Point, b: Point, c: Point) -> i32 {
    let v = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
    if v > 0.0 { 1 } else if v < 0.0 { -1 } else { 0 }
}

fn on_segment(p: Point, q: Point, r: Point) -> bool {
    p.x.min(q.x) <= r.x && r.x <= p.x.max(q.x) &&
    p.y.min(q.y) <= r.y && r.y <= p.y.max(q.y)
}

pub fn segments_intersect(a: Point, b: Point, c: Point, d: Point) -> bool {
    let (o1, o2, o3, o4) = (ccw(a,b,c), ccw(a,b,d), ccw(c,d,a), ccw(c,d,b));
    if o1 != o2 && o3 != o4 { return true; }
    if o1 == 0 && on_segment(a, b, c) { return true; }
    if o2 == 0 && on_segment(a, b, d) { return true; }
    if o3 == 0 && on_segment(c, d, a) { return true; }
    if o4 == 0 && on_segment(c, d, b) { return true; }
    false
}

pub fn line_intersection(a: Point, b: Point, c: Point, d: Point) -> Option<Point> {
    let denom = (a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x);
    if denom == 0.0 { return None; }
    let t = ((a.x - c.x) * (c.y - d.y) - (a.y - c.y) * (c.x - d.x)) / denom;
    Some(Point { x: a.x + t * (b.x - a.x), y: a.y + t * (b.y - a.y) })
}

fn main() {
    let (a, b, c, d) = (Point{x:0.,y:0.}, Point{x:4.,y:4.}, Point{x:0.,y:4.}, Point{x:4.,y:0.});
    println!("Segments intersect: {}", segments_intersect(a, b, c, d));
    if let Some(p) = line_intersection(a, b, c, d) {
        println!("Point: ({}, {})", p.x, p.y);
    }
    let (e, f, g, h) = (Point{x:0.,y:0.}, Point{x:5.,y:0.}, Point{x:0.,y:1.}, Point{x:5.,y:1.});
    println!("Parallel intersect: {}", segments_intersect(e, f, g, h));
    println!("Lines parallel: {}", line_intersection(e, f, g, h).is_none());
}

// NOTES
// -----
// Differences from Java:
//   * Java's geometry.java has no segment-intersection routine; we add it.
//   * Option<Point> models "no intersection / parallel" cleanly.
//   * f64 arithmetic mirrors Java's double; for large integers consider
//     i128 cross product to avoid floating error.
