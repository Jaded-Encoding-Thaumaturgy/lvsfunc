from __future__ import annotations

import subprocess as sp

from vstools import FramePropError, get_prop, vs

from .types import Dar

__all__ = [
    '_check_has_nvidia',
    '_calculate_dar_from_props',
]


def _check_has_nvidia() -> bool:
    """Check if the user has an Nvidia GPU."""
    try:
        sp.check_output('nvidia-smi')
        return True
    except sp.CalledProcessError:
        return False


def _calculate_dar_from_props(clip: vs.VideoNode) -> Dar:
    """Determine what DAR the clip is by checking default SAR props."""
    frame = clip.get_frame(0)

    try:
        sar = get_prop(frame, "_SARDen", int), get_prop(frame, "_SARNum", int)
    except FramePropError as e:
        raise FramePropError(
            "PARser", "", f"SAR props not found! Make sure your video indexing plugin sets them!\n\t{e}"
        )

    match sar:
        case (11, 10) | (9, 8): return Dar.FULLSCREEN
        case (33, 40) | (27, 32): return Dar.WIDESCREEN
        case _: raise ValueError("Could not calculate DAR. Please set the DAR manually.")
