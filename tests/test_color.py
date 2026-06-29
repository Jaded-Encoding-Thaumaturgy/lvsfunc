from __future__ import annotations

import pytest
from jetpytools import NotFoundEnumValue
from vstools import core, vs

from lvsfunc.color import RGBColor


@pytest.mark.parametrize(
    ("colour", "expected"),
    [
        (RGBColor.RED, (1.0, 0.0, 0.0)),
        (RGBColor.GREEN, (0.0, 1.0, 0.0)),
        (RGBColor.BLUE, (0.0, 0.0, 1.0)),
        (RGBColor.BLACK, (0.0, 0.0, 0.0)),
        (RGBColor.WHITE, (1.0, 1.0, 1.0)),
    ],
)
def test_rgb_color_values(colour: RGBColor, expected: tuple[float, float, float]) -> None:
    assert colour == expected


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("red", RGBColor.RED),
        ("RED", RGBColor.RED),
        ("forest_green", RGBColor.FOREST_GREEN),
        ("Forest_Green", RGBColor.FOREST_GREEN),
    ],
)
def test_rgb_color_from_name(name: str, expected: RGBColor) -> None:
    assert RGBColor.from_name(name) is expected


def test_rgb_color_from_name_rejects_unknown_name() -> None:
    with pytest.raises(NotFoundEnumValue):
        RGBColor.from_name("not-a-colour")


@pytest.mark.parametrize(
    ("colour", "bitdepth", "expected"),
    [
        (RGBColor.BLACK, 8, [16, 16, 16]),
        (RGBColor.WHITE, 8, [235, 235, 235]),
        (RGBColor.RED, 10, [940, 64, 64]),
        (RGBColor.GREEN, 10, [64, 940, 64]),
        (RGBColor.BLUE, 16, [4096, 4096, 60160]),
    ],
)
def test_rgb_color_scale_value(colour: RGBColor, bitdepth: int, expected: list[int]) -> None:
    assert colour.scale_value(bitdepth) == expected  # type: ignore[arg-type]


def test_rgb_color_to_clip_without_ref() -> None:
    clip = RGBColor.RED.to_clip()

    assert clip.format.color_family == vs.RGB
    assert clip.format.sample_type == vs.FLOAT


def test_rgb_color_to_clip_matches_rgb_reference_format() -> None:
    ref = core.std.BlankClip(format=vs.RGB24, width=64, height=64)

    clip = RGBColor.GREEN.to_clip(ref)

    assert clip.format.id == ref.format.id
    assert (clip.width, clip.height) == (ref.width, ref.height)


def test_rgb_color_to_clip_matches_yuv_reference_format() -> None:
    ref = core.std.BlankClip(format=vs.YUV420P8, width=64, height=64)

    clip = RGBColor.BLUE.to_clip(ref)

    assert clip.format.id == ref.format.id
    assert (clip.width, clip.height) == (ref.width, ref.height)
