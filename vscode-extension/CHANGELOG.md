# Changelog

All notable changes to the DSA Journey VS Code extension are recorded here.
Versions follow [Semantic Versioning](https://semver.org/).

## [0.1.0] — 2026-05-21

Initial scaffold release. Not yet published to the marketplace; install via
sideload (see `README.md`).

### Added

- `dsa-journey.openQuiz` — runs `./scripts/journey quiz <week>` for the
  currently active file's week in the integrated terminal.
- `dsa-journey.openChallenges` — opens the active week's `challenges.md`.
- `dsa-journey.openPatterns` — opens the active week's `patterns.md`.
- `dsa-journey.openTopicAcrossLanguages` — opens the equivalent topic file
  for the other four language tracks (Java, Python, C++, Rust, Web) in
  separate editor columns.
- `dsa-journey.runTests` — runs `python tests/harness/harness.py --all`
  in the integrated terminal.
- `dsa-journey.openIndex` — opens the top-level `INDEX.md`.
- Editor title-bar shortcut for "Open This Topic in All Languages" on
  `.java`, `.py`, `.cpp`, `.rs`, and `.html` files.
- Workspace activation on the presence of any `mastery.yml` file.
