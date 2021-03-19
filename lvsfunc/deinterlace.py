"""
    Functions to help with deinterlacing or deinterlaced content.
"""

from functools import partial
from typing import Any, Optional

import vapoursynth as vs

from . import util

core = vs.core


def deblend(clip: vs.VideoNode, rep: Optional[int] = None) -> vs.VideoNode:
    """
    A simple function to fix deblending for interlaced video with an AABBA blending pattern,
    where A is a regular frame and B is a blended frame.

    Assuming there's a constant pattern of frames (labeled A, B, C, CD, and DA in this function),
    blending can be fixed by calculating the D frame by getting halves of CD and DA, and using that
    to fix up CD. DA is then dropped because it's a duplicated frame.

    Doing this will result in some of the artifacting being added to the deblended frame,
    but we can mitigate that by repairing the frame with the non-blended frame before it.

    For more information, please refer to this blogpost by torchlight:
    https://mechaweaponsvidya.wordpress.com/2012/09/13/adventures-in-deblending/

    Dependencies: rgsf (optional: 32bit clip)

    :param clip:     Input clip
    :param rep:      Repair mode for the deblended frames, no repair if None (Default: None)

    :return:         Deblended clip
    """

    blends_a = range(2, clip.num_frames - 1, 5)
    blends_b = range(3, clip.num_frames - 1, 5)
    expr_cd = ["z a 2 / - y x 2 / - +"]

    def deblend(n: int, clip: vs.VideoNode, rep: Optional[int]
                ) -> vs.VideoNode:
        # Thanks Myaa, motbob and kageru!
        if n % 5 in [0, 1, 4]:
            return clip
        else:
            if n in blends_a:
                c, cd, da, a = clip[n - 1], clip[n], clip[n + 1], clip[n + 2]
                debl = core.std.Expr([c, cd, da, a], expr_cd)
                return util.pick_repair(clip)(debl, c, rep) if rep else debl
            return clip

    debl = core.std.FrameEval(clip, partial(deblend, clip=clip, rep=rep))
    return core.std.DeleteFrames(debl, blends_b).std.AssumeFPS(fpsnum=24000, fpsden=1001)


def decomb(clip: vs.VideoNode,
           TFF: bool,
           mode: int = 1,
           ref: Optional[vs.VideoNode] = None,
           decimate: bool = True,
           vinv: bool = False,
           sharpen: bool = False, dir: str = 'v',
           rep: Optional[int] = None,
           show_mask: bool = False,
           **kwargs: Any) -> vs.VideoNode:
    """
    A filter that performs relatively aggressive filtering to get rid of the combing on a interlaced/telecined source.
    Decimation can be disabled if the user wishes to decimate the clip themselves.
    Enabling vinverse will result in more aggressive decombing at the cost of potential detail loss.
    Sharpen will perform a directional unsharpening. Direction can be set using `dir`.
    A reference clip can be passed with `ref`, which will be used by VFM to create the output frames.

    Base function written by Midlifecrisis from the WEEB AUTISM server, and modified by LightArrowsEXE.

    Dependencies: combmask, havsfunc (QTGMC), rgsf (optional: 32bit clip)

    Deciphering havsfunc's dependencies is left as an exercise for the user.

    :param clip:          Input clip
    :param TFF:           Top-Field-First
    :param mode:          Sets the matching mode or strategy to use for VFM
    :param ref:           Reference clip for VFM's `clip2` parameter
    :param decimate:      Decimate the video after deinterlacing (Default: True)
    :param vinv:          Use vinverse to get rid of additional combing (Default: False)
    :param sharpen:       Unsharpen after deinterlacing (Default: False)
    :param dir:           Directional vector. 'v' = Vertical, 'h' = Horizontal (Default: v)
    :param rep:           Repair mode for repairing the decombed clip using the original clip (Default: None)
    :param show_mask:     Return combmask
    :param kwargs:        Arguments to pass to QTGMC
                          (Default: SourceMatch=3, Lossless=2, TR0=1, TR1=2, TR2=3, FPSDivisor=2)

    :return:              Decombed and optionally decimated clip
    """
    try:
        from havsfunc import QTGMC
    except ModuleNotFoundError:
        raise ModuleNotFoundError("decomb: missing dependency 'havsfunc'")

    qtgmc_args = dict(SourceMatch=3, Lossless=2, TR0=1, TR1=2, TR2=3, FPSDivisor=2)
    qtgmc_args.update(kwargs)

    VFM_TFF = int(TFF)

    def _pp(n: int, f: vs.VideoFrame, clip: vs.VideoNode, pp: vs.VideoNode
            ) -> vs.VideoNode:
        return pp if f.props._Combed == 1 else clip

    clip = core.vivtc.VFM(clip, order=VFM_TFF, mode=mode, clip2=ref) if ref is not None \
        else core.vivtc.VFM(clip, order=VFM_TFF, mode=1)

    combmask = core.comb.CombMask(clip, cthresh=1, mthresh=3)
    combmask = core.std.Maximum(combmask, threshold=250).std.Maximum(threshold=250) \
        .std.Maximum(threshold=250).std.Maximum(threshold=250)
    combmask = core.std.BoxBlur(combmask, hradius=2, vradius=2)

    if show_mask:
        return combmask

    qtgmc = QTGMC(clip, TFF=TFF, **qtgmc_args)
    qtgmc_merged = core.std.MaskedMerge(clip, qtgmc, combmask, first_plane=True)

    decombed = core.std.FrameEval(clip, partial(_pp, clip=clip, pp=qtgmc_merged), clip)

    decombed = decombed.vinverse.Vinverse() if vinv else decombed
    decombed = dir_unsharp(decombed, dir=dir) if sharpen else decombed
    decombed = util.pick_repair(clip)(decombed, clip, rep) if rep else decombed
    return core.vivtc.VDecimate(decombed) if decimate else decombed


