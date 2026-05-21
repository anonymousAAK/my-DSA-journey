# Python Playground

A browser-native runner for every Python file in this repo. No backend, no
build step, no install — Python is executed inside the page by
[Pyodide](https://pyodide.org/) (CPython compiled to WebAssembly).

## Run it locally

The playground is plain static HTML/JS; it only needs to be served by an HTTP
server (it cannot run from a `file://` URL because it `fetch`es `.py` files
and the JSON index relative to the repo root).

From the repository root:

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/playground/>.

To open a specific file directly:

```
http://localhost:8000/playground/?file=Week+1/python/2.hello_world.py
```

## How it works

1. On load, the page fetches `playground/file_index.json` (a manifest of every
   `Week N/python/*.py` file). The left sidebar is rendered from this manifest.
2. When you click a file in the sidebar, the playground does
   `fetch('../Week N/python/<name>.py')` and loads the source into a CodeMirror
   6 editor (loaded from a CDN as an ES module — no bundler required).
3. Pyodide is loaded once from `https://cdn.jsdelivr.net/pyodide/v0.27.0/full/`.
   Pressing **Run** (or **Ctrl/Cmd+Enter**) executes the current editor buffer
   via `pyodide.runPythonAsync`. `stdout` / `stderr` are captured and streamed
   into the output pane on the right.
4. The **stdin** textarea acts as a typed-in stdin buffer: each call to
   Python's `input()` consumes one line from it. Type your inputs (one per
   line) before pressing Run.
5. The **Reset** button reverts the editor buffer to the original file
   contents. **GitHub** opens the file on github.com.

## Regenerating the file index

Whenever you add, rename, or delete a `Week N/python/*.py` file, regenerate
the manifest:

```bash
python3 scripts/generate_playground_index.py
```

This rewrites `playground/file_index.json`. The script walks `Week 1` through
`Week 30`, sorts files by their leading number prefix, and skips dunder /
private files (those starting with `_`).

## Limitations

- **No filesystem access.** Files that read sibling data files won't work.
  Pyodide provides a virtual in-memory FS only.
- **No network from Python.** Pyodide can't hit arbitrary sockets. Use
  `pyodide-http` patching if you really need `requests`/`urllib` — not bundled
  here.
- **Cold start ~1-3 s.** First load downloads ~10 MB of WASM + stdlib. The
  browser caches these aggressively on subsequent visits.
- **Single-threaded.** Long-running code blocks the UI. Keep it short.
- **No C extensions outside the Pyodide repo.** Pure-Python and a curated set
  of scientific packages only.

## Integration with the static per-week site

Each `Week N/web/index.html` already has a **Live Demos** section (item-by-item
links to pre-rendered demo pages). The playground is the natural sibling:
"Run it yourself, edit it, break it." A *Try it live* link is injected into
the **Live Demos** card of every week's `index.html`, pointing at the
playground with the corresponding file pre-loaded — for example:

```
../playground/?file=Week%201/python/2.hello_world.py
```

The static site can also iframe the playground if you want a fully embedded
experience — the page is self-contained and responds to the `?file=` query
parameter.

## Architecture choices

- **CodeMirror 6** over Monaco — ~10× smaller, ES-module-friendly, no worker
  needed.
- **No build step** — everything is `<script type="module">` straight from CDNs
  (jsdelivr, esm.sh). The whole UI is ~480 lines in one HTML file.
- **Vanilla JS only** — no React/Vue/Svelte. Keeps the surface area minimal.
- **No service worker.** The browser's HTTP cache + Pyodide's own cache headers
  are enough; adding a SW would complicate iteration without meaningful win.
