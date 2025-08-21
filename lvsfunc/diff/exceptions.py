from typing import Any

from vstools import CustomError, FuncExceptT, SupportsString

__all__: list[str] = [
    "NoDifferencesFoundError",
    "NoGpuError",
    "VMAFError",
    "CustomOSError",
]


class NoDifferencesFoundError(CustomError):
    """Raised when no differences are found."""

    def __init__(
        self,
        message: SupportsString | None = "No differences found!",
        func: FuncExceptT | None = None,
        reason: Any = None,
        **kwargs: Any,
    ) -> None:
        self.message = message
        self.func = func
        self.reason = reason
        self.kwargs = kwargs

        super().__init__(message)


class NoGpuError(CustomError):
    """Raised when no GPU is detected."""

    def __init__(
        self,
        message: str = "No GPU detected!",
        func: FuncExceptT | None = None,
        reason: Any = None,
        **kwargs: Any,
    ) -> None:
        self.message = message
        self.func = func
        self.reason = reason
        self.kwargs = kwargs

        super().__init__(message)


class VMAFError(CustomError):
    """Raised when there's an issue with VMAF."""

    def __init__(
        self,
        message: SupportsString | None = "There was an issue with VMAF!",
        func: FuncExceptT | None = None,
        reason: Any = None,
        **kwargs: Any,
    ) -> None:
        self.message = message
        self.func = func
        self.reason = reason
        self.kwargs = kwargs

        super().__init__(message)


class CustomOSError(CustomError):
    """Raised when there's an OS error."""

    def __init__(
        self,
        message: SupportsString | None = "There was an OS error!",
        func: FuncExceptT | None = None,
        reason: Any = None,
        **kwargs: Any,
    ) -> None:
        self.message = message
        self.func = func
        self.reason = reason
        self.kwargs = kwargs

        super().__init__(message)
