from math import log2
from typing import Any

from jetpytools import inject_kwargs_params
from vskernels import (Bilinear, BorderHandling, Center, ComplexScaler,
                       LeftShift, Point, SampleGridModel, Slope, TopShift)
from vstools import Dar, Sar, fallback, inject_self, vs

__all__ = [
    'SharpBilinear'
]


class SharpBilinear(ComplexScaler):
    """
    Pre-supersample using Point, then scale to the target dimensions with Bilinear.

    This is used for pixel art to preserve the "sharpness", while still allowing for
    non-integer ratio scaling without messing up the intended look of the image.
    """

    @inject_self.cached
    @inject_kwargs_params
    def scale(
        self, clip: vs.VideoNode, width: int | None = None, height: int | None = None,
        shift: tuple[TopShift, LeftShift] = (0, 0),
        *,
        border_handling: BorderHandling = BorderHandling.MIRROR,
        sample_grid_model: SampleGridModel = SampleGridModel.MATCH_EDGES,
        sar: Sar | bool | float | None = None, dar: Dar | bool | float | None = None, keep_ar: bool | None = None,
        linear: bool | None = None, sigmoid: bool | tuple[Slope, Center] = False,
        **kwargs: Any
    ) -> vs.VideoNode:
        target_width = int(width or clip.width)
        target_height = int(height or clip.height)

        if (clip.width, clip.height) == (target_width, target_height):
            return clip

        # Ideally, we should always scale in linear light by default.
        kernel_kwargs = dict(
            linear=bool(fallback(linear, self.kwargs.get('linear', True)))
        )

        scale_args: dict[str, Any] = {
            'border_handling': border_handling,
            'sample_grid_model': sample_grid_model,
            'sar': sar, 'dar': dar, 'keep_ar': keep_ar,
            'sigmoid': sigmoid
        }

        if target_width <= clip.width and target_height <= clip.height:
            return Bilinear(**kernel_kwargs).scale(
                clip, target_width, target_height, shift=shift,
                **scale_args
            )

        max_ratio = max(target_width / clip.width, target_height / clip.height)
        int_ratio = 2 ** int(log2(max_ratio) + 0.5)
        ss_width, ss_height = clip.width * int_ratio, clip.height * int_ratio

        ss_clip = Point(**kernel_kwargs).scale(
            clip, ss_width, ss_height, shift,
            **scale_args
        )

        if (ss_clip.width, ss_clip.height) == (target_width, target_height):
            return ss_clip

        return Bilinear(**kernel_kwargs).scale(
            ss_clip, target_width, target_height,
            **scale_args
        )

    @inject_self.cached.property
    def kernel_radius(self) -> int:
        return 1
