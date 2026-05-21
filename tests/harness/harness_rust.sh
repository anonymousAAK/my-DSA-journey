#!/usr/bin/env bash
# Rust harness — dispatches per-topic to a tiny stdin-driven Rust binary.
#
# Pattern mirrors harness_cpp.sh: this shell wrapper handles JSON parsing (via
# tests/harness/emit_lines.py) and emits a simple line-based format that the
# per-topic Rust binary reads on stdin.
#
# Each topic's driver lives at tests/refs/<topic>.rs.
#
# Usage:
#     bash tests/harness/harness_rust.sh tests/cases/<topic>.json
#     bash tests/harness/harness_rust.sh --all

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REFS_DIR="${TESTS_DIR}/refs"
CASES_DIR="${TESTS_DIR}/cases"
EMITTER="${SCRIPT_DIR}/emit_lines.py"
BUILD_DIR="${TMPDIR:-/tmp}/dsa-harness-rust"
mkdir -p "${BUILD_DIR}"

run_one () {
    local fixture_path="$1"
    local topic
    topic="$(basename "${fixture_path}" .json)"

    local src="${REFS_DIR}/${topic}.rs"
    local out="${BUILD_DIR}/${topic}"
    if [[ ! -f "${src}" ]]; then
        echo "SKIP ${topic} :: no Rust driver yet"
        return 0
    fi

    rustc --edition 2021 -O "${src}" -o "${out}" 2>/dev/null
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
