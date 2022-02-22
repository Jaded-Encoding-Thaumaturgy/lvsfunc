"""
    Deblocking functions and wrappers.
"""
from __future__ import annotations

from functools import partial
from typing import Any, Optional, Sequence, SupportsFloat, Tuple

import vapoursynth as vs
from vsutil import (Dither, depth, disallow_variable_format,
                    disallow_variable_resolution, get_depth)

from .kernels import Catrom, Kernel
from .types import Matrix
from .util import get_prop

core = vs.core


@disallow_variable_format
@disallow_variable_resolution
def autodb_dpir(clip: vs.VideoNode, edgevalue: int = 24,
                strs: Sequence[float] = [30, 50, 75],
                thrs: Sequence[Tuple[float, float, float]] = [(1.5, 2.0, 2.0), (3.0, 4.5, 4.5), (5.5, 7.0, 7.0)],
                matrix: Optional[Matrix | int] = None,
                cuda: bool = True,
                write_props: bool = False,
                **vsdpir_args: Any) -> vs.VideoNode:
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

    :param clip:            Input clip
    :param edgevalue:       Remove edges from the edgemask that exceed this threshold (higher means more edges removed)
    :param strs:            A list of DPIR strength values (higher means stronger deblocking).
                            You can pass any arbitrary number of values here.
                            Sane deblocking strenghts lie between 1–20 for most regular deblocking.
                            Going higher than 50 is not recommended outside of very extreme cases.
                            The amount of values in strs and thrs need to be equal.
    :param thrs:            A list of thresholds, written as [(EdgeValRef, NextFrameDiff, PrevFrameDiff)].
                            You can pass any arbitrary number of values here.
                            The amount of values in strs and thrs need to be equal.
    :param matrix:          Enum for the matrix of the input clip. See ``types.Matrix`` for more info.
                            If `None`, gets matrix from the "_Matrix" prop of the clip unless it's an RGB clip,
                            in which case it stays as `None`.
    :param cuda:            Use CUDA backend if True, else CPU backend
    :param write_props:     Will write verbose props
    :param vsdpir_args:     Additional args to pass to ``vsdpir``

    :return:                Deblocked clip
    """
    assert clip.format

    def _eval_db(n: int, f: Sequence[vs.VideoFrame],
                 clip: vs.VideoNode, db_clips: Sequence[vs.VideoNode],
                 nthrs: Sequence[Tuple[float, float, float]]) -> vs.VideoNode:

        evref_diff, y_next_diff, y_prev_diff = [
            get_prop(f[i], prop, float)
            for i, prop in zip(range(3), ['EdgeValRefDiff', 'YNextDiff', 'YPrevDiff'])
        ]
        f_type = get_prop(f[0], '_PictType', bytes).decode('utf-8')

        if f_type == 'I':
            y_next_diff = (y_next_diff + evref_diff) / 2

        out = clip
        nthr_used = (-1., ) * 3
        for dblk, nthr in zip(db_clips, nthrs):
            if all(p > t for p, t in zip([evref_diff, y_next_diff, y_prev_diff], nthr)):
                out = dblk
                nthr_used = nthr

        if write_props:
            for prop_name, prop_val in zip(
                ['Adb_EdgeValRefDiff', 'Adb_YNextDiff', 'Adb_YPrevDiff',
                 'Adb_EdgeValRefDiffThreshold', 'Adb_YNextDiffThreshold', 'Adb_YPrevDiffThreshold'],
                [evref_diff, y_next_diff, y_prev_diff] + list(nthr_used)
            ):
                out = out.std.SetFrameProp(prop_name, floatval=max(prop_val * 255, -1))

        return out

    if len(strs) != len(thrs):
        raise ValueError('autodb_dpir: You must pass an equal amount of values to '
                         f'strenght {len(strs)} and thrs {len(thrs)}!')

    nthrs = [tuple(x / 255 for x in thr) for thr in thrs]

    is_rgb = clip.format.color_family is vs.RGB

    if not matrix and not is_rgb:
        matrix = get_prop(clip.get_frame(0), "_Matrix", int)

    rgb = core.resize.Bicubic(clip, format=vs.RGBS, matrix_in=matrix) if not is_rgb else clip

    assert rgb.format

    maxvalue = (1 << rgb.format.bits_per_sample) - 1
    evref = core.std.Prewitt(rgb)
    evref = core.std.Expr(evref, f"x {edgevalue} >= {maxvalue} x ?")
    evref_rm = evref.std.Median().std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])

    diffevref = core.std.PlaneStats(evref, evref_rm, prop='EdgeValRef')
    diffnext = core.std.PlaneStats(rgb, rgb.std.DeleteFrames([0]), prop='YNext')
    diffprev = core.std.PlaneStats(rgb, rgb[0] + rgb, prop='YPrev')

    db_clips = [
        vsdpir(rgb, strength=st, mode='deblock', cuda=cuda, **vsdpir_args)
        .std.SetFrameProp('Adb_DeblockStrength', intval=int(st)) for st in strs
    ]

    debl = core.std.FrameEval(
        rgb, partial(_eval_db, clip=rgb, db_clips=db_clips, nthrs=nthrs),
        prop_src=[diffevref, diffnext, diffprev]
    )

    return core.resize.Bicubic(debl, format=clip.format.id, matrix=matrix if not is_rgb else None)


@disallow_variable_format
@disallow_variable_resolution
def vsdpir(clip: vs.VideoNode, strength: SupportsFloat | vs.VideoNode | None = 25, mode: str = 'deblock',
           matrix: Matrix | int | None = None, tiles: int | Tuple[int] | None = None,
           cuda: bool = True, i444: bool = False, kernel: Kernel = Catrom(), **dpir_args: Any) -> vs.VideoNode:
    """
    A simple vs-mlrt DPIR wrapper for convenience.

    You must install vs-mlrt. For more information, see the following links:

    * https://github.com/AmusementClub/vs-mlrt
    * https://github.com/AmusementClub/vs-mlrt/wiki/DPIR
    * https://github.com/AmusementClub/vs-mlrt/releases/latest

    Converts to RGB -> runs DPIR -> converts back to original format, and with no subsampling if ``i444=True``.
    For more information, see https://github.com/cszn/DPIR.

    Dependencies:

    * vs-mlrt

    :param clip:            Input clip
    :param strength:        DPIR strength. Sane values lie between 1–20 for ``mode='deblock'``,
                            and 1–3 for ``mode='denoise'``
    :param mode:            DPIR mode. Valid modes are 'deblock' and 'denoise'.
    :param matrix:          Enum for the matrix of the input clip. See ``types.Matrix`` for more info.
                            If not specified, gets matrix from the "_Matrix" prop of the clip unless it's an RGB clip,
                            in which case it stays as `None`.
    :param cuda:            Use CUDA backend if True, else CPU backend
    :param i444:            Forces the returned clip to be YUV444PS instead of the input clip's format
    :param dpir_args:       Additional args to pass to vs-mlrt.
                            Note: strength, tiles, and model cannot be overridden!

    :return:                Deblocked or denoised clip in either the given clip's format or YUV444PS
    """
    try:
        from vsmlrt import DPIR, Backend, DPIRModel
    except ModuleNotFoundError:
        raise ModuleNotFoundError("deblock: 'vsmlrt is required to use deblocking function.'")

    assert clip.format

    bit_depth = get_depth(clip)
    is_rgb, is_gray = (clip.format.color_family is f for f in (vs.RGB, vs.GRAY))

    clip_32 = depth(clip, 32, dither_type=Dither.ERROR_DIFFUSION).std.Limiter()

    # TODO: Replace with a match-case?
    if mode.lower() == 'deblock':
        model = DPIRModel.drunet_deblocking_color if not is_gray else DPIRModel.drunet_deblocking_grayscale
    elif mode.lower() == 'denoise':
        model = DPIRModel.drunet_color if not is_gray else DPIRModel.drunet_gray
    else:
        raise ValueError(f"""vsdpir: '"{mode}" is not a valid mode!'""")

    dpir_args |= dict(strength=strength, tiles=tiles, model=model)

    if "backend" not in dpir_args:
        dpir_args |= dict(backend=Backend.ORT_CUDA if cuda else Backend.OV_CPU)

    if is_rgb or is_gray:
        return depth(DPIR(clip_32, **dpir_args), bit_depth)

    if matrix is None:
        matrix = get_prop(clip.get_frame(0), "_Matrix", int)

    targ_matrix = Matrix(matrix)
    targ_format = clip.format.replace(subsampling_w=0, subsampling_h=0) if i444 else clip.format

    clip_rgb = kernel.resample(clip_32, vs.RGBS, matrix_in=targ_matrix)  # type:ignore[arg-type]

    run_dpir = DPIR(clip_rgb, **dpir_args)

    return kernel.resample(run_dpir, targ_format, targ_matrix)  # type:ignore[arg-type]
