import colorsys
import random
from typing import Any

from jetpytools import CustomIndexError, CustomValueError
from vstools import core, vs

__all__ = [
    "colored_clips",
]


def colored_clips(
    amount: int,
    max_hue: int = 300,
    rand: bool = True,
    seed: Any | None = None,
    **kwargs: Any,
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
        raise CustomValueError(
            "`max_hue` must be greater than 0 and less than 360 degrees!", colored_clips
        )

    blank_clip_args: dict[str, Any] = dict(keep=1) | kwargs

    hues = [i * max_hue / (amount - 1) for i in range(amount - 1)] + [max_hue]

    hls_color_list = [colorsys.hls_to_rgb(h / 360, 0.5, 1) for h in hues]
    rgb_color_list = [[int(f * 255) for f in color] for color in hls_color_list]

    if rand:
        shuffle = random.shuffle if seed is None else random.Random(seed).shuffle
        shuffle(rgb_color_list)

    return [
        core.std.BlankClip(color=color, **blank_clip_args) for color in rgb_color_list
    ]
