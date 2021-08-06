"""
    Deblocking functions.
"""
from functools import partial
from typing import List, Optional, Sequence, Tuple, cast

import vapoursynth as vs
from vsutil import scale_value

from .types import Matrix

core = vs.core


def autodb_dpir(clip: vs.VideoNode, edgevalue: int = 24,
                strs: Sequence[float] = (30, 50, 75),
                thrs: Sequence[Tuple[float, float, float]] = [(1.5, 2.0, 2.0), (3.0, 4.5, 4.5), (5.5, 7.0, 7.0)],
                matrix: Optional[Matrix] = None,
                cuda: bool = True, device_index: int = 0,
                ) -> vs.VideoNode:
    """
    A rewrite of fvsfunc.AutoDeblock that uses vspdir instead of dfttest to deblock.

    This function checks for differences between a frame and an edgemask with some processing done on it,
    and for differences between the current frame and the next frame.
    For frames where both thresholds are exceeded, it will perform deblocking at a specified strength.
    This will ideally be frames that show big temporal *and* spatial inconsistencies.

    Thresholds and calculations are added to the frameprops to use as reference when setting the thresholds.

    Keep in mind that vsdpir is not perfect; it may cause weird, black dots to appear sometimes.
    If that happens, you can perform a denoise on the original clip (maybe even using vsdpir's denoising mode)
    and grab the brightest pixels from your two clips. That should return a perfectly fine clip.

    Thanks Vardë, louis, setsugen_no_ao!

    Dependencies:

    * vs-dpir
    * rgsf

    :param clip:            Input clip
    :param edgevalue:       Remove edges from the edgemask that exceed this threshold (higher means more edges removed)
    :param strs:            A list of DPIR strength values (higher means stronger deblocking).
                            You can pass any arbitrary number of values here.
                            The amount of values in strs and thrs need to be equal.
                            Note that the current highest vsdpir can go as of writing is ``strength=75``
    :param thrs:            A list of thresholds, written as [(EdgeValRef, NextFrameDiff, PrevFrameDiff)].
                            You can pass any arbitrary number of values here.
                            The amount of values in strs and thrs need to be equal.
    :param matrix:          Enum for the matrix of the input clip. See ``types.Matrix`` for more info.
                            If `None`, gets matrix from the "_Matrix" prop of the clip
    :param cuda:            Device type used for deblocking. Uses CUDA if True, else CPU
    :param device_index:    The 'device_index' + 1º device of type device type in the system

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

        evref_diff = scale_value(cast(float, f[0].props['EdgeValRefDiff']), 32, 8)
        y_next_diff = scale_value(cast(float, f[1].props['YNextDiff']), 32, 8)
        y_prev_diff = scale_value(cast(float, f[2].props['YPrevDiff']), 32, 8)
        f_type = cast(bytes, f[0].props['_PictType']).decode('utf-8')

        if f_type == 'I':
            y_next_diff = (y_next_diff + evref_diff) / 2

        for i, thr in enumerate(thrs):
            if evref_diff > thr[0] and y_next_diff > thr[1] and y_prev_diff > thr[2]:
                out, i = clips[i+1], i
                deblocked = True

        out = out.std.SetFrameProp('adb_EdgeValRefDiff', floatval=evref_diff) \
            .std.SetFrameProp('adb_YNextDiff', floatval=y_next_diff) \
            .std.SetFrameProp('adb_YPrevDiff', floatval=y_prev_diff)

        if deblocked:
            # TO-DO: Figure out why it doesn't appear to be adding these props
            out.std.SetFrameProp('adb_EdgeValRefDiff_threshold', floatval=thrs[i][0]) \
                .std.SetFrameProp('adb_YNextDiff_threshold', floatval=thrs[i][1]) \
                .std.SetFrameProp('adb_YPrevDiff_threshold', floatval=thrs[i][2])

        return out

    if len(strs) != len(thrs):
        raise ValueError('autodb_dpir: You must pass an equal amount of values to '
                         f'strenght {len(strs)} and thrs {len(thrs)}!')

    rgb = core.resize.Bicubic(clip, format=vs.RGBS, matrix_in=matrix)

    assert rgb.format

    maxvalue = (1 << rgb.format.bits_per_sample) - 1
    evref = core.std.Prewitt(rgb)
    evref = core.std.Expr(evref, f"x {edgevalue} >= {maxvalue} x ?")
    evref_rm = evref.rgsf.RemoveGrain(4).std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])

    diffevref = core.std.PlaneStats(evref, evref_rm, prop='EdgeValRef')
    diffnext = core.std.PlaneStats(rgb, rgb.std.DeleteFrames([0]), prop='YNext')
    diffprev = core.std.PlaneStats(rgb, rgb[0] + rgb, prop='YPrev')

    db_clips = [rgb] + [DPIR(rgb, strength=st, task='deblock', device_type='cuda' if cuda else 'cpu',
                        device_index=device_index).std.SetFrameProp('adb_DeblockStrength', floatval=st) for st in strs]

    debl = core.std.FrameEval(rgb, partial(_eval_db, clips=db_clips), prop_src=[diffevref, diffnext, diffprev])

    return core.resize.Bicubic(debl, format=clip.format.id, matrix=matrix)
