"""
    Functions for (de)scaling.
"""
import math
from collections import namedtuple
from functools import partial
from typing import List, Optional

from descale import get_filter
from nnedi3_resample import \
    nnedi3_resample  # https://github.com/mawen1250/VapourSynth-script/blob/master/nnedi3_resample.py
from vsutil import get_depth, get_w, get_y, join, plane, split

import vapoursynth as vs

from . import aa, util

try:
    import nnedi3_rpow2 as nnp2                 # https://github.com/darealshinji/vapoursynth-plugins/blob/master/scripts/nnedi3_rpow2.py
except ImportError:
    import edi_rpow2 as nnp2                    # https://gist.github.com/YamashitaRen/020c497524e794779d9c

core = vs.core


def conditional_descale(clip: vs.VideoNode, height: int,
                        kernel: str = 'bicubic',
                        b: float = 1 / 3, c: float = 1 / 3,
                        taps: int = 4,
                        threshold: float = 0.003,
                        upscaler: str = "nnedi3_rpow2",
                        **upscale_args) -> vs.VideoNode:
    """
    Descales and reupscales a clip; if the difference exceeds the threshold, the frame will not be descaled.
    If it does not exceed the threshold, the frame will upscaled using either nnedi3_rpow2 or waifu2x-caffe.

    Useful for bad BDs that have additional post-processing done on some scenes, rather than all of them.

    Currently only works with bicubic, and has no native 1080p masking.
    Consider scenefiltering OP/EDs with a different descale function instead.

    The code for _get_error was mostly taken from kageru's Made in Abyss script.
    Special thanks to Lypheo for holding my hand as this was written.

    :param clip:                   Input clip
    :param height:                 Target descale height
    :param kernel:                 Kernel used to descale (see :py:func:`lvsfunc.util.get_scale_filter`, Default: bicubic)
    :param b:                      B-param for bicubic kernel (Default: 1 / 3)
    :param c:                      C-param for bicubic kernel (Default: 1 / 3)
    :param taps:                   Taps param for lanczos kernel (Default: 4)
    :param threshold:              Threshold for deciding to descale or leave the original frame (Default: 0.003)
    :param upscaler:               Which upscaler to use ("nnedi3_rpow2" (default), "upscaled_sraa", "waifu2x" (caffe))
    :param upscale_args:           Arguments passed to upscaler

    :return:                       Constant-resolution rescaled clip
    """
    def _get_error(clip, height, kernel, b, c, taps):
        descale = get_filter(b, c, taps, kernel)(clip, get_w(height, clip.width / clip.height), height)
        upscale = util.get_scale_filter(kernel, b=b, c=c, taps=taps)(clip, clip.width, clip.height)
        diff = core.std.PlaneStats(upscale, clip)
        return descale, diff

    def _diff(n, f, clip_a, clip_b, threshold):
        return clip_a if f.props.PlaneStatsDiff > threshold else clip_b

    if get_depth(clip) != 32:
        clip = util.resampler(clip, 32)

    planes = split(clip)
    descaled, diff = _get_error(planes[0], height=height, kernel=kernel, b=b, c=c, taps=taps)

    if upscaler in ['nnedi3_rpow2', 'nnedi3', 'nn3_rp2']:
        planes[0] = nnp2(descaled, upscale_args, width=clip.width, height=clip.height)
    elif upscaler in ['nnedi3_resample', 'nn3_res']:
        nnargs = dict(kernel='gauss', invks=True, invkstaps=2, taps=1, a1=32, nns=4, qual=2, pscrn=4) or upscale_args
        planes[0] = nnedi3_resample(descaled, clip.width, clip.height, nnargs)
    elif upscaler in ['upscaled_sraa', 'up_sraa', 'sraa']:
        srargs = dict(sharp_downscale=False) or upscale_args
        planes[0] = aa.upscaled_sraa(descaled, srargs, h=clip.height)
    elif upscaler in ['waifu2x', 'w2x']:
        w2xargs = dict(noise=-1, scale=2, model=6, cudnn=True, processor=0, tta=False) or upscale_args
        planes[0] = core.caffe.Waifu2x(descaled, w2xargs).resize.Spline36(clip.width, clip.height)
    else:
        raise ValueError(f"conditional_descale: '\"{upscaler}\" is not a valid option for \"upscaler\". Please pick either \"nnedi3_rpow2\", \"nnedi3_resample\", \"upscaled_sraa\", or \"waifu2x\"'")


    descaled = join(planes).resize.Spline36(format=clip.format)
    descaled = descaled.std.SetFrameProp("_descaled", intval=1)
    clip = clip.std.SetFrameProp("_descaled", intval=0)

    return core.std.FrameEval(clip, partial(_diff, clip_a=clip, clip_b=descaled, threshold=threshold),  diff)


