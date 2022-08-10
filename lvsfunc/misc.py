from __future__ import annotations

import os
import warnings
from functools import partial
from typing import Any, Sequence

import vapoursynth as vs
from vskernels import Bicubic, Catrom, Kernel, Matrix, get_prop
from vsutil import depth, get_depth, is_image, scale_value

from .exceptions import InvalidMatrixError
from .helpers import _check_index_exists, _generate_dgi, _get_dgidx, _load_dgi, _tail
from .mask import BoundingBox
from .types import IndexExists, Position, Range, Size
from .util import check_variable, match_clip, normalize_ranges, replace_ranges

core = vs.core


__all__ = [
    'edgefixer', 'ef',
    'limit_dark',
    'overlay_sign',
    'shift_tint',
    'source', 'src',
    'unsharpen',
    'wipe_row',
]


def source(path: os.PathLike[str] | str, ref: vs.VideoNode | None = None,
           film_thr: float = 99.0, force_lsmas: bool = False,
           tail_lines: int = 4, kernel: Kernel | str = Bicubic(b=0, c=1/2),
           **index_args: Any) -> vs.VideoNode:
    """
    Index and load video clips for use in VapourSynth automatically.

    .. note::
        | For this function to work properly, you NEED to have DGIndex(NV) in your PATH!
        | DGIndexNV will be faster, but it only works with an NVidia GPU.

    This function will try to index the given video file using DGIndex(NV).
    If it can't, it will fall back on L-SMASH. L-SMASH can also be forced using ``force_lsmas``.
    It also automatically determines if an image has been imported.

    This function will automatically check whether your clip is mostly FILM.
    If FILM is above ``film_thr`` and the order is above 0,
    it will automatically set ``fieldop=1`` and ``_FieldBased=0``.
    This can be disabled by passing ``fieldop=0`` to the function yourself.

    You can pass a ref clip to further adjust the clip.
    This affects the dimensions, framerates, matrix/transfer/primaries,
    and in the case of an image, the length of the clip.

    Alias for this function is ``lvsfunc.src``.

    Dependencies:

    * `dgdecode <https://www.rationalqm.us/dgmpgdec/dgmpgdec.html>`_
    * `dgdecodenv <https://www.rationalqm.us/dgdecnv/binaries/>`_
    * `L-SMASH-Works <https://github.com/AkarinVS/L-SMASH-Works>`_
    * `vs-imwri <https://github.com/vapoursynth/vs-imwri>`_

    Thanks `RivenSkaye <https://github.com/RivenSkaye>`_!

    :param file:            File to index and load in.
    :param ref:             Use another clip as reference for the clip's format,
                            resolution, framerate, and matrix/transfer/primaries (Default: None).
    :param film_thr:        FILM percentage the dgi must exceed for ``fieldop=1`` to be set automatically.
                            If set above 100.0, it's silently lowered to 100.0 (Default: 99.0).
    :param force_lsmas:     Force files to be imported with L-SMASH (Default: False).
    :param kernel:          py:class:`vskernels.Kernel` object used for converting the `clip` to match `ref`.
                            This can also be the string name of the kernel
                            (Default: py:class:`vskernels.Bicubic(b=0, c=1/2)`).
    :param tail_lines:      Lines to check on the tail of the dgi file.
                            Increase this value if FILM and ORDER do exist in your dgi file
                            but it's having trouble finding them.
                            Set to 2 for a very minor speed-up, as that's usually enough to find them (Default: 4).
    :param kwargs:          Optional arguments passed to the indexing filter.

    :return:                VapourSynth clip representing the input file.

    :raises ValueError:     Something other than a path is passed to ``path``.
    """
    if not isinstance(path, (os.PathLike, str)):
        raise ValueError(f"source: 'Please input a path, not a {type(path).__class__.__name__}!'")

    path = str(path)
    film_thr = 100.0 if film_thr >= 100 else film_thr

    if path.startswith('file:///'):
        path = path[8::]

    dgidx, dgsrc = _get_dgidx()

    match IndexExists.LWI_EXISTS if force_lsmas else _check_index_exists(path):
        case IndexExists.PATH_IS_DGI:
            order, film = _tail(path, tail_lines)
            clip = _load_dgi(path, film_thr, dgsrc, order, film, **index_args)
        case IndexExists.PATH_IS_IMG:
            clip = core.imwri.Read(path, **index_args).std.SetFrameProps(lvf_idx='imwri')
        case IndexExists.LWI_EXISTS:
            clip = core.lsmas.LWLibavSource(path, **index_args).std.SetFrameProps(lvf_idx='lsmas')
        case IndexExists.DGI_EXISTS:
            order, film = _tail(f"{path}.dgi", tail_lines)
            clip = _load_dgi(f"{path}.dgi", film_thr, dgsrc, order, film, **index_args)
        case _:
            filename, _ = os.path.splitext(path)
            dgi_file = f'{filename}.dgi'

            dgi = _generate_dgi(path, dgidx)

            if not dgi:
                warnings.warn(f"source: 'Unable to index using {dgidx}! Falling back to lsmas...'")
                clip = core.lsmas.LWLibavSource(path, **index_args).std.SetFrameProps(lvf_idx='lsmas')
            else:
                order, film = _tail(dgi_file, tail_lines)
                clip = _load_dgi(dgi_file, film_thr, dgsrc, order, film, **index_args)

    if ref:
        return match_clip(clip, ref, length=is_image(path), kernel=kernel)
    return clip


