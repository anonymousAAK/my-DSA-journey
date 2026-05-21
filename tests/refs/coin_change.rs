// Reference Rust driver for tests/cases/coin_change.json.
use std::io::{self, BufRead};

fn coin_change(coins: &[i64], amount: i64) -> i64 {
    let inf = i64::MAX / 2;
    let n = amount as usize;
    let mut dp = vec![inf; n + 1];
    dp[0] = 0;
    for a in 1..=n as i64 {
        for &c in coins {
            if c <= a && dp[(a - c) as usize] + 1 < dp[a as usize] {
                dp[a as usize] = dp[(a - c) as usize] + 1;
            }
        }
    }
    if dp[n] == inf { -1 } else { dp[n] }
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut coins: Vec<i64> = Vec::new();
    let mut amount: i64 = 0; let mut expected: i64 = 0;
    let mut phase = 0i32; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, coins: &mut Vec<i64>, amount: i64, expected: i64,
                 phase: &mut i32, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *phase >= 2 && *he {
            let got = coin_change(coins, amount);
            if got == expected { println!("PASS coin_change :: {}", name); *p += 1; }
            else { println!("FAIL coin_change :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); coins.clear(); *phase = 0; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut coins, amount, expected, &mut phase, &mut he, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); phase = 0; }
            "ARR" => {
                coins.clear();
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { coins.push(v); } } }
                phase = 1;
            }
            "INT" => {
                let v: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                if phase == 1 { amount = v; phase = 2; } else { expected = v; he = true; }
            }
            _ => {}
        }
    }
    flush(&mut name, &mut coins, amount, expected, &mut phase, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
