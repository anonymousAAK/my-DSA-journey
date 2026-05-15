"""Tests for leaderboard.py. Run: python test_leaderboard.py"""
from __future__ import annotations

import sys
import time

from leaderboard import BIT, Leaderboard, _hit, serve


def test_bit_basic() -> None:
    b = BIT(10)
    for i in [3, 3, 7, 1, 10]:
        b.update(i, 1)
    assert b.total() == 5
    assert b.prefix_sum(3) == 3   # values <= 3: {1, 3, 3}
    assert b.range_sum(4, 10) == 2  # values in [4,10]: {7, 10}
    assert b.range_sum(11, 20) == 0  # out of range returns 0
    b.update(3, -1)
    assert b.prefix_sum(3) == 2


def test_leaderboard_rank() -> None:
    lb = Leaderboard(max_score=1000)
    lb.set_score("alice", 50)
    lb.set_score("bob", 90)
    lb.set_score("carol", 30)
    assert lb.rank_of("bob")[0] == 1
    assert lb.rank_of("alice")[0] == 2
    assert lb.rank_of("carol")[0] == 3
    # Update alice; ranks shift
    lb.set_score("alice", 95)
    assert lb.rank_of("alice")[0] == 1
    assert lb.rank_of("bob")[0] == 2


def test_ties_share_rank() -> None:
    lb = Leaderboard(max_score=100)
    lb.set_score("a", 80)
    lb.set_score("b", 80)
    lb.set_score("c", 70)
    # a and b are tied; both should be rank 1, c rank 3 (competition style)
    assert lb.rank_of("a")[0] == 1
    assert lb.rank_of("b")[0] == 1
    assert lb.rank_of("c")[0] == 3


def test_top_k_order() -> None:
    lb = Leaderboard(max_score=100)
    for name, score in [("zara", 50), ("anna", 90), ("mike", 90), ("bob", 30)]:
        lb.set_score(name, score)
    top = lb.top_k(3)
    # 90s come first (tied -> alpha), then 50, then 30 (which wouldn't be in top 3)
    assert top == [("anna", 90), ("mike", 90), ("zara", 50)]


def test_range_count() -> None:
    lb = Leaderboard(max_score=100)
    for v in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]:
        lb.set_score(f"p{v}", v)
    assert lb.count_in_range(20, 60) == 5
    assert lb.count_in_range(1, 5) == 0
    assert lb.count_in_range(95, 100) == 1


def test_http_endpoints() -> None:
    port = 8767  # avoid the demo port
    server = serve(port)
    try:
        # POST scores
        for name, score in [("alice", 50), ("bob", 80), ("carol", 30)]:
            r = _hit("POST", "/score", {"player": name, "score": score}, port=port)
            assert r["ok"] is True

        # rank
        r = _hit("GET", "/rank/bob", port=port)
        assert r["rank"] == 1 and r["score"] == 80

        # top
        r = _hit("GET", "/top/2", port=port)
        assert [x["player"] for x in r] == ["bob", "alice"]

        # range
        r = _hit("GET", "/range/40/100", port=port)
        assert r["count"] == 2

        # update + re-query
        _hit("POST", "/score", {"player": "carol", "score": 99}, port=port)
        r = _hit("GET", "/rank/carol", port=port)
        assert r["rank"] == 1

        # error cases
        try:
            _hit("GET", "/rank/nobody", port=port)
            raise AssertionError("expected 404")
        except Exception as e:  # urllib raises HTTPError for non-2xx
            assert "404" in str(e) or "not found" in str(e).lower()
    finally:
        server.shutdown()
        time.sleep(0.05)


def main() -> int:
    test_bit_basic()
    test_leaderboard_rank()
    test_ties_share_rank()
    test_top_k_order()
    test_range_count()
    test_http_endpoints()
    print("leaderboard: all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
