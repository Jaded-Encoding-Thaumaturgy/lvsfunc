from __future__ import annotations

import os
import sys
import time
import warnings
from fractions import Fraction
from functools import partial
from pathlib import Path
from typing import Any, Sequence, cast

import vapoursynth as vs
from vsexprtools import mod2, mod4
from vskernels import Bicubic, BicubicDidee, Catrom, Kernel, get_kernel, get_prop
from vsrgtools import repair
from vsutil import Dither, depth, get_depth, get_neutral_value, get_w, get_y, scale_value

from .comparison import Stack
from .exceptions import InvalidFramerateError, TopFieldFirstError
from .render import clip_async_render, get_render_progress
from .types import Direction
from .util import check_variable, check_variable_format

core = vs.core

__all__ = [
    'check_patterns',
    'deblend',
    'decomb',
    'descale_fields',
    'fix_telecined_fades',
    'pulldown_credits', 'ivtc_credits',
    'seek_cycle',
    'sivtc', 'SIVTC',
    'tivtc_vfr', 'TIVTC_VFR',
    'vinverse',
]

main_file = os.path.realpath(sys.argv[0]) if sys.argv[0] else None
main_file = f"{os.path.splitext(os.path.basename(str(main_file)))[0]}_"
main_file = "{yourScriptName}_" if main_file in ("__main___", "setup_") else main_file


def sivtc(clip: vs.VideoNode, pattern: int = 0,
          tff: bool = True, decimate: bool = True) -> vs.VideoNode:
    """
    Simplest form of a fieldmatching function.

    This is essentially a stripped-down JIVTC offering JUST the basic fieldmatching and decimation part.
    As such, you may need to combine multiple instances if patterns change throughout the clip.

    :param clip:        Clip to process.
    :param pattern:     First frame of any clean-combed-combed-clean-clean sequence.
    :param tff:         Top-Field-First.
    :param decimate:    Drop a frame every 5 frames to get down to 24000/1001.

    :return:            IVTC'd clip.
    """
    pattern = pattern % 5

    defivtc = core.std.SeparateFields(clip, tff=tff).std.DoubleWeave()
    selectlist = [[0, 3, 6, 8], [0, 2, 5, 8], [0, 2, 4, 7], [2, 4, 6, 9], [1, 4, 6, 8]]
    dec = core.std.SelectEvery(defivtc, 10, selectlist[pattern]) if decimate else defivtc
    return dec.std.SetFieldBased(0).std.SetFrameProp(prop='SIVTC_pattern', intval=pattern)


def seek_cycle(clip: vs.VideoNode, write_props: bool = True, scale: int = -1) -> vs.VideoNode:
    """
    Purely visual tool to view telecining cycles.

    .. warning::
        | This is purely a visual tool and has no matching parameters!
        | Just use `Wobbly <https://github.com/dubhater/Wobbly>`_ instead if you need that.

    Displays the current frame, two previous and future frames,
    and whether they are combed or not.

    ``P`` indicates a progressive frame,
    and ``C`` a combed frame.

    Dependencies:

    * `VapourSynth-TDeintMod <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-TDeintMod>`_

    :param clip:            Clip to process.
    :param write_props:     Write props on frames. Disabling this will also speed up the function.
    :param scale:           Integer scaling of all clips. Must be to the power of 2.

    :return:                Viewing UI for standard telecining cycles.

    :raises ValueError:     `scale` is a value that is not to the power of 2.
    """
    if (scale & (scale-1) != 0) and scale != 0 and scale != -1:
        raise ValueError("seek_cycle: '`scale` must be a value that is the power of 2!'")

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
    clip_down = BicubicDidee().scale(clip, mod2(width/4), mod2(height/4))
    if write_props:
        clip_down = core.std.FrameEval(clip_down, partial(check_combed, clip=clip_down), clip_down).text.FrameNum(2)
    blank_frame = clip_down.std.BlankClip(length=1, color=[0] * 3)

    pad_c = clip_down.text.Text("Current", 8) if write_props else clip_down
    pad_a, pad_b = blank_frame * 2 + clip_down[:-2], blank_frame + clip_down[:-1]
    pad_d, pad_e = clip_down[1:] + blank_frame, clip_down[2:] + blank_frame * 2

    # Cycling
    cycle_clips = [pad_a, pad_b, pad_c, pad_d, pad_e]
    pad_x = [pad_a.std.BlankClip(mod4(pad_a.width/15))] * 4
    cycle = cycle_clips + pad_x  # no shot this can't be done way cleaner
    cycle[::2], cycle[1::2] = cycle_clips, pad_x

    # Final stacking
    stack_abcde = Stack(cycle).clip

    vert_pad = stack_abcde.std.BlankClip(height=mod2(stack_abcde.height / 5))
    horz_pad = clip.std.BlankClip(mod2((stack_abcde.width-clip.width) / 2))

    stack = Stack([horz_pad, clip, horz_pad]).clip
    return Stack([vert_pad, stack, vert_pad, stack_abcde], direction=Direction.VERTICAL).clip


