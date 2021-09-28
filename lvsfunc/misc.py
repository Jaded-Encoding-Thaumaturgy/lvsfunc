"""
    Miscellaneous functions and wrappers that didn't really have a place in any other submodules.
"""
import colorsys
import os
import random
import warnings
from functools import partial, wraps
from typing import (Any, Callable, Dict, List, Optional, Sequence, Tuple,
                    TypeVar, Union, cast)

import vapoursynth as vs
from vsutil import get_depth, get_w, get_y, is_image, scale_value

from .mask import BoundingBox
from .types import Position, Size
from .util import get_prop
from .util import replace_ranges as _replace_ranges
from .util import scale_thresh as _scale_thresh

core = vs.core


# List of containers that are better off being indexed externally
annoying_formats = ['.iso', '.ts', '.vob']


def source(file: str, ref: Optional[vs.VideoNode] = None,
           force_lsmas: bool = False,
           mpls: bool = False, mpls_playlist: int = 0, mpls_angle: int = 0,
           **index_args: Any) -> vs.VideoNode:
    """
    Generic clip import function.
    Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced.
    It also automatically determines if an image has been imported.
    You can set its fps using 'fpsnum' and 'fpsden', or using a reference clip with 'ref'.

    Alias for this function is `lvsfunc.src`.

    WARNING: This function may be rewritten in the future, and functionality may change!
             No warning is currently printed for this in your terminal to avoid spam.

    Dependencies:

    * ffms2
    * L-SMASH-Works (optional: m2ts sources or when forcing lsmas)
    * d2vsource (optional: d2v sources)
    * dgdecodenv (optional: dgi sources)
    * VapourSynth-ReadMpls (optional: mpls sources)

    :param file:              Input file
    :param ref:               Use another clip as reference for the clip's format,
                              resolution, and framerate (Default: None)
    :param force_lsmas:       Force files to be imported with L-SMASH (Default: False)
    :param mpls:              Load in a mpls file (Default: False)
    :param mpls_playlist:     Playlist number, which is the number in mpls file name (Default: 0)
    :param mpls_angle:        Angle number to select in the mpls playlist (Default: 0)
    :param kwargs:            Arguments passed to the indexing filter

    :return:                  Vapoursynth clip representing input file
    """

    # TODO: find a way to NOT have to rely on a million elif's
    if file.startswith('file:///'):
        file = file[8::]

    # Error handling for some file types
    if file.endswith('.mpls') and mpls is False:
        raise ValueError("source: 'Set \"mpls = True\" and pass a path to the base Blu-ray directory for this kind of file'")  # noqa: E501
    if os.path.splitext(file)[1].lower() in annoying_formats:
        raise ValueError("source: 'Use an external indexer like d2vwitch or DGIndexNV for this kind of file'")  # noqa: E501

    if force_lsmas:
        clip = core.lsmas.LWLibavSource(file, **index_args)

    elif mpls:
        mpls_in = core.mpls.Read(file, mpls_playlist, mpls_angle)
        clip = core.std.Splice([core.lsmas.LWLibavSource(mpls_in['clip'][i], **index_args)
                                for i in range(mpls_in['count'])])

    elif file.endswith('.d2v'):
        clip = core.d2v.Source(file, **index_args)
    elif file.endswith('.dgi'):
        clip = core.dgdecodenv.DGSource(file, **index_args)
    elif is_image(file):
        clip = core.imwri.Read(file, **index_args)
    else:
        if file.endswith('.m2ts'):
            clip = core.lsmas.LWLibavSource(file, **index_args)
        else:
            clip = core.ffms2.Source(file, **index_args)

    if ref:
        if ref.format is None:
            raise ValueError("source: 'Variable-format clips not supported.'")
        clip = core.std.AssumeFPS(clip, fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)
        clip = core.resize.Bicubic(clip, width=ref.width, height=ref.height,
                                   format=ref.format.id, matrix=get_matrix(ref))
        if is_image(file):
            clip = clip * (ref.num_frames - 1)

    return clip


def edgefixer(clip: vs.VideoNode,
              left: Union[int, List[int], None] = None,
              right: Union[int, List[int], None] = None,
              top: Union[int, List[int], None] = None,
              bottom: Union[int, List[int], None] = None,
              radius: Optional[List[int]] = None,
              full_range: bool = False) -> vs.VideoNode:
    """
    A wrapper for ContinuityFixer (https://github.com/MonoS/VS-ContinuityFixer).

    Fixes the issues with over- and undershoot that it may create when fixing the edges,
    and adds what are in my opinion "more sane" ways of handling the parameters and given values.

    ...If possible, you should be using bbmod instead, though.

    Alias for this function is `lvsfunc.ef`.

    WARNING: This function may be rewritten in the future, and functionality may change!

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


def get_matrix(clip: vs.VideoNode) -> int:
    """
    Helper function to get the matrix for a clip.

    :param clip:    src clip

    :return:        Value representing a matrix
    """
    frame = clip.get_frame(0)
    w, h = frame.width, frame.height

    if frame.format.color_family == vs.RGB:
        return 0
    if frame.format.color_family == vs.YCOCG:
        return 8
    if w <= 1024 and h <= 576:
        return 5
    if w <= 2048 and h <= 1536:
        return 1
    return 9


def shift_tint(clip: vs.VideoNode, values: Union[int, Sequence[int]] = 16) -> vs.VideoNode:
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
               threshold: float = 0.25, threshold_range: Optional[int] = None) -> vs.VideoNode:
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
              threshold_range: Optional[int]) -> vs.VideoNode:
        psa = get_prop(f, "PlaneStatsAverage", float)
        if threshold_range:
            return filtered if threshold_range <= psa <= threshold else clip
        else:
            return clip if psa > threshold else filtered

    if threshold_range and threshold_range > threshold:
        raise ValueError(f"limit_dark: '\"threshold_range\" ({threshold_range}) must be a lower value than \"threshold\" ({threshold})'")  # noqa: E501

    avg = core.std.PlaneStats(clip)
    return core.std.FrameEval(clip, partial(_diff, clip=clip, filtered=filtered,
                                            threshold=threshold, threshold_range=threshold_range), avg)


def wipe_row(clip: vs.VideoNode,
             ref: Optional[vs.VideoNode] = None,
             pos: Union[Position, Tuple[int, int]] = (1, 1),
             size: Union[Size, Tuple[int, int], None] = None,
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


def allow_variable(width: Optional[int] = None, height: Optional[int] = None,
                   format: Optional[int] = None
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

        out_fmt: Optional[vs.Format] = None
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
                  seed: Union[bytearray, bytes, float, int, str, None] = None,
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

    hues: List[Union[float, int]] = [i * max_hue / (amount - 1) for i in range(amount - 1)]
    hues.append(max_hue)

    hls_color_list: List[Tuple[float, float, float]] = [colorsys.hls_to_rgb(h / 360, 0.5, 1) for h in hues]
    rgb_color_list = [[int(f * 255) for f in color] for color in hls_color_list]

    if rand:
        shuffle = random.shuffle if seed is None else random.Random(seed).shuffle
        shuffle(rgb_color_list)

    return [core.std.BlankClip(color=color, **blank_clip_args) for color in rgb_color_list]


# compatibility since these were moved to util
replace_ranges = _replace_ranges
scale_thresh = _scale_thresh

# TODO: Write function that only masks px of a certain color/threshold of colors.
#       Think the magic wand tool in various image-editing programs.
