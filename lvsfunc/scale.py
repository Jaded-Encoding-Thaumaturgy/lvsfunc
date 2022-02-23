"""
    (De)scaling and conversion functions and wrappers.
"""
from __future__ import annotations

import math
from functools import partial
from typing import Any, Callable, Dict, List, Literal, NamedTuple, cast

import vapoursynth as vs
from vsutil import (depth, disallow_variable_format,
                    disallow_variable_resolution, get_depth, get_w, get_y,
                    iterate, join, plane)

from . import kernels
from .kernels import Bicubic, BicubicSharp, Catrom, Kernel, Spline36
from .types import VSFunction
from .util import get_coefs, get_prop, quick_resample

try:
    from cytoolz import functoolz
except ModuleNotFoundError:
    try:
        from toolz import functoolz  # type: ignore
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Cannot find functoolz: Please install toolz or cytoolz")

core = vs.core


class Resolution(NamedTuple):
    """ Tuple representing a resolution. """

    width: int
    """ Width. """

    height: int
    """ Height. """


class ScaleAttempt(NamedTuple):
    """ Tuple representing a descale attempt. """

    descaled: vs.VideoNode
    """ Descaled frame in native resolution. """

    rescaled: vs.VideoNode
    """ Descaled frame reupscaled with the same kernel. """

    resolution: Resolution
    """ The native resolution. """

    diff: vs.VideoNode
    """ The subtractive difference between the original and descaled frame. """


def _transpose_shift(n: int, f: vs.VideoFrame, clip: vs.VideoNode,
                     kernel: kernels.Kernel, caller: str) -> vs.VideoNode:
    h = f.height
    w = f.width
    clip = kernel.scale(clip, w, h*2, (0.5, 0))
    return core.std.Transpose(clip)


def _perform_descale(resolution: Resolution, clip: vs.VideoNode,
                     kernel: kernels.Kernel) -> ScaleAttempt:
    descaled = kernel.descale(clip, resolution.width, resolution.height) \
        .std.SetFrameProp('descaleResolution', intval=resolution.height)
    rescaled = kernel.scale(descaled, clip.width, clip.height)
    diff = core.std.Expr([rescaled, clip], 'x y - abs').std.PlaneStats()
    return ScaleAttempt(descaled, rescaled, resolution, diff)


def _select_descale(n: int, f: vs.VideoFrame | List[vs.VideoFrame],
                    threshold: float, clip: vs.VideoNode,
                    clips_by_resolution: Dict[int, ScaleAttempt]
                    ) -> vs.VideoNode:
    if type(f) is vs.VideoFrame:
        f = [f]
    f = cast(List[vs.VideoFrame], f)
    best_res = max(f, key=lambda frame:
                   math.log(clip.height - get_prop(frame, "descaleResolution", int), 2)
                   * round(1 / max(get_prop(frame, "PlaneStatsAverage", float), 1e-12))
                   ** 0.2)

    best_attempt = clips_by_resolution[get_prop(best_res, "descaleResolution", int)]
    if threshold == 0:
        return best_attempt.descaled
    if get_prop(best_res, "PlaneStatsAverage", float) > threshold:
        return clip
    return best_attempt.descaled


@functoolz.curry
def reupscale(clip: vs.VideoNode,
              width: int | None = None, height: int = 1080,
              kernel: kernels.Kernel = kernels.Bicubic(b=0, c=1/2),
              **kwargs: Any) -> vs.VideoNode:
    """
    A quick 'n easy wrapper used to re-upscale a clip descaled with descale using znedi3.

    Function is curried to allow parameter tuning when passing to :py:func:`lvsfunc.scale.descale`

    Stolen from Varde with some adjustments made.

    Dependencies:

    * znedi3

    :param clip:         Input clip
    :param width:        Upscale width. If None, determine from `height` assuming 16:9 aspect ratio (Default: None)
    :param height:       Upscale height (Default: 1080)
    :param kernel:       Kernel used to downscale the doubled clip (see :py:class:`lvsfunc.kernels.Kernel`,
                         Default: kernels.Bicubic(b=0, c=1/2))
    :param kwargs:       Arguments passed to znedi3 (Default: nsize=4, nns=4, qual=2, pscrn=2)

    :return:             Reupscaled clip
    """
    width = width or get_w(height)

    # Doubling and downscale to given "h"
    znargs = dict(nsize=4, nns=4, qual=2, pscrn=2)
    znargs.update(kwargs)

    upsc = quick_resample(clip, partial(core.znedi3.nnedi3, field=0, dh=True, **znargs))
    upsc = core.std.FrameEval(upsc, partial(_transpose_shift, clip=upsc,
                                            kernel=kernel,
                                            caller="reupscale"),
                              prop_src=upsc)
    upsc = quick_resample(upsc, partial(core.znedi3.nnedi3, field=0, dh=True, **znargs))
    return kernel.scale(upsc, width=height, height=width, shift=(0.5, 0)) \
        .std.Transpose()


