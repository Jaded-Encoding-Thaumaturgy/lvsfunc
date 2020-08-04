"""
    Functions for (de)scaling.
"""
import math
from functools import partial
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Tuple, Union, cast

import vapoursynth as vs
from vsutil import depth, get_depth, get_w, get_y, iterate, join, plane

from . import kernels, util

try:
    from cytoolz import functoolz
except ModuleNotFoundError:
    try:
        from toolz import functoolz  # type: ignore
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Cannot find functoolz: Please install toolz or cytoolz")

core = vs.core


class Resolution(NamedTuple):
    """ Tuple representing a resolution. """

    width: int
    """ Width. """

    height: int
    """ Height. """


class ScaleAttempt(NamedTuple):
    """ Tuple representing a descale attempt. """

    descaled: vs.VideoNode
    """ Descaled frame in native resolution. """

    rescaled: vs.VideoNode
    """ Descaled frame reupscaled with the same kernel. """

    resolution: Resolution
    """ The native resolution. """

    diff: vs.VideoNode
    """ The subtractive difference between the original and descaled frame. """


def _transpose_shift(n: int, f: vs.VideoFrame, clip: vs.VideoNode,
                     kernel: kernels.Kernel, caller: str) -> vs.VideoNode:
    h = f.height
    w = f.width
    clip = kernel.scale(clip, w, h*2, (0.5, 0))
    return core.std.Transpose(clip)


def _perform_descale(resolution: Resolution, clip: vs.VideoNode,
                     kernel: kernels.Kernel) -> ScaleAttempt:
    descaled = kernel.descale(clip, resolution.width, resolution.height) \
        .std.SetFrameProp('descaleResolution', intval=resolution.height)
    rescaled = kernel.scale(descaled, clip.width, clip.height)
    diff = core.std.Expr([rescaled, clip], 'x y - abs').std.PlaneStats()
    return ScaleAttempt(descaled, rescaled, resolution, diff)


def _select_descale(n: int, f: Union[vs.VideoFrame, List[vs.VideoFrame]],
                    threshold: float, clip: vs.VideoNode,
                    clips_by_resolution: Dict[int, ScaleAttempt]
                    ) -> vs.VideoNode:
    if type(f) is vs.VideoFrame:
        f = [cast(vs.VideoFrame, f)]
    f = cast(List[vs.VideoFrame], f)
    best_res = max(f, key=lambda frame:
                   math.log(clip.height - util.get_prop(frame, "descaleResolution", int), 2)
                   * round(1 / max(util.get_prop(frame, "PlaneStatsAverage", float), 1e-12))
                   ** 0.2)

    best_attempt = clips_by_resolution[util.get_prop(best_res, "descaleResolution", int)]
    if threshold == 0:
        return best_attempt.descaled
    if util.get_prop(best_res, "PlaneStatsAverage", float) > threshold:
        return clip
    return best_attempt.descaled


@functoolz.curry
def reupscale(clip: vs.VideoNode,
              width: Optional[int] = None, height: int = 1080,
              kernel: kernels.Kernel = kernels.Bicubic(b=0, c=1/2),
              **kwargs: Any) -> vs.VideoNode:
    """
    A quick 'n easy wrapper used to re-upscale a clip descaled with descale using znedi3.

    Function is curried to allow parameter tuning when passing to :py:func:`lvsfunc.scale.descale`

    Stolen from Varde with some adjustments made.

    Dependencies: znedi3

    :param clip:         Input clip
    :param width:        Upscale width. If None, determine from `height` assuming 16:9 aspect ratio (Default: None)
    :param height:       Upscale height (Default: 1080)
    :param kernel:       Kernel used to downscale the doubled clip (see :py:class:`lvsfunc.kernels.Kernel`,
                         Default: kernels.Bicubic(b=0, c=1/2))
    :param kwargs:       Arguments passed to znedi3 (Default: nsize=4, nns=4, qual=2, pscrn=2)

    :return:             Reupscaled clip
    """

    width = width or get_w(height)

    # Doubling and downscale to given "h"
    znargs = dict(nsize=4, nns=4, qual=2, pscrn=2)
    znargs.update(kwargs)

    upsc = util.quick_resample(clip, partial(core.znedi3.nnedi3, field=0,
                                             dh=True, **znargs))
    upsc = core.std.FrameEval(upsc, partial(_transpose_shift, clip=upsc,
                                            kernel=kernel,
                                            caller="reupscale"),
                              prop_src=upsc)
    upsc = util.quick_resample(upsc, partial(core.znedi3.nnedi3, field=0,
                                             dh=True, **znargs))
    return kernel.scale(upsc, width=height, height=width, shift=(0.5, 0)) \
        .std.Transpose()


