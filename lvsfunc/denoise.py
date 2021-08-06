"""
    Denoising/Deblocking functions.
"""
from functools import partial
from typing import Any, Dict, List, Optional, Sequence, Union, cast

import vapoursynth as vs
import vsutil
from vsutil import depth, scale_value

from .types import Matrix
from .util import get_prop

core = vs.core


def bm3d(clip: vs.VideoNode, sigma: Union[float, List[float]] = 0.75,
         radius: Union[int, List[int], None] = None, ref: Optional[vs.VideoNode] = None,
         pre: Optional[vs.VideoNode] = None, refine: int = 1, matrix_s: str = "709",
         basic_args: Dict[str, Any] = {}, final_args: Dict[str, Any] = {}) -> vs.VideoNode:
    """
    A wrapper function for the BM3D denoiser.

    Dependencies:

    * VapourSynth-BM3D

    :param clip:            Input clip
    :param sigma:           Denoising strength for both basic and final estimations
    :param radius:          Temporal radius for both basic and final estimations
    :param ref:             Reference clip for the final estimation
    :param pre:             Prefiltered clip for the basic estimation
    :param refine:          Iteration of the final clip.
                            0 = basic estimation only
                            1 = basic + final estimation
                            n = basic + n final estimations
    :param matrix_s:        Color matrix of the input clip
    :param basic_args:      Args to pass to the basic estimation
    :param final_args:      Args to pass to the final estimation

    :return:                Denoised clip
    """
    if clip.format is None:
        raise ValueError("bm3d: Variable format clips not supported")
    is_gray = clip.format.color_family == vs.GRAY

    def to_opp(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.resize.Bicubic(format=vs.RGBS, matrix_in_s=matrix_s).bm3d.RGB2OPP(sample=1)

    def to_fullgray(clip: vs.VideoNode) -> vs.VideoNode:
        return vsutil.get_y(clip).resize.Point(format=vs.GRAYS, range_in=vsutil.Range.LIMITED, range=vsutil.Range.FULL)

    sigmal = [sigma] * 3 if not isinstance(sigma, list) else sigma + [sigma[-1]]*(3-len(sigma))
    sigmal = [sigmal[0], 0, 0] if is_gray else sigmal
    is_gray = True if sigmal[1] == 0 and sigmal[2] == 0 else is_gray
    if len(sigmal) != 3:
        raise ValueError("bm3d: 'invalid number of sigma parameters supplied'")
    radiusl = [0, 0] if radius is None else [radius] * 2 if not isinstance(radius, list) \
        else radius + [radius[-1]]*(2-len(radius))
    if len(radiusl) != 2:
        raise ValueError("bm3d: 'invalid number or radius parameters supplied'")

    if sigmal[0] == 0 and sigmal[1] == 0 and sigmal[2] == 0:
        return clip

    pre = pre if pre is None else to_opp(pre) if not is_gray else to_fullgray(pre)

    def basic(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.bm3d.Basic(sigma=sigmal, ref=pre, matrix=100, **basic_args) if radiusl[0] < 1 \
            else clip.bm3d.VBasic(sigma=sigmal, ref=pre, radius=radiusl[0], matrix=100, **basic_args) \
            .bm3d.VAggregate(radius=radiusl[0], sample=1)

    clip_in = to_opp(clip) if not is_gray else to_fullgray(clip)
    refv = basic(clip_in) if ref is None else to_opp(ref) if not is_gray else to_fullgray(ref)

    def final(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.bm3d.Final(sigma=sigmal, ref=refv, matrix=100, **final_args) if radiusl[1] < 1 \
            else clip.bm3d.VFinal(sigma=sigmal, ref=refv, radius=radiusl[1], matrix=100, **final_args) \
            .bm3d.VAggregate(radius=radiusl[1], sample=1)

    den = vsutil.iterate(clip_in, final, refine)

    # boil everything back down to whatever input we had
    den = den.bm3d.OPP2RGB(sample=1).resize.Bicubic(format=clip.format.id, matrix_s=matrix_s) if not is_gray \
        else den.resize.Point(format=clip.format.replace(color_family=vs.GRAY, subsampling_w=0, subsampling_h=0).id,
                              range_in=vsutil.Range.FULL, range=vsutil.Range.LIMITED)
    # merge source chroma if it exists and we didn't denoise it
    den = core.std.ShufflePlanes([den, clip], planes=[0, 1, 2], colorfamily=vs.YUV) \
        if is_gray and clip.format.color_family == vs.YUV else den
    # sub clip luma back in if we only denoised chroma
    den = den if sigmal[0] != 0 else core.std.ShufflePlanes([clip, den], planes=[0, 1, 2], colorfamily=vs.YUV)

    return den


def autodb(clip: vs.VideoNode, edgevalue: int = 24,
           strs: Sequence[float] = (30, 50, 75),
           thrs: List[Sequence[float]] = [(1.5, 2.0, 2.0), (3.0, 4.5, 4.5), (5.5, 7.0, 7.0)],
           matrix: Optional[Matrix] = None,
           cuda: bool = True, device_index: int = 0,
           debug: bool = False) -> vs.VideoNode:
    """
    A rewrite of fvsfunc.AutoDeblock that uses vspdir instead of dfttest to deblock.

    This function checks for differences between a frame and an edgemask with some processing done on it,
    and for differences between the current frame and the next frame.
    For frames where both thresholds are exceeded, it will perform deblocking at a specified strength.
    This will ideally be frames that show big temporal *and* spatial inconsistencies.

    Keep in mind that vsdpir is not perfect; it may cause weird, black dots to appear sometimes.
    If that happens, you can perform a denoise on the original clip (maybe even using vsdpir's denoising mode)
    and grab the brightest pixels from your two clips. That should return a perfectly fine clip.

    Dependencies:

    * vs-dpir
    * rgsf

    :param clip:            Input clip
    :param edgevalue:       Remove edges from the edgemask that exceed this threshold (higher means more edges removed)
    :param strs:            A list of DPIR strength values (higher means stronger deblocking).
                            You can pass any arbitrary number of values here.
                            Note that the current highest vsdpir can go as of writing is ``strength=75``
    :param thrs:            A list of thresholds, written as [(dbrefDiff, NextFrameDiff, PrevFrameDiff)].
                            You can pass any arbitrary number of values here.
                            ``debug`` may help with setting this.
    :param matrix:          Enum for the matrix of the input clip. See ``types.Matrix`` for more info.
                            If `None`, gets matrix from the "_Matrix" prop of the clip
    :param cuda:            Device type used for deblocking. Uses CUDA if True, else CPU
    :param device_index:    The 'device_index' + 1º device of type device type in the system
    :param debug:           Print calculations and strength of deblocking on current frame

    :return:                Deblocked clip
    """
    try:
        from vsdpir import DPIR
    except ModuleNotFoundError:
        raise ModuleNotFoundError("autodb: missing dependency 'vsdpir'")

    assert clip.format

    def _eval_db(n: int, f: List[vs.VideoFrame], clips: List[vs.VideoNode]) -> vs.VideoNode:
        out = clips[0]
        deblocked = False

        dbref_diff = scale_value(cast(float, f[0].props['dbrefDiff']), 32, 8)
        y_next_diff = scale_value(cast(float, f[1].props['YNextDiff']), 32, 8)
        y_prev_diff = scale_value(cast(float, f[2].props['YPrevDiff']), 32, 8)
        f_type = cast(bytes, f[0].props['_PictType']).decode('utf-8')

        if f_type == 'I':
            y_next_diff = (y_next_diff + dbref_diff) / 2

        for i, thr in enumerate(thrs):
            if dbref_diff > thr[0] and y_next_diff > thr[1] and y_prev_diff > thr[2]:
                out, st, i = clips[i+1], strs[i], i
                deblocked = True

        if debug:
            if deblocked:
                print(f'Frame {n} ({f_type}): deblocked (strength: {st}) '
                      f'/ dbrefDiff: {dbref_diff:.6f} (thr: {thrs[i][0]}) '
                      f'/ YNextDiff: {y_next_diff:.6f} (thr: {thrs[i][1]}) '
                      f'/ YPrevDiff: {y_prev_diff:.6f} (thr: {thrs[i][2]})')
            else:
                print(f'Frame {n} ({f_type}): unfiltered / dbrefDiff: {dbref_diff:.6f} '
                      f'/ YNextDiff: {y_next_diff:.6f} / YPrevDiff: {y_prev_diff:.6f}')
        return out

    dpir_args: Dict[str, Any] = {'device_type': 'cuda' if cuda else 'cpu', 'device_index': device_index}

    original_format = clip.format

    if len(strs) != len(thrs):
        raise ValueError('autodb: You must pass an equal amount of values to '
                         f'strenght {len(strs)} and thrs {len(thrs)}!')

    if not matrix:
        matrix = cast(Matrix, get_prop(clip.get_frame(0), '_Matrix', int))

    if not clip.format.color_family == vs.RGB:
        clip = depth(clip, 32).std.SetFrameProp('_Matrix', intval=matrix)
        clip = core.resize.Bicubic(clip, format=vs.RGBS)

    maxvalue = (1 << original_format.bits_per_sample) - 1
    dbref = core.std.Prewitt(clip)
    dbref = core.std.Expr(dbref, f"x {edgevalue} >= {maxvalue} x ?")
    dbref_rm = dbref.rgsf.RemoveGrain(4).std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])

    diffdbref = core.std.PlaneStats(dbref, dbref_rm, prop='dbref')
    diffnext = core.std.PlaneStats(clip, clip.std.DeleteFrames([0]), prop='YNext')
    diffprev = core.std.PlaneStats(clip, clip[0] + clip, prop='YPrev')

    db_clips = [clip]
    for st in strs:
        db_clips += [DPIR(clip, strength=st, task='deblock', **dpir_args)]

    debl = core.std.FrameEval(clip, partial(_eval_db, clips=db_clips), prop_src=[diffdbref, diffnext, diffprev])

    return core.resize.Bicubic(debl, format=original_format.id, matrix=matrix)