@functoolz.curry
@disallow_variable_format
@disallow_variable_resolution
def descale_detail_mask(clip: vs.VideoNode, rescaled_clip: vs.VideoNode,
                        threshold: float = 0.05) -> vs.VideoNode:
    """
    Generate a detail mask given a clip and a clip rescaled with the same
    kernel.

    Function is curried to allow parameter tuning when passing to :py:func:`lvsfunc.scale.descale`

    :param clip:           Original clip
    :param rescaled_clip:  Clip downscaled and reupscaled using the same kernel
    :param threshold:      Binarization threshold for mask (Default: 0.05)

    :return:               Mask of lost detail
    """
    mask = core.std.Expr([get_y(clip), get_y(rescaled_clip)], 'x y - abs') \
        .std.Binarize(threshold)
    mask = iterate(mask, core.std.Maximum, 4)
    return iterate(mask, core.std.Inflate, 2)


def descale(clip: vs.VideoNode,
            upscaler:
            Callable[[vs.VideoNode, int, int], vs.VideoNode] | None = reupscale,
            width: int | List[int] | None = None,
            height: int | List[int] = 720,
            kernel: kernels.Kernel = kernels.Bicubic(b=0, c=1/2),
            threshold: float = 0.0,
            mask: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] | vs.VideoNode | None
            = descale_detail_mask, src_left: float = 0.0, src_top: float = 0.0,
            show_mask: bool = False) -> vs.VideoNode:
    """
    A unified descaling function.
    Includes support for handling fractional resolutions (experimental),
    multiple resolutions, detail masking, and conditional scaling.

    If you want to descale to a fractional resolution,
    set src_left and src_top and round up the target height.

    If the source has multiple native resolutions, specify ``height``
    as a list.

    If you want to conditionally descale, specify a non-zero threshold.

    Dependencies:

    * vapoursynth-descale
    * znedi3

    :param clip:                    Clip to descale
    :param upscaler:                Callable function with signature upscaler(clip, width, height)
                                    -> vs.VideoNode to be used for reupscaling.
                                    Must be capable of handling variable res clips
                                    for multiple heights and conditional scaling.
                                    If a single height is given and upscaler is None,
                                    a constant resolution GRAY clip will be returned instead.
                                    Note that if upscaler is None, no upscaling will be performed
                                    and neither detail masking nor proper fractional descaling can be preformed.
                                    (Default: :py:func:`lvsfunc.scale.reupscale`)
    :param width:                   Width(s) to descale to (if None, auto-calculated)
    :param height:                  Height(s) to descale to. List indicates multiple resolutions,
                                    the function will determine the best. (Default: 720)
    :param kernel:                  Kernel used to descale (see :py:class:`lvsfunc.kernels.Kernel`,
                                    (Default: kernels.Bicubic(b=0, c=1/2))
    :param threshold:               Error threshold for conditional descaling (Default: 0.0, always descale)
    :param mask:                    Function or mask clip used to mask detail. If ``None``, no masking.
                                    Function must accept a clip and a reupscaled clip and return a mask.
                                    (Default: :py:func:`lvsfunc.scale.descale_detail_mask`)
    :param src_left:                Horizontal shifting for fractional resolutions (Default: 0.0)
    :param src_top:                 Vertical shifting for fractional resolutions (Default: 0.0)
    :param show_mask:               Return detail mask

    :return:                       Descaled and re-upscaled clip with float bitdepth
    """
    assert clip.format

    if type(height) is int:
        height = [height]

    height = cast(List[int], height)

    if type(width) is int:
        width = [width]
    elif width is None:
        width = [get_w(h, aspect_ratio=clip.width/clip.height) for h in height]

    width = cast(List[int], width)

    if len(width) != len(height):
        raise ValueError("descale: Asymmetric number of heights and widths specified")

    resolutions = [Resolution(*r) for r in zip(width, height)]

    clip = depth(clip, 32)
    assert clip.format is not None  # clip was modified by depth, but that wont make it variable
    clip_y = get_y(clip) \
        .std.SetFrameProp('descaleResolution', intval=clip.height)

    variable_res_clip = core.std.Splice([
        core.std.BlankClip(clip_y, length=len(clip) - 1),
        core.std.BlankClip(clip_y, length=1, width=clip.width + 1)
    ], mismatch=True)

    descale_partial = partial(_perform_descale, clip=clip_y, kernel=kernel)
    clips_by_resolution = {c.resolution.height:
                           c for c in map(descale_partial, resolutions)}

    props = [c.diff for c in clips_by_resolution.values()]
    select_partial = partial(_select_descale, threshold=threshold,
                             clip=clip_y,
                             clips_by_resolution=clips_by_resolution)

    descaled = core.std.FrameEval(variable_res_clip, select_partial,
                                  prop_src=props)

    if src_left != 0 or src_top != 0:
        descaled = core.resize.Bicubic(descaled, src_left=src_left,
                                       src_top=src_top)

    if upscaler is None:
        upscaled = descaled
        if len(height) == 1:
            upscaled = core.resize.Point(upscaled, width[0], height[0])
        else:
            return upscaled
    else:
        upscaled = upscaler(descaled, clip.width, clip.height)

    if src_left != 0 or src_top != 0:
        upscaled = core.resize.Bicubic(descaled, src_left=-src_left,
                                       src_top=-src_top)

    if upscaled.format is None:
        raise RuntimeError("descale: 'Upscaler cannot return variable-format clips'")

    if mask:
        clip_y = clip_y.resize.Point(format=upscaled.format.id)
        rescaled = kernel.scale(descaled, clip.width, clip.height,
                                (src_left, src_top))
        rescaled = rescaled.resize.Point(format=clip.format.id)

        dmask = mask if isinstance(mask, vs.VideoNode) else mask(clip_y, rescaled)

        if upscaler is None:
            dmask = core.resize.Spline36(dmask, upscaled.width, upscaled.height)
            clip_y = core.resize.Spline36(clip_y, upscaled.width, upscaled.height)

        if show_mask:
            return dmask

        upscaled = core.std.MaskedMerge(upscaled, clip_y, dmask)

    upscaled = depth(upscaled, get_depth(clip))

    if clip.format.num_planes == 1 or upscaler is None:
        return upscaled
    return join([upscaled, plane(clip, 1), plane(clip, 2)])


