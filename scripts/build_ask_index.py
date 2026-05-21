#!/usr/bin/env python3
"""Build a TF-IDF index over all .md files in the repo, for use by `scripts/ask`.

Walks the repo from the script's parent directory, splits each markdown file into
~500-token chunks (token ~= whitespace-delimited word), computes TF-IDF, and writes
the result to ~/.journey/ask_index.pkl using pickle.

Run this once on install, and again any time you add/edit notable .md content:

    python3 scripts/build_ask_index.py

Stdlib only.
"""

from __future__ import annotations

import math
import os
import pickle
import re
import sys
import time
from pathlib import Path
from collections import Counter
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_DIR = Path.home() / ".journey"
INDEX_PATH = INDEX_DIR / "ask_index.pkl"

# Roughly the chunk size in tokens; ~500 words ≈ ~700 sub-word tokens
CHUNK_TOKENS = 500
CHUNK_OVERLAP = 60  # token overlap between adjacent chunks within the same file

# Tiny English stopword list — keeps the index tighter
STOPWORDS = set(
    """
    a an and are as at be by for from has have he in is it its of on or that the to
    was were will with you your we our us i me my so if then than this these those
    do does did not no but also can could should would may might into about over
    when where what why how who whom which while up down out off here there their
    them they it's i'm i've you're they're vs etc e.g. eg ie i.e
    """.split()
)

# split on non-alphanumeric, keep apostrophes inside words (e.g. "kadane's")
_TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9'_-]*")


def tokenize(text: str) -> list[str]:
    """Lowercase, alphanumeric-only tokens with stopwords removed."""
    return [t.lower() for t in _TOKEN_RE.findall(text) if t.lower() not in STOPWORDS and len(t) > 1]


def iter_markdown_files(root: Path) -> Iterable[Path]:
    """Yield .md files under root, skipping vendor/build/hidden directories."""
    skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "site", ".idea", ".vscode"}
    for dirpath, dirnames, filenames in os.walk(root):
        # prune in-place
        dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith(".md"):
                yield Path(dirpath) / fn


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)


def split_into_chunks(text: str, path_rel: str) -> list[dict]:
    """Split a markdown document into ~CHUNK_TOKENS-token windows.

    Each chunk carries the most recent heading as its section name so the templated
    response can show "[file.md, section "..."]" context.
    """
    # First, find heading positions so each chunk can be annotated with the
    # nearest preceding heading.
    headings = [(m.start(), m.group(2).strip()) for m in _HEADING_RE.finditer(text)]

    def heading_at(pos: int) -> str:
        h = ""
        for start, title in headings:
            if start <= pos:
                h = title
            else:
                break
        return h

    # Tokenize while tracking the byte offset of each token so we can map back.
    # For simplicity (and stdlib-only), we use whitespace splitting for chunk
    # boundaries, then call tokenize() separately for the TF stats.
    words = text.split()
    if not words:
        return []

    # Compute char offsets for words (approximate; works because we split text)
    offsets = []
    pos = 0
    for w in words:
        idx = text.find(w, pos)
        if idx < 0:
            idx = pos
        offsets.append(idx)
        pos = idx + len(w)

    chunks = []
    i = 0
    n = len(words)
    while i < n:
        j = min(i + CHUNK_TOKENS, n)
        body = " ".join(words[i:j])
        # the chunk's "anchor" position is the start of the first word
        anchor = offsets[i] if i < len(offsets) else 0
        chunks.append({
            "path": path_rel,
            "section": heading_at(anchor),
            "text": body,
            "tokens": tokenize(body),
        })
        if j >= n:
            break
        i = j - CHUNK_OVERLAP if (j - CHUNK_OVERLAP) > i else j
    return chunks


def build_index() -> dict:
    """Walk the repo, produce a TF-IDF index dict."""
    chunks: list[dict] = []
    for md in iter_markdown_files(REPO_ROOT):
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except OSError as e:
            print(f"  skip {md}: {e}", file=sys.stderr)
            continue
        # Strip fenced code blocks — they pollute the TF-IDF for explanatory text.
        text_no_code = re.sub(r"```.*?```", " ", text, flags=re.S)
        # Strip inline code too
        text_no_code = re.sub(r"`[^`]*`", " ", text_no_code)
        rel = str(md.relative_to(REPO_ROOT))
        file_chunks = split_into_chunks(text_no_code, rel)
        if file_chunks:
            chunks.extend(file_chunks)

    # IDF
    N = len(chunks)
    df: Counter[str] = Counter()
    for c in chunks:
        for term in set(c["tokens"]):
            df[term] += 1
    idf = {term: math.log((N + 1) / (cnt + 1)) + 1.0 for term, cnt in df.items()}

    # TF-IDF vectors as sparse dicts; also store norm for cosine
    vectors: list[dict] = []
    norms: list[float] = []
    for c in chunks:
        tf = Counter(c["tokens"])
        if not tf:
            vectors.append({})
            norms.append(0.0)
            continue
        # Sublinear TF (1 + log(tf)) tends to behave better than raw counts.
        vec = {term: (1.0 + math.log(cnt)) * idf.get(term, 0.0) for term, cnt in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values()))
        vectors.append(vec)
        norms.append(norm)

    # Drop the per-chunk tokens list now that vectors are computed (saves space).
    for c in chunks:
        c.pop("tokens", None)

    return {
        "version": 1,
        "built_at": time.time(),
        "repo_root": str(REPO_ROOT),
        "chunks": chunks,
        "vectors": vectors,
        "norms": norms,
        "idf": idf,
        "n_chunks": N,
        "n_files": len({c["path"] for c in chunks}),
    }


def save_index(index: dict) -> Path:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "wb") as f:
        pickle.dump(index, f, protocol=pickle.HIGHEST_PROTOCOL)
    return INDEX_PATH


def main() -> int:
    print(f"Indexing markdown files under {REPO_ROOT} ...")
    t0 = time.time()
    index = build_index()
    path = save_index(index)
    elapsed = time.time() - t0
    print(f"  files indexed:  {index['n_files']}")
    print(f"  chunks indexed: {index['n_chunks']}")
    print(f"  vocab size:     {len(index['idf'])}")
    print(f"  saved to:       {path}")
    print(f"  elapsed:        {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
