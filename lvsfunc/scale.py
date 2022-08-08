from __future__ import annotations

import warnings
from typing import Any, Callable

import vapoursynth as vs
import vsscale
from vskernels import Bicubic, BicubicSharp, Catrom, Kernel, Spline36, Transfer, VSFunction, get_kernel
from vsutil import depth, get_depth, get_w, get_y, iterate

from .util import check_variable, scale_thresh

core = vs.core


__all__ = [
    'mixed_rescale',
    # Deprecated
    'descale',
    'comparative_descale',
    'comparative_restore',
    'descale_detail_mask',
    'ssim_downsample',
    'gamma2linear',
    'linear2gamma'
]


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

    warnings.warn(
        'lvsfunc.descale_detail_mask: deprecated in favor of vsscale.descale_detail_mask!', DeprecationWarning
    )

    return vsscale.descale_detail_mask(clip, rescaled_clip, threshold)


def descale(clip: vs.VideoNode,
            upscaler:
            Callable[[vs.VideoNode, int, int], vs.VideoNode] | None = None,
            width: int | list[int] | None = None,
            height: int | list[int] = 720,
            kernel: Kernel | str = Bicubic(b=0, c=1/2),
            threshold: float = 0.0,
            mask: vsscale.CreditMaskT | vs.VideoNode | None
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

    warnings.warn(
        'lvsfunc.descale_detail_mask: deprecated in favor of vsscale.descale_detail_mask!', DeprecationWarning
    )

    up_func = upscaler and vsscale.GenericScaler(upscaler)

    out = vsscale.descale(
        clip, width, height, kernel, up_func, False if mask is None else mask,
        vsscale.DescaleMode.PlaneDiff(threshold), None, None, (src_top, src_left),
        result=True
    )

    if show_mask and out.mask:
        return out.mask

    assert out.upscaled

    return out.upscaled


def ssim_downsample(clip: vs.VideoNode, width: int | None = None, height: int = 720,
                    smooth: float | VSFunction = ((3 ** 2 - 1) / 12) ** 0.5,
                    kernel: Kernel | str = Bicubic(b=0, c=1/2), gamma: bool = False,
                    curve: Transfer | None = None,
                    sigmoid: bool = False, epsilon: float = 1e-6) -> vs.VideoNode:
    """
    SSIM_downsample rewrite taken from a Vardë gist.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

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


def gamma2linear(clip: vs.VideoNode, curve: Transfer, gcor: float = 1.0,
                 sigmoid: bool = False, thr: float = 0.5, cont: float = 6.5,
                 epsilon: float = 1e-6) -> vs.VideoNode:
    """
    Convert gamma to linear.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    """

    warnings.warn('lvsfunc.gamma2linear: deprecated in favor of vsscale.gamma2linear!', DeprecationWarning)

    return vsscale.gamma2linear(clip, curve, gcor, sigmoid, thr, cont, epsilon)


def linear2gamma(clip: vs.VideoNode, curve: Transfer, gcor: float = 1.0,
                 sigmoid: bool = False, thr: float = 0.5, cont: float = 6.5,
                 ) -> vs.VideoNode:
    """
    Convert linear to gamma.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    """

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

    warnings.warn(
        'lvsfunc.comparative_descale: deprecated in favor of vsscale.descale with mode=DescaleMode.KernelDiff!',
        DeprecationWarning
    )

    return vsscale.descale(
        clip, width, height, [BicubicSharp, kernel or Spline36],
        mask=False, mode=vsscale.DescaleMode.KernelDiff(thr),
        result=True
    ).descaled


def comparative_restore(clip: vs.VideoNode, width: int | None = None, height: int = 720,
                        kernel: Kernel | str | None = None, thr: float = 5e-8) -> vs.VideoNode:
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

    warnings.warn(
        'lvsfunc.comparative_restore: deprecated in favor of vsscale.descale with mode=DescaleMode.KernelDiff!',
        DeprecationWarning
    )

    return vsscale.descale(
        clip, width, height, [BicubicSharp, kernel or Spline36],
        mask=False, mode=vsscale.DescaleMode.KernelDiff(thr),
        result=True
    ).rescaled


def mixed_rescale(clip: vs.VideoNode, width: None | int = None, height: int = 720,
                  kernel: Kernel | str = Bicubic(b=0, c=1/2),
                  downscaler: Callable[[vs.VideoNode, int, int], vs.VideoNode] | Kernel | str = ssim_downsample,
                  credit_mask: vsscale.CreditMaskT | vs.VideoNode | None = descale_detail_mask, mask_thr: float = 0.05,
                  mix_strength: float = 0.25, show_mask: bool | int = False,
                  nnedi3_args: dict[str, Any] = {}, eedi3_args: dict[str, Any] = {}) -> vs.VideoNode:
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
    nnargs: dict[str, Any] = dict(nsize=0, nns=4, qual=2, pscrn=1)
    nnargs |= nnedi3_args

    eediargs: dict[str, Any] = dict(alpha=0.2, beta=0.25, gamma=1000, nrad=2, mdis=20)
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
