"""
    Functions for various anti-aliasing functions and wrappers.
"""
from typing import Any, Callable, Dict, Optional

import vapoursynth as vs
from vsutil import depth, fallback, get_w, get_y, join, plane

from . import kernels, util

core = vs.core


def nneedi3_clamp(clip: vs.VideoNode, strength: float = 1,
                  mask: Optional[vs.VideoNode] = None, ret_mask: bool = False,
                  mthr: float = 0.25, show_mask: bool = False,
                  opencl: bool = False, nnedi3cl: Optional[bool] = None,
                  eedi3cl: Optional[bool] = None) -> vs.VideoNode:
    """
    A function that clamps eedi3 to nnedi3 for the purpose of reducing eedi3 artifacts.
    This should fix every issue created by eedi3. For example: https://i.imgur.com/hYVhetS.jpg

    Original function written by Zastin, modified by LightArrowsEXE.

    Dependencies:
    * kagefunc (optional: retinex edgemask)
    * vapoursynth-retinex (optional: retinex edgemask)
    * vapoursynth-tcanny (optional: retinex edgemask)
    * vapoursynth-eedi3
    * vapoursynth-nnedi3
    * vapoursynth-nnedi3cl (optional: opencl)

    :param clip:                Input clip
    :param strength:            Set threshold strength for over/underflow value for clamping eedi3's result
                                to nnedi3 +/- strength * 256 scaled to 8 bit (Default: 1)
    :param mask:                Clip to use for custom mask (Default: None)
    :param ret_mask:            Replace default mask with a retinex edgemask (Default: False)
    :param mthr:                Binarize threshold for the mask, scaled to float (Default: 0.25)
    :param show_mask:           Return mask instead of clip (Default: False)
    :param opencl:              OpenCL acceleration (Default: False)
    :param nnedi3cl:            OpenCL acceleration for nnedi3 (Default: False)
    :param eedi3cl:             OpenCL acceleration for eedi3 (Default: False)

    :return:                    Antialiased clip
    """

    if clip.format is None:
        raise ValueError("nneedi3_clamp: 'Variable-format clips not supported'")

    clip_y = get_y(clip)

    bits = clip.format.bits_per_sample
    sample_type = clip.format.sample_type
    shift = bits - 8
    thr = strength * (1 >> shift) if sample_type == vs.INTEGER else strength/219
    expr = 'x z - y z - xor y x y {0} + min y {0} - max ?'.format(thr)

    if sample_type == vs.INTEGER:
        mthr = round(mthr * ((1 >> shift) - 1))

    if mask is None:
        try:
            from kagefunc import kirsch
        except ModuleNotFoundError:
            raise ModuleNotFoundError("nnedi3_clamp: missing dependency 'kagefunc'")
        mask = kirsch(clip_y)
        if ret_mask:
            # workaround to support float input
            ret = depth(clip_y, min(16, bits))
            ret = core.retinex.MSRCP(ret, sigma=[50, 200, 350], upper_thr=0.005)
            ret = depth(ret, bits)
            tcanny = core.tcanny.TCanny(ret, mode=1, sigma=[1.0])
            tcanny = core.std.Minimum(tcanny, coordinates=[1, 0, 1, 0, 0, 1, 0, 1])
            # no clamping needed when binarizing
            mask = core.std.Expr([mask, tcanny], 'x y +')
        mask = mask.std.Binarize(thr).std.Maximum().std.Convolution([1] * 9)

    nnedi3cl = fallback(nnedi3cl, opencl)
    eedi3cl = fallback(eedi3cl, opencl)

    nnedi3_args: Dict[str, Any] = dict(nsize=3, nns=3, qual=1)
    eedi3_args: Dict[str, Any] = dict(alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20)

    clip_tra = core.std.Transpose(clip_y)

    if eedi3cl:
        strong = core.eedi3m.EEDI3CL(clip_tra, 0, True, **eedi3_args)
        strong = core.resize.Spline36(strong, height=clip.width, src_top=0.5)
        strong = core.std.Transpose(strong)
        strong = core.eedi3m.EEDI3CL(strong, 0, True, **eedi3_args)
        strong = core.resize.Spline36(strong, height=clip.height, src_top=0.5)
    else:
        strong = core.eedi3m.EEDI3(clip_tra, 0, True, mclip=mask.std.Transpose(), **eedi3_args)
        strong = core.resize.Spline36(strong, height=clip.width, src_top=0.5)
        strong = core.std.Transpose(strong)
        strong = core.eedi3m.EEDI3(strong, 0, True, mclip=mask, **eedi3_args)
        strong = core.resize.Spline36(strong, height=clip.height, src_top=0.5)

    nnedi3: Callable[..., vs.VideoNode] = core.nnedi3.nnedi3
    if nnedi3cl:
        nnedi3 = core.nnedi3cl.NNEDI3CL

    weak = nnedi3(clip_tra, 0, True, **nnedi3_args)
    weak = core.resize.Spline36(weak, height=clip.width, src_top=0.5)
    weak = core.std.Transpose(weak)
    weak = nnedi3(weak, 0, True, **nnedi3_args)
    weak = core.resize.Spline36(weak, height=clip.height, src_top=0.5)

    aa = core.std.Expr([strong, weak, clip_y], expr)

    merged = core.std.MaskedMerge(clip_y, aa, mask)

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
            clip_y = clip_y.resize.Bicubic(clip.height, clip.width, src_top=.5)
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            clip_y = clip_y.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            return clip_y.resize.Bicubic(clip.width, clip.height, src_top=.5)
    else:
        def _aa(clip_y: vs.VideoNode) -> vs.VideoNode:
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            clip_y = clip_y.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            clip_y = clip_y.resize.Bicubic(clip.height, clip.width, src_top=.5)
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            clip_y = clip_y.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            return clip_y.resize.Bicubic(clip.width, clip.height, src_top=.5)

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
                  = kernels.Spline36().scale,
                  opencl: bool = False, nnedi3cl: Optional[bool] = None,
                  eedi3cl: Optional[bool] = None,
                  **eedi3_args: Any) -> vs.VideoNode:
    """
    A function that performs a supersampled single-rate AA to deal with heavy aliasing and broken-up lineart.
    Useful for Web rips, where the source quality is not good enough to descale,
    but you still want to deal with some bad aliasing and lineart.

    It works by supersampling the clip, performing AA, and then downscaling again.
    Downscaling can be disabled by setting `downscaler` to `None`, returning the supersampled luma clip.
    The dimensions of the downscaled clip can also be adjusted by setting `height` or `width`.
    Setting either `height` or `width` will also scale the chroma accordingly.

    Original function written by Zastin, heavily modified by LightArrowsEXE.

    Alias for this function is `lvsfunc.sraa`.

    Dependencies:
    * fmtconv
    * rgsf (optional: 32 bit clip),
    * vapoursynth-eedi3
    * vapoursynth-nnedi3
    * vapoursynth-nnedi3cl (optional: opencl)

    :param clip:            Input clip
    :param rfactor:         Image enlargement factor. 1.3..2 makes it comparable in strength to vsTAAmbk
                            It is not recommended to go below 1.3 (Default: 1.5)
    :param rep:             Repair mode (Default: None)
    :param width:           Target resolution width. If None, determined from `height`
    :param height:          Target resolution height (Default: ``clip.height``)
    :param downscaler:      Resizer used to downscale the AA'd clip
    :param opencl:          OpenCL acceleration (Default: False)
    :param nnedi3cl:        OpenCL acceleration for nnedi3 (Default: False)
    :param eedi3cl:         OpenCL acceleration for eedi3 (Default: False)
    :param eedi3_args:      Arguments passed to eedi3 (Default: alpha=0.2, beta=0.6, gamma=40, nrad=2, mdis=20)

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
            width = get_w(height, aspect_ratio=clip.width / clip.height)
        else:
            width = clip.width

    nnedi3cl = fallback(nnedi3cl, opencl)
    eedi3cl = fallback(eedi3cl, opencl)

    nnedi3 = core.nnedi3cl.NNEDI3CL if nnedi3cl else core.nnedi3.nnedi3
    eedi3 = core.eedi3m.EEDI3CL if eedi3cl else core.eedi3m.EEDI3

    # Nnedi3 upscale from source height to source height * rounding (Default 1.5)
    up_y = nnedi3(luma, 0, 1, 0, **nnargs)
    up_y = core.resize.Spline36(up_y, height=ssh, src_top=.5)
    up_y = core.std.Transpose(up_y)
    up_y = nnedi3(up_y, 0, 1, 0, **nnargs)
    up_y = core.resize.Spline36(up_y, height=ssw, src_top=.5)

    # Single-rate AA
    aa_y = eedi3(up_y, 0, 0, 0, sclip=nnedi3(up_y, 0, 0, 0, **nnargs), **eeargs)
    aa_y = core.std.Transpose(aa_y)
    aa_y = eedi3(aa_y, 0, 0, 0, sclip=nnedi3(aa_y, 0, 0, 0, **nnargs), **eeargs)

    # Back to source clip height or given height
    if downscaler is None:
        scaled = aa_y
    else:
        scaled = downscaler(aa_y, width, height)

    if rep:
        scaled = util.pick_repair(scaled)(scaled, luma.resize.Bicubic(width, height), mode=rep)

    if clip.format.num_planes == 1 or downscaler is None:
        return scaled
    if height is not clip.height or width is not clip.width:
        if height % 2:
            raise ValueError("upscaled_sraa: '\"height\" must be an even number when not passing a GRAY clip'")
        if width % 2:
            raise ValueError("upscaled_sraa: '\"width\" must be an even number when not passing a GRAY clip'")

        chr = kernels.Bicubic().scale(clip, width, height)
        return join([scaled, plane(chr, 1), plane(chr, 2)])
    return join([scaled, plane(clip, 1), plane(clip, 2)])
