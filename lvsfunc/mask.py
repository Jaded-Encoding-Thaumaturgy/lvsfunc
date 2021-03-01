"""
    Wrappers and masks for denoising.
"""
import math
from functools import partial
from typing import Callable, Optional, Union

import vapoursynth as vs
from vsutil import depth, get_depth, get_y, iterate, scale_value

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


@functoolz.curry
def halo_mask(clip: vs.VideoNode, rad: int = 2, sigma: float = 1.0,
              thmi: int = 80, thma: int = 128,
              thlimi: int = 50, thlima: int = 100,
              edgemasking: Callable[[vs.VideoNode, float], vs.VideoNode]
              = lambda clip, sigma: core.std.Prewitt(clip, scale=sigma)) -> vs.VideoNode:
    """
    A halo mask to catch basic haloing, inspired by the mask from FineDehalo.
    Most was copied from there, but some key adjustments were made to center it specifically around masking.

    rx and ry are now combined into rad and expects an integer.
    Float made sense for FineDehalo since it uses DeHalo_alpha for dehaloing,
    but the masks themselves use rounded rx/ry values, so there's no reason to bother with floats here.

    :param clip:            Input clip
    :param rad:             Radius for the mask
    :param scale:           Multiply all pixels by scale before outputting. Sigma if `edgemask` with a sigma is passed
    :param thmi:            Minimum threshold for sharp edges; keep only the sharpest edges
    :param thma:            Maximum threshold for sharp edges; keep only the sharpest edges
    :param thlimi:          Minimum limiting threshold; includes more edges than previously, but ignores simple details
    :param thlima:          Maximum limiting threshold; includes more edges than previously, but ignores simple details
    :param edgemasking:     Callable function with signature edgemask(clip, scale/sigma)

    :return:                Halo mask
    """
    peak = (1 << get_depth(clip)) - 1
    smax = _scale(255, peak)

    thmi = _scale(thmi, peak)
    thma = _scale(thma, peak)
    thlimi = _scale(thlimi, peak)
    thlima = _scale(thlima, peak)

    matrix = [1, 2, 1, 2, 4, 2, 1, 2, 1]

    edgemask = edgemasking(get_y(clip), sigma)

    # Preserve just the strongest edges
    strong = core.std.Expr(edgemask, expr=f"x {thmi} - {thma-thmi} / {smax} *")
    # Expand to pick up additional halos
    expand = iterate(strong, core.std.Maximum, rad)

    # Having too many intersecting lines will oversmooth the mask. We get rid of those here.
    light = core.std.Expr(edgemask, expr=f"x {thlimi} - {thma-thmi} / {smax} *")
    shrink = iterate(light, core.std.Maximum, rad)
    shrink = core.std.Binarize(shrink, scale_value(.25, 32, get_depth(clip)))
    shrink = iterate(shrink, core.std.Minimum, rad)
    shrink = iterate(shrink, partial(core.std.Convolution, matrix=matrix), 2)

    # Making sure the lines are actually excluded
    excl = core.std.Expr([strong, shrink], expr="x y max")
    # Subtract and boosting to make sure we get the max pixel values for dehaloing
    mask = core.std.Expr([expand, excl], expr="x y - 2 *")
    # Additional blurring to amplify the mask
    mask = core.std.Convolution(mask, matrix)
    return core.std.Expr(mask, expr="x 2 *")


# Helper function taken and modified from havsfunc to reduce dependencies
def _scale(value: int, peak: int) -> int:
    x = value * peak / 255
    return math.floor(x + 0.5) if x > 0 else math.ceil(x - 0.5)
