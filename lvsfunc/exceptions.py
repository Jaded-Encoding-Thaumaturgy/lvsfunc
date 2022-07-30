from __future__ import annotations

import vapoursynth as vs
from vskernels import Kernel, get_kernel

__all__ = [
    'ClipsAndNamedClipsError',
    'CompareSameKernelError',
    'FramePropError',
    'InvalidFormatError',
    'InvalidFramerateError',
    'NotEqualFormatsError',
    'TopFieldFirstError',
    'VariableFormatError',
    'VariableResolutionError',
]


class VariableFormatError(ValueError):
    """Raised when clip is of a variable format."""

    def __init__(self, function: str, message: str = "{func}: 'Variable-format clips not supported!'") -> None:
        self.function: str = function
        self.message: str = message
        super().__init__(self.message.format(func=self.function))


class VariableResolutionError(ValueError):
    """Raised when clip is of a variable resolution."""

    def __init__(self, function: str, message: str = "{func}: 'Variable-resolution clips not supported!'") -> None:
        self.function: str = function
        self.message: str = message
        super().__init__(self.message.format(func=self.function))


class NotEqualFormatsError(ValueError):
    """Raised when clips with different formats are given."""

    def __init__(self, function: str, message: str = "{func}: 'The format of both clips must be equal!'") -> None:
        self.function: str = function
        self.message: str = message
        super().__init__(self.message.format(func=self.function))


class InvalidFormatError(ValueError):
    """Raised when the given clip uses an invalid format."""

    def __init__(self, function: str, message: str = "{func}: 'Input clip must be of a YUV format!'") -> None:
        self.function: str = function
        self.message: str = message
        super().__init__(self.message.format(func=self.function))


class InvalidMatrixError(ValueError):
    """Raised when an invalid matrix is passed."""

    def __init__(self, function: str, matrix: int = 2,
                 message: str = "{func}: 'You can't set a matrix of {matrix}!'") -> None:
        self.function: str = function
        self.matrix: int = matrix
        self.message: str = message
        super().__init__(self.message.format(func=self.function))


class ClipsAndNamedClipsError(ValueError):
    """Raised when both positional clips and named clips are given."""

    def __init__(self, function: str,
                 message: str = "{func}: 'Positional clips and named keyword clips cannot both be given!") -> None:
        self.function: str = function
        self.message: str = message
        super().__init__(self.message.format(func=self.function))


class InvalidFramerateError(ValueError):
    """Raised when the given clip has an invalid framerate."""

    def __init__(self, function: str, clip: vs.VideoNode,
                 message: str = "{func}: '{fps} clips are not allowed!'") -> None:
        self.function: str = function
        self.clip: vs.VideoNode = clip
        self.message: str = message
        super().__init__(self.message.format(func=self.function, fps=self.clip.fps))


class CompareSameKernelError(ValueError):
    """Raised when two of the same kernels are compared to each other."""

    def __init__(self, function: str, kernel: Kernel | str,
                 message: str = "{func}: 'You may not compare {kernel} with itself!'") -> None:
        self.function: str = function
        self.message: str = message

        if isinstance(kernel, str):
            kernel = get_kernel(kernel)()

        self.kernel: Kernel = kernel

        super().__init__(self.message.format(func=self.function, kernel=self.kernel.__class__.__name__))


class FramePropError(ValueError):
    """Raised when there is an error with the frameprops."""

    def __init__(self, function: str, frameprop: str,
                 message: str = "{func}: 'Error while trying to get frameprop \"{frameprop}\"!'") -> None:
        self.function: str = function
        self.frameprop: str = frameprop
        self.message: str = message
        super().__init__(self.message.format(func=self.function, frameprop=frameprop))


class TopFieldFirstError(ValueError):
    """Raised when the user must pass a TFF argument."""

    def __init__(self, function: str,
                 message: str = "{func}: 'You must set `tff` for this clip!'") -> None:
        self.function: str = function
        self.message: str = message
        super().__init__(self.message.format(func=self.function))
