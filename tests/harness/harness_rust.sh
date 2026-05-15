#!/usr/bin/env bash
# Rust harness — proof-of-concept for the kadane_max_subarray topic.
#
# We deliberately avoid Cargo + serde for the one-off scope. The shell
# wrapper translates the cases.json fixture into a simple CASE/INPUT/EXPECTED
# line format the Rust binary parses on stdin. The per-topic Rust source
# lives at tests/refs/<topic>.rs.
#
# Currently supports a single topic (kadane_max_subarray). Extending to the
# other 24 topics is mechanical: add a Rust source under tests/refs/, wire it
# into SUPPORTED_TOPICS, and write a matching emit_<topic> translator.
#
# Usage:
#     bash tests/harness/harness_rust.sh tests/cases/kadane_max_subarray.json
#     bash tests/harness/harness_rust.sh --all

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TESTS_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REFS_DIR="${TESTS_DIR}/refs"
CASES_DIR="${TESTS_DIR}/cases"
BUILD_DIR="${TMPDIR:-/tmp}/dsa-harness-rust"
mkdir -p "${BUILD_DIR}"

SUPPORTED_TOPICS=(kadane_max_subarray)

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
        echo "SKIP ${topic} :: no Rust driver yet (see tests/README.md)"
        return 0
    fi

    local src="${REFS_DIR}/${topic}.rs"
    local out="${BUILD_DIR}/${topic}"
    if [[ ! -f "${src}" ]]; then
        echo "FAIL ${topic} :: missing ${src}"
        return 1
    fi

    rustc --edition 2021 -O "${src}" -o "${out}" 2>/dev/null

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
