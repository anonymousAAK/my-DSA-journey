# Building the static site

The repo doubles as a [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
site. All curriculum prose (README, mindset docs, week READMEs, case studies,
capstones) is rendered straight from the repo root — no content duplication.

## Local preview

```bash
pip install -r requirements.txt
mkdocs serve
```

Then open <http://127.0.0.1:8000/>. Pages live-reload as you edit markdown.

## One-shot build

```bash
mkdocs build --strict
```

Output goes to `site/` (gitignored). `--strict` turns broken links and missing
nav targets into errors — keep it green.

## Deployment

`.github/workflows/site.yml` builds on every push to `main` and deploys to
GitHub Pages via the official `actions/deploy-pages@v4` flow. Enable Pages
under *Settings → Pages → Source: GitHub Actions* once, and every subsequent
push publishes automatically.

## How content is organized

- `mkdocs.yml` uses `docs_dir: .` so the repository root *is* the docs source.
- `exclude_docs:` filters out code folders (`Week */java/`, `cpp/`, `python/`,
  `rust/`, `web/`), test fixtures, and build artifacts.
- The `nav:` block groups pages into: **Start Here, Mindset, Curriculum
  (Phases 1-6, Weeks 1-30), Real-world, Capstones, Reference, Contributing**.
- The dark palette in `docs/assets/theme.css` matches the existing per-week
  `web/index.html` pages (`#0d1117`, `#161b22`, `#58a6ff`, `#3fb950`).

## Optional plugins

These plugins are NOT installed by default to keep the dependency footprint
small. Install them yourself if you want the extra features:

```bash
pip install mkdocs-awesome-pages-plugin            # nav from .pages files
pip install mkdocs-git-revision-date-localized-plugin  # "last updated" dates
pip install mkdocs-minify-plugin                   # smaller HTML output
```

Then add the plugin name under the `plugins:` key in `mkdocs.yml`.
