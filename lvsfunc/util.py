"""
    Helper functions for the main functions in the script.
"""
from typing import Callable, cast

import vapoursynth as vs
from vsutil import depth

core = vs.core


def quick_resample(clip: vs.VideoNode,
                   function: Callable[[vs.VideoNode], vs.VideoNode]
                   ) -> vs.VideoNode:
    """
    A function to quickly resample to 16/8 bit and back to the original depth.
    Useful for filters that only work in 16 bit or lower when you're working in float.

    :param clip:      Input clip
    :param function:  Filter to run after resampling (accepts and returns clip)

    :return:          Filtered clip in original depth
    """
    try:
        down = depth(clip, 16)
        filtered = function(down)
    except:  # noqa: E722
        down = depth(clip, 8)
        filtered = function(down)
    return depth(filtered, clip.format.bits_per_sample)


# TODO: Merge pick_repair and pick_removegrain?
def pick_repair(clip: vs.VideoNode) -> Callable[..., vs.VideoNode]:
    """
    Returns rgvs.Repair if the clip is 16 bit or lower, else rgsf.Repair.
    This is done because rgvs doesn't work with float, but rgsf does for whatever reason.

    Dependencies: rgsf

    :param clip: Input clip

    :return:     Appropriate repair function for input clip's depth
    """
    return core.rgvs.Repair if clip.format.bits_per_sample < 32 else core.rgsf.Repair  # type: ignore


def pick_removegrain(clip: vs.VideoNode) -> Callable[..., vs.VideoNode]:
    """
    Returns rgvs.RemoveGrain if the clip is 16 bit or lower, else rgsf.RemoveGrain.
    This is done because rgvs doesn't work with float, but rgsf does for whatever reason.

    Dependencies: rgsf

    :param clip: Input clip

    :return:     Appropriate RemoveGrain function for input clip's depth
    """
    return core.rgvs.RemoveGrain if clip.format.bits_per_sample < 32 else core.rgsf.RemoveGrain  # type: ignore
