"""
    Deinterlacing, IVTC, and post-deinterlacing functions and wrappers.
"""

import os
import time
import warnings
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import vapoursynth as vs
from vsutil import Dither, depth, get_depth, get_w, get_y

from .kernels import Catrom, Kernel
from .render import get_render_progress
from .util import get_prop, pick_repair

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
              decimate: Union[int, bool] = True,
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
    :param decimate:            Perform TDecimate on the clip if true, else returns TFM'd clip only.
                                Set to -1 to use TDecimate without TFM
    :param tfm_args:            Additional arguments to pass to TFM
    :param tdecimate_args:      Additional arguments to pass to TDecimate

    :return:                    IVTC'd VFR clip
    """
    if int(decimate) not in (-1, 0, 1):
        raise ValueError("TIVTC_VFR: 'Invalid `decimate` argument. Must be True/False, their integer values, or -1'")

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

        time.sleep(0.5)  # Allow it to properly finish writing logs
        del ivtc_clip  # Releases the clip, and in turn the filter (prevents an error)

    tfm_args = {**tfm_args, 'input': str(tfm_in)}

    tdecimate_args = {
        'mode': 5, 'hybrid': 2, 'vfrDec': 1, **tdecimate_args,
        'input': str(tdec_in), 'tfmIn': str(tfm_in), 'mkvOut': str(timecodes_out),
    }

    tfm = clip.tivtc.TFM(**tfm_args) if not decimate == -1 else clip
    return tfm.tivtc.TDecimate(**tdecimate_args) if not int(decimate) == 0 else tfm


def deblend(clip: vs.VideoNode, start: int = 0,
            rep: Optional[int] = None, decimate: bool = True) -> vs.VideoNode:
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

    :param clip:        Input clip
    :param start:       First frame of the pattern (Default: 0)
    :param rep:         Repair mode for the deblended frames, no repair if None (Default: None)
    :param decimate:    Decimate the video after deblending (Default: True)

    :return:            Deblended clip
    """

    blends_a = range(start + 2, clip.num_frames - 1, 5)
    blends_b = range(start + 3, clip.num_frames - 1, 5)
    expr_cd = ["z a 2 / - y x 2 / - +"]

    def deblend(n: int, clip: vs.VideoNode, rep: Optional[int]) -> vs.VideoNode:
        # Thanks Myaa, motbob and kageru!
        if n % 5 in [0, 1, 4]:
            return clip
        else:
            if n in blends_a:
                c, cd, da, a = clip[n - 1], clip[n], clip[n + 1], clip[n + 2]
                debl = core.std.Expr([c, cd, da, a], expr_cd)
                return pick_repair(clip)(debl, c, rep) if rep else debl
            return clip

    debl = core.std.FrameEval(clip, partial(deblend, clip=clip, rep=rep))
    return core.std.DeleteFrames(debl, blends_b).std.AssumeFPS(fpsnum=24000, fpsden=1001) \
        if decimate else debl


def decomb(clip: vs.VideoNode,
           TFF: Union[bool, int] = True, mode: int = 1,
           decimate: bool = True, vinv: bool = False,
           rep: Optional[int] = None, show_mask: bool = False,
           tfm_args: Dict[str, Any] = {},
           tdec_args: Dict[str, Any] = {},
           qtgmc_args: Dict[str, Any] = {}) -> vs.VideoNode:
    """
    A filter that performs relatively aggressive filtering to get rid of the combing on a interlaced/telecined source.
    Decimation can be disabled if the user wishes to decimate the clip themselves.

    Enabling vinverse will result in more aggressive decombing at the cost of potential detail loss.
    Sharpen will perform a directional unsharpening. Direction can be set using `dir`.
    A reference clip can be passed with `ref`, which will be used by TFM to create the output frames.

    Base function written by Midlifecrisis from the WEEB AUTISM server, and modified by LightArrowsEXE.

    Dependencies:

    * combmask
    * havsfunc
    * RGSF (optional: 32 bit clip)

    :param clip:          Input clip
    :param TFF:           Top-Field-First
    :param mode:          Sets the matching mode or strategy to use for TFM
    :param decimate:      Decimate the video after deinterlacing (Default: True)
    :param vinv:          Use vinverse to get rid of additional combing (Default: False)
    :param sharpen:       Unsharpen after deinterlacing (Default: False)
    :param dir:           Directional vector. 'v' = Vertical, 'h' = Horizontal (Default: v)
    :param rep:           Repair mode for repairing the decombed clip using the original clip (Default: None)
    :param show_mask:     Return combmask
    :param tfm_args:      Arguments to pass to TFM
    :param qtgmc_args:    Arguments to pass to QTGMC

    :return:              Decombed and optionally decimated clip
    """
    try:
        from havsfunc import QTGMC, Vinverse
    except ModuleNotFoundError:
        raise ModuleNotFoundError("decomb: missing dependency 'havsfunc'")

    VFM_TFF = int(TFF)

    tfm_kwargs: Dict[str, Any] = dict(order=VFM_TFF, mode=mode, chroma=True)
    tfm_kwargs |= tfm_args  # chroma set to True by default to match VFM

    qtgmc_kwargs: Dict[str, Any] = dict(SourceMatch=3, Lossless=2, TR0=1, TR1=2, TR2=3, FPSDivisor=2, TFF=TFF)
    qtgmc_kwargs |= qtgmc_args

    def _pp(n: int, f: vs.VideoFrame, clip: vs.VideoNode, pp: vs.VideoNode) -> vs.VideoNode:
        return pp if get_prop(f, '_Combed', int) == 1 else clip

    clip = core.tivtc.TFM(clip, **tfm_kwargs)

    combmask = core.comb.CombMask(clip, cthresh=1, mthresh=3)
    combmask = core.std.Maximum(combmask, threshold=250).std.Maximum(threshold=250) \
        .std.Maximum(threshold=250).std.Maximum(threshold=250)
    combmask = core.std.BoxBlur(combmask, hradius=2, vradius=2)

    if show_mask:
        return combmask

    qtgmc = QTGMC(clip, **qtgmc_kwargs)
    qtgmc_merged = core.std.MaskedMerge(clip, qtgmc, combmask, first_plane=True)

    decombed = core.std.FrameEval(clip, partial(_pp, clip=clip, pp=qtgmc_merged), clip)

    decombed = Vinverse(decombed) if vinv else decombed
    decombed = pick_repair(clip)(decombed, clip, rep) if rep else decombed
    return core.tivtc.TDecimate(decombed, **tdec_args) if decimate else decombed


