from __future__ import annotations

import math
from functools import partial
from typing import Any, Callable, Dict, List, cast
import warnings

import vapoursynth as vs
from vskernels import Bicubic, BicubicSharp, Catrom, Kernel, Spline36, Transfer, VSFunction, get_kernel, get_matrix, get_prop
import vsscale
from vsutil import depth, get_depth, get_w, get_y, iterate, join, plane

from .exceptions import CompareSameKernelError
from .types import CURVES, CreditMask, CustomScaler, Resolution, ScaleAttempt
from .util import (
    check_variable, check_variable_format, check_variable_resolution, get_coefs, get_matrix_curve, quick_resample,
    scale_thresh
)

try:
    from cytoolz import functoolz
except ModuleNotFoundError:
    try:
        from toolz import functoolz  # type: ignore
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Cannot find functoolz: Please install toolz or cytoolz")

core = vs.core


__all__ = [
    'comparative_descale',
    'comparative_restore',
    'descale_detail_mask',
    'descale',
    'mixed_rescale',
    'reupscale',
    # Deprecated
    'ssim_downsample',
    'gamma2linear',
    'linear2gamma'
]


def _transpose_shift(n: int, f: vs.VideoFrame, clip: vs.VideoNode,
                     kernel: Kernel, caller: str) -> vs.VideoNode:
    h = f.height
    w = f.width
    clip = kernel.scale(clip, w, h*2, (0.5, 0))
    return core.std.Transpose(clip)


def _perform_descale(resolution: Resolution, clip: vs.VideoNode,
                     kernel: Kernel) -> ScaleAttempt:
    descaled = kernel.descale(clip, resolution.width, resolution.height) \
        .std.SetFrameProp('descaleResolution', intval=resolution.height)
    rescaled = kernel.scale(descaled, clip.width, clip.height)
    diff = core.akarin.Expr([rescaled, clip], 'x y - abs').std.PlaneStats()
    return ScaleAttempt(descaled, rescaled, resolution, diff)


def _select_descale(n: int, f: vs.VideoFrame | List[vs.VideoFrame],
                    threshold: float, clip: vs.VideoNode,
                    clips_by_resolution: Dict[int, ScaleAttempt]
                    ) -> vs.VideoNode:
    if type(f) is vs.VideoFrame:
        f = [f]
    f = cast(List[vs.VideoFrame], f)
    best_res = max(f, key=lambda frame:
                   math.log(clip.height - get_prop(frame, "descaleResolution", int), 2)  # type:ignore[no-any-return]
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
              kernel: Kernel | str = Bicubic(b=0, c=1/2),
              **kwargs: Any) -> vs.VideoNode:
    """
    Quick 'n easy wrapper to re-upscale a clip descaled with descale using znedi3.

    Function is curried to allow parameter tuning when passing to :py:func:`lvsfunc.scale.descale`

    Original function written by `Vardë <https://github.com/Ichunjo>`_, modified by LightArrowsEXE.

    Dependencies:

    * `znedi3 <https://github.com/sekrit-twc/znedi3>`_

    :param clip:        Clip to process.
    :param width:       Upscale width. If None, determine from `height` assuming 16:9 aspect ratio (Default: None).
    :param height:      Upscale height (Default: 1080).
    :param kernel:      py:class:`vskernels.Kernel` object used for downscaling the super-sampled clip.
                        This can also be the string name of the kernel
                        (Default: py:class:`vskernels.Bicubic(b=0, c=1/2)`).
    :param kwargs:      Arguments passed to znedi3 (Default: nsize=4, nns=4, qual=2, pscrn=2).

    :return:            Reupscaled clip.
    """
    width = width or get_w(height)

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    # Doubling and downscale to given "h"
    znargs: Dict[str, Any] = dict(nsize=4, nns=4, qual=2, pscrn=2)
    znargs |= kwargs

    upsc = quick_resample(clip, partial(core.znedi3.nnedi3, field=0, dh=True, **znargs))
    upsc = core.std.FrameEval(upsc, partial(_transpose_shift, clip=upsc,
                                            kernel=kernel,
                                            caller="reupscale"),
                              prop_src=upsc)
    upsc = quick_resample(upsc, partial(core.znedi3.nnedi3, field=0, dh=True, **znargs))
    return kernel.scale(upsc, width=height, height=width, shift=(0.5, 0)) \
        .std.Transpose()


