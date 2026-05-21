// Reference Rust driver for tests/cases/kth_largest.json. Uses a min-heap of size k.
use std::collections::BinaryHeap;
use std::cmp::Reverse;
use std::io::{self, BufRead};

fn kth_largest(a: &[i64], k: usize) -> i64 {
    let mut h: BinaryHeap<Reverse<i64>> = BinaryHeap::new();
    for &v in a {
        h.push(Reverse(v));
        if h.len() > k { h.pop(); }
    }
    h.peek().map(|r| r.0).unwrap_or(0)
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut arr: Vec<i64> = Vec::new();
    let mut k: i64 = 0; let mut expected: i64 = 0;
    let mut phase = 0i32; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, arr: &mut Vec<i64>, k: i64, expected: i64,
                 phase: &mut i32, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *phase >= 2 && *he {
            let got = kth_largest(arr, k as usize);
            if got == expected { println!("PASS kth_largest :: {}", name); *p += 1; }
            else { println!("FAIL kth_largest :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); arr.clear(); *phase = 0; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut arr, k, expected, &mut phase, &mut he, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); phase = 0; }
            "ARR" => {
                arr.clear();
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { arr.push(v); } } }
                phase = 1;
            }
            "INT" => {
                let v: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                if phase == 1 { k = v; phase = 2; } else { expected = v; he = true; }
            }
            _ => {}
        }
    }
    flush(&mut name, &mut arr, k, expected, &mut phase, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
