from __future__ import annotations

import os
import subprocess as sp
import warnings
from collections import deque
from functools import partial
from typing import Any, List, Sequence, Tuple, cast

import vapoursynth as vs
import vskernels.types as kernel_type
from vskernels import Catrom, Kernel
from vsutil import depth, get_depth, is_image, scale_value

from .exceptions import InvalidMatrixError
from .mask import BoundingBox
from .types import Matrix, Position, Range, Size, VSIdxFunction
from .util import (check_variable, get_matrix, get_prop, normalize_ranges,
                   replace_ranges)

core = vs.core


__all__: List[str] = [
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
           tail_lines: int = 4, kernel: Kernel = Catrom(),
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

    Alias for this function is `lvsfunc.src`.

    Dependencies:

    * `L-SMASH-Works <https://github.com/AkarinVS/L-SMASH-Works>`_
    * `dgdecode <https://www.rationalqm.us/dgmpgdec/dgmpgdec.html>`_
    * `dgdecodenv <https://www.rationalqm.us/dgdecnv/binaries/>`_

    Thanks RivenSkaye!

    :param file:                File to index and load in.
    :param ref:                 Use another clip as reference for the clip's format,
                                resolution, framerate, and matrix/transfer/primaries (Default: None).
    :param film_thr:            FILM percentage the dgi must exceed for ``fieldop=1`` to be set automatically.
                                If set above 100.0, it's silented lowered to 100.0 (Default: 99.0).
    :param force_lsmas:         Force files to be imported with L-SMASH (Default: False).
    :param kernel:              Kernel used for the ref clip (Default: Catrom).
    :param tail_lines:          Lines to check on the tail of the dgi file. Increase this value
                                if FILM and ORDER do exist in your dgi file but it's not finding them.
                                Set to 2 for a very minor speed-up, as that's usually enough to find them (default: 4).
    :param kwargs:              Arguments passed to the indexing filter.

    :return:                    VapourSynth clip representing the input file.
    """
    if not isinstance(path, str):
        raise ValueError(f"source: 'Please input a path, not a {type(path)}!'")

    path = str(path)

    if film_thr >= 100:
        film_thr = 100.0

    if path.startswith('file:///'):
        path = path[8::]

    if force_lsmas:
        clip = core.lsmas.LWLibavSource(path, **index_args) \
            .std.SetFrameProps(lvf_idx='lsmas')
    elif is_image(path):
        clip = core.imwri.Read(path, **index_args) \
            .std.SetFrameProps(lvf_idx='imwri')
    else:
        has_nv = _check_has_nvidia()

        dgidx = 'DGIndexNV' if has_nv else 'DGIndex'
        dgsrc = core.dgdecodenv.DGSource if has_nv else core.dgdecode.DGSource  # type:ignore[attr-defined]

        if not path.endswith('.dgi'):
            filename, _ = os.path.splitext(path)
            dgi_file = f'{filename}.dgi'

            dgi = _generate_dgi(path, dgidx)

            if not dgi:
                warnings.warn(f"source: 'Unable to index using {dgidx}! Falling back to lsmas...'")
                clip = core.lsmas.LWLibavSource(path, **index_args).std.SetFrameProps(lvf_idx='lsmas')
            else:
                order, film = _tail(dgi_file, tail_lines)
                clip = _load_dgi(dgi_file, film_thr, dgsrc, order, film, **index_args)
        else:
            order, film = _tail(path)
            clip = _load_dgi(path, film_thr, dgsrc, order, film, **index_args)

    if ref:
        check_variable(ref, "source")
        assert ref.format

        ref_frame = ref.get_frame(0)

        clip = kernel.scale(clip, ref.width, ref.height)
        clip = kernel.resample(clip, format=ref.format, matrix=cast(kernel_type.Matrix, get_matrix(ref)))
        clip = core.std.SetFrameProps(clip, _Transfer=get_prop(ref_frame, '_Transfer', int),
                                      _Primaries=get_prop(ref_frame, '_Primaries', int))
        clip = core.std.AssumeFPS(clip, fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)

        if is_image(path):
            clip = clip * (ref.num_frames - 1)

    return clip


def edgefixer(clip: vs.VideoNode,
              left: int | List[int] | None = None,
              right: int | List[int] | None = None,
              top: int | List[int] | None = None,
              bottom: int | List[int] | None = None,
              radius: List[int] | None = None,
              full_range: bool = False) -> vs.VideoNode:
    """
    Fix the issues with over- and undershoot for `ContinuityFixer <https://github.com/MonoS/VS-ContinuityFixer>`_.

    This also adds what are in my opinion "more sane" ways of handling the parameters and given values.

    ...If possible, you should be using bbmod instead, though.

    Alias for this function is `lvsfunc.ef`.

    .. warning::
        This function may be rewritten in the future, and functionality may change!

    Dependencies:

    * VS-ContinuityFixer

    :param clip:        Input clip
    :param left:        Number of pixels to fix on the left (Default: None)
    :param right:       Number of pixels to fix on the right (Default: None)
    :param top:         Number of pixels to fix on the top (Default: None)
    :param bottom:      Number of pixels to fix on the bottom (Default: None)
    :param radius:      Radius for edgefixing (Default: None)
    :param full_range:  Does not run the expression over the clip to fix over/undershoot (Default: False)

    :return:            Clip with fixed edges
    """
    warnings.warn("edgefixer: This function's functionality will change in a future version, "
                  "and will likely be renamed. Please make sure to update your older scripts once it does.",
                  FutureWarning)

    check_variable(clip, "edgefixer")

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

    :param clip:    Input clip
    :param values:  Value added to every pixel, scales accordingly to your clip's depth (Default: 16)

    :return:        Clip with pixel values added
    """
    val: Tuple[float, float, float]

    check_variable(clip, "shift_tint")

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
    cv: List[float] = [scale_value(v, 8, cdepth) for v in val] if cdepth != 8 else list(val)

    return core.std.Expr(clip, expr=[f'x {cv[0]} +', f'x {cv[1]} +', f'x {cv[2]} +'])


def limit_dark(clip: vs.VideoNode, filtered: vs.VideoNode,
               threshold: float = 0.25, threshold_range: int | None = None) -> vs.VideoNode:
    """
    Replace frames in a clip with a filtered clip when the frame's luminosity exceeds the threshold.

    This way you can run lighter (or heavier) filtering on scenes that are almost entirely dark.

    There is one caveat, however: You can get scenes where every other frame is filtered
    rather than the entire scene. Please do take care to avoid that if possible.

    :param clip:              Input clip
    :param filtered:          Filtered clip
    :param threshold:         Threshold for frame averages to be filtered (Default: 0.25)
    :param threshold_range:   Threshold for a range of frame averages to be filtered (Default: None)

    :return:                  Conditionally filtered clip
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
             pos: Position | Tuple[int, int] = (1, 1),
             size: Size | Tuple[int, int] | None = None,
             show_mask: bool = False
             ) -> vs.VideoNode:
    """
    Wipe a row or column with a blank clip.

    You can also give it a different clip to replace a row with.

    :param clip:           Input clip
    :param secondary:      Clip to replace wiped rows with (Default: None)
    :param width:          Width of row (Default: 1)
    :param height:         Height of row (Default: 1)
    :param offset_x:       X-offset of row (Default: 0)
    :param offset_y:       Y-offset of row (Default: 0)

    :return:               Clip with given rows or columns wiped
    """
    check_variable(clip, "wipe_row")

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

    :param clip:                Input clip.
    :param strength:            Amount to multiply blurred clip with original clip by.
                                Negative values will blur the clip instead.
    :param sigma:               Sigma for the gaussian blur.
    :param prefilter:           Pre-denoising to prevent the unsharpening from picking up random noise.
    :param prefilter_sigma:     Strength for the pre-denoising.
    :param show_mask:           Show halo mask.

    :return:                    Unsharpened clip
    """
    check_variable(clip, "unsharpen")
    assert clip.format

    den = clip.dfttest.DFTTest(sigma=prefilter_sigma) if prefilter else clip
    diff = core.std.MakeDiff(clip, den)

    expr: str | List[str] = f'x y - {strength} * x +'

    if clip.format.color_family is not vs.GRAY:
        expr = [str(expr), "", ""]  # mypy wtf?

    blurred_clip = core.bilateral.Gaussian(den, sigma=sigma)
    unsharp = core.std.Expr([den, blurred_clip], expr)
    return core.std.MergeDiff(unsharp, diff)


def overlay_sign(clip: vs.VideoNode, overlay: vs.VideoNode | str,
                 frame_ranges: Range | List[Range] | None = None, fade_length: int = 0,
                 matrix: Matrix | int | None = None) -> vs.VideoNode:
    """
    Overlay a logo or sign onto another clip.

    This is a rewrite of fvsfunc.InsertSign.

    This wrapper also allows you to set fades to fade a logo in and out.

    Dependencies:

    * vs-imwri

    Optional Dependencies:

    * kagefunc

    :param clip:            Input clip.
    :param overlay:         Sign or logo to overlay. Must be the png loaded in through imwri.Read()
                            or a path string to the image file, and MUST be the same dimensions as the input clip.
    :param frame_ranges:    Frame ranges or starting frame to apply the overlay to. See ``types.Range`` for more info.
                            If None, overlays the entire clip.
                            If a Range is passed, the overlaid clip will only show up inside that range.
                            If only a single integer is given, it will start on that frame and
                            stay until the end of the clip.
                            Note that this function only accepts a single Range! You can't pass a list of them!
    :param fade_length:     Length to fade the clips into each other.
                            The fade will start and end on the frames given in frame_ranges.
                            If set to 0, it won't fade and the sign will simply pop in.
    :param matrix:          Enum for the matrix of the input clip. See ``types.Matrix`` for more info.
                            If not specified, gets matrix from the "_Matrix" prop of the clip unless it's an RGB clip,
                            in which case it stays as `None`.

    :return:                Clip with a logo or sign overlaid on top for the given frame ranges,
                            either with or without a fade.
    """
    if fade_length > 0:
        try:
            from kagefunc import crossfade
        except ModuleNotFoundError:
            raise ModuleNotFoundError("overlay_sign: 'missing dependency `kagefunc`!'")

    check_variable(clip, "overlay_sign")
    assert clip.format

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

    assert overlay.format

    if overlay.format.color_family is not clip_fam:
        if clip_fam is vs.RGB:
            overlay = Catrom().resample(overlay, clip.format.id, matrix_in=matrix)  # type:ignore[arg-type]
        else:
            overlay = Catrom().resample(overlay, clip.format.id, matrix)  # type:ignore[arg-type]

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


# Helper functions
def _check_has_nvidia() -> bool:
    """Check if the user has an Nvidia GPU."""
    try:
        sp.check_output('nvidia-smi')
        return True
    except sp.CalledProcessError:
        return False


def _generate_dgi(path: str, idx: str) -> bool:
    """Generate a dgi file using the given indexer and verify it exists."""
    filename, _ = os.path.splitext(path)
    output = f'{filename}.dgi'

    if not os.path.exists(output):
        try:
            sp.run([idx, '-i', path, '-o', output, '-h'])
        except sp.CalledProcessError:
            return False

    return os.path.exists(output)


def _tail(filename: str, n: int = 10) -> Tuple[int, float]:
    """Return the last n lines of a file."""
    with open(filename, "r") as f:
        lines = deque(f, n)
        lines = cast(deque[str], [line for line in lines if 'FILM' in line or 'ORDER' in line])

        if len(lines) == 1:
            return (int(lines[0].split(' ')[1]), 0.00)

        return (int(lines.pop().split(" ")[1].replace("\n", "")),
                float(lines.pop().split(" ")[0].replace("%", "")))


def _load_dgi(path: str, film_thr: float, src_filter: VSIdxFunction,
              order: int, film: float, **index_args: Any) -> vs.VideoNode:
    """
    Run the source filter on the given dgi.

    If order > 0 and FILM % > 99%, it will automatically enable `fieldop=1`.
    """
    props = dict(dgi_order=order, dgi_film=film, dgi_fieldop=0, lvf_idx='DGIndex(NV)')

    if 'fieldop' not in index_args and (order > 0 and film >= film_thr):
        index_args['fieldop'] = 1
        props |= dict(dgi_fieldop=1, _FieldBased=0)

    return src_filter(path, **index_args).std.SetFrameProps(**props)


# Aliases
ef = edgefixer
src = source

# TODO: Write function that only masks px of a certain color/threshold of colors.
#       Think the magic wand tool in various image-editing programs.