def check_patterns(clip: vs.VideoNode, tff: bool | int | None = None) -> int:
    """
    Naïve function that iterates over a given clip and tries out every simple 3:2 IVTC pattern.

    This function will return the best pattern value that didn't result in any combing.
    If all of them resulted in combing, it will raise an error.

    Note that the clip length may seem off because I grab every fourth frame of a clip.
    This should make processing faster, and it will still find combed frames.

    This function should only be used for rudimentary testing.
    If I see it in any proper scripts, heads will roll.

    Dependencies:

    * `VapourSynth-TDeintMod <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-TDeintMod>`_

    :param clip:                    Clip to process.
    :param tff:                     Top-field-first. `False` sets it to Bottom-Field-First.
                                    If None, get the field order from the _FieldBased prop.

    :return:                        Integer representing the best pattern.

    :raises TopFieldFirstError:     No automatic ``tff`` can be determined.
    :raises StopIteration:          No pattern resulted in a clean match.
    """
    if get_prop(clip.get_frame(0), '_FieldBased', int) == 0 and tff is None:
        raise TopFieldFirstError("check_patterns")
    elif isinstance(tff, (bool, int)):
        clip = clip.std.SetFieldBased(int(tff) + 1)

    clip = depth(clip, 8)

    pattern = -1

    for n in [int(n) for n in range(0, 4)]:
        check = _check_pattern(clip, n)

        if check:
            pattern = n
            break

    if pattern == -1:
        raise StopIteration("check_patterns: 'None of the patterns resulted in a clip without combing. "
                            "Please try performing proper IVTC on the clip.")

    return pattern


