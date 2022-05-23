from __future__ import annotations

from abc import ABC, abstractmethod
from functools import lru_cache
from math import sqrt
from typing import Any, Dict, Generator, List, Sequence, Tuple, Type

import vapoursynth as vs

from .types import Matrix

core = vs.core


__all__: List[str] = [
    'Bicubic', 'Bilinear', 'FmtConv', 'Lanczos', 'Point', 'Spline16', 'Spline36', 'Spline64',
    'Bessel', 'BicubicDidee', 'BicubicDogWay', 'BicubicSharp', 'BlackHarris', 'BlackMan', 'BlackManMinLobe',
    'BlackNuttall', 'Bohman', 'Box', 'BSpline', 'Catrom', 'Cosine', 'FlatTop', 'Gaussian', 'Ginseng', 'Hamming',
    'Hann', 'Hermite', 'Impulse', 'Kaiser', 'MinSide', 'Mitchell', 'NearestNeighbour', 'Parzen', 'Point', 'Quadratic',
    'Robidoux', 'RobidouxSharp', 'RobidouxSoft', 'Sinc', 'Welch', 'Wiener',
    'get_all_kernels', 'get_kernel'
]


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
    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
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

    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
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

    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
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

    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
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

    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
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

    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
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

    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
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

    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
        return core.resize.Spline64(clip, format=int(format),
                                    matrix=matrix, matrix_in=matrix_in, **self.kwargs)

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.resize.Spline64(clip, src_top=shift[0], src_left=shift[1],
                                    **self.kwargs)


class Example(Kernel):
    """
    Example Kernel class for documentation purposes.
    """
    def __init__(self, b: float = 0, c: float = 1/2, **kwargs: Any) -> None:
        self.b = b
        self.c = c
        super().__init__(**kwargs)

    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        """
        Perform a regular scaling operation

        :param clip:        Input clip
        :param width:       Output width
        :param height:      Output height
        :param shift:       Shift clip during the operation.
                            Expects a tuple of (src_top, src_left).
        """
        return core.resize.Bicubic(clip, width, height,
                                   src_top=shift[0], src_left=shift[1],
                                   filter_param_a=self.b, filter_param_b=self.c,
                                   **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        """
        Perform a regular descaling operation

        :param clip:        Input clip
        :param width:       Output width
        :param height:      Output height
        :param shift:       Shift clip during the operation.
                            Expects a tuple of (src_top, src_left).
        """
        return core.descale.Debicubic(clip, width, height, b=self.b,
                                      c=self.c, src_top=shift[0],
                                      src_left=shift[1])

    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
        """
        Perform a regular resampling operation

        :param clip:        Input clip
        :param format:      Output format
        :param matrix:      Output matrix. If `None`, will take the matrix from the input clip's frameprops.
        :param matrix_in:   Input matrix. If `None`, will take the matrix from the input clip's frameprops.

        :rtype:             ``VideoNode``
        """
        return core.resize.Bicubic(clip, format=int(format),
                                   filter_param_a=self.b, filter_param_b=self.c,
                                   matrix=matrix, matrix_in=matrix_in,
                                   **self.kwargs)

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        """
        Perform a regular shifting operation

        :param clip:        Input clip
        :param shift:       Shift clip during the operation.
                            Expects a tuple of (src_top, src_left).
        """
        return core.resize.Bicubic(clip, src_top=shift[0], src_left=shift[1],
                                   filter_param_a=self.b, filter_param_b=self.c,
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
    | Kernel inspired by a Didée post.
    | `See this doom9 post for more information <https://forum.doom9.org/showthread.php?p=1748922#post1748922>`_.

    Bicubic b=-0.5, c=0.25

    This is useful for downscaling content, but might not help much with upscaling.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(b=-1/2, c=1/4, **kwargs)


class BicubicDogWay(Bicubic):
    """
    Kernel inspired by DogWay.

    Bicubic b=-0.6, c=0.4

    This is useful for downscaling content with ringing.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(b=-0.6, c=0.4, **kwargs)


class FmtConv(Kernel):
    """
    Abstract fmtconv's resizer.

    Dependencies:

    * fmtconv
    """

    kernel: str

    def __init__(self, taps: int = 4, **kwargs: Any) -> None:
        self.taps = taps
        super().__init__(**kwargs)

    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.fmtc.resample(clip, width, height, shift[1], shift[0],
                                  kernel=self.kernel, **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.fmtc.resample(clip, width, height, shift[1], shift[0],
                                  kernel=self.kernel, invks=True,
                                  invkstaps=self.taps, **self.kwargs)

    def resample(self, clip: vs.VideoNode, format: vs.PresetFormat | vs.VideoFormat,
                 matrix: vs.MatrixCoefficients | Matrix | None = None,
                 matrix_in: vs.MatrixCoefficients | Matrix | None = None) -> vs.VideoNode:
        raise NotImplementedError()

    def shift(self, clip: vs.VideoNode, shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.fmtc.resample(clip, sw=shift[1], sy=shift[0], kernel=self.kernel,
                                  **self.kwargs)


class Box(FmtConv):
    """
    fmtconv's box resizer.
    """
    kernel = 'box'


class BlackMan(FmtConv):
    """
    fmtconv's blackman resizer.
    """
    kernel = 'blackman'


class BlackManMinLobe(FmtConv):
    """
    fmtconv's blackmanminlobe resizer.
    """
    kernel = 'blackmanminlobe'


class Sinc(FmtConv):
    """
    fmtconv's sinc resizer.
    """
    kernel = 'sinc'


class Gaussian(FmtConv):
    """
    fmtconv's gaussian resizer.
    """
    kernel = 'gaussian'

    def __init__(self, curve: int = 30, **kwargs: Any) -> None:
        super().__init__(a1=curve, **kwargs)


class NearestNeighbour(Gaussian):
    """
    Nearest Neighbour kernel.
    """
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(100, **kwargs)


class Impulse(FmtConv):
    """
    fmtconv's impulse resizer.
    """
    kernel = 'impulse'

    def __init__(self, impulse: Sequence[float], oversample: int = 8, taps: int = 1, **kwargs: Any) -> None:
        super().__init__(
            taps, impulse=[*impulse[:-1], *impulse[::-1]],
            kovrspl=oversample, **kwargs)

    def scale(self, clip: vs.VideoNode, width: int, height: int,
              shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.fmtc.resample(clip, width, height, shift[1], shift[0],
                                  kernel=self.kernel, sw=clip.width,
                                  sh=clip.height, **self.kwargs)

    def descale(self, clip: vs.VideoNode, width: int, height: int,
                shift: Tuple[float, float] = (0, 0)) -> vs.VideoNode:
        return core.fmtc.resample(clip, width, height, shift[1], shift[0],
                                  kernel=self.kernel, invks=True,
                                  invkstaps=self.taps, sw=clip.width,
                                  sh=clip.height, **self.kwargs)


class Quadratic(Impulse):
    """
    Quadratic kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            0.75, 0.746094, 0.734375, 0.714844, 0.6875,
            0.652344, 0.609375, 0.558594, 0.5, 0.439453,
            0.382813, 0.330078, 0.28125, 0.236328, 0.195313,
            0.158203, 0.125, 0.095703, 0.070313, 0.048828,
            0.03125, 0.017578, 0.007813, 0.001953
        ], 16, **kwargs)


