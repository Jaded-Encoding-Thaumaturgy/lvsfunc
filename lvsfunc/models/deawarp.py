import warnings
from dataclasses import dataclass
from typing import Any

from vstools import PlanesT, depth, inject_self, normalize_planes, vs

from .base import Base1xModel

__all__: list[str] = [
    "LDeawarp",
]


@dataclass
class LDeawarp(Base1xModel):
    """
    Experimental de-awarpsharp model to (attempt to) undo warpsharped sources.
    This model is unlikely to work for anything in particular, but it exists for anyone who may want to try it out.

    Trained by running awarpsharp2 on a variety of sources,
    and comparing the output to the input to correct the warping.
    """

    _model_filename = '1x_deawarp_fp32.onnx'

    @inject_self
    def apply(
        self, clip: vs.VideoNode,
        iterations: int = 1, planes: PlanesT = 0,
        **kwargs: Any
    ) -> vs.VideoNode:
        """
        Apply the model to the clip.

        :param clip:        The clip to process.
        :param iterations:  The number of iterations to apply the model.
                            This is as simple as applying the model `iterations` times.
                            Default: 1.
        :param planes:      The planes to apply the model to. Default: luma only.
        :param kwargs:      Additional keyword arguments.

        :return:            The processed clip.
        """

        warnings.warn(
            'LDeawarp: "This model is highly experimental and '
            'unlikely to work for your source. Use with caution!"'
        )

        nplanes = normalize_planes(clip, planes)

        kwargs |= dict(planes=nplanes, iterations=iterations)

        processed = super().apply(clip, **kwargs)

        return depth(processed, clip)
