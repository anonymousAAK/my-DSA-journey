# Building the eBook

`scripts/build_book.sh` compiles the curriculum's prose into a portable
PDF + ePub eBook for offline reading, Kindle/Kobo sideloading, or sharing.

## Run it

```bash
./scripts/build_book.sh
```

Output lands in `dist/` (gitignored):

```
dist/
├── dsa-journey.epub
└── dsa-journey.pdf
```

If `pandoc` is missing, the script prints install instructions and exits
cleanly (`exit 0`) without crashing. If pandoc is installed but no LaTeX
engine is available, the ePub still builds and the PDF step is skipped with
a warning.

## What's included

Chapters appear in this order:

1. **Front matter** — `README.md`, `PROBLEM_SOLVING.md`, `QUICKSTART.md`
2. **Mindset & methodology** — `docs/diagnostic.md`, `docs/SOLUTION_JOURNAL.md`,
   `docs/estimation.md`, `docs/REVIEW_SCHEDULE.md`, `docs/MASTERY.md`
3. **Curriculum** — `Week 1/README.md` through `Week 30/README.md`
4. **Case studies** — six phase walkthroughs, then the fifteen real-world
   essays under `case_studies/real_world/`
5. **Capstones** — six multi-weekend project specs

Excluded (intentionally — the eBook is *prose*, not code):

- `Week */java/`, `cpp/`, `python/`, `rust/` source trees
- `Week */web/` HTML pages
- `tests/`, `scripts/`, `mock_interviews/`
- Per-week `problems.md`, `patterns.md`, `challenges.md`, `mastery.yml`

## Dependencies

```bash
# Debian/Ubuntu
sudo apt-get install pandoc texlive-xetex

# macOS
brew install pandoc basictex

# Fedora
sudo dnf install pandoc texlive-scheme-basic
```

`pandoc` alone is enough for ePub. PDF needs a LaTeX engine — the script
auto-detects `xelatex`, `pdflatex`, `lualatex`, or `wkhtmltopdf` in that
order.

## Metadata

The generated book is tagged with:

- **Title:** My DSA Journey
- **Subtitle:** Beginner to Research-Advanced — 30 weeks, 4 languages
- **Author:** anonymousAAK and contributors
- **TOC:** auto-generated, depth 2

Edit `scripts/build_book.sh` to change these.