def tivtc_vfr(clip: vs.VideoNode,
              tfm_in: Path | str = f".ivtc/{main_file}matches.txt",
              tdec_in: Path | str = f".ivtc/{main_file}metrics.txt",
              timecodes_out: Path | str = f".ivtc/{main_file}timecodes.txt",
              decimate: int | bool = True,
              tfm_args: dict[str, Any] = {},
              tdecimate_args: dict[str, Any] = {}) -> vs.VideoNode:
    """
    Perform TFM and TDecimate on a clip that is supposed to be VFR.

    Includes automatic generation of a metrics/matches/timecodes txt file.

    | This function took *heavy* inspiration from atomchtools.TIVTC_VFR,
    | and is basically an improved rewrite on the concept.

    .. warning::
        | When calculating the matches and metrics for the first time, your previewer may error out!
        | To fix this, simply refresh your previewer. If it still doesn't work, open the ``.ivtc`` directory
        | and check if the files are **0kb**. If they are, **delete them** and run the function again.
        | You may need to restart your previewer entirely for it to work!

    Dependencies:

    * `TIVTC <https://github.com/dubhater/vapoursynth-tivtc>`_

    :param clip:                Clip to process.
    :param tfmIn:               File location for TFM's matches analysis.
                                By default it will be written to ``.ivtc/{yourScriptName}_matches.txt``.
    :param tdecIn:              File location for TDecimate's metrics analysis.
                                By default it will be written to ``.ivtc/{yourScriptName}_metrics.txt``.
    :param timecodes_out:       File location for TDecimate's timecodes analysis.
                                By default it will be written to ``.ivtc/{yourScriptName}_timecodes.txt``.
    :param decimate:            Perform TDecimate on the clip if true, else returns TFM'd clip only.
                                Set to -1 to use TDecimate without TFM.
    :param tfm_args:            Additional arguments to pass to TFM.
    :param tdecimate_args:      Additional arguments to pass to TDecimate.

    :return:                    IVTC'd VFR clip with external timecode/matches/metrics txt files.

    :raises TypeError:          Invalid ``decimate`` argument is passed.
    """
    if int(decimate) not in (-1, 0, 1):
        raise TypeError("TIVTC_VFR: 'Invalid `decimate` argument. Must be True/False, their integer values, or -1!'")

    tfm_f = tdec_f = timecodes_f = Path()

    def _set_paths() -> None:
        nonlocal tfm_f, tdec_f, timecodes_f
        tfm_f = Path(tfm_in).resolve().absolute()
        tdec_f = Path(tdec_in).resolve().absolute()
        timecodes_f = Path(timecodes_out).resolve().absolute()

    _set_paths()

    # TIVTC can't write files into directories that don't exist
    for p in (tfm_f, tdec_f, timecodes_f):
        if not p.parent.exists():
            p.parent.mkdir(parents=True)

    if not (tfm_f.exists() and tdec_f.exists()):
        warnings.warn("tivtc_vfr: 'When calculating the matches and metrics for the first time, "
                      "your previewer may error out! To fix this, simply refresh your previewer. "
                      "If it still doesn't work, open the ``.ivtc`` directory and check if the files are 0kb. "
                      "If they are, delete them and run the function again.'")

        tfm_analysis: dict[str, Any] = {**tfm_args, 'output': str(tfm_f)}
        tdec_analysis: dict[str, Any] = {'mode': 4, **tdecimate_args, 'output': str(tdec_f)}

        ivtc_clip = core.tivtc.TFM(clip, **tfm_analysis)
        ivtc_clip = core.tivtc.TDecimate(ivtc_clip, **tdec_analysis)

        with get_render_progress() as pr:
            task = pr.add_task("Analyzing frames...", total=ivtc_clip.num_frames)

            def _cb(n: int, total: int) -> None:
                pr.update(task, advance=1)

            with open(os.devnull, 'wb') as dn:
                ivtc_clip.output(dn, progress_update=_cb)

        del ivtc_clip  # Releases the clip, and in turn the filter (prevents an error)

        _set_paths()

    while not (tfm_f.stat().st_size > 0 and tdec_f.stat().st_size > 0):
        time.sleep(0.5)  # Allow it to properly finish writing logs if necessary

    tfm_args = {**tfm_args, 'input': str(tfm_in)}

    tdecimate_args = {
        'mode': 5, 'hybrid': 2, 'vfrDec': 1, **tdecimate_args,
        'input': str(tdec_f), 'tfmIn': str(tfm_f), 'mkvOut': str(timecodes_f),
    }

    tfm = clip.tivtc.TFM(**tfm_args) if decimate != -1 else clip
    return tfm.tivtc.TDecimate(**tdecimate_args) if int(decimate) != 0 else tfm


