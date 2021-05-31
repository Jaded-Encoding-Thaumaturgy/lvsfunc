"""
Kernels for vapoursynth internal resizers. Intended for use by
:py:mod:`lvsfunc.scale` functions.
"""
from abc import ABC, abstractmethod
from typing import Any, Tuple

import vapoursynth as vs

core = vs.core


class Kernel(ABC):
    """
    Abstract scaling kernel interface.

    Additional kwargs supplied to constructor are passed only to the internal
    resizer, not the descale resizer.
    """
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


class Bicubic(Kernel):
    """
    Built-in bicubic resizer.

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
                                   filter_param_a=self.b,
                                   filter_param_b=self.c, src_top=shift[0],
                                   src_left=shift[1],
                                   **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.descale.Debicubic(clip, width, height, b=self.b,
                                      c=self.c, src_top=shift[0],
                                      src_left=shift[1])


class Lanczos(Kernel):
    """
    Built-in lanczos resizer.

    Dependencies:
    * VapourSynth-descale

    :param taps: taps param for lanczos kernel
    """
    def __init__(self, taps: int = 4, **kwargs: Any) -> None:
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
