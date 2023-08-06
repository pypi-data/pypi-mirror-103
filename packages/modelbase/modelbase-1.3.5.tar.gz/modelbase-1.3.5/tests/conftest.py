from __future__ import annotations

import pytest


def _multiline_comparison(expected: list[str], test: str):
    for l1, l2 in zip(expected, test.split("\n")):
        assert l1 == l2.strip("\r")  # for windows


@pytest.fixture()
def multiline_comparison():
    return _multiline_comparison
