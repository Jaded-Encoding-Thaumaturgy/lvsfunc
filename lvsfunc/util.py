from __future__ import annotations

import colorsys
import random
import warnings
from functools import partial, wraps
from typing import Any, Callable, cast

import vapoursynth as vs
from typing_extensions import TypeGuard
from vskernels import Bicubic, Kernel, VNodeCallable, get_kernel, get_matrix, get_prop
from vsutil import depth, get_subsampling, get_w, get_y

from .exceptions import InvalidFormatError, VariableFormatError, VariableResolutionError
from .types import Range, _VideoNode

core = vs.core


__all__ = [
    'allow_variable',
    'check_variable',
    'chroma_injector',
    'colored_clips',
    'frames_since_bookmark',
    'load_bookmarks',
    'normalize_ranges',
    'padder',
    'quick_resample',
    'replace_ranges', 'rfs',
    'scale_peak',
    'scale_thresh'
]


def quick_resample(clip: vs.VideoNode,
                   function: Callable[[vs.VideoNode], vs.VideoNode]
                   ) -> vs.VideoNode:
    """
    Quickly resample to 32/16/8 bit and back to the original depth in a one-liner.

    .. warning:
        This function will be either reworked or removed in a future version!

    Useful for filters that only work in 16 bit or lower when you're working in float.

    :param clip:        Clip to process.
    :param function:    Filter to run after resampling (accepts and returns clip).

    :return:            Filtered clip in original depth.
    """
    warnings.warn("quick_resample: 'This function will be either reworked or removed in a future version!'",
                  FutureWarning)

    assert check_variable_format(clip, "quick_resample")

    try:  # Excepts all generic because >plugin/script writers being consistent >_>
        dither = depth(clip, 32)
        filtered = function(dither)
    except:  # noqa: E722
        try:
            dither = depth(clip, 16)
            filtered = function(dither)
        except:  # noqa: E722
            dither = depth(clip, 8)
            filtered = function(dither)

    return depth(filtered, clip.format.bits_per_sample)


def normalize_ranges(clip: vs.VideoNode, ranges: Range | list[Range]) -> list[tuple[int, int]]:
    r"""
    Normalize :py:func:`lvsfunc.types.Range`\(s) to a list of inclusive positive integer ranges.

    :param clip:        Reference clip used for length.
    :param ranges:      Single :py:class:`lvsfunc.types.Range`,
                        or a list of :py:class:`lvsfunc.types.Range`\(s).

    :return:            List of inclusive positive ranges.
    """
    ranges = ranges if isinstance(ranges, list) else [ranges]

    out = []
    for r in ranges:
        if isinstance(r, tuple):
            start, end = r
            if start is None:
                start = 0
            if end is None:
                end = clip.num_frames - 1
        elif r is None:
            start = clip.num_frames - 1
            end = clip.num_frames - 1
        else:
            start = r
            end = r
        if start < 0:
            start = clip.num_frames - 1 + start
        if end < 0:
            end = clip.num_frames - 1 + end
        out.append((start, end))

    return out


def replace_ranges(clip_a: vs.VideoNode,
                   clip_b: vs.VideoNode,
                   ranges: Range | list[Range] | None,
                   exclusive: bool = False,
                   use_plugin: bool = True) -> vs.VideoNode:
    """
    Remaps frame indices in a clip using ints and tuples rather than a string.

    Frame ranges are inclusive. This behaviour can be changed by setting `exclusive=True`.

    If you're trying to splice in clips, it's recommended you use `vsutil.insert_clip` instead.

    This function will try to call the `VapourSynth-RemapFrames` plugin before doing any of its own processing.
    This should come with a speed boost, so it's recommended you install it.

    Examples with clips ``black`` and ``white`` of equal length:

        * ``replace_ranges(black, white, [(0, 1)])``: replace frames 0 and 1 with ``white``
        * ``replace_ranges(black, white, [(None, None)])``: replace the entire clip with ``white``
        * ``replace_ranges(black, white, [(0, None)])``: same as previous
        * ``replace_ranges(black, white, [(200, None)])``: replace 200 until the end with ``white``
        * ``replace_ranges(black, white, [(200, -1)])``: replace 200 until the end with ``white``,
          leaving 1 frame of ``black``

    Alias for this function is ``lvsfunc.rfs``.

    Dependencies:

    * `VapourSynth-RemapFrames <https://github.com/Irrational-Encoding-Wizardry/Vapoursynth-RemapFrames>`_

    :param clip_a:          Original clip.
    :param clip_b:          Replacement clip.
    :param ranges:          Ranges to replace clip_a (original clip) with clip_b (replacement clip).

                            Integer values in the list indicate single frames,

                            Tuple values indicate inclusive ranges.

                            Negative integer values will be wrapped around based on clip_b's length.

                            None values are context dependent:

                                * None provided as sole value to ranges: no-op
                                * Single None value in list: Last frame in clip_b
                                * None as first value of tuple: 0
                                * None as second value of tuple: Last frame in clip_b
    :param exclusive:       Use exclusive ranges (Default: False).
    :param use_plugin:      Use the ReplaceFramesSimple plugin for the rfs call (Default: True).

    :return:                Clip with ranges from clip_a replaced with clip_b.

    :raises ValueError:     A string is passed instead of a list of ranges.
    """
    if ranges != 0 and not ranges:
        return clip_a

    if isinstance(ranges, str):  # type:ignore[unreachable]
        raise ValueError("replace_ranges: 'This function does not take strings! Please use a list of tuples or ints!")

    if clip_a.num_frames != clip_b.num_frames:
        warnings.warn("replace_ranges: "
                      f"'The number of frames ({clip_a.num_frames} vs. {clip_b.num_frames}) do not match! "
                      "The function will still work, but you may run into unintended errors with the output clip!'")

    nranges = normalize_ranges(clip_b, ranges)

    if use_plugin and hasattr(core, 'remap'):
        return core.remap.ReplaceFramesSimple(
            clip_a, clip_b, mismatch=True,
            mappings=' '.join(f'[{s} {e + (exclusive if s != e else 0)}]' for s, e in nranges)
        )

    out = clip_a
    shift = 1 + exclusive

    for start, end in nranges:
        tmp = clip_b[start:end + shift]
        if start != 0:
            tmp = out[: start] + tmp
        if end < out.num_frames - 1:
            tmp = tmp + out[end + shift:]
        out = tmp

    return out


