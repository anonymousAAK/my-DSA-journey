# Certified learners

This page is the **authoritative public roster** of people who have
completed the DSA Journey and been issued a signed credential.  See
[`docs/CERTIFICATION.md`](docs/CERTIFICATION.md) for the full rubric
and how the credentials are signed.

## How to get added

1. Pass the mastery quizzes for your target level's week range
   (`>=80%` on each — see
   [`docs/CERTIFICATION_LEVELS.md`](docs/CERTIFICATION_LEVELS.md)).
2. Submit the required number of capstones as PRs under `showcase/`.
3. Open a **Certification claim** issue using the
   [`cert_claim.yml`](.github/ISSUE_TEMPLATE/cert_claim.yml) template.
4. A maintainer runs `scripts/verify_certification.py`, posts your
   signed credential JSON back on the issue, and opens a one-line PR
   adding your row to the table below.

The roster is the source of truth: if a name appears here, that
person holds a valid credential at the listed level.  Revocations are
done by removing the row in a follow-up PR (with a brief reason in
the commit message).

---

## Roster

| GitHub user | Level         | Issued (UTC) | Capstones | Credential                                  |
|-------------|---------------|--------------|-----------|---------------------------------------------|
| _(empty)_   | _-_           | _-_          | _-_       | _Be the first — see instructions above._    |

<!--
When adding a row, please keep the table sorted by ascending "Issued"
date, and include a relative link to the claim issue in the
"Credential" column, e.g. `#42`.
-->
