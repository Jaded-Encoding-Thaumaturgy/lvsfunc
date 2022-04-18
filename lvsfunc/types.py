from __future__ import annotations

from enum import IntEnum
from typing import (Any, List, NamedTuple, NoReturn, Optional, Protocol, Tuple,
                    Union)

import vapoursynth as vs


__all__: List[str] = [
    'Range',
    'Coordinate', 'Position', 'Size',
    'Matrix', 'Coefs',
    'VSFunction'
]

Range = Union[Optional[int], Tuple[Optional[int], Optional[int]]]


class Coordinate():
    """
    A positive set of (x, y) coordinates.
    """
    x: int
    y: int

    def __init__(self, x: int, y: int):
        if x < 0 or y < 0:
            raise ValueError(f"{self.__class__.__name__}: 'Can't be negative!'")
        self.x = x
        self.y = y


class Position(Coordinate):
    pass


class Size(Coordinate):
    pass


class Matrix(IntEnum):
    """Matrix coefficients (ITU-T H.265 Table E.5)"""
    RGB = 0
    GBR = 0
    BT709 = 1
    UNKNOWN = 2
    _RESERVED = 3
    FCC = 4
    BT470BG = 5
    SMPTE170M = 6
    SMPTE240M = 7
    YCGCO = 8
    BT2020NC = 9
    BT2020C = 10
    SMPTE2085 = 11
    CHROMA_DERIVED_NC = 12
    CHROMA_DERIVED_C = 13
    ICTCP = 14

    @property
    def RESERVED(self) -> NoReturn:
        raise PermissionError


class Coefs(NamedTuple):
    k0: float
    phi: float
    alpha: float
    gamma: float


class VSFunction(Protocol):
    def __call__(self, clip: vs.VideoNode, *args: Any, **kwargs: Any) -> vs.VideoNode:
        ...


class Shapes(IntEnum):
    RECTANGLE = 0
    ELLIPSE = 1
    LOSANGE = 2
