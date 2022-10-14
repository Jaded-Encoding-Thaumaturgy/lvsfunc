from __future__ import annotations

import subprocess as sp

__all__ = [
    '_check_has_nvidia'
]


def _check_has_nvidia() -> bool:
    """Check if the user has an Nvidia GPU."""
    try:
        sp.check_output('nvidia-smi')
        return True
    except sp.CalledProcessError:
        return False
