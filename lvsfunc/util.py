from __future__ import annotations

import colorsys
import random
import re
from typing import Any

from vskernels import Catrom, Kernel, KernelT
from vstools import (
    CustomIndexError, CustomValueError, FrameRangeN, FrameRangesN, Matrix, check_variable, core, get_prop, vs
)

__all__ = [
    'colored_clips',
    'match_clip',
    'convert_rfs',
]


def colored_clips(
    amount: int, max_hue: int = 300, rand: bool = True, seed: Any | None = None, **kwargs: Any
) -> list[vs.VideoNode]:
    """
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
        raise CustomIndexError("`amount` must be at least 2!", colored_clips)
    if not (0 < max_hue <= 360):
        raise CustomValueError("`max_hue` must be greater than 0 and less than 360 degrees!", colored_clips)

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


def convert_rfs(rfs_string: str) -> FrameRangesN:
    """
    A utility function to convert `ReplaceFramesSimple`-styled ranges to `replace_ranges`-styled ranges.

    This function accepts the RFS ranges as a string only. This is in line with how RFS handles them.
    The string will be validated before it's passed on. As with all framerange-related functions,
    the more ranges you have, the slower the function will become.

    This function works with both '[x y]' and 'x' styles of frame numbering.
    If no frames could be found, it will simply return an empty list.

    :param rfs_string:      A string representing frame ranges, as you would for ReplaceFramesSimple.

    :return:                A FrameRangesN list containing frame ranges as accepted by `replace_ranges`.
                            If no frames are found, it will simply return an empty list.

    :raises ValueError:     Invalid input string is passed.
    """
    rfs_string = str(rfs_string).strip()

    if not set(rfs_string).issubset('0123456789[] '):
        raise CustomValueError('Invalid characters were found in the input string.', convert_rfs)

    matches = re.findall(r'\[(\s*?\d+\s\d+\s*?)\]|(\d+)', rfs_string)
    ranges = list[FrameRangeN]()

    if not matches:
        return ranges

    for match in [next(y for y in x if y) for x in matches]:
        try:
            ranges += [int(match)]
        except ValueError:
            ranges += [tuple(int(x) for x in str(match).strip().split(' '))]  # type:ignore[list-item]

    return ranges
