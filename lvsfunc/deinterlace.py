"""
    Deinterlacing, IVTC, and post-deinterlacing functions and wrappers.
"""

from __future__ import annotations

import warnings
from fractions import Fraction
from functools import partial
from pathlib import Path
from typing import Any, Dict, List

import vapoursynth as vs
from vsutil import (Dither, depth, disallow_variable_format,
                    disallow_variable_resolution, get_depth, get_w, get_y,
                    scale_value)

from .comparison import Direction, Stack
from .kernels import BicubicDidee, Catrom, Kernel
from .render import get_render_progress
from .util import force_mod, get_neutral_value, get_prop, pick_repair

core = vs.core


def SIVTC(clip: vs.VideoNode, pattern: int = 0,
          tff: bool = True, decimate: bool = True) -> vs.VideoNode:
    """
    A very simple fieldmatching function.

    This is essentially a stripped-down JIVTC offering JUST the basic fieldmatching and decimation part.
    As such, you may need to combine multiple instances if patterns change throughout the clip.

    :param clip:        Input clip
    :param pattern:     First frame of any clean-combed-combed-clean-clean sequence
    :param tff:         Top-Field-First
    :param decimate:    Drop a frame every 5 frames to get down to 24000/1001

    :return:            IVTC'd clip
    """
    pattern = pattern % 5

    defivtc = core.std.SeparateFields(clip, tff=tff).std.DoubleWeave()
    selectlist = [[0, 3, 6, 8], [0, 2, 5, 8], [0, 2, 4, 7], [2, 4, 6, 9], [1, 4, 6, 8]]
    dec = core.std.SelectEvery(defivtc, 10, selectlist[pattern]) if decimate else defivtc
    return dec.std.SetFieldBased(0).std.SetFrameProp(prop='SIVTC_pattern', intval=pattern)


def seek_cycle(clip: vs.VideoNode, write_props: bool = True, scale: int = -1) -> vs.VideoNode:
    """
    Purely visual tool to view telecining cycles. This is purely a visual tool!
    This function has no matching parameters, just use wobbly instead if you need that.

    Displays the current frame, two previous and two future frames,
    as well as whether they are combed or not.

    P indicates a progressive frame, C a combed frame.

    Dependencies:

    * VapourSynth-TDeintMod

    :param clip:            Input clip
    :param write_props:     Write props on frames. Disabling this will also speed up the function.
    :param scale:           Integer scaling of all clips. Must be to the power of 2.

    :return:                Viewing UI for standard telecining cycles
    """
    if not (scale & (scale-1) == 0) and scale != 0 and scale != -1:
        raise ValueError("seek_cycle: 'scale must be a value that is the power of 2!'")

    # TODO: 60i checks and flags somehow? false positives gonna be a pain though
    def check_combed(n: int, f: vs.VideoFrame, clip: vs.VideoNode) -> vs.VideoNode:
        return clip.text.Text("C" if get_prop(f, "_Combed", int) else "P", 7)

    # Scaling of the main clip
    scale = 1 if scale == -1 else 2 ** scale

    height = clip.height * scale
    width = get_w(height, clip.width/clip.height)

    clip = clip.tdm.IsCombed()
    clip = Catrom().scale(clip, width, height)

    # Downscaling for the cycle clips
    clip_down = BicubicDidee().scale(clip, force_mod(width/4, 2), force_mod(height/4, 2))
    if write_props:
        clip_down = core.std.FrameEval(clip_down, partial(check_combed, clip=clip_down), clip_down).text.FrameNum(2)
    blank_frame = clip_down.std.BlankClip(length=1, color=[0] * 3)

    pad_c = clip_down.text.Text("Current", 8) if write_props else clip_down
    pad_a, pad_b = blank_frame * 2 + clip_down[:-2], blank_frame + clip_down[:-1]
    pad_d, pad_e = clip_down[1:] + blank_frame, clip_down[2:] + blank_frame * 2

    # Cycling
    cycle_clips = [pad_a, pad_b, pad_c, pad_d, pad_e]
    pad_x = [pad_a.std.BlankClip(force_mod(pad_a.width/15))] * 4
    cycle = cycle_clips + pad_x  # no shot this can't be done way cleaner
    cycle[::2], cycle[1::2] = cycle_clips, pad_x

    # Final stacking
    stack_abcde = Stack(cycle).clip

    vert_pad = stack_abcde.std.BlankClip(height=force_mod(stack_abcde.height / 5, 2))
    horz_pad = clip.std.BlankClip(force_mod((stack_abcde.width-clip.width) / 2, 2))

    stack = Stack([horz_pad, clip, horz_pad]).clip
    return Stack([vert_pad, stack, vert_pad, stack_abcde], direction=Direction.VERTICAL).clip