class Wiener(Impulse):
    """
    Wiener kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.928293, 0.847768, 0.749610, 0.625, 0.470033,
            0.300445, 0.136885, 0, -0.094068, -0.147204,
            -0.165801, -0.15625, -0.1255, -0.082723,
            -0.037647, 0, 0.022825, 0.032783, 0.034161,
            0.03125, 0.02491, 0.017308, 0.008864
        ], oversample, **kwargs)


class Hann(Impulse):
    """
    Hann kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.9721491276507364, 0.8916666533754284, 0.7673293227933666,
            0.6123898750249921, 0.44274830753566713, 0.27481699575031854,
            0.12341360408603762, 0, -0.08848381495693607, -0.14005052617158592,
            -0.1573484857988253, -0.14670726866144826, -0.11675289338122011,
            -0.0768542368708979, -0.035667086889988917, 0, 0.025852297356152947,
            0.040259628673424544, 0.043939594567039456, 0.039299593276647324,
            0.029609836521073, 0.018187607754470616, 0.007745261904000362,
            0, -0.0044240051920867865, -0.005835794531242358, -0.005144384187084287,
            -0.0034614139060841795, -0.0017466187017072979, -0.0005766441854451786,
            -0.00007568486302246578
        ], oversample, **kwargs)


class Hamming(Impulse):
    """
    Hamming kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.9723291304741598, 0.8923302555040387, 0.7686246617990514,
            0.6142487927491155, 0.4448795641717659, 0.27675712509487843,
            0.1246257815086694, 0, -0.0900023682175275, -0.1431203033588165,
            -0.16168530396390082, -0.1517323766550889, -0.12167980632033411,
            -0.0808254466432445, -0.0379149269102415, 0, 0.02826674933221172,
            0.044845606381107544, 0.05006826118507596, 0.0460528222676711,
            0.03593314767037512, 0.02307155155805429, 0.010401622971455375,
            0, -0.00707512686962141, -0.010701323742157228, -0.011434689771183611,
            -0.010173206936358085, -0.00783656756150458, -0.005137221895242707,
            -0.002481597155711647
        ], oversample, **kwargs)


class BlackHarris(Impulse):
    """
    Black-Harris kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.9690685474542851, 0.8804147429536661, 0.7457038324654484,
            0.5820238498592893, 0.408897820926439, 0.24504664162741924,
            0.10556008266546878, 0, -0.06828556374209023, -0.10164720692199704,
            -0.10668443324736704, -0.09229279162100884, -0.0676826118865924,
            -0.040770939188391156, -0.01719366607497128, 0, 0.010072521093743276,
            0.013950171901372979, 0.013442938661666109, 0.010539924532807445,
            0.006912782290973393, 0.0036717082778625404, 0.001343980906503044,
            0, -0.0005599450449479095, -0.0006299356259012779, -0.00047599901604884737,
            -0.0002782179944466215, -0.0001254132897686219, -0.00003940328671242334,
            -0.000006272327028117027
        ], oversample, **kwargs)