@functoolz.curry
def descale_detail_mask(clip: vs.VideoNode, rescaled_clip: vs.VideoNode,
                        threshold: float = 0.05) -> vs.VideoNode:
    """
    Generate a detail mask given a clip and a clip rescaled with the same
    kernel.

    Function is curried to allow parameter tuning when passing to :py:func:`lvsfunc.scale.descale`

    :param clip:           Original clip
    :param rescaled_clip:  Clip downscaled and reupscaled using the same kernel
    :param threshold:      Binarization threshold for mask (Default: 0.05)

    :return:               Mask of lost detail
    """
    mask = core.std.Expr([get_y(clip), get_y(rescaled_clip)], 'x y - abs') \
        .std.Binarize(threshold)
    mask = iterate(mask, core.std.Maximum, 4)
    return iterate(mask, core.std.Inflate, 2)


def descale(clip: vs.VideoNode,
            upscaler:
            Optional[Callable[[vs.VideoNode, int, int], vs.VideoNode]]
            = reupscale,
            width: Union[int, List[int], None] = None,
            height: Union[int, List[int]] = 720,
            kernel: kernels.Kernel = kernels.Bicubic(b=0, c=1/2),
            threshold: float = 0.0,
            mask: Optional[Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode]]
            = descale_detail_mask, src_left: float = 0.0, src_top: float = 0.0,
            show_mask: bool = False) -> vs.VideoNode:
    """
    A unified descaling function.
    Includes support for handling fractional resolutions (experimental),
    multiple resolutions, detail masking, and conditional scaling.

    If you want to descale to a fractional resolution,
    set src_left and src_top and round up the target height.

    If the source has multiple native resolutions, specify ``height``
    as a list.

    If you want to conditionally descale, specify a non-zero threshold.

    Dependencies: vapoursynth-descale, znedi3

    :param clip:                    Clip to descale
    :param upscaler:                Callable function with signature upscaler(clip, width, height)
                                    -> vs.VideoNode to be used for reupscaling.
                                    Must be capable of handling variable res clips
                                    for multiple heights and conditional scaling.
                                    If a single height is given and upscaler is None,
                                    a constant resolution GRAY clip will be returned instead.
                                    Note that if upscaler is None, no upscaling will be performed
                                    and neither detail masking nor proper fractional descaling can be preformed.
                                    (Default: :py:func:`lvsfunc.scale.reupscale`)
    :param width:                   Width to descale to (if None, auto-calculated)
    :param height:                  Height(s) to descale to. List indicates multiple resolutions,
                                    the function will determine the best. (Default: 720)
    :param kernel:                  Kernel used to descale (see :py:class:`lvsfunc.kernels.Kernel`,
                                    (Default: kernels.Bicubic(b=0, c=1/2))
    :param threshold:               Error threshold for conditional descaling (Default: 0.0, always descale)
    :param mask:                    Function used to mask detail. If ``None``, no masking.
                                    Function must accept a clip and a reupscaled clip and return a mask.
                                    (Default: :py:func:`lvsfunc.scale.descale_detail_mask`)
    :param src_left:                Horizontal shifting for fractional resolutions (Default: 0.0)
    :param src_top:                 Vertical shifting for fractional resolutions (Default: 0.0)
    :param show_mask:               Return detail mask

    :return:                       Descaled and re-upscaled clip
    """
    if clip.format is None:
        raise ValueError("descale: 'Variable-format clips not supported'")

    if type(height) is int:
        height = [cast(int, height)]

    height = cast(List[int], height)

    if type(width) is int:
        width = [cast(int, width)]
    elif width is None:
        width = [get_w(h, aspect_ratio=clip.width/clip.height) for h in height]

    width = cast(List[int], width)

    if len(width) != len(height):
        raise ValueError("descale: Asymmetric number of heights and widths specified")

    resolutions = [Resolution(*r) for r in zip(width, height)]

    clip_y = depth(get_y(clip), 32) \
        .std.SetFrameProp('descaleResolution', intval=clip.height)

    variable_res_clip = core.std.Splice([
        core.std.BlankClip(clip_y, length=len(clip) - 1),
        core.std.BlankClip(clip_y, length=1, width=clip.width + 1)
    ], mismatch=True)

    descale_partial = partial(_perform_descale, clip=clip_y, kernel=kernel)
    clips_by_resolution = {c.resolution.height:
                           c for c in map(descale_partial, resolutions)}

    props = [c.diff for c in clips_by_resolution.values()]
    select_partial = partial(_select_descale, threshold=threshold,
                             clip=clip_y,
                             clips_by_resolution=clips_by_resolution)

    descaled = core.std.FrameEval(variable_res_clip, select_partial,
                                  prop_src=props)

    if src_left != 0 or src_top != 0:
        descaled = core.resize.Bicubic(descaled, src_left=src_left,
                                       src_top=src_top)

    if upscaler is None:
        upscaled = descaled
        if len(height) == 1:
            upscaled = core.resize.Point(upscaled, width[0], height[0])
        else:
            return upscaled
    else:
        upscaled = upscaler(descaled, clip.width, clip.height)

    if src_left != 0 or src_top != 0:
        upscaled = core.resize.Bicubic(descaled, src_left=-src_left,
                                       src_top=-src_top)

    if upscaled.format is None:
        raise RuntimeError("descale: 'Upscaler cannot return variable-format clips'")

    if mask:
        clip_y = clip_y.resize.Point(format=upscaled.format.id)
        rescaled = kernel.scale(descaled, clip.width, clip.height,
                                (src_left, src_top))
        rescaled = rescaled.resize.Point(format=clip.format.id)
        dmask = mask(clip_y, rescaled)

        if upscaler is None:
            dmask = core.resize.Spline36(dmask, upscaled.width, upscaled.height)
            clip_y = core.resize.Spline36(clip_y, upscaled.width, upscaled.height)

        if show_mask:
            return dmask

        upscaled = core.std.MaskedMerge(upscaled, clip_y, dmask)

    upscaled = depth(upscaled, get_depth(clip))

    if clip.format.num_planes == 1 or upscaler is None:
        return upscaled
    return join([upscaled, plane(clip, 1), plane(clip, 2)])


