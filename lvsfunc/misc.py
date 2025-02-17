from __future__ import annotations

from typing import cast

from vskernels import Catrom
from vstools import (
    CustomValueError, DependencyNotFoundError, FileWasNotFoundError, FramePropError,
    FrameRangeN, FrameRangesN, Matrix, ResolutionsMismatchError, SPath, SPathLike,
    check_variable, core, depth, get_depth, limiter, normalize_ranges, replace_ranges, vs
)

__all__ = [
    'overlay_sign'
]


def overlay_sign(
    clip: vs.VideoNode, overlay: vs.VideoNode | SPathLike,
    frame_ranges: FrameRangeN | FrameRangesN | None = None, fade_length: int = 0,
    matrix: Matrix | int | None = None, return_mask: bool = False
) -> vs.VideoNode:
    """
    Overlay a logo or sign onto another clip.

    This is a rewrite of fvsfunc.InsertSign.

    `overlay` can be a VideoNode or a path to an image file, and must have an alpha channel.
    This wrapper also allows you to set fades to fade a logo in and out.

    Dependencies:

    * `kagefunc <https://github.com/Irrational-Encoding-Wizardry/kagefunc>`_ (optional: ``fade_length``)

    :param clip:                    Clip to process.
    :param overlay:                 Sign or logo to overlay. Must be the png loaded in
                                    through :py:func:`core.vapoursynth.imwri.Read` or a path string to the image file,
                                    and **MUST** be the same dimensions as the ``clip`` to process.
                                    The clip **MUST** also have an alpha channel.
    :param frame_ranges:            Frame ranges or starting frame to apply the overlay to.
                                    See :py:attr:`vstools.FrameRange` for more info.
                                    If None, overlays the entire clip.
                                    If a FrameRange is passed, the overlaid clip will only show up inside that range.
                                    If only a single integer is given, it will start on that frame and
                                    stay until the end of the clip.
                                    Note that this function only accepts a single FrameRange!
                                    You can't pass a list of them!
    :param fade_length:             Length to fade the clips into each other.
                                    The fade will start and end on the frames given in frame_ranges.
                                    If set to 0, it won't fade and the sign will simply pop in.
    :param matrix:                  Enum for the matrix of the Clip to process.
                                    See :py:attr:`vstools.types.Matrix` for more info.
                                    If not specified, gets matrix from the "_Matrix" prop of the input clip.
    :param return_mask:             Whether to return the mask of the overlay. Default: False.

    :return:                        Clip with a logo or sign overlaid on top for the given frame ranges,
                                    either with or without a fade.

    :raises DependencyNotFoundError:        `fade_length` > 0 and dependencies are missing.
    :raises ValueError:                     ``overlay`` is not a VideoNode or a path.
    :raises ResolutionsMismatchError:       The overlay clip is not of the same dimensions as the input clip.
    :raises InvalidMatrixError:             ``Matrix`` is an invalid value.
    :raises FramePropError:                 Overlay does not have an alpha channel.
    :raises FramePropError:                 Overlay clip was not loaded in using :py:func:`vapoursynth.core.imwri.Read`.
    """

    if fade_length > 0:
        try:
            from kagefunc import crossfade
        except ModuleNotFoundError as e:
            raise DependencyNotFoundError(overlay_sign, e, reason="fade_length > 0")

    assert check_variable(clip, overlay_sign)

    matrix = matrix or Matrix.from_video(clip)

    if isinstance(overlay, SPathLike):
        overlay = _get_overlay_from_file(overlay)
    elif not isinstance(overlay, vs.VideoNode):
        raise CustomValueError('`overlay` must be a VideoNode object or a path to an image file!', overlay_sign)

    overlay = cast(vs.VideoNode, overlay)

    assert check_variable(overlay, overlay_sign)

    ResolutionsMismatchError.check(overlay_sign, clip, overlay)

    if isinstance(frame_ranges, list) and len(frame_ranges) > 1:
        import warnings
        warnings.warn("overlay_sign: 'Only one range is currently supported! Grabbing the first item in list.'")
        frame_ranges = frame_ranges[0]

    overlay = _resample_overlay_matrix(overlay, clip, matrix)
    overlay = overlay[0] * clip.num_frames

    merged = _merge_with_mask(clip, overlay, return_mask)

    if return_mask or not frame_ranges:
        return merged

    if fade_length > 0:
        return _overlay_fade(clip, merged, fade_length, frame_ranges)

    return replace_ranges(clip, merged, frame_ranges)


def _get_overlay_from_file(overlay: SPathLike) -> vs.VideoNode:
    spath = SPath(overlay)

    if not spath.exists():
        raise FileWasNotFoundError(f"The given path, \"{spath}\" does not exist!", overlay_sign)

    if hasattr(core, 'bs'):
        return core.bs.VideoSource(overlay)

    return core.imwri.Read(overlay, alpha=True)


def _resample_overlay_matrix(
    overlay: vs.VideoNode, clip: vs.VideoNode, matrix: Matrix | int | None
) -> vs.VideoNode:
    """Resample the overlay to the clip's format and matrix."""

    if overlay.format.color_family is clip.format.color_family:
        return overlay

    if clip.format.color_family is vs.RGB:
        return Catrom.resample(overlay, clip.format.id, matrix_in=matrix)

    return Catrom.resample(overlay, clip.format.id, matrix)


def _merge_with_mask(
    clip: vs.VideoNode, overlay: vs.VideoNode, return_mask: bool = False
) -> vs.VideoNode:
    """Extract alpha mask and merge the overlay with the base clip."""

    try:
        mask = overlay.std.PropToClip('_Alpha')
    except vs.Error:
        if isinstance(overlay, SPathLike):
            raise FramePropError(overlay_sign, "Your image must have an alpha channel (transparency)!")

        raise FramePropError(overlay_sign, "You must load in the sign using `bs.VideoSource` or `imwri.Read`!")

    mask = limiter(depth(mask, get_depth(overlay)))

    if return_mask:
        return mask

    return clip.std.MaskedMerge(overlay, mask)


def _overlay_fade(
    clip: vs.VideoNode, merged: vs.VideoNode, fade_length: int, frame_ranges: FrameRangeN | FrameRangesN
) -> vs.VideoNode:
    """Overlay a fade on the overlay."""

    from kagefunc import crossfade

    if isinstance(frame_ranges, int):
        return crossfade(clip[:frame_ranges + fade_length], merged[frame_ranges:], fade_length)

    start, end = normalize_ranges(clip, frame_ranges)[0]

    merged = crossfade(clip[:start + fade_length], merged[start:], fade_length)

    return crossfade(merged[:end], clip[end - fade_length:], fade_length)
