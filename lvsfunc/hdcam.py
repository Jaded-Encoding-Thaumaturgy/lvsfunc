from warnings import warn

from vsaa import Nnedi3
from vsdehalo import base_dehalo_mask
from vsdeinterlace import vinverse
from vsexprtools import ExprOp, expr_func
from vskernels import Bilinear, Catrom, Gaussian, Kernel, KernelT, Lanczos, Scaler, ScalerT
from vsmasktools import Kirsch, MagDirection, retinex
from vsrgtools import BlurMatrix, RemoveGrainMode, limit_filter
from vstools import ConvMode, CustomValueError, FunctionUtil, plane, vs

__all__: list[str] = [
    "hdcam_dering"
]


warn(
    "lvsfunc.hdcam: These are all experimental functions! "
    "Please report any issues you find in the #lvsfunc channel in the IEW discord!"
)


def hdcam_dering(
    clip: vs.VideoNode,
    kernel: KernelT = Lanczos(taps=5),
    upscaler: ScalerT = Nnedi3
) -> vs.VideoNode:
    """
    Experimental deringing function for HDCAM material.

    It's not uncommon for HDCAM productions to suffer from immense ringing introduced during resampling.
    This function does a faux-descale pass to gather information to use for deringing.

    Originally written by setsugennoao for Hayate no Gotoku S1.

    :param clip:        Clip to process.
    :param kernel:      Kernel used for descaling.
                        Defaults to Lanczos 5-tap.
    :param upscaler:    Primary scaler used for re-upscaling. This should ideally not be too sharp.
                        Defaults to Nnedi3.

    :return:            Deringed clip.
    """
    func = FunctionUtil(clip, hdcam_dering, 0, (vs.YUV, vs.GRAY), 16)

    kernel = Kernel.ensure_obj(kernel, func.func)
    upscaler = Scaler.ensure_obj(upscaler, func.func)

    if (clip.width, clip.height) != (1920, 1080):
        raise CustomValueError("You must pass a 1920x1080 clip!", func.func, (clip.width, clip.height))

    clip_y = plane(func.work_clip, 0)

    descaled_y = kernel.descale(clip_y, 1440, clip.height)
    ret_y = retinex(descaled_y)

    kirsch = Kirsch(MagDirection.E | MagDirection.W).edgemask(ret_y)

    ring0 = expr_func(kirsch, 'x 2 * 65535 >= x 0 ?')
    ring1 = expr_func(kirsch, 'x 2 * 65535 >= 0 x ?')
    ring2 = ring0.resize.Bilinear(clip.width, clip.height)

    ring = RemoveGrainMode.BOB_TOP_CLOSE(RemoveGrainMode.BOB_BOTTOM_INTER(ring1))
    ring = ring.std.Transpose()

    ring = RemoveGrainMode.SMART_RGCL(ring)
    ring = ring.std.Transpose()

    ring = expr_func([
        ring, kirsch.std.Maximum().std.Maximum().std.Maximum()
    ], 'y 2 * 65535 >= x 0 ?').std.Maximum()

    nag0 = vinverse(clip_y, 6.0, 255, 0.25, ConvMode.HORIZONTAL)
    nag1 = vinverse(clip_y, 5.0, 255, 0.2, ConvMode.HORIZONTAL)
    nag = nag0.std.MaskedMerge(nag1, ring)

    gauss = BlurMatrix.gauss(0.35)
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

    deringed = limit_filter(nag, nag1, clip_y)
    deringed = nag2.std.MaskedMerge(nag2, Bilinear.scale(ring, clip.width, clip.height))

    return func.return_clip(deringed)


# TODO: Chroma reconstruction presets. HDCAM chroma tends to get really
#       screwed up because of the 422/420 => 311 => 422/420 (=> 420) conversion.

# TODO: descale wrapper to handle the horizontal upscale from HDCAM
#       *and* perform a vertical descale to the original native res if possible.


# List of HDCAM productions, kept for no reason other than for people to grab sources to test these funcs on.
hdcam_productions: list[str] = [
    "Hayate no Gotoku",
    "Zettai Karen Children (presumed)",
    "One Piece",
    "Heartcatch! Precure",
    "Joshiraku (presumed)",
    "Kyousougiga (presumed)",
]
