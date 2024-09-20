from dataclasses import dataclass
from typing import Any, ClassVar

from vskernels import Hermite, Lanczos
from vsscale import GenericScaler, autoselect_backend
from vstools import (DependencyNotFoundError, FunctionUtil, Matrix,
                     inject_self, vs)

from .base import _get_model_path

__all__: list[str] = [
    "LHzDelowpass",
]


class _BaseLHzDelowpass:
    _model: ClassVar[int]
    _func = "LHzDelowpass"


@dataclass
class BaseLHzDelowpass(_BaseLHzDelowpass, GenericScaler):
    """Light's Horizontal Delowpassing models."""

    backend: Any | None = None
    """
    vs-mlrt backend. Will attempt to autoselect the most suitable one with fp16=True if None.
    In order of trt > cuda > directml > nncn > cpu.
    """

    tiles: int | tuple[int, int] | None = None
    """
    Splits up the frame into multiple tiles.
    Helps if you're lacking in vram but models may behave differently.
    """

    tilesize: int | tuple[int, int] | None = None
    """
    Size of the tiles.
    """

    overlap: int | tuple[int, int] | None = None
    """
    Overlap between tiles.
    """

    _static_kernel_radius = 4

    @inject_self
    def apply(self, clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        """
        Apply the delowpass model to the clip.

        Example usage:

        .. code-block:: python

            # Choosing a model and applying it to a clip.
            >>> LHzDelowpass.DoubleTaps_4_4_15_15.apply(clip)

        :param clip:        The clip to apply the delowpass model to.
        :param kwargs:      Additional keyword arguments.

        :return:            The delowpassed clip.

        :raises DependencyNotFoundError:    If vsmlrt is not installed.
        :raises FileWasNotFoundError:       If the model is not found.
        :raises CustomValueError:           If the model is not a valid delowpass model.
        """

        try:
            from vsmlrt import inference
        except ImportError:
            raise DependencyNotFoundError("vsmlrt", self._func)

        func = FunctionUtil(clip, self.__class__, kwargs.pop('planes', 0), vs.RGB, 32)

        fp16 = kwargs.pop('fp16', func.bitdepth != 32)
        matrix = Matrix.from_param_or_video(kwargs.pop('matrix', None), clip)

        work_clip = Lanczos.resample(func.work_clip, vs.RGBS, matrix_in=matrix)

        model_path = _get_model_path('delowpass', str(self).split('(')[0], fp16)

        if self.backend is None:
            self.backend = autoselect_backend(fp16=fp16)

        delowpassed = inference(work_clip, model_path, self.overlap, self.tilesize, self.backend)
        # TODO: Add horizontal-only masking logic here so we don't affect areas we shouldn't
        delowpassed = self._finish_scale(delowpassed, work_clip, work_clip.width, work_clip.height)

        if clip.format.color_family != vs.RGB:
            delowpassed = Hermite(linear=True).resample(delowpassed, func.work_clip, matrix=matrix)

        return func.return_clip(delowpassed)


class LHzDelowpass(BaseLHzDelowpass):
    """
    Light's Horizontal Delowpassing model.

    These models should only be used on sources that feature horizontal lowpassing
    where you have no clean source to use for delowpassing instead.
    This will typically be R2J anime DVDs with R1s that don't align with it or don't exist.

    DO NOT, UNDER ANY CIRCUMSTANCES, use this model because you're too lazy to delowpass manually!
    Doing it manually is ALWAYS going to be safer and give you much better results!

    The models are named using the following formats:

        - For Single (lowpassed once) models:
            `SingleTaps{taps1}_{blursize1 * 10}`

        - For Double (lowpassed twice) models:
            `DoubleTaps{taps1}_{taps2}_{blursize1 * 10}_{blursize2 * 10}`

    Single lowpass models have negative model numbers,
    and double lowpass models have positive model numbers.

    Each model is trained on different lowpassing values.
    As such, you may need to experiment to find the one that best suits your source.

    Defaults to Double 4-taps (1.5, 1.5).
    """

    _model = 0

    # Double models
    class DoubleTaps_4_4_15_15(BaseLHzDelowpass):
        """
        Lowpass model for R2J DVD horizontal lowpassing.

        Trained on double 4-taps (1.5, 1.5).
        """

        _model = 0