def deblend(clip: vs.VideoNode, start: int = 0,
            rep: int | None = None, decimate: bool = True) -> vs.VideoNode:
    """
    Deblending function for blended AABBA patterns.

    .. warning:
        This function's base functionality and settings will be updated in a future version!

    Assuming there's a constant pattern of frames (labeled A, B, C, CD, and DA in this function),
    blending can be fixed by calculating the D frame by getting halves of CD and DA, and using that
    to fix up CD. DA is then dropped because it's a duplicated frame.

    Doing this will result in some of the artifacting being added to the deblended frame,
    but we can mitigate that by repairing the frame with the non-blended frame before it.

    For more information, please refer to `this blogpost by torchlight
    <https://mechaweaponsvidya.wordpress.com/2012/09/13/adventures-in-deblending/>`_.

    Dependencies:

    * `RGSF <https://github.com/IFeelBloated/RGSF>`_ (optional: 32 bit clip)

    :param clip:        Clip to process.
    :param start:       First frame of the pattern (Default: 0).
    :param rep:         Repair mode for the deblended frames, no repair if None (Default: None).
    :param decimate:    Decimate the video after deblending (Default: True).

    :return:            Deblended clip.
    """
    warnings.warn("deblend: 'This function's base functionality and settings "
                  "will be updated in a future version!'", DeprecationWarning)

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
                debl = core.akarin.Expr([c, cd, da, a], expr_cd)
                return repair(debl, c, rep) if rep else debl
            return clip

    debl = core.std.FrameEval(clip, partial(deblend, clip=clip, rep=rep))
    return core.std.DeleteFrames(debl, blends_b).std.AssumeFPS(fpsnum=24000, fpsden=1001) \
        if decimate else debl


def decomb(clip: vs.VideoNode,
           tff: bool | int = True, mode: int = 1,
           decimate: bool = True, vinv: bool = False,
           rep: int | Sequence[int] = 0,
           show_mask: bool = False,
           tfm_args: dict[str, Any] = {},
           tdec_args: dict[str, Any] = {},
           vinv_args: dict[str, Any] = {},
           qtgmc_args: dict[str, Any] = {}) -> vs.VideoNode:
    """
    Perform relatively aggressive filtering to get rid of the combing on a interlaced/telecined source.

    .. warning:
        This function will be removed in a future version!

    Decimation can be disabled if the user wishes to decimate the clip themselves.

    Enabling vinverse will result in more aggressive decombing at the cost of potential detail loss.
    A reference clip can be passed with `ref`, which will be used by TFM to create the output frames.

    Original function written by Midlifecrisis, modified by LightArrowsEXE.

    Dependencies:

    * `combmask <https://drive.google.com/file/d/15E0Ua27AndT-0zSHHCC1iL5SZO09Ntbv/view?usp=sharing>`_
    * `havsfunc <https://github.com/HomeOfVapourSynthEvolution/havsfunc>`_
    * `RGSF <https://github.com/IFeelBloated/RGSF>`_ (optional: 32 bit clip)

    :param clip:                    Clip to process.
    :param tff:                     Top-Field-First.
    :param mode:                    Sets the matching mode or strategy to use for TFM.
    :param decimate:                Decimate the video after deinterlacing (Default: True).
    :param vinv:                    Use vinverse to get rid of additional combing (Default: False).
    :param rep:                     Repair mode for repairing the decombed clip using the original clip (Default: None).
    :param show_mask:               Return combmask.
    :param tfm_args:                Arguments to pass to TFM.
    :param vinv_args:               Arguments to pass to vinverse.
    :param qtgmc_args:              Arguments to pass to QTGMC.

    :return:                        Decombed and optionally decimated clip.

    :raises ModuleNotFoundError:    Dependencies are missing.
    """
    try:
        from havsfunc import QTGMC
    except ModuleNotFoundError:
        raise ModuleNotFoundError("decomb: missing dependency `havsfunc`!")

    warnings.warn("decomb: 'This function will be removed in a future version!'", FutureWarning)

    VFM_TFF = int(tff)

    tfm_kwargs: dict[str, Any] = dict(order=VFM_TFF, mode=mode, chroma=True)
    tfm_kwargs |= tfm_args  # chroma set to True by default to match VFM

    qtgmc_kwargs: dict[str, Any] = dict(SourceMatch=3, Lossless=2, TR0=1, TR1=2, TR2=3, FPSDivisor=2, TFF=tff)
    qtgmc_kwargs |= qtgmc_args

    def _pp(n: int, f: vs.VideoFrame, clip: vs.VideoNode, pp: vs.VideoNode) -> vs.VideoNode:
        return pp if get_prop(f, '_Combed', int) == 1 else clip

    clip = core.tivtc.TFM(clip, **tfm_kwargs)

    combmask = core.comb.CombMask(clip, cthresh=1, mthresh=3)
    combmask = core.std.Maximum(combmask, threshold=250).std.Maximum(threshold=250) \
        .std.Maximum(threshold=250).std.Maximum(threshold=250)
    combmask = core.std.BoxBlur(combmask, hradius=2, vradius=2).std.Limiter()

    if show_mask:
        return combmask

    qtgmc = QTGMC(clip, **qtgmc_kwargs)
    qtgmc_merged = core.std.MaskedMerge(clip, qtgmc, combmask, first_plane=True)

    decombed = core.std.FrameEval(clip, partial(_pp, clip=clip, pp=qtgmc_merged), clip)

    decombed = vinverse(decombed, **vinv_args) if vinv else decombed
    decombed = repair(decombed, clip, rep)
    return core.tivtc.TDecimate(decombed, **tdec_args) if decimate else decombed


