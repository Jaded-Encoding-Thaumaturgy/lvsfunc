"""
    Wrappers and masks for denoising.
"""
from functools import partial
from typing import Optional

import vapoursynth as vs
from vsutil import depth, get_depth, get_y, scale_value

from . import util

try:
    from cytoolz import functoolz
except ModuleNotFoundError:
    try:
        from toolz import functoolz  # type: ignore
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Cannot find functoolz: Please install toolz or cytoolz")

core = vs.core


@functoolz.curry
def adaptive_mask(clip: vs.VideoNode, luma_scaling: float = 8.0) -> vs.VideoNode:
    """
    A wrapper to create a luma mask for denoising and/or debanding.

    Function is curried to allow parameter tuning when passing to denoisers
    that allow you to pass your own mask.

    Dependencies: adaptivegrain

    :param clip:         Input clip
    :param luma_scaling: Luma scaling factor (Default: 8.0)

    :return:             Luma mask
    """
    return core.adg.Mask(clip.std.PlaneStats(), luma_scaling)


@functoolz.curry
def detail_mask(clip: vs.VideoNode, sigma: Optional[float] = None,
                rad: int = 3, radc: int = 2,
                brz_a: float = 0.005, brz_b: float = 0.005) -> vs.VideoNode:
    """
    A wrapper for creating a detail mask to be used during denoising and/or debanding.
    The detail mask is created using debandshit's rangemask,
    and is then merged with Prewitt to catch lines it may have missed.

    Function is curried to allow parameter tuning when passing to denoisers
    that allow you to pass your own mask.

    Dependencies: VapourSynth-Bilateral (optional: sigma), debandshit

    :param clip:        Input clip
    :param sigma:       Sigma for Bilateral for pre-blurring (Default: False)
    :param rad:         The luma equivalent of gradfun3's "mask" parameter
    :param radc:        The chroma equivalent of gradfun3's "mask" parameter
    :param brz_a:       Binarizing for the detail mask (Default: 0.05)
    :param brz_b:       Binarizing for the edge mask (Default: 0.05)

    :return:            Detail mask
    """
    try:
        from debandshit import rangemask
    except ModuleNotFoundError:
        raise ModuleNotFoundError("detail_mask: missing dependency 'debandshit'")

    if clip.format is None:
        raise ValueError("detail_mask: 'Variable-format clips not supported'")

    # Handling correct value scaling if there's a assumed depth mismatch
    # To the me in the future, long after civilisation has fallen, make sure to check 3.10's pattern matching.
    if get_depth(clip) != 32:
        if isinstance(brz_a, float):
            brz_a = scale_value(brz_a, 32, get_depth(clip))
        if isinstance(brz_b, float):
            brz_b = scale_value(brz_b, 32, get_depth(clip))
    else:
        if isinstance(brz_a, int):
            brz_a = scale_value(brz_a, get_depth(clip), 32)
        if isinstance(brz_b, int):
            brz_b = scale_value(brz_b, get_depth(clip), 32)

    blur = (util.quick_resample(clip, partial(core.bilateral.Gaussian, sigma=sigma))
            if sigma else clip)

    mask_a = rangemask(get_y(blur), rad=rad, radc=radc)
    mask_a = depth(mask_a, clip.format.bits_per_sample)
    mask_a = core.std.Binarize(mask_a, brz_a)

    mask_b = core.std.Prewitt(get_y(blur))
    mask_b = core.std.Binarize(mask_b, brz_b)

    mask = core.std.Expr([mask_a, mask_b], 'x y max')
    mask = util.pick_removegrain(mask)(mask, 22)
    return util.pick_removegrain(mask)(mask, 11)
