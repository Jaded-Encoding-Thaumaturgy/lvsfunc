from __future__ import annotations

from typing import Any, NamedTuple, Protocol

from vstools import CustomIntEnum, vs

__all__ = [
    'Coordinate',
    'SceneChangeMode',
    'Position',
    'Size',
    'VSIdxFunction',
    'Shapes',
    'RegressClips'
]


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


class SceneChangeMode(CustomIntEnum):
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


class Shapes(CustomIntEnum):
    """Convolution coordinates for :py:func:`lvsfunc.mask.mt_xxpand_multi`."""

    RECTANGLE = 0
    ELLIPSE = 1
    LOSANGE = 2


class RegressClips(NamedTuple):
    """Regress clip types for :py:func:`lvsfunc.recon.regress`."""

    slope: vs.VideoNode
    intercept: vs.VideoNode
    correlation: vs.VideoNode
