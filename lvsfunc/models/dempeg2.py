import warnings
from dataclasses import dataclass
from math import ceil
from typing import Any, SupportsFloat

from vsexprtools import expr_func
from vskernels import Catrom
from vstools import (InvalidColorFamilyError, LengthMismatchError, PlanesT,
                     UnsupportedVideoFormatError, depth, inject_self, iterate,
                     normalize_planes, vs, depth)

from .base import Base1xModelWithStrength

__all__: list[str] = [
    "LDempeg2",
]


# TODO: Expand upon this with different models for different bitrates and encoders.
@dataclass
class LDempeg2(Base1xModelWithStrength):
    """
    Dempeg2 model to denoise MPEG-2 sources.
    """

    _model_filename = '1x_dempeg2_fp32.onnx'

    @inject_self
    def apply(
        self, clip: vs.VideoNode,
        strength: SupportsFloat | vs.VideoNode | None = None, show_mask: bool = False,
        iterations: int = 1, planes: PlanesT = 0, **kwargs: Any
    ) -> vs.VideoNode:
        """
        Apply the model to the clip.

        :param clip:        The clip to process.
        :param strength:    The "strength" of the model. Works by merging the clip with a "strength" mask,
                            just like DPIR. Higher values remove more noise, but also more detail.
                            Sane values are between 75 and 125. A custom strength clip can be provided instead.
                            If None, do not apply a strength mask.
                            Default: None.
        :param show_mask:   Whether to show the strength mask. Default: False.
        :param iterations:  The number of iterations to apply the model.
                            This is as simple as applying the model `iterations` times.
                            Default: 1.
        :param planes:      The planes to apply the model to. Default: luma only.
        :param kwargs:      Additional keyword arguments.

        :return:            The processed clip.
        """

        if not self._should_process():
            return clip

        nplanes = normalize_planes(clip, planes)

        if any(x in nplanes for x in [1, 2]):
            warnings.warn('Chroma denoising may be more destructive than expected. Be extra careful!')

        kwargs |= dict(planes=nplanes, iterations=iterations)

        processed = super().apply(clip, **kwargs)

        if self._strength is None:
            return depth(processed, clip)

        self._initialize_strength(clip, strength)

        if show_mask:
            return self._strength

        limited = depth(clip, processed).std.MaskedMerge(processed, self._strength, nplanes)

        return depth(limited, clip)
