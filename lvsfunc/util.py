"""
    Helper functions for the main functions in the script.
"""
from typing import Any, Callable, List, Optional, Sequence, Tuple, Type, TypeVar, Union, cast

import vapoursynth as vs
from vsutil import depth

from .types import Range

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
    if clip.format is None:
        raise ValueError("quick_resample: 'Variable-format clips not supported'")
    try:
        down = depth(clip, 16)
        filtered = function(down)
    except:  # noqa: E722
        down = depth(clip, 8)
        filtered = function(down)
    return depth(filtered, clip.format.bits_per_sample)


def pick_repair(clip: vs.VideoNode) -> Callable[..., vs.VideoNode]:
    """
    Returns rgvs.Repair if the clip is 16 bit or lower, else rgsf.Repair.
    This is done because rgvs doesn't work with float, but rgsf does for whatever reason.

    Dependencies: rgsf

    :param clip: Input clip

    :return:     Appropriate repair function for input clip's depth
    """
    if clip.format is None:
        raise ValueError("pick_repair: 'Variable-format clips not supported'")
    return core.rgvs.Repair if clip.format.bits_per_sample < 32 else core.rgsf.Repair


def pick_removegrain(clip: vs.VideoNode) -> Callable[..., vs.VideoNode]:
    """
    Returns rgvs.RemoveGrain if the clip is 16 bit or lower, else rgsf.RemoveGrain.
    This is done because rgvs doesn't work with float, but rgsf does for whatever reason.

    Dependencies:
    * RGSF

    :param clip: Input clip

    :return:     Appropriate RemoveGrain function for input clip's depth
    """
    if clip.format is None:
        raise ValueError("pick_removegrain: 'Variable-format clips not supported'")
    return core.rgvs.RemoveGrain if clip.format.bits_per_sample < 32 else core.rgsf.RemoveGrain


VideoProp = Union[
    int, Sequence[int],
    float, Sequence[float],
    str, Sequence[str],
    vs.VideoNode, Sequence[vs.VideoNode],
    vs.VideoFrame, Sequence[vs.VideoFrame],
    Callable[..., Any], Sequence[Callable[..., Any]]
]

T = TypeVar("T", bound=VideoProp)


def get_prop(frame: vs.VideoFrame, key: str, t: Type[T]) -> T:
    """
    Gets gets FrameProp ``prop`` from frame ``frame`` with expected type ``t``
    to satisfy the type checker.

    :param frame:   Frame containing props
    :param key:     Prop to get
    :param t:       Type of prop

    :return:        frame.prop[key]
    """
    try:
        prop = frame.props[key]
    except KeyError:
        raise KeyError(f"get_prop: 'Key {key} not present in props'")
    real_type = type(prop)
    if real_type is not t:
        raise ValueError(f"get_prop: 'Key {key} did not contain expected type: Expected {t} got {real_type}'")

    return cast(T, prop)


def replace_ranges(clip_a: vs.VideoNode,
                   clip_b: vs.VideoNode,
                   ranges: Union[Range, List[Range]]) -> vs.VideoNode:
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
    if not isinstance(ranges, list):
        ranges = [ranges]

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


def scale_thresh(thresh: float, clip: vs.VideoNode, assume: Optional[int] = None) -> float:
    """
    Scale binarization thresholds from float to int.

    :param thresh: Threshold [0, 1]. If greater than 1, assumed to be in native clip range
    :param clip:   Clip to scale to
    :param assume: Assume input is this depth when given input >1. If ``None``\\, assume ``clip``\\'s format.
                   (Default: None)

    :return:       Threshold scaled to [0, 2^clip.depth - 1] (if vs.INTEGER)
    """
    if clip.format is None:
        raise ValueError("scale_thresh: 'Variable-format clips not supported.'")
    if thresh < 0:
        raise ValueError("scale_thresh: 'Thresholds must be positive.'")
    if thresh > 1:
        return thresh if not assume \
            else round(thresh/((1 << assume) - 1) * ((1 << clip.format.bits_per_sample) - 1))
    return thresh if clip.format.sample_type == vs.FLOAT or thresh > 1 \
        else round(thresh * ((1 << clip.format.bits_per_sample) - 1))
