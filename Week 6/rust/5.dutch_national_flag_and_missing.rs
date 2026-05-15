/*
 * WEEK 6 - RUST DSA
 * Topic: Dutch National Flag + Missing / Duplicate
 * File: 5.dutch_national_flag_and_missing.rs
 *
 * CONCEPT:
 *     A) Dutch National Flag — three-way partition over {0,1,2}.
 *     B) Missing number — sum formula and XOR variants.
 *     C) Find duplicate — Floyd's cycle detection on indices.
 *
 * KEY POINTS:
 *     - Dutch flag is single-pass, in-place, O(n) / O(1).
 *     - XOR variant avoids overflow; sum variant is simpler to read.
 *     - Floyd's algorithm needs no extra memory and never mutates input.
 *
 * ALGORITHM / APPROACH:
 *     Dutch flag:
 *         low = mid = 0; high = n - 1
 *         while mid <= high:
 *             match arr[mid] {
 *                 0 => { swap(low, mid); low++; mid++; }
 *                 1 => { mid++; }
 *                 _ => { swap(mid, high); high--; }
 *             }
 *     Missing (sum): n*(n+1)/2 - sum(arr)
 *     Missing (XOR): xor of [0..n] xor of all arr values
 *     Duplicate    : Floyd two-phase
 *
 * RUST-SPECIFIC NOTES:
 *     - Use isize/i64 for the high pointer to avoid usize underflow
 *       (high may be -1 when arr is empty); we guard explicitly.
 *     - .swap(i, j) is a slice method; no temporary needed.
 *     - Use i64 for the sum to avoid overflow on huge n.
 *
 * DRY RUN:
 *     Dutch on [2,0,2,1,1,0]:
 *         (low, mid, high) = (0, 0, 5)
 *         arr[0]=2 swap(0,5) -> [0,0,2,1,1,2] high=4
 *         arr[0]=0 swap(0,0) -> low=1 mid=1
 *         arr[1]=0 swap(1,1) -> low=2 mid=2
 *         arr[2]=2 swap(2,4) -> [0,0,1,1,2,2] high=3
 *         arr[2]=1 mid=3
 *         arr[3]=1 mid=4 stop
 *
 *     Missing on [3,0,1] -> 6 - 4 = 2.
 *     Duplicate on [1,3,4,2,2] -> 2.
 *
 * COMPLEXITY:
 *     All three: O(n) time, O(1) extra space.
 */

fn dutch_flag(arr: &mut [i32]) {
    if arr.is_empty() {
        return;
    }
    let mut low: usize = 0;
    let mut mid: usize = 0;
    let mut high: isize = arr.len() as isize - 1;
    while (mid as isize) <= high {
        match arr[mid] {
            0 => {
                arr.swap(low, mid);
                low += 1;
                mid += 1;
            }
            1 => {
                mid += 1;
            }
            _ => {
                // 2
                arr.swap(mid, high as usize);
                high -= 1;
            }
        }
    }
}

fn missing_number_sum(arr: &[i64]) -> i64 {
    let n = arr.len() as i64;
    let expected = n * (n + 1) / 2;
    let actual: i64 = arr.iter().sum();
    expected - actual
}

fn missing_number_xor(arr: &[i64]) -> i64 {
    let n = arr.len() as i64;
    let mut x: i64 = 0;
    for i in 0..=n {
        x ^= i;
    }
    for &v in arr {
        x ^= v;
    }
    x
}

fn find_duplicate(arr: &[usize]) -> usize {
    let mut slow = arr[0];
    let mut fast = arr[0];
    loop {
        slow = arr[slow];
        fast = arr[arr[fast]];
        if slow == fast {
            break;
        }
    }
    slow = arr[0];
    while slow != fast {
        slow = arr[slow];
        fast = arr[fast];
    }
    slow
}

fn main() {
    // Dutch flag
    let mut colors = vec![2, 0, 2, 1, 1, 0];
    println!("Before: {:?}", colors);
    dutch_flag(&mut colors);
    println!("After:  {:?}", colors);

    let mut colors2 = vec![2, 2, 2, 0, 0, 1];
    dutch_flag(&mut colors2);
    println!("Sorted: {:?}", colors2);

    // Missing
    let arr1: Vec<i64> = vec![3, 0, 1];
    println!("\narr = {:?}", arr1);
    println!("Missing (sum): {}", missing_number_sum(&arr1));
    println!("Missing (XOR): {}", missing_number_xor(&arr1));

    let arr2: Vec<i64> = vec![9, 6, 4, 2, 3, 5, 7, 0, 1];
    println!("\narr = {:?}", arr2);
    println!("Missing (sum): {}", missing_number_sum(&arr2));
    println!("Missing (XOR): {}", missing_number_xor(&arr2));

    // Duplicate
    let dup: Vec<usize> = vec![1, 3, 4, 2, 2];
    println!("\narr = {:?}", dup);
    println!("Duplicate: {}", find_duplicate(&dup));

    let dup2: Vec<usize> = vec![3, 1, 3, 4, 2];
    println!("arr = {:?}", dup2);
    println!("Duplicate: {}", find_duplicate(&dup2));
}

/*
 * NOTES — Rust vs Java:
 *     - usize is the indexing type; convert with `as` when arithmetic
 *       can go negative.
 *     - .swap(i, j) replaces the temp-variable swap idiom.
 *     - Pattern `match arr[mid]` is more readable than the if/else chain.
 *     - find_duplicate takes &[usize] because the values are array indices.
 */
