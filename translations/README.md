# Translations

The foundational mindset documents of `my-DSA-journey` are available in several languages so the curriculum is not gated behind English fluency. Code stays in English (variable names, syntax, library APIs) — translations cover prose: the *how-to-think* layer.

## Available languages

| Language | Folder | Files translated |
|---|---|---|
| English (default) | (repo root) | All |
| हिन्दी (Hindi) | [`hi/`](hi/) | `PROBLEM_SOLVING.md`, `QUICKSTART.md`, `diagnostic.md`, `README.md` (partial) |
| Español (Spanish) | [`es/`](es/) | `PROBLEM_SOLVING.md`, `QUICKSTART.md`, `diagnostic.md`, `README.md` (partial) |
| 中文 (Mandarin Simplified) | [`zh/`](zh/) | `PROBLEM_SOLVING.md`, `QUICKSTART.md`, `diagnostic.md`, `README.md` (partial) |

The root README's *Start Here*, *Learning Paths*, and *How to Use This Guide* sections are translated; the per-week breakdowns, complexity tables, and references stay in the English README for now (they're mostly technical reference, much of which is universal vocabulary).

## Status: AI-assisted, awaiting native review

> **Important.** These translations were drafted with the help of an AI assistant. They aim to be natural and idiomatic, not literal — for example, "binary search" is rendered as *búsqueda binaria* in Spanish but is often left as English mid-sentence in Hindi text where that's how speakers actually use the term. Technical jargon is left in English where Romanization or transliteration would be unnatural.
>
> They have **not yet been reviewed by native speakers**. If you are a native speaker of Hindi, Spanish, or Mandarin, your review (or corrections via PR) is the single most valuable contribution you can make to these files. See *How to contribute* below.

If you spot a phrasing that reads as a literal-translated English idiom rather than natural target-language phrasing, please file an issue or PR. We'd rather sound right than be word-for-word loyal to the English.

## How to contribute

### Improving an existing translation

1. Pick a file you want to improve (e.g. `translations/es/PROBLEM_SOLVING.md`).
2. Read it side-by-side with the English original (linked in the note at the top of each file).
3. Edit for naturalness, accuracy, and idiom — **not** for word-for-word fidelity. Where a technical term has a well-established target-language version, use it; where the English term is what speakers actually say, keep it.
4. **Preserve all code blocks as-is.** Code, identifiers, library names, file paths, and command snippets stay in English.
5. **Preserve markdown structure** — headings, tables, lists, links — so internal references and the site build keep working.
6. Open a PR titled `translations(<lang>): <short description>`. Example: `translations(es): refine sliding window phrasing in PROBLEM_SOLVING`.

### Adding a new language

The current 3 translations cover roughly 2 billion speakers, but there are gaps. Particularly welcome additions:

- Portuguese (`pt`) — Brazil + Lusophone Africa.
- French (`fr`) — Francophone Africa is a huge underserved learner base.
- Arabic (`ar`) — RTL formatting required; mkdocs handles this if `dir="rtl"` is set on the language root.
- Bengali (`bn`), Indonesian (`id`), Japanese (`ja`), Korean (`ko`), Russian (`ru`), German (`de`), Turkish (`tr`), Vietnamese (`vi`).

To add a language:

1. Open an issue first using the *Translation request* topic — short note saying which language you'll cover, and whether you're a native speaker. This avoids two volunteers doing the same work.
2. Create `translations/<lang>/` where `<lang>` is the ISO 639-1 code (`pt`, `fr`, `ar`, …). For variants, append a region: `pt-BR`, `zh-TW`.
3. Translate the **four foundational docs first**, in this order:
   - `PROBLEM_SOLVING.md` — the mindset manifesto
   - `QUICKSTART.md` — the 4-hour on-ramp
   - `diagnostic.md` — the 15-question placement test
   - `README.md` — partial (Start Here + Learning Paths + How to Use sections)

   These four are the minimum viable translation set; further docs can be added incrementally.
4. Each file must begin with a one-line note in the target language saying *"This is a translation of the English original. If unclear, refer to the English version."* — and linking back to the English source. See the existing files for the format.
5. Add a row to the *Available languages* table above.
6. Add an entry to the *Languages* line in the root `README.md` under *Start Here*.
7. Add yourself to the contributors section of your translation files (or to a `translations/CONTRIBUTORS.md` if it exists by then) so credit is preserved.

### Style guidelines (apply to all languages)

- **Match register, not text.** The English original is plainspoken-but-precise. Aim for the equivalent register in your target language — not academic, not slangy.
- **Keep code blocks identical.** No translating Python keywords or function names. Comments inside code may be translated, but think about whether a learner will compare with the English version — if so, keep code comments English too.
- **Don't translate URLs or anchor links.** Internal links to `Week N/` paths and to anchors like `#path-2-interview-prep-8-weeks` must stay as-is.
- **Tables and lists**: translate the prose content but keep column structure and bullet ordering identical to the English.
- **Markers like `[needs translation]`** are explicitly allowed where you're unsure of a phrase. Better to flag uncertainty than silently invent.
- **One pull request per language**, ideally. If a language is split across multiple contributors, coordinate via the issue thread first.

### What we do not need

- Mechanical, sentence-by-sentence translation. If a paragraph is awkward in the target language, restructure it. The *content* is the contract, not the sentence boundaries.
- Translation of the per-week DSA technical material. That work is enormous and the technical vocabulary is largely universal — for now we are deliberately keeping it English. If you want to translate a single `Week N/README.md` because it's the on-ramp to a self-contained topic, open an issue first.

---

Thank you for helping make this curriculum accessible. The next learner who picks this up in their first language is the audience you're writing for.
