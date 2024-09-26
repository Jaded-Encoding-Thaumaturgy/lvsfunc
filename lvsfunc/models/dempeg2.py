import warnings
from dataclasses import dataclass
from typing import Any, SupportsFloat

from vstools import PlanesT, depth, inject_self, normalize_planes, vs

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
                            Sane values are between 50-100. A custom strength clip can be provided instead.
                            If None, do not apply a strength mask. Values above 100 are not recommended.
                            Default: None.
        :param show_mask:   Whether to show the strength mask. Default: False.
        :param iterations:  The number of iterations to apply the model.
                            This is as simple as applying the model `iterations` times.
                            Default: 1.
        :param planes:      The planes to apply the model to. Default: luma only.
        :param kwargs:      Additional keyword arguments.

        :return:            The processed clip.
        """

        if not self._should_process(strength):
            return clip

        nplanes = normalize_planes(clip, planes)

        if any(x in nplanes for x in [1, 2]):
            warnings.warn('Chroma denoising may be more destructive than expected. Be extra careful!')

        kwargs |= dict(planes=nplanes, iterations=iterations)

        processed = super().apply(clip, **kwargs)

        if strength is None:
            return depth(processed, clip)

        strength_mask = self._initialize_strength(clip, strength)

        if show_mask:
            return strength_mask

        limited = depth(clip, processed).std.MaskedMerge(processed, strength_mask, nplanes)

        return depth(limited, clip)