def scale_thresh(thresh: float, clip: vs.VideoNode, assume: int | None = None) -> float:
    """
    Scale binarization thresholds from float to int.

    :param thresh:          Threshold [0, 1]. If greater than 1, assumed to be in native clip range.
    :param clip:            Clip to scale to.
    :param assume:          | Assume input is this depth when given input > 1.
                            | If ``None``, assume ``clip``'s format (Default: None).

    :return:                Threshold scaled to [0, 2^clip.depth - 1] (if vs.INTEGER).

    :raises ValueError:     Thresholds are negative.
    """
    assert check_variable_format(clip, "scale_thresh")

    if thresh < 0:
        raise ValueError("scale_thresh: 'Thresholds must be positive!'")
    if thresh > 1:
        return thresh if not assume \
            else round(thresh/((1 << assume) - 1) * ((1 << clip.format.bits_per_sample) - 1))
    return thresh if clip.format.sample_type == vs.FLOAT or thresh > 1 \
        else round(thresh * ((1 << clip.format.bits_per_sample) - 1))


def scale_peak(value: float, peak: float) -> float:
    """Full-range scale function that scales a value from [0, 255] to [0, peak]."""
    return value * peak / 255


def padder(clip: vs.VideoNode,
           left: int = 32, right: int = 32,
           top: int = 32, bottom: int = 32) -> vs.VideoNode:
    """
    Pad out the pixels on the side by the given amount of pixels.

    For a 4:2:0 clip, the output must be an even resolution.

    Dependencies:

    * `VapourSynth-fillborders <https://github.com/dubhater/vapoursynth-fillborders>`_

    :param clip:        Clip to process.
    :param left:        Padding added to the left side of the clip.
    :param right:       Padding added to the right side of the clip.
    :param top:         Padding added to the top side of the clip.
    :param bottom:      Padding added to the bottom side of the clip.

    :return:            Padded clip.

    :raises ValueError: A non-even resolution is passed on a YUV420 clip.
    """
    assert check_variable(clip, "padder")

    width = clip.width+left+right
    height = clip.height+top+bottom

    if get_subsampling(clip) == '420' and ((width % 2 != 0) or (height % 2 != 0)):
        raise ValueError("padder: 'Values must result in an even resolution when passing a YUV420 clip!'")

    scaled = core.resize.Point(clip, width, height,
                               src_top=-1*top, src_left=-1*left,
                               src_width=width, src_height=height)
    return core.fb.FillBorders(scaled, left=left, right=right, top=top, bottom=bottom)


def check_variable_format(clip: vs.VideoNode, function: str) -> TypeGuard[_VideoNode]:
    """
    Check for variable format and return an error if found.

    :raises VariableFormatError:    The clip is of a variable format.
    """
    if clip.format is None:
        raise VariableFormatError(function)
    return True


def check_variable_resolution(clip: vs.VideoNode, function: str) -> None:
    """
    Check for variable width or height and return an error if found.

    :raises VariableResolutionError:    The clip has a variable resolution.
    """
    if 0 in (clip.width, clip.height):
        raise VariableResolutionError(function)


