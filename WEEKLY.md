# Weekly Digest — 2026-08-24 (ISO 2026-W35)

One case study, one pattern drill, one challenge. Rotated weekly. Read these in any order; the goal is one bite-sized prompt per week to keep recognition warm even when you can't sit down for a full session.

## Case study
**Rope Data Structure in VS Code / Sublime**

A text editor displays a document and lets the user type, delete, paste, and undo. If the document is 10 lines, any data structure works — even a flat string. If it's a 500 MB log file or a 200,000-line generated source file, naïve representations collapse: inserting one character at the beginning of a 500 MB string would require shifting all 500 MB. VS Code, Sublime, Atom, Vim — all face this. How do you represent a giant editable document so every keystroke is fast?

Read it in full: [`case_studies/real_world/12_text_editor_rope.md`](case_studies/real_world/12_text_editor_rope.md)

## Pattern drill
_From Week 16 (drill #6)._

> Distractor: Given a *sorted* array and a target sum, find a pair summing to T. (Should you use a hash set?)

Name the pattern in one word and justify in one sentence. Do **not** look at the answer key until you've written your guess down.

Drill source: [`Week 16/patterns.md`](Week 16/patterns.md)

## Hard-mode challenge
### Challenge 1 (Week 16): Custom Open-Addressing HashMap

**Spec**:
Implement a hashmap from scratch using **open addressing with linear probing** (or quadratic — pick one). No `HashMap` library. Support `put`, `get`, `remove`. Use a tombstone marker for deletions. Resize (double + rehash) when load factor exceeds 0.7. Implement your own hash function for integer or string keys.

**Constraints**:
- Up to `10^6` ops
- Time: O(1) amortized per op
- Memory: O(capacity)

**Test inputs**:
| Input | Expected output |
|

Full spec: [`Week 16/challenges.md`](Week 16/challenges.md)

---

Subscribe via RSS: point your reader at `https://raw.githubusercontent.com/anonymousAAK/my-DSA-journey/main/feed.xml`. See [`docs/NEWSLETTER.md`](docs/NEWSLETTER.md) for details.
