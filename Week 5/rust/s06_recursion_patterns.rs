/*
 * WEEK 5 - RUST FUNCTIONS & RECURSION
 * Topic: Common Recursion Patterns
 * File: 6.recursion_patterns.rs
 *
 * PATTERNS DEMONSTRATED:
 *  1. Linear recursion -- reverse a string.
 *  2. Tail recursion w/ accumulator -- factorial.
 *  3. Mutual recursion -- isEven / isOdd.
 *  4. Helper / accumulator -- digit sum.
 *  5. Subset enumeration -- foundation of backtracking.
 *  6. Two-pointer recursion -- palindrome.
 */

fn reverse_str(s: &str) -> String {
    if s.is_empty() { return String::new(); }
    let mut chars = s.chars();
    let first = chars.next().unwrap();
    let rest: String = chars.collect();
    let mut acc = reverse_str(&rest);
    acc.push(first);
    acc
}

fn fact_tail(n: u64, acc: u64) -> u64 {
    if n <= 1 { acc } else { fact_tail(n - 1, n * acc) }
}

fn is_even(n: i32) -> bool { if n == 0 { true } else { is_odd(n - 1) } }
fn is_odd (n: i32) -> bool { if n == 0 { false } else { is_even(n - 1) } }

fn digit_sum(n: u64) -> u64 {
    if n == 0 { 0 } else { (n % 10) + digit_sum(n / 10) }
}

fn subsets(arr: &[i32], idx: usize, current: &mut Vec<i32>) {
    if idx == arr.len() {
        print!("{{");
        for (i, x) in current.iter().enumerate() {
            if i > 0 { print!(","); }
            print!("{x}");
        }
        println!("}}");
        return;
    }
    // exclude
    subsets(arr, idx + 1, current);
    // include
    current.push(arr[idx]);
    subsets(arr, idx + 1, current);
    current.pop();    // backtrack
}

fn is_palindrome(bytes: &[u8], l: usize, r: usize) -> bool {
    if l >= r { return true; }
    if bytes[l] != bytes[r] { return false; }
    is_palindrome(bytes, l + 1, r - 1)
}

fn main() {
    println!("reverse('hello') = {}", reverse_str("hello"));
    println!("fact_tail(5)   = {}", fact_tail(5, 1));
    println!("fact_tail(10)  = {}", fact_tail(10, 1));
    println!("is_even(4) = {}", is_even(4));
    println!("is_odd(7)  = {}", is_odd(7));
    println!("digit_sum(1234) = {}", digit_sum(1234));

    println!("\nAll subsets of [1, 2, 3]:");
    let arr = vec![1, 2, 3];
    let mut current = Vec::new();
    subsets(&arr, 0, &mut current);

    println!("\nis_palindrome('racecar') = {}", is_palindrome("racecar".as_bytes(), 0, 6));
    println!("is_palindrome('hello')   = {}", is_palindrome("hello".as_bytes(), 0, 4));
}

/*
 * NOTES:
 *  - Rust does NOT guarantee TCO; deep tail recursion may blow the stack.
 *  - Subset enumeration uses backtracking with `push` + `pop` to share one Vec.
 *  - Palindrome operates on byte indices because Rust strings are UTF-8 (chars
 *    aren't directly indexable). For non-ASCII, use chars() and collect into Vec<char>.
 */