@functoolz.curry
def descale_detail_mask(clip: vs.VideoNode, rescaled_clip: vs.VideoNode,
                        threshold: float = 0.05) -> vs.VideoNode:
    """
    Generate a detail mask given a clip and a clip rescaled with the same kernel.

    Function is curried to allow parameter tuning when passing to :py:func:`lvsfunc.scale.descale`

    :param clip:           Original clip.
    :param rescaled_clip:  Clip downscaled and reupscaled using the same kernel.
    :param threshold:      Binarization threshold for mask (Default: 0.05).

    :return:               Mask of lost detail.
    """
    check_variable_resolution(clip, "descale_detail_mask")
    check_variable_resolution(rescaled_clip, "descale_detail_mask")

    mask = core.akarin.Expr([get_y(clip), get_y(rescaled_clip)], 'x y - abs') \
        .std.Binarize(threshold)
    mask = iterate(mask, core.std.Maximum, 4)
    return iterate(mask, core.std.Inflate, 2).std.Limiter()


def descale(clip: vs.VideoNode,
            upscaler:
            Callable[[vs.VideoNode, int, int], vs.VideoNode] | None = reupscale,
            width: int | List[int] | None = None,
            height: int | List[int] = 720,
            kernel: Kernel | str = Bicubic(b=0, c=1/2),
            threshold: float = 0.0,
            mask: CreditMask | vs.VideoNode | None
            = descale_detail_mask, src_left: float = 0.0, src_top: float = 0.0,
            show_mask: bool = False) -> vs.VideoNode:
    """
    Unified descaling function.

    Includes support for handling fractional resolutions (experimental),
    multiple resolutions, detail masking, and conditional scaling.

    If you want to descale to a fractional resolution,
    set src_left and src_top and round up the target height.

    If the source has multiple native resolutions, specify ``height``
    as a list.

    If you want to conditionally descale, specify a non-zero threshold.

    Dependencies:

    * `VapourSynth-descale <https://github.com/Irrational-Encoding-Wizardry/VapourSynth-descale>`_
    * `znedi3 <https://github.com/sekrit-twc/znedi3>`_

    :param clip:        Clip to descale.
    :param upscaler:        Callable function with signature upscaler(clip, width, height)
                            -> vs.VideoNode to be used for reupscaling.
                            Must be capable of handling variable res clips
                            for multiple heights and conditional scaling.

                            If a single height is given and upscaler is None,
                            a constant resolution GRAY clip will be returned instead.

                            Note that if upscaler is None, no upscaling will be performed
                            and neither detail masking nor proper fractional descaling can be performed.
                            (Default: :py:func:`lvsfunc.scale.reupscale`)
    :param width:           Width(s) to descale to (if None, auto-calculated).
    :param height:          Height(s) to descale to. List indicates multiple resolutions,
                            the function will determine the best. (Default: 720)
    :param kernel:          py:class:`vskernels.Kernel` object used for the descaling.
                            This can also be the string name of the kernel (Default: py:class:`vskernels.Catrom`).
    :param threshold:       Error threshold for conditional descaling (Default: 0.0, always descale).
    :param mask:            Function or mask clip used to mask detail. If ``None``, no masking.
                            Function must accept a clip and a reupscaled clip and return a mask.
                            (Default: :py:func:`lvsfunc.scale.descale_detail_mask`)
    :param src_left:        Horizontal shifting for fractional resolutions (Default: 0.0).
    :param src_top:         Vertical shifting for fractional resolutions (Default: 0.0).
    :param show_mask:       Return detail mask.

    :return:                Descaled and re-upscaled clip with float bitdepth.

    :raises ValueError:     Asymmetric number of heights and widths are specified.
    :raises RuntimeError:   Variable clip gets returned.
    """
    assert check_variable(clip, "descale")

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    if type(height) is int:
        height = [height]

    height = cast(List[int], height)

    if type(width) is int:
        width = [width]
    elif width is None:
        width = [get_w(h, aspect_ratio=clip.width/clip.height) for h in height]

    width = cast(List[int], width)

    if len(width) != len(height):
        raise ValueError("descale: Asymmetric number of heights and widths specified!")

    resolutions = [Resolution(*r) for r in zip(width, height)]

    clip = depth(clip, 32)
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
        raise RuntimeError("descale: 'Upscaler cannot return variable-format clips!'")

    if mask:
        clip_y = clip_y.resize.Point(format=upscaled.format.id)
        rescaled = kernel.scale(descaled, clip.width, clip.height,
                                (src_left, src_top))
        rescaled = rescaled.resize.Point(format=clip.format.id)  # type:ignore[union-attr]

        dmask = mask if isinstance(mask, vs.VideoNode) else mask(clip_y, rescaled)

        if upscaler is None:
            dmask = core.resize.Spline36(dmask, upscaled.width, upscaled.height)
            clip_y = core.resize.Spline36(clip_y, upscaled.width, upscaled.height)

        if show_mask:
            return dmask

        upscaled = core.std.MaskedMerge(upscaled, clip_y, dmask)

    upscaled = depth(upscaled, get_depth(clip))

    if clip.format.num_planes == 1 or upscaler is None:  # type:ignore[union-attr]
        return upscaled
    return join([upscaled, plane(clip, 1), plane(clip, 2)])


