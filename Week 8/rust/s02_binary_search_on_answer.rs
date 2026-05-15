/*
 * WEEK 8 - RUST DSA
 * Topic: Binary Search on the Answer
 * File: 2.binary_search_on_answer.rs
 *
 * CONCEPT:
 *     Binary-search the *answer* space using a monotonic predicate.
 *
 * KEY POINTS:
 *     - Template: lo..hi; while lo<hi: mid=...; if pred(mid) hi=mid else lo=mid+1.
 *     - Problems: integer sqrt, Koko bananas, ship-packages-in-D-days.
 *
 * ALGORITHM / APPROACH:
 *     See per-problem code; each shares the same template.
 *
 * RUST-SPECIFIC NOTES:
 *     - Use i64 for products that may exceed i32 (mid*mid in sqrt).
 *     - iter().max() returns Option<&T>; unwrap when bounds are known nonempty.
 *
 * DRY RUN:
 *     sqrt(17) -> 4
 *     Koko [3,6,7,11] H=8 -> 4
 *     Ship 1..=10 D=5 -> 15
 *
 * COMPLEXITY:
 *     O(log(range) * predicate cost).
 */

fn sqrt_int(n: i64) -> i64 {
    if n < 2 {
        return n;
    }
    let mut lo: i64 = 1;
    let mut hi: i64 = n / 2;
    while lo < hi {
        let mid = lo + (hi - lo + 1) / 2;
        if mid * mid <= n {
            lo = mid;
        } else {
            hi = mid - 1;
        }
    }
    lo
}

fn can_finish(piles: &[i64], h: i64, speed: i64) -> bool {
    let mut hours: i64 = 0;
    for &p in piles {
        hours += (p + speed - 1) / speed;
    }
    hours <= h
}

fn min_eating_speed(piles: &[i64], h: i64) -> i64 {
    let mut lo: i64 = 1;
    let mut hi: i64 = *piles.iter().max().unwrap();
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if can_finish(piles, h, mid) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn can_ship(weights: &[i64], days: i64, capacity: i64) -> bool {
    let mut current_load: i64 = 0;
    let mut days_needed: i64 = 1;
    for &w in weights {
        if w > capacity {
            return false;
        }
        if current_load + w > capacity {
            days_needed += 1;
            current_load = 0;
        }
        current_load += w;
    }
    days_needed <= days
}

fn min_ship_capacity(weights: &[i64], days: i64) -> i64 {
    let mut lo: i64 = *weights.iter().max().unwrap();
    let mut hi: i64 = weights.iter().sum();
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if can_ship(weights, days, mid) {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    lo
}

fn main() {
    println!("=== Integer Square Root ===");
    for n in [0, 1, 4, 8, 9, 16, 17, 100i64] {
        println!("sqrt({:3}) = {}", n, sqrt_int(n));
    }

    println!("\n=== Koko Eating Bananas ===");
    let piles: Vec<i64> = vec![3, 6, 7, 11];
    println!("Piles: {:?}", piles);
    println!("Min speed for H=8: {}", min_eating_speed(&piles, 8));

    let piles2: Vec<i64> = vec![30, 11, 23, 4, 20];
    println!("Piles: {:?}", piles2);
    println!("Min speed for H=5: {}", min_eating_speed(&piles2, 5));
    println!("Min speed for H=6: {}", min_eating_speed(&piles2, 6));

    println!("\n=== Ship Packages ===");
    let weights: Vec<i64> = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    println!("Weights: {:?}", weights);
    println!("Min capacity for D=5 days:  {}", min_ship_capacity(&weights, 5));
    println!("Min capacity for D=10 days: {}", min_ship_capacity(&weights, 10));
}

/*
 * NOTES — Rust vs Java:
 *     - .iter().max() / .iter().sum() express the bounds in one expression.
 *     - i64 arithmetic dodges overflow in mid*mid.
 *     - The monotonic-predicate idea is language-independent — Rust just makes
 *       it pleasantly type-safe.
 */
