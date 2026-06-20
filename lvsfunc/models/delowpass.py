from .base import _LvsfuncRgbModel

__all__: list[str] = [
    "LHzDelowpass",
]


class LHzDelowpass(_LvsfuncRgbModel):
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

    class DoubleTaps_4_4_15_15(_LvsfuncRgbModel):
        """
        Lowpass model for common R2J DVD horizontal lowpassing.

        Trained on double 4-taps (1.5, 1.5).
        """

        _model = "1x_lanczos_hz_delowpass_4_4_15_15_fp32"

    class DoubleTaps_4_4_15_15_mpeg2(_LvsfuncRgbModel):
        """
        Lowpass model for common R2J DVD horizontal lowpassing.

        Trained on double 4-taps (1.5, 1.5) + mpeg2 compression.
        """

        _model = "1x_lanczos_hz_delowpass_4_4_15_15_mpeg2_fp32"

    class DoubleTaps_4_4_125_1375_mpeg2(_LvsfuncRgbModel):
        """
        Lowpass model for common R2J DVD horizontal lowpassing.

        Trained on double 4-taps (1.25, 1.375) + mpeg2 compression.
        """

        _model = "1x_lanczos_hz_delowpass_4_4_125_1375_mpeg2_fp32"
