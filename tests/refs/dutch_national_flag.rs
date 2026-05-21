// Reference Rust driver for tests/cases/dutch_national_flag.json.
use std::io::{self, BufRead};

fn dutch_flag(a: &mut Vec<i32>) {
    let (mut lo, mut mid) = (0usize, 0usize);
    if a.is_empty() { return; }
    let mut hi = a.len() - 1;
    loop {
        if mid > hi { break; }
        match a[mid] {
            0 => { a.swap(lo, mid); lo += 1; mid += 1; }
            2 => { a.swap(mid, hi); if hi == 0 { break; } hi -= 1; }
            _ => { mid += 1; }
        }
    }
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut arr: Vec<i32> = Vec::new();
    let mut expected: Vec<i32> = Vec::new();
    let mut hi = false; let mut he = false; let mut phase = 0;
    let mut p = 0u32; let mut f = 0u32;

    let flush = |name: &mut String, arr: &mut Vec<i32>, expected: &mut Vec<i32>,
                 hi: &mut bool, he: &mut bool, phase: &mut i32, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let mut got = arr.clone();
            dutch_flag(&mut got);
            if got == *expected { println!("PASS dutch_national_flag :: {}", name); *p += 1; }
            else {
                println!("FAIL dutch_national_flag :: {}\n  expected: {:?}\n  got: {:?}", name, expected, got);
                *f += 1;
            }
        }
        name.clear(); arr.clear(); expected.clear(); *hi = false; *he = false; *phase = 0;
    };

    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() {
            flush(&mut name, &mut arr, &mut expected, &mut hi, &mut he, &mut phase, &mut p, &mut f);
            continue;
        }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); phase = 0; }
            "ARR" => {
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                let mut tmp: Vec<i32> = Vec::with_capacity(n);
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i32>() { tmp.push(v); } } }
                if phase == 0 { arr = tmp; hi = true; phase = 1; }
                else { expected = tmp; he = true; }
            }
            _ => {}
        }
    }
    flush(&mut name, &mut arr, &mut expected, &mut hi, &mut he, &mut phase, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
