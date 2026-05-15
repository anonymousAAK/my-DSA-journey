/*
 * WEEK 9 - RUST DSA
 * Topic: Quick Sort
 * File: 3.quick_sort.rs
 *
 * CONCEPT:
 *     Pivot + partition + recurse. Both Lomuto and Hoare partition
 *     schemes shown; a randomised variant guards against O(n^2).
 *
 * KEY POINTS:
 *     - Lomuto: pivot at end; simpler.
 *     - Hoare:  pivot at start; fewer swaps.
 *     - Quickselect: same partition gives kth smallest in O(n) average.
 *
 * ALGORITHM / APPROACH:
 *     See per-function code; identical to Java/Python.
 *
 * RUST-SPECIFIC NOTES:
 *     - We implement a tiny pseudo-RNG (xorshift) so no external crate
 *       is needed; it's reproducible with a fixed seed.
 *     - Vec::sort_unstable is the standard library's fast unstable sort.
 *
 * DRY RUN:
 *     [10,7,8,9,1,5] Lomuto pivot=5:
 *         scan -> swap(10,1) -> [1,7,8,9,10,5]
 *         place pivot       -> [1,5,8,9,10,7]
 *         pivot index = 1
 *
 * COMPLEXITY:
 *     Average: O(n log n) time, O(log n) stack
 *     Worst:   O(n^2) time
 *     Stable:  NO
 */

// Simple xorshift RNG so we don't need an external crate.
struct Xor64 {
    state: u64,
}
impl Xor64 {
    fn new(seed: u64) -> Self {
        Self { state: if seed == 0 { 0xDEAD_BEEFu64 } else { seed } }
    }
    fn next_u64(&mut self) -> u64 {
        let mut x = self.state;
        x ^= x << 13;
        x ^= x >> 7;
        x ^= x << 17;
        self.state = x;
        x
    }
    /// Inclusive range [lo..=hi].
    fn range(&mut self, lo: usize, hi: usize) -> usize {
        let span = (hi - lo + 1) as u64;
        lo + (self.next_u64() % span) as usize
    }
}

fn lomuto_partition(arr: &mut [i32], low: usize, high: usize) -> usize {
    let pivot = arr[high];
    let mut i: i64 = low as i64 - 1;
    for j in low..high {
        if arr[j] <= pivot {
            i += 1;
            arr.swap(i as usize, j);
        }
    }
    let pivot_pos = (i + 1) as usize;
    arr.swap(pivot_pos, high);
    pivot_pos
}

fn quick_sort_lomuto(arr: &mut [i32], low: i64, high: i64) {
    if low >= high {
        return;
    }
    let p = lomuto_partition(arr, low as usize, high as usize) as i64;
    quick_sort_lomuto(arr, low, p - 1);
    quick_sort_lomuto(arr, p + 1, high);
}

fn hoare_partition(arr: &mut [i32], low: usize, high: usize) -> i64 {
    let pivot = arr[low];
    let mut i: i64 = low as i64 - 1;
    let mut j: i64 = high as i64 + 1;
    loop {
        loop {
            i += 1;
            if arr[i as usize] >= pivot {
                break;
            }
        }
        loop {
            j -= 1;
            if arr[j as usize] <= pivot {
                break;
            }
        }
        if i >= j {
            return j;
        }
        arr.swap(i as usize, j as usize);
    }
}

fn quick_sort_hoare(arr: &mut [i32], low: i64, high: i64) {
    if low >= high {
        return;
    }
    let p = hoare_partition(arr, low as usize, high as usize);
    quick_sort_hoare(arr, low, p);
    quick_sort_hoare(arr, p + 1, high);
}

fn quick_sort_random(arr: &mut [i32], low: i64, high: i64, rng: &mut Xor64) {
    if low >= high {
        return;
    }
    let pivot_idx = rng.range(low as usize, high as usize);
    arr.swap(pivot_idx, high as usize);
    let p = lomuto_partition(arr, low as usize, high as usize) as i64;
    quick_sort_random(arr, low, p - 1, rng);
    quick_sort_random(arr, p + 1, high, rng);
}

fn quick_select(arr: &mut [i32], low: i64, high: i64, k: i64, rng: &mut Xor64) -> i32 {
    if low == high {
        return arr[low as usize];
    }
    let pivot_idx = rng.range(low as usize, high as usize);
    arr.swap(pivot_idx, high as usize);
    let p = lomuto_partition(arr, low as usize, high as usize) as i64;
    let rank = p - low + 1;
    if rank == k {
        arr[p as usize]
    } else if k < rank {
        quick_select(arr, low, p - 1, k, rng)
    } else {
        quick_select(arr, p + 1, high, k - rank, rng)
    }
}

fn main() {
    let base = vec![10, 7, 8, 9, 1, 5];

    let mut arr1 = base.clone();
    let hi1 = arr1.len() as i64 - 1;
    println!("Lomuto QuickSort:");
    println!("Before: {:?}", arr1);
    quick_sort_lomuto(&mut arr1, 0, hi1);
    println!("After:  {:?}", arr1);

    let mut arr2 = base.clone();
    let hi2 = arr2.len() as i64 - 1;
    println!("\nHoare QuickSort:");
    println!("Before: {:?}", arr2);
    quick_sort_hoare(&mut arr2, 0, hi2);
    println!("After:  {:?}", arr2);

    let mut rng = Xor64::new(42);
    let mut arr3 = base.clone();
    let hi3 = arr3.len() as i64 - 1;
    println!("\nRandomized QuickSort:");
    quick_sort_random(&mut arr3, 0, hi3, &mut rng);
    println!("After:  {:?}", arr3);

    let mut worst = vec![1, 2, 3, 4, 5, 6, 7, 8];
    let hi_w = worst.len() as i64 - 1;
    quick_sort_random(&mut worst, 0, hi_w, &mut rng);
    println!("\nAlready sorted -> randomised: {:?}", worst);

    let arr4 = vec![3, 2, 1, 5, 6, 4];
    println!("\nQuickSelect — kth smallest:");
    for k in 1..=arr4.len() {
        let mut copy = arr4.clone();
        let n = copy.len() as i64;
        let v = quick_select(&mut copy, 0, n - 1, k as i64, &mut rng);
        println!("k={}: {}", k, v);
    }
}

/*
 * NOTES — Rust vs Java:
 *     - i64 indices simplify "i = low - 1" / "j = high + 1" without
 *       fighting usize underflow.
 *     - We embed a tiny xorshift RNG to remain crate-free; the `rand`
 *       crate would normally provide this.
 *     - Vec::sort_unstable is the standard library's quicksort-derived sort.
 */
