from __future__ import annotations

import warnings
from functools import partial
from pathlib import Path
from typing import Any, Sequence

from vsexprtools import ExprOp
from vskernels import Catrom, KernelT
from vsparsedvd import DGIndexNV, SPath  # type: ignore
from vstools import (
    MISSING, CustomIndexError, CustomTypeError, CustomValueError, DependencyNotFoundError, FileType, FrameRangeN,
    FrameRangesN, IndexingType, Matrix, check_perms, check_variable, core, depth, get_depth, normalize_ranges,
    normalize_seq, replace_ranges, scale_8bit, vs
)

from .util import match_clip

__all__ = [
    'limit_dark',
    'overlay_sign',
    'shift_tint',
    'source', 'src'
]


def source(filepath: str | Path = MISSING, /, ref: vs.VideoNode | None = None,  # type: ignore
           force_lsmas: bool = False, film_thr: float = 99.0,
           tail_lines: int = 4, kernel: KernelT = Catrom,
           debug: bool = False, **index_args: Any) -> vs.VideoNode:
    """
    Index and load video clips for use in VapourSynth automatically.

    .. note::
        | For this function to work properly, it's recommended you have DGIndexNV in your PATH!

    This function will try to index the given video file using DGIndexNV.
    If it can't, it will fall back on L-SMASH. L-SMASH can also be forced using ``force_lsmas``.
    It also automatically determines if an image has been passed instead.

    This function will automatically check whether your clip is mostly FILM.
    If FILM is above ``film_thr`` and the order is above 0,
    it will automatically set ``fieldop=1`` and ``_FieldBased=0``.
    This can be disabled by passing ``fieldop=0`` to the function yourself.

    You can pass a ref clip to further adjust the clip.
    This affects the dimensions, framerates, matrix/transfer/primaries,
    and in the case of an image, the length of the clip.

    And finally, this function will also add the given filepath to the props.
    This allows for conditional filtering in the event you have multiple input clips.

    If you'd like additional information concerning the input file,
    please consult py:func:`comparison.source_mediainfo`.

    Alias for this function is ``lvsfunc.src``.

    Dependencies:

    * `dgdecode <https://www.rationalqm.us/dgmpgdec/dgmpgdec.html>`_
    * `dgdecodenv <https://www.rationalqm.us/dgdecnv/binaries/>`_
    * `L-SMASH-Works <https://github.com/AkarinVS/L-SMASH-Works>`_
    * `vs-imwri <https://github.com/vapoursynth/vs-imwri>`_

    Thanks `RivenSkaye <https://github.com/RivenSkaye>`_!

    :param filepath:            File to index and load in.
    :param ref:                 Use another clip as reference for the clip's format,
                                resolution, framerate, and matrix/transfer/primaries (Default: None).
    :param force_lsmas:         Force files to be imported with L-SMASH (Default: False).
    :param film_thr:            FILM percentage the dgi must exceed for ``fieldop=1`` to be set automatically.
                                If set above 100.0, it's silently lowered to 100.0 (Default: 99.0).
    :param tail_lines:          Lines to check on the tail of the dgi file.
                                Increase this value if FILM and ORDER do exist in your dgi file
                                but it's having trouble finding them.
                                Set to 2 for a very minor speed-up, as that's usually enough to find them (Default: 4).
    :param kernel:              py:class:`vskernels.Kernel` object used for converting the `clip` to match `ref`.
                                This can also be the string name of the kernel
                                (Default: py:class:`vskernels.Catrom`).
    :param debug:               Return debug information as frame properties. Default: False.
    :param kwargs:              Optional arguments passed to the indexing filter.

    :return:                    VapourSynth clip representing the input file.

    :raises ValueError:         Something other than a path is passed to ``filepath``.
    :raises CustomValueError:   Something other than a video or image file is passed to ``filepath``.
    """
    if filepath is MISSING:  # type: ignore
        return partial(  # type: ignore
            source, ref=ref, force_lsmas=force_lsmas, film_thr=film_thr,
            tail_lines=tail_lines, kernel=kernel, debug=debug, **index_args
        )

    clip = None
    film_thr = float(min(100, film_thr))

    if str(filepath).startswith('file:///'):
        filepath = str(filepath)[8::]

    filepath = Path(filepath)
    check_perms(filepath, 'r', func=source)

    file = FileType.parse(filepath) if filepath.exists() else None

    def _check_file_type(file_type: FileType) -> bool:
        return (  # type:ignore[return-value]
            file_type is FileType.VIDEO or file_type is FileType.IMAGE
        ) or (
            file_type.is_index  # and _check_file_type(file_type.file_type)  # type: ignore
        )

    if not file or not _check_file_type(FileType(file.file_type)):
        for itype in IndexingType:
            if (newpath := filepath.with_suffix(f'{filepath.suffix}{itype.value}')).exists():
                file = FileType.parse(newpath)

    if not file or not _check_file_type(FileType(file.file_type)):
        raise CustomValueError('File isn\'t a video!', source)

    props = dict[str, Any]()
    debug_props = dict[str, Any]()

    if force_lsmas or file.ext is IndexingType.LWI:
        clip = core.lsmas.LWLibavSource(str(filepath), **index_args)
        debug_props |= dict(idx_used='lsmas')
    elif file.file_type is FileType.IMAGE:
        clip = core.imwri.Read(str(filepath), **index_args)
        debug_props |= dict(idx_used='imwri')
    elif file.ext is IndexingType.DGI or not force_lsmas:
        try:
            indexer = DGIndexNV()

            if filepath.suffix != ".dgi":
                filepath = indexer.index([SPath(filepath)], False, False)[0]

            idx_info = indexer.get_info(filepath, 0).footer

            props |= dict(
                dgi_fieldop=0,
                dgi_order=idx_info.order,
                dgi_film=idx_info.film
            )

            indexer_kwargs = dict[str, Any]()
            if idx_info.film >= film_thr:
                indexer_kwargs |= dict(fieldop=1)
                props |= dict(dgi_fieldop=1, _FieldBased=0)

            clip = indexer.vps_indexer(filepath, **indexer_kwargs)
            debug_props |= dict(idx_used='DGIndexNV')
        except Exception as e:
            warnings.warn(f"source: 'Unable to index using DGIndexNV! Falling back to lsmas...'\n\t{e}", RuntimeWarning)

    if clip is None:
        return source(
            filepath, ref=ref, force_lsmas=True, film_thr=film_thr,
            tail_lines=tail_lines, kernel=kernel, debug=debug, **index_args
        )

    props |= dict(idx_filepath=str(filepath))

    if debug:
        props |= debug_props

    clip = clip.std.SetFrameProps(**props)

    if ref:
        return match_clip(clip, ref, length=file.file_type is FileType.IMAGE, kernel=kernel)

    return clip


