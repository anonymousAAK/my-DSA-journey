"""Tests for maze.py. Run: python test_maze.py"""
from __future__ import annotations

import sys

from maze import astar, bfs, dfs, dijkstra, generate


def test_generated_maze_is_connected() -> None:
    m = generate(15, 15, seed=1)
    # BFS from (0,0) should reach every cell (recursive backtracker -> spanning tree)
    from collections import deque
    seen = {(0, 0)}
    q = deque([(0, 0)])
    while q:
        cur = q.popleft()
        for nb in m.neighbors(cur):
            if nb not in seen:
                seen.add(nb)
                q.append(nb)
    assert len(seen) == 15 * 15, f"only {len(seen)} of {15*15} cells reachable"


def test_each_algorithm_finds_a_path() -> None:
    for seed in (1, 7, 42, 123):
        m = generate(11, 11, seed=seed)
        start, goal = (0, 0), (10, 10)
        for fn in (bfs, dfs, dijkstra, astar):
            r = fn(m, start, goal)
            assert r.path, f"{fn.__name__} found no path (seed={seed})"
            assert r.path[0] == start and r.path[-1] == goal
            # Path must be valid: every consecutive pair must be a maze neighbour.
            for a, b in zip(r.path, r.path[1:]):
                assert b in list(m.neighbors(a)), f"{fn.__name__}: {a}->{b} not a neighbour"


def test_bfs_path_le_dfs_path() -> None:
    # BFS gives shortest path in an unweighted graph; DFS in general does not.
    for seed in range(1, 11):
        m = generate(15, 15, seed=seed)
        s, g = (0, 0), (14, 14)
        assert bfs(m, s, g).path_length <= dfs(m, s, g).path_length


def test_astar_explores_le_dijkstra() -> None:
    # On a unit-weight maze, A* with admissible Manhattan heuristic should
    # explore <= Dijkstra. Equality is fine when the heuristic carries no info.
    for seed in range(1, 11):
        m = generate(21, 21, seed=seed)
        s, g = (0, 0), (20, 20)
        a = astar(m, s, g)
        d = dijkstra(m, s, g)
        assert a.explored <= d.explored, f"seed={seed}: A* {a.explored} > Dijkstra {d.explored}"
        # And A* should still return a path of the same length as Dijkstra
        assert a.path_length == d.path_length


def test_weighted_dijkstra() -> None:
    m = generate(7, 7, seed=99)
    # Bump some weights; verify Dijkstra still works and produces a valid path
    m.weights[3][3] = 50
    m.weights[3][4] = 50
    r = dijkstra(m, (0, 0), (6, 6))
    assert r.path and r.path[0] == (0, 0) and r.path[-1] == (6, 6)


def test_json_roundtrip_shape() -> None:
    m = generate(5, 5, seed=3)
    s = m.to_json()
    import json
    obj = json.loads(s)
    assert obj["rows"] == 5 and obj["cols"] == 5
    assert len(obj["walls"]) == 5 and len(obj["walls"][0]) == 5


def main() -> int:
    test_generated_maze_is_connected()
    test_each_algorithm_finds_a_path()
    test_bfs_path_le_dfs_path()
    test_astar_explores_le_dijkstra()
    test_weighted_dijkstra()
    test_json_roundtrip_shape()
    print("maze: all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