CURVES = Literal[
    vs.TransferCharacteristics.TRANSFER_IEC_61966_2_1,
    vs.TransferCharacteristics.TRANSFER_BT709,
    vs.TransferCharacteristics.TRANSFER_BT601,
    vs.TransferCharacteristics.TRANSFER_ST240_M,
    vs.TransferCharacteristics.TRANSFER_BT2020_10,
    vs.TransferCharacteristics.TRANSFER_BT2020_12,
]


@disallow_variable_format
@disallow_variable_resolution
def ssim_downsample(clip: vs.VideoNode, width: int | None = None, height: int = 720,
                    smooth: float | VSFunction = ((3 ** 2 - 1) / 12) ** 0.5,
                    kernel: Kernel = Catrom(), gamma: bool = False,
                    curve: CURVES = vs.TransferCharacteristics.TRANSFER_BT709,
                    sigmoid: bool = False, epsilon: float = 1e-6) -> vs.VideoNode:
    """
    muvsfunc.ssim_downsample rewrite taken from a Vardë gist.
    Unlike muvsfunc's implementation, this function also works in float and does not use nnedi3_resample.
    Most of the documentation is taken from muvsfunc.

    SSIM downsampler is an image downscaling technique that aims to optimize
    for the perceptual quality of the downscaled results.
    Image downscaling is considered as an optimization problem
    where the difference between the input and output images is measured
    using famous Structural SIMilarity (SSIM) index.
    The solution is derived in closed-form, which leads to the simple, efficient implementation.
    The downscaled images retain perceptually important features and details,
    resulting in an accurate and spatio-temporally consistent representation of the high resolution input.

    Original gist: https://gist.github.com/Ichunjo/16ab1f893588aafcb096c1f35a0cfb15

    :param clip:        Input clip
    :param width:       Output width. If None, autocalculates using height
    :param height:      Output height (default: 720)
    :param smooth:      Image smoothening method.
                        If you pass an int, it specifies the "radius" of the internel used boxfilter,
                        i.e. the window has a size of (2*smooth+1)x(2*smooth+1).
                        If you pass a float, it specifies the "sigma" of core.tcanny.TCanny,
                        i.e. the standard deviation of gaussian blur.
                        If you pass a function, it acts as a general smoother.
                        Default uses a gaussian blur.
    :param curve:       Gamma mapping
    :param sigmoid:     When True, applies a sigmoidal curve after the power-like curve
                        (or before when converting from linear to gamma-corrected).
                        This helps reduce the dark halo artefacts found around sharp edges
                        caused by resizing in linear luminance.
    :param epsilon:     Machine epsilon

    :return: Downsampled clip
    """
    if isinstance(smooth, int):
        filter_func = partial(core.std.BoxBlur, hradius=smooth, vradius=smooth)
    elif isinstance(smooth, float):
        filter_func = partial(core.tcanny.TCanny, sigma=smooth, mode=-1)
    else:
        filter_func = smooth  # type: ignore[assignment]

    if width is None:
        width = get_w(height, aspect_ratio=clip.width/clip.height)

    clip = depth(clip, 32)

    if gamma:
        clip = gamma2linear(clip, curve, sigmoid=sigmoid, epsilon=epsilon)

    l1 = kernel.scale(clip, width, height)
    l2 = kernel.scale(clip.std.Expr('x dup *'), width, height)

    m = filter_func(l1)

    sl_plus_m_square = filter_func(l1.std.Expr('x dup *'))
    sh_plus_m_square = filter_func(l2)
    m_square = m.std.Expr('x dup *')
    r = core.std.Expr([sl_plus_m_square, sh_plus_m_square, m_square], f'x z - {epsilon} < 0 y z - x z - / sqrt ?')
    t = filter_func(core.std.Expr([r, m], 'x y *'))
    m = filter_func(m)
    r = filter_func(r)
    d = core.std.Expr([m, r, l1, t], 'x y z * + a -')

    if gamma:
        d = linear2gamma(d, curve, sigmoid=sigmoid)

    return d


