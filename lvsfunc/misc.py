"""
    Miscellaneous functions and wrappers that didn't really have a place in any other submodules.
"""
import colorsys
import contextlib
import os
import pathlib
import random
import warnings
from functools import partial, wraps
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union, cast

import vapoursynth as vs
from vsutil import Dither, Range, depth, get_depth, get_subsampling, get_w, get_y, is_image

from .util import get_prop

core = vs.core


def source(file: str, ref: Optional[vs.VideoNode] = None,
           force_lsmas: bool = False,
           mpls: bool = False, mpls_playlist: int = 0, mpls_angle: int = 0) -> vs.VideoNode:
    """
    Generic clip import function.
    Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced.
    It also automatically determines if an image has been imported.
    You can set its fps using 'fpsnum' and 'fpsden', or using a reference clip with 'ref'.

    Alias for this function is `lvsfunc.src`.

    Dependencies:

        * d2vsource (optional: d2v sources)
        * dgdecodenv (optional: dgi sources)
        * mvsfunc (optional: reference clip mode)
        * vapoursynth-readmpls (optional: mpls sources)

    :param file:              Input file
    :param ref:               Use another clip as reference for the clip's format,
                              resolution, and framerate (Default: None)
    :param force_lsmas:       Force files to be imported with L-SMASH (Default: False)
    :param mpls:              Load in a mpls file (Default: False)
    :param mpls_playlist:     Playlist number, which is the number in mpls file name (Default: 0)
    :param mpls_angle:        Angle number to select in the mpls playlist (Default: 0)

    :return:                  Vapoursynth clip representing input file
    """

    # TODO: Consider adding kwargs for additional options,
    #       find a way to NOT have to rely on a million elif's
    if file.startswith('file:///'):
        file = file[8::]

    # Error handling for some file types
    if file.endswith('.mpls') and mpls is False:
        raise ValueError("source: 'Please set \"mpls = True\" and give a path to the base Blu-ray directory when trying to load in mpls files'")  # noqa: E501
    if file.endswith('.vob') or file.endswith('.ts'):
        raise ValueError("source: 'Please index VOB and TS files with d2v before importing them'")

    if force_lsmas:
        return core.lsmas.LWLibavSource(file)

    elif mpls:
        mpls_in = core.mpls.Read(file, mpls_playlist, mpls_angle)
        clip = core.std.Splice([core.lsmas.LWLibavSource(mpls_in['clip'][i]) for i in range(mpls_in['count'])])

    elif file.endswith('.d2v'):
        clip = core.d2v.Source(file)
    elif file.endswith('.dgi'):
        clip = core.dgdecodenv.DGSource(file)
    elif is_image(file):
        clip = core.imwri.Read(file)
    else:
        if file.endswith('.m2ts'):
            clip = core.lsmas.LWLibavSource(file)
        else:
            clip = core.ffms2.Source(file)

    if ref:
        try:
            from mvsfunc import GetMatrix
        except ModuleNotFoundError:
            raise ModuleNotFoundError("source: missing dependency 'mvsfunc'")

        if ref.format is None:
            raise ValueError("source: 'Variable-format clips not supported.'")
        clip = core.std.AssumeFPS(clip, fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)
        clip = core.resize.Bicubic(clip, width=ref.width, height=ref.height,
                                   format=ref.format.id, matrix_s=str(GetMatrix(ref)))
        if is_image(file):
            clip = clip * (ref.num_frames - 1)

    return clip


