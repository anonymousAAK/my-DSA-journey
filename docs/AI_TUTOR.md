# AI Tutor (`scripts/ask`)

`scripts/ask` is a small command-line tutor for this repo. Ask a natural-language question and it returns the most relevant passages from the curriculum, case studies, and methodology docs.

By default, **no question ever leaves your machine** — retrieval runs locally against a TF-IDF index of every `.md` file in the repo. There is an optional `--llm` mode that uses the Anthropic API if you've opted in.

---

## Install

```sh
# stdlib only — works on any Python 3.9+
python3 scripts/build_ask_index.py
```

That walks every `.md` file under the repo root, splits each into ~500-token chunks, and writes a TF-IDF index to `~/.journey/ask_index.pkl`.

Rebuild whenever you add or edit notable markdown content:

```sh
python3 scripts/build_ask_index.py
# or, equivalently:
./scripts/ask --rebuild-index
```

---

## Usage

### Default (offline, templated)

```sh
./scripts/ask "why does Kadane fail on all-negative arrays?"
./scripts/ask "explain consistent hashing"
./scripts/ask "what's the difference between heap and treap?"
```

You'll see something like:

```
Question: why does Kadane fail on all-negative arrays?

Based on the repository, here's what I found:

📌 [Week 6/patterns.md, section "Answer Key"]  (score 0.31)
... excerpt ...

📌 [PROBLEM_SOLVING.md, section "Brute → better → optimal"]  (score 0.28)
... excerpt ...

Related curriculum: Week 6, Week 18
```

The top **5** chunks are returned by default; tune with `--k 10` (or `--k 3`).

### LLM mode (optional)

```sh
export ANTHROPIC_API_KEY=sk-ant-...
pip install anthropic
./scripts/ask --llm "compare BFS and DFS for shortest path"
```

The retrieved chunks become context for a single Claude call (`claude-haiku-4-5-20251001` by default). The response is **streamed**, with citations like `[Source 2]` that point back to the chunks shown above.

If `--llm` is passed but `ANTHROPIC_API_KEY` is unset, or if the `anthropic` SDK isn't installed, the CLI prints a notice and falls back to the templated mode — it never silently degrades to "no answer".

---

## How retrieval works

It is intentionally small enough that you can read the whole thing in one sitting.

1. **Indexer** (`scripts/build_ask_index.py`):
   - Walks all `.md` files; skips `.git`, `node_modules`, build outputs.
   - Strips fenced (\`\`\`) and inline (\`) code blocks so code doesn't dominate the vocabulary.
   - Splits each doc into ~500-word chunks with a 60-word overlap; tags each chunk with the most recent markdown heading.
   - Computes sublinear-TF × IDF (`(1 + log(tf)) * idf`), stores sparse vectors + per-vector L2 norms.

2. **Retriever** (`scripts/ask`):
   - Same tokenizer + stopword list as the indexer.
   - Cosine similarity against every chunk vector.
   - Diversification: caps each source file to 2 chunks in the top-k.

3. **Templated response**: prints each hit with its file path, section heading, similarity score, and a 600-char excerpt. Adds a "Related curriculum: Week N, …" footer derived from chunk paths.

4. **LLM mode** (when enabled): same retrieval; the top chunks are concatenated as `[Source N]` blocks and passed to the model with a system prompt that constrains it to those sources only.

---

## Privacy

| Mode | What leaves your machine |
|---|---|
| default | nothing — pure local retrieval + printing |
| `--llm` | your question + the top retrieved chunks, sent to Anthropic's API |
| `--rebuild-index` | nothing — purely local |

The index file at `~/.journey/ask_index.pkl` is a `pickle` of plain text excerpts from your repo. It is not encrypted; treat it as you would any local copy of the repo.

---

## Limitations

- TF-IDF is a **keyword retriever**. If you ask using words the repo doesn't use, results will be weak. Try paraphrasing in the repo's vocabulary (e.g. "Kadane" rather than "max-subarray DP").
- The index is rebuilt manually. If you've edited markdown but not rebuilt, the retriever may miss your latest additions.
- No code-file retrieval. By design — code is in `Week N/<lang>/` and is typically not what you're asking about. If you want to retrieve over code too, extend `iter_markdown_files` and broaden the suffix filter.
- LLM mode currently uses a single model (`claude-haiku-4-5-20251001`). Change `LLM_MODEL` at the top of `scripts/ask` if you want a different one.

---

## Examples to try

```sh
./scripts/ask "what is the loop invariant for binary search?"
./scripts/ask "why prefer iterative dp over recursion with memoization?"
./scripts/ask "trade-offs of adjacency list vs adjacency matrix"
./scripts/ask "common bugs in floyd's tortoise and hare"
./scripts/ask --llm "I keep getting TLE on a sliding-window problem. What should I check?"
```
