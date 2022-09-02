from __future__ import annotations

import subprocess as sp
from pathlib import Path

import vapoursynth as vs
from vsutil import is_image

from .types import IndexFile, IndexingType, IndexType

core = vs.core

__all__ = [
    '_check_has_nvidia',
    '_check_index_exists'
]


def _check_has_nvidia() -> bool:
    """Check if the user has an Nvidia GPU."""
    try:
        sp.check_output('nvidia-smi')
        return True
    except sp.CalledProcessError:
        return False


def _check_index_exists(path: str | Path) -> IndexFile | IndexType:
    """Check whether a lwi or dgi exists. Returns an IndexExists Enum."""
    path = Path(path)

    for itype in IndexingType:
        if path.suffix == itype.value:
            return IndexFile(itype, path.exists())

    for itype in IndexingType:
        if path.with_suffix(f'{path.suffix}{itype.value}').exists():
            return IndexFile(itype, True)

    if is_image(str(path)):
        return IndexType.IMAGE

    return IndexType.NONE
