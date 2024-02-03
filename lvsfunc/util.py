from __future__ import annotations

import colorsys
import random
import re
from typing import Any

from vstools import (CustomIndexError, CustomValueError, FrameRangeN,
                     FrameRangesN, KwargsT, check_variable_resolution, core,
                     get_h, get_w, vs)

__all__ = [
    'colored_clips',
    'convert_rfs',
    'get_match_centers_scaling',
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


def get_match_centers_scaling(
    clip: vs.VideoNode, target_width: int | None = None, target_height: int | None = 720
) -> KwargsT:
    """
    Convenience function to calculate the native resolution for sources that were upsampled
    using the "match centers" model as opposed to the more common "match edges" models.

    While match edges will align the edges of the outermost pixels in the target image,
    match centers will instead align the *centers* of the outermost pixels.

    Here's a visual example for a 3x1 image upsampled to 9x1:

        * Match edges:

    +-----------+-----------+-----------+
    |     .     |     .     |     .     |
    +-----------+-----------+-----------+
    ↓                                   ↓
    +---+---+---+---+---+---+---+---+---+
    | . | . | . | . | . | . | . | . | . |
    +---+---+---+---+---+---+---+---+---+

        * Match centers:

    +-----------+-----------+-----------+
    |     .     |     .     |     .     |
    +-----------+-----------+-----------+
      ↓                               ↓
    +---+---+---+---+---+---+---+---+---+
    | . | . | . | . | . | . | . | . | . |
    +---+---+---+---+---+---+---+---+---+

    For a more detailed explanation, refer to this page: `<https://entropymine.com/imageworsener/matching/>`.

    The formula for calculating values we can use during desampling is simple:

    * width: clip.width * (target_width - 1) / (clip.width - 1)
    * height: clip.height * (target_height - 1) / (clip.height - 1)

    Example usage:

    .. code-block:: python

        >>> from vodesfunc import DescaleTarget
        >>> ...
        >>> native_res = get_match_centers_scaling(src, 1280, 720)
        >>> rescaled = DescaleTarget(kernel=Catrom, upscaler=Waifu2x, downscaler=Hermite(linear=True), **native_res)

    The output is meant to be passed to `vodesfunc.DescaleTarget` as keyword arguments,
    but it may also apply to other functions that require similar parameters.

    :param clip:            The clip to base the calculations on.
    :param target_width:    Target width for the descale. This should probably be equal to the base width.
                            If not provided, this value is calculated using the `target_height`.
                            Default: None.
    :param target_height:   Target height for the descale. This should probably be equal to the base height.
                            If not provided, this value is calculated using the `target_width`.
                            Default: 720.

    :return:                A dictionary with the keys, {width, height, base_width, base_height},
                            which can be passed directly to `vodesfunc.DescaleTarget` or similar functions.
    """

    if target_width is None and target_height is None:
        raise CustomValueError("Either `target_width` or `target_height` must be provided.", get_match_centers_scaling)

    check_variable_resolution(clip, get_match_centers_scaling)

    if target_height is None:
        target_height = get_h(target_width, clip, 1)

        if not float(target_height).is_integer():
            raise CustomValueError("`target_height` must be an integer.", get_match_centers_scaling)

    elif target_width is None:
        target_width = get_w(target_height, clip, 1)

        if not float(target_width).is_integer():
            raise CustomValueError("`target_width` must be an integer.", get_match_centers_scaling)

    width = clip.width * (target_width - 1) / (clip.width - 1)
    height = clip.height * (target_height - 1) / (clip.height - 1)

    return KwargsT(width=width, height=height, base_width=target_width, base_height=target_height)
