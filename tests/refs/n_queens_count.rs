// Reference Rust driver for tests/cases/n_queens_count.json.
use std::io::{self, BufRead};

fn n_queens_count(n: i32) -> i32 {
    if n <= 0 { return 0; }
    let mut q: Vec<i32> = vec![-1; n as usize];
    let mut count = 0;
    fn go(row: i32, n: i32, q: &mut Vec<i32>, count: &mut i32) {
        if row == n { *count += 1; return; }
        for col in 0..n {
            let mut ok = true;
            for r in 0..row {
                let c = q[r as usize];
                if c == col || (c - col).abs() == (r - row).abs() { ok = false; break; }
            }
            if ok { q[row as usize] = col; go(row + 1, n, q, count); q[row as usize] = -1; }
        }
    }
    go(0, n, &mut q, &mut count);
    count
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut n_in: i64 = 0; let mut expected: i64 = 0;
    let mut phase = 0i32; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, n_in: i64, expected: i64,
                 phase: &mut i32, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *phase >= 1 && *he {
            let got = n_queens_count(n_in as i32) as i64;
            if got == expected { println!("PASS n_queens_count :: {}", name); *p += 1; }
            else { println!("FAIL n_queens_count :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); *phase = 0; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, n_in, expected, &mut phase, &mut he, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); phase = 0; }
            "INT" => {
                let v: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                if phase == 0 { n_in = v; phase = 1; } else { expected = v; he = true; }
            }
            _ => {}
        }
    }
    flush(&mut name, n_in, expected, &mut phase, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
