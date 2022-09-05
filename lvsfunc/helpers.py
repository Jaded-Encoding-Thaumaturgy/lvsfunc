from __future__ import annotations

import subprocess as sp
from pathlib import Path

import vapoursynth as vs
from vskernels import VideoPropError, get_prop
from vsutil import is_image

from .exceptions import FramePropError
from .types import Dar, IndexFile, IndexingType, IndexType

core = vs.core

__all__ = [
    '_check_has_nvidia',
    '_check_index_exists',
    '_calculate_dar_from_props',
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


def _calculate_dar_from_props(clip: vs.VideoNode) -> Dar:
    """Determine what DAR the clip is by checking default SAR props."""
    frame = clip.get_frame(0)

    try:
        sar = get_prop(frame, "_SARDen", int), get_prop(frame, "_SARNum", int)
    except VideoPropError as e:
        raise FramePropError(
            "PARser", "", f"SAR props not found! Make sure your video indexing plugin sets them!\n\t{e}"
        )

    match sar:
        case (11, 10) | (9, 8): return Dar.FULLSCREEN
        case (33, 40) | (27, 32): return Dar.WIDESCREEN
        case _: raise ValueError("Could not calculate DAR. Please set the DAR manually.")
