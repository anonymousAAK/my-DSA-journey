// Reference Rust driver for tests/cases/merge_sort.json.
use std::io::{self, BufRead};

fn merge_sort_rec(a: &mut [i64]) {
    let n = a.len();
    if n <= 1 { return; }
    let m = n / 2;
    merge_sort_rec(&mut a[..m]);
    merge_sort_rec(&mut a[m..]);
    let mut tmp = Vec::with_capacity(n);
    let (mut i, mut j) = (0usize, m);
    while i < m && j < n {
        if a[i] <= a[j] { tmp.push(a[i]); i += 1; } else { tmp.push(a[j]); j += 1; }
    }
    while i < m { tmp.push(a[i]); i += 1; }
    while j < n { tmp.push(a[j]); j += 1; }
    a.copy_from_slice(&tmp);
}
fn merge_sort(mut a: Vec<i64>) -> Vec<i64> { merge_sort_rec(&mut a); a }

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut arr: Vec<i64> = Vec::new(); let mut expected: Vec<i64> = Vec::new();
    let mut hi = false; let mut he = false; let mut phase = 0;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, arr: &mut Vec<i64>, expected: &mut Vec<i64>,
                 hi: &mut bool, he: &mut bool, phase: &mut i32, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = merge_sort(arr.clone());
            if got == *expected { println!("PASS merge_sort :: {}", name); *p += 1; }
            else { println!("FAIL merge_sort :: {}\n  expected: {:?}\n  got: {:?}", name, expected, got); *f += 1; }
        }
        name.clear(); arr.clear(); expected.clear(); *hi = false; *he = false; *phase = 0;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut arr, &mut expected, &mut hi, &mut he, &mut phase, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); phase = 0; }
            "ARR" => {
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                let mut tmp: Vec<i64> = Vec::with_capacity(n);
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { tmp.push(v); } } }
                if phase == 0 { arr = tmp; hi = true; phase = 1; } else { expected = tmp; he = true; }
            }
            _ => {}
        }
    }
    flush(&mut name, &mut arr, &mut expected, &mut hi, &mut he, &mut phase, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
