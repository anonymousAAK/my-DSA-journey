// Reference Rust driver for tests/cases/two_sum.json.
use std::collections::HashMap;
use std::io::{self, BufRead};

fn two_sum(nums: &[i64], target: i64) -> Vec<i32> {
    let mut seen: HashMap<i64, i32> = HashMap::new();
    for (i, &x) in nums.iter().enumerate() {
        let comp = target - x;
        if let Some(&j) = seen.get(&comp) { return vec![j, i as i32]; }
        seen.insert(x, i as i32);
    }
    vec![-1, -1]
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut nums: Vec<i64> = Vec::new();
    let mut expected: Vec<i32> = Vec::new();
    let mut target: i64 = 0;
    let mut phase = 0i32; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, nums: &mut Vec<i64>, expected: &mut Vec<i32>, target: i64,
                 phase: &mut i32, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *phase >= 2 && *he {
            let got = two_sum(nums, target);
            if got == *expected { println!("PASS two_sum :: {}", name); *p += 1; }
            else { println!("FAIL two_sum :: {}\n  expected: {:?}\n  got: {:?}", name, expected, got); *f += 1; }
        }
        name.clear(); nums.clear(); expected.clear(); *phase = 0; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut nums, &mut expected, target, &mut phase, &mut he, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); phase = 0; }
            "ARR" => {
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                if phase == 0 {
                    nums.clear();
                    for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { nums.push(v); } } }
                    phase = 1;
                } else {
                    expected.clear();
                    for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i32>() { expected.push(v); } } }
                    he = true;
                }
            }
            "INT" => {
                target = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                phase = 2;
            }
            _ => {}
        }
    }
    flush(&mut name, &mut nums, &mut expected, target, &mut phase, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