def smart_descale(clip: vs.VideoNode,
                  resolutions: List[int],
                  kernel: str = 'bicubic',
                  b: float = 0, c: float = 1/2, taps: int = 4,
                  thr: float = 0.05, rescale: bool = False) -> vs.VideoNode:
    """
    Allows you to descale to multiple native resolutions.
    Written by kageru, and slightly adjusted by me. Thanks Varde for helping me fix some bugs with it.

    This function will descale clips to multiple resolutions and return the descaled clip
    that is mostly likely to be the actual resolution of the clip. This is useful for shows
    like Shield Hero, Made in Abyss, or Symphogear that love jumping between multiple resolutions.

    The returned clip will be multiple resolutions, meaning most resamplers will break,
    as well as encoding it as-is. When handling it, please ensure you return the clip to
    a steady resolution before further processing.

    Setting rescaled will use `smart_rescaler` to reupscale the clip to its original resolution.
    This will return a proper YUV clip as well. If rescaled is set to False, the returned clip
    will be GRAY.

    :param clip:             Input clip
    :param resolutions:      A list of resolutions to descale to
    :param kernel:           Kernel used to descale (see :py:func:`lvsfunc.util.get_scale_filter`, Default: bicubic)
    :param b:                B-param for bicubic kernel (Default: 1 / 3)
    :param c:                C-param for bicubic kernel (Default: 1 / 3)
    :param taps:             Taps param for lanczos kernel (Default: 4)
    :param thr:              Threshold for when a clip is discerned as "non-scaleable" (Default: 0.05)
    :param rescale:          Rescale the clip to the original resolution after descaling (Default: False)

    :return:                 Variable-resolution clip containing descaled frames
    """
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
        core.std.BlankClip(clip, length=len(clip)-1), core.std.BlankClip(clip, length=1, width=clip.width + 1)
    ], mismatch=True)

    def _select_descale(n: int, f: List[vs.VideoFrame]):
        best_res = max(f, key=lambda frame: math.log(clip.height - frame.props.descaleResolution, 2) * round(1/max(frame.props.PlaneStatsAverage, 1e-12)) ** 0.2)

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


def smart_reupscale(clip: vs.VideoNode, width: Optional[int] = None, height: int = 1080,
                    kernel: str = 'bicubic', b: float = 0, c: float = 1 / 2, taps: int = 4,
                    **znargs) -> vs.VideoNode:
    """
    A quick 'n easy wrapper used to re-upscale a clip descaled with smart_descale.
    Uses znedi3, which seems to miraculously work with a multi-res clip.

    Stolen from Varde.

    :param clip:         Input clip
    :param width:        Upscale width. If None, determine from `height` assuming 16:9 aspect ratio (Default: None)
    :param height:       Upscale height (Default: 1080)
    :param kernel:       Kernel used to upscale (see :py:func:`lvsfunc.util.get_scale_filter`)
    :param b:            B-param for bicubic kernel (Default: 0)
    :param c:            C-param for bicubic kernel (Default: 1 / 2)
    :param taps:         Taps param for lanczos kernel. (Default: 4)
    :param znargs:       Arguments passed to znedi3

    :return:             Reupscaled clip
    """
    def _transpose_shift(n, f, clip):
        try:
            h = f.props['descaleResolution']
        except:
            raise ValueError(f"smart_reupscale: 'This clip was not descaled using smart_descale'")
        w = get_w(h)
        clip = core.resize.Bicubic(clip, w, h*2, src_top=.5)
        clip = core.std.Transpose(clip)
        return clip

    width = width or get_w(height)

    # Doubling and downscale to given "h"
    znargs = dict(field=0, dh=True, nsize=4, nns=4, qual=2) or znargs

    clip_c = clip
    if get_depth(clip) == 32:
        clip = util.resampler(clip, 16)

    try:
        upsc = core.znedi3.nnedi3(clip, **znargs)
    except:
        upsc = util.resampler(core.znedi3.nnedi3(util.resampler(clip, 16), **znargs), get_depth(clip))
    upsc = core.std.FrameEval(upsc, partial(_transpose_shift, clip=upsc), prop_src=upsc)
    upsc = core.znedi3.nnedi3(upsc, **znargs)
    return util.resampler(util.get_scale_filter(kernel, b=b, c=c, taps=taps)(upsc, height, width, src_top=.5).std.Transpose(), get_depth(clip_c))


def test_descale(clip: vs.VideoNode,
                 height: int,
                 kernel: str = 'bicubic',
                 b: float = 1 / 3, c: float = 1 / 3,
                 taps: int = 3,
                 show_error: bool = True) -> vs.VideoNode:
    """
    Generic function to test descales with;
    descales and reupscales a given clip, allowing you to compare the two easily.

    When comparing, it is recommended to do atleast a 4x zoom using Nearest Neighbor.
    I also suggest using 'compare', as that will make comparison a lot easier.

    Some of this code was leveraged from DescaleAA found in fvsfunc.

    :param clip:           Input clip
    :param height:         Target descaled height.
    :param kernel:         Kernel used to descale (see :py:func:`lvsfunc.util.get_scale_filter`)
    :param b:              B-param for bicubic kernel (Default: 1 / 3)
    :param c:              C-param for bicubic kernel (Default: 1 / 3)
    :param taps:           Taps param for lanczos kernel (Default: 3)
    :param show_error:     Show diff between the original clip and the reupscaled clip (Default: True)

    :return: A clip re-upscaled with the same kernel
    """
    if get_depth(clip) != 32:
        clip = util.resampler(clip, 32)

    clip_y = get_y(clip)

    desc = get_filter(b, c, taps, kernel)(clip_y, get_w(height, clip.width / clip.height), height)
    upsc = util.get_scale_filter(kernel, b=b, c=c, taps=taps)(desc, clip.width, clip.height)
    upsc = core.std.PlaneStats(clip_y, upsc)

    if clip is vs.GRAY:
        return core.text.FrameProps(upsc, "PlaneStatsDiff") if show_error else upsc
    merge = core.std.ShufflePlanes([upsc, clip], [0, 1, 2], vs.YUV)
    return core.text.FrameProps(merge, "PlaneStatsDiff") if show_error else merge


# TO-DO: Write a function that checks every possible combination of B and C in bicubic
#        and returns a list of the results. Possibly return all the frames in order of
#        smallest difference to biggest. Not reliable, but maybe useful as starting point.


# TO-DO: Write "multi_descale", a function that allows you to descale a frame twice,
#        like for example when the CGI in a show is handled in a different resolution
#        than the drawn animation.
