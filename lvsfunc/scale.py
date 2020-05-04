"""
    Functions for (de)scaling.
"""
import math
from collections import namedtuple
from fractions import Fraction
from functools import partial
from typing import Callable, List, Optional, Union

import vapoursynth as vs
from vsutil import get_depth, get_w, get_y, iterate, join, plane, split

from . import util

core = vs.core


def descale(clip: vs.VideoNode,
            upscaler: Callable[[vs.VideoNode, int, int], vs.VideoNode],
            width: Optional[int] = None, height: int = 720,
            kernel: str = 'bicubic', brz: float = 0.05,
            b: float = 0, c: float = 1 / 2, taps: int = 4,
            src_left: float = 0.0,
            src_top: float = 0.0) -> vs.VideoNode:
    """
    A generic descaling function.
    includes support for handling fractional resolutions (although that's still experimental)

    If you want to descale to a fractional resolution,
    set src_left and src_top and round up the target height.

    :param clip:                   Clip to descale
    :param upscaler:               Callable function with signature upscaler(clip, width, height) -> vs.VideoNode to be used for reupscaling.
                                   Example for nnedi3_rpow2: `clip, upscaler = nnedi3_rpow2, ...`
    :param width:                  Width to descale to (if None, auto-calculated)
    :param height:                 Height to descale to (Default: 720)
    :param kernel:                 Kernel used to descale (see :py:func:`descale.get_filter`, default: bicubic)
    :param brz:                    Binarizing for the credit mask
    :param b:                      B-param for bicubic kernel (Default: 0)
    :param c:                      C-param for bicubic kernel (Default: 1 / 2)
    :param taps:                   Taps param for lanczos kernel (Default: 4)
    :param src_left:               Horizontal shifting for fractional resolutions
    :param src_top:                Vertical shifting for fractional resolutions

    :return:                       Descaled and re-upscaled clip
    """
    try:
        from descale import get_filter
    except ModuleNotFoundError:
        raise ModuleNotFoundError("fractional_descale: missing dependency 'descale'")

    def _create_credit_mask(clip: vs.VideoNode, descaled_clip: vs.VideoNode,
                            kernel: str = 'bicubic', brz: float = 0.05,
                            b: float = 0, c: float = 1/2, taps: int = 4,
                            src_left: Optional[float] = False,
                            src_top: Optional[float] = False) -> vs.VideoNode:
        src_left = src_left or 0
        src_top = src_top or 0

        rescaled = util.get_scale_filter(kernel, b=b, c=c, taps=taps)(descaled_clip, clip.width, clip.height,
                                                                      src_left = src_left, src_top = src_top)
        credit_mask = core.std.Expr([clip, rescaled], 'x y - abs').std.Binarize(brz)
        credit_mask = iterate(credit_mask, core.std.Maximum, 4)
        return iterate(credit_mask, core.std.Inflate, 2)

    kernel = kernel.lower()

    if width is None:
        width = get_w(clip, clip.width / clip.height)

    clip_y = get_y(clip)
    descaled = get_filter(b, c, taps, kernel)(clip_y, width, height)

    # This is done this way to prevent it from doing a needless conversion if params not passed
    if src_left is not 0 or src_top is not 0:
        descaled = core.resize.Bicubic(descaled, src_left = src_left, src_top = src_top)

    upscaled = upscaler(descaled, width=clip.width, height=clip.height)

    if src_left is not 0 or src_top is not 0:
        upscaled = core.resize.Bicubic(descaled, src_left = -src_left, src_top = -src_top)

    credit_mask = _create_credit_mask(clip_y, descaled, kernel, brz, b, c, taps, src_left, src_top)
    merged = core.std.MaskedMerge(upscaled, clip_y, credit_mask)
    merged = core.std.SetFrameProp(merged, "_descaled", data="True")

    if clip.format is vs.GRAY:
        return merged
    return join([merged, plane(clip, 1), plane(clip, 2)])