def test_descale(clip: vs.VideoNode,
                 width: Optional[int] = None, height: int = 720,
                 kernel: kernels.Kernel = kernels.Bicubic(b=0, c=1/2),
                 show_error: bool = True) -> Tuple[vs.VideoNode, ScaleAttempt]:
    """
    Generic function to test descales with;
    descales and reupscales a given clip, allowing you to compare the two easily.
    Also returns a :py:class:`lvsfunc.scale.ScaleAttempt` with additional
    information.

    When comparing, it is recommended to do atleast a 4x zoom using Nearest Neighbor.
    I also suggest using 'compare' (:py:func:`lvsfunc.comparison.compare`),
    as that will make comparing the output with the source clip a lot easier.

    Some of this code was leveraged from DescaleAA found in fvsfunc.

    Dependencies: vapoursynth-descale

    :param clip:           Input clip
    :param width:          Target descale width. If None, determine from `height`
    :param height:         Target descale height (Default: 720)
    :param kernel:         Kernel used to descale (see :py:class:`lvsfunc.kernels.Kernel`,
                           Default: kernels.Bicubic(b=0, c=1/2))
    :param show_error:     Render PlaneStatsDiff on the reupscaled frame (Default: True)

    :return: A tuple containing a clip re-upscaled with the same kernel and
             a ScaleAttempt tuple.
    """
    if clip.format is None:
        raise ValueError("test_descale: 'Variable-format clips not supported'")

    width = width or get_w(height, clip.width / clip.height)

    clip_y = depth(get_y(clip), 32)

    descale = _perform_descale(Resolution(width, height), clip_y, kernel)
    rescaled = depth(core.std.PlaneStats(descale.rescaled, clip_y), get_depth(clip))

    if clip.format.num_planes == 1:
        rescaled = core.text.FrameProps(rescaled, "PlaneStatsDiff") if show_error else rescaled
    else:
        merge = core.std.ShufflePlanes([rescaled, clip], [0, 1, 2], vs.YUV)
        rescaled = core.text.FrameProps(merge, "PlaneStatsDiff") if show_error else merge

    return rescaled, descale


# TODO: Write a function that checks every possible combination of B and C in bicubic
#       and returns a list of the results. Possibly return all the frames in order of
#       smallest difference to biggest. Not reliable, but maybe useful as starting point.


# TODO: Write "multi_descale", a function that allows you to descale a frame twice,
#       like for example when the CGI in a show is handled in a different resolution
#       than the drawn animation.
