"""
    Dehaloing functions and wrappers.
"""
import warnings
from functools import partial
from typing import Any, Dict, Optional

import vapoursynth as vs
from vsutil import depth, fallback, get_depth, get_y, iterate

from . import denoise, kernels
from .util import force_mod, pick_repair, scale_peak, clamp_values

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


def deemphasize(clip: vs.VideoNode, strength: int = 95,
                interlaced: bool = False, TFF: bool = True) -> vs.VideoNode:
    """
    A function that attempts to deemphasize ringing common to SD video signals
    resulting from a playback device in the transfer chain poorly compensating
    for pre-emphasis baked into the source signal.

    Ported and modified from an AVS gist: https://gist.github.com/acuozzo/940869257cc79016215600a2392b33eb.
    This was mainly ported as an exercise. Usefulness not guaranteed.

    WARNING: This function will be deprecated in lvsfunc 0.4.0!

    Dependencies:

    * fmtconv

    :param clip:        Source clip
    :param strength:    Gauss strength, lower is stronger. Ranged 1–100
    :param interlaced:  Whether the clip is interlaced or not
    :param TFF:         Top Field First if True, else Bottom Field First

    :return:            Deringed clip
    """
    warnings.warn("deemphasize: This function will no longer be supported in future versions. "
                  "Please make sure to update your older scripts. "
                  "This function will be removed in lvsfunc v0.4.0.", DeprecationWarning)

    if clip.format is None:
        raise ValueError("deemphasize: 'Variable-format clips not supported'")

    clip = clip.std.SeparateFields(tff=TFF) if interlaced else clip

    assert clip.format

    coords = [0, 1, 0, 0, 0, 0, 1, 0]
    mask = core.std.Sobel(clip)
    mask = iterate(mask, partial(core.std.Minimum, coordinates=coords), 3)
    mask = iterate(mask, partial(core.std.Maximum, coordinates=coords), 3)

    blurred = clip.fmtc.resample(clip.width-2, kernel='gauss', taps=4, a1=strength) \
        .resize.Spline64(clip.width, format=clip.format.id)
    merged = core.std.MaskedMerge(blurred, clip, mask)
    return merged.std.DoubleWeave().std.SelectEvery(2, 0) if interlaced else merged


# TO-DO: Add `ref` param that actually works...
def masked_dha(clip: vs.VideoNode, rx: float = 2.0, ry: float = 2.0,
               brightstr: float = 1.0, darkstr: float = 0.0,
               lowsens: float = 50, highsens: float = 50, rfactor: float = 1.0,
               maskpull: float = 48, maskpush: float = 192, show_mask: bool = False) -> vs.VideoNode:
    """
    A combination of the best of DeHalo_alpha and BlindDeHalo3, plus a few minor tweaks to the masking.

    This function is rather sensitive to the rx and ry settings.
    Set them as low as possible! If the radii are set too high, it will start missing small spots.

    `darkstr` is set to 0 by default in this function. This is because more often than not,
    it simply does more damage than people will likely want.

    The sensitivity settings are rather difficult to define.
    In essence, they define the window between how weak an effect is for it to be processed,
    and how strong it has to be before it's fully discarded.

    Adopted from G41Fun, original by `Orum <https://forum.doom9.org/showthread.php?t=148498>.
    Heavily modified by LightArrowsEXE.

    :param clip:            Input clip
    :param rx:              Horizontal radius for halo removal. Must be greater than 1.
    :param ry:              Vertical radius for halo removal. Must be greater than 1.
    :param brightstr:       Strength for bright halo removal
    :param darkstr:         Strength for dark halo removal. Must be between 0 and 1.
    :param lowsens:         Lower sensitivity range. The lower this is, the more it will process.
                            Must be between 0 and 100.
    :param highsens:        Upper sensitivity range. The higher this is, the more it will process.
                            Must be between 0 and 100.
    :param rfactor:         Image enlargment factor. Set to >1 to enable some form of aliasing-protection.
                            Must be greater than 1.
    :param maskpull:        Mask pulling factor
    :param maskpush:        Mask pushing factor
    :param show_mask:       Return mask clip

    :return:                Dehalo'd clip or halo mask clip
    """
    if clip.format is None:
        raise ValueError("masked_dha: 'Variable-format clips not supported'")

    # Original silently changed values around, which I hate. Throwing errors instead.
    if not all(x >= 1 for x in (rfactor, rx, ry)):
        raise ValueError("masked_dha: 'rfactor, rx, and ry must all be bigger than 1.0'")

    if not 0 <= darkstr <= 1:
        raise ValueError("masked_dha: 'darkstr must be between 1.0 and 0.0'")

    if not all(0 < sens < 100 for sens in (lowsens, highsens)):
        raise ValueError("masked_dha: 'lowsens and highsens must be between 0 and 100'")

    # These are the only two I'm going to keep, as these will still give expected results.
    maskpull = clamp_values(maskpull, max_val=254, min_val=0)
    maskpush = clamp_values(maskpush, max_val=255, min_val=maskpull + 1)

    peak_r = 1.0 if get_depth(clip) == 32 else 1 << get_depth(clip)
    peak = 1.0 if get_depth(clip) == 32 else peak_r - 1
    lowsens, maskpull, maskpush = map(partial(scale_peak, peak=peak), [lowsens, maskpull, maskpush])
    expr_i = f'y x - y 0.000001 + / {peak} * {lowsens} - y {peak_r} + {peak_r*2} / {highsens/100} + *'

    clip_y = get_y(clip)  # Should still work even if GRAY clip

    clip_ds = kernels.Catrom().scale(clip_y, force_mod(clip.width/rx, 4), force_mod(clip.height/ry, 4))
    clip_ss = kernels.BSpline().scale(clip_ds, clip.width, clip.height)

    chl = core.std.Expr([clip_y.std.Maximum(), clip_y.std.Minimum()], 'x y -')
    lhl = core.std.Expr([clip_ss.std.Maximum(), clip_ss.std.Minimum()], 'x y -')

    mask_i = core.std.Expr([chl, lhl], expr_i)
    mask_f = core.std.Expr([clip_ds.std.Maximum(), clip_ds.std.Minimum()], 'x y - 4 *').std.Convolution(matrix=[1]*9)
    mask_f = kernels.BSpline().scale(mask_f, clip.width, clip.height)
    mask_f = core.std.Expr(mask_f, f'{peak} {peak} {maskpull} - {peak} {maskpush} - - / x {maskpull} - *')

    if show_mask:
        return mask_f

    mmg = core.std.MaskedMerge(clip_ss, clip_y, mask_i)

    if rfactor == 1:
        ssc = pick_repair(clip)(clip_y, mmg, 1)
    else:
        ss_w, ss_h = force_mod(clip.width * rfactor, 4), force_mod(clip.height * rfactor, 4)
        ssc = kernels.Catrom().scale(clip_y, ss_w, ss_h)
        ssc = core.std.Expr([ssc, kernels.Catrom().scale(mmg.std.Maximum(), ss_w, ss_h)], 'x y min')
        ssc = core.std.Expr([ssc, kernels.Catrom().scale(mmg.std.Minimum(), ss_w, ss_h)], 'x y max')
        ssc = kernels.Catrom().scale(ssc, clip.width, clip.height)

    umfc = core.std.Expr([clip_y, ssc], f'x y < x dup y - {darkstr} * - x dup y - {brightstr} * - ?')
    mfc = core.std.MaskedMerge(clip_y, umfc, mask_f)
    return core.std.ShufflePlanes([mfc, clip], [0, 1, 2], vs.YUV) if not clip.format.id == vs.GRAY else mfc
