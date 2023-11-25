from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable

from stgpytools import FileNotExistsError, SPath, SPathLike, FuncExceptT
from vstools import FieldBased, FieldBasedT, Keyframes, VSCoreProxy, core, vs

from .exceptions import InvalidMatchError
from .types import Match, SectionPreset

__all__: list[str] = [
    "WobblyMeta",
    "WobblyVideo",
    "VfmParams",
    "VDecParams",
    "OrphanField",
    "InterlacedFade",
    "FreezeFrame"
]


@dataclass
class WobblyMeta:
    """Meta information about Wobbly."""

    version: int
    """The Wobbly version used. A value of -1 indicates an unknown version."""

    format_version: int
    """The project formatting version used. A value of -1 indicates an unknown version."""

    author: str | None = None
    """An optional field for external wobbly file authoring functions, such as lvsfunc/vsdeinterlace's."""


@dataclass
class WobblyVideo:
    """A class containing information about the clip used inside of wobbly."""

    file_path: SPathLike
    """The path to the input file."""

    source_filter: Callable[[str], vs.VideoNode] | str | VSCoreProxy
    """The source filter used to index the input file."""

    trims: list[tuple[int, int]]
    """The trims applied to the clip"""

    frame_rate: Fraction
    """The base framerate of the input clip."""

    def __post_init__(self) -> None:
        if isinstance(self.source_filter, str):
            obj = core

            for p in self.source_filter.split('.'):
                obj = getattr(obj, p)

            self.source_filter = obj

    def source(self, func_except: FuncExceptT | None = None, **kwargs: Any) -> vs.VideoNode:
        """Index the video."""
        func_except = func_except or self.source

        if not (sfile := SPath(self.file_path)).exists():
            raise FileNotExistsError(f"Could not find the input file, \"{sfile}\"!", func_except)

        src = self.source_filter(sfile.to_str(), **kwargs)  # type:ignore[operator]

        if src.fps != self.frame_rate:
            src = src.std.AssumeFPS(src, self.frame_rate.numerator, self.frame_rate.denominator)

        if not self.trims:
            return src

        return core.std.Splice([src.std.Trim(s, e) for s, e in self.trims])


@dataclass
class VfmParams:
    """VFM parameters used by Wobbly obtained from Wibbly."""

    order: FieldBasedT = True
    field: int = 2

    mode: int = 1
    mchroma: bool = True
    cthresh: float = 9.0
    chroma: bool = True

    mi: float = 80.0
    blockx: float = 16.0
    blocky: float = 16.0
    y0: float = 16.0
    y1: float = 16.0
    scthresh: float = 12.0
    micmatch: bool = False
    micout: bool = False

    def __post_init__(self) -> None:
        self.order = bool(int(FieldBased.from_param(self.order)) - 1)


@dataclass
class VDecParams:
    """VDecimate parameters used by Wobbly obtained from Wibbly."""

    cycle: int = 5
    chroma: bool = True

    dupthresh: float = 1.1
    scthresh: float = 15.0
    blockx: float = 32.0
    blocky: float = 32.0

    ovr: str | None = None
    dryrun: bool = False


@dataclass
class OrphanField:
    """Information about the orphan fields."""

    framenum: int
    """The frame number."""

    match: Match
    """The match for the given field."""

    def __str__(self) -> str:
        return f"Frame {self.framenum}: {self.match=} (orphan field)"

    @property
    def deinterlace_order(self) -> FieldBased:
        """The fieldorder to deinterlace in to properly deinterlace the orphan field."""
        if self.match in ("c"):
            raise InvalidMatchError(f"Orphans only exist on non-c matched frames ({self.framenum=})!", OrphanField)

        return FieldBased.TFF if self.match in ("n", "p") else FieldBased.BFF


@dataclass
class Section:
    """Information about the sections of a Wobbly file."""

    framenum: int
    """The first frame number of a section."""

    presets: list[SectionPreset] = field(default_factory=lambda: [])
    """A list of presets applied to the section of a clip."""


@dataclass
class InterlacedFade:
    """Information about interlaced fades."""

    framenum: int
    """The frame number."""

    field_difference: float
    """The differences between the two fields."""


@dataclass
class FreezeFrame:
    """Frame ranges to freeze."""

    start: int
    """The first frame of the frame range."""

    end: int
    """The last frame of the frame range."""

    replacement: int
    """The frame to replace all frames in the range with."""
