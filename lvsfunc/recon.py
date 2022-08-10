from __future__ import annotations

from functools import partial

import vapoursynth as vs
from vsutil import depth, get_depth, join, split

from .types import RegressClips
from .util import check_variable

core = vs.core


__all__ = [
    'chroma_reconstruct',
    'reconstruct_multi',
    'regress',
]


def chroma_reconstruct(clip: vs.VideoNode, radius: int = 2, i444: bool = False) -> vs.VideoNode:
    """
    Chroma reconstruction filter using regress.

    This function should be used with care, and not blindly applied to anything.
    Ideally you should see how the function works,
    and then mangle the luma of your source to match how your chroma was mangled.

    This function can also return a 4:4:4 clip. This is not recommended
    except for very specific cases, like for example where you're
    dealing with a razor-sharp 1080p source with a lot of bright colours.
    Otherwise, have it return the 4:2:0 clip instead.

    Original function by shane, modified by Ichunjo and LightArrowsEXE.

    Aliases for this function are ``lvsfunc.demangle`` and ``lvsfunc.crecon``.

    :param clip:     Clip to process.
    :param radius:  Boxblur radius.
    :param i444:    Return a 4:4:4 clip.

    :return:        Clip with demangled chroma in either 4:2:0 or 4:4:4.
    """
    assert check_variable(clip, "chroma_reconstruct")

    def dmgl(clip: vs.VideoNode) -> vs.VideoNode:
        return core.resize.Bicubic(clip, w, h, src_left=0.25)

    w, h = clip.width, clip.height

    clipb = depth(clip, 32)
    planes = split(clipb)
    clip_y = planes[0]
    planes[0] = planes[0].resize.Bicubic(planes[1].width, planes[1].height,
                                         src_left=-.5, filter_param_a=1/3, filter_param_b=1/3)
    planes[0], planes[1], planes[2] = map(dmgl, (planes[0], planes[1], planes[2]))
    y_fix = core.std.MakeDiff(clip_y, planes[0])
    yu, yv = regress(planes[0], planes[1], planes[2], radius=radius)

    u_fix = reconstruct_multi(y_fix, yu, radius=radius)
    planes[1] = core.std.MergeDiff(planes[1], u_fix)
    v_fix = reconstruct_multi(y_fix, yv, radius=radius)
    planes[2] = core.std.MergeDiff(planes[2], v_fix)

    merged = join([clip_y, planes[1], planes[2]])
    return core.resize.Bicubic(merged, format=clip.format.id) if not i444 \
        else depth(merged, get_depth(clip))


def regress(x: vs.VideoNode, *ys: vs.VideoNode, radius: int = 2, eps: float = 1e-7) -> list[RegressClips]:
    """
    Regress a clip using mangled luma and chroma.

    Fit a line for every neighborhood of values of a given size in a clip
    with corresponding neighborhoods in one or more other clips.

    For more info see `this Wikipedia article <https://en.wikipedia.org/wiki/Simple_linear_regression>`_.

    :raises ValueError:     ``radius`` is lesser than 0.
    """
    if radius <= 0:
        raise ValueError("Regress: 'radius must be greater than 0!'")

    Expr = core.akarin.Expr
    E = partial(vs.core.std.BoxBlur, hradius=radius, vradius=radius)

    def mul(*c: vs.VideoNode) -> vs.VideoNode:
        return Expr(c, "x y *")

    def sq(c: vs.VideoNode) -> vs.VideoNode:
        return mul(c, c)

    Ex = E(x)
    Exx = E(sq(x))
    Eys = [E(y) for y in ys]
    Exys = [E(mul(x, y)) for y in ys]
    Eyys = [E(sq(y)) for y in ys]

    var_x = Expr((Exx, Ex), "x y dup * - 0 max")
    var_ys = [Expr((Eyy, Ey), "x y dup * - 0 max") for Eyy, Ey in zip(Eyys, Eys)]
    cov_xys = [Expr((Exy, Ex, Ey), "x y z * -") for Exy, Ey in zip(Exys, Eys)]

    slopes = [Expr((cov_xy, var_x), f"x y {eps} + /") for cov_xy in cov_xys]
    intercepts = [Expr((Ey, slope, Ex), "x y z * -") for Ey, slope in zip(Eys, slopes)]
    corrs = [
        Expr((cov_xy, var_x, var_y), f"x dup * y z * {eps} + / sqrt")
        for cov_xy, var_y in zip(cov_xys, var_ys)
    ]

    return [RegressClips(*x) for x in zip(slopes, intercepts, corrs)]


def reconstruct_multi(c: vs.VideoNode, r: RegressClips, radius: int = 2) -> vs.VideoNode:
    """
    Reconstruct regressed clips using a base video clip.

    :param c:       Original clip.
    :param r:       Regressed clips.
    :param radius:  Internal boxblur radii.

    :returns:       Fixed regressed clips.
    """
    assert check_variable(c, "reconstruct_multi")

    weights = core.akarin.Expr(r.correlation, 'x 0.5 - 0.5 / 0 max')
    slope_pm = core.akarin.Expr((r.slope, weights), 'x y *')
    slope_pm_sum = _mean(slope_pm, radius)
    recons = core.akarin.Expr((c, slope_pm_sum), 'x y *')
    return recons


def _mean(c: vs.VideoNode, radius: int) -> vs.VideoNode:
    return core.std.BoxBlur(c, hradius=radius, vradius=radius)