def edgefixer(clip: vs.VideoNode,
              left: int | list[int] | None = None,
              right: int | list[int] | None = None,
              top: int | list[int] | None = None,
              bottom: int | list[int] | None = None,
              radius: list[int] | None = None,
              full_range: bool = False) -> vs.VideoNode:
    """
    Fix the issues with over- and undershoot for `ContinuityFixer <https://github.com/MonoS/VS-ContinuityFixer>`_.

    This also adds what are in my opinion "more sane" ways of handling the parameters and given values.

    ...If possible, you should be using bbmod instead, though.

    Alias for this function is ``lvsfunc.ef``.

    .. warning::
        This function may be rewritten in the future, and functionality may change!

    Dependencies:

    * `vs-ContinuityFixer <https://github.com/MonoS/VS-ContinuityFixer>`_

    :param clip:            Clip to process.
    :param left:            Number of pixels to fix on the left (Default: None).
    :param right:           Number of pixels to fix on the right (Default: None).
    :param top:             Number of pixels to fix on the top (Default: None).
    :param bottom:          Number of pixels to fix on the bottom (Default: None).
    :param radius:          Radius for edgefixing (Default: None).
    :param full_range:      Does not run the expression over the clip to fix over/undershoot (Default: False).

    :return:                Clip with fixed edges.
    """
    warnings.warn("edgefixer: This function's functionality will change in a future version, "
                  "and will likely be renamed. Please make sure to update your scripts once it does.",
                  FutureWarning)

    assert check_variable(clip, "edgefixer")

    if left is None:
        left = 0
    if right is None:
        right = left
    if top is None:
        top = left
    if bottom is None:
        bottom = top

    ef = core.cf.ContinuityFixer(clip, left, top, right, bottom, radius)
    limit: vs.VideoNode = ef if full_range else core.std.Limiter(ef, 16.0, [235, 240])
    return limit


def shift_tint(clip: vs.VideoNode, values: int | Sequence[int] = 16) -> vs.VideoNode:
    """
    Forcibly adds pixel values to a clip.

    Can be used to fix green tints in Crunchyroll sources, for example.
    Only use this if you know what you're doing!

    This function accepts a single integer or a list of integers.
    Values passed should mimic those of an 8bit clip.
    If your clip is not 8bit, they will be scaled accordingly.

    If you only pass 1 value, it will copied to every plane.
    If you pass 2, the 2nd one will be copied over to the 3rd.
    Don't pass more than three.

    :param clip:            Clip to process.
    :param values:          Value added to every pixel, scales accordingly to your clip's depth (Default: 16).

    :return:                Clip with pixel values added.

    :raises ValueError:     Too many values are supplied.
    :raises ValueError:     Any value in ``values`` are above 255.
    """
    val: tuple[int, int, int]

    assert check_variable(clip, "shift_tint")

    if isinstance(values, int):
        val = (values, values, values)
    elif len(values) == 2:
        val = (values[0], values[1], values[1])
    elif len(values) == 3:
        val = (values[0], values[1], values[2])
    else:
        raise ValueError("shift_tint: 'Too many values supplied!'")

    if any(v > 255 or v < -255 for v in val):
        raise ValueError("shift_tint: 'Every value in \"values\" must be below 255!'")

    cdepth = get_depth(clip)
    cv = [scale_value(v, 8, cdepth) for v in val] if cdepth != 8 else list(val)

    return core.akarin.Expr(clip, expr=[f'x {cv[0]} +', f'x {cv[1]} +', f'x {cv[2]} +'])


