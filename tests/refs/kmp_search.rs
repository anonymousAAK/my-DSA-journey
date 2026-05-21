// Reference Rust driver for tests/cases/kmp_search.json.
use std::io::{self, BufRead};

fn build_lps(p: &[u8]) -> Vec<usize> {
    let m = p.len();
    let mut lps = vec![0usize; m];
    if m == 0 { return lps; }
    let mut len = 0usize; let mut i = 1usize;
    while i < m {
        if p[i] == p[len] { len += 1; lps[i] = len; i += 1; }
        else if len != 0 { len = lps[len - 1]; }
        else { lps[i] = 0; i += 1; }
    }
    lps
}
fn kmp_search(t: &[u8], p: &[u8]) -> Vec<i32> {
    let mut out = Vec::new();
    let (n, m) = (t.len(), p.len());
    if m == 0 || m > n { return out; }
    let lps = build_lps(p);
    let (mut i, mut j) = (0usize, 0usize);
    while i < n {
        if t[i] == p[j] { i += 1; j += 1; }
        if j == m { out.push((i - j) as i32); j = lps[j - 1]; }
        else if i < n && t[i] != p[j] {
            if j != 0 { j = lps[j - 1]; } else { i += 1; }
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
            let got = kmp_search(t.as_bytes(), pat.as_bytes());
            if got == *expected { println!("PASS kmp_search :: {}", name); *p += 1; }
            else { println!("FAIL kmp_search :: {}\n  expected: {:?}\n  got: {:?}", name, expected, got); *f += 1; }
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
