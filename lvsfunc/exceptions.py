from __future__ import annotations

from typing import Any

from stgpytools import SupportsString
from vstools import CustomTypeError, CustomValueError, FuncExceptT

__all__ = [
    'ClipsAndNamedClipsError',

    'NumpyArrayLoadError',
]


class ClipsAndNamedClipsError(CustomTypeError):
    """Raised when both positional clips and named clips are given."""

    def __init__(
        self, func: FuncExceptT, message: str = 'Positional clips and named keyword clips cannot both be given!'
    ) -> None:
        super().__init__(message, func)


class NumpyArrayLoadError(CustomValueError):
    """Raised when there's an issue with loading a numpy array."""

    def __init__(
        self, message: SupportsString | None = None, func: FuncExceptT | None = None, reason: Any = None, **kwargs: Any
    ) -> None:

        super().__init__(message, func, reason, **kwargs)
