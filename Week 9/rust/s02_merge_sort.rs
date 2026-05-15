/*
 * WEEK 9 - RUST DSA
 * Topic: Merge Sort
 * File: 2.merge_sort.rs
 *
 * CONCEPT:
 *     Recursive divide-and-conquer: split, sort halves, merge.
 *
 * KEY POINTS:
 *     - Stable; O(n log n) all cases; O(n) auxiliary space.
 *     - Inversion count adapts the merging step at no extra asymptotic cost.
 *
 * ALGORITHM / APPROACH:
 *     merge_sort(arr, lo, hi):
 *         if lo >= hi: return
 *         mid = (lo + hi) / 2
 *         merge_sort(arr, lo, mid)
 *         merge_sort(arr, mid + 1, hi)
 *         merge(arr, lo, mid, hi)
 *
 * RUST-SPECIFIC NOTES:
 *     - Vec<i32> + indexes for ergonomic recursive calls.
 *     - We allocate the L/R buffers once per merge; reusing buffers is
 *       an optimisation left as an exercise.
 *
 * DRY RUN:
 *     [38,27,43,3,9,82,10] -> [3,9,10,27,38,43,82]
 *     Inversions of [2,4,1,3,5] = 3.
 *
 * COMPLEXITY:
 *     Time: O(n log n)  Space: O(n)  Stable.
 */

fn merge(arr: &mut Vec<i32>, left: usize, mid: usize, right: usize) {
    let l_slice: Vec<i32> = arr[left..=mid].to_vec();
    let r_slice: Vec<i32> = arr[mid + 1..=right].to_vec();
    let mut i = 0usize;
    let mut j = 0usize;
    let mut k = left;
    while i < l_slice.len() && j < r_slice.len() {
        if l_slice[i] <= r_slice[j] {
            arr[k] = l_slice[i];
            i += 1;
        } else {
            arr[k] = r_slice[j];
            j += 1;
        }
        k += 1;
    }
    while i < l_slice.len() {
        arr[k] = l_slice[i];
        i += 1;
        k += 1;
    }
    while j < r_slice.len() {
        arr[k] = r_slice[j];
        j += 1;
        k += 1;
    }
}

fn merge_sort_range(arr: &mut Vec<i32>, left: usize, right: usize) {
    if left >= right {
        return;
    }
    let mid = left + (right - left) / 2;
    merge_sort_range(arr, left, mid);
    merge_sort_range(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

fn merge_sort(arr: &mut Vec<i32>) {
    if arr.is_empty() {
        return;
    }
    let n = arr.len();
    merge_sort_range(arr, 0, n - 1);
}

// --- BONUS: inversion count ---
fn merge_count(arr: &mut Vec<i32>, left: usize, mid: usize, right: usize) -> u64 {
    let l_slice: Vec<i32> = arr[left..=mid].to_vec();
    let r_slice: Vec<i32> = arr[mid + 1..=right].to_vec();
    let mut inv: u64 = 0;
    let mut i = 0usize;
    let mut j = 0usize;
    let mut k = left;
    while i < l_slice.len() && j < r_slice.len() {
        if l_slice[i] <= r_slice[j] {
            arr[k] = l_slice[i];
            i += 1;
        } else {
            inv += (l_slice.len() - i) as u64;
            arr[k] = r_slice[j];
            j += 1;
        }
        k += 1;
    }
    while i < l_slice.len() {
        arr[k] = l_slice[i];
        i += 1;
        k += 1;
    }
    while j < r_slice.len() {
        arr[k] = r_slice[j];
        j += 1;
        k += 1;
    }
    inv
}

fn merge_sort_count_range(arr: &mut Vec<i32>, left: usize, right: usize) -> u64 {
    if left >= right {
        return 0;
    }
    let mid = left + (right - left) / 2;
    let mut inv = merge_sort_count_range(arr, left, mid);
    inv += merge_sort_count_range(arr, mid + 1, right);
    inv += merge_count(arr, left, mid, right);
    inv
}

fn count_inversions(arr: &[i32]) -> u64 {
    if arr.is_empty() {
        return 0;
    }
    let mut copy = arr.to_vec();
    let n = copy.len();
    merge_sort_count_range(&mut copy, 0, n - 1)
}

fn main() {
    let mut arr = vec![38, 27, 43, 3, 9, 82, 10];
    println!("Before: {:?}", arr);
    merge_sort(&mut arr);
    println!("After:  {:?}", arr);

    let mut single = vec![5];
    merge_sort(&mut single);
    println!("\nSingle: {:?}", single);

    let mut already = vec![1, 2, 3, 4, 5];
    merge_sort(&mut already);
    println!("Already sorted: {:?}", already);

    let mut reverse = vec![5, 4, 3, 2, 1];
    merge_sort(&mut reverse);
    println!("Reverse sorted: {:?}", reverse);

    println!("\n=== Count Inversions ===");
    for t in [vec![2, 4, 1, 3, 5], vec![5, 3, 1, 4, 2], vec![1, 2, 3]] {
        println!("{:?} -> inversions: {}", t, count_inversions(&t));
    }
}

/*
 * NOTES — Rust vs Java:
 *     - Slice copies (`arr[a..=b].to_vec()`) replace Arrays.copyOfRange.
 *     - Use Vec::sort for the production-grade stable sort (TimSort-derived).
 *     - We return the inversion count as a value rather than tracking a
 *       global; Rust strongly discourages mutable globals.
 */
