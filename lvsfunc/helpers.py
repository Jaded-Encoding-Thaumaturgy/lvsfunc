from __future__ import annotations

import os
import subprocess as sp
from collections import deque
from pathlib import Path
from typing import Any, Tuple, cast

import vapoursynth as vs
from vsexprtools import PlanesT, normalise_planes
from vsutil import Dither
from vsutil import Range as CRange
from vsutil import depth, get_depth, get_neutral_value, get_peak_value, is_image, join, scale_value, split

from .types import IndexExists, VSIdxFunction

core = vs.core

__all__ = [
    '_check_has_nvidia',
    '_check_index_exists',
    '_generate_dgi',
    '_get_dgidx',
    '_load_dgi',
    '_tail'
]


def _check_has_nvidia() -> bool:
    """Check if the user has an Nvidia GPU."""
    try:
        sp.check_output('nvidia-smi')
        return True
    except sp.CalledProcessError:
        return False


def _get_dgidx() -> Tuple[str, VSIdxFunction]:
    """Return the dgindex idx as a string and the actual source filter."""
    has_nv = _check_has_nvidia()

    dgidx = 'DGIndexNV' if has_nv else 'DGIndex'
    dgsrc = core.dgdecodenv.DGSource if has_nv else core.dgdecode.DGSource  # type:ignore[attr-defined]

    return dgidx, dgsrc


def _check_index_exists(path: os.PathLike[str] | str) -> IndexExists:
    """Check whether a lwi or dgi exists. Returns an IndexExists Enum."""
    path = str(path)

    if path.endswith('.dgi'):
        return IndexExists.PATH_IS_DGI
    elif is_image(path):
        return IndexExists.PATH_IS_IMG
    elif Path(f"{path}.dgi").exists():
        return IndexExists.DGI_EXISTS
    elif Path(f"{path}.lwi").exists():
        return IndexExists.LWI_EXISTS
    return IndexExists.NONE


def _generate_dgi(path: str, idx: str) -> bool:
    """Generate a dgi file using the given indexer and verify it exists."""
    filename, _ = os.path.splitext(path)
    output = f'{filename}.dgi'

    if not os.path.exists(output):
        try:
            sp.run([idx, '-i', path, '-o', output, '-h'])
        except sp.CalledProcessError:
            return False

    return os.path.exists(output)


def _tail(filename: str, n: int = 10) -> Tuple[int, float]:
    """Return the last n lines of a file."""
    with open(filename, "r") as f:
        lines = deque(f, n)
        lines = cast(deque[str], [line for line in lines if 'FILM' in line or 'ORDER' in line])

        if len(lines) == 1:
            return (int(lines[0].split(' ')[1]), 0.00)

        return (int(lines.pop().split(" ")[1].replace("\n", "")),
                float(lines.pop().split(" ")[0].replace("%", "")))


def _load_dgi(path: str, film_thr: float, src_filter: VSIdxFunction,
              order: int, film: float, **index_args: Any) -> vs.VideoNode:
    """
    Run the source filter on the given dgi.

    If order > 0 and FILM % > 99%, it will automatically enable `fieldop=1`.
    """
    props = dict(dgi_order=order, dgi_film=film, dgi_fieldop=0, lvf_idx='DGIndex(NV)')

    if 'fieldop' not in index_args and (order > 0 and film >= film_thr):
        index_args['fieldop'] = 1
        props |= dict(dgi_fieldop=1, _FieldBased=0)

    return src_filter(path, **index_args).std.SetFrameProps(**props)


def _prefilter_to_full_range(pref: vs.VideoNode, range_conversion: float, planes: PlanesT = None) -> vs.VideoNode:
    """From vsdenoise, will be removed once it has been made public."""
    planes = normalise_planes(pref, planes)
    work_clip, *chroma = split(pref) if planes == [0] else (pref, )
    assert (fmt := work_clip.format) and pref.format

    bits = get_depth(pref)
    is_gray = fmt.color_family == vs.GRAY
    is_integer = fmt.sample_type == vs.INTEGER

    # Luma expansion TV->PC (up to 16% more values for motion estimation)
    if range_conversion >= 1.0:
        neutral = get_neutral_value(work_clip, True)
        max_val = get_peak_value(work_clip)
        min_tv_val = scale_value(16, 8, bits)
        max_tv_val = scale_value(219, 8, bits)

        c = 0.0625

        k = (range_conversion - 1) * c
        t = f'x {min_tv_val} - {max_tv_val} / 0 max 1 min' if is_integer else 'x 0 max 1 min'

        pref_full = work_clip.std.Expr([
            f"{k} {1 + c} {(1 + c) * c} {t} {c} + / - * {t} 1 {k} - * + {f'{max_val} *' if is_integer else ''}",
            f'x {neutral} - 128 * 112 / {neutral} +'
        ][:1 + (not is_gray and is_integer)])
    elif range_conversion > 0.0:
        pref_full = work_clip.retinex.MSRCP(None, range_conversion, None, False, True)
    else:
        pref_full = depth(work_clip, bits, range=CRange.FULL, range_in=CRange.LIMITED, dither_type=Dither.NONE)

    if chroma:
        return join([pref_full, *chroma], pref.format.color_family)

    return pref_full
