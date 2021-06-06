"""
    Wrappers for dehaloing functions.
"""
from typing import Any, Dict, Optional

import vapoursynth as vs
from vsutil import depth

from . import denoise

core = vs.core


def bidehalo(clip: vs.VideoNode, ref: Optional[vs.VideoNode] = None,
             sigmaS: float = 1.5, sigmaR: float = 5/255,
             bilateral_args: Dict[str, Any] = {},
             bm3d_args: Dict[str, Any] = {},
             ) -> vs.VideoNode:
    """
    A simple dehaloing function using bilateral and BM3D to remove bright haloing around edges.
    If a ref clip is passed, that will be masked onto the clip instead of a blurred clip.

    :param clip:                Source clip
    :param ref:                 Ref clip
    :param sigmaS:              Bilateral's spatial weight sigma
    :param sigmaS:              Bilateral's range weight sigma
    :param bilateral_args:      Additional parameters to pass to bilateral
    :param bm3d_args:           Additional parameters to pass to denoise.bm3d

    :return:                    Dehalo'd clip
    """
    bm3ddh_args: Dict[str, Any] = dict(sigma=8, radius=1, pre=clip)
    bm3ddh_args.update(bm3d_args)

    if clip.format is None:
        raise ValueError("lfdeband: 'Variable-format clips not supported'")

    if ref is None:
        bm3ddh = depth(denoise.bm3d(clip, **bm3ddh_args), 16)
        bidh_ref = core.bilateral.Bilateral(bm3ddh, sigmaS=sigmaS, sigmaR=sigmaR, **bilateral_args)
        bidh = core.bilateral.Bilateral(bm3ddh, ref=bidh_ref, sigmaS=sigmaS, sigmaR=sigmaR, **bilateral_args)
        bidh = depth(bidh, clip.format.bits_per_sample)
    else:
        bidh = depth(ref, clip.format.bits_per_sample)

    restore_dark = core.std.Expr([clip, bidh], "x y < x y ?")
    return restore_dark
