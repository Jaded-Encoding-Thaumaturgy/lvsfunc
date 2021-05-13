"""
    Denoising functions.
"""
from typing import Any, Dict, List, Optional, Union

import vapoursynth as vs
import vsutil

core = vs.core


def bm3d(clip: vs.VideoNode, matrix_s: str = "709", sigma: Union[float, List[float]] = 0.75,
         radius: Union[int, List[int], None] = None, ref: Optional[vs.VideoNode] = None,
         pre: Optional[vs.VideoNode] = None, refine: int = 1,
         basic_args: Dict[str, Any] = {}, final_args: Dict[str, Any] = {}) -> vs.VideoNode:
    assert clip.format is not None
    isGray = clip.format.color_family == vs.GRAY

    def to_opp(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.resize.Bicubic(format=vs.RGBS, matrix_in_s=matrix_s).bm3d.RGB2OPP(sample=1)

    def to_fullgray(clip: vs.VideoNode) -> vs.VideoNode:
        return vsutil.get_y(clip).resize.Point(format=vs.GRAYS, range_in=vsutil.Range.LIMITED, range=vsutil.Range.FULL)

    sigmal = [sigma] * 3 if not isinstance(sigma, list) else sigma + [sigma[-1]]*(3-len(sigma))
    sigmal = [sigmal[0], 0, 0] if isGray else sigmal
    isGray = True if sigmal[1] == 0 and sigmal[2] == 0 else isGray
    if len(sigmal) != 3:
        raise ValueError("bm3d: 'invalid number of sigma parameters supplied'")
    radiusl = [0, 0] if radius is None else [radius] * 2 if not isinstance(radius, list) \
        else radius + [radius[-1]]*(2-len(radius))
    if len(radiusl) != 2:
        raise ValueError("bm3d: 'invalid number or radius parameters supplied'")

    if sigmal[0] == 0 and sigmal[1] == 0 and sigmal[2] == 0:
        return clip

    pre = pre if pre is None else to_opp(pre) if not isGray else to_fullgray(pre)

    def basic(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.bm3d.Basic(sigma=sigmal, ref=pre, matrix=100, **basic_args) if radiusl[0] < 1 \
            else clip.bm3d.VBasic(sigma=sigmal, ref=pre, radius=radiusl[0], matrix=100, **basic_args) \
            .bm3d.VAggregate(radius=radiusl[0], sample=1)

    clip_in = to_opp(clip) if not isGray else to_fullgray(clip)
    refv = basic(clip_in) if ref is None else to_opp(ref) if not isGray else to_fullgray(ref)

    def final(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.bm3d.Final(sigma=sigmal, ref=refv, matrix=100, **final_args) if radiusl[1] < 1 \
            else clip.bm3d.VFinal(sigma=sigmal, ref=refv, radius=radiusl[1], matrix=100, **final_args) \
            .bm3d.VAggregate(radius=radiusl[1], sample=1)

    den = vsutil.vsutil.iterate(clip_in, final, refine)

    # boil everything back down to whatever input we had
    den = den.bm3d.OPP2RGB(sample=1).resize.Bicubic(format=clip.format.id, matrix_s=matrix_s) if not isGray \
        else den.resize.Point(format=clip.format.replace(color_family=vs.GRAY, subsampling_w=0, subsampling_h=0).id,
                              range_in=vsutil.Range.FULL, range=vsutil.Range.LIMITED)
    # merge source chroma if it exists and we didn't denoise it
    den = core.std.ShufflePlanes([den, clip], planes=[0, 1, 2], colorfamily=vs.YUV) \
        if isGray and clip.format.color_family == vs.YUV else den
    # sub clip luma back in if we only denoised chroma
    den = den if sigmal[0] != 0 else core.std.ShufflePlanes([clip, den], planes=[0, 1, 2], colorfamily=vs.YUV)

    return den
