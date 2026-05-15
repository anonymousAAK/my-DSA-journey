// WEEK 27 - RUST ADVANCED TOPICS
// Topic: Closest Pair of Points
// File: closest_pair.rs
//
// CONCEPT:
//   Smallest pairwise Euclidean distance among n points. Sort by x, recurse,
//   then combine using a strip of width 2d sorted by y; each strip point
//   compares against at most ~7 successors -> O(n log n).
//
// KEY POINTS:
//   - Base case <= 3 -> brute force.
//   - Combine step is O(strip size).
//   - Use f64::hypot for stable distance.
//
// ALGORITHM / APPROACH:
//   sort by x
//   solve(l, r):
//     if small -> brute force
//     d = min(left, right)
//     build strip; sort by y; scan adjacent pairs while dy < d
//
// RUST-SPECIFIC NOTES:
//   - Pure recursion; the borrow checker is happy because we pass the
//     immutable slice through.
//   - sort_by with closure returning Ordering for f64 (use partial_cmp +
//     unwrap_or for total ordering).
//
// DRY RUN / EXAMPLE:
//   pts = [(2,3),(12,30),(40,50),(5,1),(12,10),(3,4)] -> ~1.4142.
//
// COMPLEXITY:
//   Time O(n log n)   Space O(n)

#[derive(Copy, Clone, Debug)]
pub struct Point { pub x: f64, pub y: f64 }

fn dist(a: Point, b: Point) -> f64 {
    (a.x - b.x).hypot(a.y - b.y)
}

fn solve(pts: &[Point], l: usize, r: usize) -> f64 {
    if r - l < 3 {
        let mut best = f64::INFINITY;
        for i in l..=r {
            for j in (i + 1)..=r {
                best = best.min(dist(pts[i], pts[j]));
            }
        }
        return best;
    }
    let mid = (l + r) / 2;
    let mid_x = pts[mid].x;
    let d_left = solve(pts, l, mid);
    let d_right = solve(pts, mid + 1, r);
    let mut d = d_left.min(d_right);
    let mut strip: Vec<Point> = pts[l..=r].iter().copied()
        .filter(|p| (p.x - mid_x).abs() < d)
        .collect();
    strip.sort_by(|a, b| a.y.partial_cmp(&b.y).unwrap());
    for i in 0..strip.len() {
        let mut j = i + 1;
        while j < strip.len() && strip[j].y - strip[i].y < d {
            d = d.min(dist(strip[i], strip[j]));
            j += 1;
        }
    }
    d
}

pub fn closest_pair(mut pts: Vec<Point>) -> f64 {
    if pts.len() < 2 { return f64::INFINITY; }
    pts.sort_by(|a, b| a.x.partial_cmp(&b.x).unwrap());
    solve(&pts, 0, pts.len() - 1)
}

pub fn closest_pair_brute(pts: &[Point]) -> f64 {
    let mut best = f64::INFINITY;
    for i in 0..pts.len() {
        for j in (i + 1)..pts.len() {
            best = best.min(dist(pts[i], pts[j]));
        }
    }
    best
}

fn main() {
    let pts = vec![
        Point{x:2.0,y:3.0},  Point{x:12.0,y:30.0}, Point{x:40.0,y:50.0},
        Point{x:5.0,y:1.0},  Point{x:12.0,y:10.0}, Point{x:3.0,y:4.0},
    ];
    println!("Closest pair (D&C):       {:.4}", closest_pair(pts.clone()));
    println!("Closest pair (brute force): {:.4}", closest_pair_brute(&pts));
}

// NOTES
// -----
// Differences from Java:
//   * f64::hypot replaces Math.sqrt + Math.pow for stable distance.
//   * partial_cmp().unwrap() yields a total Ord on f64 — assumes no NaN.
//   * Brute-force baseline included for self-check.
