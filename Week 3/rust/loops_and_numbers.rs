//! WEEK 3 — Rust: Advanced Loops & Number Theory Basics
//! Covers: Fibonacci, primes, binary/decimal conversion, bitwise operators.

// --- Fibonacci ---
/// Return the Nth Fibonacci number (0-indexed).
/// Time: O(n), Space: O(1)
fn fibonacci(n: u32) -> u64 {
    if n <= 1 {
        return n as u64;
    }
    let (mut a, mut b) = (0u64, 1u64);
    for _ in 2..=n {
        let tmp = a + b;
        a = b;
        b = tmp;
    }
    b
}

// --- Prime Numbers ---
/// Check if n is prime. Time: O(sqrt(n))
fn is_prime(n: u64) -> bool {
    if n < 2 { return false; }
    if n < 4 { return true; }
    if n % 2 == 0 || n % 3 == 0 { return false; }
    let mut i = 5u64;
    while i * i <= n {
        if n % i == 0 || n % (i + 2) == 0 {
            return false;
        }
        i += 6;
    }
    true
}

/// Find all primes up to limit using Sieve of Eratosthenes.
/// Time: O(n log log n), Space: O(n)
fn sieve_of_eratosthenes(limit: usize) -> Vec<usize> {
    if limit < 2 { return vec![]; }
    let mut is_p = vec![true; limit + 1];
    is_p[0] = false;
    is_p[1] = false;
    let mut i = 2;
    while i * i <= limit {
        if is_p[i] {
            let mut j = i * i;
            while j <= limit {
                is_p[j] = false;
                j += i;
            }
        }
        i += 1;
    }
    (0..=limit).filter(|&x| is_p[x]).collect()
}

// --- Reverse a Number ---
/// Reverse digits of n. Time: O(d), Space: O(1)
fn reverse_number(n: i64) -> i64 {
    let neg = n < 0;
    let mut n = n.abs();
    let mut rev: i64 = 0;
    while n > 0 {
        rev = rev * 10 + n % 10;
        n /= 10;
    }
    if neg { -rev } else { rev }
}

// --- Binary <-> Decimal ---
/// Convert decimal to binary string. Time: O(log n)
fn decimal_to_binary(n: u64) -> String {
    if n == 0 { return "0".to_string(); }
    let mut bits = Vec::new();
    let mut val = n;
    while val > 0 {
        bits.push(if val % 2 == 1 { '1' } else { '0' });
        val /= 2;
    }
    bits.iter().rev().collect()
}

/// Convert binary string to decimal. Time: O(len)
fn binary_to_decimal(s: &str) -> u64 {
    let mut result = 0u64;
    for ch in s.chars() {
        result = result * 2 + (ch as u64 - '0' as u64);
    }
    result
}

// --- Bit Tricks ---
/// Count set bits (Kernighan's method). Time: O(set bits)
fn count_set_bits(mut n: u32) -> u32 {
    let mut count = 0;
    while n != 0 {
        n &= n - 1;
        count += 1;
    }
    count
}

/// Check if n is a power of 2.
fn is_power_of_two(n: u32) -> bool {
    n > 0 && (n & (n - 1)) == 0
}

// --- Valley Sequence ---
/// Check if sequence strictly decreases then strictly increases (valley shape).
/// Time: O(n), Space: O(1)
fn is_valley_sequence(arr: &[i32]) -> bool {
    let n = arr.len();
    if n < 3 { return false; }
    let mut i = 0;
    while i < n - 1 && arr[i] > arr[i + 1] {
        i += 1;
    }
    if i == 0 || i == n - 1 { return false; }
    while i < n - 1 && arr[i] < arr[i + 1] {
        i += 1;
    }
    i == n - 1
}

fn main() {
    // Fibonacci
    println!("--- Fibonacci ---");
    let fibs: Vec<u64> = (0..10).map(fibonacci).collect();
    println!("First 10: {:?}", fibs);

    // Primes
    println!("\n--- Primes ---");
    println!("is_prime(17): {}", is_prime(17));
    println!("is_prime(20): {}", is_prime(20));
    println!("Primes up to 50: {:?}", sieve_of_eratosthenes(50));

    // Reverse Number
    println!("\n--- Reverse Number ---");
    for &num in &[1234i64, -567, 1000] {
        println!("reverse({}) = {}", num, reverse_number(num));
    }

    // Binary Conversion
    println!("\n--- Binary Conversion ---");
    for &num in &[0u64, 5, 10, 42, 255] {
        let b = decimal_to_binary(num);
        let back = binary_to_decimal(&b);
        println!("{} -> {} -> {}", num, b, back);
    }

    // Bitwise Operators
    println!("\n--- Bitwise Operators ---");
    let (a, b): (u32, u32) = (12, 10);
    println!("a = {} ({:b}), b = {} ({:b})", a, a, b, b);
    println!("a & b  = {} ({:b})", a & b, a & b);
    println!("a | b  = {} ({:b})", a | b, a | b);
    println!("a ^ b  = {} ({:b})", a ^ b, a ^ b);
    println!("a << 2 = {}", a << 2);
    println!("a >> 2 = {}", a >> 2);

    // Bit Tricks
    println!("\n--- Bit Tricks ---");
    println!("Is 20 power of 2? {}", is_power_of_two(20));
    println!("Is 16 power of 2? {}", is_power_of_two(16));
    println!("Set bits in 13 (1101): {}", count_set_bits(13));
    println!("Set bits in 255 (11111111): {}", count_set_bits(255));

    // Valley Sequence
    println!("\n--- Valley Sequence ---");
    println!("{}", is_valley_sequence(&[5, 3, 1, 2, 4]));  // true
    println!("{}", is_valley_sequence(&[1, 2, 3]));          // false
    println!("{}", is_valley_sequence(&[3, 2, 1]));          // false
}
