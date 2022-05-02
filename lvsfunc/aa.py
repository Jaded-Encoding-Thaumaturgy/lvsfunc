from __future__ import annotations

from math import ceil
from typing import Any, Callable, Dict, List

import vapoursynth as vs
from vsutil import (depth, fallback, get_depth, get_w, get_y, join, plane,
                    scale_value)

from .kernels import Bicubic, Catrom, Point
from .scale import ssim_downsample
from .util import check_variable, pick_repair, scale_thresh

core = vs.core


__all__: List[str] = [
    'based_aa',
    'clamp_aa',
    'nnedi3', 'eedi3',
    'nneedi3_clamp',
    'taa',
    'transpose_aa',
    'upscaled_sraa', 'sraa',
]


def clamp_aa(src: vs.VideoNode, weak: vs.VideoNode, strong: vs.VideoNode, strength: float = 1) -> vs.VideoNode:
    """
    Clamp stronger AAs to weaker AAs.
    Useful for clamping upscaled_sraa or eedi3 to nnedi3 for a strong but precise AA.

    Stolen from Zastin.

    :param src:      Non-AA'd source clip.
    :param weak:     Weakly-AA'd clip (eg: nnedi3)
    :param strong:   Strongly-AA'd clip (eg: eedi3)
    :param strength: Clamping strength (Default: 1)

    :return:         Clip with clamped anti-aliasing.
    """
    check_variable(src, "clamp_aa")

    if src.format is None or weak.format is None or strong.format is None:
        raise ValueError("clamp_aa: 'Variable-format clips not supported'")
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
    Example for nnedi3cl: taa(clip, nnedi3(opencl=True))

    :param clip:   Input clip.
    :param aafun:  Antialiasing function

    :return:       Antialiased clip
    """
    check_variable(clip, "taa")
    assert clip.format

    y = get_y(clip)

    aa = aafun(y.std.Transpose())
    aa = Catrom().scale(aa, width=clip.height, height=clip.width, shift=(0.5, 0))
    aa = aafun(aa.std.Transpose())
    aa = Catrom().scale(aa, width=clip.width, height=clip.height, shift=(0.5, 0))

    return aa if clip.format.color_family == vs.GRAY \
        else core.std.ShufflePlanes([aa, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


def nnedi3(opencl: bool = False, **override: Any) -> Callable[[vs.VideoNode], vs.VideoNode]:
    """
    Generate nnedi3 antialiaser.

    Dependencies:

    * vapoursynth-nnedi3
    * vapoursynth-NNEDI3CL (Optional: opencl)

    :param opencl:   Use OpenCL (Default: False)
    :param override: nnedi3 parameter overrides

    :return:         Configured nnedi3 function
    """
    nnedi3_args: Dict[str, Any] = dict(field=0, dh=True, nsize=3, nns=3, qual=1)
    nnedi3_args.update(override)

    def _nnedi3(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.nnedi3cl.NNEDI3CL(**nnedi3_args) if opencl \
            else clip.nnedi3.nnedi3(**nnedi3_args)

    return _nnedi3


def eedi3(opencl: bool = False, **override: Any) -> Callable[[vs.VideoNode], vs.VideoNode]:
    """
    Generate eedi3 antialiaser.

    Dependencies:

    * vapoursynth-EEDI3

    :param opencl:   Use OpenCL (Default: False)
    :param override: eedi3 parameter overrides

    :return:         Configured eedi3 function
    """
    eedi3_args: Dict[str, Any] = dict(field=0, dh=True, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20)
    eedi3_args.update(override)

    def _eedi3(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.eedi3m.EEDI3CL(**eedi3_args) if opencl \
            else clip.eedi3m.EEDI3(**eedi3_args)

    return _eedi3


def nneedi3_clamp(clip: vs.VideoNode, strength: float = 1,
                  mask: vs.VideoNode | None = None,
                  mthr: float = 0.25, opencl: bool = False) -> vs.VideoNode:
    """
    A function that clamps eedi3 to nnedi3 for the purpose of reducing eedi3 artifacts.
    This should fix every issue created by eedi3. For example, `see this image <https://i.imgur.com/hYVhetS.jpg>`_.

    Original function written by Zastin, modified by LightArrowsEXE.

    :param clip:                Input clip
    :param strength:            Set threshold strength for over/underflow value for clamping eedi3's result
                                to nnedi3 +/- strength * 256 scaled to 8 bit (Default: 1)
    :param mask:                Clip to use for custom mask (Default: None)
    :param mthr:                Binarize threshold for the mask, scaled to float (Default: 0.25)
    :param opencl:              OpenCL acceleration (Default: False)

    :return:                    Antialiased clip
    """
    check_variable(clip, "nneedi3_clamp")
    assert clip.format

    y = get_y(clip)
    mask = mask or y.std.Prewitt().std.Binarize(scale_thresh(mthr, y)).std.Maximum().std.Convolution([1]*9)
    merged = core.std.MaskedMerge(y,
                                  clamp_aa(y, taa(y, nnedi3(opencl=opencl)), taa(y, eedi3(opencl=opencl)), strength),
                                  mask)
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
    check_variable(clip, "transpose_aa")
    assert clip.format

    clip_y = get_y(clip)

    def _aafun(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2).znedi3.nnedi3(1, 0, 0, 3, 4, 2) if eedi3 \
            else clip.nnedi3.nnedi3(0, 1, 0, 3, 3, 2).nnedi3.nnedi3(1, 0, 0, 3, 3, 2)

    def _taa(clip: vs.VideoNode) -> vs.VideoNode:
        aa = _aafun(clip.std.Transpose())
        aa = Catrom().scale(aa, clip.height, clip.width, shift=(0.5, 0))
        aa = _aafun(aa.std.Transpose())
        return Catrom().scale(aa, clip.width, clip.height, shift=(0.5, 0))

    def _csharp(flt: vs.VideoNode, clip: vs.VideoNode) -> vs.VideoNode:
        blur = core.std.Convolution(flt, [1] * 9)
        return core.std.Expr([flt, clip, blur], 'x y < x x + z - x max y min x x + z - x min y max ?')

    aaclip = _taa(clip_y)
    aaclip = _csharp(aaclip, clip_y)
    aaclip = pick_repair(clip_y)(aaclip, clip_y, rep)

    return aaclip if clip.format.color_family is vs.GRAY else core.std.ShufflePlanes([aaclip, clip], [0, 1, 2], vs.YUV)


def _nnedi3_supersample(clip: vs.VideoNode, width: int, height: int, opencl: bool = False) -> vs.VideoNode:
    check_variable(clip, "_nnedi3_supersample")

    nnargs: Dict[str, Any] = dict(field=0, dh=True, nsize=0, nns=4, qual=2)
    _nnedi3 = nnedi3(opencl=opencl, **nnargs)
    up_y = _nnedi3(get_y(clip))
    up_y = Catrom().scale(up_y, width=up_y.width, height=height, shift=(0.5, 0))
    up_y = _nnedi3(up_y.std.Transpose())
    up_y = Catrom().scale(up_y, width=up_y.width, height=width, shift=(0.5, 0))
    return up_y.std.Transpose()


def _eedi3_singlerate(clip: vs.VideoNode) -> vs.VideoNode:
    check_variable(clip, "_eedi3_singlerate")

    eeargs: Dict[str, Any] = dict(field=0, dh=False, alpha=0.2, beta=0.6, gamma=40, nrad=2, mdis=20)
    nnargs: Dict[str, Any] = dict(field=0, dh=False, nsize=0, nns=4, qual=2)
    y = get_y(clip)
    return eedi3(sclip=nnedi3(**nnargs)(y), **eeargs)(y)


def upscaled_sraa(clip: vs.VideoNode,
                  rfactor: float = 1.5,
                  width: int | None = None, height: int | None = None,
                  supersampler: Callable[[vs.VideoNode, int, int], vs.VideoNode] = _nnedi3_supersample,
                  downscaler: Callable[[vs.VideoNode, int, int], vs.VideoNode] | None
                  = Bicubic(b=0, c=1/2).scale,
                  aafun: Callable[[vs.VideoNode], vs.VideoNode] = _eedi3_singlerate) -> vs.VideoNode:
    """
    A function that performs a supersampled single-rate AA to deal with heavy aliasing and broken-up lineart.
    Useful for heavy antialiasing.

    It works by supersampling the clip, performing AA, and then downscaling again.
    Downscaling can be disabled by setting `downscaler` to `None`, returning the supersampled luma clip.
    The dimensions of the downscaled clip can also be adjusted by setting `height` or `width`.
    Setting either `height` or `width` will also scale the chroma accordingly.

    Original function written by Zastin, heavily modified by LightArrowsEXE.

    Alias for this function is `lvsfunc.sraa`.

    Dependencies:

    * vapoursynth-eedi3 (default aafun)
    * vapoursynth-nnedi3 (default supersampler and aafun)

    :param clip:            Input clip
    :param rfactor:         Image enlargement factor. 1.3..2 makes it comparable in strength to vsTAAmbk
                            It is not recommended to go below 1.3 (Default: 1.5)
    :param width:           Target resolution width. If None, determined from `height`
    :param height:          Target resolution height (Default: ``clip.height``)
    :param supersampler:    Supersampler used for upscaling before AA (Default: nnedi3 supersampler)
    :param downscaler:      Downscaler to use after supersampling (Default: Bicubic(b=0, c=1/2)
    :param aafun:           Function used to antialias after supersampling (Default: eedi3 with nnedi3 sclip)

    :return:                Antialiased clip
    """
    check_variable(clip, "upscaled_sraa")
    assert clip.format

    luma = get_y(clip)

    if rfactor < 1:
        raise ValueError("upscaled_sraa: '\"rfactor\" must be above 1'")

    ssw = round(clip.width * rfactor)
    ssw = (ssw + 1) & ~1
    ssh = round(clip.height * rfactor)
    ssh = (ssh + 1) & ~1

    height = height or clip.height

    if width is None:
        width = clip.width if height == clip.height else get_w(height, aspect_ratio=clip.width / clip.height)

    up_y = supersampler(luma, ssw, ssh)

    aa_y = aafun(aafun(up_y.std.Transpose()).std.Transpose())

    scaled = aa_y if downscaler is None else downscaler(aa_y, width, height)

    if clip.format.num_planes == 1 or downscaler is None or height != clip.height or width != clip.width:
        return scaled

    return core.std.ShufflePlanes([scaled, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


def based_aa(clip: vs.VideoNode, shader_file: str = "FSRCNNX_x2_56-16-4-1.glsl",
             rfactor: float = 2.0, tff: bool = True,
             mask_thr: float = 60, show_mask: bool = False,
             lmask: vs.VideoNode | None = None, **eedi3_args: Any) -> vs.VideoNode:
    """
    As the name implies, this is a based anti-aliaser. Thank you, based Zastin.
    This relies on FSRCNNX being very sharp, and as such it very much acts like the main "AA" here.

    Original function by Zastin, modified by LightArrowsEXE.

    Dependencies:

    * vapoursynth-eedi3
    * vs-placebo

    :param clip:            Input clip
    :param shader_file:     Path to FSRCNNX shader file
    :param rfactor:         Image enlargement factor
    :param tff:             Top-Field-First if true, Bottom-Field-First if false
    :param mask_thr:        Threshold for the edge mask binarisation.
                            Scaled internally to match bitdepth of clip.
    :param show_mask:       Output mask
    :param eedi3_args:      Additional args to pass to eedi3
    :param lmask:           Line mask clip to use for eedi3

    :return:                AA'd clip or mask clip
    """
    def _eedi3s(clip: vs.VideoNode, mclip: vs.VideoNode | None = None,
                **eedi3_kwargs: Any) -> vs.VideoNode:
        edi_args: Dict[str, Any] = {  # Eedi3 args for `eedi3s`
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
        return core.fmtc.resample(mclip, ow, oh, kernel='box', fulls=1, fulld=1)

    check_variable(clip, "based_aa")
    assert clip.format

    aaw = (round(clip.width * rfactor) + 1) & ~1
    aah = (round(clip.height * rfactor) + 1) & ~1

    clip_y = get_y(clip)

    if not lmask:
        if mask_thr > 255:
            raise ValueError(f"based_aa: 'mask_thr must be equal to or lower than 255 (current: {mask_thr})'")

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
