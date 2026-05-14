//! WEEK 1 — Rust Fundamentals
//! Equivalent to Java Week 1: hello world, variables, data types, operators, I/O.
//!
//! Rust is statically typed, compiled, with guaranteed memory safety (no GC).
//! Key concepts: ownership, borrowing, lifetimes — these make Rust unique.
//!
//! Compile: rustc fundamentals.rs
//! Run:     ./fundamentals

use std::io;

fn main() {
    // --- Hello World ---
    println!("Hello, World!");

    // --- Variables ---
    // In Rust, variables are IMMUTABLE by default. Use `mut` for mutability.
    let name = "Alice";             // &str (string slice — immutable, stack-allocated)
    let mut age = 25;               // i32 (mutable — can be changed)
    let height: f64 = 5.9;         // explicit type annotation
    let is_student = true;          // bool
    let grade = 'A';                // char (4 bytes — Unicode scalar value!)

    println!("Name: {}, Age: {}, Height: {}, Grade: {}", name, age, height, grade);

    age += 1; // allowed because age is `mut`
    println!("Next year, age = {}", age);

    // Shadowing: re-declare a variable with the same name (even with different type)
    let x = 5;
    let x = x + 1;       // shadows previous x
    let x = x * 2;       // shadows again
    println!("Shadowed x = {}", x); // 12

    // --- Data Types ---
    println!("\n--- Data Types ---");
    println!("i8 range:   [{}, {}]", i8::MIN, i8::MAX);
    println!("i16 range:  [{}, {}]", i16::MIN, i16::MAX);
    println!("i32 range:  [{}, {}]", i32::MIN, i32::MAX);
    println!("i64 range:  [{}, {}]", i64::MIN, i64::MAX);
    println!("i128 range: [{}, {}]", i128::MIN, i128::MAX);
    println!("u8 range:   [0, {}]", u8::MAX);
    println!("u64 range:  [0, {}]", u64::MAX);
    println!("f32 max:    {}", f32::MAX);
    println!("f64 max:    {}", f64::MAX);
    println!("usize size: {} bytes (pointer-sized)", std::mem::size_of::<usize>());

    // Type sizes
    println!("\n--- Type Sizes ---");
    println!("i32:    {} bytes", std::mem::size_of::<i32>());
    println!("i64:    {} bytes", std::mem::size_of::<i64>());
    println!("f64:    {} bytes", std::mem::size_of::<f64>());
    println!("char:   {} bytes", std::mem::size_of::<char>()); // 4 bytes! (Unicode)
    println!("bool:   {} byte",  std::mem::size_of::<bool>());
    println!("String: {} bytes (on stack)", std::mem::size_of::<String>());

    // --- Type Casting ---
    let pi: f64 = 3.14159;
    let truncated = pi as i32;       // 3 (truncation, not rounding)
    let promoted = 25_i32 as f64;    // 25.0
    println!("\n--- Type Casting ---");
    println!("3.14159 as i32 = {}", truncated);
    println!("25_i32 as f64  = {}", promoted);
    println!("5 / 2   = {} (integer division)", 5 / 2);
    println!("5.0 / 2.0 = {} (float division)", 5.0_f64 / 2.0);

    // --- Arithmetic Operators ---
    let a = 17_i32;
    let b = 5_i32;
    println!("\n--- Arithmetic ({} and {}) ---", a, b);
    println!("a + b  = {}", a + b);   // 22
    println!("a - b  = {}", a - b);   // 12
    println!("a * b  = {}", a * b);   // 85
    println!("a / b  = {}", a / b);   // 3 (integer division)
    println!("a % b  = {}", a % b);   // 2
    // Rust has no ** operator; use .pow() or f64::powi()
    println!("a^b    = {}", (a as f64).powi(b)); // 1419857

    // --- Comparison & Logical ---
    println!("\n--- Comparison ---");
    println!("5 == 5: {}", 5 == 5);
    println!("5 != 3: {}", 5 != 3);
    println!("5 > 3:  {}", 5 > 3);

    println!("\n--- Logical ---");
    println!("true && false: {}", true && false);
    println!("true || false: {}", true || false);
    println!("!true:         {}", !true);

    // --- Bitwise ---
    println!("\n--- Bitwise ---");
    println!("5 & 3  = {}", 5 & 3);    // 1
    println!("5 | 3  = {}", 5 | 3);    // 7
    println!("5 ^ 3  = {}", 5 ^ 3);    // 6
    println!("!5     = {}", !5_i32);    // -6 (bitwise NOT)
    println!("5 << 1 = {}", 5 << 1);   // 10
    println!("5 >> 1 = {}", 5 >> 1);   // 2

    // --- User Input ---
    println!("\n--- Input ---");
    println!("Enter a number:");
    let mut input = String::new();
    match io::stdin().read_line(&mut input) {
        Ok(_) => {
            match input.trim().parse::<i32>() {
                Ok(num) => println!("Double of {} is {}", num, num * 2),
                Err(_) => println!("(Could not parse as number)"),
            }
        }
        Err(_) => println!("(No input available)"),
    }

    // --- Strings ---
    // Rust has TWO string types:
    // &str  — string slice (immutable reference, like viewing a portion of data)
    // String — heap-allocated, growable, owned string
    let s: &str = "Hello, Rust!";       // string literal (on stack, immutable)
    let mut owned = String::from(s);    // owned String (on heap, mutable)

    println!("\n--- String Operations ---");
    println!("String:    {}", s);
    println!("Length:    {}", s.len());        // bytes, not chars!
    println!("Chars:     {}", s.chars().count()); // actual character count
    println!("Contains:  {}", s.contains("Rust"));
    println!("Uppercase: {}", s.to_uppercase());
    println!("Lowercase: {}", s.to_lowercase());

    owned.push_str(" Welcome!");
    println!("Appended:  {}", owned);

    // Reverse
    let reversed: String = s.chars().rev().collect();
    println!("Reversed:  {}", reversed);

    // --- Ownership & Borrowing (Rust's unique feature) ---
    println!("\n--- Ownership ---");
    let s1 = String::from("hello");
    let s2 = s1;        // s1 is MOVED to s2 — s1 is no longer valid!
    // println!("{}", s1); // ERROR: value used after move
    println!("s2 = {}", s2);

    let s3 = s2.clone(); // explicit deep copy
    println!("s2 = {}, s3 = {}", s2, s3); // both valid

    // Borrowing: pass references instead of transferring ownership
    let s4 = String::from("world");
    print_length(&s4);    // borrow s4 (immutable reference)
    println!("s4 still valid: {}", s4); // s4 is still ours

    // --- Arrays & Vectors ---
    let arr = [10, 20, 30, 40, 50]; // fixed-size array
    let mut vec = vec![1, 2, 3, 4, 5]; // growable vector (like ArrayList)

    println!("\n--- Arrays & Vectors ---");
    print!("Array: ");
    for x in &arr { print!("{} ", x); }
    println!();

    vec.push(6);
    println!("Vector after push: {:?}", vec);
    println!("vec[0] = {}", vec[0]);
    println!("vec.len() = {}", vec.len());
}

/// Borrows a String reference — doesn't take ownership
fn print_length(s: &String) {
    println!("Length of '{}' is {}", s, s.len());
}
