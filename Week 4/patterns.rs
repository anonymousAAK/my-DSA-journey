//! WEEK 4 — Rust: Pattern Printing
//! Master nested loops with various patterns. Rust uses print!/println! macros.

fn right_triangle_stars(n: usize) {
    for i in 1..=n {
        for _ in 0..i { print!("* "); }
        println!();
    }
}

fn inverted_triangle(n: usize) {
    for i in (1..=n).rev() {
        for _ in 0..i { print!("* "); }
        println!();
    }
}

fn pyramid(n: usize) {
    for i in 1..=n {
        print!("{}", " ".repeat(n - i));
        for _ in 0..i { print!("* "); }
        println!();
    }
}

fn diamond(n: usize) {
    for i in 1..=n {
        print!("{}", " ".repeat(n - i));
        for _ in 0..i { print!("* "); }
        println!();
    }
    for i in (1..n).rev() {
        print!("{}", " ".repeat(n - i));
        for _ in 0..i { print!("* "); }
        println!();
    }
}

fn number_pyramid(n: usize) {
    for i in 1..=n {
        print!("{}", " ".repeat(n - i));
        for j in 1..=i { print!("{} ", j); }
        println!();
    }
}

fn alphabet_triangle(n: usize) {
    for i in 0..n {
        let ch = (b'A' + i as u8) as char;
        for _ in 0..=i { print!("{} ", ch); }
        println!();
    }
}

fn floyds_triangle(n: usize) {
    let mut num = 1;
    for i in 1..=n {
        for _ in 0..i {
            print!("{} ", num);
            num += 1;
        }
        println!();
    }
}

fn butterfly(n: usize) {
    for i in 1..=n {
        for _ in 0..i { print!("* "); }
        for _ in 0..2*(n-i) { print!("  "); }
        for _ in 0..i { print!("* "); }
        println!();
    }
    for i in (1..=n).rev() {
        for _ in 0..i { print!("* "); }
        for _ in 0..2*(n-i) { print!("  "); }
        for _ in 0..i { print!("* "); }
        println!();
    }
}

fn hollow_rectangle(rows: usize, cols: usize) {
    for i in 0..rows {
        for j in 0..cols {
            if i == 0 || i == rows-1 || j == 0 || j == cols-1 {
                print!("* ");
            } else {
                print!("  ");
            }
        }
        println!();
    }
}

fn main() {
    let n = 5;

    println!("=== Right Triangle ===");
    right_triangle_stars(n);

    println!("\n=== Inverted Triangle ===");
    inverted_triangle(n);

    println!("\n=== Pyramid ===");
    pyramid(n);

    println!("\n=== Diamond ===");
    diamond(n);

    println!("\n=== Number Pyramid ===");
    number_pyramid(n);

    println!("\n=== Alphabet Triangle ===");
    alphabet_triangle(n);

    println!("\n=== Floyd's Triangle ===");
    floyds_triangle(n);

    println!("\n=== Butterfly ===");
    butterfly(4);

    println!("\n=== Hollow Rectangle 4x6 ===");
    hollow_rectangle(4, 6);

    // Rust-specific: using iterators for a compact pattern
    println!("\n=== Compact Triangle (Rust iterator style) ===");
    for i in 1..=5 {
        println!("{}", "* ".repeat(i));
    }
}
