from __future__ import annotations

from uuid import uuid4

import numpy as np
import pytest
from vsdenoise import DFTTest
from vstools import core

from lvsfunc.presets.mv import SlocCurves, autoselect_pel
from lvsfunc.util import sloc_curve_to_graph


def test_prefilter_presets_are_expanded() -> None:
    sloc: DFTTest.SLocation = SlocCurves.Prefilter.Standard

    assert len(sloc) > 4
    assert sloc[0.0] == 4.0
    assert sloc[1.0] == 12.0


def test_mfilter_presets_are_expanded() -> None:
    sloc: DFTTest.SLocation = SlocCurves.MFilter.Standard

    assert len(sloc) > 4
    assert sloc[0.0] == 0.0
    assert sloc[1.0] == 4.0


def test_sloc_curve_to_graph_returns_matplotlib_figure() -> None:
    slocation: DFTTest.SLocation = SlocCurves.Prefilter.Extreme
    expected = slocation.interpolate(res=100)

    uuid = uuid4()
    fig = sloc_curve_to_graph(slocation, res=100, title=f"test-{uuid}")

    ax = fig.axes[0]

    assert ax.get_title() == f"test-{uuid}"
    assert len(ax.lines) == 1

    if len(slocation) <= 8:
        assert len(ax.collections) == 1
        assert list(np.asarray(ax.collections[0].get_offsets()).T[1]) == pytest.approx(list(slocation.sigmas))

    assert list(np.asarray(ax.lines[0].get_ydata())) == pytest.approx(list(expected.sigmas))


@pytest.mark.parametrize(
    "width, height, expected",
    [
        (1024, 576, 4),
        (1920, 1080, 2),
        (2048, 1440, 2),
        (2560, 1440, 2),
        (3840, 2160, 1),
    ],
)
def test_autoselect_pel_selects_correct_pel(width: int, height: int, expected: int) -> None:
    clip = core.std.BlankClip(width=width, height=height)

    assert autoselect_pel(clip) == expected
