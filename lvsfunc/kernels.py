"""
Kernels for vapoursynth internal resizers. Intended for use by
:py:mod:`lvsfunc.scale` functions.
"""
from abc import ABC, abstractmethod

import vapoursynth as vs

core = vs.core


class Kernel(ABC):
    """ Abstract scaling kernel interface. """
    @abstractmethod
    def scale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        pass

    @abstractmethod
    def descale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        pass


class Bilinear(Kernel):
    """ Built-in bilinear resizer. """
    def scale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.resize.Bilinear(clip, width, height, **kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int, **kwargs):
        return core.descale.Debilinear(clip, width, height, **kwargs)


class Bicubic(Kernel):
    """
    Built-in bicubic resizer.

    :param b: B-param for bicubic kernel
    :param c: C-param for bicubic kernel
    """
    def __init__(self, b: float = 0, c: float = 1/2):
        self.b = b
        self.c = c

    def scale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.resize.Bicubic(clip, width, height,
                                   filter_param_a=self.b,
                                   filter_param_b=self.c, **kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.descale.Debicubic(clip, width, height, b=self.b,
                                      c=self.c, **kwargs)


class Lanczos(Kernel):
    """
    Built-in lanczos resizer.

    :param taps: taps param for lanczos kernel
    """
    def __init__(self, taps: int = 4):
        self.taps = taps

    def scale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.resize.Lanczos(clip, width, height,
                                   filter_param_a=self.taps, **kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.descale.Delanczos(clip, width, height, taps=self.taps,
                                      **kwargs)


class Spline16(Kernel):
    """ Built-in spline16 resizer. """
    def scale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.resize.Spline16(clip, width, height, **kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.descale.Despline16(clip, width, height, **kwargs)


class Spline36(Kernel):
    """ Built-in spline36 resizer. """
    def scale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.resize.Spline36(clip, width, height, **kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.descale.Despline36(clip, width, height, **kwargs)


class Spline64(Kernel):
    """ Built-in spline64 resizer. """
    def scale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.resize.Spline64(clip, width, height, **kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int, **kwargs) -> vs.VideoNode:
        return core.descale.Despline64(clip, width, height, **kwargs)
