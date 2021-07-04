from __future__ import annotations

from ..sector import Sector
from enum import IntEnum
from fractions import Fraction
from io import BufferedReader
from typing import Dict, List

class PGCOffset(IntEnum):
    NB_PROGRAMS: int
    NB_CELLS: int
    PLAYBACK_TIME: int
    UOPS: int
    PGC_AST_CTL: int
    PGC_SPST_CTL: int
    NEXT_PGCN: int
    PREVIOUS_PGCN: int
    GOUP_PGCN: int
    PGC_STILL_TIME: int
    PG_PLAYBACK_MODE: int
    PALETTE: int
    COMMANDS_OFFSET: int
    PROGRAM_MAP_OFFSET: int
    CELL_PLAYBACK_INFO_TABLE_OFFSET: int
    CELL_POS_INFO_TABLE_OFFSET: int

class PlaybackTime:
    fps: int
    hours: int
    minutes: int
    seconds: int
    frames: int

class ProgramChain:
    duration: PlaybackTime
    nb_program: int
    playback_times: List[PlaybackTime]

class VTSPGCI(Sector):
    nb_program_chains: int
    program_chains: List[ProgramChain]
    chain_offset: int
    def __init__(self, ifo: BufferedReader) -> None: ...
    def load(self) -> VTSPGCI: ...

FRAMERATE: Dict[int, Fraction]
