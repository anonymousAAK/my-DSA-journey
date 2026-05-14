"""
WEEK 1 - PYTHON FUNDAMENTALS
Topic: Python Installation & IDE Setup
File: 1.installation.py

CONCEPT:
Setting up the Python development environment. Unlike Java which needs the
JDK + an IDE, Python ships with both an interpreter and a standard REPL out
of the box on most operating systems.

KEY POINTS:
- Python interpreter (CPython) is downloaded from https://www.python.org/downloads/
- On macOS / Linux, Python 3 is usually pre-installed; check with `python3 --version`
- On Windows, tick "Add Python to PATH" during the installer wizard
- Recommended IDEs: VS Code (free, lightweight), PyCharm (full-featured)
- A virtual environment isolates project dependencies:
    python3 -m venv .venv
    source .venv/bin/activate          # macOS / Linux
    .venv\\Scripts\\activate            # Windows
- pip is the package manager: `pip install <package>`
- Run a script with: `python3 script.py`
- The interactive REPL is started with just `python3`

SYNTAX:
- File extension is `.py`
- No `class` wrapper required (unlike Java) — you can write code at module level
- Indentation defines code blocks (4 spaces by convention)

PYTHON-SPECIFIC NOTES vs Java:
- No JDK, no compilation step — Python is interpreted
- No `public static void main(String[] args)` ceremony — code runs top-to-bottom
- The convention `if __name__ == "__main__":` lets a file act as both
  an importable module and a runnable script
- No semicolons; one statement per line
- No `package` declaration; modules ARE files, packages ARE folders containing __init__.py

DRY RUN:
1. User installs Python 3.12 from python.org -> `python3 --version` prints "Python 3.12.x"
2. User creates `hello.py` with `print("Hi")` -> `python3 hello.py` prints "Hi"
"""

import sys
import platform


def show_environment() -> None:
    """Print details about the running Python interpreter."""
    print("=== Python Environment Check ===")
    print(f"Python version : {sys.version.split()[0]}")
    print(f"Implementation : {platform.python_implementation()}")
    print(f"Platform       : {platform.system()} {platform.release()}")
    print(f"Executable path: {sys.executable}")


def installation_checklist() -> list[str]:
    """Return the recommended install / setup steps."""
    return [
        "1. Download Python 3 from https://www.python.org/downloads/",
        "2. During install (Windows), tick 'Add Python to PATH'",
        "3. Verify with: python3 --version",
        "4. Install VS Code or PyCharm as your IDE",
        "5. (Optional) create a virtual env: python3 -m venv .venv",
        "6. Activate the venv and install packages with pip",
        "7. Write your first file: hello.py -> print('Hello, world!')",
        "8. Run it: python3 hello.py",
    ]


if __name__ == "__main__":
    show_environment()
    print("\n=== Setup Checklist ===")
    for step in installation_checklist():
        print(step)


# NOTES:
# - Python is dynamically typed and interpreted; Java is statically typed and compiled to bytecode.
# - Python uses indentation; Java uses braces {}.
# - Python's "main" guard is `if __name__ == "__main__":` instead of a `main` method.
# - Package management: pip + venv (Python) vs Maven/Gradle (Java).
# - No `import java.util.Scanner;` style boilerplate — `input()` is built in.
