# Public progress badges

Your `~/.journey/progress.json` is local. If you'd like a piece of
verifiable, public proof-of-progress — a shields.io badge for your
profile README — this page walks you through it.

The flow is:

1. Run a generator that turns your `progress.json` into a handful of
   tiny shields.io endpoint JSON files.
2. Upload those JSON files to a public GitHub Gist.
3. Embed the gist's raw URL in your README via `shields.io/endpoint`.

No external services, no scraping — shields.io fetches your gist JSON
directly each time the badge is rendered.

---

## 1. Generate the badge files

From the repo root:

```bash
python3 scripts/badge_generator.py
```

That reads `~/.journey/progress.json` and writes the following into
`~/.journey/`:

| File                          | What it shows                          |
|-------------------------------|----------------------------------------|
| `badge.json`                  | "Week N / 30" — the headline badge      |
| `badge_weeks_complete.json`   | Count of weeks passed at >=80%          |
| `badge_current_week.json`     | The current week you're on              |
| `badge_streak.json`           | Consecutive-day study streak            |
| `badge_total_skills.json`     | Total skill checks passed across weeks  |

Other useful flags:

```bash
# Point at a non-default progress file
python3 scripts/badge_generator.py --input /tmp/progress.json

# Write the JSON somewhere else (e.g. a checkout of your gist)
python3 scripts/badge_generator.py --output-dir ~/code/my-badge-gist

# Suppress chatty output
python3 scripts/badge_generator.py --quiet
```

Each file is a tiny shields.io endpoint document:

```json
{
  "schemaVersion": 1,
  "label": "DSA Journey",
  "message": "Week 18 / 30",
  "color": "blue"
}
```

---

## 2. Upload to a public gist

### Option A — `gh` CLI (recommended)

If you have the [GitHub CLI](https://cli.github.com/) installed and
authenticated:

```bash
# First time: create the gist with all five badge files
gh gist create --public \
  ~/.journey/badge.json \
  ~/.journey/badge_weeks_complete.json \
  ~/.journey/badge_current_week.json \
  ~/.journey/badge_streak.json \
  ~/.journey/badge_total_skills.json
```

The command prints the new gist URL. Note the gist ID (the hex string
at the end of the URL) — you'll need it for embedding.

Subsequent updates (after rerunning the badge generator):

```bash
gh gist edit <GIST_ID> \
  --add ~/.journey/badge.json \
  --add ~/.journey/badge_weeks_complete.json \
  --add ~/.journey/badge_current_week.json \
  --add ~/.journey/badge_streak.json \
  --add ~/.journey/badge_total_skills.json
```

> Tip: `gh gist edit <ID> -a <file>` overwrites the named file in
> the gist, so the same command works for "create new file" and
> "update existing file".

### Option B — web UI

1. Visit <https://gist.github.com/> while signed in.
2. Drag each `badge_*.json` file from `~/.journey/` into the editor
   (or copy/paste contents).
3. Make sure "Create public gist" is selected and click **Create**.

---

## 3. Find your raw URL

For any file in a public gist, the raw URL has the shape:

```
https://gist.githubusercontent.com/<github-user>/<gist-id>/raw/<filename>
```

Open the gist, click **Raw** on the badge file, and copy the URL from
the address bar.

---

## 4. Embed in your README

Use shields.io's `endpoint` mode:

```markdown
![DSA Journey](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<user>/<gist>/raw/badge.json)
```

A more complete README block:

```markdown
## DSA progress

![DSA Journey](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<user>/<gist>/raw/badge.json)
![Weeks aced](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<user>/<gist>/raw/badge_weeks_complete.json)
![Streak](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<user>/<gist>/raw/badge_streak.json)
![Skill checks](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<user>/<gist>/raw/badge_total_skills.json)
```

That renders roughly like:

> ![DSA Journey](https://img.shields.io/badge/DSA%20Journey-Week%2018%20%2F%2030-blue)
> ![Weeks aced](https://img.shields.io/badge/weeks%20aced-12%20%2F%2030-yellowgreen)
> ![Streak](https://img.shields.io/badge/streak-9%20days-blueviolet)
> ![Skill checks](https://img.shields.io/badge/skill%20checks%20passed-87-green)

(Those are static placeholders — the real ones above will reflect
your live gist.)

You can also force a style, change the logo, etc., using shields.io's
standard query parameters:

```markdown
![DSA Journey](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/<user>/<gist>/raw/badge.json&style=for-the-badge&logo=python)
```

---

## 5. Keep it fresh

You have two options:

- **Manual.** Re-run `python3 scripts/badge_generator.py` then
  `gh gist edit ...` whenever you ace a week.
- **Automated.** Copy `.github/workflows/sync_badge.yml.example`
  into your own fork at `.github/workflows/sync_badge.yml`, set the
  required secrets, and let CI push updates for you. See the comments
  inside that file for setup instructions.

---

## Privacy notes

- Only the numbers in your badge JSONs are public — never the contents
  of `progress.json` itself.
- shields.io caches endpoint responses (typically for a few minutes),
  so updates may not appear immediately.
- If you'd rather not publish a gist, just skip everything past step 1
  and use the JSON files locally (for example, in a dashboard).