def descale_fields(clip: vs.VideoNode, tff: bool = True,
                   width: int | None = None, height: int = 720,
                   kernel: Kernel | str = Bicubic(b=0, c=1/2),
                   src_top: float = 0.0) -> vs.VideoNode:
    """
    Descale interwoven upscaled fields, also known as a cross conversion.

    This function also sets a frameprop with the kernel that was used.

    The kernel is set using an py:class:`vskernels.Kernel` object.
    For more information, check the `vskernels documentation <https://vskernels.encode.moe/en/latest/>`_.

    ``src_top`` allows you to to shift the clip prior to descaling.
    This may be useful, as sometimes clips are shifted before or after the original upscaling.

    :param clip:        Clip to process.
    :param tff:         Top-field-first. `False` sets it to Bottom-Field-First.
    :param width:       Native width. Will be automatically determined if set to `None`.
    :param height:      Native height. Will be divided by two internally.
    :param kernel:      py:class:`vskernels.Kernel` object used for the descaling.
                        This can also be the string name of the kernel (Default: py:class:`vskernels.Catrom`).
    :param src_top:     Shifts the clip vertically during the descaling.

    :return:            Descaled GRAY clip.
    """
    height_field = int(height/2)
    width = width or get_w(height, clip.width/clip.height)

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    clip = clip.std.SetFieldBased(2-int(tff))

    sep = core.std.SeparateFields(get_y(clip))
    descaled = kernel.descale(sep, width, height_field, (src_top, 0))
    weave_y = core.std.DoubleWeave(descaled)
    weave_y = weave_y.std.SetFrameProp('scaler', data=f'{kernel.__class__.__name__} (Fields)')
    return weave_y.std.SetFieldBased(0)[::2]