def replace_ranges(clip_a: vs.VideoNode,
                   clip_b: vs.VideoNode,
                   ranges: List[Union[int, Tuple[int, int]]]) -> vs.VideoNode:
    """
    A replacement for ReplaceFramesSimple that uses ints and tuples rather than a string.
    Frame ranges are inclusive.

    Written by louis.

    Alias for this function is `lvsfunc.rfs`.

    :param clip_a:     Original clip
    :param clip_b:     Replacement clip
    :param ranges:     Ranges to replace clip_a (original clip) with clip_b (replacement clip).
                       Integer values in the list indicate single frames,
                       Tuple values indicate inclusive ranges.

    :return:           Clip with ranges from clip_a replaced with clip_b
    """
    out = clip_a
    for r in ranges:
        if type(r) is tuple:
            start, end = cast(Tuple[int, int], r)
        else:
            start = cast(int, r)
            end = cast(int, r)
        tmp = clip_b[start:end + 1]
        if start != 0:
            tmp = out[: start] + tmp
        if end < out.num_frames - 1:
            tmp = tmp + out[end + 1:]
        out = tmp
    return out


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

    Dependencies: vs-continuityfixer

    :param clip:        Input clip
    :param left:        Number of pixels to fix on the left (Default: None)
    :param right:       Number of pixels to fix on the right (Default: None)
    :param top:         Number of pixels to fix on the top (Default: None)
    :param bottom:      Number of pixels to fix on the bottom (Default: None)
    :param radius:      Radius for edgefixing (Default: None)
    :param full_range:  Does not run the expression over the clip to fix over/undershoot (Default: False)

    :return:            Clip with fixed edges
    """

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


def fix_cr_tint(clip: vs.VideoNode, value: int = 128) -> vs.VideoNode:
    """
    Tries to forcibly fix Crunchyroll's green tint by adding pixel values.

    :param clip:   Input clip
    :param value:  Value added to every pixel (Default: 128)

    :return:       Clip with CR tint fixed
    """
    if get_depth(clip) != 16:
        clip = depth(clip, 16)
    return core.std.Expr(clip, f'x {value} +')


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
             secondary: Optional[vs.VideoNode] = None,
             width: int = 1, height: int = 1,
             offset_x: int = 0, offset_y: int = 0,
             width2: Optional[int] = None, height2: Optional[int] = None,
             offset_x2: Optional[int] = None, offset_y2: Optional[int] = None,
             show_mask: bool = False) -> vs.VideoNode:
    """
    Simple function to wipe a row with a blank clip.
    You can also give it a different clip to replace a row with.

    if width2, height2, etc. are given, it will merge the two masks.

    Dependencies: kagefunc

    :param clip:           Input clip
    :param secondary:      Clip to replace wiped rows with (Default: None)
    :param width:          Width of row (Default: 1)
    :param height:         Height of row (Default: 1)
    :param offset_x:       X-offset of row (Default: 0)
    :param offset_y:       Y-offset of row (Default: 0)
    :param width2:         Width of row 2 (Default: None)
    :param height2:        Height of row 2 (Default: None)
    :param offset_x2:      X-offset of row 2 (Default: None)
    :param offset_y2:      Y-offset of row 2 (Default: None)

    :return:               Clip with rows wiped
    """
    try:
        import kagefunc as kgf
    except ModuleNotFoundError:
        raise ModuleNotFoundError("wipe_row: missing dependency 'kagefunc'")

    secondary = secondary or core.std.BlankClip(clip)

    sqmask = kgf.squaremask(clip, width, height, offset_x, offset_y)
    if width2 and height2:
        if offset_x2 is None:
            raise TypeError("wipe_row: 'offset_x2 cannot be None if using two masks'")
        sqmask2 = kgf.squaremask(clip, width2, height2, offset_x2, offset_y - 1 if offset_y2 is None else offset_y2)
        sqmask = core.std.Expr([sqmask, sqmask2], "x y +")

    if show_mask:
        return sqmask
    return core.std.MaskedMerge(clip, secondary, sqmask)


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
                  seed: Optional[Union[bytearray, bytes, float, int, str]] = None,
                  **kwargs: Any
                  ) -> List[vs.VideoNode]:
    """
    Returns a list of BlankClips with unique colors in sequential or random order.
    The colors will be evenly spaced by hue in the HSL colorspace.

    Useful maybe for comparison functions or just for getting multiple uniquely colored BlankClips for testing purposes.

    Will always return a pure red clip in the list as this is the RGB equivalent of the lowest HSL hue possible (0).

    Written by Dave <orangechannel@pm.me>.

    :param amount:  Number of ``vapoursynth.VideoNode``s to return
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


