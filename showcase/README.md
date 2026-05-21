# Showcase — finished capstones

This is the public board for capstone projects built by learners working through the 30-week curriculum. If you finished any of the capstones in [`capstones/`](../capstones/), open a PR to add yourself — it's a low-effort, high-signal way to show others what's possible.

The index is rebuilt automatically from individual submission files: [`SUBMISSIONS.md`](SUBMISSIONS.md).

---

## How to submit

You can either:

**(A)** Open a new issue using the [Showcase submission template](../.github/ISSUE_TEMPLATE/showcase_submission.yml). The issue gets the maintainers' attention; once they ack, you copy the issue content into a PR (step B).

**(B)** Open a PR directly. Add **one** Markdown file at:

```
showcase/submissions/<github-handle>-<capstone-slug>.md
```

For example, `showcase/submissions/octocat-graph-router.md`. The file must start with YAML frontmatter (between `---` fences) followed by free-form Markdown content. After your PR is merged, the index regenerator picks the new file up on the next push.

To regenerate locally before pushing:

```bash
python3 scripts/generate_showcase_index.py
```

---

## Submission template

Copy this into your submission file verbatim and fill in the blanks. Don't rename the frontmatter keys — the index script reads them.

```markdown
---
name: "Your Project Name"
capstone: "Phase 1 — Mini Graph Router"   # or whichever phase
repo_url: "https://github.com/your-handle/your-project"
github_handle: "your-handle"
demo_url: ""                              # optional; live demo / asciicast / video
languages: ["Python", "Rust"]             # optional
date_finished: "2026-04-12"               # YYYY-MM-DD
---

# Your Project Name

A one-paragraph elevator pitch. What does it do? Who is it for? What makes it interesting?

## Capstone phase

Which capstone(s) from `capstones/` did you base this on? Did you stay within scope or extend?

## Stack

- Language(s):
- Notable libraries:
- How to run it:

## What was hardest

Two or three paragraphs on the hardest part of building this. Not "the deadline" — the *technical* part that almost beat you. The point of this section is to be useful to the next learner who attempts the same capstone.

## What you learned

What surprised you? What concept finally clicked while you were debugging at 2 AM? What would you tell your past self?

## What you'd do differently

If you started over with what you know now, what would change?

## Screenshots / demo

A picture, an asciicast, a one-liner of output. Anything that conveys what the thing does in 5 seconds.
```

---

## Example submissions

The two files below are deliberately fake — they exist to show the format. Treat them as templates, not as quality bars.

- [`submissions/example-graph-router.md`](submissions/example-graph-router.md) — Phase 1 mini graph router in Python
- [`submissions/example-search-engine.md`](submissions/example-search-engine.md) — Phase 3 mini search engine in Rust

Browse [`SUBMISSIONS.md`](SUBMISSIONS.md) for the live index of real submissions.

---

## Rules

1. **One submission per project, per learner.** If you want to update an existing submission, edit the same file.
2. **Real projects only.** No vapor, no "coming soon." If the repo link is private or 404s, the maintainers will close the PR.
3. **Your own work.** You can stand on the curriculum's shoulders, but the implementation has to be yours. Don't fork someone else's capstone and submit it.
4. **Keep it kind.** Other learners read this. Avoid bragging about how fast you finished; do tell us what was hard.
