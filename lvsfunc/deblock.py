from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Sequence, SupportsFloat, Tuple, cast

import vapoursynth as vs
from vskernels import Bicubic, Catrom, Kernel, Point, get_kernel
from vsutil import Dither, depth, get_depth

from .misc import _check_has_nvidia
from .types import VSDPIR_STRENGTH_TYPE, Matrix, Range
from .util import check_variable, get_prop, replace_ranges

core = vs.core

__all__: List[str] = [
    'autodb_dpir', 'vsdpir'
]

if TYPE_CHECKING:
    from vsmlrt import backendT
else:
    backendT = Any


def autodb_dpir(clip: vs.VideoNode, edgevalue: int = 24,
                strs: Sequence[float] = [30, 50, 75],
                thrs: Sequence[Tuple[float, float, float]] = [(1.5, 2.0, 2.0), (3.0, 4.5, 4.5), (5.5, 7.0, 7.0)],
                matrix: Matrix | int | None = None,
                kernel: Kernel | str = Bicubic(b=0, c=0.5),
                cuda: bool = True, write_props: bool = False,
                **vsdpir_args: Any) -> vs.VideoNode:
    """
    Rewrite of fvsfunc.AutoDeblock that uses vspdir instead of dfttest to deblock.

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
                            Sane deblocking strengths lie between 1–20 for most regular deblocking.
                            Going higher than 50 is not recommended outside of very extreme cases.
                            The amount of values in strs and thrs need to be equal.
    :param thrs:            A list of thresholds, written as [(EdgeValRef, NextFrameDiff, PrevFrameDiff)].
                            You can pass any arbitrary number of values here.
                            The amount of values in strs and thrs need to be equal.
    :param matrix:          Enum for the matrix of the input clip. See ``types.Matrix`` for more info.
                            If `None`, gets matrix from the "_Matrix" prop of the clip unless it's an RGB clip,
                            in which case it stays as `None`.
    :param kernel:          `Kernel` object used for conversions between YUV <-> RGB.
    :param cuda:            Use CUDA backend if True, else CPU backend.
    :param write_props:     whether to write verbose props.
    :param vsdpir_args:     Additional args to pass to ``vsdpir``.

    :return:                Deblocked clip with different strengths applied based on the given parameters.
    """
    check_variable(clip, "autodb_dpir")
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

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    nthrs = [tuple(x / 255 for x in thr) for thr in thrs]

    is_rgb = clip.format.color_family is vs.RGB

    if not is_rgb:
        if matrix is None:
            matrix = get_prop(clip.get_frame(0), "_Matrix", int)

        targ_matrix = vs.MatrixCoefficients(matrix)

        rgb = kernel.resample(clip, format=vs.RGBS, matrix_in=targ_matrix)
    else:
        rgb = clip

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

    return kernel.resample(debl, format=clip.format, matrix=targ_matrix if not is_rgb else None)


