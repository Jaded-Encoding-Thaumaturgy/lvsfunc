from __future__ import annotations

import pytest
from jetpytools import CustomValueError

from lvsfunc.diff.strategies import PlaneAvgFloatDiff, PlaneStatsDiff


@pytest.mark.parametrize("threshold", [-129, 129])
def test_plane_stats_diff_out_of_range_threshold(threshold: int) -> None:
    with pytest.raises(CustomValueError):
        PlaneStatsDiff(threshold)


@pytest.mark.parametrize("threshold", [-1.0, 2.0])
def test_plane_avg_float_diff_out_of_range_threshold(threshold: float) -> None:
    with pytest.raises(CustomValueError):
        PlaneAvgFloatDiff(threshold)
