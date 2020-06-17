"""
    Functions for various anti-aliasing functions and wrappers.
"""
from typing import Any, Callable, Dict, Optional

import vapoursynth as vs
from vsutil import get_w, get_y, join, plane

from . import util

core = vs.core


def nneedi3_clamp(clip: vs.VideoNode, strength: int = 1,
                  mask: Optional[vs.VideoNode] = None, ret_mask: bool = False,
                  show_mask: bool = False,
                  opencl: bool = False) -> vs.VideoNode:
    """
    A function that clamps eedi3 to nnedi3 for the purpose of reducing eedi3 artifacts.
    This should fix every issue created by eedi3. For example: https://i.imgur.com/hYVhetS.jpg

    Original function written by Zastin, modified by LightArrowsEXE.

    Dependencies:

    * kagefunc (optional: retinex edgemask)
    * vapoursynth-retinex (optional: retinex edgemask)
    * vapoursynth-tcanny (optional: retinex edgemask)
    * vapoursynth-eedi3
    * vapoursynth-nnedi3 or znedi3
    * vapoursynth-nnedi3cl (optional: opencl)
    * vsTAAmbk

    :param clip:                Input clip
    :param strength:            Set threshold strength (Default: 1)
    :param mask:                Clip to use for custom mask (Default: None)
    :param ret_mask:            Replace default mask with a retinex edgemask (Default: False)
    :param show_mask:           Return mask instead of clip (Default: False)
    :param opencl:              OpenCL acceleration (Default: False)

    :return:                    Antialiased clip
    """
    try:
        from vsTAAmbk import TAAmbk
    except ModuleNotFoundError:
        raise ModuleNotFoundError("nnedi3_clamp: missing dependency 'vsTAAmbk'")

    if clip.format is None:
        raise ValueError("nneedi3_clamp: 'Variable-format clips not supported'")

    bits = clip.format.bits_per_sample - 8
    thr = strength * (1 >> bits)
    strong = TAAmbk(clip, aatype='Eedi3', alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, mtype=0, opencl=opencl)
    weak = TAAmbk(clip, aatype='Nnedi3', nsize=3, nns=3, qual=1, mtype=0, opencl=opencl)
    expr = 'x z - y z - * 0 < y x y {0} + min y {0} - max ?'.format(thr)

    if clip.format.num_planes > 1:
        aa = core.std.Expr([strong, weak, clip], [expr, ''])
    else:
        aa = core.std.Expr([strong, weak, clip], expr)

    if mask:
        merged = clip.std.MaskedMerge(aa, mask, planes=0)
    elif ret_mask:
        try:
            import kagefunc as kgf
        except ModuleNotFoundError:
            raise ModuleNotFoundError("nnedi3_clamp: missing dependency 'kagefunc'")
        mask = kgf.retinex_edgemask(clip, 1).std.Binarize()
        merged = clip.std.MaskedMerge(aa, mask, planes=0)
    else:
        mask = clip.std.Prewitt(planes=0).std.Binarize(planes=0) \
            .std.Maximum(planes=0).std.Convolution([1] * 9, planes=0)
        mask = get_y(mask)
        merged = clip.std.MaskedMerge(aa, mask, planes=0)

    if show_mask:
        return mask
    return merged if clip.format.color_family == vs.GRAY else core.std.ShufflePlanes([merged, clip], [0, 1, 2], vs.YUV)


def transpose_aa(clip: vs.VideoNode,
                 eedi3: bool = False,
                 rep: int = 13) -> vs.VideoNode:
    """
    Function that performs anti-aliasing over a clip by using nnedi3/eedi3 and transposing multiple times.
    This results in overall stronger anti-aliasing.
    Useful for shows like Yuru Camp with bad lineart problems.

    Original function written by Zastin, modified by LightArrowsEXE.

    Dependencies: rgsf (optional: 32 bit clip), vapoursynth-eedi3, vapoursynth-nnedi3, znedi3

    :param clip:      Input clip
    :param eedi3:     Use eedi3 for the interpolation (Default: False)
    :param rep:       Repair mode. Pass it 0 to not repair (Default: 13)

    :return:          Antialiased clip
    """
    if clip.format is None:
        raise ValueError("transpose_aa: 'Variable-format clips not supported'")

    clip_y = get_y(clip)

    if eedi3:
        def _aa(clip_y: vs.VideoNode) -> vs.VideoNode:
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            clip_y = clip_y.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            clip_y = clip_y.resize.Spline36(clip.height, clip.width, src_top=.5)
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            clip_y = clip_y.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            return clip_y.resize.Spline36(clip.width, clip.height, src_top=.5)
    else:
        def _aa(clip_y: vs.VideoNode) -> vs.VideoNode:
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            clip_y = clip_y.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            clip_y = clip_y.resize.Spline36(clip.height, clip.width, src_top=.5)
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            clip_y = clip_y.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            return clip_y.resize.Spline36(clip.width, clip.height, src_top=.5)

    def _csharp(flt: vs.VideoNode, clip: vs.VideoNode) -> vs.VideoNode:
        blur = core.std.Convolution(flt, [1] * 9)
        return core.std.Expr([flt, clip, blur], 'x y < x x + z - x max y min x x + z - x min y max ?')

    aaclip = _aa(clip_y)
    aaclip = _csharp(aaclip, clip_y)
    aaclip = util.pick_repair(clip_y)(aaclip, clip_y, rep)

    return aaclip if clip.format.color_family is vs.GRAY else core.std.ShufflePlanes([aaclip, clip], [0, 1, 2], vs.YUV)


