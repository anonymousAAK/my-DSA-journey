// WEEK 30 - RUST ADVANCED TOPICS
// Topic: Merge Intervals Pattern
// File: merge_intervals.rs
//
// CONCEPT:
//   Merge / insert intervals; count meeting rooms; check attendance. Sort
//   by start, then linear scan.
//
// KEY POINTS:
//   - Sort by start (and end for tie-breaks).
//   - Merge: extend last when overlap; else push new.
//   - Insert (sorted input): 3 passes (before/overlap/after).
//   - Meeting rooms: sorted starts/ends two-pointer.
//
// ALGORITHM / APPROACH:
//   See per-function doc.
//
// RUST-SPECIFIC NOTES:
//   - Vec<(i32,i32)> for intervals; sort_unstable_by_key on start.
//   - Returning Vec is fine; intervals borrowed immutably elsewhere.
//
// DRY RUN / EXAMPLE:
//   merge [(1,3),(2,6),(8,10),(15,18)] -> [(1,6),(8,10),(15,18)]
//   insert [(1,3),(6,9)] with (2,5) -> [(1,5),(6,9)]
//   meeting rooms [(0,30),(5,10),(15,20)] -> 2.
//
// COMPLEXITY:
//   Merge / Rooms: O(n log n).  Insert: O(n).

pub fn merge_intervals(mut intervals: Vec<(i32, i32)>) -> Vec<(i32, i32)> {
    if intervals.is_empty() { return Vec::new(); }
    intervals.sort_unstable_by_key(|iv| iv.0);
    let mut out: Vec<(i32, i32)> = vec![intervals[0]];
    for &(s, e) in intervals.iter().skip(1) {
        let last = out.last_mut().unwrap();
        if s <= last.1 { last.1 = last.1.max(e); }
        else { out.push((s, e)); }
    }
    out
}

pub fn insert_interval(intervals: &[(i32, i32)], mut new_iv: (i32, i32)) -> Vec<(i32, i32)> {
    let mut out = Vec::new();
    let n = intervals.len();
    let mut i = 0;
    while i < n && intervals[i].1 < new_iv.0 { out.push(intervals[i]); i += 1; }
    while i < n && intervals[i].0 <= new_iv.1 {
        new_iv.0 = new_iv.0.min(intervals[i].0);
        new_iv.1 = new_iv.1.max(intervals[i].1);
        i += 1;
    }
    out.push(new_iv);
    while i < n { out.push(intervals[i]); i += 1; }
    out
}

pub fn min_meeting_rooms(intervals: &[(i32, i32)]) -> usize {
    if intervals.is_empty() { return 0; }
    let mut starts: Vec<i32> = intervals.iter().map(|iv| iv.0).collect();
    let mut ends:   Vec<i32> = intervals.iter().map(|iv| iv.1).collect();
    starts.sort_unstable();
    ends.sort_unstable();
    let mut rooms = 0usize;
    let mut busiest = 0usize;
    let mut j = 0usize;
    for &s in &starts {
        if s < ends[j] { rooms += 1; busiest = busiest.max(rooms); }
        else { j += 1; }
    }
    busiest
}

pub fn can_attend_all(intervals: &mut Vec<(i32, i32)>) -> bool {
    intervals.sort_unstable();
    intervals.windows(2).all(|w| w[1].0 >= w[0].1)
}

fn main() {
    let m = merge_intervals(vec![(1,3),(2,6),(8,10),(15,18)]);
    println!("Merged: {:?}", m);

    let ins = insert_interval(&[(1,3),(6,9)], (2,5));
    println!("Inserted: {:?}", ins);

    println!("Min meeting rooms: {}", min_meeting_rooms(&[(0,30),(5,10),(15,20)]));
    let mut iv = vec![(0,30),(5,10),(15,20)];
    println!("Can attend all: {}", can_attend_all(&mut iv));
}

// NOTES
// -----
// Differences from Java:
//   * Vec<(i32,i32)> for intervals; tuple ordering is lexicographic by
//     default.
//   * Adds min_meeting_rooms (LC 253) and can_attend_all (LC 252) on top
//     of Java's set.