def limit_dark(clip: vs.VideoNode, filtered: vs.VideoNode,
               threshold: float = 0.25, threshold_range: int | None = None) -> vs.VideoNode:
    """
    Replace frames in a clip with a filtered clip when the frame's luminosity exceeds the threshold.

    This way you can run lighter (or heavier) filtering on scenes that are almost entirely dark.

    There is one caveat, however: You can get scenes where every other frame is filtered
    rather than the entire scene. Please do take care to avoid that if possible.

    :param clip:                Clip to process.
    :param filtered:            Filtered clip.
    :param threshold:           Threshold for frame averages to be filtered (Default: 0.25).
    :param threshold_range:     Threshold for a range of frame averages to be filtered (Default: None).

    :return:                    Conditionally filtered clip.

    :raises ValueError:         ``threshold_range`` is a higher value than ``threshold``.
    """
    def _diff(n: int, f: vs.VideoFrame, clip: vs.VideoNode,
              filtered: vs.VideoNode, threshold: float,
              threshold_range: int | None) -> vs.VideoNode:
        psa = get_prop(f, "PlaneStatsAverage", float)
        if threshold_range:
            return filtered if threshold_range <= psa <= threshold else clip
        else:
            return clip if psa > threshold else filtered

    if threshold_range and threshold_range > threshold:
        raise ValueError(f"limit_dark: '\"threshold_range\" ({threshold_range}) must be "
                         f"a lower value than \"threshold\" ({threshold})!'")

    avg = core.std.PlaneStats(clip)
    return core.std.FrameEval(clip, partial(_diff, clip=clip, filtered=filtered,
                                            threshold=threshold, threshold_range=threshold_range), avg)


def wipe_row(clip: vs.VideoNode,
             ref: vs.VideoNode | None = None,
             pos: Position | tuple[int, int] = (1, 1),
             size: Size | tuple[int, int] | None = None,
             show_mask: bool = False
             ) -> vs.VideoNode:
    """
    Wipe a row or column with a blank clip.

    You can also give it a different clip to replace a row with.

    :param clip:            Clip to process.
    :param secondary:       Clip to replace wiped rows with (Default: None).
    :param width:           Width of row (Default: 1).
    :param height:          Height of row (Default: 1).
    :param offset_x:        X-offset of row (Default: 0).
    :param offset_y:        Y-offset of row (Default: 0).

    :return:                Clip with given rows or columns wiped.
    """
    assert check_variable(clip, "wipe_row")

    ref = ref or core.std.BlankClip(clip)

    if size is None:
        size = (clip.width-2, clip.height-2)
    sqmask = BoundingBox(pos, size).get_mask(clip)

    if show_mask:
        return sqmask
    return core.std.MaskedMerge(clip, ref, sqmask)


def unsharpen(clip: vs.VideoNode, strength: float = 1.0, sigma: float = 1.5,
              prefilter: bool = True, prefilter_sigma: float = 0.75) -> vs.VideoNode:
    """
    Diff'd unsharpening function.

    Performs one-dimensional sharpening as such: "Original + (Original - blurred) * Strength"
    It then merges back noise and detail that was prefiltered away,

    Negative values will blur instead. This can be useful for trying to undo sharpening.

    This function is not recommended for normal use,
    but may be useful as prefiltering for detail- or edgemasks.

    :param clip:                Clip to process.
    :param strength:            Amount to multiply blurred clip with original clip by.
                                Negative values will blur the clip instead.
    :param sigma:               Sigma for the gaussian blur.
    :param prefilter:           Pre-denoising to prevent the unsharpening from picking up random noise.
    :param prefilter_sigma:     Strength for the pre-denoising.
    :param show_mask:           Show halo mask.

    :return:                    Unsharpened clip.
    """
    assert check_variable(clip, "unsharpen")

    den = clip.dfttest.DFTTest(sigma=prefilter_sigma) if prefilter else clip
    diff = core.std.MakeDiff(clip, den)

    expr: str | list[str] = f'x y - {strength} * x +'

    if clip.format.color_family is not vs.GRAY:
        expr = [str(expr), "", ""]  # mypy wtf?

    blurred_clip = core.bilateral.Gaussian(den, sigma=sigma)
    unsharp = core.akarin.Expr([den, blurred_clip], expr)
    return core.std.MergeDiff(unsharp, diff)


