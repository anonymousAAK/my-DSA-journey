# Weekly Competitions

A new competition opens every **Monday at 12:00 UTC** as a pinned GitHub
issue. The workflow that posts it lives in
[`.github/workflows/weekly_competition.yml`](../.github/workflows/weekly_competition.yml).

## How to participate

1. Find the pinned issue tagged `competition` on the repo.
2. Read the problem statement (or the linked seed file in this directory).
3. Post your solution as a **comment** on that issue. A solution is:
   - A code block in any of the curriculum's five languages (Java, Python,
     C++, Rust, Web).
   - A short note on time/space complexity.
   - Sample IO matching the spec.
4. The issue auto-closes when the next week's competition opens. Late
   solutions can still be posted but will not appear on the leaderboard for
   that week.

## Judging

Two modes — each competition's spec says which it uses:

- **Auto-graded.** Hidden test cases live in
  `competitions/judges/<iso_week>.json`. A maintainer runs the judge script
  against each submission (or links a CI job that does it). Scoring is
  pass/fail per test case plus a tie-breaker on wall-clock runtime.
- **Peer-voted.** Participants react with `+1` on the comments they think
  best solve the problem. Top three reactions at competition close win.
  Used for open-ended design problems where there is no single right answer.

## Leaderboard

The cumulative leaderboard is at
[`competitions/LEADERBOARD.md`](LEADERBOARD.md). It's updated manually for now
by running:

```sh
python3 scripts/update_leaderboard.py
```

The script takes a list of `{username, week, score}` records (currently
hard-coded for the manual workflow — see the script's docstring) and rewrites
the leaderboard sorted by total score, with a per-week breakdown table.

## Authoring a competition

Use the template at
[`competitions/templates/competition_template.md`](templates/competition_template.md)
as a starting point. Place the file at `competitions/<iso_week>.md` (e.g.
`competitions/2026-W22.md`). When the workflow runs on Monday it will pick up
that file automatically as the issue body; otherwise it falls back to a
"Problem TBD" placeholder.

If your problem is auto-graded, also drop a `competitions/judges/<iso_week>.json`
with the hidden tests. Format:

```json
{
  "tests": [
    {"input": "...", "expected": "..."},
    {"input": "...", "expected": "..."}
  ],
  "timeout_seconds": 5
}
```

## Seed competitions

- [`2026-W21.md`](2026-W21.md) — Circular-buffer `tail` implementation.

More to come; PRs welcome.
