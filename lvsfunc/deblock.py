"""
    Deblocking functions.
"""
from functools import partial
from typing import List, Optional, Sequence, Tuple, cast

import vapoursynth as vs
from vsutil import depth, scale_value

from .types import Matrix
from .util import get_prop

core = vs.core


def autodb_dpir(clip: vs.VideoNode, edgevalue: int = 24,
                strs: Sequence[float] = (30, 50, 75),
                thrs: Sequence[Tuple[float, float, float]] = [(1.5, 2.0, 2.0), (3.0, 4.5, 4.5), (5.5, 7.0, 7.0)],
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
                            The amount of values in strs and thrs need to be equal.
                            Note that the current highest vsdpir can go as of writing is ``strength=75``
    :param thrs:            A list of thresholds, written as [(dbrefDiff, NextFrameDiff, PrevFrameDiff)].
                            You can pass any arbitrary number of values here.
                            The amount of values in strs and thrs need to be equal.
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
        raise ModuleNotFoundError("autodb_dpir: missing dependency 'vsdpir'")

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

    original_format = clip.format

    if len(strs) != len(thrs):
        raise ValueError('autodb_dpir: You must pass an equal amount of values to '
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

    db_clips = [clip] + [DPIR(clip, strength=st, task='deblock', device_type='cuda' if cuda else 'cpu',
                              device_index=device_index) for st in strs]

    debl = core.std.FrameEval(clip, partial(_eval_db, clips=db_clips), prop_src=[diffdbref, diffnext, diffprev])

    return core.resize.Bicubic(debl, format=original_format.id, matrix=matrix)
