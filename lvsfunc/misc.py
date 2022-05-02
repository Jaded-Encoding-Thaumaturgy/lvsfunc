from __future__ import annotations

import colorsys
import os
import random
import warnings
from functools import partial, wraps
from typing import Any, Callable, Dict, List, Sequence, Tuple, TypeVar, cast

import vapoursynth as vs
from vsutil import depth, get_depth, get_w, get_y, is_image, scale_value

from .kernels import Catrom
from .mask import BoundingBox
from .types import Matrix, Position, Range, Size
from .util import check_variable
from .util import get_matrix as _get_matrix
from .util import get_prop, normalize_ranges
from .util import replace_ranges as _replace_ranges
from .util import scale_thresh as _scale_thresh

core = vs.core


__all__: List[str] = [
    'allow_variable',
    'chroma_injector',
    'colored_clips',
    'edgefixer', 'ef',
    'frames_since_bookmark',
    'get_matrix',
    'limit_dark',
    'load_bookmarks',
    'overlay_sign',
    'shift_tint',
    'source', 'src',
    'unsharpen',
    'wipe_row',
]


# List of containers that are better off being indexed externally
annoying_formats = ['.iso', '.ts', '.vob']


def source(file: str, ref: vs.VideoNode | None = None,
           force_lsmas: bool = False,
           mpls: bool = False, mpls_playlist: int = 0, mpls_angle: int = 0,
           **index_args: Any) -> vs.VideoNode:
    """
    Generic clip import function.
    Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced.
    It also automatically determines if an image has been imported.
    You can set its fps using 'fpsnum' and 'fpsden', or using a reference clip with 'ref'.

    Alias for this function is `lvsfunc.src`.

    .. warning::
        | WARNING: This function will be rewritten in the future, and functionality may change!
        |         No warning is currently printed for this in your terminal to avoid spam.

    Dependencies:

    * ffms2
    * L-SMASH-Works (optional: m2ts sources or when forcing lsmas)
    * d2vsource (optional: d2v sources)
    * dgdecodenv (optional: dgi sources)
    * VapourSynth-ReadMpls (optional: mpls sources)

    :param file:              Input file. This MUST have an extension.
    :param ref:               Use another clip as reference for the clip's format,
                              resolution, and framerate (Default: None).
    :param force_lsmas:       Force files to be imported with L-SMASH (Default: False)
    :param mpls:              Load in a mpls file (Default: False).
    :param mpls_playlist:     Playlist number, which is the number in mpls file name (Default: 0).
    :param mpls_angle:        Angle number to select in the mpls playlist (Default: 0).
    :param kwargs:            Arguments passed to the indexing filter.

    :return:                  Vapoursynth clip representing input file.
    """
    if file.startswith('file:///'):
        file = file[8::]

    fname, ext = os.path.splitext(file)

    if not ext:
        raise ValueError("source: 'No extension found in filename!'")

    # Error handling for some file types
    if ext == '.mpls' and mpls is False:
        raise ValueError("source: 'Set \"mpls = True\" and pass a path to the base Blu-ray directory "
                         "for this kind of file'")

    if ext in annoying_formats:
        raise ValueError("source: 'Use an external indexer like d2vwitch or DGIndexNV for this kind of file'")

    if force_lsmas:
        clip = core.lsmas.LWLibavSource(file, **index_args)
    elif mpls:
        mpls_in = core.mpls.Read(file, mpls_playlist, mpls_angle)
        clip = core.std.Splice([core.lsmas.LWLibavSource(mpls_in['clip'][i], **index_args)
                                for i in range(mpls_in['count'])])
    elif is_image(file):
        clip = core.imwri.Read(file, **index_args)
    else:
        match ext:
            case 'd2v': clip = core.d2v.Source(file, **index_args)
            case '.dgi': clip = core.dgdecodenv.DGSource(file, **index_args)
            case '.mp4': clip = core.lsmas.LibavSMASHSource(file, **index_args)
            case '.m2ts': clip = core.lsmas.LWLibavSource(file, **index_args)
            case _: clip = core.ffms2.Source(file, **index_args)

    if ref:
        check_variable(ref, "source")
        assert ref.format

        clip = core.std.AssumeFPS(clip, fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)
        clip = core.resize.Bicubic(clip, width=ref.width, height=ref.height,
                                   format=ref.format.id, matrix=get_matrix(ref))
        if is_image(file):
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
    A wrapper for ContinuityFixer (https://github.com/MonoS/VS-ContinuityFixer).

    Fixes the issues with over- and undershoot that it may create when fixing the edges,
    and adds what are in my opinion "more sane" ways of handling the parameters and given values.

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

    ef = core.edgefixer.ContinuityFixer(clip, left, top, right, bottom, radius)
    return ef if full_range else core.std.Limiter(ef, 16.0, [235, 240])


def shift_tint(clip: vs.VideoNode, values: int | Sequence[int] = 16) -> vs.VideoNode:
    """
    A function for forcibly adding pixel values to a clip.
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
        raise ValueError("shift_tint: 'Too many values supplied'")

    if any(v > 255 or v < -255 for v in val):
        raise ValueError("shift_tint: 'Every value in \"values\" must be below 255'")

    cdepth = get_depth(clip)
    cv: List[float] = [scale_value(v, 8, cdepth) for v in val] if cdepth != 8 else list(val)

    return core.std.Expr(clip, expr=[f'x {cv[0]} +', f'x {cv[1]} +', f'x {cv[2]} +'])


def limit_dark(clip: vs.VideoNode, filtered: vs.VideoNode,
               threshold: float = 0.25, threshold_range: int | None = None) -> vs.VideoNode:
    """
    Replaces frames in a clip with a filtered clip when the frame's darkness exceeds the threshold.
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
                         "a lower value than \"threshold\" ({threshold})'")

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
    Simple function to wipe a row or column with a blank clip.
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


