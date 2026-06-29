from __future__ import annotations

from math import isqrt, log2
from typing import Final, overload

from jetpytools import CustomValueError, KwargsT, classproperty
from vsdenoise import (
    AnalyzeArgs,
    DegrainArgs,
    DFTTest,
    MotionMode,
    MVToolsPreset,
    RecalculateArgs,
    SADMode,
    SearchMode,
    prefilter_to_full_range,
)
from vstools import get_h, get_w, vs

__all__: list[str] = [
    "LightMVPresets",
    "SlocCurves",
    "autoselect_blksize",
    "autoselect_pel",
    "mv_refine_kwargs",
]


VALID_BLKSIZES: Final[frozenset[int]] = frozenset(2**i for i in range(2, 8))
_MAX_REFINE: Final[int] = max(bs.bit_length() - 3 for bs in VALID_BLKSIZES)


# TODO: Update all these once mvutensils is fully supported in vsjetpack.
class LightMVPresets:
    """MVTools motion-estimation presets."""

    @classproperty  # type: ignore[arg-type]
    def fast(self) -> MVToolsPreset:
        """
        MVTools preset optimized for speed, built on vodesfunc's ``MaybeNotTerrible``.

        This results in lower quality motion estimation, but is significantly faster.

        See: https://github.com/Vodes/vodesfunc/blob/ba3e209/vodesfunc/denoise.py#L13-L26
        """

        return MVToolsPreset(
            search_clip=lambda clip: prefilter_to_full_range(
                clip,
                slope=4.5,
            ),
            pel=1,
            analyze_args=AnalyzeArgs(
                truemotion=MotionMode.SAD,
                search=SearchMode.DIAMOND,
                pelsearch=2,
            ),
            recalculate_args=RecalculateArgs(
                truemotion=MotionMode.SAD,
                search=SearchMode.DIAMOND,
                searchparam=1,
            ),
        )

    @classproperty  # type: ignore[arg-type]
    def hq(self) -> MVToolsPreset:
        """
        MVTools preset optimized for quality.
        """

        return MVToolsPreset(
            search_clip=lambda clip: prefilter_to_full_range(
                clip,
                slope=4.5,
            ),
            pel=4,
            analyze_args=AnalyzeArgs(
                truemotion=MotionMode.COHERENCE,
                search=SearchMode.HEXAGON,
                pelsearch=2,
            ),
            recalculate_args=RecalculateArgs(
                truemotion=MotionMode.COHERENCE,
                search=SearchMode.HEXAGON,
                searchparam=1,
            ),
            degrain_args=DegrainArgs(thsad=75),
        )

    @classproperty  # type: ignore[arg-type]
    def heavy_grain(self) -> MVToolsPreset:
        """
        Preset optimized for heavily grained, super unstable sources.

        An example of this would be Kyousougiga's blu-rays.
        """

        return MVToolsPreset(
            search_clip=lambda clip: prefilter_to_full_range(
                DFTTest().denoise(clip, SlocCurves.Prefilter.Extreme),
                slope=4.5,
            ),
            pel=2,
            analyze_args=AnalyzeArgs(
                blksize=64,
                truemotion=MotionMode.SAD,
                search=SearchMode.HEXAGON,
                dct=SADMode.ADAPTIVE_SPATIAL_MIXED,
            ),
            recalculate_args=RecalculateArgs(
                truemotion=MotionMode.SAD,
                search=SearchMode.HEXAGON,
                searchparam=1,
                dct=SADMode.ADAPTIVE_SATD_MIXED,
            ),
            degrain_args=DegrainArgs(thsad=150),
        )


