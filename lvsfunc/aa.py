"""
    Functions for various anti-aliasing functions and wrappers.
"""
from typing import Any, Callable, Dict, Optional

import vapoursynth as vs
from vsutil import fallback, get_w, get_y, join, plane

from . import kernels, util
from .misc import scale_thresh

core = vs.core


def clamp_aa(src: vs.VideoNode, weak: vs.VideoNode, strong: vs.VideoNode, strength: float = 1) -> vs.VideoNode:
    """
    Clamp stronger AAs to weaker AAs.

    Stolen from Zastin.

    :param src:      Non-AA'd source clip.
    :param weak:     Weakly-AA'd clip (eg: nnedi3)
    :param strong:   Strongly-AA'd clip (eg: eedi3)
    :param strength: Clamping strength (Default: 1)

    :return:         Clip with clamped anti-aliasing.
    """
    if src.format is None or weak.format is None or strong.format is None:
        raise ValueError("nneedi3_clamp: 'Variable-format clips not supported'")
    thr = strength * (1 << (src.format.bits_per_sample - 8)) if src.format.sample_type == vs.INTEGER \
        else strength/219
    clamp = core.std.Expr([get_y(src), get_y(weak), get_y(strong)],
                          expr=f"x y - x z - xor x x y - abs x z - abs < z y {thr} + min y {thr} - max z ? ?"
                          if thr != 0 else "x y z min max y z max min")
    return clamp if src.format.color_family == vs.GRAY \
        else core.std.ShufflePlanes([clamp, src], planes=[0, 1, 2], colorfamily=vs.YUV)