def shift_tint(clip: vs.VideoNode, values: int | Sequence[int] = 16) -> vs.VideoNode:
    """
    Forcibly adds pixel values to a clip.

    Can be used to fix green tints in Crunchyroll sources, for example.
    Only use this if you know what you're doing!

    This function accepts a single int8 or a list of int8 values.

    :param clip:            Clip to process.
    :param values:          Value added to every pixel, scales accordingly to your clip's depth (Default: 16).

    :return:                Clip with pixel values added.

    :raises IndexError:     Any value in ``values`` are above 255.
    """
    assert check_variable(clip, "shift_tint")

    val = normalize_seq(values)

    if any(v > 255 or v < -255 for v in val):
        raise CustomIndexError('Every value in "values" must be an 8 bit number!', shift_tint)

    return ExprOp.ADD.combine(clip, suffix=[scale_8bit(clip, v) for v in val])


def limit_dark(
    clip: vs.VideoNode, filtered: vs.VideoNode, thr: float = 0.25, thr_lower: float | None = None
) -> vs.VideoNode:
    """
    Replace frames in a clip with a filtered clip when the frame's luminosity exceeds the threshold.

    This way you can run lighter (or heavier) filtering on scenes that are almost entirely dark.

    There is one caveat, however: You can get scenes where every other frame is filtered
    rather than the entire scene. Please do take care to avoid that if possible.

    :param clip:                Clip to process.
    :param filtered:            Filtered clip.
    :param threshold:           Threshold for frame averages to be filtered (Default: 0.25).
    :param threshold_range:     Threshold for a range of frame averages to be filtered (Default: None).

    :return:                    Conditionally filtered clip.

    :raises ValueError:         ``threshold_range`` is a higher value than ``threshold``.
    """
    if thr_lower is None:
        def _diff(n: int, f: vs.VideoFrame) -> vs.VideoNode:
            return clip if f[0][0, 0] > thr else filtered  # type: ignore
    else:
        def _diff(n: int, f: vs.VideoFrame) -> vs.VideoNode:
            return filtered if thr_lower <= f[0][0, 0] <= thr else clip  # type: ignore

    if thr_lower is not None and thr_lower > thr:
        raise CustomValueError('"thr_lower" must be a lower value than "thr"!', limit_dark, (thr_lower, thr))

    avg = clip.std.BlankClip(1, 1, vs.GRAYS).std.CopyFrameProps(clip.std.PlaneStats())

    return clip.std.FrameEval(_diff, avg.akarin.Expr('x.PlaneStatsAverage'))