def TIVTC_VFR(clip: vs.VideoNode,
              tfm_in: Path | str = ".ivtc/matches.txt",
              tdec_in: Path | str = ".ivtc/metrics.txt",
              timecodes_out: Path | str = ".ivtc/timecodes.txt",
              decimate: int | bool = True,
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

            for _ in ivtc_clip.frames(close=True):
                pr.update(task, advance=1)

        return TIVTC_VFR(clip, tfm_in, tdec_in, timecodes_out, decimate, tfm_args, tdecimate_args)

    tfm_args = {**tfm_args, 'input': str(tfm_in)}

    tdecimate_args = {
        'mode': 5, 'hybrid': 2, 'vfrDec': 1, **tdecimate_args,
        'input': str(tdec_in), 'tfmIn': str(tfm_in), 'mkvOut': str(timecodes_out),
    }

    tfm = clip.tivtc.TFM(**tfm_args) if not decimate == -1 else clip
    return tfm.tivtc.TDecimate(**tdecimate_args) if not int(decimate) == 0 else tfm


def deblend(clip: vs.VideoNode, start: int = 0,
            rep: int | None = None, decimate: bool = True) -> vs.VideoNode:
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

    # Thanks Myaa, motbob and kageru!
    def deblend(n: int, clip: vs.VideoNode, rep: int | None) -> vs.VideoNode:
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
           tff: bool | int = True, mode: int = 1,
           decimate: bool = True, vinv: bool = False,
           rep: int | None = None, show_mask: bool = False,
           tfm_args: Dict[str, Any] = {},
           tdec_args: Dict[str, Any] = {},
           vinv_args: Dict[str, Any] = {},
           qtgmc_args: Dict[str, Any] = {}) -> vs.VideoNode:
    """
    A filter that performs relatively aggressive filtering to get rid of the combing on a interlaced/telecined source.
    Decimation can be disabled if the user wishes to decimate the clip themselves.

    Enabling vinverse will result in more aggressive decombing at the cost of potential detail loss.
    A reference clip can be passed with `ref`, which will be used by TFM to create the output frames.

    Base function written by Midlifecrisis from the WEEB AUTISM server, modified by LightArrowsEXE.

    Dependencies:

    * combmask
    * havsfunc
    * RGSF (optional: 32 bit clip)

    :param clip:          Input clip
    :param tff:           Top-Field-First
    :param mode:          Sets the matching mode or strategy to use for TFM
    :param decimate:      Decimate the video after deinterlacing (Default: True)
    :param vinv:          Use vinverse to get rid of additional combing (Default: False)
    :param rep:           Repair mode for repairing the decombed clip using the original clip (Default: None)
    :param show_mask:     Return combmask
    :param tfm_args:      Arguments to pass to TFM
    :param vinv_args:     Arguments to pass to vinverse
    :param qtgmc_args:    Arguments to pass to QTGMC

    :return:              Decombed and optionally decimated clip
    """
    try:
        from havsfunc import QTGMC
    except ModuleNotFoundError:
        raise ModuleNotFoundError("decomb: missing dependency 'havsfunc'")

    VFM_TFF = int(tff)

    tfm_kwargs: Dict[str, Any] = dict(order=VFM_TFF, mode=mode, chroma=True)
    tfm_kwargs |= tfm_args  # chroma set to True by default to match VFM

    qtgmc_kwargs: Dict[str, Any] = dict(SourceMatch=3, Lossless=2, TR0=1, TR1=2, TR2=3, FPSDivisor=2, TFF=tff)
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

    decombed = vinverse(decombed, **vinv_args) if vinv else decombed
    decombed = pick_repair(clip)(decombed, clip, rep) if rep else decombed
    return core.tivtc.TDecimate(decombed, **tdec_args) if decimate else decombed


