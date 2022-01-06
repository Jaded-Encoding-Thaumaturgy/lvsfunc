"""
    Helper functions for module functions and wrapper.
    Some of these may also be useful for regular scripting or other modules.
"""
from typing import (Any, Callable, List, Optional, Sequence, Tuple, Type,
                    TypeVar, Union)

import vapoursynth as vs
from vsutil import depth, get_subsampling

from .types import Range, Coefs

core = vs.core


def quick_resample(clip: vs.VideoNode,
                   function: Callable[[vs.VideoNode], vs.VideoNode]
                   ) -> vs.VideoNode:
    """
    A function to quickly resample to 32/16/8 bit and back to the original depth in a one-liner.
    Useful for filters that only work in 16 bit or lower when you're working in float.

    :param clip:      Input clip
    :param function:  Filter to run after resampling (accepts and returns clip)

    :return:          Filtered clip in original depth
    """
    if clip.format is None:
        raise ValueError("quick_resample: 'Variable-format clips not supported'")

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
    Gets FrameProp ``prop`` from frame ``frame`` with expected type ``t``
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

    if not isinstance(prop, t):
        raise ValueError(f"get_prop: 'Key {key} did not contain expected type: Expected {t} got {type(prop)}'")

    return prop


def normalize_ranges(clip: vs.VideoNode, ranges: Union[Range, List[Range]]) -> List[Tuple[int, int]]:
    """
    Normalize ``Range``\\(s) to a list of inclusive positive integer ranges.

    :param clip:   Reference clip used for length.
    :param ranges: Single ``Range`` or list of ``Range``\\s.

    :return:       List of inclusive positive ranges.
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
                   ranges: Union[Range, List[Range], None]) -> vs.VideoNode:
    """
    A replacement for ReplaceFramesSimple that uses ints and tuples rather than a string.
    Frame ranges are inclusive.

    Examples with clips ``black`` and ``white`` of equal length:

        * ``replace_ranges(black, white, [(0, 1)])``: replace frames 0 and 1 with ``white``
        * ``replace_ranges(black, white, [(None, None)])``: replace the entire clip with ``white``
        * ``replace_ranges(black, white, [(0, None)])``: same as previous
        * ``replace_ranges(black, white, [(200, None)])``: replace 200 until the end with ``white``
        * ``replace_ranges(black, white, [(200, -1)])``: replace 200 until the end with ``white``,
          leaving 1 frame of ``black``

    :param clip_a:     Original clip
    :param clip_b:     Replacement clip
    :param ranges:     Ranges to replace clip_a (original clip) with clip_b (replacement clip).

                       Integer values in the list indicate single frames,

                       Tuple values indicate inclusive ranges.

                       Negative integer values will be wrapped around based on clip_b's length.

                       None values are context dependent:

                           * None provided as sole value to ranges: no-op
                           * Single None value in list: Last frame in clip_b
                           * None as first value of tuple: 0
                           * None as second value of tuple: Last frame in clip_b

    :return:           Clip with ranges from clip_a replaced with clip_b
    """
    if ranges is None:
        return clip_a

    out = clip_a

    nranges = normalize_ranges(clip_b, ranges)

    for start, end in nranges:
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


def scale_peak(value: float, peak: float) -> float:
    """
    Full-range scale function that scales a value from [0, 255] to [0, peak]
    """
    return value * peak / 255


def force_mod(x: float, mod: int = 4) -> int:
    """
    Force output to fit a specific MOD.
    Minimum returned value will always be mod².
    """
    return mod ** 2 if x < mod ** 2 else int(x / mod + 0.5) * mod


def clamp_values(x: float, max_val: float, min_val: float) -> float:
    """
    Forcibly clamps the given value x to a max and/or min value.
    """
    return min_val if x < min_val else max_val if x > max_val else x


def padder(clip: vs.VideoNode,
           left: int = 32, right: int = 32,
           top: int = 32, bottom: int = 32) -> vs.VideoNode:
    """
    Pads out the pixels on the side by the given amount of pixels.
    For a 4:2:0 clip, the output must be an even resolution.

    :param clip:        Input clip
    :param left:        Padding added to the left side of the clip
    :param right:       Padding added to the right side of the clip
    :param top:         Padding added to the top side of the clip
    :param bottom:      Padding added to the bottom side of the clip

    :return:            Padded clip
    """
    if clip.format is None:
        raise ValueError("padder: 'Variable-format clips not supported'")

    width = clip.width+left+right
    height = clip.height+top+bottom

    if get_subsampling(clip) == '420' and ((width % 2 != 0) or (height % 2 != 0)):
        raise ValueError("padder: 'Values must result in an even resolution when passing a YUV420 clip!'")

    scaled = core.resize.Point(clip, width, height,
                               src_top=-1*top, src_left=-1*left,
                               src_width=width, src_height=height)
    return core.fb.FillBorders(scaled, left=left, right=right, top=top, bottom=bottom)


def get_coefs(curve: vs.TransferCharacteristics) -> Coefs:
    srgb = Coefs(0.04045, 12.92, 0.055, 2.4)
    bt709 = Coefs(0.08145, 4.5, 0.0993, 2.22222)
    smpte240m = Coefs(0.0912, 4.0, 0.1115, 2.22222)
    bt2020 = Coefs(0.08145, 4.5, 0.0993, 2.22222)

    gamma_linear_map = {
        vs.TransferCharacteristics.TRANSFER_IEC_61966_2_1: srgb,
        vs.TransferCharacteristics.TRANSFER_BT709: bt709,
        vs.TransferCharacteristics.TRANSFER_BT601: bt709,
        vs.TransferCharacteristics.TRANSFER_ST240_M: smpte240m,
        vs.TransferCharacteristics.TRANSFER_BT2020_10: bt2020,
        vs.TransferCharacteristics.TRANSFER_BT2020_12: bt2020
    }

    return gamma_linear_map[curve]