def overlay_sign(clip: vs.VideoNode, overlay: vs.VideoNode | str,
                 frame_ranges: FrameRangeN | FrameRangesN | None = None, fade_length: int = 0,
                 matrix: Matrix | int | None = None) -> vs.VideoNode:
    """
    Overlay a logo or sign onto another clip.

    This is a rewrite of fvsfunc.InsertSign.

    This wrapper also allows you to set fades to fade a logo in and out.

    Dependencies:

    * `vs-imwri <https://github.com/vapoursynth/vs-imwri>`_
    * `kagefunc <https://github.com/Irrational-Encoding-Wizardry/kagefunc>`_ (optional: ``fade_length``)

    :param clip:                    Clip to process.
    :param overlay:                 Sign or logo to overlay. Must be the png loaded in
                                    through :py:func:`core.vapoursnth.imwri.Read` or a path string to the image file,
                                    and **MUST** be the same dimensions as the ``clip`` to process.
    :param frame_ranges:            Frame ranges or starting frame to apply the overlay to.
                                    See :py:attr:`vstools.FrameRange` for more info.
                                    If None, overlays the entire clip.
                                    If a FrameRange is passed, the overlaid clip will only show up inside that range.
                                    If only a single integer is given, it will start on that frame and
                                    stay until the end of the clip.
                                    Note that this function only accepts a single FrameRange!
                                    You can't pass a list of them!
    :param fade_length:             Length to fade the clips into each other.
                                    The fade will start and end on the frames given in frame_ranges.
                                    If set to 0, it won't fade and the sign will simply pop in.
    :param matrix:                  Enum for the matrix of the Clip to process.
                                    See :py:attr:`lvsfunc.types.Matrix` for more info.
                                    If not specified, gets matrix from the "_Matrix" prop of the clip
                                    unless it's an RGB clip, in which case it stays as `None`.

    :return:                        Clip with a logo or sign overlaid on top for the given frame ranges,
                                    either with or without a fade.

    :raises DependencyNotFoundError: Dependencies are missing.
    :raises ValueError:             ``overlay`` is not a VideoNode or a path.
    :raises ValueError:             The overlay clip is not of the same dimensions as the input clip.
    :raises InvalidMatrixError:     ``Matrix`` is an invalid value.
    :raises ValueError:             Overlay does not have an alpha channel.
    :raises TypeError:              Overlay clip was not loaded in using :py:func:`vapoursynth.core.imwri.Read`.
    """
    if fade_length > 0:
        try:
            from kagefunc import crossfade
        except ModuleNotFoundError as e:
            raise DependencyNotFoundError(overlay_sign, e, reason="fade_length > 0")

    assert check_variable(clip, overlay_sign)

    is_string = isinstance(overlay, str)
    clip_fam = clip.format.color_family

    if is_string:
        overlay = core.imwri.Read(overlay, alpha=True)  # type: ignore

    if not isinstance(overlay, vs.VideoNode):
        raise CustomValueError('`overlay` must be a VideoNode object or a string path!', overlay_sign)

    assert check_variable(overlay, overlay_sign)

    if (clip.width, clip.height) != (overlay.width, overlay.height):
        raise CustomValueError('Your overlay clip must have the same dimensions as your input clip!', overlay_sign)

    if isinstance(frame_ranges, list) and len(frame_ranges) > 1:
        warnings.warn("overlay_sign: 'Only one range is currently supported! Grabbing the first item in list.'")
        frame_ranges = frame_ranges[0]

    if overlay.format.color_family is not clip_fam:
        if clip_fam is vs.RGB:
            overlay = Catrom.resample(overlay, clip.format.id, matrix_in=matrix)
        else:
            overlay = Catrom.resample(overlay, clip.format.id, matrix)

    overlay = overlay[0] * clip.num_frames

    try:
        mask = overlay.std.PropToClip('_Alpha')
    except vs.Error:
        if is_string:
            raise CustomValueError('Please make sure your image has an alpha channel!', overlay_sign)

        raise CustomTypeError('Please make sure you loaded your sign in using imwri.Read!', overlay_sign)

    merge = clip.std.MaskedMerge(overlay, depth(mask, get_depth(overlay)).std.Limiter())

    if not frame_ranges:
        return merge

    if fade_length > 0:
        if isinstance(frame_ranges, int):
            return crossfade(clip[:frame_ranges + fade_length], merge[frame_ranges:], fade_length)

        start, end = normalize_ranges(clip, frame_ranges)[0]

        merge = crossfade(clip[:start + fade_length], merge[start:], fade_length)

        return crossfade(merge[:end], clip[end - fade_length:], fade_length)

    return replace_ranges(clip, merge, frame_ranges)


# Aliases
src = source
