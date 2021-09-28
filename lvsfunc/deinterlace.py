"""
    Functions to help with deinterlacing or deinterlaced content.
"""

import os
import time
import warnings
from functools import partial
from pathlib import Path
from typing import Any, Dict, Optional, Union

import vapoursynth as vs

from . import util
from .render import get_render_progress

core = vs.core


def SIVTC(clip: vs.VideoNode, pattern: int = 0,
          TFF: bool = True, decimate: bool = True) -> vs.VideoNode:
    """
    A very simple fieldmatching function.

    This is essentially a stripped-down JIVTC offering JUST the basic fieldmatching and decimation part.
    As such, you may need to combine multiple instances if patterns change throughout the clip.

    :param clip:        Input clip
    :param pattern:     First frame of any clean-combed-combed-clean-clean sequence
    :param TFF:         Top-Field-First
    :param decimate:    Drop a frame every 5 frames to get down to 24000/1001

    :return:            IVTC'd clip
    """
    pattern = pattern % 5

    defivtc = core.std.SeparateFields(clip, tff=TFF).std.DoubleWeave()
    selectlist = [[0, 3, 6, 8], [0, 2, 5, 8], [0, 2, 4, 7], [2, 4, 6, 9], [1, 4, 6, 8]]
    dec = core.std.SelectEvery(defivtc, 10, selectlist[pattern]) if decimate else defivtc
    return core.std.SetFrameProp(dec, prop='_FieldBased', intval=0) \
        .std.SetFrameProp(prop='SIVTC_pattern', intval=pattern)


def TIVTC_VFR(clip: vs.VideoNode,
              tfm_in: Union[Path, str] = ".ivtc/matches.txt",
              tdec_in: Union[Path, str] = ".ivtc/metrics.txt",
              timecodes_out: Union[Path, str] = ".ivtc/timecodes.txt",
              tfm_args: Dict[str, Any] = {},
              tdecimate_args: Dict[str, Any] = {}) -> vs.VideoNode:
    """
    Wrapper for performing TFM and TDecimate on a clip that is supposed to be VFR,
    including generating a metrics/matches/timecodes txt file.

    Largely based on, if not basically rewritten from, atomchtools.TIVTC_VFR.

    Dependencies:

    * TIVTC

    :param clip:                Input clip
    :param tfmIn:               File location for TFM's matches analysis
    :param tdecIn:              File location for TDecimate's metrics analysis
    :param mkvOut:              File location for TDecimate's timecode file output
    :param tfm_args:            Additional arguments to pass to TFM
    :param tdecimate_args:      Additional arguments to pass to TDecimate

    :return:                    IVTC'd VFR clip
    """
    tfm_in = Path(tfm_in).resolve()
    tdec_in = Path(tdec_in).resolve()
    timecodes_out = Path(timecodes_out).resolve()

    # TIVTC can't write files into directories that don't exist
    for p in (tfm_in, tdec_in, timecodes_out):
        if not p.parent.exists():
            p.parent.mkdir(parents=True)

    if not (tfm_in.exists() and tdec_in.exists()):
        tfm_analysis: Dict[str, Any] = {**tfm_args, 'output': str(tfm_in)}
        tdec_analysis: Dict[str, Any] = {**tdecimate_args, 'output': str(tdec_in), 'mode': 4}

        ivtc_clip = core.tivtc.TFM(clip, **tfm_analysis).tivtc.TDecimate(**tdec_analysis)

        with get_render_progress() as pr:
            task = pr.add_task("Analyzing frames...", total=ivtc_clip.num_frames)

            def _cb(n: int, total: int) -> None:
                pr.update(task, advance=1)

            with open(os.devnull, 'wb') as dn:
                ivtc_clip.output(dn, progress_update=_cb)

        # Allow it to properly finish writing the logs
        time.sleep(0.5)
        del ivtc_clip  # Releases the clip, and in turn the filter (prevents it from erroring out)

    tfm_args = {**tfm_args, 'input': str(tfm_in)}

    tdecimate_args = {
        'mode': 5, **tdecimate_args,
        'input': str(tdec_in), 'tfmIn': str(tfm_in), 'mkvOut': str(timecodes_out),
        'hybrid': 2, 'vfrDec': 1
    }

    return clip.tivtc.TFM(**tfm_args).tivtc.TDecimate(**tdecimate_args)


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

    Dependencies:

    * RGSF (optional: 32 bit clip)

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

    Dependencies:

    * combmask
    * havsfunc
    * RGSF (optional: 32 bit clip)

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

    WARNING: This function will be deprecated in lvsfunc 0.4.0!

    Dependencies:

    * vapoursynth-nnedi3

    :param clip:         Input clip
    :param TFF:          Top Field First. Set to False if TFF doesn't work (Default: True)
    :param dh:           Interpolate to double the height of given clip beforehand (Default: False)
    :param transpose:    Transpose the clip before attempting to deshimmer (Default: True)
    :param show_mask:    Show nnedi3's mask (Default: False)

    :return:             Deshimmered clip
    """
    warnings.warn("dir_deshimmer: This function will no longer be supported in future versions. "
                  "Please make sure to update your older scripts. "
                  "This function will be removed in lvsfunc v0.4.0.", DeprecationWarning)

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

    WARNING: This function may be rewritten in the future, and functionality may change!

    Dependencies:

    * knlmeanscl

    :param clip:            Input clip
    :param strength:        Amount to multiply blurred clip with original clip by (Default: 1.0)
    :param dir:             Directional vector. 'v' = Vertical, 'h' = Horizontal (Default: v)
    :param h:               Sigma for knlmeans, to prevent noise from getting sharpened (Default: 3.4)

    :return:                Unsharpened clip
    """
    warnings.warn("dir_unsharp: This function's functionality will change in a future version, "
                  "and will likely be renamed. Please make sure to update your older scripts once it does.",
                  FutureWarning)

    dir = dir.lower()
    if dir not in ['v', 'h']:
        raise ValueError("dir_unsharp: '\"dir\" must be either \"v\" or \"h\"'")

    den = core.knlm.KNLMeansCL(clip, d=3, a=3, h=h)
    diff = core.std.MakeDiff(clip, den)

    blur_matrix = [1, 2, 1]
    blurred_clip = core.std.Convolution(den, matrix=blur_matrix, mode=dir)
    unsharp = core.std.Expr(clips=[den, blurred_clip], expr=['x y - ' + str(strength) + ' * x +', "", ""])
    return core.std.MergeDiff(unsharp, diff)