def load_bookmarks(bookmark_path: str) -> List[int]:
    """
    VSEdit bookmark loader.

    load_bookmarks(os.path.basename(__file__)+".bookmarks")
    will load the VSEdit bookmarks for the current Vapoursynth script.

    :param bookmark_path:  Path to bookmarks file

    :return:               A list of bookmarked frames
    """
    with open(bookmark_path) as f:
        bookmarks = [int(i) for i in f.read().split(", ")]

        if bookmarks[0] != 0:
            bookmarks.insert(0, 0)

    return bookmarks


def frames_since_bookmark(clip: vs.VideoNode, bookmarks: List[int]) -> vs.VideoNode:
    """
    Displays frames since last bookmark to create easily reusable scenefiltering.
    Can be used in tandem with :py:func:`lvsfunc.misc.load_bookmarks` to import VSEdit bookmarks.

    :param clip:        Input clip
    :param bookmarks:   A list of bookmarks

    :return:            Clip with bookmarked frames
    """
    def _frames_since_bookmark(n: int, clip: vs.VideoNode, bookmarks: List[int]) -> vs.VideoNode:
        for i, bookmark in enumerate(bookmarks):
            frames_since = n - bookmark

            if frames_since >= 0 and i + 1 >= len(bookmarks):
                result = frames_since
            elif frames_since >= 0 and n - bookmarks[i + 1] < 0:
                result = frames_since
                break

        return core.text.Text(clip, str(result))
    return core.std.FrameEval(clip, partial(_frames_since_bookmark, clip=clip, bookmarks=bookmarks))


F = TypeVar("F", bound=Callable[..., vs.VideoNode])


def allow_variable(width: int | None = None, height: int | None = None,
                   format: int | None = None
                   ) -> Callable[[Callable[..., vs.VideoNode]], Callable[..., vs.VideoNode]]:
    """
    Decorator allowing a variable-res and/or variable-format clip to be passed
    to a function that otherwise would not be able to accept it. Implemented by
    FrameEvaling and resizing the clip to each frame. Does not work when the
    function needs to return a different format unless an output format is
    specified. As such, this decorator must be called as a function when used
    (e.g. ``@allow_variable()`` or ``@allow_variable(format=vs.GRAY16)``). If
    the provided clip is variable format, no output format is required to be
    specified.

    :param width:       Output clip width
    :param height:      Output clip height
    :param format:      Output clip format

    :return:            Function decorator for the given output format.
    """
    if height is not None:
        width = width if width else get_w(height)

    def inner(func: F) -> F:
        @wraps(func)
        def inner2(clip: vs.VideoNode, *args: Any, **kwargs: Any) -> vs.VideoNode:
            def frameeval_wrapper(n: int, f: vs.VideoFrame) -> vs.VideoNode:
                res = func(clip.resize.Point(f.width, f.height, format=f.format.id), *args, **kwargs)
                return res.resize.Point(format=format) if format else res

            clip_out = clip.resize.Point(format=format) if format else clip
            clip_out = clip_out.resize.Point(width, height) if width and height else clip_out
            return core.std.FrameEval(clip_out, frameeval_wrapper, prop_src=[clip])

        return cast(F, inner2)

    return inner


