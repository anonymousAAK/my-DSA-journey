/*
 * WEEK 1 - RUST FUNDAMENTALS
 * Topic: Rust Installation & Toolchain Setup
 * File: 1.installation.rs
 *
 * CONCEPT:
 * Rust is installed via `rustup`, the official toolchain manager. `rustup`
 * pulls down `rustc` (compiler), `cargo` (build tool + package manager),
 * `rustfmt` (formatter), and `clippy` (linter) in one step.
 *
 * KEY POINTS:
 *  - One-liner install: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
 *  - Verify with: `rustc --version`, `cargo --version`
 *  - Update toolchain: `rustup update`
 *  - Create a project:  `cargo new hello`
 *  - Build:             `cargo build`
 *  - Run:               `cargo run`
 *  - Check (no codegen): `cargo check`   (fast feedback loop)
 *  - Test:              `cargo test`
 *  - Format:            `cargo fmt`
 *  - Lint:              `cargo clippy`
 *  - For a single file: `rustc 1.installation.rs && ./1.installation`
 *
 * SYNTAX:
 *  fn main() { ... }                  // entry point; takes no args
 *  println!("...")                     // macro (note the `!`)
 *
 * RUST-SPECIFIC NOTES vs Java:
 *  - Compiled to native code (like C++); no VM.
 *  - Memory safety enforced at COMPILE time via the borrow checker — no GC.
 *  - Macros end with `!` (e.g. `println!`, `vec!`).
 *  - Cargo handles dependencies (similar to Maven/Gradle for Java).
 *
 * DRY RUN:
 *  After `rustup install`, run `cargo new myapp && cd myapp && cargo run`
 *  -> prints "Hello, world!" using the auto-generated `src/main.rs`.
 *
 * COMPLEXITY: N/A.
 */

fn main() {
    println!("=== Rust Environment Check ===");
    // option_env! returns Option<&'static str> at compile time
    let pkg = option_env!("CARGO_PKG_NAME").unwrap_or("n/a (single-file build)");
    println!("cargo package: {}", pkg);
    println!("(run `rustc --version` to inspect compiler version)");

    println!();
    println!("=== Setup Checklist ===");
    let steps = [
        "1. Install rustup from https://rustup.rs/",
        "2. Verify: rustc --version  &&  cargo --version",
        "3. Add an editor/IDE: VS Code + rust-analyzer extension",
        "4. Create a project: cargo new myapp",
        "5. Run it:           cargo run",
        "6. Format / lint:    cargo fmt && cargo clippy",
        "7. Single-file mode: rustc file.rs && ./file",
    ];
    for s in steps.iter() {
        println!("{}", s);
    }
}

/*
 * NOTES:
 *  - Java needs JDK + IDE; Rust bundles the toolchain via rustup.
 *  - Java compiles to bytecode for the JVM; Rust compiles to a native binary.
 *  - Rust's Cargo is closest to Node's npm or Python's pip+setuptools — built in.
 *  - Macros (`println!`) look like functions but expand at compile time.
 *  - `env!()` reads compile-time env vars — used here just to demo macro use.
 */
