from __future__ import annotations

import warnings
from functools import partial
from typing import Any, Sequence

import vapoursynth as vs
import vsdehalo
from vsexprtools import clamp, mod4
from vskernels import BSpline, Catrom
from vsrgtools import repair
from vsutil import get_depth, get_y

from .util import check_variable, scale_peak

core = vs.core


__all__ = [
    'masked_dha',
    # Deprecated
    'bidehalo',
    'fine_dehalo',
]


def bidehalo(clip: vs.VideoNode, ref: vs.VideoNode | None = None,
             sigmaS: float = 1.5, sigmaR: float = 5/255,
             sigmaS_final: float | None = None, sigmaR_final: float | None = None,
             planes: int | Sequence[int] | None = None,
             bilateral_args: dict[str, Any] = {},
             bm3d_args: dict[str, Any] = {},
             ) -> vs.VideoNode:
    """
    Dehaloing function that uses bilateral and BM3D to remove bright haloing around edges.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    If a ref clip is passed, that will be masked onto the clip instead of a blurred clip.

    :param clip:                Source clip.
    :param ref:                 Ref clip.
    :param sigmaS:              Bilateral's spatial weight sigma.
    :param sigmaR:              Bilateral's range weight sigma.
    :param sigmaS_final:        Final bilateral call's spatial weight sigma.
                                You'll want this to be much weaker than the initial `sigmaS`.
                                If `None`, 1/3rd of `sigmaS`.
    :param sigmaR_final:        Bilateral's range weight sigma.
                                if `None`, same as `sigmaR`
    :param bilateral_args:      Additional parameters to pass to bilateral.
    :param bm3d_args:           Additional parameters to pass to :py:func:`lvsfunc.noise.bm3d`.
    :param planes:              Specifies which planes will be processed.
                                Any unprocessed planes will be simply copied.

    :return:                    Dehalo'd clip.
    """

    warnings.warn('lvsfunc.bidehalo: deprecated in favor of vsdehalo.bidehalo!', DeprecationWarning)

    return vsdehalo.bidehalo(
        clip, sigmaS, sigmaR, sigmaS_final, sigmaR_final,
        planes=planes, bm3d_args=bm3d_args, bilateral_args=bilateral_args
    )


