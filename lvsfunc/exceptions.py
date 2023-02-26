from __future__ import annotations

from vstools import CustomTypeError, FuncExceptT

__all__ = [
    'ClipsAndNamedClipsError',
]


class ClipsAndNamedClipsError(CustomTypeError):
    """Raised when both positional clips and named clips are given."""

    def __init__(
        self, func: FuncExceptT, message: str = 'Positional clips and named keyword clips cannot both be given!'
    ) -> None:
        super().__init__(message, func)