def descale_fields(clip: vs.VideoNode, tff: bool = True,
                   width: Optional[int] = None, height: int = 720,
                   kernel: Kernel = Catrom(), src_top: float = 0.0) -> vs.VideoNode:
    """
    Simple descaling wrapper for interwoven upscaled fields.
    This function also sets a frameprop with the kernel that was used.

    The kernel is set using an lvsfunc.Kernel object.
    You can call these by doing for example ``kernel=lvf.kernels.Bilinear()``.
    You can also set specific values manually. For example: ``kernel=lvf.kernels.Bicubic(b=0, c=1)``.
    For more information, check the documentation on Kernels.

    ``src_top`` allows you to to shift the clip prior to descaling.
    This may be useful, as sometimes clips are shifted before or after the original upscaling.

    :param clip:        Input clip
    :param tff:         Top-field-first. `False` sets it to Bottom-Field-First
    :param width:       Native width. Will be automatically determined if set to `None`
    :param height:      Native height. Will be divided by two internally
    :param kernel:      lvsfunc.Kernel object (default: Catrom)
    :param src_top:     Shifts the clip vertically during the descaling

    :return:            Descaled GRAY clip
    """
    height_field = int(height/2)
    width = width or get_w(height, clip.width/clip.height)

    clip = clip.std.SetFieldBased(2-int(tff))

    sep = core.std.SeparateFields(get_y(clip))
    descaled = kernel.descale(sep, width, height_field, (src_top, 0))
    weave_y = core.std.DoubleWeave(descaled)
    weave_y = weave_y.std.SetFrameProp('scaler', data=f'{kernel.__name__} (Fields)')  # type: ignore[attr-defined]
    return weave_y.std.SetFieldBased(0)[::2]


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


def fix_telecined_fades(clip: vs.VideoNode, tff: Optional[Union[bool, int]] = None,
                        thr: float = 2.2) -> vs.VideoNode:
    """
    A filter that gives a mathematically perfect solution to fades made *after* telecining
    (which made perfect IVTC impossible). This is an improved version of the Fix-Telecined-Fades plugin
    that deals with overshoot/undershoot by adding a check.

    Make sure to run this *after* IVTC/deinterlacing!

    If the value surpases thr * original value, it will not affect any pixels in that frame
    to avoid it damaging frames it shouldn't need to. This helps a lot with orphan fields as well,
    which would otherwise create massive swings in values, sometimes messing up the fade fixing.

    If you pass your own float clip, you'll want to make sure to properly dither it down after.
    If you don't do this, you'll run into some serious issues!

    Taken from this gist and modified by LightArrowsEXE.
    <https://gist.github.com/blackpilling/bf22846bfaa870a57ad77925c3524eb1>

    :param clip:        Input clip
    :param tff:         Top-field-first. `False` sets it to Bottom-Field-First.
                        If None, get the field order from the _FieldBased prop.
    :param thr:         Threshold for when a field should be adjusted.
                        Default is 2.2, which appears to be a safe value that doesn't
                        cause it to do weird stuff with orphan fields.

    :return:            Clip with only fades fixed

    """
    def _ftf(n: int, f: List[vs.VideoFrame]) -> vs.VideoNode:
        avg = (get_prop(f[0], 'PlaneStatsAverage', float),
               get_prop(f[1], 'PlaneStatsAverage', float))

        if avg[0] != avg[1]:
            mean = sum(avg) / 2
            fixed = (sep[0].std.Expr(f"x {mean} {avg[0]} / dup 2.2 <= swap 1 ? *"),
                     sep[1].std.Expr(f"x {mean} {avg[1]} / *"))
        else:
            fixed = sep

        return core.std.Interleave(fixed).std.DoubleWeave()[::2]

    # I want to catch this before it reaches SeperateFields and give newer users a more useful error
    if get_prop(clip.get_frame(0), '_FieldBased', int) == 0 and tff is None:
        raise vs.Error("fix_telecined_fades: 'You must set `tff` for this clip!'")
    elif isinstance(tff, (bool, int)):
        clip = clip.std.SetFieldBased(int(tff) + 1)

    clip32 = depth(clip, 32).std.Limiter()
    bits = get_depth(clip)

    sep = clip32.std.SeparateFields().std.PlaneStats()
    sep = sep[::2], sep[1::2]  # type: ignore # I know this isn't good, but frameeval breaks otherwise
    ftf = core.std.FrameEval(clip32, _ftf, sep)  # and I don't know how or why

    if bits == 32:
        warnings.warn("fix_telecined_fades: 'Make sure to dither down BEFORE setting the FieldBased prop to 0! "
                      "Not doing this MAY return some of the combing!'")
    else:
        ftf = depth(ftf, bits, dither_type=Dither.ERROR_DIFFUSION)
        ftf = ftf.std.SetFieldBased(0)

    return ftf
