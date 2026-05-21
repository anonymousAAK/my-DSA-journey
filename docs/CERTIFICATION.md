# DSA Journey — Certification

This page describes how to claim a credential for completing the
DSA Journey curriculum, what "completion" actually means here, and
how a verifier on the other side checks that your claim holds up.

The certification is **not** a paid course or accredited diploma — it
is a community-issued, cryptographically-signed JSON document plus a
permanent entry in `CERTIFIED_LEARNERS.md`.  It's only as valuable as
the rigor of the rubric, which is why the rubric is mechanical and
the verifier is open source.

> Looking for the rubric?  See **`docs/CERTIFICATION_LEVELS.md`**.

---

## What counts as completion

Three things together:

1. **Mastery quizzes** — `>=80%` on the mastery quiz of every week
   inside your target level's range (see `CERTIFICATION_LEVELS.md`).
   These are recorded automatically in `~/.journey/progress.json`
   when you run:

   ```bash
   ./scripts/journey quiz <week>
   ```

2. **Capstones** — at least `N` of the six capstones under
   `capstones/` completed and submitted as a PR into the
   repo's `showcase/` directory (or your fork's equivalent).
   `N` depends on level (1 / 2 / 4).

3. **Self-attestation** — a checkbox on the claim form confirming that
   your `progress.json` and capstone PRs were genuinely earned (not
   hand-edited, not copy-pasted from a friend).

The full level matrix lives in `docs/CERTIFICATION_LEVELS.md`.

---

## How to claim

1. **Open a claim issue.**  Use the
   [Certification claim](../.github/ISSUE_TEMPLATE/cert_claim.yml)
   template (you'll see it on the "New Issue" page as
   "Certification claim").  Required fields:
   - GitHub username
   - Target level (Foundation / Practitioner / Master)
   - Your `progress.json` contents (or a public gist link)
   - Capstone PR URLs (one per line)
   - Self-attestation checkbox

2. **A maintainer verifies.**  They run:

   ```bash
   export JOURNEY_CERT_SECRET=...                # repo bot's secret
   python3 scripts/verify_certification.py \
       --progress /tmp/your-progress.json \
       --user <your-handle> \
       --capstone <PR-url-1> \
       --capstone <PR-url-2> \
       --capstone <PR-url-3>
   ```

   The verifier:
   - Loads your `progress.json`.
   - Checks `>=80%` on every week in the level's range — and tells you
     **exactly** which weeks failed if any did.
   - Confirms you've submitted enough capstone PRs.
   - Determines the highest level you qualify for (yes, you can
     "level up" — claiming Foundation but qualifying for Practitioner
     will produce a Practitioner credential).
   - Builds a payload of the form

     ```json
     {
       "learner": "<github-user>",
       "issued": "<iso8601-utc>",
       "weeks_completed": [1, 2, ..., 10],
       "capstones_completed": ["<pr-url-1>", ...],
       "level": "Foundation",
       "schema": "dsa-journey-credential-v1"
     }
     ```

   - HMAC-SHA256 signs the payload using `JOURNEY_CERT_SECRET`.
   - Writes `credential.json` and a human-readable `credential.txt`.

3. **Maintainer posts the credential** as a comment on your claim
   issue and opens a tiny follow-up PR adding you to
   `CERTIFIED_LEARNERS.md`.

4. **You can verify it yourself** (and so can anyone you share it
   with) using the matching secret:

   ```bash
   JOURNEY_CERT_SECRET=... python3 scripts/verify_credential.py credential.json
   ```

   `verify_credential.py` uses `hmac.compare_digest` for constant-time
   comparison, refuses unknown algorithms / schemas, and exits
   non-zero on any mismatch.

---

## What you get

- **A signed credential JSON.**  Tamper-evident — flipping a single
  byte invalidates the signature.  Pin it to your README, dotfiles,
  blog, wherever.
- **A line in `CERTIFIED_LEARNERS.md`.**  Public, permanent (unless
  revoked), and trivially searchable.
- **Bragging rights.**  Standard.

A note on what this is *not*:

- Not a credit-bearing certificate.
- Not a job guarantee.
- Not signed by any third-party authority — only by this repo's bot
  keypair (an HMAC secret, in practice).

---

## Security model

We sign credentials with an HMAC because it's the simplest thing that
gives us tamper-evidence with stdlib only.  A few honest tradeoffs:

- **Symmetric.**  Anyone with the secret can forge a credential.
  In practice the secret is held by repo maintainers; verifiers need
  the same secret to validate.  If/when this grows beyond a hobbyist
  scale, swap to Ed25519 + a public key.
- **Revocable.**  If a credential is later found to have been issued
  in error (or fraudulently), the maintainer entry in
  `CERTIFIED_LEARNERS.md` is the authoritative record — a revocation
  is just a PR that removes the row.

For the current scale of this project, that's the right balance: easy
to run, easy to audit, no live signing key in the repo, no
dependencies.

---

## Frequently asked

**Can I claim more than one level?**  Just claim the highest one
you qualify for; the verifier figures out the rest.

**Do I have to do the capstones in order?**  No.  Foundation needs
`1` capstone of any kind; Practitioner needs `2`; Master needs
`4` *or* the specific phase 1-3 set plus a showcase entry.

**What if my `progress.json` is on a different machine?**  Move the
file or paste the contents in the claim.  The verifier only cares
about the JSON.

**I aced everything but my streak/history is short — does that
matter?**  No.  Only `weeks[<n>].rate >= 80` matters for the rubric.

**Can someone steal my credential and pretend to be me?**  They could
republish the JSON, but the `learner` field is part of the signed
payload — flipping it invalidates the signature.  If you suspect
abuse, open an issue and a maintainer will revoke and reissue.
