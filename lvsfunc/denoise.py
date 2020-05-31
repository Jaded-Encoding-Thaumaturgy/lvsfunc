"""
    Wrappers and masks for denoising.
"""
from typing import Any, Optional, cast

import vapoursynth as vs
from vsutil import depth, get_y, join, split

from . import util

try:
    from cytoolz import functoolz
except ModuleNotFoundError:
    try:
        from toolz import functoolz  # type: ignore
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Cannot find functoolz: Please install toolz or cytoolz")

core = vs.core


def quick_denoise(clip: vs.VideoNode,
                  ref: Optional[vs.VideoNode] = None,
                  cmode: str = 'knlm',
                  sigma: float = 2,
                  **kwargs: Any) -> vs.VideoNode:
    """
    This wrapper is used to denoise both the luma and chroma using various denoisers of your choosing.
    If you wish to use just one denoiser,
    you're probably better off using that specific filter rather than this wrapper.

    A rewrite of my old 'quick_denoise'. I still hate it, but whatever.
    This will probably be removed in a future commit.

    BM3D is used for denoising the luma.

    Special thanks to kageru for helping me out with some ideas and pointers.

    Alias for this function is `lvsfunc.qden`.

    Dependencies: havsfunc (optional: SMDegrain mode), mvsfunc

    Deciphering havsfunc's dependencies is left as an excercise for the user.

    :param clip:         Input clip
    :param cmode:        Chroma denoising modes:
                          'knlm' - Use knlmeans for denoising the chroma (Default),
                          'tnlm' - Use tnlmeans for denoising the chroma,
                          'dft'  - Use dfttest for denoising the chroma (requires setting 'sbsize' in kwargs),
                          'smd'  - Use SMDegrain for denoising the chroma,
    :param sigma:        Denoising strength for BM3D (Default: 2)
    :param ref:          Optional reference clip to replace BM3D's basic estimate
    :param kwargs:       Parameters passed to chroma denoiser

    :return:             Denoised clip
    """
    try:
        import mvsfunc as mvf
    except ModuleNotFoundError:
        raise ModuleNotFoundError("quick_denoise: missing dependency 'mvsfunc'")

    if clip.format is None or clip.format.color_family not in (vs.YUV, vs.YCOCG, vs.RGB):
        raise ValueError("quick_denoise: input clip must be vs.YUV, vs.YCOCG, or vs.RGB")

    planes = split(clip)
    cmode = cmode.lower()

    if cmode in [1, 'knlm', 'knlmeanscl']:
        planes[1] = planes[1].knlm.KNLMeansCL(d=3, a=2, **kwargs)
        planes[2] = planes[2].knlm.KNLMeansCL(d=3, a=2, **kwargs)
    elif cmode in [2, 'tnlm', 'tnlmeans']:
        planes[1] = planes[1].tnlm.TNLMeans(ax=2, ay=2, az=2, **kwargs)
        planes[2] = planes[2].tnlm.TNLMeans(ax=2, ay=2, az=2, **kwargs)
    elif cmode in [3, 'dft', 'dfttest']:
        try:
            sbsize = cast(int, kwargs['sbsize'])
            planes[1] = planes[1].dfttest.DFTTest(sosize=int(sbsize * 0.75), **kwargs)
            planes[2] = planes[2].dfttest.DFTTest(sosize=int(sbsize * 0.75), **kwargs)
        except KeyError:
            raise ValueError(f"quick_denoise: '\"sbsize\" not specified'")
    elif cmode in [4, 'smd', 'smdegrain']:
        try:
            import havsfunc as haf
        except ModuleNotFoundError:
            raise ModuleNotFoundError("quick_denoise: missing dependency 'havsfunc'")

        planes[1] = haf.SMDegrain(planes[1], prefilter=3, **kwargs)
        planes[2] = haf.SMDegrain(planes[2], prefilter=3, **kwargs)
    else:
        raise ValueError(f"quick_denoise: 'Unknown cmode'")

    ref = ref or planes[0]
    planes[0] = mvf.BM3D(planes[0], sigma=sigma, psample=0, radius1=1, ref=ref)
    return join(planes)


@functoolz.curry
def adaptive_mask(clip: vs.VideoNode, luma_scaling: float = 8.0) -> vs.VideoNode:
    """
    A wrapper to create a luma mask for denoising and/or debanding.

    Function is curried to allow parameter tuning when passing to denoisers
    that allow you to pass your own mask.

    Dependencies: adaptivegrain

    :param clip:         Input clip
    :param luma_scaling: Luma scaling factor (Default: 8.0)

    :return:             Luma mask
    """
    return core.adg.Mask(clip.std.PlaneStats(), luma_scaling)


@functoolz.curry
def detail_mask(clip: vs.VideoNode, pre_denoise: Optional[float] = None,
                rad: int = 3, radc: int = 2,
                brz_a: float = 0.005, brz_b: float = 0.005) -> vs.VideoNode:
    """
        A wrapper for creating a detail mask to be used during denoising and/or debanding.
        The detail mask is created using debandshit's rangemask,
        and is then merged with Prewitt to catch lines it may have missed.

        Function is curried to allow parameter tuning when passing to denoisers
        that allow you to pass your own mask.

        Dependencies: knlmeans (optional: pre_denoise), debandshit

        :param clip:        Input clip
        :param pre_denoise: Denoise the clip before creating the mask (Default: False)
        :param rad:         The luma equivalent of gradfun3's "mask" parameter
        :param radc:        The chroma equivalent of gradfun3's "mask" parameter
        :brz_a:             Binarizing for the detail mask (Default: 0.05)
        :brz_b:             Binarizing for the edge mask (Default: 0.05)

        :return:            Detail mask
    """
    try:
        from debandshit import rangemask
    except ModuleNotFoundError:
        raise ModuleNotFoundError("detail_mask: missing dependency 'debandshit'")

    if clip.format is None:
        raise ValueError("detail_mask: 'Variable-format clips not supported'")

    den_a = core.knlm.KNLMeansCL(clip, d=2, a=3, h=pre_denoise, device_type='GPU') if pre_denoise is not None else clip
    den_b = core.knlm.KNLMeansCL(clip, d=2, a=3, h=pre_denoise/2, device_type='GPU') if pre_denoise is not None else clip

    mask_a = depth(get_y(den_a), 16) if clip.format.bits_per_sample < 32 else get_y(den_a)
    mask_a = rangemask(mask_a, rad=rad, radc=radc)
    mask_a = depth(mask_a, clip.format.bits_per_sample)
    mask_a = core.std.Binarize(mask_a, brz_a)

    mask_b = core.std.Prewitt(get_y(den_b))
    mask_b = core.std.Binarize(mask_b, brz_b)

    mask = core.std.Expr([mask_a, mask_b], 'x y max')
    mask = util.pick_removegrain(mask)(mask, 22)
    return util.pick_removegrain(mask)(mask, 11)