class SlocCurves:
    """DFTTest ``sloc`` preset curves."""

    class Prefilter:
        """Curves for MVTools prefiltering."""

        @classproperty  # type: ignore[arg-type]
        def Light(self) -> DFTTest.SLocation:  # noqa: N802
            """Preset for light-noise sources."""

            return DFTTest.SLocation(
                [
                    (0.0, 4.0),
                    (0.3, 8.0),
                    (0.35, 24.0),
                    (1.0, 16.0),
                ],
                interpolate=DFTTest.SLocation.InterMode.LINEAR,
            )

        @classproperty  # type: ignore[arg-type]
        def Standard(self) -> DFTTest.SLocation:  # noqa: N802
            """Preset for typical dithering strength."""

            return DFTTest.SLocation(
                [
                    (0.0, 4.0),
                    (0.3, 12.0),
                    (0.35, 48.0),
                    (0.65, 72.0),
                    (1.0, 12.0),
                ],
                interpolate=DFTTest.SLocation.InterMode.CUBIC,
            )

        @classproperty  # type: ignore[arg-type]
        def Grainy(self) -> DFTTest.SLocation:  # noqa: N802
            """Preset for grainy sources."""

            return DFTTest.SLocation(
                [
                    (0.0, 4.0),
                    (0.3, 24.0),
                    (0.35, 48.0),
                    (1.0, 96.0),
                ],
                interpolate=DFTTest.SLocation.InterMode.SPLINE_LINEAR,
            )

        @classproperty  # type: ignore[arg-type]
        def Extreme(self) -> DFTTest.SLocation:  # noqa: N802
            """Very heavy grain preset."""

            return DFTTest.SLocation(
                [
                    (0.0, 8.0),
                    (0.3, 24.0),
                    (0.35, 64.0),
                    (1.0, 128.0),
                ],
                interpolate=DFTTest.SLocation.InterMode.QUADRATIC,
            )

    class MFilter:
        """Curves for MVTools fallback denoise."""

        @classproperty  # type: ignore[arg-type]
        def Standard(self) -> DFTTest.SLocation:  # noqa: N802
            """Preset for light-noise sources."""

            return DFTTest.SLocation(
                [
                    (0.0, 0.0),
                    (0.3, 0.3),
                    (0.35, 1.5),
                    (1.0, 4.0),
                ],
                interpolate=DFTTest.SLocation.InterMode.LINEAR,
            )

        @classproperty  # type: ignore[arg-type]
        def Heavy(self) -> DFTTest.SLocation:  # noqa: N802
            """Preset for heavy-noise sources."""

            return DFTTest.SLocation(
                [
                    (0.0, 0.5),
                    (0.3, 1.0),
                    (0.35, 2.0),
                    (1.0, 8.0),
                ],
                interpolate=DFTTest.SLocation.InterMode.SPLINE_LINEAR,
            )


def autoselect_pel(clip: vs.VideoNode) -> int:
    """
    Automatically select the pel value based on the clip's dimension.

    Uses pel=4 for SD, pel=2 for HD, and pel=1 for UHD/4K and above.

    :param clip:    The clip to select the pel for.
    :return:        pel for MVTools.
    """

    w, h = clip.width, clip.height

    if w <= 1024 or h <= 576:
        return 4

    if w <= 2048 or h <= 1440:
        return 2

    return 1


@overload
def autoselect_blksize(width_or_clip: vs.VideoNode) -> int: ...


@overload
def autoselect_blksize(width_or_clip: int, height: int) -> int: ...


@overload
def autoselect_blksize(width_or_clip: int) -> int: ...


@overload
def autoselect_blksize(width_or_clip: None, height: int) -> int: ...


def autoselect_blksize(width_or_clip: int | vs.VideoNode | None = None, height: int | None = None) -> int:
    """
    Automatically select MVTools block size from clip dimensions or a VideoNode.

    If either width or height is passed, the other will be automatically determined (assuming 16:9 aspect ratio).
    If a VideoNode is passed, its dimensions will be used.

    :param width_or_clip: Clip width or a VideoNode.
    :param height:        Clip height. If `width_or_clip` is a VideoNode, this should be None.

    :return:              A valid MVTools block size.
    """

    width: int | None = None

    if isinstance(width_or_clip, vs.VideoNode):
        width = width_or_clip.width
        height = width_or_clip.height

    if isinstance(width_or_clip, int):
        width = width_or_clip

    if width is not None and height is None:
        height = get_h(width, 16 / 9, mod=2)

    if width is None and isinstance(height, int):
        width = get_w(height, 16 / 9, mod=2)

    if width is None or height is None:
        raise CustomValueError(
            f"You must pass either a VideoNode, width, or height! Not {type(width_or_clip)}!",
            autoselect_blksize,
        )

    diag = isqrt(int(width) * int(height))
    ref_diag = isqrt(1920 * 1080)

    exponent = round(log2(diag / ref_diag * 64))

    exponent = max(
        int(log2(min(VALID_BLKSIZES))),
        min(int(log2(max(VALID_BLKSIZES))), exponent),
    )

    return 2**exponent


def mv_refine_kwargs(
    blksize: int | None = None,
    max_refine: int = _MAX_REFINE,
    *,
    ref: vs.VideoNode | None = None,
) -> KwargsT:
    """
    Generate kwargs for MVTools blksize refining.

    :param blksize:     The block size to use. If None, automatically determine based on
                        the reference clip's dimensions.
    :param max_refine:  Cap on refinement steps (halving blksize down to 4).
    :param ref:         The reference clip to use. Must be set if `blksize` is None.

    :return:            Kwargs containing `blksize` and `refine` keywords for MVTools.
    """

    if blksize is None:
        if not ref:
            raise CustomValueError("`ref` must be set if `blksize` is None!", mv_refine_kwargs)

        blksize = autoselect_blksize(ref)

    if blksize not in VALID_BLKSIZES:
        raise CustomValueError(
            f"Invalid blksize: {blksize}! Valid values are {sorted(VALID_BLKSIZES)}.",
            mv_refine_kwargs,
        )

    return {"blksize": blksize, "refine": min(max(0, blksize.bit_length() - 3), max_refine)}