def ssim_downsample(clip: vs.VideoNode, width: int | None = None, height: int = 720,
                    smooth: float | VSFunction = ((3 ** 2 - 1) / 12) ** 0.5,
                    kernel: Kernel | str = Bicubic(b=0, c=1/2), gamma: bool = False,
                    curve: Transfer | None = None,
                    sigmoid: bool = False, epsilon: float = 1e-6) -> vs.VideoNode:
    """
    SSIM_downsample rewrite taken from a Vardë gist.

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

    `Original gist <https://gist.github.com/Ichunjo/16ab1f893588aafcb096c1f35a0cfb15>`_

    :param clip:        Clip to process.
    :param width:       Output width. If None, autocalculates using height.
    :param height:      Output height (Default: 720).
    :param smooth:      Image smoothening method.
                        If you pass an int, it specifies the "radius" of the internally-used boxfilter,
                        i.e. the window has a size of (2*smooth+1)x(2*smooth+1).
                        If you pass a float, it specifies the "sigma" of core.tcanny.TCanny,
                        i.e. the standard deviation of gaussian blur.
                        If you pass a function, it acts as a general smoother.
                        Default uses a gaussian blur.
    :param kernel:      py:class:`vskernels.Kernel` object used for certain scaling operations.
                        This can also be the string name of the kernel
                        (Default: py:class:`vskernels.Bicubic(0, 0.5)`).
    :param curve:       Gamma mapping. Will auto-determine based on the input props or resolution.
                        Can be forced with for example `curve=vs.TransferCharacteristics.TRANSFER_BT709`.
    :param gamma:       Perform a gamma conversion prior to scaling and after scaling.
                        This function MUST be set to `True` for `sigmoid` and `epsilon` to function.
    :param sigmoid:     When True, applies a sigmoidal curve after the power-like curve
                        (or before when converting from linear to gamma-corrected).
                        This helps reduce the dark halo artefacts found around sharp edges
                        caused by resizing in linear luminance.
                        This parameter only works if `gamma=True`.
    :param epsilon:     Machine epsilon. This parameter only works if `gamma=True`.

    :return:            Downsampled clip.
    """

    warnings.warn('lvsfunc.ssim_downsample: deprecated in favor of vsscale.SSIM!', DeprecationWarning)

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    return vsscale.ssim_downsample(
        clip, width, height, smooth, kernel, gamma if curve is None else curve, sigmoid
    )


def gamma2linear(clip: vs.VideoNode, curve: CURVES, gcor: float = 1.0,
                 sigmoid: bool = False, thr: float = 0.5, cont: float = 6.5,
                 epsilon: float = 1e-6) -> vs.VideoNode:
    """Convert gamma to linear."""

    warnings.warn('lvsfunc.gamma2linear: deprecated in favor of vsscale.gamma2linear!', DeprecationWarning)

    return vsscale.gamma2linear(clip, curve, gcor, sigmoid, thr, cont, epsilon)


def linear2gamma(clip: vs.VideoNode, curve: Transfer, gcor: float = 1.0,
                 sigmoid: bool = False, thr: float = 0.5, cont: float = 6.5,
                 ) -> vs.VideoNode:
    """Convert linear to gamma."""

    warnings.warn('lvsfunc.linear2gamma: deprecated in favor of vsscale.linear2gamma!', DeprecationWarning)

    return vsscale.linear2gamma(clip, curve, gcor, sigmoid, thr, cont)