def check_variable(clip: vs.VideoNode, function: str) -> TypeGuard[_VideoNode]:
    """
    Check for variable format and a variable resolution and return an error if found.

    :raises VariableFormatError:        The clip is of a variable format.
    :raises VariableResolutionError:    The clip has a variable resolution.
    """
    check_variable_format(clip, function)
    check_variable_resolution(clip, function)
    return True


def load_bookmarks(bookmark_path: str) -> list[int]:
    """
    Load VSEdit bookmarks.

    load_bookmarks(os.path.basename(__file__)+".bookmarks")
    will load the VSEdit bookmarks for the current Vapoursynth script.

    :param bookmark_path:  Path to bookmarks file.

    :return:               A list of bookmarked frames.
    """
    with open(bookmark_path) as f:
        bookmarks = [int(i) for i in f.read().split(", ")]

        if bookmarks[0] != 0:
            bookmarks.insert(0, 0)

    return bookmarks


def frames_since_bookmark(clip: vs.VideoNode, bookmarks: list[int]) -> vs.VideoNode:
    """
    Display frames since last bookmark to create easily reusable scenefiltering.

    Can be used in tandem with :py:func:`lvsfunc.misc.load_bookmarks` to import VSEdit bookmarks.

    :param clip:        Clip to process.
    :param bookmarks:   A list of bookmarks.

    :return:            Clip with bookmarked frames.
    """
    def _frames_since_bookmark(n: int, clip: vs.VideoNode, bookmarks: list[int]) -> vs.VideoNode:
        for i, bookmark in enumerate(bookmarks):
            frames_since = n - bookmark

            if frames_since >= 0 and i + 1 >= len(bookmarks):
                result = frames_since
            elif frames_since >= 0 and n - bookmarks[i + 1] < 0:
                result = frames_since
                break

        return core.text.Text(clip, str(result))
    return core.std.FrameEval(clip, partial(_frames_since_bookmark, clip=clip, bookmarks=bookmarks))


