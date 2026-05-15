#!/usr/bin/env bash
# Local smoke test: compile every file in every language.
# Usage: ./scripts/build_all.sh [python|cpp|rust|java|all]
set -e
LANG="${1:-all}"

run_python() { find "Week "* -maxdepth 2 -name "*.py" -print0 | xargs -0 -n1 python3 -m py_compile; echo "Python OK"; }
run_cpp()    { while IFS= read -r -d '' f; do g++ -std=c++17 -w "$f" -o /tmp/a.out || { echo "FAIL $f"; exit 1; }; done < <(find "Week "* -maxdepth 2 -name "*.cpp" -print0); echo "C++ OK"; }
run_rust()   { while IFS= read -r -d '' f; do base=$(basename "$f" .rs); crate=$(echo "$base" | tr -c 'A-Za-z0-9_' '_' | sed 's/^[0-9]/c&/'); rustc --edition 2021 --crate-name "$crate" "$f" -o /tmp/$crate || { echo "FAIL $f"; exit 1; }; done < <(find "Week "* -maxdepth 2 -name "*.rs" -print0); echo "Rust OK"; }
run_java()   { mkdir -p /tmp/java-out; while IFS= read -r -d '' f; do if grep -qxF "$f" .ci-skip-java 2>/dev/null; then continue; fi; javac -d /tmp/java-out "$f" || { echo "FAIL $f"; exit 1; }; done < <(find "Week "* -maxdepth 2 -name "*.java" -print0); echo "Java OK"; }

case "$LANG" in
  python) run_python;;
  cpp)    run_cpp;;
  rust)   run_rust;;
  java)   run_java;;
  all)    run_python; run_cpp; run_rust; run_java;;
  *) echo "Usage: $0 [python|cpp|rust|java|all]"; exit 2;;
esac
