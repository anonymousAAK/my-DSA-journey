// Reference Rust driver for tests/cases/linear_search.json.
use std::io::{self, BufRead};

fn linear_search(arr: &[i64], target: i64) -> i64 {
    for (i, &x) in arr.iter().enumerate() {
        if x == target { return i as i64; }
    }
    -1
}

fn main() {
    let stdin = io::stdin();
    let mut case_name = String::new();
    let mut arr: Vec<i64> = Vec::new();
    let mut target: i64 = 0;
    let mut expected: i64 = 0;
    let mut hi = false; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;

    let mut flush = |name: &mut String, arr: &mut Vec<i64>, t: i64, e: i64,
                     hi: &mut bool, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = linear_search(arr, t);
            if got == e { println!("PASS linear_search :: {}", name); *p += 1; }
            else { println!("FAIL linear_search :: {}\n  expected: {}\n  got: {}", name, e, got); *f += 1; }
        }
        name.clear(); arr.clear(); *hi = false; *he = false;
    };

    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut case_name, &mut arr, target, expected, &mut hi, &mut he, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { case_name = parts.next().unwrap_or("").to_string(); }
            "INPUT" => {
                arr.clear();
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { arr.push(v); } } }
                target = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                hi = true;
            }
            "INT" => { expected = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0); he = true; }
            _ => {}
        }
    }
    flush(&mut case_name, &mut arr, target, expected, &mut hi, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