def comparative_descale(clip: vs.VideoNode, width: int | None = None, height: int = 720,
                        kernel: Kernel | str | None = None, thr: float = 5e-8) -> vs.VideoNode:
    """
    Descale to SharpBicubic and an additional kernel, compare them, then pick one or the other.

    The output clip has props that can be used to frameeval specific kernels by the user.

    :param clip:                        Clip to process.
    :param width:                       Width to descale to (if None, auto-calculated).
    :param height:                      Descale height.
    :param kernel:                      py:class:`vskernels.Kernel` object to compare
                                        py:class:`vskernels.BicubicSharp` to.
                                        This can also be the string name of the kernel
                                        (Default: py:class:`vskernels.Spline36` if ``kernel=None``).
    :param thr:                         Threshold for which kernel to pick.

    :return:                            Descaled clip.

    :raises CompareSameKernelError:     py:class:`vskernels.BicubicSharp` gets passed to ``kernel``.
    """
    def _compare(n: int, f: List[vs.VideoFrame], sharp: vs.VideoNode, other: vs.VideoNode) -> vs.VideoNode:
        sharp_diff = get_prop(f[0], 'PlaneStatsDiff', float)
        other_diff = get_prop(f[1], 'PlaneStatsDiff', float)

        return sharp if other_diff - thr > sharp_diff else other

    check_variable_resolution(clip, "comparative_descale")

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    bsharp = BicubicSharp()
    kernel = kernel or Spline36()

    if isinstance(kernel, Bicubic) and bsharp.b == kernel.b and bsharp.c == kernel.c:
        raise CompareSameKernelError("comparative_descale", kernel=bsharp)

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


def comparative_restore(clip: vs.VideoNode, width: int | None = None, height: int = 720,
                        kernel: Kernel | str | None = None) -> vs.VideoNode:
    """
    Companion function for comparative_descale to reupscale the clip for descale detail masking.

    :param clip:                        Clip to process.
    :param width:                       Width to upscale to (if None, auto-calculated).
    :param height:                      Upscale height.
    :param kernel:                      py:class:`vskernels.Kernel` object to compare
                                        py:class:`vskernels.BicubicSharp` to.
                                        This can also be the string name of the kernel
                                        (Default: py:class:`vskernels.Spline36` if ``kernel=None``).

    :return:                            Reupscaled clip.

    :raises CompareSameKernelError:     py:class:`vskernels.BicubicSharp` gets passed to ``kernel``.
    """
    check_variable_resolution(clip, "comparative_restore")

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    bsharp = BicubicSharp()
    kernel = kernel or Spline36()

    if isinstance(kernel, Bicubic) and bsharp.b == kernel.b and bsharp.c == kernel.c:
        raise CompareSameKernelError("comparative_descale", kernel=bsharp)

    if width is None:
        width = get_w(height, aspect_ratio=clip.width/clip.height)

    def _compare(n: int, f: vs.VideoFrame, sharp_up: vs.VideoNode, other_up: vs.VideoNode) -> vs.VideoNode:
        return sharp_up if get_prop(f, 'scaler', bytes) == b'BicubicSharp' else other_up

    # TODO: just read prop and automatically figure out scaler TBH
    sharp_up = bsharp.scale(clip, width, height)
    other_up = kernel.scale(clip, width, height)

    return core.std.FrameEval(sharp_up, partial(_compare, sharp_up=sharp_up, other_up=other_up), clip)


