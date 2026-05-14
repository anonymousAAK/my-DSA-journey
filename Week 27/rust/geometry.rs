// Week 27: Computational Geometry
// Convex Hull O(n log n), Closest Pair O(n log n)

#[derive(Clone, Copy, Debug, PartialEq)]
struct Point { x: f64, y: f64 }

fn cross(o: Point, a: Point, b: Point) -> f64 {
    (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)
}

fn dist(a: Point, b: Point) -> f64 {
    ((a.x-b.x).powi(2) + (a.y-b.y).powi(2)).sqrt()
}

// === Convex Hull (Andrew's Monotone Chain) ===
fn convex_hull(points: &mut Vec<Point>) -> Vec<Point> {
    points.sort_by(|a, b| a.x.partial_cmp(&b.x).unwrap().then(a.y.partial_cmp(&b.y).unwrap()));
    let n = points.len();
    if n < 2 { return points.clone(); }
    let mut hull = Vec::new();
    for &p in points.iter() {
        while hull.len() >= 2 && cross(hull[hull.len()-2], hull[hull.len()-1], p) <= 0.0 {
            hull.pop();
        }
        hull.push(p);
    }
    let lower = hull.len() + 1;
    for i in (0..n-1).rev() {
        while hull.len() >= lower && cross(hull[hull.len()-2], hull[hull.len()-1], points[i]) <= 0.0 {
            hull.pop();
        }
        hull.push(points[i]);
    }
    hull.pop();
    hull
}

// === Closest Pair ===
fn closest_pair(pts: &mut [Point]) -> f64 {
    let n = pts.len();
    if n <= 3 {
        let mut best = f64::MAX;
        for i in 0..n { for j in i+1..n { best = best.min(dist(pts[i], pts[j])); } }
        return best;
    }
    let mid = n / 2;
    let mid_x = pts[mid].x;
    let d1 = closest_pair(&mut pts[..mid]);
    let d2 = closest_pair(&mut pts[mid..]);
    let mut d = d1.min(d2);
    let mut strip: Vec<Point> = pts.iter().filter(|p| (p.x - mid_x).abs() < d).copied().collect();
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

fn main() {
    let mut points = vec![
        Point{x:0.0,y:0.0}, Point{x:1.0,y:1.0}, Point{x:2.0,y:2.0},
        Point{x:3.0,y:1.0}, Point{x:0.0,y:3.0}, Point{x:2.0,y:4.0},
    ];
    let hull = convex_hull(&mut points);
    println!("Convex Hull: {:?}", hull);

    let mut pts = vec![
        Point{x:2.0,y:3.0}, Point{x:12.0,y:30.0}, Point{x:40.0,y:50.0},
        Point{x:5.0,y:1.0}, Point{x:12.0,y:10.0}, Point{x:3.0,y:4.0},
    ];
    pts.sort_by(|a,b| a.x.partial_cmp(&b.x).unwrap());
    println!("Closest pair: {:.4}", closest_pair(&mut pts));
}
