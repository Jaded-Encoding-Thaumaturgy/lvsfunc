from typing import Callable

from vsaa import Nnedi3
from vsdehalo import base_dehalo_mask
from vsdeinterlace import vinverse
from vsexprtools import ExprOp, expr_func
from vskernels import (Bilinear, Catrom, Gaussian, Kernel, KernelT, Lanczos,
                       Scaler, ScalerT)
from vsmasktools import Kirsch, MagDirection, retinex
from vsrgtools import BlurMatrix, RemoveGrainMode, limit_filter
from vstools import ConvMode, CustomValueError, FunctionUtil, plane, vs

from .priv import _warn_hdcam

__all__: list[str] = [
    "hdcam_dering"
]


def hdcam_dering(
    clip: vs.VideoNode,
    kernel: KernelT | vs.VideoNode = Lanczos(taps=4),
    upscaler: ScalerT = Nnedi3,
    limiter: bool | Callable[[vs.VideoNode, vs.VideoNode, vs.VideoNode], vs.VideoNode] = True,
    show_mask: bool = False
) -> vs.VideoNode:
    """
    Experimental deringing function for HDCAM material.

    It's not uncommon for HDCAM productions to suffer from immense ringing introduced during resampling.
    This function does a faux-descale pass to gather information to use for deringing.

    Originally written by setsugennoao for Hayate no Gotoku S1.

    :param clip:        Clip to process.
    :param kernel:      Kernel used for descaling. Defaults to Lanczos 4-tap.
                        Optionally, if a VideoNode is passed, it will replace the descaled clip with that.
    :param upscaler:    Primary scaler used for re-upscaling. This should ideally not be too sharp,
                        so you shouldn't use Waifu2x or FSRCNNX with this. Defaults to Nnedi3.
    :param limiter:     Whether to limit the clip or not. If a callable is passed, it will run that instead.
                        The callable must accept a src, a filtered clip, and a ref clip.
                        Defaults to True.
    :param show_mask:   Return the mask. Defaults to False.

    :return:            Deringed clip or the ringing mask if show_mask=True.
    """

    _warn_hdcam()

    func = FunctionUtil(clip, hdcam_dering, 0, (vs.YUV, vs.GRAY), 16)

    if not isinstance(kernel, vs.VideoNode):
        kernel = Kernel.ensure_obj(kernel, func.func)

    upscaler = Scaler.ensure_obj(upscaler, func.func)

    if (clip.width, clip.height) != (1920, 1080):
        raise CustomValueError("You must pass a 1920x1080 clip!", func.func, (clip.width, clip.height))

    clip_y = plane(func.work_clip, 0)

    if isinstance(kernel, vs.VideoNode):
        descaled_y = plane(kernel, 0)
    elif isinstance(kernel, Kernel):
        descaled_y = kernel.descale(clip_y, 1440, clip.height)
    else:
        raise CustomValueError(f"Could not determine how to handle the given kernel, \"{kernel=}\"!", hdcam_dering)

    ret_y = retinex(descaled_y)

    kirsch = Kirsch(MagDirection.E | MagDirection.W).edgemask(ret_y)

    ring0 = expr_func(kirsch, 'x 2 * 65535 >= x 0 ?')
    ring1 = expr_func(kirsch, 'x 2 * 65535 >= 0 x ?')
    ring2 = Bilinear.scale(ring0, clip.width, clip.height)

    ring = RemoveGrainMode.BOB_TOP_CLOSE(RemoveGrainMode.BOB_BOTTOM_INTER(ring1))
    ring = ring.std.Transpose()

    ring = RemoveGrainMode.SMART_RGCL(ring)
    ring = ring.std.Transpose()

    ring = expr_func([
        ring, kirsch.std.Maximum().std.Maximum().std.Maximum()
    ], 'y 2 * 65535 >= x 0 ?').std.Maximum()

    nag0 = vinverse(descaled_y, 6.0, 255, 0.25, ConvMode.HORIZONTAL)
    nag1 = vinverse(descaled_y, 5.0, 255, 0.2, ConvMode.HORIZONTAL)
    nag = nag0.std.MaskedMerge(nag1, ring)

    gauss = BlurMatrix.GAUSS(0.35)
    nag = gauss(nag, 0, ConvMode.HORIZONTAL, passes=2)

    nag1 = upscaler.scale(nag, clip.width, clip.height)
    nag2 = Gaussian(curve=12).scale(nag, clip.width, clip.height)
    nag3 = nag2.std.MaskedMerge(nag1, ring2.std.Maximum())

    fine_mask = ring2.std.Minimum().std.Inflate()

    nag = nag3.std.MaskedMerge(clip_y, fine_mask)
    nag = nag.std.MaskedMerge(nag2, Bilinear.scale(ring, clip.width, clip.height))

    de_mask = ExprOp.ADD(
        base_dehalo_mask(ret_y),
        ring1,
        Catrom.scale(
            expr_func([clip_y, nag], 'x y - abs 120 * 65535 >= 65535 0 ?'),
            ring1.width, ring1.height
        )
    )

    de_mask = Bilinear.scale(de_mask, clip.width, clip.height)
    de_mask = de_mask.std.MaskedMerge(de_mask.std.BlankClip(keep=True), fine_mask)
    de_mask = de_mask.std.Inflate().std.Maximum().std.Deflate()
    de_mask = de_mask.std.Minimum().std.Minimum().std.Maximum().std.Minimum().std.Minimum()
    de_mask = expr_func(de_mask, 'x 1.5 *').std.Maximum().std.Deflate()
    de_mask = de_mask.std.MaskedMerge(de_mask.std.BlankClip(keep=True), fine_mask)

    nag1 = clip_y.std.Merge(nag, 0.5).std.MaskedMerge(nag, de_mask)

    if callable(limiter):
        deringed = limiter(nag, nag1, clip_y)
    elif limiter:
        deringed = limit_filter(nag, nag1, clip_y)
    else:
        deringed = nag

    ring = upscaler.scale(ring, clip.width, clip.height)

    if show_mask:
        return ring

    deringed = deringed.std.MaskedMerge(nag2, ring)

    return func.return_clip(deringed)
