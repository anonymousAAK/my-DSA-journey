// Reference Rust driver for tests/cases/balanced_parens.json.
use std::io::{self, BufRead};

fn is_balanced(s: &str) -> bool {
    let mut st: Vec<char> = Vec::new();
    for c in s.chars() {
        match c {
            '(' | '[' | '{' => st.push(c),
            ')' | ']' | '}' => {
                let t = match st.pop() { Some(x) => x, None => return false };
                let ok = matches!((t, c), ('(', ')') | ('[', ']') | ('{', '}'));
                if !ok { return false; }
            }
            _ => {}
        }
    }
    st.is_empty()
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
            let got = is_balanced(s);
            if (got as i32) == expected { println!("PASS balanced_parens :: {}", name); *p += 1; }
            else { println!("FAIL balanced_parens :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); s.clear(); *hi = false; *he = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut s, expected, &mut hi, &mut he, &mut p, &mut f); continue; }
        if let Some(rest) = line.strip_prefix("CASE ") { name = rest.to_string(); }
        else if line.starts_with("STR ") { s = parse_str(&line); hi = true; }
        else if let Some(rest) = line.strip_prefix("BOOL ") { expected = rest.parse().unwrap_or(0); he = true; }
    }
    flush(&mut name, &mut s, expected, &mut hi, &mut he, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