def upscaled_sraa(clip: vs.VideoNode,
                  rfactor: float = 1.5,
                  rep: Optional[int] = None,
                  width: Optional[int] = None, height: Optional[int] = None,
                  downscaler: Optional[Callable[[vs.VideoNode, int, int], vs.VideoNode]]
                  = core.resize.Spline36,
                  **eedi3_args: Any) -> vs.VideoNode:
    """
    A function that performs an upscaled single-rate AA to deal with heavy aliasing and broken-up lineart.
    Useful for Web rips, where the source quality is not good enough to descale,
    but you still want to deal with some bad aliasing and lineart.

    Original function written by Zastin, heavily modified by LightArrowsEXE.

    Alias for this function is `lvsfunc.sraa`.

    Dependencies: fmtconv, rgsf (optional: 32 bit clip), vapoursynth-eedi3, vapoursynth-nnedi3

    :param clip:            Input clip
    :param rfactor:         Image enlargement factor. 1.3..2 makes it comparable in strength to vsTAAmbk
                            It is not recommended to go below 1.3 (Default: 1.5)
    :param rep:             Repair mode (Default: None)
    :param width:           Target resolution width. If None, determine from `height`
    :param height:          Target resolution height (Default: ``clip.height``)
    :param downscaler:      Resizer used to downscale the AA'd clip
    :param kwargs:          Arguments passed to znedi3 (Default: alpha=0.2, beta=0.6, gamma=40, nrad=2, mdis=20)

    :return:                Antialiased and optionally rescaled clip
    """
    if clip.format is None:
        raise ValueError("upscaled_sraa: 'Variable-format clips not supported'")

    luma = get_y(clip)

    nnargs: Dict[str, Any] = dict(nsize=0, nns=4, qual=2)
    # TAAmbk defaults are 0.5, 0.2, 20, 3, 30
    eeargs: Dict[str, Any] = dict(alpha=0.2, beta=0.6, gamma=40, nrad=2, mdis=20)
    eeargs.update(eedi3_args)

    if rfactor < 1:
        raise ValueError("upscaled_sraa: '\"rfactor\" must be above 1'")

    ssw = round(clip.width * rfactor)
    ssh = round(clip.height * rfactor)

    while ssw % 2:
        ssw += 1
    while ssh % 2:
        ssh += 1

    if height is None:
        height = clip.height
    if width is None:
        if height != clip.height:
            width = get_w(height, aspect_ratio = clip.width / clip.height)
        else:
            width = clip.width

    # Nnedi3 upscale from source height to source height * rounding (Default 1.5)
    up_y = core.nnedi3.nnedi3(luma, 0, 1, 0, **nnargs)
    up_y = core.resize.Spline36(up_y, height=ssh, src_top=.5)
    up_y = core.std.Transpose(up_y)
    up_y = core.nnedi3.nnedi3(up_y, 0, 1, 0, **nnargs)
    up_y = core.resize.Spline36(up_y, height=ssw, src_top=.5)

    # Single-rate AA
    aa_y = core.eedi3m.EEDI3(up_y, 0, 0, 0, sclip=core.nnedi3.nnedi3(up_y, 0, 0, 0, **nnargs), **eeargs)
    aa_y = core.std.Transpose(aa_y)
    aa_y = core.eedi3m.EEDI3(aa_y, 0, 0, 0, sclip=core.nnedi3.nnedi3(aa_y, 0, 0, 0, **nnargs), **eeargs)

    # Back to source clip height or given height
    scaled = downscaler(aa_y, width, height)

    if rep:
        scaled = util.pick_repair(scaled)(scaled, luma.resize.Bicubic(width, height), mode=rep)

    if clip.format.num_planes == 1:
        return scaled
    return join([scaled, plane(clip, 1), plane(clip, 2)])