def conditional_descale(clip: vs.VideoNode,
                        upscaler: Callable[[vs.VideoNode, int, int], vs.VideoNode],
                        width: Optional[int] = None, height: int = 720,
                        kernel: str = 'bicubic',
                        b: Union[float, Fraction] = Fraction(0),
                        c: Union[float, Fraction] = Fraction(1, 2),
                        taps: int = 4,
                        threshold: float = 0.003,
                        **upscaler_args) -> vs.VideoNode:
    """
    Descales and reupscales a clip; if the difference exceeds the threshold, the frame will not be descaled.
    If it does not exceed the threshold, the frame will upscaled using the caller-supplied upscaler function.

    Useful for bad BDs that have additional post-processing done on some scenes, rather than all of them.

    Currently only works with bicubic, and has no native 1080p masking.
    Consider scenefiltering OP/EDs with a different descale function instead.

    The code for _get_error was mostly taken from kageru's Made in Abyss script.
    Special thanks to Lypheo for holding my hand as this was written.

    Dependencies: vapoursynth-descale

    :param clip:                   Input clip
    :param upscaler:               Callable function with signature upscaler(clip, width, height) -> vs.VideoNode to be used for reupscaling.
                                   Example for nnedi3_rpow2: `lambda clip, width, height: nnedi3_rpow2(clip).resize.Spline36(width, height)`
    :param width:                  Target descale width. If None, determine from `height`
    :param height:                 Target descale height (Default: 720)
    :param kernel:                 Kernel used to descale (see :py:func:`lvsfunc.util.get_scale_filter`, Default: bicubic)
    :param b:                      B-param for bicubic kernel (Default: 1 / 3)
    :param c:                      C-param for bicubic kernel (Default: 1 / 3)
    :param taps:                   Taps param for lanczos kernel (Default: 4)
    :param threshold:              Threshold for deciding to descale or leave the original frame (Default: 0.003)

    :return:                       Constant-resolution rescaled clip
    """
    try:
        from descale import get_filter
    except ModuleNotFoundError:
        raise ModuleNotFoundError("conditional_descale: missing dependency 'descale'")

    b = float(b)
    c = float(c)

    width = width or get_w(height, clip.width / clip.height)

    def _get_error(clip, width, height, kernel, b, c, taps):
        descale = get_filter(b, c, taps, kernel)(clip, width, height)
        upscale = util.get_scale_filter(kernel, b=b, c=c, taps=taps)(descale, clip.width, clip.height)
        diff = core.std.PlaneStats(upscale, clip)
        return descale, diff

    def _diff(n, f, clip_a, clip_b, threshold):
        return clip_a if f.props.PlaneStatsDiff > threshold else clip_b

    if get_depth(clip) != 32:
        clip = util.resampler(clip, 32)

    planes = split(clip)
    descaled, diff = _get_error(planes[0], width=width, height=height, kernel=kernel, b=b, c=c, taps=taps)

    planes[0] = upscaler(descaled, clip.width, clip.height, **upscaler_args)

    descaled = join(planes).resize.Spline36(format=clip.format)
    descaled = descaled.std.SetFrameProp("_descaled", intval=1)
    clip = clip.std.SetFrameProp("_descaled", intval=0)

    return core.std.FrameEval(clip, partial(_diff, clip_a=clip, clip_b=descaled, threshold=threshold), diff)


