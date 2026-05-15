/*
 * WEEK 5 - RUST FUNCTIONS & RECURSION
 * Topic: Tower of Hanoi
 * File: 5.tower_of_hanoi.rs
 *
 * COMPLEXITY: O(2^n) -- minimum number of moves is 2^n - 1.
 */

fn hanoi(n: u32, src: char, aux: char, dst: char, count: &mut u64) {
    if n == 0 { return; }
    hanoi(n - 1, src, dst, aux, count);
    *count += 1;
    println!("Move disk {n}: {src} -> {dst}");
    hanoi(n - 1, aux, src, dst, count);
}

fn main() {
    println!("=== Tower of Hanoi: 3 Disks ===");
    let mut count = 0;
    hanoi(3, 'A', 'B', 'C', &mut count);
    println!("Total moves: {count} (expected {})", (1u64 << 3) - 1);

    println!("\n=== Tower of Hanoi: 4 Disks ===");
    count = 0;
    hanoi(4, 'A', 'B', 'C', &mut count);
    println!("Total moves: {count} (expected {})", (1u64 << 4) - 1);

    println!("\nDisks | Moves");
    println!("------+------");
    for i in 1..=20 {
        println!("  {i:>2}  | {:>10}", (1u64 << i) - 1);
    }
}

/*
 * NOTES:
 *  - We pass a `&mut u64 count` to thread mutable state through the recursion
 *    -- Rust's idiomatic alternative to a global counter.
 *  - Printing all moves becomes impractical for n > 25.
 */
