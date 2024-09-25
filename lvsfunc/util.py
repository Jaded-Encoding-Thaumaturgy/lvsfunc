import colorsys
import random
import re
from typing import Any

from vstools import (CustomIndexError, CustomValueError, FrameRangesN,
                     FuncExceptT, KwargsT, check_variable_resolution, core,
                     fallback, get_h, get_w, vs)

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
                            Setting this higher than 315 may result in the clip colors looping back towards red
                            and is not recommended for visually distinct colors.
                            If the `amount` of clips is higher than `max_hue`, expect there to be identical
                            or visually similar colored clips returned.
                            Default: 300.
    :param rand:            Randomizes order of the returned list. Default: True.
    :param seed:            Seed for random number generator. Allows for consistent randomized order
                            of the resulting clips if specified. Default: None.
    :param kwargs:          Additional keyword arguments passed to :py:func:`vapoursynth.core.std.BlankClip`.

    :return:                List of uniquely colored clips in sequential or random order.

    :raises CustomIndexError:   If `amount` is less than 2.
    :raises CustomValueError:   If `max_hue` is not between 0 and 360.
    """

    if amount < 2:
        raise CustomIndexError("`amount` must be at least 2!", colored_clips)
    if not (0 < max_hue <= 360):
        raise CustomValueError("`max_hue` must be greater than 0 and less than 360 degrees!", colored_clips)

    blank_clip_args: dict[str, Any] = dict(keep=1) | kwargs

    hues = [i * max_hue / (amount - 1) for i in range(amount - 1)] + [max_hue]

    hls_color_list = [colorsys.hls_to_rgb(h / 360, 0.5, 1) for h in hues]
    rgb_color_list = [[int(f * 255) for f in color] for color in hls_color_list]

    if rand:
        shuffle = random.shuffle if seed is None else random.Random(seed).shuffle
        shuffle(rgb_color_list)

    return [core.std.BlankClip(color=color, **blank_clip_args) for color in rgb_color_list]


def convert_rfs(rfs_string: str) -> FrameRangesN:
    """
    Convert `ReplaceFramesSimple`-styled ranges to `replace_ranges`-styled ranges.

    This function accepts RFS ranges as a string, consistent with RFS handling.
    The input string is validated before processing.

    Performance may decrease with a larger number of ranges.

    Supports both '[x y]' and 'x' frame numbering styles.
    Returns an empty list if no valid frames are found.

    :param rfs_string:          A string representing frame ranges in ReplaceFramesSimple format.

    :return:                    A FrameRangesN list containing frame ranges compatible with `replace_ranges`.
                                Returns an empty list if no valid frames are found.

    :raises CustomValueError:   If the input string contains invalid characters.
    """

    rfs_string = str(rfs_string).strip()

    if not rfs_string:
        return []

    valid_chars = set('0123456789[] ')
    illegal_chars = set(rfs_string) - valid_chars

    if illegal_chars:
        reason = ', '.join(f"{c}:{rfs_string.index(c)}" for c in sorted(illegal_chars, key=rfs_string.index))
        raise CustomValueError('Invalid characters found in input string!', convert_rfs, reason)

    return [
        int(match[2]) if match[2] else (int(match[0]), int(match[1]))
        for match in re.findall(r'\[(\d+)\s+(\d+)\]|(\d+)', rfs_string)
    ]


def get_match_centers_scaling(
    clip: vs.VideoNode,
    target_width: int | None = None,
    target_height: int | None = 720,
    func_except: FuncExceptT | None = None
) -> KwargsT:
    """
    Convenience function to calculate the native resolution for sources that were upsampled
    using the "match centers" model as opposed to the more common "match edges" models.

    While match edges will align the edges of the outermost pixels in the target image,
    match centers will instead align the *centers* of the outermost pixels.

    Here's a visual example for a 3x1 image upsampled to 7x1:

        * Match edges:

    +-------------+-------------+-------------+
    |      ·      |      ·      |      ·      |
    +-------------+-------------+-------------+
    ↓                                         ↓
    +-----+-----+-----+-----+-----+-----+-----+
    |  ·  |  ·  |  ·  |  ·  |  ·  |  ·  |  ·  |
    +-----+-----+-----+-----+-----+-----+-----+

        * Match centers:

    +-----------------+-----------------+-----------------+
    |        ·        |        ·        |        ·        |
    +-----------------+-----------------+-----------------+
             ↓                                   ↓
          +-----+-----+-----+-----+-----+-----+-----+
          |  ·  |  ·  |  ·  |  ·  |  ·  |  ·  |  ·  |
          +-----+-----+-----+-----+-----+-----+-----+

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
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                A dictionary with the keys, {width, height, base_width, base_height},
                            which can be passed directly to `vodesfunc.DescaleTarget` or similar functions.
    """

    func = fallback(func_except, get_match_centers_scaling)

    if target_width is None and target_height is None:
        raise CustomValueError("Either `target_width` or `target_height` must be a positive integer.", func)

    for target, name in [(target_width, 'width'), (target_height, 'height')]:
        if target is not None and (not isinstance(target, int) or target <= 0):
            raise CustomValueError(f"`target_{name}` must be a positive integer or None.", func)

    check_variable_resolution(clip, func)

    if target_height is None:
        target_height = get_h(target_width, clip, 1)
    elif target_width is None:
        target_width = get_w(target_height, clip, 1)

    width = clip.width * (target_width - 1) / (clip.width - 1)
    height = clip.height * (target_height - 1) / (clip.height - 1)

    return KwargsT(width=width, height=height, base_width=target_width, base_height=target_height)
