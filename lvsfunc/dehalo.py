from __future__ import annotations

import math
from functools import partial
from typing import Any, Dict, List

import vapoursynth as vs
from vsutil import depth, fallback, get_depth, get_y

from .noise import bm3d
from .kernels import BSpline, Catrom
from .mask import maxm, minm
from .types import Shapes
from .util import (check_variable, clamp_values, force_mod, pick_repair,
                   scale_peak)

core = vs.core


__all__: List[str] = [
    'bidehalo',
    'fine_dehalo',
    'masked_dha',
]


def bidehalo(clip: vs.VideoNode, ref: vs.VideoNode | None = None,
             sigmaS: float = 1.5, sigmaR: float = 5/255,
             sigmaS_final: float | None = None, sigmaR_final: float | None = None,
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
    :param bm3d_args:           Additional parameters to pass to :py:class:`lvsfunc.noise.bm3d`

    :return:                    Dehalo'd clip
    """
    bm3ddh_args: Dict[str, Any] = dict(sigma=8, radius=1, pre=clip)
    bm3ddh_args.update(bm3d_args)

    check_variable(clip, "bidehalo")
    assert clip.format

    sigmaS_final = fallback(sigmaS_final, sigmaS / 3)
    sigmaR_final = fallback(sigmaR_final, sigmaR)

    if ref is None:
        den = depth(bm3d(clip, **bm3ddh_args), 16)

        ref = den.bilateral.Bilateral(sigmaS=sigmaS, sigmaR=sigmaR, **bilateral_args)
        bidh = den.bilateral.Bilateral(ref=ref, sigmaS=sigmaS_final, sigmaR=sigmaR_final, **bilateral_args)
        bidh = depth(bidh, clip.format.bits_per_sample)
    else:
        bidh = depth(ref, clip.format.bits_per_sample)

    return core.std.Expr([clip, bidh], "x y min")


# TO-DO: Add `ref` param that actually works...
def masked_dha(clip: vs.VideoNode, ref: vs.VideoNode | None = None,
               rx: float = 2.0, ry: float = 2.0,
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

    Adopted from G41Fun, original by ``Orum <https://forum.doom9.org/showthread.php?t=148498>``.
    Heavily modified by LightArrowsEXE.

    :param clip:            Input clip
    :param ref:             Reference clip. Will replace regular dehaloing with the given clip.
    :param rx:              Horizontal radius for halo removal. Must be greater than 1.
    :param ry:              Vertical radius for halo removal. Must be greater than 1.
    :param brightstr:       Strength for bright halo removal
    :param darkstr:         Strength for dark halo removal. Must be between 0 and 1.
    :param lowsens:         Lower sensitivity range. The lower this is, the more it will process.
                            Must be between 0 and 100.
    :param highsens:        Upper sensitivity range. The higher this is, the more it will process.
                            Must be between 0 and 100.
    :param rfactor:         Image enlargement factor. Set to >1 to enable some form of aliasing-protection.
                            Must be greater than 1.
    :param maskpull:        Mask pulling factor
    :param maskpush:        Mask pushing factor
    :param show_mask:       Return mask clip

    :return:                Dehalo'd clip or halo mask clip
    """
    check_variable(clip, "masked_dha")
    assert clip.format

    # Original silently changed values around, which I hate. Throwing errors instead.
    if not all(x >= 1 for x in (rfactor, rx, ry)):
        raise ValueError("masked_dha: 'rfactor, rx, and ry must all be bigger than 1.0!'")

    if not 0 <= darkstr <= 1:
        raise ValueError("masked_dha: 'darkstr must be between 1.0 and 0.0!'")

    if not all(0 < sens < 100 for sens in (lowsens, highsens)):
        raise ValueError("masked_dha: 'lowsens and highsens must be between 0 and 100!'")

    # These are the only two I'm going to keep, as these will still give expected results.
    maskpull = clamp_values(maskpull, max_val=254, min_val=0)
    maskpush = clamp_values(maskpush, max_val=255, min_val=maskpull + 1)

    peak_r = 1.0 if get_depth(clip) == 32 else 1 << get_depth(clip)
    peak = 1.0 if get_depth(clip) == 32 else peak_r - 1
    lowsens, maskpull, maskpush = map(partial(scale_peak, peak=peak), [lowsens, maskpull, maskpush])
    expr_i = f'y x - y 0.000001 + / {peak} * {lowsens} - y {peak_r} + {peak_r*2} / {highsens/100} + *'

    clip_y = get_y(clip)  # Should still work even if GRAY clip

    clip_ds = Catrom().scale(clip_y, force_mod(clip.width/rx, 4), force_mod(clip.height/ry, 4))
    clip_ss = BSpline().scale(clip_ds, clip.width, clip.height)

    chl = core.std.Expr([clip_y.std.Maximum(), clip_y.std.Minimum()], 'x y -')
    lhl = core.std.Expr([clip_ss.std.Maximum(), clip_ss.std.Minimum()], 'x y -')

    mask_i = core.std.Expr([chl, lhl], expr_i)
    mask_f = core.std.Expr([clip_ds.std.Maximum(), clip_ds.std.Minimum()], 'x y - 4 *').std.Convolution(matrix=[1]*9)
    mask_f = BSpline().scale(mask_f, clip.width, clip.height)
    mask_f = core.std.Expr(mask_f, f'{peak} {peak} {maskpull} - {peak} {maskpush} - - / x {maskpull} - *')

    if show_mask:
        return mask_f

    if ref:
        umfc = get_y(ref)
    else:
        mmg = core.std.MaskedMerge(clip_ss, clip_y, mask_i.std.Limiter())

        if rfactor == 1:
            ssc = pick_repair(clip)(clip_y, mmg, 1)

        ss_w, ss_h = force_mod(clip.width * rfactor, 4), force_mod(clip.height * rfactor, 4)
        ssc = Catrom().scale(clip_y, ss_w, ss_h)
        ssc = core.std.Expr([ssc, Catrom().scale(mmg.std.Maximum(), ss_w, ss_h)], 'x y min')
        ssc = core.std.Expr([ssc, Catrom().scale(mmg.std.Minimum(), ss_w, ss_h)], 'x y max')
        ssc = Catrom().scale(ssc, clip.width, clip.height)

        umfc = core.std.Expr([clip_y, ssc], f'x y < x dup y - {darkstr} * - x dup y - {brightstr} * - ?')

    mfc = core.std.MaskedMerge(clip_y, umfc, mask_f)
    return core.std.ShufflePlanes([mfc, clip], [0, 1, 2], vs.YUV) \
        if clip.format.color_family != vs.GRAY else mfc


def fine_dehalo(clip: vs.VideoNode, ref: vs.VideoNode | None = None,
                rx: float = 1.8, ry: float = 1.8,
                brightstr: float = 1.0, darkstr: float = 0.0,
                thmi: float = 80, thma: float = 128, thlimi: float = 50, thlima: float = 100,
                lowsens: float = 50, highsens: float = 50, rfactor: float = 1.25,
                show_mask: bool | int = False) -> vs.VideoNode:
    """
    Slight rewrite of fine_dehalo.

    This is a slight rewrite of the standalone script that has been floating around
    with support for a ``ref`` clip. Original can be found in havsfunc if requested.

    There have been changes made to the way the masks are expanded/inpanded, as well as strengths.
    This isn't strictly better or worse than the original version, just different.

    This function is rather sensitive to the rx and ry settings.
    Set them as low as possible! If the radii are set too high, it will start missing small spots.

    `darkstr` is set to 0 by default in this function. This is because more often than not,
    it simply does more damage than people will likely want.

    The sensitivity settings are rather difficult to define.
    In essence, they define the window between how weak an effect is for it to be processed,
    and how strong it has to be before it's fully discarded.

    :param clip:            Input clip
    :param ref:             Reference clip. Will replace regular dehaloing.
    :param rx:              Horizontal radius for halo removal. Must be greater than 1.
    :param ry:              Vertical radius for halo removal. Must be greater than 1.
    :param brightstr:       Strength for bright halo removal
    :param darkstr:         Strength for dark halo removal. Must be between 0 and 1.
    :param thmi:            Minimum threshold for sharp edges. Keep only the sharpest edges (line edges).
                            To see the effects of this setting take a look at the strong mask (show_mask=4).
    :param thma:            Maximum threshold for sharp edges. Keep only the sharpest edges (line edges).
                            To see the effects of this setting take a look at the strong mask (show_mask=4).
    :param thlimi:          Minimum limiting threshold. Includes more edges than previously, but ignores simple details.
    :param thlima:          Maximum limiting threshold. Includes more edges than previously, but ignores simple details.
    :param lowsens:         Lower sensitivity range. The lower this is, the more it will process.
                            Must be between 0 and 100.
    :param highsens:        Upper sensitivity range. The higher this is, the more it will process.
                            Must be between 0 and 100.
    :param rfactor:         Image enlargement factor. Set to >1 to enable some form of aliasing-protection.
                            Must be greater than 1.
    :param show_mask:       Return mask clip.

    :return:                Dehalo'd clip or halo mask clip
    """
    try:
        from havsfunc import DeHalo_alpha
    except ModuleNotFoundError:
        raise ModuleNotFoundError("fine_dehalo: missing dependency `havsfunc`!'")

    check_variable(clip, "fine_dehalo")
    assert clip.format

    if ref:
        check_variable(ref, "fine_dehalo")
        assert ref.format

    # Original silently changed values around, which I hate. Throwing errors instead.
    if not all(x >= 1 for x in (rfactor, rx, ry)):
        raise ValueError("fine_dehalo: 'rfactor, rx, and ry must all be bigger than 1.0!'")

    if not 0 <= darkstr <= 1:
        raise ValueError("fine_dehalo: 'darkstr must be between 1.0 and 0.0!'")

    if not all(0 < sens < 100 for sens in (lowsens, highsens)):
        raise ValueError("fine_dehalo: 'lowsens and highsens must be between 0 and 100!'")

    if not 0 <= int(show_mask) < 7:
        raise ValueError("fine_dehalo: 'Valid values for show_mask are 0-7!'")

    bits = get_depth(clip)
    peak = (1 << bits) - 1
    smax = scale_peak(255, peak)
    thmi, thma, thlimi, thlima = map(partial(scale_peak, peak=peak), [thmi, thma, thlimi, thlima])

    rx_i, ry_i = int(math.ceil(rx)), int(round(ry))

    dehaloed = ref or DeHalo_alpha(clip, rx=rx, ry=ry, darkstr=darkstr, brightstr=brightstr,
                                   lowsens=lowsens, highsens=highsens, ss=rfactor)

    clip_y = get_y(clip)

    # Basic edge detection, thresholding will be applied later.
    edges = clip_y.std.Prewitt()

    # Keeps only the sharpest edges (line edges)
    strong = core.std.Expr(edges, f"x {thmi} - {thma-thmi} / {smax} *")

    # Extends them to include the potential halos
    large: vs.VideoNode = maxm(strong, rx_i, ry_i)[-1]

    # Includes more edges than previously, but ignores simple details
    light = core.std.Expr(edges, f"x {thlimi} - {thlima-thlimi} / {smax} *")

    # Growing the mask
    shrink = maxm(light, sw=rx_i, sh=ry_i, mode=Shapes.ELLIPSE)[-1]
    shrink = core.std.Expr(shrink, "x 2 *")
    shrink = minm(shrink, sw=rx_i, sh=rx_i, mode=Shapes.ELLIPSE)[-1]
    shrink = shrink.std.Convolution(matrix=[1] * 9).std.Convolution(matrix=[1] * 9)

    shr_med = core.std.Expr([strong, shrink], expr="x y max")

    mask = core.std.Expr([large, shr_med], expr="x y - 2 *")
    mask = core.std.Convolution(mask, matrix=[1] * 9)
    mask = core.std.Expr([mask], expr="x 2 *").std.Limiter()

    match show_mask:
        case 1: return mask
        case 2: return shrink
        case 3: return edges
        case 4: return strong
        case 5: return light
        case 6: return large
        case 7: return shr_med

    return core.std.MaskedMerge(clip, dehaloed, mask, planes=[0])
