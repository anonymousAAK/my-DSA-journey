# Dev Container / Codespaces

One-click development environment for `my-DSA-journey`. Provisions Python 3.12,
Java 21 (Temurin), Rust (stable), C++ via `g++`, and pandoc — everything needed
to build, test, and document the entire repo.

## One-click flow

### GitHub Codespaces (browser, zero install)

1. Open the repo on GitHub.
2. Click **Code → Codespaces → Create codespace on main**.
3. Wait ~2-3 minutes while the container builds and `postCreateCommand`
   installs `build-essential`, `g++`, `pandoc`, and `mkdocs-material`.
4. You land in a full VS Code session with all four languages ready.

### VS Code Dev Containers (local)

1. Install [VS Code](https://code.visualstudio.com/) +
   [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
2. `git clone` this repo and open it in VS Code.
3. Run **Dev Containers: Reopen in Container** from the command palette.

## What you get

| Component | Version | Source |
|-----------|---------|--------|
| Base OS | Ubuntu 22.04 | `mcr.microsoft.com/devcontainers/base` |
| Python | 3.12 | `features/python:1` |
| Java | 21 (Temurin) | `features/java:1` |
| Rust | stable | `features/rust:1` |
| C++ | g++ (apt) | `postCreateCommand` |
| pandoc | apt | `postCreateCommand` (for `scripts/build_book.sh`) |
| mkdocs-material | latest | `pip install -r requirements.txt` |

## Pre-installed VS Code extensions

- `redhat.java` + `vscjava.vscode-java-pack`
- `rust-lang.rust-analyzer`
- `ms-python.python`
- `ms-vscode.cpptools` + extension pack
- `vadimcn.vscode-lldb` (debugger)
- `yzhang.markdown-all-in-one`
- `streetsidesoftware.code-spell-checker`

## Common tasks inside the container

```bash
# Run the full smoke test (compiles every Java/Python/C++/Rust file)
./scripts/build_all.sh

# Per-week mastery quiz
./scripts/journey quiz 1

# Serve the docs site locally (port 8000 is auto-forwarded)
mkdocs serve

# Build the eBook
./scripts/build_book.sh
```

## Forwarded ports

- **8000** — `mkdocs serve` (announced automatically when started).
