"""
    Wrappers and masks for denoising.
"""
import havsfunc as haf
import mvsfunc as mvf
from vsutil import join, split
from typing import Optional

import vapoursynth as vs

core = vs.core


def quick_denoise(clip: vs.VideoNode,
                  ref: vs.VideoNode = Optional[None],
                  cmode: str = 'knlm',
                  sigma: float = 2,
                  **kwargs) -> vs.VideoNode:
    """
    This wrapper is used to denoise both the luma and chroma using various denoisers of your choosing.
    If you wish to use just one denoiser,
    you're probably better off using that specific filter rather than this wrapper.

    A rewrite of my old 'quick_denoise'. I still hate it, but whatever.
    This will probably be removed in a future commit.

    BM3D is used for denoising the luma.

    Special thanks to kageru for helping me out with some ideas and pointers.

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
            planes[1] = planes[1].dfttest.DFTTest(sosize=kwargs['sbsize'] * 0.75, **kwargs)
            planes[2] = planes[2].dfttest.DFTTest(sosize=kwargs['sbsize'] * 0.75, **kwargs)
        except KeyError:
            raise ValueError(f"denoise: '\"sbsize\" not specified'")
    elif cmode in [4, 'smd', 'smdegrain']:
        planes[1] = haf.SMDegrain(planes[1], prefilter=3, **kwargs)
        planes[2] = haf.SMDegrain(planes[2], prefilter=3, **kwargs)
    else:
        raise ValueError(f"denoise: 'Unknown cmode'")

    planes[0] = mvf.BM3D(planes[0], sigma=sigma, psample=0, radius1=1, ref=ref)
    return join(planes)
