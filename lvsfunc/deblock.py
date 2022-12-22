from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Any, Callable, Literal, Sequence, SupportsFloat, cast

from vskernels import Catrom, Kernel, KernelT, Point
from vstools import (
    DependencyNotFoundError, DitherType, FrameRangeN, FrameRangesN, Matrix, check_variable, core, depth, get_depth,
    get_nvidia_version, get_prop, replace_ranges, vs
)

__all__ = [
    'autodb_dpir', 'dpir'
]


def autodb_dpir(clip: vs.VideoNode, edgevalue: int = 24,
                strs: Sequence[float] = [10, 50, 75],
                thrs: Sequence[tuple[float, float, float]] = [(1.5, 2.0, 2.0), (3.0, 4.5, 4.5), (5.5, 7.0, 7.0)],
                matrix: Matrix | int | None = None,
                edgemasker: Callable[[vs.VideoNode], vs.VideoNode] | None = None,
                kernel: KernelT = Catrom,
                cuda: bool | Literal['trt'] | None = None,
                return_mask: bool = False,
                write_props: bool = False,
                **vsdpir_args: Any) -> vs.VideoNode:
    r"""
    Rewrite of fvsfunc.AutoDeblock that uses vspdir instead of dfttest to deblock.

    This function checks for differences between a frame and an edgemask with some processing done on it,
    and for differences between the current frame and the next frame.
    For frames where both thresholds are exceeded, it will perform deblocking at a specified strength.
    This will ideally be frames that show big temporal *and* spatial inconsistencies.

    Thresholds and calculations are added to the frameprops to use as reference when setting the thresholds.

    Keep in mind that dpir is not perfect; it may cause weird, black dots to appear sometimes.
    If that happens, you can perform a denoise on the original clip (maybe even using dpir's denoising mode)
    and grab the brightest pixels from your two clips. That should return a perfectly fine clip.

    Thanks `Vardë <https://github.com/Ichunjo>`_, `louis <https://github.com/tomato39>_`,
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

    :raises ValueError:     Unequal number of ``strength``\s and ``thr``\s passed.
    """
    assert check_variable(clip, "autodb_dpir")

    def _eval_db(n: int, f: Sequence[vs.VideoFrame],
                 clip: vs.VideoNode, db_clips: Sequence[vs.VideoNode],
                 nthrs: Sequence[tuple[float, float, float]]) -> vs.VideoNode:

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
                         f'strength {len(strs)} and thrs {len(thrs)}!')

    if edgemasker is None:
        edgemasker = core.std.Prewitt

    kernel = Kernel.ensure_obj(kernel)

    vsdpir_final_args = dict[str, Any](mode='deblock', cuda=cuda)
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
    evref = core.akarin.Expr(evref, f"x {edgevalue} >= {maxvalue} x ?")
    evref_rm = evref.std.Median().std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])

    if return_mask:
        return kernel.resample(evref_rm, format=clip.format, matrix=targ_matrix if not is_rgb else None)

    diffevref = core.std.PlaneStats(evref, evref_rm, prop='EdgeValRef')
    diffnext = core.std.PlaneStats(rgb, rgb.std.DeleteFrames([0]), prop='YNext')
    diffprev = core.std.PlaneStats(rgb, rgb[0] + rgb, prop='YPrev')

    db_clips = [
        dpir(rgb, strength=st, **vsdpir_final_args)
        .std.SetFrameProp('Adb_DeblockStrength', intval=int(st)) for st in strs
    ]

    debl = core.std.FrameEval(
        rgb, partial(_eval_db, clip=rgb, db_clips=db_clips, nthrs=nthrs),
        prop_src=[diffevref, diffnext, diffprev]
    )

    return kernel.resample(debl, format=clip.format, matrix=targ_matrix if not is_rgb else None)


