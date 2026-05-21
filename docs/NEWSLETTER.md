# Weekly Digest — Newsletter

The repo publishes a tiny weekly digest every Monday at 09:00 UTC. One case study, one pattern drill, one hard-mode challenge. Nothing more. The intent is to keep you in light contact with the material even on weeks when you can't sit down for a full session.

---

## How to subscribe

Point any RSS reader (Feedly, NetNewsWire, Reeder, Miniflux, Thunderbird, ...) at:

```
https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml
```

You'll get a new item every Monday morning. The feed keeps up to 52 history entries (one year), so newcomers see the most recent year of digests on first sync.

If you don't use an RSS reader, you can also:

- Star the repo and watch the `main` branch for `WEEKLY.md` updates.
- Bookmark [`WEEKLY.md`](../WEEKLY.md) and visit it on Mondays.
- Subscribe to GitHub Actions notifications for the `Weekly Digest` workflow.

---

## What's in each digest

Every issue has three sections:

1. **Case study** — one entry from [`case_studies/real_world/`](../case_studies/real_world/). These are short essays on how named companies use a specific algorithm. The digest shows the title plus the first paragraph; click through for the full essay.

2. **Pattern drill** — one prompt from a randomly-selected week's [`patterns.md`](../Week%201/patterns.md). You're asked to *name the pattern* in a single word and justify it in a sentence. Pattern recognition is the muscle that matters most; this is the cheapest possible rep for it.

3. **Hard-mode challenge** — one challenge from a randomly-selected week's `challenges.md`. The digest includes the spec and constraints; you go solve it on your own time, then peek at the canonical solution in that week's language folders.

Each section links back to the source file in the repo, so you can read further if a prompt sparks something.

---

## How the rotation works

The picker is **deterministic on the ISO week number** — two runs in the same calendar week produce the same digest. Concretely:

```python
iso_year, iso_week, _ = today.isocalendar()
idx = iso_year * 100 + iso_week
case_study  = case_studies[idx % len(case_studies)]
pattern_drill = patterns_files[idx % len(patterns_files)]
challenge   = challenges_files[idx % len(challenges_files)]
```

A few consequences:

- Two consecutive weeks always advance every index by exactly one, so the rotation is a linear sweep through each list — you'll see the full corpus in ~30 weeks for drills/challenges and ~15 weeks for case studies, then it repeats.
- Adding a new case study or challenge **shifts the rotation** for all future weeks, because the lists are sorted and indexed by position.
- The picker uses no randomness, so a regenerated digest for the same week is byte-identical (modulo timestamps in the RSS feed).

Override the date for testing with `DIGEST_DATE=YYYY-MM-DD python3 scripts/generate_digest.py`.

---

## Implementation

- Picker: [`scripts/generate_digest.py`](../scripts/generate_digest.py) (stdlib only)
- Workflow: [`.github/workflows/weekly_digest.yml`](../.github/workflows/weekly_digest.yml)
- Output: [`WEEKLY.md`](../WEEKLY.md) and [`feed.xml`](../feed.xml) at repo root.
- Commit author: `github-actions[bot]` via the `git-auto-commit-action`.

If the workflow fails (case-study count drops to zero, YAML parse error, etc.), nothing breaks — `WEEKLY.md` and `feed.xml` are left as-is on the previous week's content, and the next Monday's run tries again.