def chroma_injector(func: F) -> F:
    """
    Decorator allowing injection of reference chroma into a function which
    would normally only receive luma, such as an upscaler passed to
    :py:func:`lvsfunc.scale.descale`. The chroma is resampled to the input
    clip's width, height, and pixel format, shuffled to YUV444PX, then passed
    to the function. Luma is then extracted from the function result and
    returned. The first argument of the function is assumed to be the luma
    source. This works with variable resolution and may work with variable
    format, however the latter is wholly untested and likely a bad idea in
    every conceivable use case.

    :param func:        Function to call with injected chroma

    :return:            Decorated function
    """

    @wraps(func)
    def inner(_chroma: vs.VideoNode, clip: vs.VideoNode, *args: Any,
              **kwargs: Any) -> vs.VideoNode:

        def upscale_chroma(n: int, f: vs.VideoFrame) -> vs.VideoNode:
            luma = y.resize.Point(f.width, f.height, format=f.format.id)
            if out_fmt is not None:
                fmt = out_fmt
            else:
                fmt = core.register_format(vs.YUV, f.format.sample_type,
                                           f.format.bits_per_sample, 0, 0)
            chroma = _chroma.resize.Spline36(f.width, f.height,
                                             format=fmt.id)
            res = core.std.ShufflePlanes([luma, chroma], planes=[0, 1, 2],
                                         colorfamily=vs.YUV)
            return res

        out_fmt: vs.VideoFormat | None = None
        if clip.format is not None:
            if clip.format.color_family not in (vs.GRAY, vs.YUV):
                raise ValueError("chroma_injector: only YUV and GRAY clips are supported")

            in_fmt = core.register_format(vs.GRAY, clip.format.sample_type,
                                          clip.format.bits_per_sample, 0, 0)
            y = allow_variable(format=in_fmt.id)(get_y)(clip)
            # We want to use YUV444PX for chroma injection
            out_fmt = core.register_format(vs.YUV, clip.format.sample_type,
                                           clip.format.bits_per_sample, 0, 0)
        else:
            y = allow_variable()(get_y)(clip)

        if y.width != 0 and y.height != 0 and out_fmt is not None:
            chroma = _chroma.resize.Spline36(y.width, y.height, format=out_fmt.id)
            clip_in = core.std.ShufflePlanes([y, chroma], planes=[0, 1, 2],
                                             colorfamily=vs.YUV)
        else:
            y_f = y.resize.Point(format=out_fmt.id) if out_fmt is not None else y
            clip_in = core.std.FrameEval(y_f, upscale_chroma, prop_src=[y])

        result = func(clip_in, *args, **kwargs)

        if result.format is not None:
            if result.format.color_family not in (vs.GRAY, vs.YUV):
                raise ValueError("chroma_injector: can only decorate function with YUV and/or GRAY format return")

            if result.format.color_family == vs.GRAY:
                return result

            res_fmt = core.register_format(vs.GRAY, result.format.sample_type,
                                           result.format.bits_per_sample, 0, 0)
            return allow_variable(format=res_fmt.id)(get_y)(result)
        else:
            return allow_variable()(get_y)(result)

    return cast(F, inner)