def chroma_injector(func: VNodeCallable) -> VNodeCallable:
    """
    Inject reference chroma.

    This is a function decorator. That means it must be called above a function. For example:

    .. code-block:: py

        @chroma_injector()
        def function(clip: vs.VideoNode) -> vs.VideoNode:
            ...

    This can be used to inject reference chroma into a function which would normally
    only receive luma, such as an upscaler passed to :py:func:`lvsfunc.scale.descale`.

    The chroma is resampled to the input clip's width, height, and pixel format,
    shuffled to YUV444PX, then passed to the function.
    Luma is then extracted from the function result and returned.

    The first argument of the function is assumed to be the luma source.
    This works with variable resolution and may work with variable format,
    however the latter is wholly untested and likely a bad idea in every conceivable use case.

    :param func:                    Function to call with injected chroma.

    :return:                        Decorated function.

    :raises InvalidFormatError:     Input clip is not YUV or GRAY.
    :raises InvalidFormatError:     Output clip is not YUV or GRAY.
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
                raise InvalidFormatError("chroma_injector", "{func}: 'Input clip must be of a YUV or GRAY format!'")

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
                raise InvalidFormatError("chroma_injector",
                                         "{func}: 'can only decorate function with YUV and/or GRAY format return!'")

            if result.format.color_family == vs.GRAY:
                return result

            res_fmt = core.register_format(vs.GRAY, result.format.sample_type,
                                           result.format.bits_per_sample, 0, 0)
            return allow_variable(format=res_fmt.id)(get_y)(result)
        else:
            return allow_variable()(get_y)(result)

    return cast(VNodeCallable, inner)


def colored_clips(amount: int,
                  max_hue: int = 300,
                  rand: bool = True,
                  seed: bytearray | bytes | float | str | None = None,
                  **kwargs: Any
                  ) -> list[vs.VideoNode]:
    r"""
    Return a list of BlankClips with unique colors in sequential or random order.

    The colors will be evenly spaced by hue in the HSL colorspace.

    Useful maybe for comparison functions or just for getting multiple uniquely colored BlankClips for testing purposes.

    Will always return a pure red clip in the list as this is the RGB equivalent of the lowest HSL hue possible (0).

    Written by `Dave <https://github.com/OrangeChannel>`_.

    :param amount:          Number of VideoNodes to return.
    :param max_hue:         Maximum hue (0 < hue <= 360) in degrees to generate colors from (uses the HSL color model).
                            Setting this higher than ``315`` will result in the clip colors looping back towards red
                            and is not recommended for visually distinct colors.
                            If the `amount` of clips is higher than the `max_hue` expect there to be identical
                            or visually similar colored clips returned (Default: 300)
    :param rand:            Randomizes order of the returned list (Default: True).
    :param seed:            Bytes-like object passed to ``random.seed`` which allows for consistent randomized order.
                            of the resulting clips (Default: None)
    :param kwargs:          Arguments passed to :py:func:`vapoursynth.core.std.BlankClip` (Default: keep=1).

    :return:                List of uniquely colored clips in sequential or random order.

    :raises ValueError:     ``amount`` is less than 2.
    :raises ValueError:     ``max_hue`` is not between 0–360.
    """
    if amount < 2:
        raise ValueError("colored_clips: `amount` must be at least 2!")
    if not (0 < max_hue <= 360):
        raise ValueError("colored_clips: `max_hue` must be greater than 0 and less than 360 degrees!")

    blank_clip_args: dict[str, Any] = {'keep': 1, **kwargs}

    hues = [i * max_hue / (amount - 1) for i in range(amount - 1)] + [max_hue]

    hls_color_list = [colorsys.hls_to_rgb(h / 360, 0.5, 1) for h in hues]
    rgb_color_list = [[int(f * 255) for f in color] for color in hls_color_list]

    if rand:
        shuffle = random.shuffle if seed is None else random.Random(seed).shuffle
        shuffle(rgb_color_list)

    return [core.std.BlankClip(color=color, **blank_clip_args) for color in rgb_color_list]


def allow_variable(width: int | None = None, height: int | None = None,
                   format: int | None = None
                   ) -> Callable[[Callable[..., vs.VideoNode]], Callable[..., vs.VideoNode]]:
    """
    Allow a variable-res and/or variable-format clip to be passed to a function.

    This is a function decorator. That means it must be called above a function. For example:

    .. code-block:: py

        @allow_variable()
        def function(clip: vs.VideoNode) -> vs.VideoNode:
            ...

    This can be used on functions that otherwise would not be able to accept it.
    Implemented by FrameEvaling and resizing the clip to each frame.

    Does not work when the function needs to return a different format unless an output format is specified.
    As such, this decorator must be called as a function when used (e.g. ``@allow_variable()``
    or ``@allow_variable(format=vs.GRAY16)``).

    If the provided clip is variable format, no output format is required to be specified.

    :param width:       Output clip width.
    :param height:      Output clip height.
    :param format:      Output clip format.

    :return:            Function decorator for the given output format.
    """
    if height is not None:
        width = width if width else get_w(height)

    def inner(func: VNodeCallable) -> VNodeCallable:
        @wraps(func)
        def inner2(clip: vs.VideoNode, *args: Any, **kwargs: Any) -> vs.VideoNode:
            def frameeval_wrapper(n: int, f: vs.VideoFrame) -> vs.VideoNode:
                res = func(clip.resize.Point(f.width, f.height, format=f.format.id), *args, **kwargs)
                return res.resize.Point(format=format) if format else res

            clip_out = clip.resize.Point(format=format) if format else clip
            clip_out = clip_out.resize.Point(width, height) if width and height else clip_out
            return core.std.FrameEval(clip_out, frameeval_wrapper, prop_src=[clip])

        return cast(VNodeCallable, inner2)

    return inner


def match_clip(clip: vs.VideoNode, ref: vs.VideoNode,
               dimensions: bool = True, vformat: bool = True,
               matrices: bool = True, length: bool = False,
               kernel: Kernel | str = Bicubic(b=0, c=1/2)) -> vs.VideoNode:
    """
    Try matching the given clip's format with the reference clip's.

    :param clip:        Clip to process.
    :param ref:         Reference clip.
    :param dimensions:  Match video dimensions (Default: True).
    :param vformat:     Match video formats (Default: True).
    :param matrices:    Match matrix/transfer/primaries (Default: True).
    :param length:      Match clip length (Default: False).
    :param kernel:      py:class:`vskernels.Kernel` object used for the format conversion.
                        This can also be the string name of the kernel
                        (Default: py:class:`vskernels.Bicubic(b=0, c=1/2)`).

    :return:            Clip that matches the ref clip in format.
    """
    assert check_variable(clip, "match_clip")
    assert check_variable(ref, "match_clip")

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    clip = clip * ref.num_frames if length else clip
    clip = kernel.scale(clip, ref.width, ref.height) if dimensions else clip

    if vformat:
        clip = kernel.resample(clip, format=ref.format, matrix=get_matrix(ref))

    if matrices:
        ref_frame = ref.get_frame(0)

        clip = clip.std.SetFrameProps(
            _Matrix=get_prop(ref_frame, '_Matrix', int),
            _Transfer=get_prop(ref_frame, '_Transfer', int),
            _Primaries=get_prop(ref_frame, '_Primaries', int))

    return clip.std.AssumeFPS(fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)


# Aliases
rfs = replace_ranges
