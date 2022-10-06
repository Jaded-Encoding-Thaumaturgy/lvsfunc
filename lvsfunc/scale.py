from __future__ import annotations

from typing import Any, Callable

from vskernels import Bicubic, Catrom, Kernel
from vsscale import CreditMaskT, descale_detail_mask, ssim_downsample
from vstools import core, depth, get_depth, get_w, get_y, iterate, vs

from .util import check_variable, scale_thresh

__all__ = [
    'mixed_rescale'
]


def mixed_rescale(clip: vs.VideoNode, width: None | int = None, height: int = 720,
                  kernel: Kernel | str = Bicubic(b=0, c=1/2),
                  downscaler: Callable[[vs.VideoNode, int, int], vs.VideoNode] | Kernel | str = ssim_downsample,
                  credit_mask: CreditMaskT | vs.VideoNode | None = descale_detail_mask, mask_thr: float = 0.05,
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

    if not isinstance(kernel, Kernel):
        kernel = Kernel.from_param(kernel)()

    if not isinstance(downscaler, Kernel):
        downscaler = Kernel.from_param(downscaler)()

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
