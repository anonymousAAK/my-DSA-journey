//! # Week 19: Greedy Algorithms
//!
//! Greedy algorithms make the locally optimal choice at each step, hoping to
//! find a global optimum. They work when the problem has:
//! - **Greedy choice property**: A global optimum can be reached by choosing
//!   the locally optimal option.
//! - **Optimal substructure**: An optimal solution contains optimal solutions
//!   to subproblems.
//!
//! ## Complexity Summary
//! | Algorithm            | Time          | Space |
//! |---------------------|---------------|-------|
//! | Activity Selection  | O(n log n)    | O(n)  |
//! | Fractional Knapsack | O(n log n)    | O(n)  |
//! | Merge Intervals     | O(n log n)    | O(n)  |
//! | Min Meeting Rooms   | O(n log n)    | O(n)  |

use std::collections::BinaryHeap;
use std::cmp::Reverse;

// =============================================================================
// Activity Selection
// =============================================================================

/// Selects the maximum number of non-overlapping activities.
///
/// # Algorithm
/// 1. Sort activities by their finish time.
/// 2. Greedily pick the activity that finishes earliest and doesn't overlap
///    with the last selected activity.
///
/// # Why Greedy Works
/// By always picking the earliest-finishing activity, we leave as much room
/// as possible for subsequent activities. This is provably optimal.
///
/// # Complexity
/// - Time: O(n log n) for sorting
/// - Space: O(n) for the sorted copy and result
///
/// # Parameters
/// - `activities`: slice of (start, finish) tuples
///
/// # Returns
/// Indices of selected activities in the original array.
fn activity_selection(activities: &[(i32, i32)]) -> Vec<usize> {
    if activities.is_empty() {
        return Vec::new();
    }

    // Create indices sorted by finish time
    let mut indices: Vec<usize> = (0..activities.len()).collect();
    indices.sort_unstable_by_key(|&i| activities[i].1);

    let mut selected = vec![indices[0]];
    let mut last_finish = activities[indices[0]].1;

    for &i in &indices[1..] {
        if activities[i].0 >= last_finish {
            selected.push(i);
            last_finish = activities[i].1;
        }
    }

    selected
}

// =============================================================================
// Fractional Knapsack
// =============================================================================

/// Solves the fractional knapsack problem where items can be partially taken.
///
/// # Algorithm
/// 1. Compute value-to-weight ratio for each item.
/// 2. Sort items by ratio in descending order.
/// 3. Greedily take as much of the highest-ratio item as possible.
///
/// # Difference from 0/1 Knapsack
/// Unlike 0/1 knapsack (which requires DP), fractional knapsack has the
/// greedy choice property because we can take fractions of items.
///
/// # Complexity
/// - Time: O(n log n) for sorting
/// - Space: O(n)
///
/// # Parameters
/// - `items`: slice of (weight, value) tuples
/// - `capacity`: maximum weight the knapsack can hold
fn fractional_knapsack(items: &[(f64, f64)], capacity: f64) -> f64 {
    // Create indices sorted by value/weight ratio (descending)
    let mut indices: Vec<usize> = (0..items.len()).collect();
    indices.sort_unstable_by(|&a, &b| {
        let ratio_a = items[a].1 / items[a].0;
        let ratio_b = items[b].1 / items[b].0;
        ratio_b.partial_cmp(&ratio_a).unwrap()
    });

    let mut remaining = capacity;
    let mut total_value = 0.0;

    for &i in &indices {
        let (weight, value) = items[i];
        if remaining <= 0.0 {
            break;
        }

        if weight <= remaining {
            // Take the entire item
            total_value += value;
            remaining -= weight;
        } else {
            // Take a fraction of the item
            let fraction = remaining / weight;
            total_value += value * fraction;
            remaining = 0.0;
        }
    }

    total_value
}

// =============================================================================
// Merge Intervals
// =============================================================================

/// Merges overlapping intervals.
///
/// # Algorithm
/// 1. Sort intervals by start time.
/// 2. Iterate through sorted intervals. If the current interval overlaps
///    with the last merged interval, extend the end. Otherwise, start a new
///    merged interval.
///
/// # Complexity
/// - Time: O(n log n) for sorting
/// - Space: O(n) for the result
///
/// # Ownership Note
/// Takes `&[(i32, i32)]` and returns a new `Vec` — we don't modify the input.
fn merge_intervals(intervals: &[(i32, i32)]) -> Vec<(i32, i32)> {
    if intervals.is_empty() {
        return Vec::new();
    }

    // Sort by start time
    let mut sorted: Vec<(i32, i32)> = intervals.to_vec();
    sorted.sort_unstable_by_key(|&(start, _)| start);

    let mut merged: Vec<(i32, i32)> = vec![sorted[0]];

    for &(start, end) in &sorted[1..] {
        let last = merged.last_mut().unwrap();
        if start <= last.1 {
            // Overlapping — extend the end if necessary
            last.1 = last.1.max(end);
        } else {
            // Non-overlapping — start a new interval
            merged.push((start, end));
        }
    }

    merged
}

