from __future__ import annotations

from jetpytools import CustomValueError
from vskernels import Catrom
from vssource import BestSource
from vstools import (
    FramePropError,
    FrameRangeN,
    FrameRangesN,
    Matrix,
    ResolutionsMismatchError,
    check_variable,
    depth,
    get_depth,
    limiter,
    normalize_ranges,
    replace_ranges,
    vs,
)

__all__ = ["overlay_sign"]


def overlay_sign(
    clip: vs.VideoNode,
    overlay: vs.VideoNode | str,
    frame_ranges: FrameRangeN | FrameRangesN | None = None,
    fade_length: int = 0,
    matrix: Matrix | int | None = None,
) -> vs.VideoNode:
    """
    Overlay a logo or sign onto another clip.

    This is a rewrite of fvsfunc.InsertSign.

    This wrapper also allows you to set fades to fade a logo in and out.

    Args:
        clip: Clip to process.
        overlay: Sign or logo to overlay.
            Must be the png loaded in through :py:func:`core.vapoursynth.imwri.Read`
            or a path string to the image file, and **MUST** be the same dimensions
            as the ``clip`` to process.
        frame_ranges: Frame ranges or starting frame to apply the overlay to.
            See :py:attr:`vstools.FrameRange` for more info.
            If ``None``, overlays the entire clip.
            If a FrameRange is passed, the overlaid clip will only show up inside that range.
            If only a single integer is given, it will start on that frame and stay until the end
            of the clip.
            Note that this function only accepts a single FrameRange!
            You can't pass a list of them!
        fade_length: Length to fade the clips into each other.
            The fade will start and end on the frames given in ``frame_ranges``.
            If set to ``0``, it won't fade and the sign will simply pop in.
        matrix: Enum for the matrix of the clip to process.
            See :py:attr:`lvsfunc.types.Matrix` for more info.
            If not specified, gets matrix from the ``_Matrix`` prop of the clip unless it's an RGB
            clip, in which case it stays as ``None``.

    Returns:
        Clip with a logo or sign overlaid on top for the given frame ranges,
        either with or without a fade.

    Raises:
        ValueError: ``overlay`` is not a VideoNode or a path.
        ResolutionsMismatchError: The overlay clip is not the same dimensions as the input clip.
        InvalidMatrixError: ``matrix`` is an invalid value.
        FramePropError: Overlay does not have an alpha channel.
        FramePropError: Overlay clip was not loaded using :py:func:`vapoursynth.core.imwri.Read`.
    """

    if fade_length > 0:
        from kagefunc import crossfade

    assert check_variable(clip, overlay_sign)

    if is_string_path := isinstance(overlay, str):
        overlay = BestSource.source(str(overlay))

    if not isinstance(overlay, vs.VideoNode):
        raise CustomValueError("`overlay` must be a VideoNode object or a string path!", overlay_sign)

    assert check_variable(overlay, overlay_sign)

    ResolutionsMismatchError.check(overlay_sign, clip, overlay)

    if isinstance(frame_ranges, list) and len(frame_ranges) > 1:
        import warnings

        warnings.warn("overlay_sign: 'Only one range is currently supported! Grabbing the first item in list.'")
        frame_ranges = frame_ranges[0]

    overlay = Catrom().resample(overlay, clip, Matrix.from_param_or_video(matrix, clip))
    overlay = overlay[0] * clip.num_frames

    try:
        mask = overlay.std.PropToClip("_Alpha")
    except vs.Error:
        if is_string_path:
            raise FramePropError(overlay_sign, "Your image must have an alpha channel (transparency)!")

        raise FramePropError(overlay_sign, "You must load in the sign using `imwri.Read`!")

    merge = clip.std.MaskedMerge(overlay, depth(mask, get_depth(overlay)))
    merge = limiter(merge, func=overlay_sign)

    if not frame_ranges:
        return merge

    if fade_length > 0:
        if isinstance(frame_ranges, int):
            return crossfade(clip[: frame_ranges + fade_length], merge[frame_ranges:], fade_length)

        start, end = normalize_ranges(clip, frame_ranges)[0]

        merge = crossfade(clip[: start + fade_length], merge[start:], fade_length)

        return crossfade(merge[:end], clip[end - fade_length :], fade_length)

    return replace_ranges(clip, merge, frame_ranges)