class BlackNuttall(Impulse):
    """
    BlackNuttall kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.9691956173858006, 0.8808777891436077, 0.7465903227462598,
            0.583261858851737, 0.41026820009726694, 0.2462414690601752,
            0.10626931490160989, 0, -0.06906778816628918, -0.10311203169060508,
            -0.10858461954425613, -0.09429622625282544, -0.06945329948290131,
            -0.04204507233452078, -0.0178310531150637, 0, 0.010590373575929674,
            0.014791046691013261, 0.0143917812832477, 0.01141108308851331,
            0.007582722772125722, 0.004090031528918704, 0.0015247187900517072,
            0, -0.0006668666328159042, -0.0007753811435345259, -0.0006111170869562098,
            -0.0003782503724444364, -0.00018625686680715366, -0.00006947677421552765,
            -0.00001734615796446616
        ], oversample, **kwargs)


class FlatTop(Impulse):
    """
    FlatTop kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.9633262343597194, 0.859593850914732, 0.7061738614429447,
            0.5274619393571068, 0.3494083785508531, 0.1941326535234994,
            0.07599859616307823, 0, -0.03742790728859844, -0.045746423402100424,
            -0.03680885348596081, -0.021591047728118973, -0.007969308213425627,
            0.00010539639481656004, 0.002167459237080162, 0, -0.003812769923009659,
            -0.007053787251496119, -0.008498312606009256, -0.007982808809703638,
            -0.0060878619550795154, -0.003677603986271232, -0.0015053481284463162,
            0, 0.0007565960905941711, 0.0009239058962157, 0.0007553677173860026,
            0.0004791071697109673, 0.00023850930336092043, 0.00008824527524187423,
            0.000021135402405053327
        ], oversample, **kwargs)


class MinSide(Impulse):
    """
    MinSide kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.9677067397427601, 0.8754735424031383, 0.7363116111669247,
            0.5690387749427253, 0.3947100931903589, 0.2328726279464744,
            0.09846997346812622, 0, -0.060828473848914016, -0.08807741082408858,
            -0.08963798222912361, -0.07495103916223587, -0.05294982732350461,
            -0.030621864426414024, -0.012354100121804074, 0, 0.006550750370351611,
            0.008581357979868063, 0.007789505667884757, 0.00572824890289049,
            0.0035077922683009735, 0.001731217648211203, 0.0005857853596332941,
            0, -0.0002050370640200731, -0.0002095361090755842, -0.00014308227339085642,
            -0.00007543851733140218, -0.000030927452169915216, -0.000009168350688844679,
            -0.00000158174014270345
        ], oversample, **kwargs)


class Ginseng(Impulse):
    """
    Ginseng kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.9706924517023813, 0.8863037293563394, 0.7568846746026882,
            0.5974484350594943, 0.42568771143242046, 0.2593638071484244,
            0.1138155395729318, 0, -0.07663423509063601, -0.11630395745498025,
            -0.12412241952630289, -0.10861320529064979, -0.07983137551487393,
            -0.04746371544549015, -0.01925303598542219, 0, 0.008737966998564498,
            0.00827789347498015, 0.0019289633237434013, -0.006160413752293629,
            -0.012153940393777712, -0.013434473237575344, -0.00910161101088654
        ], oversample, **kwargs)


class Welch(Impulse):
    """
    Welch kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.972804, 0.894064, 0.771960, 0.618936, 0.450106, 0.281349,
            0.127371, 0, -0.093051, -0.148802, -0.168948, -0.159155, -0.127874,
            -0.0848512, -0.039589, 0, 0.028562, 0.0437654, 0.046219, 0.0389045,
            0.026257, 0.0130728, 0.003457
        ], oversample, **kwargs)


class Cosine(Impulse):
    """
    Cosine kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.972409, 0.892614, 0.769145, 0.614928, 0.445557, 0.277261,
            0.124857, -0, -0.090029, -0.142854, -0.160801, -0.150053, -0.119324,
            -0.0782968, -0.036093, 0, 0.025353, 0.0382818, 0.039802, 0.0329539,
            0.021856, 0.0106832, 0.002771
        ], oversample, **kwargs)