// =============================================================================
// Minimum Meeting Rooms — Using BinaryHeap
// =============================================================================

/// Determines the minimum number of meeting rooms required to accommodate
/// all meetings.
///
/// # Algorithm
/// 1. Sort meetings by start time.
/// 2. Use a min-heap to track the end times of ongoing meetings.
/// 3. For each meeting, if it starts after the earliest-ending meeting,
///    that room can be reused (pop the heap). Push the new meeting's end time.
/// 4. The heap size at the end is the answer.
///
/// # Complexity
/// - Time: O(n log n) — sorting + n heap operations each O(log n)
/// - Space: O(n) — at most n meetings in the heap
///
/// # Rust Note
/// `BinaryHeap` is a max-heap. We use `Reverse` to create a min-heap
/// ordered by end time, so `heap.peek()` gives the earliest ending meeting.
fn min_meeting_rooms(meetings: &[(i32, i32)]) -> usize {
    if meetings.is_empty() {
        return 0;
    }

    // Sort by start time
    let mut sorted: Vec<(i32, i32)> = meetings.to_vec();
    sorted.sort_unstable_by_key(|&(start, _)| start);

    // Min-heap of end times (using Reverse for min-heap behavior)
    let mut heap: BinaryHeap<Reverse<i32>> = BinaryHeap::new();

    for &(start, end) in &sorted {
        // If the earliest-ending meeting has finished, reuse that room
        if let Some(&Reverse(earliest_end)) = heap.peek() {
            if start >= earliest_end {
                heap.pop();
            }
        }
        heap.push(Reverse(end));
    }

    heap.len()
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 19: Greedy Algorithms ===\n");

    // --- Activity Selection ---
    println!("--- Activity Selection ---");
    let activities = vec![(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)];
    let selected = activity_selection(&activities);
    println!("Activities: {:?}", activities);
    println!("Selected indices: {:?}", selected);
    let selected_activities: Vec<(i32, i32)> = selected.iter().map(|&i| activities[i]).collect();
    println!("Selected activities: {:?}", selected_activities);
    // Verify non-overlapping
    for i in 1..selected.len() {
        assert!(activities[selected[i]].0 >= activities[selected[i - 1]].1);
    }
    assert_eq!(selected.len(), 4); // Optimal: 4 activities
    println!("PASS\n");

    // --- Fractional Knapsack ---
    println!("--- Fractional Knapsack ---");
    let items = vec![(10.0, 60.0), (20.0, 100.0), (30.0, 120.0)];
    let capacity = 50.0;
    let max_value = fractional_knapsack(&items, capacity);
    println!("Items (weight, value): {:?}", items);
    println!("Capacity: {}, Max value: {:.2}", capacity, max_value);
    assert!((max_value - 240.0).abs() < 1e-6); // 60 + 100 + 80 (2/3 of last)
    println!("PASS\n");

    // --- Merge Intervals ---
    println!("--- Merge Intervals ---");
    let intervals = vec![(1, 3), (2, 6), (8, 10), (15, 18)];
    let merged = merge_intervals(&intervals);
    println!("Input:  {:?}", intervals);
    println!("Merged: {:?}", merged);
    assert_eq!(merged, vec![(1, 6), (8, 10), (15, 18)]);

    let intervals2 = vec![(1, 4), (4, 5)];
    let merged2 = merge_intervals(&intervals2);
    println!("Input:  {:?}", intervals2);
    println!("Merged: {:?}", merged2);
    assert_eq!(merged2, vec![(1, 5)]); // Touching intervals merge

    let intervals3 = vec![(1, 4), (0, 4)];
    let merged3 = merge_intervals(&intervals3);
    assert_eq!(merged3, vec![(0, 4)]);
    println!("PASS\n");

    // --- Min Meeting Rooms ---
    println!("--- Min Meeting Rooms ---");
    let meetings = vec![(0, 30), (5, 10), (15, 20)];
    let rooms = min_meeting_rooms(&meetings);
    println!("Meetings: {:?}", meetings);
    println!("Min rooms needed: {}", rooms);
    assert_eq!(rooms, 2);

    let meetings2 = vec![(7, 10), (2, 4)];
    let rooms2 = min_meeting_rooms(&meetings2);
    assert_eq!(rooms2, 1); // No overlap

    let meetings3 = vec![(1, 5), (2, 6), (3, 7), (4, 8)];
    let rooms3 = min_meeting_rooms(&meetings3);
    assert_eq!(rooms3, 4); // All overlap with each other
    println!("PASS\n");

    println!("All Week 19 tests passed!");
}
