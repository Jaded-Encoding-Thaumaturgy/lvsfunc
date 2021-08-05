"""
    Denoising/Deblocking functions.
"""
from functools import partial
from typing import Any, Dict, List, Optional, Tuple, Union, cast

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


def autodb_dpir(clip: vs.VideoNode, edgevalue: int = 24,
                strength: Tuple[int, int, int] = (30, 50, 75),
                thrs: List[Tuple[float, float]] = [(2.0, 1.0), (3.0, 3.25), (5.0, 7.5)],
                matrix: Optional[Matrix] = None,
                cuda: bool = True, device_index: int = 0,
                debug: bool = False) -> vs.VideoNode:
    """
    A rewrite of fvsfunc.AutoDeblock that uses vspdir instead of dfttest to deblock.

    This function checks for differences between a frame and an edgemask with some processing done on it,
    and for differences between the current frame and the next frame.
    For frames where both thresholds are exceeded, it will perform deblocking at a specified strength.
    This will ideally be frames that show big temporal *and* spatial inconsistencies.

    Dependencies:

    * vs-dpir
    * rgsf

    :param clip:            Input clip
    :param edgevalue:       Remove edges from the edgemask that exceed this threshold
    :param strength:        DPIR strength values (higher is stronger)
    :param thrs:            Invididual thresholds, written as a List of (OrigDiff, NextFrameDiff)
    :param matrix:          Enum for the matrix of the input clip. See ``types.Matrix`` for more info.
                            If `None`, gets matrix from the "_Matrix" prop of the clip
    :param cuda:            Device type used for deblocking. Uses CUDA if True, else CPU
    :param device_index:    The 'device_index' + 1º device of type device type in the system
    :param debug:           Print calculations and how strong the denoising is

    :return:                Deblocked clip
    """
    from vsdpir import DPIR

    assert clip.format

    def _eval_db(n: int, f: List[vs.VideoFrame], clips: List[vs.VideoNode]) -> vs.VideoNode:
        out = clips[0]
        mode, i, st = 'unfiltered passthrough', None, None
        orig_diff = scale_value(cast(float, f[0].props['OrigDiff']), 32, 8)
        y_next_diff = scale_value(cast(float, f[1].props['YNextDiff']), 32, 8)
        f_type = str(f[0].props['_PictType'])[2:3]  # This is very dumb it fuck bytes

        if f_type == 'I':
            y_next_diff = (y_next_diff + orig_diff) / 2

        if orig_diff > thrs[2][0] and y_next_diff > thrs[2][1]:
            out = clips[3]
            mode, i, st = 'strong deblocking', 2, strength[2]
        elif orig_diff > thrs[1][0] and y_next_diff > thrs[1][1]:
            out = clips[2]
            mode, i, st = 'medium deblocking', 1, strength[1]
        elif orig_diff > thrs[0][0] and y_next_diff > thrs[0][1]:
            out = clips[1]
            mode, i, st = 'weak deblocking', 0, strength[0]

        if debug:
            if i is not None:
                print(f'Frame {n} ({f_type}): {mode} (strength: {st}) '
                      f'/ OrigDiff: {orig_diff} (thr: {thrs[i][0]}) '
                      f'/ YNextDiff: {y_next_diff} (thr: {thrs[i][1]})')
            else:
                print(f'Frame {n} ({f_type}): {mode} / OrigDiff: {orig_diff} / YNextDiff: {y_next_diff}')
        return out

    dpir_args: Dict[str, Any] = {'device_type': cuda, 'device_index': device_index}

    original_format = clip.format

    if not matrix:
        matrix = cast(Matrix, get_prop(clip.get_frame(0), '_Matrix', int))

    if not clip.format.color_family == vs.RGB:
        clip = depth(clip, 32).std.SetFrameProp('_Matrix', intval=matrix)
        clip = core.resize.Bicubic(clip, format=vs.RGBS)

    maxvalue = (1 << original_format.bits_per_sample) - 1
    orig = core.std.Prewitt(clip)
    orig = core.std.Expr(orig, f"x {edgevalue} >= {maxvalue} x ?")
    orig_d = orig.rgsf.RemoveGrain(4).std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])

    difforig = core.std.PlaneStats(orig, orig_d, prop='Orig')
    diffnext = core.std.PlaneStats(clip, clip.std.DeleteFrames([0]), prop='YNext')

    db_weak = DPIR(clip, strength=strength[0], task='deblock', **dpir_args)
    db_med = DPIR(clip, strength=strength[1], task='deblock', **dpir_args)
    db_str = DPIR(clip, strength=strength[2], task='deblock', **dpir_args)
    db_clips = [clip, db_weak, db_med, db_str]

    debl = core.std.FrameEval(clip, partial(_eval_db, clips=db_clips), prop_src=[difforig, diffnext])

    return core.resize.Bicubic(debl, format=original_format.id, matrix=matrix)
