/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: C++ Installation & IDE Setup
 * File: 1.installation.cpp
 *
 * CONCEPT:
 * Setting up a C++ toolchain. Unlike Java (which bundles JDK + JRE) C++
 * needs you to install a COMPILER (g++, clang++, MSVC) and optionally an
 * IDE/build system (VS Code + CMake, CLion, Visual Studio).
 *
 * KEY POINTS:
 *  - macOS:    `xcode-select --install`  (provides clang++)
 *  - Linux:    `sudo apt install build-essential`  (g++)
 *  - Windows:  Install MSYS2 + MinGW-w64, OR Visual Studio with C++ workload
 *  - Verify with: `g++ --version` or `clang++ --version`
 *  - Compile a single file:  g++ -std=c++17 -Wall -O2 hello.cpp -o hello
 *  - Run the produced binary: ./hello   (or hello.exe on Windows)
 *
 * SYNTAX:
 *  #include <iostream>           // standard I/O streams
 *  int main() { ... return 0; }   // entry point; returns int (0 = success)
 *
 * C++-SPECIFIC NOTES vs Java:
 *  - C++ is COMPILED to native code; Java compiles to JVM bytecode.
 *  - There is no `package` declaration; namespaces (`namespace foo {}`) play
 *    a similar role.
 *  - Header (.h/.hpp) files declare; source (.cpp) files define.
 *  - `main` is a free function — there is no enclosing class as in Java.
 *
 * DRY RUN:
 *  1. Install g++ -> `g++ --version` prints "g++ (Ubuntu 13.x.x)..."
 *  2. Save this file as 1.installation.cpp -> compile with
 *       g++ -std=c++17 1.installation.cpp -o setup
 *     and run `./setup` to print the environment summary below.
 *
 * COMPLEXITY: N/A (informational program).
 */

#include <iostream>
#include <vector>
#include <string>

int main() {
    std::cout << "=== C++ Environment Check ===\n";

#ifdef __clang__
    std::cout << "Compiler        : clang++ "
              << __clang_major__ << "." << __clang_minor__ << "\n";
#elif defined(__GNUC__)
    std::cout << "Compiler        : g++ "
              << __GNUC__ << "." << __GNUC_MINOR__ << "\n";
#elif defined(_MSC_VER)
    std::cout << "Compiler        : MSVC " << _MSC_VER << "\n";
#else
    std::cout << "Compiler        : unknown\n";
#endif

    std::cout << "C++ standard    : " << __cplusplus << "  (e.g. 201703 = C++17)\n";

    std::cout << "\n=== Setup Checklist ===\n";
    const std::vector<std::string> steps = {
        "1. Install a C++ compiler (g++ on Linux, clang++ on macOS, MSVC on Windows).",
        "2. Verify with: g++ --version  OR  clang++ --version",
        "3. Choose an IDE: VS Code + C/C++ extension, CLion, or Visual Studio.",
        "4. Optional: install CMake for cross-platform builds.",
        "5. Compile a hello.cpp:  g++ -std=c++17 -Wall hello.cpp -o hello",
        "6. Run:  ./hello",
    };
    for (const auto& step : steps) std::cout << step << '\n';

    return 0;
}

/*
 * NOTES:
 *  - Java is compile-once-run-anywhere on the JVM; C++ binaries are platform-
 *    specific (recompile per OS / architecture).
 *  - Java has automatic memory management (GC); C++ uses RAII + smart pointers.
 *  - Java's `System.out.println` -> C++'s `std::cout << ... << std::endl`.
 *  - C++ supports both procedural and OO styles; main() does not need a class.
 *  - Conditional compilation via `#ifdef __clang__` / `__GNUC__` / `_MSC_VER`
 *    is the C++ way to detect compiler — Java has no equivalent.
 */
