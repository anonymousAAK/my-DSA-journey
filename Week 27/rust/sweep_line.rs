// WEEK 27 - RUST ADVANCED TOPICS
// Topic: Sweep Line - Skyline & Max Overlap
// File: sweep_line.rs
//
// CONCEPT:
//   Sweep an imaginary vertical line across the plane, processing events in
//   x order while maintaining an active set. Two classics:
//     - Skyline: max-heap of building heights gives the silhouette.
//     - Max overlap: counting +1/-1 events finds the simultaneous maximum.
//
// KEY POINTS:
//   - Sort events lexicographically (x then tie-breaker).
//   - For skyline: BinaryHeap of (height, end_x); lazy pop expired tops.
//
// ALGORITHM / APPROACH:
//   skyline: events for (l, r, h) -> (l, h, r) start, (r, 0, 0) end.
//            sort; max-heap on h; emit (x, h_max) whenever h_max changes.
//   overlap: +1 on start, -1 on end; sort with +1 before -1 at same x.
//
// RUST-SPECIFIC NOTES:
//   - std::collections::BinaryHeap is a max-heap by default.
//   - Use std::cmp::Reverse for min-heap behaviour if needed.
//   - Use i32 throughout; convert at boundaries.
//
// DRY RUN / EXAMPLE:
//   buildings = [(2,9,10),(3,7,15),(5,12,12),(15,20,10),(19,24,8)]
//   skyline   = [(2,10),(3,15),(7,12),(12,0),(15,10),(20,8),(24,0)]
//
// COMPLEXITY:
//   Time O(n log n)   Space O(n)

use std::collections::BinaryHeap;

pub fn skyline(buildings: &[(i32, i32, i32)]) -> Vec<(i32, i32)> {
    let mut events: Vec<(i32, i32, i32)> = Vec::new();
    for &(l, r, h) in buildings {
        events.push((l, h, r));    // start
        events.push((r, 0, 0));    // end
    }
    events.sort_by(|a, b| {
        if a.0 != b.0 { a.0.cmp(&b.0) } else { b.1.cmp(&a.1) }  // taller starts first
    });
    let mut heap: BinaryHeap<(i32, i32)> = BinaryHeap::new();
    heap.push((0, i32::MAX));
    let mut result = Vec::new();
    for (x, h, r) in events {
        if h != 0 { heap.push((h, r)); }
        while let Some(&(_, end)) = heap.peek() {
            if end <= x { heap.pop(); } else { break; }
        }
        let cur_h = heap.peek().unwrap().0;
        match result.last() {
            Some(&(_, prev)) if prev == cur_h => {}
            _ => result.push((x, cur_h)),
        }
    }
    result
}

pub fn max_overlap(intervals: &[(i32, i32)]) -> i32 {
    let mut events: Vec<(i32, i32)> = Vec::new();
    for &(s, e) in intervals {
        events.push((s, 1));
        events.push((e, -1));
    }
    events.sort_by(|a, b| {
        if a.0 != b.0 { a.0.cmp(&b.0) } else { b.1.cmp(&a.1) }  // +1 before -1
    });
    let (mut cur, mut best) = (0, 0);
    for (_, d) in events {
        cur += d;
        if cur > best { best = cur; }
    }
    best
}

fn main() {
    let sk = skyline(&[(2,9,10),(3,7,15),(5,12,12),(15,20,10),(19,24,8)]);
    print!("Skyline:");
    for (x, h) in &sk { print!(" ({},{})", x, h); }
    println!();
    println!("Max overlap: {}", max_overlap(&[(1,5),(2,6),(3,4),(7,8)]));
}

// NOTES
// -----
// Differences from Java:
//   * Java's geometry.java does not include sweep-line algorithms; we add
//     skyline and overlap classics here.
//   * BinaryHeap is max-heap by default — convenient for the skyline.
//   * Tuple ordering / sort_by with closures keeps the comparator concise.