def overlay_sign(clip: vs.VideoNode, overlay: vs.VideoNode | str,
                 frame_ranges: Range | list[Range] | None = None, fade_length: int = 0,
                 matrix: Matrix | int | None = None) -> vs.VideoNode:
    """
    Overlay a logo or sign onto another clip.

    This is a rewrite of fvsfunc.InsertSign.

    This wrapper also allows you to set fades to fade a logo in and out.

    Dependencies:

    * `vs-imwri <https://github.com/vapoursynth/vs-imwri>`_
    * `kagefunc <https://github.com/Irrational-Encoding-Wizardry/kagefunc>`_ (optional: ``fade_length``)

    :param clip:                    Clip to process.
    :param overlay:                 Sign or logo to overlay. Must be the png loaded in
                                    through :py:func:`core.vapoursnth.imwri.Read` or a path string to the image file,
                                    and **MUST** be the same dimensions as the ``clip`` to process.
    :param frame_ranges:            Frame ranges or starting frame to apply the overlay to.
                                    See :py:attr:`lvsfunc.types.Range` for more info.
                                    If None, overlays the entire clip.
                                    If a Range is passed, the overlaid clip will only show up inside that range.
                                    If only a single integer is given, it will start on that frame and
                                    stay until the end of the clip.
                                    Note that this function only accepts a single Range! You can't pass a list of them!
    :param fade_length:             Length to fade the clips into each other.
                                    The fade will start and end on the frames given in frame_ranges.
                                    If set to 0, it won't fade and the sign will simply pop in.
    :param matrix:                  Enum for the matrix of the Clip to process.
                                    See :py:attr:`lvsfunc.types.Matrix` for more info.
                                    If not specified, gets matrix from the "_Matrix" prop of the clip
                                    unless it's an RGB clip, in which case it stays as `None`.

    :return:                        Clip with a logo or sign overlaid on top for the given frame ranges,
                                    either with or without a fade.

    :raises ModuleNotFoundError:    Dependencies are missing.
    :raises ValueError:             ``overlay`` is not a VideoNode or a path.
    :raises ValueError:             The overlay clip is not of the same dimensions as the input clip.
    :raises InvalidMatrixError:     ``Matrix`` is an invalid value.
    :raises ValueError:             Overlay does not have an alpha channel.
    :raises TypeError:              Overlay clip was not loaded in using :py:func:`vapoursynth.core.imwri.Read`.
    """
    if fade_length > 0:
        try:
            from kagefunc import crossfade
        except ModuleNotFoundError:
            raise ModuleNotFoundError("overlay_sign: 'missing dependency `kagefunc`!'")

    assert check_variable(clip, "overlay_sign")

    ov_type = type(overlay)
    clip_fam = clip.format.color_family

    # TODO: This can probably be done better
    if not isinstance(overlay, (vs.VideoNode, str)):
        raise ValueError("overlay_sign: '`overlay` must be a VideoNode object or a string path!'")
    elif isinstance(overlay, str):
        overlay = core.imwri.Read(overlay, alpha=True)

    if (clip.width != overlay.width) or (clip.height != overlay.height):
        raise ValueError("overlay_sign: 'Your overlay clip must have the same dimensions as your input clip!'")

    if isinstance(frame_ranges, list) and len(frame_ranges) > 1:
        warnings.warn("overlay_sign: 'Only one range is currently supported! "
                      "Grabbing the first item in list.'")
        frame_ranges = frame_ranges[0]

    overlay = overlay[0] * clip.num_frames

    if matrix is None:
        matrix = get_prop(clip.get_frame(0), "_Matrix", int)

    if matrix == 2:
        raise InvalidMatrixError("overlay_sign")

    if overlay.format.color_family is not clip_fam:  # type:ignore[union-attr]
        if clip_fam is vs.RGB:
            overlay = Catrom().resample(overlay, clip.format.id, matrix_in=matrix)
        else:
            overlay = Catrom().resample(overlay, clip.format.id, matrix)

    try:
        mask = core.std.PropToClip(overlay)
    except vs.Error:
        if ov_type is str:
            raise ValueError("overlay_sign: 'Please make sure your image has an alpha channel!'")
        else:
            raise TypeError("overlay_sign: 'Please make sure you loaded your sign in using imwri.Read!'")

    merge = core.std.MaskedMerge(clip, overlay, depth(mask, get_depth(overlay)).std.Limiter())

    if not frame_ranges:
        return merge

    if fade_length > 0:
        if isinstance(frame_ranges, int):
            return crossfade(clip[:frame_ranges+fade_length], merge[frame_ranges:], fade_length)
        else:
            start, end = normalize_ranges(clip, frame_ranges)[0]
            merge = crossfade(clip[:start+fade_length], merge[start:], fade_length)
            return crossfade(merge[:end], clip[end-fade_length:], fade_length)
    else:
        return replace_ranges(clip, merge, frame_ranges)


# Aliases
ef = edgefixer
src = source

# TODO: Write function that only masks px of a certain color/threshold of colors.
#       Think the magic wand tool in various image-editing programs.