def smart_descale(clip: vs.VideoNode,
                  resolutions: List[int],
                  kernel: str = 'bicubic',
                  b: Union[float, Fraction] = Fraction(0),
                  c: Union[float, Fraction] = Fraction(1, 2), taps: int = 4,
                  thr: float = 0.05, rescale: bool = False) -> vs.VideoNode:
    """
    A function that descales a clip to multiple resolutions.

    This function will descale clips to multiple resolutions and return the descaled clip
    that is mostly likely to be the actual resolution of the clip. This is useful for shows
    like Shield Hero, Made in Abyss, or Symphogear that love jumping between multiple resolutions.

    The returned clip will be multiple resolutions, meaning most resamplers will break,
    as well as encoding it as-is. When handling it, please ensure you return the clip to
    a steady resolution before further processing.

    Setting rescaled will use `smart_rescaler` to reupscale the clip to its original resolution.
    This will return a proper YUV clip as well. If rescaled is set to False, the returned clip
    will be GRAY.

    Original written by kageru, and in part rewritten by me. Thanks Varde for helping me fix some bugs with it.

    Dependencies: vapoursynth-descale

    :param clip:             Input clip
    :param resolutions:      A list of resolutions to descale to
    :param kernel:           Kernel used to descale (see :py:func:`lvsfunc.util.get_scale_filter`, Default: bicubic)
    :param b:                B-param for bicubic kernel (Default: 0)
    :param c:                C-param for bicubic kernel (Default: 1 / 2)
    :param taps:             Taps param for lanczos kernel (Default: 4)
    :param thr:              Threshold for when a clip is discerned as "non-scaleable" (Default: 0.05)
    :param rescale:          Rescale the clip to the original resolution after descaling (Default: False)

    :return:                 Variable-resolution clip containing descaled frames
    """
    try:
        from descale import get_filter
    except ModuleNotFoundError:
        raise ModuleNotFoundError("smart_descale: missing dependency 'descale'")

    b = float(b)
    c = float(c)

    Resolution = namedtuple('Resolution', ['width', 'height'])
    ScaleAttempt = namedtuple('ScaleAttempt', ['descaled', 'rescaled', 'resolution', 'diff'])
    clip_c = clip

    clip = util.resampler((get_y(clip) if clip.format.num_planes != 1 else clip), 32) \
        .std.SetFrameProp('descaleResolution', intval=clip.height)

    def _perform_descale(height: int) -> ScaleAttempt:
        resolution = Resolution(get_w(height, clip.width / clip.height), height)
        descaled = get_filter(b, c, taps, kernel)(clip, resolution.width, resolution.height) \
            .std.SetFrameProp('descaleResolution', intval=height)
        rescaled = util.get_scale_filter(kernel, b=b, c=c, taps=taps)(descaled, clip.width, clip.height)
        diff = core.std.Expr([rescaled, clip], 'x y - abs').std.PlaneStats()
        return ScaleAttempt(descaled, rescaled, resolution, diff)

    clips_by_resolution = {c.resolution.height: c for c in map(_perform_descale, resolutions)}
    # If we pass a variable res clip as first argument to FrameEval, we’re also allowed to return one.
    variable_res_clip = core.std.Splice([
        core.std.BlankClip(clip, length=len(clip) - 1), core.std.BlankClip(clip, length=1, width=clip.width + 1)
    ], mismatch=True)

    def _select_descale(n: int, f: List[vs.VideoFrame]):
        best_res = max(f, key=lambda frame: math.log(clip.height - frame.props.descaleResolution, 2) * round(1 / max(frame.props.PlaneStatsAverage, 1e-12)) ** 0.2)

        best_attempt = clips_by_resolution.get(best_res.props.descaleResolution)
        if thr == 0:
            return best_attempt.descaled
        # No blending here because src and descaled have different resolutions.
        # The caller can use the frameProps to deal with that if they so desire.
        if best_res.props.PlaneStatsAverage > thr:
            return clip
        return best_attempt.descaled

    props = [c.diff for c in clips_by_resolution.values()]
    descaled = core.std.FrameEval(variable_res_clip, _select_descale,
                                  prop_src=props)

    if rescale:
        upscale = smart_reupscale(descaled, height=clip.height, kernel=kernel, b=b, c=c, taps=taps)
        if clip_c.format is vs.GRAY:
            return upscale
        return join([upscale, plane(clip_c, 1), plane(clip_c, 2)])
    return descaled


