//! WEEK 2 — Rust: Control Flow & Loops
//! Covers: if/else, match, loop/while/for, break/continue, iterators
//! Equivalent to Java Week 2.

/// Sum even and odd digits — O(d) time, O(1) space
fn sum_even_odd_digits(mut n: i32) -> (i32, i32) {
    let (mut even_sum, mut odd_sum) = (0, 0);
    n = n.abs();
    while n > 0 {
        let digit = n % 10;
        if digit % 2 == 0 { even_sum += digit; }
        else { odd_sum += digit; }
        n /= 10;
    }
    (even_sum, odd_sum)
}

/// All factors — O(sqrt(n)) time
fn factors(n: i32) -> Vec<i32> {
    let mut result = Vec::new();
    let mut i = 1;
    while i * i <= n {
        if n % i == 0 {
            result.push(i);
            if i != n / i { result.push(n / i); }
        }
        i += 1;
    }
    result.sort();
    result
}

/// Power x^n — O(n) time
fn power(x: i64, n: u32) -> i64 {
    let mut result: i64 = 1;
    for _ in 0..n {
        result *= x;
    }
    result
}

fn main() {
    // --- If / Else ---
    // In Rust, if/else is an EXPRESSION (returns a value!)
    let x = 42;
    let category = if x > 100 { "Big" }
                   else if x > 10 { "Medium" }
                   else { "Small" };
    println!("{} is {}", x, category);

    let status = if x % 2 == 0 { "even" } else { "odd" };
    println!("{} is {}", x, status);

    // --- Match (Rust's powerful switch) ---
    println!("\n--- Match ---");
    let day = 3;
    let day_name = match day {
        1 => "Monday",
        2 => "Tuesday",
        3 => "Wednesday",
        4 => "Thursday",
        5 => "Friday",
        6 | 7 => "Weekend",   // or pattern
        _ => "Invalid",        // default (required — must be exhaustive!)
    };
    println!("Day {}: {}", day, day_name);

    // Match with ranges
    let score = 85;
    let grade = match score {
        90..=100 => "A",
        80..=89 => "B",
        70..=79 => "C",
        _ => "F",
    };
    println!("Score {}: Grade {}", score, grade);

    // --- While Loop ---
    println!("\n--- Multiplication Table (while) ---");
    let n = 7;
    let mut i = 1;
    while i <= 10 {
        println!("{} x {} = {}", n, i, n * i);
        i += 1; // Rust has no ++ operator
    }

    // --- Loop (infinite loop with break) ---
    println!("\n--- Loop with break ---");
    let mut count = 0;
    let result = loop {
        count += 1;
        if count == 5 {
            break count * 10; // loop can return a value via break!
        }
    };
    println!("Loop returned: {}", result); // 50

    // --- For Loop ---
    // Rust uses iterators, not C-style for loops
    println!("\n--- For Loop ---");
    print!("1 to 5: ");
    for i in 1..=5 { print!("{} ", i); } // ..= is inclusive range
    println!();

    print!("5 to 1: ");
    for i in (1..=5).rev() { print!("{} ", i); }
    println!();

    print!("Even 0-10: ");
    for i in (0..=10).step_by(2) { print!("{} ", i); }
    println!();

    // --- Even/Odd Digit Sum ---
    println!("\n--- Even/Odd Digit Sum ---");
    for num in [1234, 9876, 555] {
        let (e, o) = sum_even_odd_digits(num);
        println!("{}: even={}, odd={}", num, e, o);
    }

    // --- Factors ---
    println!("\n--- Factors ---");
    for num in [12, 28, 7] {
        println!("Factors of {}: {:?}", num, factors(num));
    }

    // --- Power ---
    println!("\n--- Power ---");
    println!("2^10 = {}", power(2, 10));
    println!("3^5 = {}", power(3, 5));
    // Rust also has: 2_i64.pow(10)

    // --- F to C ---
    println!("\n--- F to C ---");
    println!("{:>5} | {:>8}", "F", "C");
    let mut f = 32;
    while f <= 212 {
        let c = (f as f64 - 32.0) * 5.0 / 9.0;
        println!("{:>5} | {:>8.2}", f, c);
        f += 20;
    }

    // --- Break / Continue ---
    println!("\n--- First prime after 20 ---");
    'outer: for n in 21..100 {
        let mut is_prime = true;
        let mut i = 2;
        while i * i <= n {
            if n % i == 0 { is_prime = false; break; }
            i += 1;
        }
        if is_prime {
            println!("{}", n);
            break 'outer; // labeled break (Rust feature)
        }
    }

    print!("Non-multiples of 3 (1-15): ");
    for i in 1..=15 {
        if i % 3 == 0 { continue; }
        print!("{} ", i);
    }
    println!();

    // --- Iterators (Rust-specific — very powerful) ---
    println!("\n--- Iterators ---");
    let squares: Vec<i32> = (0..10).map(|x| x * x).collect();
    println!("Squares: {:?}", squares);

    let evens: Vec<i32> = (0..20).filter(|x| x % 2 == 0).collect();
    println!("Evens: {:?}", evens);

    let sum: i32 = (1..=100).sum();
    println!("Sum 1..100: {}", sum); // 5050
}