def fix_telecined_fades(clip: vs.VideoNode, tff: bool | int | None = None,
                        thr: float = 2.2) -> vs.VideoNode:
    """
    Give a mathematically perfect solution to fades made *after* telecining (which made perfect IVTC impossible).

    This is an improved version of the Fix-Telecined-Fades plugin
    that deals with overshoot/undershoot by adding a check.

    Make sure to run this *after* IVTC/deinterlacing!

    If the value surpases thr * original value, it will not affect any pixels in that frame
    to avoid it damaging frames it shouldn't need to. This helps a lot with orphan fields as well,
    which would otherwise create massive swings in values, sometimes messing up the fade fixing.

    .. warning::
        | If you pass your own float clip, you'll want to make sure to properly dither it down after.
        | If you don't do this, you'll run into some serious issues!

    Taken from this gist and modified by LightArrowsEXE.
    <https://gist.github.com/blackpilling/bf22846bfaa870a57ad77925c3524eb1>

    :param clip:                    Clip to process.
    :param tff:                     Top-field-first. `False` sets it to Bottom-Field-First.
                                    If None, get the field order from the _FieldBased prop.
    :param thr:                     Threshold for when a field should be adjusted.
                                    Default is 2.2, which appears to be a safe value that doesn't
                                    cause it to do weird stuff with orphan fields.

    :return:                        Clip with only fades fixed.

    :raises TopFieldFirstError:     No automatic ``tff`` can be determined.
    """
    def _ftf(n: int, f: list[vs.VideoFrame]) -> vs.VideoNode:
        avg = (get_prop(f[0], 'PlaneStatsAverage', float),
               get_prop(f[1], 'PlaneStatsAverage', float))

        if avg[0] != avg[1]:
            mean = sum(avg) / 2
            fixed = (sep[0].akarin.Expr(f"x {mean} {avg[0]} / dup {thr} <= swap 1 ? *"),
                     sep[1].akarin.Expr(f"x {mean} {avg[1]} / *"))
        else:
            fixed = cast(tuple[vs.VideoNode, vs.VideoNode], sep)

        return core.std.Interleave(fixed).std.DoubleWeave()[::2]

    # I want to catch this before it reaches separateFields and give newer users a more useful error
    if get_prop(clip.get_frame(0), '_FieldBased', int) == 0 and tff is None:
        raise TopFieldFirstError("fix_telecined_fades")
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