def save(clips: Dict[str, vs.VideoNode],
         frames: Optional[List[int]] = None,
         random_number: int = 0,
         zoom: int = 1,
         dither_type: Optional[Union[str, Dither]] = None,
         folder: bool = False,
         save_location: Optional[Union[str, pathlib.Path]] = None,
         ) -> None:
    """
    Writes frames as RGB24 PNG files for comparison websites or local comparison.

    Written by Dave <orangechannel@pm.me>.

    :param clips:         Dictionary of `name:clip` for all clips you want to save frames from.
                          Accepts YUV or RGB clips only.
                          Assumes all YUV-clips are limited range and all RGB-clips are full range.
    :param frames:        List of frame numbers to save from each clip.
    :param random_number: Number of random frames to save from each clip.
                          Will default to ``1`` if no `frames` are given (Default: ``0``)
    :param folder:        Whether or not to save clips in named folders
                          instead of prefixing the files with the clip names (Default: ``False``)
    :param dither_type:   ``dither_type`` override for ``vsutil.depth`` for clips >8-bit (Default: ``None``)
    :param zoom:          Zoom factor for image output.
                          Useful for comparison websites as zooming with a browser is not reliable
                          and might not use point/nearest-neighbor (Default: ``1``)
    :param save_location: An optional folder path to save the images/sub-folders to
                          (will normally save in the same folder as the script is ran in) (Default: ``None``)
    """
    @contextlib.contextmanager
    def _cd(newdir: Union[str, pathlib.Path]) -> None:
        prevdir = os.getcwd()
        os.chdir(os.path.expanduser(newdir))
        try:
            yield
        finally:
            os.chdir(prevdir)

    should_cd_back = False
    cwdir = os.getcwd()

    if frames is None:
        frames = []
    else:
        frames = list(set(frames))

    widths = [clip.width for clip in clips.values()]
    heights = [clip.height for clip in clips.values()]

    if 0 in widths or 0 in heights:  # because of the zoom resize, input width/height can't be `0`
        raise ValueError("save: variable-resolution clips not allowed")
    if None in [clip.format for clip in clips.values()]:
        raise ValueError("save: variable-format clips not allowed")

    if len(set(widths)) > 1 or len(set(heights)) > 1:
        warnings.warn("save: all clips should have same dimensions for a comparison")

    max_frame = min([clip.num_frames for clip in clips.values()]) - 1
    if not all(f <= max_frame for f in frames):
        raise ValueError("save: specified frame numbers out of range on one or more clips")
    if len(frames) == 0 and random_number == 0:
        random_number = 1

    if random_number:
        if len(frames) == max_frame + 1:
            pass  # every frame possible is already in the `frames` list
        else:
            # makes sure not to generate more random frame numbers than currently missing in `frames`
            random_number = min([random_number, (max_frame + 1) - len(frames)])

            random_frame_numbers = random.sample(range(max_frame + 1), random_number)
            while any(f in frames for f in random_frame_numbers):
                random_frame_numbers = random.sample(range(max_frame + 1), random_number)

            frames += random_frame_numbers

    if save_location and os.path.isdir(save_location):
        should_cd_back = True
        os.chdir(save_location)

    for name, clip in clips.items():
        subsampled = get_subsampling(clip) not in ('444', None)
        if subsampled:
            assert clip.format is not None
            clip = clip.resize.Bicubic(filter_param_a_uv=1/3,
                                       filter_param_b_uv=1/3,
                                       format=clip.format.replace(subsampling_w=0, subsampling_h=0).id,
                                       )

        assert clip.format is not None
        range_in = Range.LIMITED if clip.format.color_family == vs.ColorFamily.YUV else Range.FULL
        clips[name] = depth(clip, 8, range_in=range_in, dither_type=dither_type)

    def _get_matrix_s(clip: vs.VideoNode) -> str:
        assert clip.format is not None
        if clip.format.color_family == vs.ColorFamily.YUV:
            return '709'
        elif clip.format.color_family == vs.ColorFamily.RGB:
            return 'rgb'
        else:
            raise ValueError("save: expected a YUV or RGB clip")

    def _to_rgb(clip: vs.VideoNode, f: int) -> vs.VideoNode:
        return clip[f].resize.Point(width=zoom * clip.width,
                                    height=zoom * clip.height,
                                    format=vs.RGB24,
                                    range=Range.FULL,
                                    matrix_in_s=_get_matrix_s(clip),
                                    dither_type=Dither.ERROR_DIFFUSION.value,
                                    prefer_props=True,
                                    )

    if folder:
        for name, clip in clips.items():
            os.makedirs(name, exist_ok=True)
            with _cd(name):
                for f in frames:
                    out = core.imwri.Write(_to_rgb(clip, f), 'PNG', '%06d.png', firstnum=f)
                    out.get_frame(0)
    else:
        for name, clip in clips.items():
            for f in frames:
                # this syntax is picked up by https://slow.pics/ for easy drag-n-drop
                out = core.imwri.Write(_to_rgb(clip, f), 'PNG', f'{name}%06d.png', firstnum=f)
                out.get_frame(0)

    if should_cd_back:
        os.chdir(cwdir)


# TODO: Write function that only masks px of a certain color/threshold of colors.
#       Think the magic wand tool in various image-editing programs.


# TODO: Write a wrapper for duplex's Chroma Reconstructor.
#       It should optimally be able to accept anything and accurately reconstruct it,
#       so long as the user gives it the right clips. Otherwise, it should assume
#       that the chroma was scaled down using Nearest Neighbor or something alike.