def smart_reupscale(clip: vs.VideoNode,
                    width: Optional[int] = None, height: int = 1080,
                    kernel: str = 'bicubic',
                    b: Union[float, Fraction] = Fraction(0),
                    c: Union[float, Fraction] = Fraction(1, 2), taps: int = 4,
                    **znargs) -> vs.VideoNode:
    """
    A quick 'n easy wrapper used to re-upscale a clip descaled with smart_descale using znedi3.

    Stolen from Varde.

    Dependencies: znedi3

    :param clip:         Input clip
    :param width:        Upscale width. If None, determine from `height` assuming 16:9 aspect ratio (Default: None)
    :param height:       Upscale height (Default: 1080)
    :param kernel:       Kernel used to downscale the doubled clip (see :py:func:`lvsfunc.util.get_scale_filter`)
    :param b:            B-param for bicubic kernel (Default: 0)
    :param c:            C-param for bicubic kernel (Default: 1 / 2)
    :param taps:         Taps param for lanczos kernel. (Default: 4)
    :param znargs:       Arguments passed to znedi3

    :return:             Reupscaled clip
    """

    b = float(b)
    c = float(c)

    def _transpose_shift(n, f, clip):
        try:
            h = f.props.descaleResolution
        except:
            raise ValueError(f"smart_reupscale: 'This clip was not descaled using smart_descale'")
        w = get_w(h)
        clip = util.get_scale_filter(kernel, b=b, c=c, taps=taps)(clip, width=w, height=h * 2, src_top=.5)
        return core.std.Transpose(clip)

    width = width or get_w(height)

    # Doubling and downscale to given "h"
    znargs = znargs or dict(nsize=4, nns=4, qual=2, pscrn=2)

    upsc = util.quick_resample(clip, core.znedi3.nnedi3, field=0, dh=True, **znargs)
    upsc = core.std.FrameEval(upsc, partial(_transpose_shift, clip=upsc), prop_src=upsc)
    upsc = util.quick_resample(upsc, core.znedi3.nnedi3, field=0, dh=True, **znargs)
    return util.get_scale_filter(kernel, b=b, c=c, taps=taps)(upsc, height=width, width=height, src_top=.5).std.Transpose()


def test_descale(clip: vs.VideoNode,
                 width: Optional[int] = None, height: int = 720,
                 kernel: str = 'bicubic',
                 b: Union[float, Fraction] = Fraction(0),
                 c: Union[float, Fraction] = Fraction(1, 2),
                 taps: int = 4,
                 show_error: bool = True) -> vs.VideoNode:
    """
    Generic function to test descales with;
    descales and reupscales a given clip, allowing you to compare the two easily.

    When comparing, it is recommended to do atleast a 4x zoom using Nearest Neighbor.
    I also suggest using 'compare' (py:func:lvsfunc.comparison.compare),
    as that will make comparing the output with the source clip a lot easier.

    Some of this code was leveraged from DescaleAA found in fvsfunc.

    Dependencies: vapoursynth-descale

    :param clip:           Input clip
    :param width:          Target descale width. If None, determine from `height`
    :param height:         Target descale height (Default: 720)
    :param kernel:         Kernel used to descale (see :py:func:`lvsfunc.util.get_scale_filter`)
    :param b:              B-param for bicubic kernel (Default: 0)
    :param c:              C-param for bicubic kernel (Default: 1 / 2)
    :param taps:           Taps param for lanczos kernel (Default: 4)
    :param show_error:     Show diff between the original clip and the re-upscaled clip (Default: True)

    :return: A clip re-upscaled with the same kernel
    """
    try:
        from descale import get_filter
    except ModuleNotFoundError:
        raise ModuleNotFoundError("test_descale: missing dependency 'descale'")

    b = float(b)
    c = float(c)

    width = width or get_w(height, clip.width / clip.height)

    if get_depth(clip) != 32:
        clip = util.resampler(clip, 32)

    clip_y = get_y(clip)

    desc = get_filter(b, c, taps, kernel)(clip_y, width, height)
    upsc = util.get_scale_filter(kernel, b=b, c=c, taps=taps)(desc, clip.width, clip.height)
    upsc = core.std.PlaneStats(clip_y, upsc)

    if clip is vs.GRAY:
        return core.text.FrameProps(upsc, "PlaneStatsDiff") if show_error else upsc
    merge = core.std.ShufflePlanes([upsc, clip], [0, 1, 2], vs.YUV)
    return core.text.FrameProps(merge, "PlaneStatsDiff") if show_error else merge


# TODO: Write a function that checks every possible combination of B and C in bicubic
#       and returns a list of the results. Possibly return all the frames in order of
#       smallest difference to biggest. Not reliable, but maybe useful as starting point.


# TODO: Write "multi_descale", a function that allows you to descale a frame twice,
#       like for example when the CGI in a show is handled in a different resolution
#       than the drawn animation.
