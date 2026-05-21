#!/usr/bin/env bash
# C++ harness — dispatches per-topic to a tiny stdin-driven C++ driver.
#
# Pattern: this shell wrapper handles JSON parsing (via tests/harness/emit_lines.py)
# and emits a simple line-based format that the per-topic C++ binary reads on
# stdin. That keeps the C++ side free of any JSON dependency while reusing the
# canonical tests/cases/*.json fixtures.
#
# Each topic's driver lives at tests/refs/<topic>.cpp. The emitter (shared with
# the Rust harness) is in tests/harness/emit_lines.py.
#
# Usage:
#     bash tests/harness/harness_cpp.sh tests/cases/<topic>.json
#     bash tests/harness/harness_cpp.sh --all

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REFS_DIR="${TESTS_DIR}/refs"
CASES_DIR="${TESTS_DIR}/cases"
EMITTER="${SCRIPT_DIR}/emit_lines.py"
BUILD_DIR="${TMPDIR:-/tmp}/dsa-harness-cpp"
mkdir -p "${BUILD_DIR}"

run_one () {
    local fixture_path="$1"
    local topic
    topic="$(basename "${fixture_path}" .json)"

    local src="${REFS_DIR}/${topic}.cpp"
    local out="${BUILD_DIR}/${topic}.out"
    if [[ ! -f "${src}" ]]; then
        echo "SKIP ${topic} :: no C++ driver yet"
        return 0
    fi

    g++ -std=c++17 -O2 -Wall -Wextra "${src}" -o "${out}"
    python3 "${EMITTER}" "${topic}" "${fixture_path}" | "${out}"
}

if [[ "${1:-}" == "--all" ]]; then
    rc=0
    for f in "${CASES_DIR}"/*.json; do
        run_one "${f}" || rc=$?
    done
    exit "${rc}"
fi

run_one "${1:-${CASES_DIR}/kadane_max_subarray.json}"
