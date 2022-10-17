from __future__ import annotations

from vstools import CustomValueError, FuncExceptT

__all__ = [
    'ClipsAndNamedClipsError'
]


class ClipsAndNamedClipsError(CustomValueError):
    """Raised when both positional clips and named clips are given."""

    def __init__(
        self, func: FuncExceptT, message: str = 'Positional clips and named keyword clips cannot both be given!'
    ) -> None:
        super().__init__(message, func)
