from __future__ import annotations

from functools import partial
from typing import Any, Callable, Literal, Sequence
from warnings import warn

from vsdenoise import dpir
from vsexprtools import expr_func
from vskernels import Catrom, Kernel, KernelT
from vstools import (CustomValueError, Matrix, check_variable, core, get_prop,
                     vs)

__all__ = [
    'autodb_dpir'
]


def autodb_dpir(
    clip: vs.VideoNode,
    edgevalue: int = 24,
    strs: Sequence[float] = [10, 50, 75],
    thrs: Sequence[tuple[float, float, float]] = [(1.5, 2.0, 2.0), (3.0, 4.5, 4.5), (5.5, 7.0, 7.0)],
    matrix: Matrix | int | None = None,
    edgemasker: Callable[[vs.VideoNode], vs.VideoNode] | None = None,
    kernel: KernelT = Catrom,
    cuda: bool | Literal['trt'] | None = None,
    return_mask: bool = False,
    write_props: bool = False,
    **vsdpir_args: Any
) -> vs.VideoNode:
    """
    Rewrite of fvsfunc.AutoDeblock that uses vspdir instead of dfttest to deblock.

    This function checks for differences between a frame and an edgemask with some processing done on it,
    and for differences between the current frame and the next frame.
    For frames where both thresholds are exceeded, it will perform deblocking at a specified strength.
    This will ideally be frames that show big temporal *and* spatial inconsistencies.

    Thresholds and calculations are added to the frameprops to use as reference when setting the thresholds.

    Keep in mind that dpir is not perfect; it may cause weird, black dots to appear sometimes.
    If that happens, you can perform a denoise on the original clip (maybe even using dpir's denoising mode)
    and grab the brightest pixels from your two clips. That should return a perfectly fine clip.

    Thanks `Vardë <https://github.com/Ichunjo>`_, `louis <https://github.com/tomato39>`_,
    `Setsugen no ao <https://github.com/Setsugennoao>`_!

    Dependencies:

    * `vs-mlrt <https://github.com/AmusementClub/vs-mlrt>`_

    :param clip:            Clip to process.
    :param edgevalue:       Remove edges from the edgemask that exceed this threshold (higher means more edges removed).
    :param strs:            A list of DPIR strength values (higher means stronger deblocking).
                            You can pass any arbitrary number of values here.
                            Sane deblocking strengths lie between 1–20 for most regular deblocking.
                            Going higher than 50 is not recommended outside of very extreme cases.
                            The amount of values in strs and thrs need to be equal.
    :param thrs:            A list of thresholds, written as [(EdgeValRef, NextFrameDiff, PrevFrameDiff)].
                            You can pass any arbitrary number of values here.
                            The amount of values in strs and thrs need to be equal.
    :param matrix:          Enum for the matrix of the Clip to process.
                            See :py:attr:`lvsfunc.types.Matrix` for more info.
                            If `None`, gets matrix from the "_Matrix" prop of the clip unless it's an RGB clip,
                            in which case it stays as `None`.
    :param edgemasker:      Edgemasking function to use for calculating the edgevalues.
                            Default: Prewitt.
    :param kernel:          py:class:`vskernels.Kernel` object used for conversions between YUV <-> RGB.
                            This can also be the string name of the kernel
                            (Default: py:class:`vskernels.Bicubic(0, 0.5)`).
    :param cuda:            Used to select backend.
                            Use CUDA if True, CUDA TensorRT if 'trt', else CPU OpenVINO if False.
                            If ``None``, it will detect your system's capabilities
                            and select the fastest backend.
    :param return_mask:     Return the mask used for calculating the edgevalues.
    :param write_props:     whether to write verbose props.
    :param vsdpir_args:     Additional args to pass to :py:func:`lvsfunc.deblock.vsdpir`.

    :return:                Deblocked clip with different strengths applied based on the given parameters.

    :raises ValueError:     Unequal number of ``strength``s and ``thr``s passed.
    """

    assert check_variable(clip, "autodb_dpir")

    def _eval_db(
        n: int, f: Sequence[vs.VideoFrame],
        clip: vs.VideoNode, db_clips: Sequence[vs.VideoNode],
        nthrs: Sequence[tuple[float, float, float]]
    ) -> vs.VideoNode:
        evref_diff, y_next_diff, y_prev_diff = [
            get_prop(f[i], prop, float)
            for i, prop in zip(range(3), ['EdgeValRefDiff', 'YNextDiff', 'YPrevDiff'])
        ]

        f_type = get_prop(f[0], '_PictType', str)

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
        raise CustomValueError(
            f"You must pass an equal amount of values to strength {len(strs)} and thrs {len(thrs)}!",
            autodb_dpir, f"{len(strs)} != {len(thrs)}"
        )

    if edgemasker is None:
        edgemasker = core.std.Prewitt

    kernel = Kernel.ensure_obj(kernel)

    if vsdpir_args.get('fp16', None):
        warn("autodb_dpir: fp16 has been known to cause issues! It's highly recommended to set it to False!")

    vsdpir_final_args = dict[str, Any](cuda=cuda, fp16=vsdpir_args.pop('fp16', False))
    vsdpir_final_args |= vsdpir_args
    vsdpir_final_args.pop('strength', None)

    nthrs = [tuple(x / 255 for x in thr) for thr in thrs]

    is_rgb = clip.format.color_family is vs.RGB

    if not is_rgb:
        if matrix is None:
            matrix = get_prop(clip.get_frame(0), "_Matrix", int)

        targ_matrix = Matrix(matrix)

        rgb = kernel.resample(clip, format=vs.RGBS, matrix_in=targ_matrix)
    else:
        rgb = clip

    maxvalue = (1 << rgb.format.bits_per_sample) - 1  # type:ignore[union-attr]
    evref = edgemasker(rgb)
    evref = expr_func(evref, f"x {edgevalue} >= {maxvalue} x ?")
    evref_rm = evref.std.Median().std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])

    if return_mask:
        return kernel.resample(evref_rm, format=clip.format, matrix=targ_matrix if not is_rgb else None)

    diffevref = core.std.PlaneStats(evref, evref_rm, prop='EdgeValRef')
    diffnext = core.std.PlaneStats(rgb, rgb.std.DeleteFrames([0]), prop='YNext')
    diffprev = core.std.PlaneStats(rgb, rgb[0] + rgb, prop='YPrev')

    db_clips = [
        dpir.DEBLOCK(rgb, strength=st, **vsdpir_final_args)
        .std.SetFrameProp('Adb_DeblockStrength', intval=int(st)) for st in strs
    ]

    debl = core.std.FrameEval(
        rgb, partial(_eval_db, clip=rgb, db_clips=db_clips, nthrs=nthrs),
        prop_src=[diffevref, diffnext, diffprev]
    )

    return kernel.resample(debl, format=clip.format, matrix=targ_matrix if not is_rgb else None)
