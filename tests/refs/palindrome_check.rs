// Reference Rust driver for tests/cases/palindrome_check.json.
use std::io::{self, BufRead};

fn is_palindrome(s: &str) -> bool {
    let bytes: Vec<char> = s.chars().collect();
    let (mut l, mut r) = (0isize, bytes.len() as isize - 1);
    while l < r {
        while l < r && !bytes[l as usize].is_alphanumeric() { l += 1; }
        while l < r && !bytes[r as usize].is_alphanumeric() { r -= 1; }
        if bytes[l as usize].to_lowercase().next() != bytes[r as usize].to_lowercase().next() { return false; }
        l += 1; r -= 1;
    }
    true
}

fn parse_str_line(line: &str) -> String {
    // "STR <len> <content>"; content may contain spaces
    let rest = &line[4..];
    if let Some(sp) = rest.find(' ') {
        let len: usize = rest[..sp].parse().unwrap_or(0);
        let content = &rest[sp+1..];
        let mut s: String = content.to_string();
        if s.chars().count() < len { s.push_str(&" ".repeat(len - s.chars().count())); }
        s
    } else {
        // length 0
        String::new()
    }
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new(); let mut s = String::new();
    let mut expected = 0i32;
    let mut hi = false; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, s: &mut String, expected: i32, hi: &mut bool, he: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = is_palindrome(s);
            if (got as i32) == expected { println!("PASS palindrome_check :: {}", name); *p += 1; }
            else { println!("FAIL palindrome_check :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); s.clear(); *hi = false; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut s, expected, &mut hi, &mut he, &mut p, &mut f); continue; }
        if let Some(rest) = line.strip_prefix("CASE ") { name = rest.to_string(); }
        else if line.starts_with("STR ") { s = parse_str_line(&line); hi = true; }
        else if let Some(rest) = line.strip_prefix("BOOL ") { expected = rest.parse().unwrap_or(0); he = true; }
    }
    flush(&mut name, &mut s, expected, &mut hi, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