def descale_fields(clip: vs.VideoNode, tff: bool = True,
                   width: int | None = None, height: int = 720,
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
    weave_y = weave_y.std.SetFrameProp('scaler', data=f'{kernel.__class__.__name__} (Fields)')
    return weave_y.std.SetFieldBased(0)[::2]


def bob(clip: vs.VideoNode, tff: bool | None = None) -> vs.VideoNode:
    """
    Very simple bobbing function. Shouldn't be used for regular filtering,
    but as a very cheap bobber for other functions.

    :param clip:    Input clip
    :param tff:     Top-field-first. `False` sets it to Bottom-Field-First.
                    If None, get the field order from the _FieldBased prop.

    :return:        Bobbed clip
    """
    if get_prop(clip.get_frame(0), '_FieldBased', int) == 0 and tff is None:
        raise vs.Error("bob: 'You must set `tff` for this clip!'")
    elif isinstance(tff, (bool, int)):
        clip = clip.std.SetFieldBased(int(tff) + 1)

    return Catrom().scale(clip.std.SeparateFields(), clip.width, clip.height)


def fix_telecined_fades(clip: vs.VideoNode, tff: bool | int | None = None,
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
            fixed = (sep[0].std.Expr(f"x {mean} {avg[0]} / dup {thr} <= swap 1 ? *"),
                     sep[1].std.Expr(f"x {mean} {avg[1]} / *"))
        else:
            fixed = sep  # type: ignore

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


@disallow_variable_format
@disallow_variable_resolution
def ivtc_credits(clip: vs.VideoNode, frame_ref: int, tff: bool | None = None,
                 interlaced: bool = True, dec: bool | None = None,
                 bob_clip: vs.VideoNode | None = None, qtgmc_args: Dict[str, Any] = {}
                 ) -> vs.VideoNode:
    """
    Deinterlacing function for interlaced credits (60i/30p) on top of telecined video (24p).
    This is a combination of havsfunc's dec_txt60mc, ivtc_txt30mc, and ivtc_txt60mc functions.
    The credits are interpolated and decimated to match the output clip.

    The function assumes you're passing a telecined clip (that's native 24p).
    If your clip is already fieldmatched, decimation will automatically be enabled unless set it to False.
    Likewise, if your credits are 30p (as opposed to 60i), you should set `interlaced` to False.

    The recommended way to use this filter is to trim out the area with interlaced credits,
    apply this function, and `vsutil.insert_clip` the clip back into a properly IVTC'd clip.
    Alternatively, use `muvsfunc.VFRSplice` to splice the clip back in if you're dealing with a VFR clip.

    :param clip:            Input clip. Framerate must be 30000/1001.
    :param frame_ref:       First frame in the pattern. Expected pattern is ABBCD,
                            except for when ``dec`` is enabled, in which case it's AABCD.
    :param tff:             Top-field-first. `False` sets it to Bottom-Field-First.
    :param interlaced:      60i credits. Set to false for 30p credits.
    :param dec:             Decimate input clip as opposed to IVTC.
                            Automatically enabled if certain fieldmatching props are found.
                            Can be forcibly disabled by setting it to `False`.
    :param bob_clip:        Custom bobbed clip. If `None`, uses a QTGMC clip.
                            Framerate must be 60000/1001.
    :param qtgmc_args:      Arguments to pass on to QTGMC.
                            Accepts any parameter except for FPSDivisor and TFF.

    :return:                IVTC'd/decimated clip with deinterlaced credits
    """
    try:
        from havsfunc import QTGMC, DitherLumaRebuild
    except ModuleNotFoundError:
        raise ModuleNotFoundError("ivtc_credits: missing dependency 'havsfunc'")

    if clip.fps != Fraction(30000, 1001):
        raise ValueError("ivtc_credits: 'Your clip must have a framerate of 30000/1001!'")

    if get_prop(clip.get_frame(0), '_FieldBased', int) == 0 and tff is None:
        raise vs.Error("ivtc_credits: 'You must set `tff` for this clip!'")
    elif isinstance(tff, (bool, int)):
        clip = clip.std.SetFieldBased(int(tff) + 1)

    qtgmc_kwargs: Dict[str, Any] = dict(SourceMatch=3, Lossless=2, TR0=2, TR1=2, TR2=3, Preset="Placebo")
    qtgmc_kwargs |= qtgmc_args
    qtgmc_kwargs |= dict(FPSDivisor=1, TFF=tff or bool(get_prop(clip.get_frame(0), '_FieldBased', int) - 1))

    if dec is not False:  # Automatically enable dec unless set to False
        dec = any(x in clip.get_frame(0).props for x in {"VFMMatch", "TFMMatch"})

        if dec:
            warnings.warn("ivtc_credits: 'Fieldmatched clip passed to function! "
                          "dec is set to True. If you want to disable this, set dec=False!'")

    # motion vector and other values
    field_ref = frame_ref * 2
    frame_ref %= 5
    invpos = (5 - field_ref) % 5

    offset = [0, 0, -1, 1, 1][frame_ref]
    pattern = [0, 1, 0, 0, 1][frame_ref]
    direction = [-1, -1, 1, 1, 1][frame_ref]

    blksize = 16 if clip.width > 1024 or clip.height > 576 else 8
    overlap = blksize // 2

    ivtc_fps = dict(fpsnum=24000, fpsden=1001)
    ivtc_fps_div = dict(fpsnum=12000, fpsden=1001)

    # Bobbed clip
    bobbed = bob_clip or QTGMC(clip, **qtgmc_kwargs)

    if bobbed.fps != Fraction(60000, 1001):
        raise ValueError("ivtc_credits: 'Your bobbed clip must have a framerate of 60000/1001!'")

    if interlaced:  # 60i credits. Start of ABBCD
        if dec:  # Decimate the clip instead of properly IVTC
            clean = bobbed.std.SelectEvery(5, [4 - invpos])

            if invpos > 2:
                jitter = core.std.AssumeFPS(
                    bobbed[0] * 2 + bobbed.std.SelectEvery(5, [6 - invpos, 7 - invpos]),
                    **ivtc_fps)  # type:ignore[arg-type]
            elif invpos > 1:
                jitter = core.std.AssumeFPS(
                    bobbed[0] + bobbed.std.SelectEvery(5, [2 - invpos, 6 - invpos]),
                    **ivtc_fps)  # type:ignore[arg-type]
            else:
                jitter = bobbed.std.SelectEvery(5, [1 - invpos, 2 - invpos])
        else:  # Properly IVTC
            if invpos > 1:
                clean = core.std.AssumeFPS(bobbed[0] + bobbed.std.SelectEvery(5, [6 - invpos]),
                                           **ivtc_fps_div)  # type:ignore[arg-type]
            else:
                clean = bobbed.std.SelectEvery(5, [1 - invpos])

            if invpos > 3:
                jitter = core.std.AssumeFPS(bobbed[0] + bobbed.std.SelectEvery(5, [4 - invpos, 8 - invpos]),
                                            **ivtc_fps)  # type:ignore[arg-type]
            else:
                jitter = bobbed.std.SelectEvery(5, [3 - invpos, 4 - invpos])

        jsup_pre = DitherLumaRebuild(jitter, s0=1).mv.Super(pel=2)
        jsup = jitter.mv.Super(pel=2, levels=1)
        vect_f = jsup_pre.mv.Analyse(blksize=blksize, isb=False, delta=1, overlap=overlap)
        vect_b = jsup_pre.mv.Analyse(blksize=blksize, isb=True, delta=1, overlap=overlap)
        comp = core.mv.FlowInter(jitter, jsup, vect_b, vect_f)
        out = core.std.Interleave([comp[::2], clean] if dec else [clean, comp[::2]])
        offs = 3 if dec else 2
        return out[invpos // offs:]
    else:  # 30i credits
        if pattern == 0:
            if offset == -1:
                c1 = core.std.AssumeFPS(bobbed[0] + bobbed.std.SelectEvery(
                    10, [2 + offset, 7 + offset, 5 + offset, 10 + offset]), **ivtc_fps)  # type:ignore[arg-type]
            else:
                c1 = bobbed.std.SelectEvery(10, [offset, 2 + offset, 7 + offset, 5 + offset])

            if offset == 1:
                c2 = core.std.Interleave([
                    bobbed.std.SelectEvery(10, [4]),
                    bobbed.std.SelectEvery(10, [5]),
                    bobbed[10:].std.SelectEvery(10, [0]),
                    bobbed.std.SelectEvery(10, [9])
                ])
            else:
                c2 = bobbed.std.SelectEvery(10, [3 + offset, 4 + offset, 9 + offset, 8 + offset])
        else:
            if offset == 1:
                c1 = core.std.Interleave([
                    bobbed.std.SelectEvery(10, [3]),
                    bobbed.std.SelectEvery(10, [5]),
                    bobbed[10:].std.SelectEvery(10, [0]),
                    bobbed.std.SelectEvery(10, [8])
                ])
            else:
                c1 = bobbed.std.SelectEvery(10, [2 + offset, 4 + offset, 9 + offset, 7 + offset])

            if offset == -1:
                c2 = core.std.AssumeFPS(bobbed[0] + bobbed.std.SelectEvery(
                    10, [1 + offset, 6 + offset, 5 + offset, 10 + offset]), **ivtc_fps)  # type:ignore[arg-type]
            else:
                c2 = bobbed.std.SelectEvery(10, [offset, 1 + offset, 6 + offset, 5 + offset])

        super1_pre = DitherLumaRebuild(c1, s0=1).mv.Super(pel=2)
        super1 = c1.mv.Super(pel=2, levels=1)
        vect_f1 = super1_pre.mv.Analyse(blksize=blksize, isb=False, delta=1, overlap=overlap)
        vect_b1 = super1_pre.mv.Analyse(blksize=blksize, isb=True, delta=1, overlap=overlap)
        fix1 = c1.mv.FlowInter(super1, vect_b1, vect_f1, time=50 + direction * 25).std.SelectEvery(4, [0, 2])

        super2_pre = DitherLumaRebuild(c2, s0=1).mv.Super(pel=2)
        super2 = c2.mv.Super(pel=2, levels=1)
        vect_f2 = super2_pre.mv.Analyse(blksize=blksize, isb=False, delta=1, overlap=overlap)
        vect_b2 = super2_pre.mv.Analyse(blksize=blksize, isb=True, delta=1, overlap=overlap)
        fix2 = c2.mv.FlowInter(super2, vect_b2, vect_f2).std.SelectEvery(4, [0, 2])

        return core.std.Interleave([fix1, fix2] if pattern == 0 else [fix2, fix1])


@disallow_variable_format
def vinverse(clip: vs.VideoNode, sstr: float = 2.0,
             amount: int = 128, scale: float = 1.5) -> vs.VideoNode:
    """
    A simple function to clean up residual combing after a deinterlacing pass.
    This is Setsugen_no_ao's implementation, adopted into lvsfunc.

    :param clip:    Input clip.
    :param sstr:    Contrasharpening strength. Increase this if you find
                    the decombing blurs the image a bit too much.
    :param amount:  Maximum difference allowed between the original pixels and adjusted pixels.
                    Scaled to input clip's depth. Set to 255 to effectively disable this.
    :param scale:   Scale amount for vertical sharp * vertical blur.

    :return:        Clip with residual combing largely removed
    """
    assert clip.format

    if amount > 255:
        raise ValueError("vinverse: '`amount` may not be set higher than 255!'")

    neutral = get_neutral_value(clip)

    # Expression to find combing and seperate it from the rest of the clip
    find_combs = clip.akarin.Expr(f'{neutral} n! x x 2 * x[0,-1] x[0,1] + + 4 / - n@ +')

    # Expression to decomb it (creates blending)
    decomb = core.akarin.Expr([find_combs, clip],
                              f'{neutral} n! x 2 * x[0,-1] x[0,1] + + 4 / blur! y x blur@ - x n@ - * 0 < n@ x blur@ '
                              ' - abs x n@ - abs < x blur@ - n@ + x ? ? - n@ +')

    # Final expression to properly merge it and avoid creating too much damage
    return core.akarin.Expr([clip, decomb],
                            f'{neutral} n! {scale_value(amount, 8, clip.format.bits_per_sample)} a! y y y y 2 * y[0,-1]'
                            f' y[0,1] + + 4 / - {sstr} * + y - n@ + sdiff! x y - n@ + diff! sdiff@ n@ - diff@ n@ - '
                            f'* 0 < sdiff@ n@ - abs diff@ n@ - abs < sdiff@ diff@ ? n@ - {scale} * n@ + sdiff@ n@ '
                            '- abs diff@ n@ - abs < sdiff@ diff@ ? ? n@ - + merge! x a@ + merge@ < x a@ + x a@ - '
                            'merge@ > x a@ - merge@ ? ?')
