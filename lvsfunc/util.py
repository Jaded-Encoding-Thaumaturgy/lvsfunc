from __future__ import annotations

import colorsys
import random
from functools import partial, wraps
from typing import Any, Callable, cast

from vskernels import Catrom, Kernel, KernelT
from vstools import F_VD, InvalidColorFamilyError, Matrix, check_variable, core, get_prop, get_w, get_y, vs

__all__ = [
    'allow_variable',
    'chroma_injector',
    'colored_clips',
    'frames_since_bookmark',
    'load_bookmarks'
]


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


def chroma_injector(func: F_VD) -> F_VD:
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

    :raises InvalidColorFamilyError:     Input clip is not YUV or GRAY.
    :raises InvalidColorFamilyError:     Output clip is not YUV or GRAY.
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
            InvalidColorFamilyError.check(clip, (vs.GRAY, vs.YUV), chroma_injector)

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
            InvalidColorFamilyError.check(
                result, (vs.GRAY, vs.YUV), chroma_injector,
                message='Can only decorate function returning clips having {correct} color family!'
            )

            if result.format.color_family == vs.GRAY:
                return result

            res_fmt = core.register_format(vs.GRAY, result.format.sample_type,
                                           result.format.bits_per_sample, 0, 0)
            return allow_variable(format=res_fmt.id)(get_y)(result)
        else:
            return allow_variable()(get_y)(result)

    return cast(F_VD, inner)


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

    def inner(func: F_VD) -> F_VD:
        @wraps(func)
        def inner2(clip: vs.VideoNode, *args: Any, **kwargs: Any) -> vs.VideoNode:
            def frameeval_wrapper(n: int, f: vs.VideoFrame) -> vs.VideoNode:
                res = func(clip.resize.Point(f.width, f.height, format=f.format.id), *args, **kwargs)
                return res.resize.Point(format=format) if format else res

            clip_out = clip.resize.Point(format=format) if format else clip
            clip_out = clip_out.resize.Point(width, height) if width and height else clip_out
            return core.std.FrameEval(clip_out, frameeval_wrapper, prop_src=[clip])

        return cast(F_VD, inner2)

    return inner


def match_clip(clip: vs.VideoNode, ref: vs.VideoNode,
               dimensions: bool = True, vformat: bool = True,
               matrices: bool = True, length: bool = False,
               kernel: KernelT = Catrom) -> vs.VideoNode:
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
                        (Default: py:class:`vskernels.Catrom`).

    :return:            Clip that matches the ref clip in format.
    """
    assert check_variable(clip, "match_clip")
    assert check_variable(ref, "match_clip")

    kernel = Kernel.ensure_obj(kernel)

    clip = clip * ref.num_frames if length else clip
    clip = kernel.scale(clip, ref.width, ref.height) if dimensions else clip

    if vformat:
        assert ref.format
        clip = kernel.resample(clip, format=ref.format, matrix=Matrix.from_video(ref))

    if matrices:
        ref_frame = ref.get_frame(0)

        clip = clip.std.SetFrameProps(
            _Matrix=get_prop(ref_frame, '_Matrix', int),
            _Transfer=get_prop(ref_frame, '_Transfer', int),
            _Primaries=get_prop(ref_frame, '_Primaries', int)
        )

    return clip.std.AssumeFPS(fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)
