"""
    Kernels for VapourSynth internal resizers.
    Intended for use by :py:mod:`lvsfunc.scale` functions.
"""
from abc import ABC, abstractmethod
from math import sqrt
from typing import Any, Dict, Tuple, Union, Optional

import vapoursynth as vs

core = vs.core


class Kernel(ABC):
    """
    Abstract scaling kernel interface.

    Additional kwargs supplied to constructor are passed only to the internal
    resizer, not the descale resizer.
    """

    kwargs: Dict[str, Any]
    """Arguments passed to the kernel filter"""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    @abstractmethod
    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        pass

    @abstractmethod
    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        pass

    @abstractmethod
    def resample(self, clip: vs.VideoNode, format: Union[vs.PresetFormat, vs.VideoFormat],
                 matrix: Optional[vs.MatrixCoefficients] = None,
                 matrix_in: Optional[vs.MatrixCoefficients] = None) -> vs.VideoNode:
        pass

    @abstractmethod
    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        pass


class Point(Kernel):
    """ Built-in point resizer. """
    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Point(clip, width, height, src_top=shift[0],
                                 src_left=shift[1], **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Point(clip, width, height, src_top=shift[0],
                                 src_left=shift[1])

    def resample(self, clip: vs.VideoNode, format: Union[vs.PresetFormat, vs.VideoFormat],
                 matrix: Optional[vs.MatrixCoefficients] = None,
                 matrix_in: Optional[vs.MatrixCoefficients] = None) -> vs.VideoNode:
        return core.resize.Point(clip, format=int(format),
                                 matrix=matrix, matrix_in=matrix_in,
                                 **self.kwargs)

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Point(clip, src_top=shift[0], src_left=shift[1], **self.kwargs)


class Bilinear(Kernel):
    """ Built-in bilinear resizer. """
    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Bilinear(clip, width, height, src_top=shift[0],
                                    src_left=shift[1], **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.descale.Debilinear(clip, width, height, src_top=shift[0],
                                       src_left=shift[1])

    def resample(self, clip: vs.VideoNode, format: Union[vs.PresetFormat, vs.VideoFormat],
                 matrix: Optional[vs.MatrixCoefficients] = None,
                 matrix_in: Optional[vs.MatrixCoefficients] = None) -> vs.VideoNode:
        return core.resize.Bilinear(clip, format=int(format),
                                    matrix=matrix, matrix_in=matrix_in,
                                    **self.kwargs)

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Bilinear(clip, src_top=shift[0], src_left=shift[1], **self.kwargs)


class Bicubic(Kernel):
    """
    Built-in bicubic resizer.
    b=0, c=0.5

    Dependencies:

    * VapourSynth-descale

    :param b: B-param for bicubic kernel
    :param c: C-param for bicubic kernel
    """
    def __init__(self, b: float = 0, c: float = 1/2, **kwargs: Any) -> None:
        self.b = b
        self.c = c
        super().__init__(**kwargs)

    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Bicubic(clip, width, height,
                                   src_top=shift[0], src_left=shift[1],
                                   filter_param_a=self.b, filter_param_b=self.c,
                                   **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.descale.Debicubic(clip, width, height, b=self.b,
                                      c=self.c, src_top=shift[0],
                                      src_left=shift[1])

    def resample(self, clip: vs.VideoNode, format: Union[vs.PresetFormat, vs.VideoFormat],
                 matrix: Optional[vs.MatrixCoefficients] = None,
                 matrix_in: Optional[vs.MatrixCoefficients] = None) -> vs.VideoNode:
        return core.resize.Bicubic(clip, format=int(format),
                                   filter_param_a=self.b, filter_param_b=self.c,
                                   matrix=matrix, matrix_in=matrix_in,
                                   **self.kwargs)

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Bicubic(clip, src_top=shift[0], src_left=shift[1],
                                   filter_param_a=self.b, filter_param_b=self.c,
                                   **self.kwargs)


class Lanczos(Kernel):
    """
    Built-in lanczos resizer.

    Dependencies:

    * VapourSynth-descale

    :param taps: taps param for lanczos kernel
    """
    def __init__(self, taps: int = 3, **kwargs: Any) -> None:
        self.taps = taps
        super().__init__(**kwargs)

    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Lanczos(clip, width, height, src_top=shift[0],
                                   src_left=shift[1], filter_param_a=self.taps,
                                   **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.descale.Delanczos(clip, width, height, taps=self.taps,
                                      src_top=shift[0], src_left=shift[1])

    def resample(self, clip: vs.VideoNode, format: Union[vs.PresetFormat, vs.VideoFormat],
                 matrix: Optional[vs.MatrixCoefficients] = None,
                 matrix_in: Optional[vs.MatrixCoefficients] = None) -> vs.VideoNode:
        return core.resize.Lanczos(clip, format=int(format),
                                   matrix=matrix, matrix_in=matrix_in,
                                   filter_param_a=self.taps, **self.kwargs)

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Lanczos(clip, src_top=shift[0], src_left=shift[1],
                                   filter_param_a=self.taps, **self.kwargs)


class Spline16(Kernel):
    """
    Built-in spline16 resizer.

    Dependencies:

    * VapourSynth-descale
    """
    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Spline16(clip, width, height, src_top=shift[0],
                                    src_left=shift[1], **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.descale.Despline16(clip, width, height, src_top=shift[0],
                                       src_left=shift[1])

    def resample(self, clip: vs.VideoNode, format: Union[vs.PresetFormat, vs.VideoFormat],
                 matrix: Optional[vs.MatrixCoefficients] = None,
                 matrix_in: Optional[vs.MatrixCoefficients] = None) -> vs.VideoNode:
        return core.resize.Spline16(clip, format=int(format),
                                    matrix=matrix, matrix_in=matrix_in, **self.kwargs)

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Spline16(clip, src_top=shift[0], src_left=shift[1],
                                    **self.kwargs)


class Spline36(Kernel):
    """
    Built-in spline36 resizer.

    Dependencies:

    * VapourSynth-descale
    """
    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Spline36(clip, width, height, src_top=shift[0],
                                    src_left=shift[1], **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.descale.Despline36(clip, width, height, src_top=shift[0],
                                       src_left=shift[1])

    def resample(self, clip: vs.VideoNode, format: Union[vs.PresetFormat, vs.VideoFormat],
                 matrix: Optional[vs.MatrixCoefficients] = None,
                 matrix_in: Optional[vs.MatrixCoefficients] = None) -> vs.VideoNode:
        return core.resize.Spline36(clip, format=int(format),
                                    matrix=matrix, matrix_in=matrix_in, **self.kwargs)

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Spline36(clip, src_top=shift[0], src_left=shift[1],
                                    **self.kwargs)


class Spline64(Kernel):
    """
    Built-in spline64 resizer.

    Dependencies:

    * VapourSynth-descale
    """
    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Spline64(clip, width, height, src_top=shift[0],
                                    src_left=shift[1], **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.descale.Despline64(clip, width, height, src_top=shift[0],
                                       src_left=shift[1])

    def resample(self, clip: vs.VideoNode, format: Union[vs.PresetFormat, vs.VideoFormat],
                 matrix: Optional[vs.MatrixCoefficients] = None,
                 matrix_in: Optional[vs.MatrixCoefficients] = None) -> vs.VideoNode:
        return core.resize.Spline64(clip, format=int(format),
                                    matrix=matrix, matrix_in=matrix_in, **self.kwargs)

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Spline64(clip, src_top=shift[0], src_left=shift[1],
                                    **self.kwargs)


class BSpline(Bicubic):
    """
    Bicubic b=1, c=0
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(b=1, c=0, **kwargs)


class Hermite(Bicubic):
    """
    Bicubic b=0, c=0
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(b=0, c=0, **kwargs)


class Mitchell(Bicubic):
    """
    Bicubic b=1/3, c=1/3
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(b=1/3, c=1/3, **kwargs)


class Catrom(Bicubic):
    """
    Bicubic b=0, c=0.5
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(b=0, c=1/2, **kwargs)


class BicubicSharp(Bicubic):
    """
    Bicubic b=0, c=1
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(b=0, c=1, **kwargs)


class RobidouxSoft(Bicubic):
    """
    Bicubic b=0.67962, c=0.16019
    """
    def __init__(self, **kwargs: Any) -> None:
        b = (9 - 3 * sqrt(2)) / 7
        c = (1 - b) / 2
        super().__init__(b=b, c=c, **kwargs)


class Robidoux(Bicubic):
    """
    Bicubic b=0.37822, c=0.31089
    """
    def __init__(self, **kwargs: Any) -> None:
        b = 12 / (19 + 9 * sqrt(2))
        c = 113 / (58 + 216 * sqrt(2))
        super().__init__(b=b, c=c, **kwargs)


class RobidouxSharp(Bicubic):
    """
    Bicubic b=0.26201, c=0.36899
    """
    def __init__(self, **kwargs: Any) -> None:
        b = 6 / (13 + 7 * sqrt(2))
        c = 7 / (2 + 12 * sqrt(2))
        super().__init__(b=b, c=c, **kwargs)


class BicubicDidee(Bicubic):
    """
    Kernel inspired by a Didée post.
    See: https://forum.doom9.org/showthread.php?p=1748922#post1748922.

    Bicubic b=-0.5, c=0.25

    This is useful for downscaling content, but might not help much with upscaling.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(b=-1/2, c=1/4, **kwargs)
