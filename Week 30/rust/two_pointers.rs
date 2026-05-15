// WEEK 30 - RUST ADVANCED TOPICS
// Topic: Two Pointers Pattern
// File: two_pointers.rs
//
// CONCEPT:
//   Two indices traverse an array (often sorted) under monotonic rules.
//   Total movement <= 2n -> O(n) or O(n log n) overall.
//
// KEY POINTS:
//   - On sorted input, the sum a[l]+a[r] is monotone in (l,r).
//   - For container/area problems, always shrink the smaller side.
//
// ALGORITHM / APPROACH:
//   TWO SUM SORTED: l=0,r=n-1; shift by sign of s vs target.
//   3SUM:           sort + iterate i + two-pointer inside.
//   MAX AREA:       shrink lower wall.
//   REMOVE DUPS:    write/read pointer in sorted array.
//
// RUST-SPECIFIC NOTES:
//   - Vec<i32> + sort_unstable.
//   - Returns (i32, i32) for two-sum to avoid Option<(usize,usize)>.
//
// DRY RUN / EXAMPLE:
//   two_sum_sorted [2,7,11,15], 9 -> (1,2).
//   three_sum [-1,0,1,2,-1,-4] -> [[-1,-1,2],[-1,0,1]].
//   max_area [1,8,6,2,5,4,8,3,7] -> 49.
//
// COMPLEXITY:
//   Two-sum O(n); 3Sum O(n^2); Max area O(n).

pub fn two_sum_sorted(nums: &[i32], target: i32) -> (i32, i32) {
    let (mut l, mut r) = (0usize, nums.len() - 1);
    while l < r {
        let s = nums[l] + nums[r];
        if s == target { return ((l + 1) as i32, (r + 1) as i32); }
        if s < target { l += 1; } else { r -= 1; }
    }
    (-1, -1)
}

pub fn three_sum(mut nums: Vec<i32>) -> Vec<Vec<i32>> {
    nums.sort_unstable();
    let n = nums.len();
    let mut out: Vec<Vec<i32>> = Vec::new();
    for i in 0..n.saturating_sub(2) {
        if i > 0 && nums[i] == nums[i - 1] { continue; }
        let (mut l, mut r) = (i + 1, n - 1);
        while l < r {
            let s = nums[i] + nums[l] + nums[r];
            if s == 0 {
                out.push(vec![nums[i], nums[l], nums[r]]);
                while l < r && nums[l] == nums[l + 1] { l += 1; }
                while l < r && nums[r] == nums[r - 1] { r -= 1; }
                l += 1; r -= 1;
            } else if s < 0 { l += 1; } else { r -= 1; }
        }
    }
    out
}

pub fn max_area(h: &[i32]) -> i32 {
    let (mut l, mut r) = (0usize, h.len() - 1);
    let mut best = 0;
    while l < r {
        let area = ((r - l) as i32) * h[l].min(h[r]);
        if area > best { best = area; }
        if h[l] < h[r] { l += 1; } else { r -= 1; }
    }
    best
}

pub fn remove_duplicates_sorted(nums: &mut Vec<i32>) -> usize {
    if nums.is_empty() { return 0; }
    let mut w = 1usize;
    for r in 1..nums.len() {
        if nums[r] != nums[w - 1] {
            nums[w] = nums[r];
            w += 1;
        }
    }
    w
}

fn main() {
    let arr = vec![2, 7, 11, 15];
    println!("Two Sum II [2,7,11,15] t=9: {:?}", two_sum_sorted(&arr, 9));

    println!("3Sum: {:?}", three_sum(vec![-1, 0, 1, 2, -1, -4]));

    println!("Max area: {}", max_area(&[1,8,6,2,5,4,8,3,7]));

    let mut v = vec![0,0,1,1,1,2,2,3,3,4];
    let n = remove_duplicates_sorted(&mut v);
    println!("Remove dup: len={} prefix={:?}", n, &v[..n]);
}

// NOTES
// -----
// Differences from Java:
//   * sort_unstable is in-place and faster; Java's Arrays.sort guarantees
//     stable ordering on objects but uses TimSort.
//   * remove_duplicates_sorted (LC 26) added on top of Java's set.
