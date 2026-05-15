/*
 * WEEK 9 - RUST DSA
 * Topic: Bubble / Selection / Insertion Sort
 * File: 1.bubble_selection_insertion.rs
 *
 * CONCEPT:
 *     Three O(n^2) elementary sorts; differ in stability, swap counts,
 *     and best-case behaviour.
 *
 * KEY POINTS:
 *     Bubble:    O(n) best with early-stop; stable.
 *     Selection: O(n) swaps; not stable.
 *     Insertion: O(n) best on nearly-sorted; stable; used inside many
 *                hybrid sorts (introsort, TimSort).
 *
 * ALGORITHM / APPROACH:
 *     See per-function code; same as Java/Python.
 *
 * RUST-SPECIFIC NOTES:
 *     - &mut [i32] for in-place sorting.
 *     - .swap(i, j) on slices replaces the explicit temp-swap idiom.
 *     - Stable production sort: Vec::sort (TimSort-derived).
 *
 * DRY RUN:
 *     [64,25,12,22,11]:
 *         bubble pass1: [25,12,22,11,64]
 *         bubble pass2: [12,22,11,25,64]
 *         bubble pass3: [12,11,22,25,64]
 *         bubble pass4: [11,12,22,25,64] (no swaps, done)
 *
 * COMPLEXITY:
 *     Bubble    : O(n^2) avg/worst, O(n) best, O(1) space, stable
 *     Selection : O(n^2), O(1) space, not stable
 *     Insertion : O(n^2) avg/worst, O(n) best, O(1) space, stable
 */

fn bubble_sort(arr: &mut [i32]) {
    let n = arr.len();
    if n < 2 {
        return;
    }
    for i in 0..n - 1 {
        let mut swapped = false;
        for j in 0..n - 1 - i {
            if arr[j] > arr[j + 1] {
                arr.swap(j, j + 1);
                swapped = true;
            }
        }
        if !swapped {
            break;
        }
    }
}

fn selection_sort(arr: &mut [i32]) {
    let n = arr.len();
    if n < 2 {
        return;
    }
    for i in 0..n - 1 {
        let mut min_idx = i;
        for j in (i + 1)..n {
            if arr[j] < arr[min_idx] {
                min_idx = j;
            }
        }
        if min_idx != i {
            arr.swap(i, min_idx);
        }
    }
}

fn insertion_sort(arr: &mut [i32]) {
    let n = arr.len();
    for i in 1..n {
        let key = arr[i];
        let mut j: i64 = i as i64 - 1;
        while j >= 0 && arr[j as usize] > key {
            arr[(j + 1) as usize] = arr[j as usize];
            j -= 1;
        }
        arr[(j + 1) as usize] = key;
    }
}

fn count_inversions(arr: &[i32]) -> u64 {
    let mut count: u64 = 0;
    let n = arr.len();
    for i in 0..n {
        for j in (i + 1)..n {
            if arr[i] > arr[j] {
                count += 1;
            }
        }
    }
    count
}

fn main() {
    let base = vec![64, 25, 12, 22, 11];

    let mut arr1 = base.clone();
    println!("Bubble Sort:");
    println!("Before: {:?}", arr1);
    bubble_sort(&mut arr1);
    println!("After:  {:?}", arr1);

    let mut arr2 = base.clone();
    println!("\nSelection Sort:");
    println!("Before: {:?}", arr2);
    selection_sort(&mut arr2);
    println!("After:  {:?}", arr2);

    let mut arr3 = base.clone();
    println!("\nInsertion Sort:");
    println!("Before: {:?}", arr3);
    insertion_sort(&mut arr3);
    println!("After:  {:?}", arr3);

    let mut already = vec![1, 2, 3, 4, 5];
    println!("\nAlready sorted — bubble sort:");
    println!("Before: {:?}", already);
    bubble_sort(&mut already);
    println!("After:  {:?}", already);

    let inv = vec![5, 3, 1, 4, 2];
    println!("\nArray: {:?}", inv);
    println!("Inversions: {}", count_inversions(&inv));
}

/*
 * NOTES — Rust vs Java:
 *     - .swap(i, j) is a slice method — clean and panic-checked.
 *     - Use i64 for the insertion-sort inner counter to avoid usize
 *       underflow at j = -1.
 *     - Vec::sort uses a TimSort-derived stable sort; for a fast
 *       unstable production sort use Vec::sort_unstable.
 */
