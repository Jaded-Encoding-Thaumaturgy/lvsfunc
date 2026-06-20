from .base import _BaseLvsfuncLuma

__all__: list[str] = [
    "LDempeg2",
]


# TODO: Expand upon this with different models for different bitrates and encoders.
class LDempeg2(_BaseLvsfuncLuma):
    """
    Dempeg2 model to denoise MPEG-2 sources.
    """

    _model = "1x_dempeg2_fp32"
