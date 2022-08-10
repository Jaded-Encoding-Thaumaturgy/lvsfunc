from __future__ import annotations

import os
import subprocess as sp
from collections import deque
from pathlib import Path
from typing import Any, cast

import vapoursynth as vs
from vsutil import is_image

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


def _get_dgidx() -> tuple[str, VSIdxFunction]:
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


def _tail(filename: str, n: int = 10) -> tuple[int, float]:
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
