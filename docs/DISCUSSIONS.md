# GitHub Discussions — Category Plan

GitHub Discussions can't be enabled from code — a repo admin has to flip the toggle in **Settings → General → Features → Discussions**. Once it's on, this document is the seeding plan: which categories to create, what each is for, and the welcome post template to pin in each.

When you create a category in the UI, GitHub asks for:
- **Name** — short
- **Description** — one sentence
- **Format** — `Open` (free-form), `Q&A` (question + accepted answer), `Announcement` (maintainers-only post), or `Poll`

Use the table below verbatim.

---

## Categories to create

### 1. Q&A: Stuck on a problem?

- **Name**: `Stuck on a problem?`
- **Description**: Working through a week's challenges or LeetCode list and hit a wall? Ask here — describe the problem, your approach so far, and where you got stuck.
- **Format**: Q&A
- **Pinned welcome post**:

  ```markdown
  Welcome! This is the place to ask for help on any problem in the curriculum or in your own practice.

  **Before you post:**
  1. State the problem in your own words (don't just paste the LeetCode URL).
  2. Show the approach you've already tried — even if you're sure it's wrong. We learn more from your wrong attempt than your final question.
  3. Include the language you're using and the actual code you have so far (in a code block).
  4. End with a specific question: "why does my DP miss this case?" beats "how do I solve this?"

  Replies that *just give the answer* are less helpful than replies that ask one follow-up question to nudge you toward seeing it yourself. Don't be shy about Socratic-style replies.
  ```

### 2. Pattern recognition help: Can't see the pattern?

- **Name**: `Can't see the pattern?`
- **Description**: For when you read a problem and have no idea which technique applies. Post the problem statement; the community helps you classify it.
- **Format**: Q&A
- **Pinned welcome post**:

  ```markdown
  Pattern recognition is the hardest part of DSA, full stop. Faster algorithms are mechanical once you know which family of techniques the problem lives in.

  **Post format:**
  - Paste the problem statement (rephrased in your own words is fine).
  - List the patterns you *considered* and why each one didn't quite fit.
  - Ask: "what am I missing?"

  This category is **not** for solutions — it's for the upstream skill of classifying the problem. Replies should name the pattern (e.g., "this is a monotonic stack problem") and point to which week of the curriculum covers it, not write the code.
  ```

### 3. Capstone show-and-tell

- **Name**: `Share your finished capstone`
- **Description**: Finished a capstone project from `capstones/`? Show it off here. Repo link, a screenshot, what was hardest, what surprised you.
- **Format**: Open
- **Pinned welcome post**:

  ```markdown
  You finished a capstone. That's a real milestone — most learners stop at Week 8. Tell us about it.

  **Template:**
  - **Capstone phase**: (1, 2, 3, ...)
  - **Repo / demo link**:
  - **Stack / language**:
  - **One screenshot or asciicast**:
  - **What was hardest**: 2-3 sentences.
  - **What surprised you**: the thing you didn't expect to learn.
  - **What you'd do differently**: if you were starting again.

  Bonus: if you'd like your project added to the public showcase, see [`showcase/README.md`](../showcase/README.md) — the submission flow is a PR away.
  ```

### 4. Study buddies

- **Name**: `Find someone studying the same week`
- **Description**: Pair up. Tell us which week you're on, your timezone, and how often you'd like to sync.
- **Format**: Open
- **Pinned welcome post**:

  ```markdown
  30 weeks is a long road and it's easier with a partner. Use this thread to find one.

  Use the structured form (Discussions → New → "Find a study buddy") so your post is searchable. The form asks for:
  - Current week
  - Timezone
  - Cadence (daily check-in / weekly sync / async / live pair-coding)
  - Language(s) you're working in
  - One sentence on what you're hoping to get out of pairing

  When someone matches your post, take it to DMs or to a private Discord — don't share contact info publicly.
  ```

### 5. Bugs and corrections

- **Name**: `Spot something wrong?`
- **Description**: Found a typo, a broken example, or a wrong complexity claim? Post a quick discussion before opening an issue if you're not sure it's a bug.
- **Format**: Open
- **Pinned welcome post**:

  ```markdown
  This is the soft on-ramp to issue reporting. If you're 100% sure it's a bug, please go straight to the [bug template](../.github/ISSUE_TEMPLATE/bug.yml). If you're not sure — start here.

  **Post format:**
  - File path (e.g. `Week 6/python/3.kadane.py`).
  - What you observed.
  - What you expected.
  - Why you think it might be a bug (vs. "this is unfamiliar to me").

  Maintainers will either convert the discussion into a tracked issue or explain why it's working as intended.
  ```

### 6. Career

- **Name**: `Interview prep questions`
- **Description**: General career, interview, and learning-strategy questions that don't fit into a specific problem. "How do I know I'm ready for FAANG interviews?", "Should I do Week 23 if I'm focused on web roles?"
- **Format**: Open
- **Pinned welcome post**:

  ```markdown
  This is the catch-all for big-picture questions: which weeks matter for your target role, when you're "ready", whether to do contests, how to journal effectively, and so on.

  **Two ground rules:**
  1. Career advice is *advice*, not gospel. Different roles need different depth. Share your context (target company size, role, timeline) so replies can be calibrated.
  2. No referral spam, no "DM me for paid coaching," no recruiting posts. Maintainers will lock these.

  For *specific* problem help, use "Stuck on a problem?" instead — keep this thread for higher-level questions.
  ```

---

## Suggested order of creation

1. Stuck on a problem? (Q&A)
2. Can't see the pattern? (Q&A)
3. Spot something wrong? (Open)
4. Find a study buddy (Open)
5. Share your finished capstone (Open)
6. Interview prep questions (Open)

The first two are the lifeblood; the others are secondary.

---

## Discussion templates

The repo ships two YAML discussion templates (forms shown when a user clicks "New discussion"):

- [`.github/DISCUSSION_TEMPLATE/welcome.yml`](../.github/DISCUSSION_TEMPLATE/welcome.yml) — a generic intro form.
- [`.github/DISCUSSION_TEMPLATE/study_buddy.yml`](../.github/DISCUSSION_TEMPLATE/study_buddy.yml) — the structured study-buddy form referenced above.

Add more under `.github/DISCUSSION_TEMPLATE/` as new categories appear.
