# Audio Walkthroughs

> **Status**: Scaffolding incomplete (translation/audio agent hit a session limit before producing transcripts). PRs welcome.

The plan is to produce narration-ready transcripts of `PROBLEM_SOLVING.md`,
`QUICKSTART.md`, and each phase walkthrough in `case_studies/`, then generate
MP3/WAV via TTS for commute-friendly study.

## To contribute

1. Copy a source doc into `audio/transcripts/<name>.txt`.
2. Strip code blocks, expand abbreviations, add `<break time="500ms"/>` markers.
3. Optionally render with espeak-ng:
   ```bash
   espeak-ng -v en-us -s 160 -f audio/transcripts/<name>.txt -w audio/output/<name>.wav
   ```
4. Open a PR.
