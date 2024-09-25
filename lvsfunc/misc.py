from __future__ import annotations

from typing import cast

from vskernels import Catrom
from vstools import (CustomValueError, DependencyNotFoundError, FramePropError,
                     FrameRangeN, FrameRangesN, Matrix,
                     ResolutionsMismatchError, check_variable, core, depth,
                     get_depth, normalize_ranges, replace_ranges, vs)

__all__ = [
    'overlay_sign'
]


def overlay_sign(
    clip: vs.VideoNode, overlay: vs.VideoNode | str,
    frame_ranges: FrameRangeN | FrameRangesN | None = None, fade_length: int = 0,
    matrix: Matrix | int | None = None
) -> vs.VideoNode:
    """
    Overlay a logo or sign onto another clip.

    This is a rewrite of fvsfunc.InsertSign.

    This wrapper also allows you to set fades to fade a logo in and out.

    Dependencies:

    * `vs-imwri <https://github.com/vapoursynth/vs-imwri>`_
    * `kagefunc <https://github.com/Irrational-Encoding-Wizardry/kagefunc>`_ (optional: ``fade_length``)

    :param clip:                    Clip to process.
    :param overlay:                 Sign or logo to overlay. Must be the png loaded in
                                    through :py:func:`core.vapoursynth.imwri.Read` or a path string to the image file,
                                    and **MUST** be the same dimensions as the ``clip`` to process.
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
                                    See :py:attr:`lvsfunc.types.Matrix` for more info.
                                    If not specified, gets matrix from the "_Matrix" prop of the clip
                                    unless it's an RGB clip, in which case it stays as `None`.

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

    is_string = isinstance(overlay, str)
    clip_fam = clip.format.color_family

    if is_string:
        overlay = core.imwri.Read(overlay, alpha=True)

    if not isinstance(overlay, vs.VideoNode):
        raise CustomValueError('`overlay` must be a VideoNode object or a string path!', overlay_sign)

    overlay = cast(vs.VideoNode, overlay)

    assert check_variable(overlay, overlay_sign)

    ResolutionsMismatchError.check(overlay_sign, clip, overlay)

    if isinstance(frame_ranges, list) and len(frame_ranges) > 1:
        import warnings
        warnings.warn("overlay_sign: 'Only one range is currently supported! Grabbing the first item in list.'")
        frame_ranges = frame_ranges[0]

    if overlay.format.color_family is not clip_fam:
        if clip_fam is vs.RGB:
            overlay = Catrom.resample(overlay, clip.format.id, matrix_in=matrix)
        else:
            overlay = Catrom.resample(overlay, clip.format.id, matrix)

    overlay = overlay[0] * clip.num_frames

    try:
        mask = overlay.std.PropToClip('_Alpha')
    except vs.Error:
        if is_string:
            raise FramePropError(overlay_sign, "Your image must have an alpha channel (transparency)!")

        raise FramePropError(overlay_sign, "You must load in the sign using `imwri.Read`!")

    merge = clip.std.MaskedMerge(overlay, depth(mask, get_depth(overlay)).std.Limiter())

    if not frame_ranges:
        return merge

    if fade_length > 0:
        if isinstance(frame_ranges, int):
            return crossfade(clip[:frame_ranges + fade_length], merge[frame_ranges:], fade_length)

        start, end = normalize_ranges(clip, frame_ranges)[0]

        merge = crossfade(clip[:start + fade_length], merge[start:], fade_length)

        return crossfade(merge[:end], clip[end - fade_length:], fade_length)

    return replace_ranges(clip, merge, frame_ranges)
