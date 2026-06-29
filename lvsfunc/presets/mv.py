from __future__ import annotations

from jetpytools import classproperty
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
from vstools import vs

__all__: list[str] = [
    "LightMVPresets",
    "SlocCurves",
    "autoselect_pel",
]


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