def taa(clip: vs.VideoNode, aafun: Callable[[vs.VideoNode], vs.VideoNode]) -> vs.VideoNode:
    """
    Perform transpose AA.

    :param clip:   Input clip.
    :param aafun:  Antialiasing function

    :return:       Antialiased clip
    """
    if clip.format is None:
        raise ValueError("taa: 'Variable-format clips not supported'")

    y = get_y(clip)

    aa = aafun(y.std.Transpose())
    aa = aa.resize.Spline36(height=clip.width, src_top=0.5).std.Transpose()
    aa = aafun(aa)
    aa = aa.resize.Spline36(height=clip.height, src_top=0.5)

    return aa if clip.format.color_family == vs.GRAY \
        else core.std.ShufflePlanes([aa, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


def nnedi3(clip: vs.VideoNode, opencl: bool = False, **override: Any) -> vs.VideoNode:
    """
    Standard nnedi3 antialiasing.

    Dependencies:
    * vapoursynth-nnedi3
    * vapoursynth-NNEDI3CL (Optional: opencl)

    :param clip:     Input clip
    :param opencl:   Use OpenCL (Default: False)
    :param override: nnedi3 parameter overrides

    :return:         Antialiased clip
    """
    nnedi3_args: Dict[str, Any] = dict(field=0, dh=True, nsize=3, nns=3, qual=1)
    nnedi3_args.update(override)

    def _nnedi3(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.nnedi3cl.NNEDI3CL(**nnedi3_args) if opencl \
            else clip.nnedi3.nnedi3(**nnedi3_args)

    return taa(clip, _nnedi3)


def eedi3(clip: vs.VideoNode, opencl: bool = False, **override: Any) -> vs.VideoNode:
    """
    Standard eedi3 antialiasing.

    Dependencies:
    * vapoursynth-EEDI3

    :param clip:     Input clip
    :param opencl:   Use OpenCL (Default: False)
    :param override: eedi3 parameter overrides

    :return:         Antialiased clip
    """
    eedi3_args: Dict[str, Any] = dict(field=0, dh=True, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20)
    eedi3_args.update(override)

    def _eedi3(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.eedi3m.EEDI3CL(**eedi3_args) if opencl \
            else clip.eedi3m.EEDI3(**eedi3_args)

    return taa(clip, _eedi3)


def kirsch_aa_mask(clip: vs.VideoNode, mthr: float = 0.25) -> vs.VideoNode:
    """
    Kirsh-based AA mask.

    Dependencies:
    * kagefunc

    :param clip: Input clip
    :param mthr: Mask threshold, scaled to clip range if between 0 and 1 (inclusive).
                 (Default: 0.25)
    """
    try:
        from kagefunc import kirsch
    except ModuleNotFoundError:
        raise ModuleNotFoundError("nnedi3_clamp: missing dependency 'kagefunc'")

    return kirsch(get_y(clip)).std.Binarize(scale_thresh(mthr, clip)).std.Maximum().std.Convolution([1] * 9)


def nneedi3_clamp(clip: vs.VideoNode, strength: float = 1,
                  mask: Optional[vs.VideoNode] = None,
                  mthr: float = 0.25, opencl: bool = False) -> vs.VideoNode:
    """
    A function that clamps eedi3 to nnedi3 for the purpose of reducing eedi3 artifacts.
    This should fix every issue created by eedi3. For example: https://i.imgur.com/hYVhetS.jpg

    Original function written by Zastin, modified by LightArrowsEXE.

    :param clip:                Input clip
    :param strength:            Set threshold strength for over/underflow value for clamping eedi3's result
                                to nnedi3 +/- strength * 256 scaled to 8 bit (Default: 1)
    :param mask:                Clip to use for custom mask (Default: None)
    :param mthr:                Binarize threshold for the mask, scaled to float (Default: 0.25)
    :param opencl:              OpenCL acceleration (Default: False)

    :return:                    Antialiased clip
    """
    if clip.format is None:
        raise ValueError("nneedi3_clamp: 'Variable-format clips not supported'")
    y = get_y(clip)
    merged = core.std.MaskedMerge(y, clamp_aa(y, nnedi3(y, opencl=opencl), eedi3(y, opencl=opencl)),
                                  mask or kirsch_aa_mask(y))
    return merged if clip.format.color_family == vs.GRAY else core.std.ShufflePlanes([merged, clip], [0, 1, 2], vs.YUV)


def transpose_aa(clip: vs.VideoNode,
                 eedi3: bool = False,
                 rep: int = 13) -> vs.VideoNode:
    """
    Function that performs anti-aliasing over a clip by using nnedi3/eedi3 and transposing multiple times.
    This results in overall stronger anti-aliasing.
    Useful for shows like Yuru Camp with bad lineart problems.

    Original function written by Zastin, modified by LightArrowsEXE.

    Dependencies:
    * RGSF (optional: 32 bit clip)
    * vapoursynth-EEDI3
    * vapoursynth-nnedi3
    * znedi3

    :param clip:      Input clip
    :param eedi3:     Use eedi3 for the interpolation (Default: False)
    :param rep:       Repair mode. Pass it 0 to not repair (Default: 13)

    :return:          Antialiased clip
    """
    if clip.format is None:
        raise ValueError("transpose_aa: 'Variable-format clips not supported'")

    clip_y = get_y(clip)

    def _aafun(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2).znedi3.nnedi3(1, 0, 0, 3, 4, 2) if eedi3 \
            else clip.nnedi3.nnedi3(0, 1, 0, 3, 3, 2).nnedi3.nnedi3(1, 0, 0, 3, 3, 2)

    def _taa(clip: vs.VideoNode) -> vs.VideoNode:
        aa = _aafun(clip.std.Transpose())
        aa = aa.resize.Bicubic(clip.height, clip.width, src_top=.5).std.Transpose()
        aa = _aafun(aa)
        return aa.resize.Bicubic(clip.width, clip.height, src_top=.5)

    def _csharp(flt: vs.VideoNode, clip: vs.VideoNode) -> vs.VideoNode:
        blur = core.std.Convolution(flt, [1] * 9)
        return core.std.Expr([flt, clip, blur], 'x y < x x + z - x max y min x x + z - x min y max ?')

    aaclip = _taa(clip_y)
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
    * RGSF (optional: 32 bit clip)
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

    nnargs: Dict[str, Any] = dict(field=0, nsize=0, nns=4, qual=2)
    # TAAmbk defaults are 0.5, 0.2, 20, 3, 30
    eeargs: Dict[str, Any] = dict(field=0, dh=False, alpha=0.2, beta=0.6, gamma=40, nrad=2, mdis=20)
    eeargs.update(eedi3_args)

    if rfactor < 1:
        raise ValueError("upscaled_sraa: '\"rfactor\" must be above 1'")

    ssw = round(clip.width * rfactor)
    ssw = (ssw + 1) & ~1
    ssh = round(clip.height * rfactor)
    ssh = (ssh + 1) & ~1

    height = height or clip.height

    if width is None:
        width = clip.width if height == clip.height else get_w(height, aspect_ratio=clip.width / clip.height)

    nnedi3cl = fallback(nnedi3cl, opencl)
    eedi3cl = fallback(eedi3cl, opencl)

    def _nnedi3(clip: vs.VideoNode, dh: bool = False) -> vs.VideoNode:
        return clip.nnedi3cl.NNEDI3CL(dh=dh, **nnargs) if nnedi3cl \
            else clip.nnedi3.nnedi3(dh=dh, **nnargs)

    def _eedi3(clip: vs.VideoNode, sclip: vs.VideoNode) -> vs.VideoNode:
        return clip.eedi3m.EEDI3CL(sclip=sclip, **eeargs) if eedi3cl \
            else clip.eedi3m.EEDI3(sclip=sclip, **eeargs)

    # Nnedi3 upscale from source height to source height * rounding (Default 1.5)
    up_y = _nnedi3(luma, dh=True)
    up_y = up_y.resize.Spline36(height=ssh, src_top=0.5).std.Transpose()
    up_y = _nnedi3(up_y, dh=True)
    up_y = up_y.resize.Spline36(height=ssw, src_top=0.5)

    # Single-rate AA
    aa_y = _eedi3(up_y, sclip=_nnedi3(up_y))
    aa_y = core.std.Transpose(aa_y)
    aa_y = _eedi3(aa_y, sclip=_nnedi3(aa_y))

    scaled = aa_y if downscaler is None else downscaler(aa_y, width, height)
    scaled = util.pick_repair(scaled)(scaled, luma.resize.Bicubic(width, height), mode=rep) if rep else scaled

    if clip.format.num_planes == 1 or downscaler is None:
        return scaled
    if height is not clip.height or width is not clip.width:
        if height % 2:
            raise ValueError("upscaled_sraa: '\"height\" must be an even number when not passing a GRAY clip'")
        if width % 2:
            raise ValueError("upscaled_sraa: '\"width\" must be an even number when not passing a GRAY clip'")

        chroma = kernels.Bicubic().scale(clip, width, height)
        return join([scaled, plane(chroma, 1), plane(chroma, 2)])
    return join([scaled, plane(clip, 1), plane(clip, 2)])