def dir_deshimmer(clip: vs.VideoNode, TFF: bool = True,
                  dh: bool = False,
                  transpose: bool = True,
                  show_mask: bool = False) -> vs.VideoNode:
    """
    Directional deshimmering function.

    Only works (in the few instances it does, anyway) for obvious horizontal and vertical shimmering.
    Odds of success are low. But if you're desperate, it's worth a shot.

    Dependencies: vapoursynth-nnedi3

    :param clip:         Input clip
    :param TFF:          Top Field First. Set to False if TFF doesn't work (Default: True)
    :param dh:           Interpolate to double the height of given clip beforehand (Default: False)
    :param transpose:    Transpose the clip before attempting to deshimmer (Default: True)
    :param show_mask:    Show nnedi3's mask (Default: False)

    :return:             Deshimmered clip
    """
    clip = core.std.Transpose(clip) if transpose else clip
    deshim = core.nnedi3.nnedi3(clip, field=TFF, dh=dh, show_mask=show_mask)
    return core.std.Transpose(deshim) if transpose else deshim


def dir_unsharp(clip: vs.VideoNode,
                strength: float = 1.0,
                dir: str = 'v',
                h: float = 3.4) -> vs.VideoNode:
    """
    Diff'd directional unsharpening function.
    Performs one-dimensional sharpening as such: "Original + (Original - blurred) * Strength"

    This particular function is recommended for SD content, specifically after deinterlacing.

    Special thanks to thebombzen and kageru for writing the bulk of this.

    Dependencies: knlmeanscl

    :param clip:            Input clip
    :param strength:        Amount to multiply blurred clip with original clip by (Default: 1.0)
    :param dir:             Directional vector. 'v' = Vertical, 'h' = Horizontal (Default: v)
    :param h:               Sigma for knlmeans, to prevent noise from getting sharpened (Default: 3.4)

    :return:                Unsharpened clip
    """

    dir = dir.lower()
    if dir not in ['v', 'h']:
        raise ValueError("dir_unsharp: '\"dir\" must be either \"v\" or \"h\"'")

    den = core.knlm.KNLMeansCL(clip, d=3, a=3, h=h)
    diff = core.std.MakeDiff(clip, den)

    blur_matrix = [1, 2, 1]
    blurred_clip = core.std.Convolution(den, matrix=blur_matrix, mode=dir)
    unsharp = core.std.Expr(clips=[den, blurred_clip], expr=['x y - ' + str(strength) + ' * x +', "", ""])
    return core.std.MergeDiff(unsharp, diff)
