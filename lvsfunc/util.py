from __future__ import annotations

import colorsys
import random
from functools import partial
from typing import Any

from vskernels import Catrom, Kernel, KernelT
from vstools import Matrix, check_variable, core, get_prop, vs

__all__ = [
    'colored_clips',
    'frames_since_bookmark',
    'load_bookmarks',
    'match_clip',
    'truncate_string',
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


def truncate_string(str_in: str, max_length: int, suffix: str = "...") -> str:
    """Truncate a string if it surpasses a certain length."""
    if len(str_in) > max_length:
        return str_in[:max_length - len(suffix)] + suffix

    return str_in
