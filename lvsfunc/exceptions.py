from __future__ import annotations

from typing import Any

from jetpytools import (
    CustomTypeError,
    CustomValueError,
    FileNotExistsError,
    FuncExceptT,
    SPath,
    SPathLike,
    SupportsString,
)

__all__ = [
    "ClipsAndNamedClipsError",
    "InvalidAssFileError",
    "NumpyArrayLoadError",
]


class ClipsAndNamedClipsError(CustomTypeError):
    """Raised when both positional clips and named clips are given."""

    def __init__(
        self,
        func: FuncExceptT,
        message: str = "Positional clips and named keyword clips cannot both be given!",
    ) -> None:
        super().__init__(message, func)


class NumpyArrayLoadError(CustomValueError):
    """Raised when there's an issue with loading a numpy array."""

    def __init__(
        self,
        message: SupportsString | None = None,
        func: FuncExceptT | None = None,
        reason: Any = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, func, reason, **kwargs)


class InvalidAssFileError(CustomValueError):
    """Raised when an ASS file is not valid."""

    def __init__(
        self,
        message: SupportsString | None = None,
        func: FuncExceptT | None = None,
        reason: Any = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, func, reason, **kwargs)

    @classmethod
    def check(cls, file: SPathLike, func: FuncExceptT | None = None) -> bool:
        if not (spath := SPath(file)).exists():
            raise FileNotExistsError(f'Could not find the file, "{spath}".', func, spath)

        if spath.read_bytes()[:3] != b"\xef\xbb\xbf":
            raise cls(f'The file, "{spath}", is not a valid UTF-8 file.', func, spath)

        return True
