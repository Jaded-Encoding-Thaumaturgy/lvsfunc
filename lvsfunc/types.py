from __future__ import annotations

from enum import IntEnum, auto
from typing import (Any, Callable, List, Literal, NamedTuple, NoReturn, Optional, Protocol, Sequence, Tuple, TypeVar,
                    Union)

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
    """Coefficients for matrix conversions."""

    k0: float
    phi: float
    alpha: float
    gamma: float


class Coordinate():
    """Positive set of (x, y) coordinates."""

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


class Resolution(NamedTuple):
    """Tuple representing a resolution."""

    """Width."""
    width: int

    """Height."""
    height: int


class ScaleAttempt(NamedTuple):
    """Tuple representing a descale attempt."""

    """Descaled frame in native resolution."""
    descaled: vs.VideoNode

    """Descaled frame reupscaled with the same kernel."""
    rescaled: vs.VideoNode

    """The native resolution."""
    resolution: Resolution

    """The subtractive difference between the original and descaled frame."""
    diff: vs.VideoNode


class SceneChangeMode(IntEnum):
    """Size type for :py:class:`lvsfunc.render.find_scene_changes`."""

    WWXD = 0
    SCXVID = 1
    WWXD_SCXVID_UNION = 2
    WWXD_SCXVID_INTERSECTION = 3


class Position(Coordinate):
    """Position type for :py:class:`lvsfunc.mask.BoundingBox`."""

    pass


class Size(Coordinate):
    """Size type for :py:class:`lvsfunc.mask.BoundingBox`."""

    pass


class Matrix(IntEnum):
    """Matrix coefficients (ITU-T H.265 Table E.5)."""

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
        """Return PermissionError if called."""
        raise PermissionError


class VSFunction(Protocol):
    """VapourSynth function."""

    def __call__(self, clip: vs.VideoNode, *args: Any, **kwargs: Any) -> vs.VideoNode:
        """Call the VapourSynth function."""
        ...


class VSIdxFunction(Protocol):
    """VapourSynth Indexing/Source function."""

    def __call__(self, path: str, *args: Any, **kwargs: Any) -> vs.VideoNode:
        """Call the VapourSynth function."""
        ...


class Shapes(IntEnum):
    """Convolution coordinates for :py:class:`lvsfunc.mask.mt_xxpand_multi`."""

    RECTANGLE = 0
    ELLIPSE = 1
    LOSANGE = 2


class RegressClips(NamedTuple):
    """Regress clip types for :py:class:`lvsfunc.recon.regress`."""

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


class IndexExists(IntEnum):
    """Check if certain files exist for :py:class:`lvsfunc.misc.source`."""

    PATH_IS_DGI = auto()
    PATH_IS_IMG = auto()
    LWI_EXISTS = auto()
    DGI_EXISTS = auto()
    NONE = auto()
