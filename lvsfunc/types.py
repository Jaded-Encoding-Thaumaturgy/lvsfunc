from __future__ import annotations

from enum import IntEnum
from typing import (Any, Callable, List, Literal, NamedTuple, NoReturn,
                    Optional, Protocol, Sequence, Tuple, TypeVar, Union)

import vapoursynth as vs

__all__: List[str] = [
    'Coefs', 'Coordinate', 'CreditMask', 'CURVES', 'CustomScaler', 'Direction', 'F', 'Matrix', 'Position', 'Range',
    'RegressClips', 'Resolution', 'ScaleAttempt', 'SceneChangeMode', 'Size', 'T', 'VideoProp', 'VSFunction'
]


CreditMask = Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode]
CustomScaler = Callable[[vs.VideoNode, int, int], vs.VideoNode]
Range = Union[Optional[int], Tuple[Optional[int], Optional[int]]]


VideoProp = Union[
    int, Sequence[int],
    float, Sequence[float],
    str, Sequence[str],
    vs.VideoNode, Sequence[vs.VideoNode],
    vs.VideoFrame, Sequence[vs.VideoFrame],
    Callable[..., Any], Sequence[Callable[..., Any]]
]

F = TypeVar("F", bound=Callable[..., vs.VideoNode])
T = TypeVar("T", bound=VideoProp)


class Coefs(NamedTuple):
    k0: float
    phi: float
    alpha: float
    gamma: float


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


class Direction(IntEnum):
    """
    Enum to simplify direction argument.
    """
    HORIZONTAL = 0
    VERTICAL = 1


class Resolution(NamedTuple):
    """ Tuple representing a resolution. """

    width: int
    """ Width. """

    height: int
    """ Height. """


class ScaleAttempt(NamedTuple):
    """ Tuple representing a descale attempt. """

    descaled: vs.VideoNode
    """ Descaled frame in native resolution. """

    rescaled: vs.VideoNode
    """ Descaled frame reupscaled with the same kernel. """

    resolution: Resolution
    """ The native resolution. """

    diff: vs.VideoNode
    """ The subtractive difference between the original and descaled frame. """


class SceneChangeMode(IntEnum):
    WWXD = 0
    SCXVID = 1
    WWXD_SCXVID_UNION = 2
    WWXD_SCXVID_INTERSECTION = 3


class Position(Coordinate):
    pass


class Size(Coordinate):
    pass


class Matrix(vs.MatrixCoefficients):
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


class VSFunction(Protocol):
    def __call__(self, clip: vs.VideoNode, *args: Any, **kwargs: Any) -> vs.VideoNode:
        ...


class Shapes(IntEnum):
    RECTANGLE = 0
    ELLIPSE = 1
    LOSANGE = 2


class RegressClips(NamedTuple):
    slope: vs.VideoNode
    intercept: vs.VideoNode
    correlation: vs.VideoNode


CURVES = Literal[
    vs.TransferCharacteristics.TRANSFER_IEC_61966_2_1,
    vs.TransferCharacteristics.TRANSFER_BT709,
    vs.TransferCharacteristics.TRANSFER_BT601,
    vs.TransferCharacteristics.TRANSFER_ST240_M,
    vs.TransferCharacteristics.TRANSFER_BT2020_10,
    vs.TransferCharacteristics.TRANSFER_BT2020_12,
]
