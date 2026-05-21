# Mentorship Program

The my-DSA-journey curriculum is self-paced, but every learner benefits from
someone a few weeks ahead of them. The mentorship program is the lightweight
structure that makes those pairings possible — no commitment beyond what each
mentor and mentee opts into.

## What mentorship looks like

A standard mentor relationship is **30 minutes per week** for as many weeks
as both sides find useful (typically 4–8). Sessions can run sync (video, voice,
screen-share) or async (paired threads in GitHub Discussions). Whatever
format, the agenda for a session is the same three questions:

1. **What did you ship since last week?** A capstone draft, a topic file, a
   quiz attempt — anything concrete.
2. **What got you stuck?** One specific bug, proof, or design decision.
3. **What's the next concrete deliverable?** Something the mentee will have
   in writing or in code before the next session.

Mentors are not tutors. They're not expected to teach a topic from scratch.
The job is to debug the mentee's current capstone or unfamiliar topic, point
at prior art, and keep momentum honest.

## Who can mentor

Anyone who has completed at least the **Foundation certification level**
(Weeks 1–10, see [`docs/MASTERY.md`](MASTERY.md)). You don't need to be
finished with all 30 weeks — you only need to be far enough ahead to help
someone earlier in the journey.

If you'd like to mentor, open a [Mentor Signup issue][signup-link] with your
availability, topics you're comfortable on, and a contact method. A
maintainer will add you to [`mentors/MENTOR_DIRECTORY.md`](../mentors/MENTOR_DIRECTORY.md).

## Who can request mentorship

Anyone working through the curriculum. There's no minimum requirement. Open a
[Mentee Request issue][request-link] describing your current week, what's
stuck, and your timezone.

## Matching

Matching happens through the GitHub Discussions **Mentorship** category. The
flow:

1. A mentee opens a request issue (`mentee_request.yml`).
2. A maintainer (or any mentor browsing the directory) cross-posts the
   request in the Mentorship Discussions category.
3. A mentor replies with availability; the two move to direct contact via
   Discord/email/whatever they prefer.
4. The mentee closes the issue with a one-line "matched with @X" note. This
   keeps the matching record searchable.

## Office hours model

Mentors who'd rather hold open hours than 1:1 pairings can run **recurring
office-hour threads** in the Mentorship Discussions category. The template:

```
# Office Hours — <Mentor handle> — <Day> <Time UTC>

**Topics I'm strong on:** <list>
**How to drop in:** post a question in this thread; I respond async within
24h. For sync sessions, comment with your timezone and we'll find a slot.
**Frequency:** every <week / two weeks>, posted as a new top-level thread.
```

Learners reply with questions in the thread, and the mentor responds async or
schedules a sync slot. Threads stay open for the duration of the office-hour
window (typically one week), after which the mentor posts a new thread for
the next round. Old threads stay searchable as a Q&A archive.

## Norms

- **Confidentiality**: anything discussed in a private mentor session stays
  private. If a mentor wants to share an interesting bug as a teaching
  example, they ask first and anonymize.
- **No-show etiquette**: if a session needs to be rescheduled, give at least
  24 hours notice. Three consecutive no-shows ends the pairing — no hard
  feelings, just freed time.
- **Code review, not code writing**: mentors review and challenge mentee
  code. They don't write the solution. The mentee is always the author of
  record on their own work.
- **Escalation**: if a pairing isn't working, either side can end it without
  explanation. The mentee posts a new request; the mentor's directory entry
  is unaffected.

## Removing yourself from the directory

Open a PR removing your row from [`mentors/MENTOR_DIRECTORY.md`](../mentors/MENTOR_DIRECTORY.md),
or comment on your original signup issue. Directory edits are merged within
a few days.

[signup-link]: ../../issues/new?template=mentor_signup.yml
[request-link]: ../../issues/new?template=mentee_request.yml