def mixed_rescale(clip: vs.VideoNode, width: None | int = None, height: int = 720,
                  kernel: Kernel | str = Bicubic(b=0, c=1/2),
                  downscaler: CustomScaler | Kernel | str = ssim_downsample,
                  credit_mask: CreditMask | vs.VideoNode | None = descale_detail_mask, mask_thr: float = 0.05,
                  mix_strength: float = 0.25, show_mask: bool | int = False,
                  nnedi3_args: Dict[str, Any] = {}, eedi3_args: Dict[str, Any] = {}) -> vs.VideoNode:
    """
    Rewrite of InsaneAA to make it easier to use and maintain.

    Descales and downscales the given clip and merges them together with a set strength.

    This can be useful for dealing with a source that you can't accurately descale,
    but you still want to force it. Not recommended to use it on everything, however.

    A string can be passed instead of a Kernel object if you want to use that.
    This gives you access to every kernel object in :py:mod:`vskernels`.
    For more information on what every kernel does, please refer to their documentation.

    This is still a work in progress at the time of writing. Please use with care.

    :param clip:            Clip to process.
    :param width:           Upscale width. If None, determine from `height` (Default: None).
    :param height:          Upscale height (Default: 720).
    :param kernel:          py:class:`vskernels.Kernel` object used for the descaling.
                            This can also be the string name of the kernel
                            (Default: py:class:`vskernels.Bicubic(b=0, c=1/2)`).
    :param downscaler:      Kernel or custom scaler used to downscale the clip.
                            This can also be the string name of the kernel
                            (Default: py:func:`lvsfunc.scale.ssim_downsample`).
    :param credit_mask:     Function or mask clip used to mask detail. If ``None``, no masking.
                            Function must accept a clip and a reupscaled clip and return a mask.
                            (Default: :py:func:`lvsfunc.scale.descale_detail_mask`).
    :param mask_thr:        Binarization threshold for :py:func:`lvsfunc.scale.descale_detail_mask` (Default: 0.05).
    :param mix_strength:    Merging strength between the descaled and downscaled clip.
                            Stronger values will make the line-art look closer to the downscaled clip.
                            This can get pretty dangerous very quickly if you use a sharp ``downscaler``!
    :param show_mask:       Return the ``credit_mask``. If set to `2`, it will return the line-art mask instead.
    :param nnedi3_args:     Additional args to pass to nnedi3.
    :param eedi3_args:      Additional args to pass to eedi3.

    :return:                Rescaled clip with a downscaled clip merged with it and credits masked.

    :raises ValueError:     ``mask_thr`` is not between 0.0–1.0.
    """
    assert check_variable(clip, "mixed_rescale")

    if not 0 <= mask_thr <= 1:
        raise ValueError(f"mixed_rescale: '`mask_thr` must be between 0.0 and 1.0! Not {mask_thr}!'")

    # Default settings set to match insaneAA as closely as reasonably possible
    nnargs: Dict[str, Any] = dict(nsize=0, nns=4, qual=2, pscrn=1)
    nnargs |= nnedi3_args

    eediargs: Dict[str, Any] = dict(alpha=0.2, beta=0.25, gamma=1000, nrad=2, mdis=20)
    eediargs |= eedi3_args

    width = width or get_w(height, clip.width/clip.height, only_even=False)

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    if isinstance(downscaler, str):
        downscaler = get_kernel(downscaler)()

    bits = get_depth(clip)
    clip_y = get_y(clip)

    line_mask = clip_y.std.Prewitt(scale=2).std.Maximum().std.Limiter()

    descaled = kernel.descale(clip_y, width, height)
    upscaled = kernel.scale(descaled, clip.width, clip.height)

    if isinstance(downscaler, Kernel):
        downscaled = downscaler.scale(clip_y, width, height)
    else:
        downscaled = depth(downscaler(clip_y, width, height), bits)
        downscaler = Catrom()

    merged = core.akarin.Expr([descaled, downscaled], f'x {mix_strength} * y 1 {mix_strength} - * +')

    if isinstance(credit_mask, vs.VideoNode):
        detail_mask = depth(credit_mask, get_depth(clip))
    elif not credit_mask:
        detail_mask = clip_y.std.BlankClip(length=1) * clip.num_frames
    else:
        detail_mask = descale_detail_mask(clip_y, upscaled, threshold=scale_thresh(mask_thr, clip))
        detail_mask = iterate(detail_mask, core.std.Inflate, 2)
        detail_mask = iterate(detail_mask, core.std.Maximum, 2).std.Limiter()

    if show_mask == 2:
        return line_mask
    elif show_mask:
        return detail_mask

    sclip = merged.std.Transpose().znedi3.nnedi3(0, True, **nnargs) \
        .std.Transpose().znedi3.nnedi3(0, True, **nnargs)
    double = merged.std.Transpose().eedi3m.EEDI3(0, True, **eediargs) \
        .std.Transpose().eedi3m.EEDI3(0, True, sclip=sclip, **eediargs)
    rescaled = ssim_downsample(downscaler.shift(double, shift=(.5, .5)), height=clip.height)
    rescaled = depth(rescaled, bits)

    masked = core.std.MaskedMerge(rescaled, clip_y, detail_mask)
    masked = core.std.MaskedMerge(clip_y, masked, line_mask)

    if clip.format.num_planes == 1:
        return masked
    return core.std.ShufflePlanes([masked, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


# TODO: Write a function that checks every possible combination of B and C in bicubic
#       and returns a list of the results. Possibly return all the frames in order of
#       smallest difference to biggest. Not reliable, but maybe useful as starting point.


# TODO: Write "multi_descale", a function that allows you to descale a frame twice,
#       like for example when the CGI in a show is handled in a different resolution
#       than the drawn animation.
