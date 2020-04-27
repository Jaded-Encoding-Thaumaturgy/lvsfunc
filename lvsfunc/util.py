"""
    Helper functions for the main functions in the script.
    Can be used as-is if you so please.
"""
from functools import partial
from typing import Callable

import vapoursynth as vs

core = vs.core


def one_plane(clip: vs.VideoNode) -> bool:
    """
        Returns True if there's only one plane (lol)
    """
    return clip.format.num_planes == 1


def resampler(clip: vs.VideoNode, bitdepth: int) -> vs.VideoNode:
    """
        Really just a barebones version of fvsfunc's Depth to remove a common dependency.
        All credit for the original script goes to Frechdachs.
    """
    clip_cf = clip.format.color_family
    dst_st = dst_st = vs.INTEGER if bitdepth < 32 else vs.FLOAT
    src_sw = clip.format.subsampling_w
    src_sh = clip.format.subsampling_h

    if clip.format.bits_per_sample == bitdepth:
        return clip

    dither_type = 'error_diffusion' if bitdepth > clip.format.bits_per_sample else 'none'
    form = core.register_format(clip_cf, dst_st, bitdepth, src_sw, src_sh)
    return core.resize.Point(clip, format=form.id, dither_type=dither_type)


def get_scale_filter(kernel: str, **kwargs):
    """
        kagefunc's get_descale_filter, but for the internal resizers.
    """
    kernel = kernel.lower()
    filters = {
        "bilinear": lambda **kwargs: core.resize.Bilinear,
        "spline16": lambda **kwargs: core.resize.Spline16,
        "spline36": lambda **kwargs: core.resize.Spline36,
        "spline64": lambda **kwargs: core.resize.Spline64,
        "bicubic": lambda b, c, **kwargs: partial(core.resize.Bicubic, filter_param_a=b, filter_param_b=c),
        "lanczos": lambda taps, **kwargs: partial(core.resize.Lanczos, filter_param_a=taps),
    }
    return filters[kernel](**kwargs)


def quick_resample(clip: vs.VideoNode, function: Callable, **func_args) -> vs.VideoNode:
    # Note: Busted for now. Will fix in a jiffy. :teehee:
    """
        A function to quickly resample to 16 bit and back to the original depth.
        Useful for filters that only work in 16 bit or lower when you're working in float.
    """
    down = resampler(clip, 16)
    filtered = function(down, *func_args)
    return resampler(filtered, clip.format.bits_per_sample)


def pick_repair(clip: vs.VideoNode):
    """
        Returns rgvs.Repair if the clip is 16 bit or lower, else rgsf.Repair.
        This is done because rgvs doesn't work with float, but rgsf does for whatever reason.
    """
    return core.rgvs.Repair if clip.format.bits_per_sample < 32 else core.rgsf.Repair


def create_dmask(clip: vs.VideoNode, luma_scaling: float = 8) -> vs.VideoNode:
    """
        A wrapper to create a luma mask for denoising, debanding, etc.
    """
    return core.adg.Mask(clip.std.PlaneStats(), luma_scaling)
