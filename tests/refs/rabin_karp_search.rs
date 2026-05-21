// Reference Rust driver for tests/cases/rabin_karp_search.json.
use std::io::{self, BufRead};

fn rabin_karp(t: &[u8], p: &[u8]) -> Vec<i32> {
    let base: i64 = 256;
    let prime: i64 = 1_000_000_007;
    let (n, m) = (t.len(), p.len());
    let mut out = Vec::new();
    if m == 0 || m > n { return out; }
    let mut h: i64 = 1;
    for _ in 0..m-1 { h = (h * base) % prime; }
    let mut ph: i64 = 0; let mut th: i64 = 0;
    for i in 0..m {
        ph = (base * ph + p[i] as i64) % prime;
        th = (base * th + t[i] as i64) % prime;
    }
    for i in 0..=n-m {
        if ph == th && &t[i..i+m] == p { out.push(i as i32); }
        if i < n - m {
            th = (base * (th - (t[i] as i64) * h) + (t[i+m] as i64)) % prime;
            if th < 0 { th += prime; }
        }
    }
    out
}

fn parse_str(line: &str) -> String {
    let rest = &line[4..];
    if let Some(sp) = rest.find(' ') {
        let len: usize = rest[..sp].parse().unwrap_or(0);
        let s: String = rest[sp+1..].to_string();
        if s.chars().count() < len { let mut s = s; s.push_str(&" ".repeat(len - s.chars().count())); s }
        else { s }
    } else { String::new() }
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut t = String::new(); let mut pat = String::new();
    let mut expected: Vec<i32> = Vec::new();
    let mut str_idx = 0i32; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, t: &mut String, pat: &mut String, expected: &mut Vec<i32>,
                 str_idx: &mut i32, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *str_idx >= 2 && *he {
            let got = rabin_karp(t.as_bytes(), pat.as_bytes());
            if got == *expected { println!("PASS rabin_karp_search :: {}", name); *p += 1; }
            else { println!("FAIL rabin_karp_search :: {}\n  expected: {:?}\n  got: {:?}", name, expected, got); *f += 1; }
        }
        name.clear(); t.clear(); pat.clear(); expected.clear(); *str_idx = 0; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut t, &mut pat, &mut expected, &mut str_idx, &mut he, &mut p, &mut f); continue; }
        if let Some(rest) = line.strip_prefix("CASE ") { name = rest.to_string(); str_idx = 0; }
        else if line.starts_with("STR ") {
            let s = parse_str(&line);
            if str_idx == 0 { t = s; str_idx += 1; } else { pat = s; str_idx += 1; }
        }
        else if line.starts_with("ARR ") {
            let mut parts = line.split_whitespace(); parts.next();
            let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
            expected.clear();
            for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i32>() { expected.push(v); } } }
            he = true;
        }
    }
    flush(&mut name, &mut t, &mut pat, &mut expected, &mut str_idx, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
