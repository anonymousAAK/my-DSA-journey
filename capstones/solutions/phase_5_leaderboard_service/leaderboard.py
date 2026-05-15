"""Leaderboard service: Fenwick tree (BIT) over fixed-range integer scores,
exposed as a tiny stdlib HTTP API.

Endpoints (all JSON in, JSON out):
- ``POST /score``      body: {"player": "...", "score": int}
- ``GET  /rank/<player>``                        -> {"player": "...", "rank": int, "score": int}
- ``GET  /top/<k>``                              -> [{"player": "...", "score": int}, ...]
- ``GET  /range/<lo>/<hi>``                      -> {"count": int}  (players with score in [lo, hi])

Run ``python leaderboard.py`` to start a demo server on :8765 and to
exercise it with a few sample requests. Stops cleanly on Ctrl-C.
"""
from __future__ import annotations

import json
import sys
import threading
import urllib.request
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


# --- Fenwick tree (BIT) ------------------------------------------------------

class BIT:
    """1-indexed Fenwick tree over scores in [1, max_score]. Stores *counts*
    of players currently at each score."""

    def __init__(self, max_score: int) -> None:
        if max_score < 1:
            raise ValueError("max_score must be >= 1")
        self.n = max_score
        self.tree = [0] * (max_score + 1)

    def update(self, idx: int, delta: int) -> None:
        if not (1 <= idx <= self.n):
            raise ValueError(f"idx {idx} out of range [1, {self.n}]")
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx

    def prefix_sum(self, idx: int) -> int:
        if idx < 1:
            return 0
        if idx > self.n:
            idx = self.n
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & -idx
        return s

    def range_sum(self, lo: int, hi: int) -> int:
        if lo > hi:
            return 0
        return self.prefix_sum(hi) - self.prefix_sum(lo - 1)

    def total(self) -> int:
        return self.prefix_sum(self.n)


# --- Leaderboard core --------------------------------------------------------

@dataclass
class Leaderboard:
    max_score: int = 10_000

    def __post_init__(self) -> None:
        self.bit = BIT(self.max_score)
        self.scores: dict[str, int] = {}
        self._lock = threading.Lock()

    def set_score(self, player: str, score: int) -> None:
        if not (1 <= score <= self.max_score):
            raise ValueError(f"score must be in [1, {self.max_score}]")
        with self._lock:
            old = self.scores.get(player)
            if old is not None:
                self.bit.update(old, -1)
            self.scores[player] = score
            self.bit.update(score, +1)

    def rank_of(self, player: str) -> tuple[int, int]:
        """Return (rank, score). Rank 1 = highest score. Players tied at the
        same score share the same rank (the standard '1224' competition style)."""
        with self._lock:
            if player not in self.scores:
                raise KeyError(player)
            s = self.scores[player]
            higher = self.bit.range_sum(s + 1, self.max_score)
            return higher + 1, s

    def count_in_range(self, lo: int, hi: int) -> int:
        with self._lock:
            return self.bit.range_sum(lo, hi)

    def top_k(self, k: int) -> list[tuple[str, int]]:
        """Return up to k (player, score) pairs sorted by score desc, then name asc."""
        with self._lock:
            items = sorted(self.scores.items(), key=lambda kv: (-kv[1], kv[0]))
            return items[:k]


# --- HTTP layer --------------------------------------------------------------

LB = Leaderboard()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: Any) -> None:  # silence default logger
        return

    def _send(self, code: int, body: Any) -> None:
        payload = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self) -> None:
        if self.path != "/score":
            return self._send(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length") or 0)
        try:
            data = json.loads(self.rfile.read(length).decode() or "{}")
            player = str(data["player"])
            score = int(data["score"])
            LB.set_score(player, score)
            return self._send(200, {"ok": True, "player": player, "score": score})
        except (KeyError, ValueError, TypeError, json.JSONDecodeError) as e:
            return self._send(400, {"error": str(e)})

    def do_GET(self) -> None:
        parts = [p for p in self.path.split("/") if p]
        try:
            if len(parts) == 2 and parts[0] == "rank":
                rank, score = LB.rank_of(parts[1])
                return self._send(200, {"player": parts[1], "rank": rank, "score": score})
            if len(parts) == 2 and parts[0] == "top":
                k = int(parts[1])
                if k < 0:
                    raise ValueError("k must be >= 0")
                return self._send(200, [{"player": p, "score": s} for p, s in LB.top_k(k)])
            if len(parts) == 3 and parts[0] == "range":
                lo, hi = int(parts[1]), int(parts[2])
                return self._send(200, {"count": LB.count_in_range(lo, hi)})
            return self._send(404, {"error": "not found"})
        except KeyError:
            return self._send(404, {"error": "player not found"})
        except (ValueError, TypeError) as e:
            return self._send(400, {"error": str(e)})


def serve(port: int = 8765) -> HTTPServer:
    server = HTTPServer(("127.0.0.1", port), Handler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server


def _hit(method: str, path: str, body: Any = None, port: int = 8765) -> Any:
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json"} if data else {},
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main() -> int:
    port = 8765
    server = serve(port)
    print(f"leaderboard demo on http://127.0.0.1:{port}")
    try:
        for player, score in [("alice", 50), ("bob", 80), ("carol", 30),
                              ("dave", 80), ("eve", 95)]:
            print(_hit("POST", "/score", {"player": player, "score": score}))
        print("top 3:", _hit("GET", "/top/3"))
        print("rank alice:", _hit("GET", "/rank/alice"))
        print("range 40..90:", _hit("GET", "/range/40/90"))
        # update alice and re-query
        _hit("POST", "/score", {"player": "alice", "score": 99})
        print("after alice=99, rank alice:", _hit("GET", "/rank/alice"))
        print("after alice=99, top 3:", _hit("GET", "/top/3"))
    finally:
        server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