@disallow_variable_format
@disallow_variable_resolution
def gamma2linear(clip: vs.VideoNode, curve: CURVES, gcor: float = 1.0,
                 sigmoid: bool = False, thr: float = 0.5, cont: float = 6.5,
                 epsilon: float = 1e-6) -> vs.VideoNode:
    assert clip.format

    if get_depth(clip) != 32 and clip.format.sample_type != vs.FLOAT:
        raise ValueError('Only 32 bits float is allowed')

    c = get_coefs(curve)

    expr = f'x {c.k0} <= x {c.phi} / x {c.alpha} + 1 {c.alpha} + / {c.gamma} pow ? {gcor} pow'
    if sigmoid:
        x0 = f'1 1 {cont} {thr} * exp + /'
        x1 = f'1 1 {cont} {thr} 1 - * exp + /'
        expr = f'{thr} 1 {expr} {x1} {x0} - * {x0} + {epsilon} max / 1 - {epsilon} max log {cont} / -'

    expr = f'{expr} 0.0 max 1.0 min'

    return core.std.Expr(clip, expr).std.SetFrameProps(_Transfer=8)


@disallow_variable_format
@disallow_variable_resolution
def linear2gamma(clip: vs.VideoNode, curve: CURVES, gcor: float = 1.0,
                 sigmoid: bool = False, thr: float = 0.5, cont: float = 6.5,
                 ) -> vs.VideoNode:
    assert clip.format

    if get_depth(clip) != 32 and clip.format.sample_type != vs.FLOAT:
        raise ValueError('Only 32 bits float is allowed')

    c = get_coefs(curve)

    expr = 'x'
    if sigmoid:
        x0 = f'1 1 {cont} {thr} * exp + /'
        x1 = f'1 1 {cont} {thr} 1 - * exp + /'
        expr = f'1 1 {cont} {thr} {expr} - * exp + / {x0} - {x1} {x0} - /'

    expr += f' {gcor} pow'
    expr = f'{expr} {c.k0} {c.phi} / <= {expr} {c.phi} * {expr} 1 {c.gamma} / pow {c.alpha} 1 + * {c.alpha} - ?'
    expr = f'{expr} 0.0 max 1.0 min'

    return core.std.Expr(clip, expr).std.SetFrameProps(_Transfer=curve)


