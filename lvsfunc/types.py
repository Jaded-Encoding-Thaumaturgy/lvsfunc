from __future__ import annotations

from enum import IntEnum, auto
from typing import Any, NamedTuple, Protocol, Tuple

import vapoursynth as vs

__all__ = [
    'Coordinate', 'Direction', 'Position', 'Range', 'RegressClips', 'SceneChangeMode', 'Size', '_VideoNode'
]

Range = int | None | Tuple[int | None, int | None]


class Coordinate():
    """
    Positive set of (x, y) coordinates.

    :raises ValueError:     Negative values get passed.
    """

    x: int
    y: int

    def __init__(self, x: int, y: int):
        if x < 0 or y < 0:
            raise ValueError(f"{self.__class__.__name__}: 'Can't be negative!'")
        self.x = x
        self.y = y


class Direction(IntEnum):
    """Enum to simplify direction argument."""

    HORIZONTAL = 0
    VERTICAL = 1


class SceneChangeMode(IntEnum):
    """Size type for :py:func:`lvsfunc.render.find_scene_changes`."""

    WWXD = 0
    SCXVID = 1
    WWXD_SCXVID_UNION = 2
    WWXD_SCXVID_INTERSECTION = 3


class Position(Coordinate):
    """Position type for :py:class:`lvsfunc.mask.BoundingBox`."""


class Size(Coordinate):
    """Size type for :py:class:`lvsfunc.mask.BoundingBox`."""


class VSIdxFunction(Protocol):
    """VapourSynth Indexing/Source function."""

    def __call__(self, path: str, *args: Any, **kwargs: Any) -> vs.VideoNode:
        """Call the VapourSynth function."""
        ...


class Shapes(IntEnum):
    """Convolution coordinates for :py:func:`lvsfunc.mask.mt_xxpand_multi`."""

    RECTANGLE = 0
    ELLIPSE = 1
    LOSANGE = 2


class RegressClips(NamedTuple):
    """Regress clip types for :py:func:`lvsfunc.recon.regress`."""

    slope: vs.VideoNode
    intercept: vs.VideoNode
    correlation: vs.VideoNode


class IndexExists(IntEnum):
    """Check if certain files exist for :py:func:`lvsfunc.misc.source`."""

    PATH_IS_DGI = auto()
    PATH_IS_IMG = auto()
    LWI_EXISTS = auto()
    DGI_EXISTS = auto()
    NONE = auto()


class _VideoNode(vs.VideoNode):
    """Use for asserting a VideoFormat exists."""

    format: vs.VideoFormat