def vsdpir(
    clip: vs.VideoNode, strength: VSDPIR_STRENGTH_TYPE = 25, mode: str = 'deblock',
    matrix: Matrix | int | None = None, tiles: int | Tuple[int, int] | None = None,
    cuda: bool | Literal['trt'] | None = None, i444: bool = False, kernel: Kernel | str = Catrom(),
    zones: List[Tuple[Range | List[Range] | None, VSDPIR_STRENGTH_TYPE]] | None = None,
    tilesize: int | Tuple[int, int] | None = None, overlap: int | Tuple[int, int] | None = None,
    fp16: bool | None = None, num_streams: int = 2, backend: backendT | None = None, device_id: int = 0
) -> vs.VideoNode:
    """
    DPIR, or Plug-and-Play Image Restoration with Deep Denoiser Prior, is a denoise and deblocking neural network.

    You must install vs-mlrt. For more information, see the following links:

    * `vs-mlrt <https://github.com/AmusementClub/vs-mlrt>`_
    * `vs-mlrt DPIR wiki page <https://github.com/AmusementClub/vs-mlrt/wiki/DPIR>`_
    * `vs-mlrt latest release <https://github.com/AmusementClub/vs-mlrt/releases/latest>`_

    Converts to RGB -> runs DPIR -> converts back to original format, and with no subsampling if ``i444=True``.
    For more information, see `the original DPIR repository <https://github.com/cszn/DPIR>`_.

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
    :param zones:           A mapping to zone the DPIR strength so you don't have to call it multiple times.
                            The key should be a `float` / ``VideoNode`` (a normalised mask, for example)
                            or `None` to pass the input clip.
                            The values should be a range that will be passed to ``replace_ranges``
    :param dpir_args:       Additional args to pass to vs-mlrt.
                            Note: strength, tiles, and model cannot be overridden!

    :return:                Deblocked or denoised clip in either the given clip's format or YUV444PS
    """
    try:
        from vsmlrt import (Backend, DPIRModel, calc_tilesize, inference,
                            models_path)
    except ModuleNotFoundError:
        raise ModuleNotFoundError("vsdpir: 'missing dependency `vsmlrt`!'")

    check_variable(clip, "vsdpir")
    assert clip.format

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    bit_depth = get_depth(clip)
    is_rgb, is_gray = (clip.format.color_family is f for f in (vs.RGB, vs.GRAY))

    clip_32 = depth(clip, 32, dither_type=Dither.ERROR_DIFFUSION)

    match mode.lower():
        case 'deblock': model = DPIRModel.drunet_deblocking_grayscale if is_gray else DPIRModel.drunet_deblocking_color
        case 'denoise': model = DPIRModel.drunet_color if not is_gray else DPIRModel.drunet_gray
        case _: raise TypeError(f"vsdpir: '\"{mode}\" is not a valid mode!'")

    def _get_strength_clip(clip: vs.VideoNode, strength: SupportsFloat) -> vs.VideoNode:
        return clip.std.BlankClip(format=vs.GRAYS, color=float(strength) / 255, keep=True)

    if isinstance(strength, vs.VideoNode):
        assert (fmt := strength.format)

        if fmt.color_family != vs.GRAY:
            raise ValueError("vsdpir: '`strength` must be a GRAY clip!'")

        if fmt.id == vs.GRAY8:
            strength = strength.std.Expr('x 255 /', vs.GRAYS)
        elif fmt.id != vs.GRAYS:
            raise ValueError("vsdpir: '`strength` must be GRAY8 or GRAYS!'")

        if strength.width != clip.width or strength.height != clip.height:
            strength = kernel.scale(strength, clip.width, clip.height)

        if strength.num_frames != clip.num_frames:
            raise ValueError("vsdpir: '`strength` must be of the same length as \"clip\"'")
    elif isinstance(strength, SupportsFloat):
        strength = float(strength)
    else:
        raise TypeError("vsdpir: '`strength` must be a float or a GRAYS clip'")

    if not is_rgb:
        if matrix is None:
            matrix = get_prop(clip.get_frame(0), "_Matrix", int)

        targ_matrix = vs.MatrixCoefficients(matrix)
    else:
        targ_matrix = vs.MatrixCoefficients(0)

    targ_format = clip.format.replace(subsampling_w=0, subsampling_h=0) if i444 else clip.format

    if is_rgb or is_gray:
        clip_rgb = clip_32.std.Limiter()
    else:
        clip_rgb = kernel.resample(clip_32, vs.RGBS, matrix_in=targ_matrix).std.Limiter()

    if overlap is None:
        overlap_w = overlap_h = 0
    elif isinstance(overlap, int):
        overlap_w = overlap_h = overlap
    else:
        overlap_w, overlap_h = overlap

    multiple = 8

    mod_w, mod_h = clip_rgb.width % multiple, clip_rgb.height % multiple

    if to_pad := any({mod_w, mod_h}):
        d_width, d_height = clip_rgb.width + mod_w, clip_rgb.height + mod_h

        clip_rgb = Point(src_width=d_width, src_height=d_height).scale(
            clip_rgb, d_width, d_height, (-mod_h, -mod_w)
        )

        if isinstance(strength, vs.VideoNode):
            strength = Point(src_width=d_width, src_height=d_height).scale(
                strength, d_width, d_height, (-mod_h, -mod_w)
            )

    (tile_w, tile_h), (overlap_w, overlap_h) = calc_tilesize(
        multiple=multiple,
        tiles=tiles, tilesize=tilesize,
        width=clip_rgb.width, height=clip_rgb.height,
        overlap_w=overlap_w, overlap_h=overlap_h
    )

    if isinstance(strength, vs.VideoNode):
        strength_clip = strength
    else:
        strength_clip = _get_strength_clip(clip_rgb, strength)

    no_dpir_zones = list[Range]()

    if zones:
        cache_strength_clips = dict[float, vs.VideoNode]()

        dpir_zones = dict[int | Tuple[int | None, int | None], vs.VideoNode]()

        for ranges, zstr in zones:
            if not zstr:
                if isinstance(ranges, List):
                    no_dpir_zones.extend(ranges)
                else:
                    no_dpir_zones.append(ranges)

                continue

            if isinstance(zstr, vs.VideoNode):
                rstr_clip = zstr
            else:
                zstr = float(zstr)

                if zstr not in cache_strength_clips:
                    cache_strength_clips[zstr] = _get_strength_clip(clip_rgb, zstr)

                rstr_clip = cache_strength_clips[zstr]

            lranges = ranges if isinstance(ranges, List) else [ranges]

            for rrange in lranges:
                if rrange:
                    dpir_zones[rrange] = rstr_clip

        if len(dpir_zones) <= 2:
            for rrange, sclip in dpir_zones.items():
                zoned_strength_clip = replace_ranges(strength_clip, sclip, rrange)
        else:
            dpir_ranges_zones = {
                range(*(
                    (r, r + 1) if isinstance(r, int) else (r[0] or 0, r[1] + 1 if r[1] else clip.num_frames)
                )): sclip for r, sclip in dpir_zones.items()
            }

            dpir_ranges_zones = {k: dpir_ranges_zones[k] for k in sorted(dpir_ranges_zones, key=lambda x: x.start)}
            dpir_ranges_keys = list(dpir_ranges_zones.keys())

            def _select_sclip(n: int) -> vs.VideoNode:
                nonlocal dpir_ranges_zones, dpir_ranges_keys

                for i, ranges in enumerate(dpir_ranges_keys):
                    if n in ranges:
                        if i > 0:
                            dpir_ranges_keys = dpir_ranges_keys[i:] + dpir_ranges_keys[:i]
                        return dpir_ranges_zones[ranges]

                return strength_clip

            zoned_strength_clip = strength_clip.std.FrameEval(_select_sclip)
    else:
        zoned_strength_clip = strength_clip

    if backend is None:
        if None in {cuda, fp16}:
            try:
                info = cast(Dict[str, int], core.trt.DeviceProperties(device_id))

                fp16_available = info['major'] >= 7
                trt_available = True
            except BaseException:
                fp16_available = False
                trt_available = False

        if cuda is None:
            cuda = 'trt' if trt_available else _check_has_nvidia()

        if fp16 is None:
            fp16 = fp16_available

        if cuda == 'trt':
            channels = 2 << (not is_gray)

            backend = Backend.TRT(
                (tile_w, tile_h), fp16=fp16, num_streams=num_streams, device_id=device_id, verbose=False
            )
        elif cuda:
            backend = Backend.ORT_CUDA(fp16=fp16, num_streams=num_streams, device_id=device_id, verbosity=False)
        else:
            backend = Backend.OV_CPU(fp16=fp16)

    if backend.__class__ is Backend.TRT:
        backend._channels = channels  # type: ignore

    network_path = Path(models_path) / 'dpir' / f'{tuple(DPIRModel.__members__)[model]}.onnx'

    run_dpir = inference(
        [clip_rgb, zoned_strength_clip], str(network_path), (overlap_w, overlap_h), (tile_w, tile_h), backend
    )

    if no_dpir_zones:
        run_dpir = replace_ranges(run_dpir, clip_rgb, no_dpir_zones)

    if to_pad:
        run_dpir = run_dpir.std.Crop(0, mod_w, mod_h, 0)

    if is_rgb or is_gray:
        return depth(run_dpir, bit_depth)

    return kernel.resample(run_dpir, targ_format, targ_matrix)