@disallow_variable_format
@disallow_variable_resolution
def comparative_descale(clip: vs.VideoNode, width: int | None = None, height: int = 720,
                        kernel: Kernel | None = None, thr: float = 5e-8) -> vs.VideoNode:
    """
    Easy wrapper to descale to SharpBicubic and an additional kernel,
    compare them, and then pick one or the other.

    The output clip has props that can be used to frameeval specific kernels by the user.

    :param clip:        Input clip
    :param width:       Width to descale to (if None, auto-calculated)
    :param height:      Descale height
    :param kernel:      Kernel to compare BicubicSharp to (Default: Spline36 if None)
    :param thr:         Threshold for which kernel to pick

    :return:            Descaled clip
    """
    def _compare(n: int, f: vs.VideoFrame, sharp: vs.VideoNode, other: vs.VideoNode) -> vs.VideoNode:
        sharp_diff = get_prop(f[0], 'PlaneStatsDiff', float)  # type:ignore[arg-type]
        other_diff = get_prop(f[1], 'PlaneStatsDiff', float)  # type:ignore[arg-type]

        return sharp if other_diff - thr > sharp_diff else other

    bsharp = BicubicSharp()
    kernel = kernel or Spline36()

    if isinstance(kernel, Bicubic) and bsharp.b == kernel.b and bsharp.c == kernel.c:
        raise ValueError("comparative_descale: 'You may not compare BicubicSharp with itself!'")

    if width is None:
        width = get_w(height, aspect_ratio=clip.width/clip.height)

    clip_y = get_y(clip)
    # TODO: Add support for multiple scaler combos. Gotta rethink how `thr` will work tho
    sharp = bsharp.descale(clip_y, width, height)
    sharp_up = bsharp.scale(sharp, clip.width, clip.height)

    # TODO: Fix so you can also pass additional params to object. Breaks currently (not callable)
    other = kernel.descale(clip_y, width, height)
    other_up = kernel.scale(other, clip.width, clip.height)

    # We need a diff between the rescaled clips and the original clip
    sharp_diff = core.std.PlaneStats(sharp_up, clip_y)
    other_diff = core.std.PlaneStats(other_up, clip_y)

    # Extra props for future frame evalling in case it might prove useful (credit masking, for example)
    sharp = sharp.std.SetFrameProp('scaler', data=bsharp.__class__.__name__)
    other = other.std.SetFrameProp('scaler', data=kernel.__class__.__name__)

    return core.std.FrameEval(sharp, partial(_compare, sharp=sharp, other=other), [sharp_diff, other_diff])


@disallow_variable_format
@disallow_variable_resolution
def comparative_restore(clip: vs.VideoNode, width: int | None = None, height: int = 720,
                        kernel: Kernel | None = None) -> vs.VideoNode:
    """
    Companion function to go with comparative_descale
    to reupscale the clip for descale detail masking.

    :param clip:        Input clip
    :param width:       Width to upscale to (if None, auto-calculated)
    :param height:      Upscale height
    :param kernel:      Kernel to compare BicubicSharp to (Default: Spline36 if None)
    """
    bsharp = BicubicSharp()
    kernel = kernel or Spline36()

    if isinstance(kernel, Bicubic) and bsharp.b == kernel.b and bsharp.c == kernel.c:
        raise ValueError("comparative_restore: 'You may not compare BicubicSharp with itself!'")

    if width is None:
        width = get_w(height, aspect_ratio=clip.width/clip.height)

    def _compare(n: int, f: vs.VideoFrame, sharp_up: vs.VideoNode, other_up: vs.VideoNode) -> vs.VideoNode:
        return sharp_up if get_prop(f, 'scaler', bytes) == b'BicubicSharp' else other_up

    # TODO: just read prop and automatically figure out scaler TBH
    sharp_up = bsharp.scale(clip, width, height)
    other_up = kernel.scale(clip, width, height)

    return core.std.FrameEval(sharp_up, partial(_compare, sharp_up=sharp_up, other_up=other_up), clip)


# TODO: Write a function that checks every possible combination of B and C in bicubic
#       and returns a list of the results. Possibly return all the frames in order of
#       smallest difference to biggest. Not reliable, but maybe useful as starting point.


# TODO: Write "multi_descale", a function that allows you to descale a frame twice,
#       like for example when the CGI in a show is handled in a different resolution
#       than the drawn animation.
