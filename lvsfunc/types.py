from __future__ import annotations

from vstools import CustomIntEnum

__all__ = [
    'Coordinate',
    'SceneChangeMode',
    'Position',
    'Size',
    'x265_me_map',
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


class Position(Coordinate):
    """Position type for :py:class:`lvsfunc.mask.BoundingBox`."""


class Size(Coordinate):
    """Size type for :py:class:`lvsfunc.mask.BoundingBox`."""


class SceneChangeMode(CustomIntEnum):
    """Size type for :py:func:`lvsfunc.render.find_scene_changes`."""

    WWXD = 0
    SCXVID = 1
    WWXD_SCXVID_UNION = 2
    WWXD_SCXVID_INTERSECTION = 3


x265_me_map: list[str] = [
    "dia", "hex", "umh", "star", "sea", "full"
]
