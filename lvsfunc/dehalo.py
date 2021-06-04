"""
    Wrappers for dehaloing functions.
"""
from typing import Any, Dict, Optional

import vapoursynth as vs
from vsutil import depth

from . import denoise, mask

core = vs.core


def bidehalo(clip: vs.VideoNode, ref: Optional[vs.VideoNode] = None,
             sigmaS: float = 1.5, sigmaR: float = 5/255,
             bilateral_args: Dict[str, Any] = {},
             mask_args: Dict[str, Any] = {},
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
    :param mask_args:           Additional parameters to pass to mask.halo_mask
    :param bm3d_args:           Additional parameters to pass to denoise.bm3d

    :return:                    Dehalo'd clip
    """
    bm3ddh_args: Dict[str, Any] = dict(sigma=8, radius=1, pre=clip)
    bm3ddh_args.update(bm3d_args)

    if clip.format is None:
        raise ValueError("lfdeband: 'Variable-format clips not supported'")

    bits = clip.format.bits_per_sample
    clip = depth(clip, 16)

    if ref is None:
        bm3ddh = denoise.bm3d(clip, **bm3ddh_args)
        bidh_ref = core.bilateral.Bilateral(bm3ddh, sigmaS=sigmaS, sigmaR=sigmaR, **bilateral_args)
        bidh = core.bilateral.Bilateral(bm3ddh, ref=bidh_ref, sigmaS=sigmaS, sigmaR=sigmaR, **bilateral_args)
    else:
        bidh = depth(ref, 16)

    halo_mask = mask.halo_mask(clip, **mask_args)
    dehalo = core.std.MaskedMerge(clip, bidh, halo_mask)

    restore_dark = core.std.Expr([clip, dehalo], "x y < x y ?")
    return depth(restore_dark, bits) if bits != 16 else restore_dark
