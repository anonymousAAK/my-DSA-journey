/*
 * WEEK 7 - RUST DSA
 * Topic: String Basics
 * File: 1.string_basics.rs
 *
 * CONCEPT:
 *     Rust has two main string types:
 *         &str  — borrowed UTF-8 string slice
 *         String — owned, heap-allocated, growable UTF-8 buffer
 *     Indexing by *byte* offset is allowed only at character boundaries;
 *     for character access prefer .chars().nth(i) (which is O(i)).
 *
 * KEY POINTS:
 *     - Strings are UTF-8; .len() returns BYTES, not chars.
 *     - .chars() yields a char iterator; .bytes() yields u8 bytes.
 *     - .push_str / .push grow a String in O(1) amortised.
 *     - .replace returns a new String; in-place edit needs Vec<char>.
 *
 * ALGORITHM / APPROACH:
 *     Demonstrates: len, chars().nth, find, contains, to_lowercase,
 *     to_uppercase, replace, trim, split, building with String/push_str.
 *
 * RUST-SPECIFIC NOTES:
 *     - .find returns Option<usize>; pattern can be &str or |c| closure.
 *     - For repeated growth use String::with_capacity to preallocate.
 *     - To reverse a UTF-8 string: .chars().rev().collect::<String>().
 *
 * DRY RUN:
 *     s = "Hello, World!"
 *     len = 13 bytes (also 13 chars in this ASCII case)
 *     chars().nth(7) = Some('W')
 *     s[7..12] = "World"     (byte slice; valid here because ASCII)
 *
 * COMPLEXITY:
 *     Most APIs O(n) in input length; chars().nth(i) is O(i).
 */

fn main() {
    let s: &str = "Hello, World!";
    println!("String: {}", s);
    println!("len (bytes): {}", s.len());
    println!("char at 7: {:?}", s.chars().nth(7));      // Some('W')
    println!("byte slice s[7..12]: {}", &s[7..12]);     // "World"
    println!("find('o'): {:?}", s.find('o'));            // Some(4)
    println!("rfind('o'): {:?}", s.rfind('o'));          // Some(8)
    println!("contains(\"World\"): {}", s.contains("World"));
    println!("to_lowercase: {}", s.to_lowercase());
    println!("to_uppercase: {}", s.to_uppercase());
    println!("replace('l',\"r\"): {}", s.replace('l', "r"));
    println!("trim of \"  hello  \": \"{}\"", "  hello  ".trim());

    // --- Comparison ---
    let a: &str = "apple";
    let b: &str = "apple";
    let c: String = String::from("apple");
    println!("\n\"apple\" == \"apple\": {}", a == b);
    println!("\"apple\" == String(\"apple\"): {}", a == c);   // PartialEq compares text
    println!("\"apple\" < \"banana\": {}", "apple" < "banana");

    // --- Iterate chars ---
    print!("\nChars: ");
    for ch in s.chars() {
        print!("{} ", ch);
    }
    println!();

    // --- Split ---
    let csv = "one,two,three,four";
    println!("\nSplit by ',':");
    for token in csv.split(',') {
        println!("  {}", token);
    }

    // --- Build (StringBuilder equivalent) ---
    let mut built = String::with_capacity(16);
    for i in 1..=5 {
        built.push_str(&i.to_string());
        if i < 5 {
            built.push('-');
        }
    }
    println!("\nBuilt: {}", built);

    // --- Reverse ---
    let rev: String = "hello".chars().rev().collect();
    println!("Reversed 'hello': {}", rev);
}

/*
 * NOTES — Rust vs Java:
 *     - String/&str distinction enforces ownership: prefer &str for params.
 *     - .len() is bytes — for char count use .chars().count().
 *     - String is mutable and amortised O(1) for push/push_str.
 *     - PartialOrd on &str is lexicographic; PartialEq compares content.
 */
