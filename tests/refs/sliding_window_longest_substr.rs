// Reference Rust driver for tests/cases/sliding_window_longest_substr.json.
use std::collections::HashMap;
use std::io::{self, BufRead};

fn longest_unique(s: &str) -> i32 {
    let mut last: HashMap<char, i32> = HashMap::new();
    let mut best = 0i32; let mut l = 0i32;
    for (i, c) in s.chars().enumerate() {
        let i = i as i32;
        if let Some(&p) = last.get(&c) { if p >= l { l = p + 1; } }
        last.insert(c, i);
        if i - l + 1 > best { best = i - l + 1; }
    }
    best
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
    let mut name = String::new(); let mut s = String::new();
    let mut expected = 0i32;
    let mut hi = false; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, s: &mut String, expected: i32, hi: &mut bool, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = longest_unique(s);
            if got == expected { println!("PASS sliding_window_longest_substr :: {}", name); *p += 1; }
            else { println!("FAIL sliding_window_longest_substr :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); s.clear(); *hi = false; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut s, expected, &mut hi, &mut he, &mut p, &mut f); continue; }
        if let Some(rest) = line.strip_prefix("CASE ") { name = rest.to_string(); }
        else if line.starts_with("STR ") { s = parse_str(&line); hi = true; }
        else if let Some(rest) = line.strip_prefix("INT ") { expected = rest.parse().unwrap_or(0); he = true; }
    }
    flush(&mut name, &mut s, expected, &mut hi, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
