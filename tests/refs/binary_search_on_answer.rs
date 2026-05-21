// Reference Rust driver for tests/cases/binary_search_on_answer.json.
use std::io::{self, BufRead};

fn min_eating_speed(piles: &[i64], h: i64) -> i64 {
    let mut lo: i64 = 1;
    let mut hi: i64 = *piles.iter().max().unwrap_or(&1);
    let can = |speed: i64| -> bool {
        let mut hrs = 0i64;
        for &p in piles { hrs += (p + speed - 1) / speed; }
        hrs <= h
    };
    while lo < hi {
        let mid = lo + (hi - lo) / 2;
        if can(mid) { hi = mid; } else { lo = mid + 1; }
    }
    lo
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut piles: Vec<i64> = Vec::new();
    let mut h: i64 = 0; let mut expected: i64 = 0;
    let mut phase = 0i32; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, piles: &mut Vec<i64>, h: i64, expected: i64,
                 phase: &mut i32, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *phase >= 2 && *he {
            let got = min_eating_speed(piles, h);
            if got == expected { println!("PASS binary_search_on_answer :: {}", name); *p += 1; }
            else { println!("FAIL binary_search_on_answer :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); piles.clear(); *phase = 0; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut piles, h, expected, &mut phase, &mut he, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); phase = 0; }
            "ARR" => {
                piles.clear();
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { piles.push(v); } } }
                phase = 1;
            }
            "INT" => {
                let v: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                if phase == 1 { h = v; phase = 2; } else { expected = v; he = true; }
            }
            _ => {}
        }
    }
    flush(&mut name, &mut piles, h, expected, &mut phase, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
