"""
    Wrappers for dehaloing functions.
"""
from typing import Any, Dict, Optional

import vapoursynth as vs
from vsutil import depth, fallback

from . import denoise

core = vs.core


def bidehalo(clip: vs.VideoNode, ref: Optional[vs.VideoNode] = None,
             sigmaS: float = 1.5, sigmaR: float = 5/255,
             sigmaS_final: Optional[float] = None, sigmaR_final: Optional[float] = None,
             bilateral_args: Dict[str, Any] = {},
             bm3d_args: Dict[str, Any] = {},
             ) -> vs.VideoNode:
    """
    A simple dehaloing function using bilateral and BM3D to remove bright haloing around edges.
    If a ref clip is passed, that will be masked onto the clip instead of a blurred clip.

    :param clip:                Source clip
    :param ref:                 Ref clip
    :param sigmaS:              Bilateral's spatial weight sigma
    :param sigmaR:              Bilateral's range weight sigma
    :param sigmaS_final:        Final bilateral call's spatial weight sigma.
                                You'll want this to be much weaker than the initial `sigmaS`.
                                If `None`, 1/3rd of `sigmaS`.
    :param sigmaR_final:        Bilateral's range weight sigma.
                                if `None`, same as `sigmaR`
    :param bilateral_args:      Additional parameters to pass to bilateral
    :param bm3d_args:           Additional parameters to pass to :py:class:`lvsfunc.denoise.bm3d`

    :return:                    Dehalo'd clip
    """
    bm3ddh_args: Dict[str, Any] = dict(sigma=8, radius=1, pre=clip)
    bm3ddh_args.update(bm3d_args)

    if clip.format is None:
        raise ValueError("bidehalo: 'Variable-format clips not supported'")

    sigmaS_final = fallback(sigmaS_final, sigmaS / 3)
    sigmaR_final = fallback(sigmaR_final, sigmaR)

    if ref is None:
        den = depth(denoise.bm3d(clip, **bm3ddh_args), 16)

        ref = den.bilateral.Bilateral(sigmaS=sigmaS, sigmaR=sigmaR, **bilateral_args)
        bidh = den.bilateral.Bilateral(ref=ref, sigmaS=sigmaS_final, sigmaR=sigmaR_final, **bilateral_args)
        bidh = depth(bidh, clip.format.bits_per_sample)
    else:
        bidh = depth(ref, clip.format.bits_per_sample)

    restore_dark = core.std.Expr([clip, bidh], "x y < x y ?")
    return restore_dark
