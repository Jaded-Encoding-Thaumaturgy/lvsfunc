from __future__ import annotations

from uuid import uuid4

import numpy as np
import pytest
from jetpytools import CustomValueError
from vsdenoise import DFTTest, MVToolsPreset
from vstools import core

from lvsfunc.presets.mv import LightMVPresets, SlocCurves, autoselect_blksize, autoselect_pel, mv_refine_kwargs
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


@pytest.mark.parametrize(
    "width, height, expected",
    [
        (640, 480, 32),
        (720, 576, 32),
        (1280, 720, 32),
        (1920, 1080, 64),
        (3840, 2160, 128),
    ],
)
def test_autoselect_blksize_selects_correct_blksize(width: int, height: int, expected: int) -> None:
    assert autoselect_blksize(width, height) == expected


def test_mv_refine_kwargs_autoselects_from_ref() -> None:
    clip = core.std.BlankClip(width=1920, height=1080)

    assert mv_refine_kwargs(ref=clip) == {"blksize": 64, "refine": 4}


def test_mv_refine_kwargs_caps_refine() -> None:
    clip = core.std.BlankClip(width=1920, height=1080)

    assert mv_refine_kwargs(max_refine=2, ref=clip) == {"blksize": 64, "refine": 2}


def test_mv_refine_kwargs_accepts_explicit_blksize() -> None:
    assert mv_refine_kwargs(blksize=32, max_refine=1) == {"blksize": 32, "refine": 1}


def test_mv_refine_kwargs_requires_ref_when_blksize_omitted() -> None:
    with pytest.raises(CustomValueError, match="`ref` must be set"):
        mv_refine_kwargs()


def test_mv_refine_kwargs_rejects_invalid_blksize() -> None:
    with pytest.raises(CustomValueError, match="Invalid blksize"):
        mv_refine_kwargs(blksize=12)


@pytest.mark.parametrize(
    ("preset", "pel"),
    [
        (LightMVPresets.fast, 1),
        (LightMVPresets.hq, 4),
        (LightMVPresets.heavy_grain, 2),
    ],
)
def test_light_mv_presets_expose_expected_pel(preset: MVToolsPreset, pel: int) -> None:
    assert preset.pel == pel
    assert preset.analyze_args is not None
    assert preset.recalculate_args is not None


@pytest.mark.parametrize(
    "sloc",
    [
        SlocCurves.Prefilter.Light,
        SlocCurves.Prefilter.Grainy,
        SlocCurves.MFilter.Heavy,
    ],
)
def test_remaining_sloc_presets_are_expanded(sloc: DFTTest.SLocation) -> None:
    assert len(sloc) > 4
    assert sloc[0.0] >= 0.0
    assert sloc[1.0] > 0.0
