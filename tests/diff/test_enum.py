from __future__ import annotations

import pytest

from lvsfunc.diff.enum import DiffMode


@pytest.mark.parametrize(
    ("mode", "results", "expected"),
    [
        # Empty lists
        (DiffMode.ANY, [], False),
        (DiffMode.ALL, [], False),
        # No differences
        (DiffMode.ANY, [False, False], False),
        # One difference
        (DiffMode.ANY, [False, True], True),
        (DiffMode.ONE_OR_MORE, [False, True], True),
        # All differences
        (DiffMode.ALL, [True, True], True),
        (DiffMode.ALL, [True, False], False),
        # Majority differences
        (DiffMode.MAJORITY, [True, False], False),
        (DiffMode.MAJORITY, [True, True, False], True),
        # Most differences
        (DiffMode.MOST, [True, False, False, False], False),
        (DiffMode.MOST, [True, True, True, False], True),
    ],
)
def test_diff_mode_check_result(mode: DiffMode, results: list[bool], expected: bool) -> None:
    assert mode.check_result(results) is expected
