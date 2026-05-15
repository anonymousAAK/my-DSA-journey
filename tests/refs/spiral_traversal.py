"""Reference: spiral order traversal of an m x n matrix."""

from __future__ import annotations
from typing import List


def spiralOrder(mat: List[List[int]]) -> List[int]:
    result: List[int] = []
    if not mat or not mat[0]:
        return result
    top, bottom = 0, len(mat) - 1
    left, right = 0, len(mat[0]) - 1
    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            result.append(mat[top][i])
        top += 1
        for i in range(top, bottom + 1):
            result.append(mat[i][right])
        right -= 1
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(mat[bottom][i])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(mat[i][left])
            left += 1
    return result
