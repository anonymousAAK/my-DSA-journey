#!/usr/bin/env bash
# C++ harness — proof-of-concept for the kadane_max_subarray topic.
#
# Pattern: this shell wrapper handles JSON parsing (via python3, which is
# already required by the Python harness) and feeds a simple line-based
# format into a tiny per-topic C++ binary. That keeps the C++ side free of
# any JSON dependency while reusing the canonical cases.json fixtures.
#
# Currently supports a single topic (kadane_max_subarray) as the foundation
# pattern. Extending to the other 24 topics is mechanical: write a new
# tests/refs/<topic>.cpp with a function-under-test + matching line parser,
# update SUPPORTED_TOPICS and emit_cases() below.
#
# Usage:
#     bash tests/harness/harness_cpp.sh tests/cases/kadane_max_subarray.json
#     bash tests/harness/harness_cpp.sh --all

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REFS_DIR="${TESTS_DIR}/refs"
CASES_DIR="${TESTS_DIR}/cases"
BUILD_DIR="${TMPDIR:-/tmp}/dsa-harness-cpp"
mkdir -p "${BUILD_DIR}"

SUPPORTED_TOPICS=(kadane_max_subarray)

# Translate the kadane fixture into the CASE / INPUT / EXPECTED line format
# the C++ binary expects. Each topic gets its own translator.
emit_kadane () {
    python3 - "$1" <<'PY'
import json, sys
data = json.load(open(sys.argv[1]))
for c in data["cases"]:
    if c.get("skip"): continue
    arr = c["input"][0]
    print(f"CASE {c['name']}")
    print("INPUT " + " ".join(str(x) for x in arr))
    print(f"EXPECTED {c['expected']}")
    print()
PY
}

run_one () {
    local fixture_path="$1"
    local topic
    topic="$(basename "${fixture_path}" .json)"

    local supported=0
    for t in "${SUPPORTED_TOPICS[@]}"; do
        [[ "${t}" == "${topic}" ]] && supported=1
    done
    if [[ "${supported}" -eq 0 ]]; then
        echo "SKIP ${topic} :: no C++ driver yet (see tests/README.md)"
        return 0
    fi

    local src="${REFS_DIR}/${topic}.cpp"
    local out="${BUILD_DIR}/${topic}.out"
    if [[ ! -f "${src}" ]]; then
        echo "FAIL ${topic} :: missing ${src}"
        return 1
    fi

    g++ -std=c++17 -O2 -Wall -Wextra "${src}" -o "${out}"

    case "${topic}" in
        kadane_max_subarray) emit_kadane "${fixture_path}" | "${out}" ;;
        *) echo "FAIL ${topic} :: no emitter wired"; return 1 ;;
    esac
}

if [[ "${1:-}" == "--all" ]]; then
    rc=0
    for f in "${CASES_DIR}"/*.json; do
        run_one "${f}" || rc=$?
    done
    exit "${rc}"
fi

run_one "${1:-${CASES_DIR}/kadane_max_subarray.json}"
