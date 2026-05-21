// Reference Rust driver for tests/cases/valid_anagram.json.
use std::io::{self, BufRead};
use std::collections::HashMap;

fn is_anagram(a: &str, b: &str) -> bool {
    if a.chars().count() != b.chars().count() { return false; }
    let mut cnt: HashMap<char, i32> = HashMap::new();
    for c in a.chars() { *cnt.entry(c).or_insert(0) += 1; }
    for c in b.chars() {
        let e = cnt.entry(c).or_insert(0); *e -= 1;
        if *e < 0 { return false; }
    }
    true
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
    let mut name = String::new(); let mut a = String::new(); let mut b = String::new();
    let mut expected = 0i32;
    let mut str_idx = 0i32; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, a: &mut String, b: &mut String, expected: i32,
                 str_idx: &mut i32, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *str_idx >= 2 && *he {
            let got = is_anagram(a, b);
            if (got as i32) == expected { println!("PASS valid_anagram :: {}", name); *p += 1; }
            else { println!("FAIL valid_anagram :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); a.clear(); b.clear(); *str_idx = 0; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut a, &mut b, expected, &mut str_idx, &mut he, &mut p, &mut f); continue; }
        if let Some(rest) = line.strip_prefix("CASE ") { name = rest.to_string(); str_idx = 0; }
        else if line.starts_with("STR ") {
            let s = parse_str(&line);
            if str_idx == 0 { a = s; str_idx += 1; } else { b = s; str_idx += 1; }
        }
        else if let Some(rest) = line.strip_prefix("BOOL ") { expected = rest.parse().unwrap_or(0); he = true; }
    }
    flush(&mut name, &mut a, &mut b, expected, &mut str_idx, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