def colored_clips(amount: int,
                  max_hue: int = 300,
                  rand: bool = True,
                  seed: bytearray | bytes | float | str | None = None,
                  **kwargs: Any
                  ) -> List[vs.VideoNode]:
    """
    Returns a list of BlankClips with unique colors in sequential or random order.
    The colors will be evenly spaced by hue in the HSL colorspace.

    Useful maybe for comparison functions or just for getting multiple uniquely colored BlankClips for testing purposes.

    Will always return a pure red clip in the list as this is the RGB equivalent of the lowest HSL hue possible (0).

    Written by Dave <orangechannel@pm.me>.

    :param amount:  Number of ``vapoursynth.VideoNode``\\s to return
    :param max_hue: Maximum hue (0 < hue <= 360) in degrees to generate colors from (uses the HSL color model).
                    Setting this higher than ``315`` will result in the clip colors looping back towards red
                    and is not recommended for visually distinct colors.
                    If the `amount` of clips is higher than the `max_hue` expect there to be identical
                    or visually similar colored clips returned (Default: 300)
    :param rand:    Randomizes order of the returned list (Default: True)
    :param seed:    Bytes-like object passed to ``random.seed`` which allows for consistent randomized order
                    of the resulting clips (Default: None)
    :param kwargs:  Arguments passed to ``vapoursynth.core.std.BlankClip`` (Default: keep=1)

    :return:        List of uniquely colored clips in sequential or random order.
    """
    if amount < 2:
        raise ValueError("colored_clips: `amount` must be at least 2")
    if not (0 < max_hue <= 360):
        raise ValueError("colored_clips: `max_hue` must be greater than 0 and less than 360 degrees")

    blank_clip_args: Dict[str, Any] = {'keep': 1, **kwargs}

    hues: List[float] = [i * max_hue / (amount - 1) for i in range(amount - 1)]
    hues.append(max_hue)

    hls_color_list: List[Tuple[float, float, float]] = [colorsys.hls_to_rgb(h / 360, 0.5, 1) for h in hues]
    rgb_color_list = [[int(f * 255) for f in color] for color in hls_color_list]

    if rand:
        shuffle = random.shuffle if seed is None else random.Random(seed).shuffle
        shuffle(rgb_color_list)

    return [core.std.BlankClip(color=color, **blank_clip_args) for color in rgb_color_list]


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
    Wrapper to overlay a logo or sign onto another clip. Rewrite of fvsfunc.InsertSign.
    This wrapper also allows you to set fades to fade a logo in and out.

    Requires:

    * vs-imwri

    :param clip:            Base clip
    :param overlay:         Sign or logo to overlay. Must be the png loaded in through imwri.Read()
                            or a path string to the image file.
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
                            either with or without a fade
    """
    try:
        from kagefunc import crossfade
    except ModuleNotFoundError:
        raise ModuleNotFoundError("overlay_sign: 'missing dependency `kagefunc`'")

    check_variable(clip, "overlay_sign")
    assert clip.format

    ov_type = type(overlay)
    clip_fam = clip.format.color_family

    # TODO: This can probably be done better
    if not isinstance(overlay, (vs.VideoNode, str)):
        raise ValueError("overlay_sign: '`overlay` must be a VideoNode object or a string path!'")
    elif isinstance(overlay, str):
        overlay = core.imwri.Read(overlay, alpha=True)

    if not all([clip.width, overlay.width]) or not all([clip.height, overlay.height]):
        raise ValueError("overlay_sign: 'Your overlay clip must have the same dimensions as your input clip!'")

    # wtf mypy this IS reachable
    if isinstance(frame_ranges, list) and len(frame_ranges) > 1:
        warnings.warn("overlay_sign: 'Only one range is currently supported! "
                      "Grabbing the first item in list.'")
        frame_ranges = frame_ranges[0]

    overlay = overlay[0] * clip.num_frames

    if matrix is None:
        matrix = get_prop(clip.get_frame(0), "_Matrix", int)

    if matrix == 2:
        raise ValueError("overlay_sign: 'You can't set a matrix of 2! "
                         "Please set the correct matrix in the parameters!'")

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
            raise ValueError("overlay_sign: 'Please make sure you loaded your sign in using imwri.Read!'")

    merge = core.std.MaskedMerge(clip, overlay, depth(mask, get_depth(overlay)))

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
get_matrix = _get_matrix
replace_ranges = _replace_ranges
scale_thresh = _scale_thresh
src = source

# TODO: Write function that only masks px of a certain color/threshold of colors.
#       Think the magic wand tool in various image-editing programs.
