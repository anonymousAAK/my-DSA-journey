/*
 * WEEK 3 - RUST LOOPS & NUMBER THEORY
 * Topic: All Prime Numbers up to N
 * File: 10.all_prime_number.rs
 *
 * PROBLEM:
 *  Print every prime in [2, N], one per line.
 *
 * KEY POINTS:
 *  - Trial division O(N * sqrt N) for ad-hoc.
 *  - Sieve of Eratosthenes O(N log log N) for many primes.
 *  - Use Vec<bool> for the sieve.
 */

use std::io::Read;

fn is_prime(n: i64) -> bool {
    if n < 2 { return false; }
    if n % 2 == 0 { return n == 2; }
    let mut j: i64 = 3;
    while j * j <= n {
        if n % j == 0 { return false; }
        j += 2;
    }
    true
}

fn sieve(n: usize) -> Vec<usize> {
    if n < 2 { return Vec::new(); }
    let mut composite = vec![false; n + 1];
    composite[0] = true;
    composite[1] = true;
    let mut i = 2_usize;
    while i * i <= n {
        if !composite[i] {
            let mut j = i * i;
            while j <= n {
                composite[j] = true;
                j += i;
            }
        }
        i += 1;
    }
    (2..=n).filter(|&k| !composite[k]).collect()
}

fn main() {
    let mut buf = String::new();
    std::io::stdin().read_to_string(&mut buf).ok();
    let n: i64 = buf.split_whitespace().next().and_then(|s| s.parse().ok()).unwrap_or(30);

    for i in 2..=n {
        if is_prime(i) {
            println!("{i}");
        }
    }
    let primes = sieve(n as usize);
    print!("# sieve up to {n}:");
    for p in primes { print!(" {p}"); }
    println!();
}

/*
 * NOTES:
 *  - Vec<bool> is space-inefficient (1 byte per bool); for memory-tight
 *    sieves, use a bit vector via the `bitvec` crate.
 *  - For huge N, segmented sieves split work into cache-sized chunks.
 */
