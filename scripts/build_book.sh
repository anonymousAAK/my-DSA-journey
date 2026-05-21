#!/usr/bin/env bash
# build_book.sh — compile the repo's prose markdown into a PDF + ePub eBook.
#
# Includes:  README.md, PROBLEM_SOLVING.md, QUICKSTART.md, docs/*.md,
#            each Week N/README.md (in order), case_studies/*, capstones/*.
# Excludes:  all source code (java/cpp/python/rust), tests, scripts, web/.
#
# Usage:     ./scripts/build_book.sh
# Output:    dist/dsa-journey.pdf
#            dist/dsa-journey.epub

set -euo pipefail

# Resolve repo root regardless of where the script is invoked from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

# --- Tool check -------------------------------------------------------------
if ! command -v pandoc >/dev/null 2>&1; then
  cat <<'EOF'
pandoc is not installed. To build the eBook, install pandoc:

  Debian/Ubuntu:   sudo apt-get install pandoc texlive-xetex
  macOS (brew):    brew install pandoc basictex
  Fedora:          sudo dnf install pandoc texlive-scheme-basic
  Windows (choco): choco install pandoc miktex
  Or download:     https://pandoc.org/installing.html

For PDF output you also need a LaTeX engine (xelatex/pdflatex/wkhtmltopdf).
ePub output works with pandoc alone.

Skipping eBook build (exit 0).
EOF
  exit 0
fi

OUT_DIR="$REPO_ROOT/dist"
mkdir -p "$OUT_DIR"

PDF_OUT="$OUT_DIR/dsa-journey.pdf"
EPUB_OUT="$OUT_DIR/dsa-journey.epub"

# --- Assemble the ordered file list -----------------------------------------
# Use a bash array so paths with spaces (e.g. "Week 1/README.md") survive.
FILES=()

# 1. Front matter: top-level prose.
[[ -f "README.md" ]]          && FILES+=("README.md")
[[ -f "PROBLEM_SOLVING.md" ]] && FILES+=("PROBLEM_SOLVING.md")
[[ -f "QUICKSTART.md" ]]      && FILES+=("QUICKSTART.md")

# 2. Mindset / methodology docs.
for f in docs/diagnostic.md \
         docs/SOLUTION_JOURNAL.md \
         docs/estimation.md \
         docs/REVIEW_SCHEDULE.md \
         docs/MASTERY.md; do
  [[ -f "$f" ]] && FILES+=("$f")
done

# 3. Curriculum: each Week N/README.md in numeric order (1..30).
for n in $(seq 1 30); do
  f="Week ${n}/README.md"
  [[ -f "$f" ]] && FILES+=("$f")
done

# 4. Case studies — phase walkthroughs, then real-world essays.
for f in case_studies/phase_1_foundations.md \
         case_studies/phase_2_arrays_strings.md \
         case_studies/phase_3_structures.md \
         case_studies/phase_4_graphs_dp.md \
         case_studies/phase_5_advanced.md \
         case_studies/phase_6_systems.md; do
  [[ -f "$f" ]] && FILES+=("$f")
done

if [[ -d case_studies/real_world ]]; then
  while IFS= read -r -d '' f; do
    FILES+=("$f")
  done < <(find case_studies/real_world -maxdepth 1 -name '*.md' -print0 | sort -z)
fi

# 5. Capstones.
if [[ -d capstones ]]; then
  while IFS= read -r -d '' f; do
    FILES+=("$f")
  done < <(find capstones -maxdepth 1 -name '*.md' -print0 | sort -z)
fi

echo "Building eBook from ${#FILES[@]} markdown files..."

# --- Common pandoc options --------------------------------------------------
COMMON_OPTS=(
  --from=gfm+yaml_metadata_block+pipe_tables+task_lists
  --toc
  --toc-depth=2
  --metadata title="My DSA Journey"
  --metadata subtitle="Beginner to Research-Advanced — 30 weeks, 4 languages"
  --metadata author="anonymousAAK and contributors"
  --metadata lang=en
)

# --- ePub -------------------------------------------------------------------
echo "  -> ePub: $EPUB_OUT"
pandoc "${COMMON_OPTS[@]}" \
  -o "$EPUB_OUT" \
  "${FILES[@]}"

# --- PDF --------------------------------------------------------------------
# Pick the first LaTeX engine that's available; fall back to wkhtmltopdf.
PDF_ENGINE=""
for eng in xelatex pdflatex lualatex wkhtmltopdf; do
  if command -v "$eng" >/dev/null 2>&1; then
    PDF_ENGINE="$eng"
    break
  fi
done

if [[ -z "$PDF_ENGINE" ]]; then
  echo "  -> PDF: skipped (no LaTeX engine or wkhtmltopdf found)."
  echo "         Install one of: texlive-xetex, basictex, wkhtmltopdf."
else
  echo "  -> PDF: $PDF_OUT  (engine: $PDF_ENGINE)"
  pandoc "${COMMON_OPTS[@]}" \
    --pdf-engine="$PDF_ENGINE" \
    -V geometry:margin=1in \
    -V mainfont="DejaVu Sans" \
    -V monofont="DejaVu Sans Mono" \
    -V colorlinks=true \
    -V linkcolor=blue \
    -o "$PDF_OUT" \
    "${FILES[@]}" || {
      echo "  !! PDF build failed (likely missing fonts/packages)." >&2
      echo "     ePub is still available at $EPUB_OUT" >&2
      exit 1
    }
fi

echo
echo "Done. Artifacts:"
ls -lh "$OUT_DIR"
