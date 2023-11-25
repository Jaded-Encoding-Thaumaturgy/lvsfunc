from typing import Literal, TypeAlias, Callable
from vstools import vs

__all__ = [
    "Match", "OrphanMatch",
    "SectionPreset"
]


Match: TypeAlias = Literal['b'] | Literal['c'] | Literal['n'] | Literal['p'] | Literal['u']
"""A type representing all possible fieldmatches."""

OrphanMatch: TypeAlias = Literal['b'] | Literal['n'] | Literal['p'] | Literal['u']
"""Valid matches to be considered orphans.."""

SectionPreset = Callable[[vs.VideoNode], vs.VideoNode]
"""A callable preset applied to a section."""