def dpir(
    clip: vs.VideoNode, strength: SupportsFloat | vs.VideoNode | None = 10, mode: str = 'deblock',
    matrix: Matrix | int | None = None, cuda: bool | Literal['trt'] | None = None, i444: bool = False,
    tiles: int | tuple[int, int] | None = None, overlap: int | tuple[int, int] | None = 8,
    zones: list[tuple[FrameRangeN | FrameRangesN | None, SupportsFloat | vs.VideoNode | None]] | None = None,
    fp16: bool | None = None, num_streams: int = 1, device_id: int = 0, kernel: KernelT = Catrom
) -> vs.VideoNode:
    """
    DPIR, or Plug-and-Play Image Restoration with Deep Denoiser Prior, is a denoise and deblocking neural network.

    You must install vs-mlrt. For more information, see the following links:

    * `vs-mlrt <https://github.com/AmusementClub/vs-mlrt>`_
    * `vs-mlrt DPIR wiki page <https://github.com/AmusementClub/vs-mlrt/wiki/DPIR>`_
    * `vs-mlrt latest release <https://github.com/AmusementClub/vs-mlrt/releases/latest>`_

    Converts to RGB -> runs DPIR -> converts back to original format, and with no subsampling if ``i444=True``.
    For more information, see `the original DPIR repository <https://github.com/cszn/DPIR>`_.

    Thanks `Setsugen no ao <https://github.com/Setsugennoao>`_!

    Dependencies:

    * `vs-mlrt <https://github.com/AmusementClub/vs-mlrt>`_

    :param clip:                    Clip to process.
    :param strength:                DPIR strength.
                                    Sane values lie between 1–10 for ``mode='deblock'``, and 1–3 for ``mode='denoise'``
                                    Other than a float, you can also pass a clip, either GRAY8 (0-255),
                                    or GRAYS (0-+inf).

                                    For example, you can pass a
                                    :py:func:`clip.std.BlankClip(format=vs.GRAYS, color=15.0 / 255)`
                                    for a solid strength across the frame, or you can combine various strengths
                                    with masks.

                                    This means you can pass higher strenghts to areas around edges with heavy ringing,
                                    and lower in textured/detailed parts, for example.
    :param mode:                    DPIR mode. Valid modes are 'deblock' and 'denoise'.
    :param matrix:                  Enum for the matrix of the Clip to process.
                                    See :py:attr:`lvsfunc.types.Matrix` for more info.
                                    If not specified, gets matrix from the "_Matrix" prop of the clip
                                    unless it's an RGB clip, in which case it stays as `None`.
    :param cuda:                    Used to select backend.
                                    Use CUDA if True, CUDA TensorRT if 'trt', else CPU OpenVINO if False.
                                    If ``None``, it will detect your system's capabilities
                                    and select the fastest backend.
    :param i444:                    Forces the returned clip to be YUV444PS instead of the input clip's format.
    :param tiles:                   Can either be an int, specifying the number of tiles the image will be split into
                                    for processing, or a tuple for manually specifying the width/height
                                    of the singular tiles.
    :param overlap:                 Number of pixels in each direction for padding the tiles.
                                    Useful for, when using tiled processing, you're having clear boundaries
                                    between tiles.
                                    To disable, set `None` or `0`. Default: 8px.
    :param zones:                   A mapping to zone the DPIR strength so you don't have to call it multiple times.
                                    The key should be a `float` / ``VideoNode`` (a normalised mask, for example)
                                    or `None` to passthrough the Clip to process.
                                    The values should be a range that will be passed to ``replace_ranges``
    :param fp16:                    Represent the clip with 16f tensors instead of 32f for a speedup, but it's useless—
                                    and may even harm performance—when enabled with a device that doesn't support it.
    :param num_streams:             Number of concurrent CUDA streams to use. Increase if GPU isn't getting saturated.
    :param device_id:               Specifies the GPU device id to use.
    :param kernel:                  py:class:`vskernels.Kernel` object used for conversions between YUV <-> RGB.
                                    This can also be the string name of the kernel
                                    (Default: py:class:`vskernels.Bicubic(0, 0.5)`).

    :return:                        Deblocked or denoised clip in either the given clip's format or YUV444PS.

    :raises DependencyNotFoundError: Dependencies are missing.
    :raises TypeError:              Invalid ``mode`` is given.
    :raises ValueError:             ``strength`` is a VideoNode, but not GRAY8 or GRAYS.
    :raises ValueError:             ``strength`` is a VideoNode, but of a different length than the input clip.
    :raises TypeError:              ``strength`` is not a :py:attr:`typing.SupportsFloat` or VideoNode.
    """
    try:
        from vsmlrt import Backend, DPIRModel, backendT, calc_tilesize, inference, models_path
    except ModuleNotFoundError as e:
        raise DependencyNotFoundError(dpir, e)

    assert check_variable(clip, "dpir")

    kernel = Kernel.ensure_obj(kernel)

    bit_depth = get_depth(clip)
    is_rgb, is_gray = (clip.format.color_family is f for f in (vs.RGB, vs.GRAY))

    clip_32 = depth(clip, 32, dither_type=DitherType.ERROR_DIFFUSION)

    match mode.lower():
        case 'deblock': model = DPIRModel.drunet_deblocking_grayscale if is_gray else DPIRModel.drunet_deblocking_color
        case 'denoise': model = DPIRModel.drunet_color if not is_gray else DPIRModel.drunet_gray
        case _: raise TypeError(f"dpir: '\"{mode}\" is not a valid mode!'")

    def _get_strength_clip(clip: vs.VideoNode, strength: SupportsFloat) -> vs.VideoNode:
        return clip.std.BlankClip(format=vs.GRAYS, color=float(strength) / 255, keep=True)

    if isinstance(strength, vs.VideoNode):
        assert (fmt := strength.format)

        if fmt.color_family != vs.GRAY:
            raise ValueError("dpir: '`strength` must be a GRAY clip!'")

        if fmt.id == vs.GRAY8:
            strength = strength.akarin.Expr('x 255 /', vs.GRAYS)
        elif fmt.id != vs.GRAYS:
            raise ValueError("dpir: '`strength` must be GRAY8 or GRAYS!'")

        if strength.width != clip.width or strength.height != clip.height:
            strength = kernel.scale(strength, clip.width, clip.height)

        if strength.num_frames != clip.num_frames:
            raise ValueError("dpir: '`strength` must be of the same length as \"clip\"'")
    elif isinstance(strength, SupportsFloat):
        strength = float(strength)
    else:
        raise TypeError("dpir: '`strength` must be a float or a GRAYS clip'")

    if not is_rgb:
        if matrix is None:
            matrix = get_prop(clip.get_frame(0), "_Matrix", int)

        targ_matrix = Matrix(matrix)
    else:
        targ_matrix = Matrix.RGB

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

    if isinstance(tiles, tuple):
        tilesize = tiles
        tiles = None
    else:
        tilesize = None

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

    no_dpir_zones = FrameRangesN()

    zoned_strength_clip = strength_clip

    if zones:
        cache_strength_clips = dict[float, vs.VideoNode]()

        dpir_zones = dict[int | tuple[int | None, int | None], vs.VideoNode]()

        for ranges, zstr in zones:
            if not zstr:
                if isinstance(ranges, list):
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

            lranges = ranges if isinstance(ranges, list) else [ranges]

            for rrange in lranges:
                if rrange:
                    dpir_zones[rrange] = rstr_clip

        if len(dpir_zones) <= 2:
            for rrange, sclip in dpir_zones.items():
                zoned_strength_clip = replace_ranges(zoned_strength_clip, sclip, rrange)
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

    if None in {cuda, fp16}:
        try:
            info = cast(dict[str, int], core.trt.DeviceProperties(device_id))

            fp16_available = info['major'] >= 7
            trt_available = True
        except BaseException:
            fp16_available = False
            trt_available = False

    if cuda is None:
        cuda = 'trt' if trt_available else get_nvidia_version() is not None

    if fp16 is None:
        fp16 = fp16_available

    backend: backendT

    if cuda == 'trt':
        channels = 2 << (not is_gray)

        backend = Backend.TRT(
            (tile_w, tile_h), fp16=fp16, num_streams=num_streams, device_id=device_id, verbose=False
        )
        backend._channels = channels
    elif cuda:
        backend = Backend.ORT_CUDA(fp16=fp16, num_streams=num_streams, device_id=device_id, verbosity=False)
    else:
        backend = Backend.OV_CPU(fp16=fp16)

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
