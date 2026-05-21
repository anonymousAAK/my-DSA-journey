// Reference Rust driver for tests/cases/kadane_max_subarray.json.
//
// Stdin line format (see tests/harness/emit_lines.py):
//   CASE <name>
//   ARR <n> <v1> ... <vn>
//   INT <expected>
//   <blank>

use std::io::{self, BufRead};

fn max_subarray_sum(arr: &[i64]) -> i64 {
    if arr.is_empty() { return 0; }
    let mut best = arr[0];
    let mut current = arr[0];
    for &x in &arr[1..] {
        current = std::cmp::max(x, current + x);
        best = std::cmp::max(best, current);
    }
    best
}

fn main() {
    let stdin = io::stdin();
    let mut case_name = String::new();
    let mut arr: Vec<i64> = Vec::new();
    let mut expected: i64 = 0;
    let mut have_input = false; let mut have_expected = false;
    let mut passed = 0u32; let mut failed = 0u32;

    let mut run = |name: &mut String, arr: &mut Vec<i64>, expected: i64,
                   hi: &mut bool, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = max_subarray_sum(arr);
            if got == expected { println!("PASS kadane_max_subarray :: {}", name); *p += 1; }
            else { println!("FAIL kadane_max_subarray :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); arr.clear(); *hi = false; *he = false;
    };

    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() {
            run(&mut case_name, &mut arr, expected, &mut have_input, &mut have_expected, &mut passed, &mut failed);
            continue;
        }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { case_name = parts.next().unwrap_or("").to_string(); }
            "ARR" => {
                arr.clear();
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                for _ in 0..n {
                    if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { arr.push(v); } }
                }
                have_input = true;
            }
            "INT" => {
                expected = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                have_expected = true;
            }
            _ => {}
        }
    }
    run(&mut case_name, &mut arr, expected, &mut have_input, &mut have_expected, &mut passed, &mut failed);
    println!("TOTAL: {} passed, {} failed", passed, failed);
    std::process::exit(if failed == 0 { 0 } else { 1 });
}