class Bessel(Impulse):
    """
    Bessel kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1.5708, 1.525858, 1.39627, 1.196854, 0.94988, 0.681773,
            0.419361, 0.186267, 0, -0.129804, -0.201802, -0.222051,
            -0.202077, -0.156337, -0.0995575, -0.044427, 0, 0.029012,
            0.0420623, 0.041868, 0.0330862, 0.020877, 0.00967627, 0.002371
        ], oversample, **kwargs)


class Parzen(Impulse):
    """
    Parzen kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            0.666667, 0.648727, 0.596804, 0.51624, 0.415088, 0.303095, 0.190509,
            0.086876, 0, -0.064824, -0.105205, -0.121655, -0.117225, -0.096848,
            -0.0665116, -0.032382, 0, 0.026335, 0.0439404, 0.051856, 0.0506892,
            0.042271, 0.0291773, 0.014224, 0, -0.011489, -0.0190243, -0.022227,
            -0.0214634, -0.017647, -0.0119891, -0.005745, 0, 0.004475, 0.00727292,
            0.008338, 0.00789788, 0.006366, 0.00423604, 0.001986, 0, -0.001471,
            -0.00232189, -0.002577, -0.00235492, -0.001824, -0.00116114, -0.000518,
            0, 0.000341, 0.000502619, 0.000515, 0.000430408, 0.000301, 0.000169602,
            0.000066, 0, -0.00003, -0.0000341078, -0.000025, -0.0000138158, -0.000005,
            -0.00000118185, 0
        ], oversample, **kwargs)


class Kaiser(Impulse):
    """
    Kaiser kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.973784, 0.897692, 0.779078, 0.629225, 0.462012, 0.29231, 0.134312,
            0, -0.102037, -0.167326, -0.195688, -0.190881, -0.159791, -0.111303,
            -0.055016, 0, 0.046264, 0.0786285, 0.094631, 0.0944555, 0.080540, 0.0569238,
            0.028458, 0, -0.024290, -0.0414535, -0.050006, -0.0499464, -0.042553, -0.0300094,
            -0.014951, 0, 0.012629, 0.0214054, 0.025619, 0.0253622, 0.021395, 0.0149254,
            0.007348, 0, -0.006043, -0.0100898, -0.011883, -0.0115622, -0.009575, -0.00654779,
            -0.003156, 0, 0.002475, 0.00402406, 0.004606, 0.00434445, 0.003478, 0.00229289,
            0.001061, 0, -0.000757, -0.0011651, -0.001252, -0.00109846, -0.000808, -0.000481802, -0.000197
        ], oversample, **kwargs)


class Bohman(Impulse):
    """
    Bohman kernel.
    """

    def __init__(self, oversample: int, **kwargs: Any) -> None:
        super().__init__([
            1, 0.973334, 0.896071, 0.77599, 0.624897, 0.457161, 0.287989, 0.131668, 0, -0.098853,
            -0.161007, -0.186917, -0.180888, -0.150148, -0.103645, -0.050742, 0, 0.04179, 0.0702274,
            0.083521, 0.0823302, 0.069284, 0.0482961, 0.023797, 0, -0.019685, -0.0330319, -0.039145,
            -0.0383729, -0.032053, -0.0221387, -0.010789, 0, 0.008687, 0.0143432, 0.016696, 0.0160458,
            0.013115, 0.00884562, 0.0042, 0, -0.003187, -0.00508814, -0.005708, -0.00526944, -0.004121,
            -0.00264747, -0.001192, 0, 0.000798, 0.00118257, 0.001221, 0.00102559, 0.00072, 0.000408479,
            0.000159, 0, -0.000073, -0.0000834291, -0.000062, -0.000033957, -0.000013, -0.00000291302, 0
        ], oversample, **kwargs)


@lru_cache
def get_all_kernels() -> List[Type[Kernel]]:
    """
    Get all kernels as a list.
    """
    def _subclasses(cls: Type[Kernel]) -> Generator[Type[Kernel], None, None]:
        for subclass in cls.__subclasses__():
            yield from _subclasses(subclass)
            yield subclass

    # https://github.com/python/mypy/issues/5374
    return list(set(_subclasses(Kernel)))  # type: ignore


@lru_cache
def get_kernel(name: str) -> Type[Kernel]:
    """
    Get a kernel by name.

    :param name: Kernel name.
    :return: Kernel class.
    """
    all_kernels = get_all_kernels()
    search_str = name.lower().strip()

    for kernel in all_kernels:
        if kernel.__name__.lower() == search_str:
            return kernel

    raise ValueError(f"get_kernel: 'Unknown kernel: {name}!'")
