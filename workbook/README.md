# Workbook — YOUR space

This directory is where you write code while learning. It's intentionally gitignored — your in-progress attempts don't belong in the upstream repo.

## How it gets populated

The `./scripts/journey` CLI writes here:

- `./scripts/journey new-attempt kadane` → creates `workbook/week_06/attempts/kadane__2026-05-21.py` with a function stub for you to fill in.
- `./scripts/journey reflect` → appends today's reflection prompts to `workbook/week_06/journal.md`.
- `./scripts/journey verify kadane workbook/week_06/attempts/kadane__2026-05-21.py` → runs YOUR code against the topic's fixtures.

## Layout

```
workbook/
├── README.md           # this file (NOT gitignored)
├── week_01/
│   ├── attempts/       # one file per topic per attempt-date
│   ├── journal.md      # your reflection entries
│   └── notes.md        # your freeform notes
├── week_02/
├── ...
└── week_30/
```

## The point

Reading the canonical solutions teaches you what good code looks like. Writing your OWN code first, then comparing, teaches you DSA. The repo gives you the canonical for reference; the workbook gives you a place to fail safely before peeking.

## Sharing

By default, nothing in `workbook/` is tracked by git. If you want to share a finished capstone or a clever solution, copy it to `showcase/submissions/<your-handle>-<topic>.md` and open a PR. See `showcase/README.md` for the format.
