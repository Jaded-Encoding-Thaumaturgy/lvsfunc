from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from jetpytools import CustomStrEnum, CustomValueError
from vsdenoise import DFTTest, SLocationLike
from vsexprtools import norm_expr
from vsrgtools import repair
from vstools import (
    Planes,
    get_depth,
    normalize_param_planes,
    normalize_planes,
    scale_value,
    vs,
)

__all__: list[str] = [
    "WEAK_DITHER_FREQS",
    "LimitMode",
    "dedither",
    "post_dedither",
]


WEAK_DITHER_FREQS: SLocationLike = (
    (0.00, 0.00),
    (0.20, 0.00),
    (0.40, 0.25),
    (0.60, 0.75),
    (0.80, 1.50),
    (1.00, 2.00),
)


class LimitMode(CustomStrEnum):
    """Method used to constrain changes made by a filter."""

    CLAMP = "y x - {negative_limit} max {limit} min x +"
    """Clamp the filtered change to the permitted range."""

    REVERT = "x y - abs {limit} > x y ?"
    """Use the source pixel when the filtered change exceeds the limit."""

    def __call__(self, limit: float) -> str:
        return self.value.format(
            limit=limit,
            negative_limit=-limit,
        )


def _scale_plane_values(
    clip: vs.VideoNode,
    values: float | Sequence[float],
    planes: list[int],
) -> list[float]:
    normalised = normalize_param_planes(clip, values, planes, 0.0)

    is_yuv = clip.format.color_family is vs.YUV

    return [
        scale_value(
            value,
            8,
            clip,
            scale_offsets=False,
            chroma=is_yuv and plane > 0,
            family=clip,
        )
        for plane, value in enumerate(normalised)
    ]


def _limit_filter(
    source: vs.VideoNode,
    filtered: vs.VideoNode,
    limit: float | Sequence[float],
    mode: LimitMode,
    planes: list[int],
) -> vs.VideoNode:
    limits = _scale_plane_values(
        source,
        limit,
        planes,
    )

    expressions = tuple(mode(plane_limit) if plane in planes else "" for plane, plane_limit in enumerate(limits))

    return norm_expr(
        [source, filtered],
        expressions,
        planes=planes,
    )


def dedither(
    clip: vs.VideoNode,
    thr: float | Sequence[float] = 1.5,
    limit: float | Sequence[float] = 1.0,
    limit_mode: LimitMode = LimitMode.CLAMP,
    planes: Planes = 0,
) -> vs.VideoNode:
    """
    Reduces fine ordered dithering using conditional spatial smoothing.

    Processing is performed in two passes: horizontal and vertical.
    Each pass checks whether the opposing neighbours are similar and whether the current pixel
    is similar to the average of the two based on `thr`. If it passes these checks,
    the current pixel is replaced with the average of all its neighbours.
    The result is then repaired to prevent overshoot.

    Args:
        clip: Clip from which to dedither. Must be at least 16-bit.
        thr: Detection threshold, optionally per plane.
            Higher values will detect more dithering, but may also affect finer details.
            Recommended values are between 1.0 and 2.0. Defaults to 1.5.
        limit: Maximum permitted change, optionally per plane.
            Higher values will allow more changes, but may also oversmooth textures.
            If you find that this function is too strong, try decreasing this value.
            Defaults to 1.0.
        limit_mode: How changes exceeding `limit` are handled:

            - CLAMP: Restricts every candidate change to the range [-limit, limit].
            - REVERT: Keeps the source pixel if the filtered change exceeds the limit.

            See `LimitMode` for more information. Defaults to `LimitMode.CLAMP`.
        planes: Planes to process. Defaults to luma only.

    Returns:
        Clip with ordered dithering reduced.

    Raises:
        CustomValueError: If the input clip is not at least 16-bit.
    """

    if (x := get_depth(clip)) < 16:
        raise CustomValueError(
            f"The input clip must be 16-bit or higher, not {x}!",
            dedither,
        )

    nplanes = normalize_planes(clip, planes)
    thresholds = _scale_plane_values(clip, thr, nplanes)

    def _expressions(vertical: bool) -> tuple[str, ...]:
        if vertical:
            previous = "x[0,-1]"
            following = "x[0,1]"
        else:
            previous = "x[-1,0]"
            following = "x[1,0]"

        return tuple(
            (
                f"{previous} {following} - abs {threshold} < "
                f"x {previous} {following} + 2 / - abs "
                f"{threshold * 2} < and "
                f"x 2 * {previous} {following} + + 4 / "
                "x ?"
            )
            if plane in nplanes
            else ""
            for plane, threshold in enumerate(thresholds)
        )

    h_pass = norm_expr(clip, _expressions(False), planes=nplanes, boundary=True)
    hv_pass = norm_expr(h_pass, _expressions(True), planes=nplanes, boundary=True)

    rep_px = repair(clip, hv_pass, repair.Mode.MINMAX_SQUARE1, planes=nplanes)

    return _limit_filter(clip, rep_px, limit, limit_mode, nplanes)


def post_dedither(
    clip: vs.VideoNode,
    freqs: SLocationLike | DFTTest.SLocation.MultiDim = WEAK_DITHER_FREQS,
    limit: float | Sequence[float] | None = 0.5,
    limit_mode: LimitMode = LimitMode.CLAMP,
    planes: Planes = 0,
    **dft_kwargs: Any,
) -> vs.VideoNode:
    """
    Apply a weak DFTTest finishing pass to denoise residual dithering.

    This function is intended to be used after `dedither`.

    Args:
        clip: Clip to process.
        freqs: DFTTest frequency/strength settings; determines noise reduction by frequency.
        limit: Maximum allowed change. `None` disables limiting. Default: 0.5.
        limit_mode: How to apply the limiting:

            - CLAMP: Restricts every candidate change to the range [-limit, limit].
            - REVERT: Keeps the source pixel if the filtered change exceeds the limit.

            See `LimitMode` for more information. Defaults to `LimitMode.CLAMP`.
        planes: Planes to process. Defaults to luma only.
        **dft_kwargs: Additional keyword arguments for DFTTest.

    Returns:
        Frequency-filtered clip.
    """

    nplanes = normalize_planes(clip, planes)

    dft = DFTTest(**{"tr": 0, "sbsize": 16, "sosize": 12, **dft_kwargs})

    filtered = dft.denoise(clip, freqs, planes=nplanes)

    if limit is None:
        return filtered

    return _limit_filter(clip, filtered, limit, limit_mode, nplanes)