def pulldown_credits(clip: vs.VideoNode, frame_ref: int, tff: bool | None = None,
                     interlaced: bool = True, dec: bool | None = None,
                     bob_clip: vs.VideoNode | None = None, qtgmc_args: dict[str, Any] = {}
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

    :param clip:                    Clip to process. Framerate must be 30000/1001.
    :param frame_ref:               First frame in the pattern. Expected pattern is ABBCD,
                                    except for when ``dec`` is enabled, in which case it's AABCD.
    :param tff:                     Top-field-first. `False` sets it to Bottom-Field-First.
    :param interlaced:              60i credits. Set to false for 30p credits.
    :param dec:                     Decimate input clip as opposed to IVTC.
                                    Automatically enabled if certain fieldmatching props are found.
                                    Can be forcibly disabled by setting it to `False`.
    :param bob_clip:                Custom bobbed clip. If `None`, uses a QTGMC clip.
                                    Framerate must be 60000/1001.
    :param qtgmc_args:              Arguments to pass on to QTGMC.
                                    Accepts any parameter except for FPSDivisor and TFF.

    :return:                        IVTC'd/decimated clip with credits pulled down to 24p.

    :raises ModuleNotFoundError:    Dependencies are missing.
    :raises ValueError:             Clip does not have a framerate of 30000/1001 (29.97).
    :raises TopFieldFirstError:     No automatic ``tff`` can be determined.
    :raises InvalidFramerateError:  Bobbed clip does not have a framerate of 60000/1001 (59.94)
    """
    try:
        from havsfunc import QTGMC
    except ModuleNotFoundError:
        raise ModuleNotFoundError("pulldown_credits: missing dependency `havsfunc`!")

    try:
        from vsdenoise import prefilter_to_full_range
    except ModuleNotFoundError:
        from havsfunc import DitherLumaRebuild as prefilter_to_full_range  # type: ignore
        warnings.warn("pulldown_credits: missing dependency `vsdenoise`!", ImportWarning)

    assert check_variable(clip, "pulldown_credits")

    if clip.fps != Fraction(30000, 1001):
        raise ValueError("pulldown_credits: 'Your clip must have a framerate of 30000/1001!'")

    if get_prop(clip.get_frame(0), '_FieldBased', int) == 0 and tff is None:
        raise TopFieldFirstError("pulldown_credits")
    elif isinstance(tff, (bool, int)):
        clip = clip.std.SetFieldBased(int(tff) + 1)

    qtgmc_kwargs: dict[str, Any] = dict(SourceMatch=3, Lossless=2, TR0=2, TR1=2, TR2=3, Preset="Placebo")
    qtgmc_kwargs |= qtgmc_args
    qtgmc_kwargs |= dict(FPSDivisor=1, TFF=tff or bool(get_prop(clip.get_frame(0), '_FieldBased', int) - 1))

    if dec is not False:  # Automatically enable dec unless set to False
        dec = any(x in clip.get_frame(0).props for x in {"VFMMatch", "TFMMatch"})

        if dec:
            warnings.warn("pulldown_credits: 'Fieldmatched clip passed to function! "
                          "dec is set to `True`. If you want to disable this, set `dec=False`!'")

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
        raise InvalidFramerateError("pulldown_credits", bobbed,
                                    "{func} 'Your bobbed clip *must* have a framerate of 60000/1001!'")

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

        jsup_pre = prefilter_to_full_range(jitter, 1.0).mv.Super(pel=2)
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

        super1_pre = prefilter_to_full_range(c1, 1.0).mv.Super(pel=2)
        super1 = c1.mv.Super(pel=2, levels=1)
        vect_f1 = super1_pre.mv.Analyse(blksize=blksize, isb=False, delta=1, overlap=overlap)
        vect_b1 = super1_pre.mv.Analyse(blksize=blksize, isb=True, delta=1, overlap=overlap)
        fix1 = c1.mv.FlowInter(super1, vect_b1, vect_f1, time=50 + direction * 25).std.SelectEvery(4, [0, 2])

        super2_pre = prefilter_to_full_range(c2, 1.0).mv.Super(pel=2)
        super2 = c2.mv.Super(pel=2, levels=1)
        vect_f2 = super2_pre.mv.Analyse(blksize=blksize, isb=False, delta=1, overlap=overlap)
        vect_b2 = super2_pre.mv.Analyse(blksize=blksize, isb=True, delta=1, overlap=overlap)
        fix2 = c2.mv.FlowInter(super2, vect_b2, vect_f2).std.SelectEvery(4, [0, 2])

        return core.std.Interleave([fix1, fix2] if pattern == 0 else [fix2, fix1])


def vinverse(clip: vs.VideoNode, sstr: float = 2.0,
             amount: int = 128, scale: float = 1.5) -> vs.VideoNode:
    """
    Clean up residual combing after a deinterlacing pass.

    This is Setsugen no ao's implementation, adopted into lvsfunc.

    :param clip:        Clip to process.
    :param sstr:        Contrasharpening strength. Increase this if you find
                        the decombing blurs the image a bit too much.
    :param amount:      Maximum difference allowed between the original pixels and adjusted pixels.
                        Scaled to input clip's depth. Set to 255 to effectively disable this.
    :param scale:       Scale amount for vertical sharp * vertical blur.

    :return:            Clip with residual combing largely removed.

    :raises ValueError: ``amount`` is set above 255.
    """
    assert check_variable_format(clip, "vinverse")

    if amount > 255:
        raise ValueError("vinverse: '`amount` may not be set higher than 255!'")

    neutral = get_neutral_value(clip)

    # Expression to find combing and separate it from the rest of the clip
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


# helpers
def _check_pattern(clip: vs.VideoNode, pattern: int = 0) -> bool:
    """:py:func:`lvsfunc.deinterlace.check_patterns` rendering behaviour."""
    clip = sivtc(clip, pattern)
    clip = core.tdm.IsCombed(clip)

    frames: list[int] = []

    def _cb(n: int, f: vs.VideoFrame) -> None:
        if get_prop(f, '_Combed', int):
            frames.append(n)

    # TODO: Tried being clever and just exiting if any combing was found, but async_render had other plans :)
    clip_async_render(clip[::4], progress=f"Checking pattern {pattern}...", callback=_cb)

    if len(frames) > 0:
        print(f"check_patterns: 'Combing found with pattern {pattern}!'")
        return False

    print(f"check_patterns: 'Clean clip found with pattern {pattern}!'")
    return True


# Temporary aliases
SIVTC = sivtc
TIVTC_VFR = tivtc_vfr
ivtc_credits = pulldown_credits
