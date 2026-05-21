#!/usr/bin/env bash
# Build a site_src/ tree that mkdocs can use as docs_dir.
#
# mkdocs requires docs_dir to be a child directory of where mkdocs.yml lives,
# so we can't point it at the repo root directly. This script creates a
# site_src/ directory and symlinks every file/folder referenced from the
# mkdocs.yml nav: section so the live markdown is the same source of truth
# without duplicating content into git.
#
# Re-runnable: blows away site_src/ at the start.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

dest=site_src
rm -rf "$dest"
mkdir -p "$dest"

# --- Top-level docs ---
ln -sf "../README.md"           "$dest/README.md"
ln -sf "../PROBLEM_SOLVING.md"  "$dest/PROBLEM_SOLVING.md"
ln -sf "../QUICKSTART.md"       "$dest/QUICKSTART.md"
ln -sf "../INDEX.md"            "$dest/INDEX.md"
ln -sf "../CONTRIBUTING.md"     "$dest/CONTRIBUTING.md"

# --- docs/ folder (already a subdir; symlink in full) ---
ln -sf "../docs"                "$dest/docs"

# --- Per-week READMEs ---
# We only want each Week's README.md, not the code subfolders.
for i in $(seq 1 30); do
    week="Week $i"
    if [ -f "$week/README.md" ]; then
        mkdir -p "$dest/$week"
        ln -sf "../../$week/README.md" "$dest/$week/README.md"
    fi
done

# --- case_studies/, capstones/, mock_interviews/, showcase/, viz/ etc. ---
# These are pure markdown trees we want rendered as-is.
for d in case_studies capstones mock_interviews showcase mentors translations competitions audio video; do
    if [ -d "$d" ]; then
        ln -sf "../$d" "$dest/$d"
    fi
done

# --- Convenience: also expose top-level WEEKLY.md if it exists ---
if [ -f "WEEKLY.md" ]; then
    ln -sf "../WEEKLY.md" "$dest/WEEKLY.md"
fi

echo "site_src/ prepared with $(find "$dest" -maxdepth 1 | wc -l) top-level entries."
