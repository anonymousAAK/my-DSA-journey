/*
 * WEEK 19 - RUST DSA
 * Topic: Greedy Algorithms — Paradigm + Classic Problems
 * File: 1.GreedyAlgorithms.rs
 *
 * CONCEPT:
 *     Greedy algorithms commit to the locally optimal choice at each step.
 *     They work when the problem has greedy-choice property + optimal
 *     substructure. Typically O(n log n) due to a sort.
 *
 * KEY POINTS:
 *     - Sort + scan is the dominant pattern.
 *     - std::collections::BinaryHeap is a MAX-heap; wrap with Reverse for min-heap.
 *     - Use Vec::sort_by(|a,b| a.cmp(b)) or sort_by_key for ergonomic sorting.
 *     - Float comparators need partial_cmp + .unwrap() (NaN handling).
 *
 * ALGORITHM / APPROACH:
 *     Five canonical problems:
 *         1. Activity Selection         (sort by end time)
 *         2. Fractional Knapsack        (sort by value/weight desc)
 *         3. Min Coins (canonical)      (always take largest coin)
 *         4. Merge Intervals            (sort by start; merge overlaps)
 *         5. Min Meeting Rooms          (sort + min-heap of end times)
 *
 * RUST-SPECIFIC NOTES:
 *     - Use BinaryHeap<Reverse<i32>> for a min-heap. Reverse comes from
 *       std::cmp::Reverse.
 *     - Sorting indices: build (0..n).collect::<Vec<_>>() then sort_by_key.
 *     - Float compare: a.partial_cmp(&b).unwrap() (input must be finite).
 *     - Vec::iter().enumerate() is the idiomatic indexed loop.
 *
 * DRY RUN:
 *     Activity Selection
 *         start = [1,3,0,5,8,5]
 *         end   = [2,4,6,7,9,9]
 *         indices sorted by end: [0,1,3,2,4,5]
 *         pick 0 (1..2); 1 (3..4); 3 (5..7); skip 2 (0<7); pick 4 (8..9); skip 5.
 *         Answer = 4.
 *
 *     Min Meeting Rooms [[0,30],[5,10],[15,20]]
 *         heap=[Reverse(30)]; (5,10): 5<30 push 10; heap=[10,30].
 *         (15,20): 15>=10 pop; push 20; heap=[20,30]. size=2.
 *
 * COMPLEXITY:
 *     activity_selection      O(n log n)
 *     fractional_knapsack     O(n log n)
 *     min_coins_greedy        O(c log c)
 *     merge_intervals         O(n log n)
 *     min_meeting_rooms       O(n log n)
 */

use std::cmp::Reverse;
use std::collections::BinaryHeap;

// 1. ACTIVITY SELECTION
pub fn activity_selection(start: &[i32], end: &[i32]) -> i32 {
    let n = start.len();
    if n == 0 { return 0; }
    let mut idx: Vec<usize> = (0..n).collect();
    idx.sort_by_key(|&i| end[i]);
    let mut count = 1;
    let mut last_end = end[idx[0]];
    for &k in &idx[1..] {
        if start[k] >= last_end {
            count += 1;
            last_end = end[k];
        }
    }
    count
}

// 2. FRACTIONAL KNAPSACK
pub fn fractional_knapsack(weights: &[i32], values: &[i32], capacity: i32) -> f64 {
    let n = weights.len();
    let mut idx: Vec<usize> = (0..n).collect();
    idx.sort_by(|&a, &b| {
        let ra = values[b] as f64 / weights[b] as f64;
        let rb = values[a] as f64 / weights[a] as f64;
        ra.partial_cmp(&rb).unwrap()                    // descending density
    });
    let mut total = 0.0f64;
    let mut remaining = capacity;
    for i in idx {
        if remaining <= 0 { break; }
        let take = weights[i].min(remaining);
        total += take as f64 * values[i] as f64 / weights[i] as f64;
        remaining -= take;
    }
    total
}

// 3. MIN COINS (canonical systems)
pub fn min_coins_greedy(mut coins: Vec<i32>, mut target: i32) -> Vec<(i32, i32)> {
    coins.sort_by(|a, b| b.cmp(a));                     // descending
    let mut result = Vec::new();
    for c in coins {
        if target <= 0 { break; }
        if c <= target {
            let count = target / c;
            result.push((c, count));
            target -= c * count;
        }
    }
    result
}

// 4. MERGE INTERVALS
pub fn merge_intervals(mut intervals: Vec<(i32, i32)>) -> Vec<(i32, i32)> {
    if intervals.len() <= 1 { return intervals; }
    intervals.sort_by_key(|iv| iv.0);
    let mut merged: Vec<(i32, i32)> = Vec::with_capacity(intervals.len());
    merged.push(intervals[0]);
    for iv in intervals.into_iter().skip(1) {
        let last = merged.last_mut().unwrap();
        if iv.0 <= last.1 {
            last.1 = last.1.max(iv.1);
        } else {
            merged.push(iv);
        }
    }
    merged
}

// 5. MIN MEETING ROOMS
pub fn min_meeting_rooms(mut intervals: Vec<(i32, i32)>) -> i32 {
    if intervals.is_empty() { return 0; }
    intervals.sort_by_key(|iv| iv.0);
    let mut ends: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    ends.push(Reverse(intervals[0].1));
    for iv in intervals.into_iter().skip(1) {
        if let Some(&Reverse(top)) = ends.peek() {
            if iv.0 >= top {
                ends.pop();
            }
        }
        ends.push(Reverse(iv.1));
    }
    ends.len() as i32
}

fn main() {
    println!("=== Activity Selection ===");
    let start = [1, 3, 0, 5, 8, 5];
    let end   = [2, 4, 6, 7, 9, 9];
    println!("Max activities: {}", activity_selection(&start, &end));         // 4

    println!("\n=== Fractional Knapsack ===");
    println!("Max value: {:.2}",
             fractional_knapsack(&[10, 20, 30], &[60, 100, 120], 50));        // 240.00

    println!("\n=== Min Coins (US denominations) ===");
    let usd = vec![1, 5, 10, 25, 50, 100];
    println!("Change for 87: {:?}", min_coins_greedy(usd.clone(), 87));
    println!("Change for 30: {:?}", min_coins_greedy(usd.clone(), 30));

    println!("\n=== Merge Intervals ===");
    let merged = merge_intervals(vec![(1,3),(2,6),(8,10),(15,18)]);
    println!("Merged: {:?}", merged);

    println!("\n=== Min Meeting Rooms ===");
    println!("Rooms needed: {}", min_meeting_rooms(vec![(0,30),(5,10),(15,20)])); // 2
    println!("Rooms needed: {}", min_meeting_rooms(vec![(7,10),(2,4)]));          // 1
}

/*
 * NOTES (Rust vs Java):
 *   - BinaryHeap is max-heap by default; wrap with Reverse(x) for a min-heap
 *     of x.  Java has both PriorityQueue (min-heap) and reverse-order constructor.
 *   - Float sort: f64 doesn't implement Ord (NaN), so we use partial_cmp.unwrap().
 *     Java's Double.compare handles NaN with a specific ordering.
 *   - sort_by_key takes a closure returning a Key: Ord. For descending order,
 *     either negate or use sort_by with a flipped cmp.
 *   - Tuples (i32,i32) replace Java's int[2]; field access via .0, .1.
 *   - intervals.into_iter() consumes the Vec — efficient because we don't
 *     need the original any more.
 */
