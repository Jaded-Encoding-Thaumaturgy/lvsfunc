from __future__ import annotations

from math import ceil
from typing import Any

from vskernels import Box, Point
from vsscale import ssim_downsample
from vstools import core, depth, fallback, get_depth, get_y, join, plane, scale_value, vs, check_variable


__all__ = [
    'based_aa'
]


def based_aa(clip: vs.VideoNode, shader_file: str = "FSRCNNX_x2_56-16-4-1.glsl",
             rfactor: float = 2.0, tff: bool = True,
             mask_thr: float = 60, show_mask: bool = False,
             lmask: vs.VideoNode | None = None, **eedi3_args: Any) -> vs.VideoNode:
    """
    Based anti-aliaser written by the based `Zastin <https://github.com/kgrabs>`_.

    This function relies on FSRCNNX being very sharp,
    and as such it very much acts like the main "AA" here.

    Original function written by `Zastin <https://github.com/kgrabs>`_, modified by LightArrowsEXE.

    Dependencies:

    * `VapourSynth-EEDI3 <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3>`_
    * `vs-placebo <https://github.com/Lypheo/vs-placebo>`_

    :param clip:            Clip to process.
    :param shader_file:     Path to FSRCNNX shader file.
    :param rfactor:         Image enlargement factor.
    :param tff:             Top-Field-First if true, Bottom-Field-First if false.
    :param mask_thr:        Threshold for the edge mask binarisation.
                            Scaled internally to match bitdepth of clip.
    :param show_mask:       Output mask.
    :param eedi3_args:      Additional args to pass to eedi3.
    :param lmask:           Line mask clip to use for eedi3.

    :return:                AA'd clip or mask clip.

    :raises ValueError:     ``l_mask`` is passed and '`mask_thr` is higher than 255.
    """
    def _eedi3s(clip: vs.VideoNode, mclip: vs.VideoNode | None = None,
                **eedi3_kwargs: Any) -> vs.VideoNode:
        edi_args: dict[str, Any] = {  # Eedi3 args for `eedi3s`
            'field': int(tff), 'alpha': 0.125, 'beta': 0.25, 'gamma': 40,
            'nrad': 2, 'mdis': 20,
            'vcheck': 2, 'vthresh0': 12, 'vthresh1': 24, 'vthresh2': 4
        }
        edi_args |= eedi3_kwargs

        out = core.eedi3m.EEDI3(clip, dh=False, sclip=clip, planes=0, **edi_args)

        if mclip:
            return core.std.Expr([clip, out, mclip], 'z y x ?')
        return out

    def _resize_mclip(mclip: vs.VideoNode,
                      width: int | None = None,
                      height: int | None = None
                      ) -> vs.VideoNode:
        iw, ih = mclip.width, mclip.height
        ow, oh = fallback(width, iw), fallback(height, ih)

        if (ow > iw and ow/iw != ow//iw) or (oh > ih and oh/ih != oh//ih):
            mclip = Point().scale(mclip, iw * ceil(ow / iw), ih * ceil(oh / ih))

        return Box(fulls=1, fulld=1).scale(mclip, ow, oh)

    assert check_variable(clip, "based_aa")

    aaw = (round(clip.width * rfactor) + 1) & ~1
    aah = (round(clip.height * rfactor) + 1) & ~1

    clip_y = get_y(clip)

    if not lmask:
        if mask_thr > 255:
            raise ValueError(f"based_aa: '`mask_thr` must be equal to or lower than 255 (current: {mask_thr})!'")

        mask_thr = scale_value(mask_thr, 8, get_depth(clip))

        lmask = clip_y.std.Prewitt().std.Binarize(mask_thr).std.Maximum().std.BoxBlur(0, 1, 1, 1, 1).std.Limiter()

    mclip_up = _resize_mclip(lmask, aaw, aah)

    if show_mask:
        return lmask

    aa = depth(clip_y, 16).std.Transpose()
    aa = join([aa] * 3).placebo.Shader(shader=shader_file, filter='box', width=aa.width * 2, height=aa.height * 2)
    aa = depth(aa, get_depth(clip_y))
    aa = ssim_downsample(get_y(aa), aah, aaw)
    aa = _eedi3s(aa, mclip=mclip_up.std.Transpose(), **eedi3_args).std.Transpose()
    aa = ssim_downsample(_eedi3s(aa, mclip=mclip_up, **eedi3_args), clip.width, clip.height)
    aa = depth(aa, get_depth(clip_y))

    aa_merge = core.std.MaskedMerge(clip_y, aa, lmask)

    if clip.format.num_planes == 1:
        return aa_merge
    return join([aa_merge, plane(clip, 1), plane(clip, 2)])


# Aliases
sraa = upscaled_sraa