def masked_dha(clip: vs.VideoNode, ref: vs.VideoNode | None = None,
               rx: float = 2.0, ry: float = 2.0,
               brightstr: float = 1.0, darkstr: float = 0.0,
               lowsens: float = 50, highsens: float = 50, rfactor: float = 1.0,
               maskpull: float = 48, maskpush: float = 192, show_mask: bool = False) -> vs.VideoNode:
    """
    Bombines the best of DeHalo_alpha and BlindDeHalo3, and adds some tweaks to the masking.

    This function is rather sensitive to the rx and ry settings.
    Set them as low as possible! If the radii are set too high, it will start missing small spots.

    `darkstr` is set to 0 by default in this function. This is because more often than not,
    it simply does more damage than people will likely want.

    The sensitivity settings are rather difficult to define.
    In essence, they define the window between how weak an effect is for it to be processed,
    and how strong it has to be before it's fully discarded.

    Adopted from G41Fun, original by ``Orum <https://forum.doom9.org/showthread.php?t=148498>``.
    Heavily modified by LightArrowsEXE.

    :param clip:            Clip to process.
    :param ref:             Reference clip. Will replace regular dehaloing with the given clip.
    :param rx:              Horizontal radius for halo removal. Must be greater than 1.
    :param ry:              Vertical radius for halo removal. Must be greater than 1.
    :param brightstr:       Strength for bright halo removal.
    :param darkstr:         Strength for dark halo removal. Must be between 0 and 1.
    :param lowsens:         Lower sensitivity range. The lower this is, the more it will process.
                            Must be between 0 and 100.
    :param highsens:        Upper sensitivity range. The higher this is, the more it will process.
                            Must be between 0 and 100.
    :param rfactor:         Image enlargement factor. Set to >1 to enable some form of aliasing-protection.
                            Must be greater than 1.
    :param maskpull:        Mask pulling factor.
    :param maskpush:        Mask pushing factor.
    :param show_mask:       Return mask clip.

    :return:                Dehalo'd clip or halo mask clip.

    :raises ValueError:     ``rfactor``, ``rx``, or ``ry`` is less than 1.0.
    :raises ValueError:     ``darkstr`` is not between 0.0–1.0.
    :raises ValueError:     ``lowsens`` or ``highsens`` is not between 0–100.
    """
    assert check_variable(clip, "masked_dha")

    # Original silently changed values around, which I hate. Throwing errors instead.
    if not all(x >= 1 for x in (rfactor, rx, ry)):
        raise ValueError("masked_dha: 'rfactor, rx, and ry must all be bigger than 1.0!'")

    if not 0 <= darkstr <= 1:
        raise ValueError("masked_dha: 'darkstr must be between 0.0 and 1.0!'")

    if not all(0 < sens < 100 for sens in (lowsens, highsens)):
        raise ValueError("masked_dha: 'lowsens and highsens must be between 0 and 100!'")

    # These are the only two I'm going to keep, as these will still give expected results.
    maskpull = clamp(maskpull, max_val=254, min_val=0)
    maskpush = clamp(maskpush, max_val=255, min_val=maskpull + 1)

    peak_r = 1.0 if get_depth(clip) == 32 else 1 << get_depth(clip)
    peak = 1.0 if get_depth(clip) == 32 else peak_r - 1
    lowsens, maskpull, maskpush = map(partial(scale_peak, peak=peak), [lowsens, maskpull, maskpush])
    expr_i = f'y x - y 0.000001 + / {peak} * {lowsens} - y {peak_r} + {peak_r*2} / {highsens/100} + *'

    clip_y = get_y(clip)  # Should still work even if GRAY clip

    clip_ds = Catrom().scale(clip_y, mod4(clip.width/rx), mod4(clip.height/ry))
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
            ssc = repair(clip_y, mmg, 1)
        else:
            ss_w, ss_h = mod4(clip.width * rfactor, 4), mod4(clip.height * rfactor)
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
                show_mask: bool | int = False,
                planes: int | Sequence[int] | None = None) -> vs.VideoNode:
    """
    Light's rewrite of fine_dehalo.py.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

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

    :param clip:                    Clip to process.
    :param ref:                     Reference clip. Will replace regular dehaloing.
    :param rx:                      Horizontal radius for halo removal. Must be greater than 1. Will be rounded up.
    :param ry:                      Vertical radius for halo removal. Must be greater than 1. Will be rounded up.
    :param brightstr:               Strength for bright halo removal.
    :param darkstr:                 Strength for dark halo removal. Must be between 0 and 1.
    :param thmi:                    Minimum threshold for sharp edges. Keep only the sharpest edges (line edges).
                                    To see the effects of this setting take a look at the strong mask (show_mask=4).
    :param thma:                    Maximum threshold for sharp edges. Keep only the sharpest edges (line edges).
                                    To see the effects of this setting take a look at the strong mask (show_mask=4).
    :param thlimi:                  Minimum limiting threshold. Includes more edges than previously,
                                    but ignores simple details.
    :param thlima:                  Maximum limiting threshold. Includes more edges than previously,
                                    but ignores simple details.
    :param lowsens:                 Lower sensitivity range. The lower this is, the more it will process.
                                    Must be between 0 and 100.
    :param highsens:                Upper sensitivity range. The higher this is, the more it will process.
                                    Must be between 0 and 100.
    :param rfactor:                 Image enlargement factor. Set to >1 to enable some form of aliasing-protection.
                                    Must be greater than 1.
    :param show_mask:               Return mask clip. Valid options are 1–7.
    :param planes:                  Specifies which planes will be processed.
                                    Any unprocessed planes will be simply copied.

    :return:                        Dehalo'd clip or halo mask clip.

    :raises ModuleNotFoundError:    Dependencies are missing.
    """

    warnings.warn('lvsfunc.fine_dehalo: deprecated in favor of vsdehalo.fine_dehalo!', DeprecationWarning)

    return vsdehalo.fine_dehalo(
        clip, ref, rx, ry, darkstr, brightstr, int(lowsens), int(highsens),
        thmi, thma, thlimi, thlima, rfactor,
        planes=planes, show_mask=show_mask
    )
