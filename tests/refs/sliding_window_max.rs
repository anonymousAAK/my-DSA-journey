// Reference Rust driver for tests/cases/sliding_window_max.json.
use std::collections::VecDeque;
use std::io::{self, BufRead};

fn sliding_window_max(a: &[i64], k: usize) -> Vec<i64> {
    let n = a.len();
    let mut out = Vec::new();
    if n == 0 || k == 0 { return out; }
    let mut dq: VecDeque<usize> = VecDeque::new();
    for i in 0..n {
        while let Some(&front) = dq.front() {
            if (front as isize) < (i as isize) - (k as isize) + 1 { dq.pop_front(); }
            else { break; }
        }
        while let Some(&back) = dq.back() {
            if a[back] < a[i] { dq.pop_back(); } else { break; }
        }
        dq.push_back(i);
        if i + 1 >= k { out.push(a[*dq.front().unwrap()]); }
    }
    out
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut arr: Vec<i64> = Vec::new(); let mut expected: Vec<i64> = Vec::new();
    let mut k: i64 = 0;
    let mut phase = 0i32; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, arr: &mut Vec<i64>, expected: &mut Vec<i64>, k: i64,
                 phase: &mut i32, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *phase >= 2 && *he {
            let got = sliding_window_max(arr, k as usize);
            if got == *expected { println!("PASS sliding_window_max :: {}", name); *p += 1; }
            else { println!("FAIL sliding_window_max :: {}\n  expected: {:?}\n  got: {:?}", name, expected, got); *f += 1; }
        }
        name.clear(); arr.clear(); expected.clear(); *phase = 0; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut arr, &mut expected, k, &mut phase, &mut he, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); phase = 0; }
            "ARR" => {
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                if phase == 0 {
                    arr.clear();
                    for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { arr.push(v); } } }
                    phase = 1;
                } else {
                    expected.clear();
                    for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { expected.push(v); } } }
                    he = true;
                }
            }
            "INT" => { k = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0); phase = 2; }
            _ => {}
        }
    }
    flush(&mut name, &mut arr, &mut expected, k, &mut phase, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
