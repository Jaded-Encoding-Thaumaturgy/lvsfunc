from dataclasses import dataclass
from typing import Any

from vstools import PlanesT, depth, fallback, inject_self, vs

from .base import Base1xModel
from .np import ModelNumpyHandling

__all__: list[str] = [
    "LHzDelowpass",
]


@dataclass
class _LHzDelowpass(Base1xModel, ModelNumpyHandling):
    """
    Light's Horizontal Delowpassing model to reconstruct high-frequency information.

    These models should only be used on sources that feature horizontal lowpassing
    where you have no clean source to use for delowpassing instead.
    This will typically be R2J anime DVDs with R1s that don't align with it or don't exist.

    DO NOT, UNDER ANY CIRCUMSTANCES, use this model because you're too lazy to delowpass manually!
    Doing it manually is ALWAYS going to be safer and give you much better results!

    The models are named using the following formats:

        - For Single (lowpassed once) models:
            `SingleTaps{taps}_{blursize * 10}`

        - For Double (lowpassed twice) models:
            `DoubleTaps{taps1}_{taps2}_{blursize1 * 10}_{blursize2 * 10}`

        - If the dataset was compressed with mpeg2:
            `*_mpeg2`

    Each model is trained on different lowpassing values.
    As such, you may need to experiment to find the one that best suits your source.

    Note that some models will also by nature perform mpeg2 compression denoising.
    If this effect is too strong, you should mask the output.
    """

    def __str__(self):
        return 'LHzDelowpass'

    @inject_self
    def apply(
        self,
        clip: vs.VideoNode,
        slice_size: int | None = None,
        planes: PlanesT = None,
        **kwargs: Any
    ) -> vs.VideoNode:
        """
        Apply the model to the clip.

        :param clip:        The clip to process.
        :param slice_size:  The size of the slice to process.
                            This is currently very slow and takes up a ton of memory!
                            Only enable for testing purposes.
                            Default: Disable.
        :param planes:      The planes to apply the model to. Default: all planes.
        :param kwargs:      Additional keyword arguments.

        :return:            The processed clip.
        """

        proc = super().apply(clip, **(dict(planes=planes) | kwargs))

        if slice_size is None or slice_size <= 0:
            # TODO: Once performance issues are solved, use slicing if None. For now, don't.
            return depth(proc, clip)

        import warnings

        warnings.warn('"apply": Slicing is currently very slow and takes up a ton of memory!', UserWarning)

        columns = fallback(slice_size, proc.width // 10)

        clip_np = self._clip_to_numpy(clip)
        proc_np = self._clip_to_numpy(proc)

        for plane in range(clip_np.shape[-1]):
            if plane not in planes:
                continue

            left_columns = proc_np[:, :, :columns, plane]
            right_columns = proc_np[:, :, -columns:, plane]

            self._replace_array_section(clip_np[:, :, :, plane], left_columns, (0, 0, 0))
            self._replace_array_section(clip_np[:, :, :, plane], right_columns, (0, 0, -columns))

        return self._numpy_to_clip(clip_np, proc.format)


@dataclass
class LHzDelowpass(_LHzDelowpass):

    @dataclass
    class DoubleTaps_4_4_15_15(_LHzDelowpass):
        """
        Lowpass model for common R2J DVD horizontal lowpassing.

        Trained on double 4-taps (1.5, 1.5).
        """

        _model_filename = '1x_lanczos_hz_delowpass_4_4_15_15_fp32.onnx'

    @dataclass
    class DoubleTaps_4_4_15_15_mpeg2(_LHzDelowpass):
        """
        Lowpass model for common R2J DVD horizontal lowpassing.

        Trained on double 4-taps (1.5, 1.5) + mpeg2 compression.
        """

        _model_filename = '1x_lanczos_hz_delowpass_4_4_15_15_mpeg2_fp32.onnx'

    @dataclass
    class DoubleTaps_4_4_125_1375_mpeg2(_LHzDelowpass):
        """
        Lowpass model for common R2J DVD horizontal lowpassing.

        Trained on double 4-taps (1.25, 1.375) + mpeg2 compression.
        """

        _model_filename = '1x_lanczos_hz_delowpass_4_4_125_1375_mpeg2_fp32.onnx'
