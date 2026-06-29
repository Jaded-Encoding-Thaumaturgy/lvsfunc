from __future__ import annotations

import importlib.resources as pkg_resources
import warnings
from logging import getLogger
from typing import Any, cast

from jetpytools import CustomNotImplementedError, FileWasNotFoundError, FuncExcept, SPath, SPathLike
from typing_extensions import deprecated
from vskernels import Catrom, Kernel, KernelLike, ScalerLike
from vsscale.onnx import BackendLike, BaseOnnxScalerRGB
from vstools import core, depth, get_y, join, vs

__all__: list[str] = [
    "_LvsfuncRgbModel",
    "_model_variants",
]

logger = getLogger(__name__)


def _model_variants(cls: type[_LvsfuncRgbModel]) -> tuple[str, ...]:
    return tuple(
        name
        for name, member in cls.__dict__.items()
        if isinstance(member, type)
        and issubclass(member, _LvsfuncRgbModel)
        and "_model" in member.__dict__
        and not name.startswith("_")
        and not name.lower().startswith("base")
    )


class _LvsfuncRgbModel(BaseOnnxScalerRGB):
    """Base class for all RGB models."""

    _static_kernel_radius = 1

    def __init__(
        self,
        model: SPathLike | None = None,
        backend: BackendLike | None = None,
        tiles: int | tuple[int, int] | None = None,
        tilesize: int | tuple[int, int] | None = None,
        overlap: int | tuple[int, int] = 0,
        multiple: int = 1,
        max_instances: int = 2,
        *,
        kernel: KernelLike = Catrom,
        scaler: ScalerLike | None = None,
        shifter: KernelLike | None = None,
        **kwargs: Any,
    ) -> None:
        """
        Initializes the scaler with the specified parameters.

        Args:
            model: Path to the ONNX model file.
            backend: The backend to be used with the vs-mlrt framework. If set to None, the most suitable backend will
                be automatically selected, prioritizing fp16 support.
            tiles: Whether to split the image into multiple tiles. This can help reduce VRAM usage, but note that the
                model's behavior may vary when they are used.
            tilesize: The size of each tile when splitting the image (if tiles are enabled).
            overlap: The size of overlap between tiles.
            multiple: Multiple of the tiles.
            max_instances: Maximum instances to spawn when scaling a variable resolution clip.
            kernel: Base kernel to be used for certain scaling/shifting operations. Defaults to Catrom.
            scaler: Scaler used for scaling operations. Defaults to kernel.
            shifter: Kernel used for shifting operations. Defaults to kernel.
            **kwargs: Additional arguments.
        """

        self._check_is_base_model()

        if model is not None:
            warnings.warn(
                f"{self.__class__.__name__} ships with bundled ONNX weights installed alongside lvsfunc; "
                "the `model` argument is ignored. Instantiate a specific model variant instead, "
                "as with vsscale's ArtCNN or Waifu2x classes.",
                UserWarning,
                stacklevel=2,
            )

        super().__init__(
            _get_onnx_model(self),
            backend,
            tiles,
            tilesize,
            overlap,
            multiple,
            max_instances,
            kernel=kernel,
            scaler=scaler,
            shifter=shifter,
            **kwargs,
        )

    @deprecated(
        "Use .scale(depth(clip, 32)) instead of .apply().",
        category=DeprecationWarning,
        stacklevel=2,
    )
    def apply(self, clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        """
        Apply the model to the clip.

        :param clip:        The clip to process.
        :param kwargs:      Additional keyword arguments.

        :return:            The processed clip.
        """

        clip32 = depth(clip, 32)

        scaled = self.scale(clip32, **kwargs)

        if scaled.format != clip.format:
            return self._resample_to_format(scaled, clip)

        return scaled

    def _resample_to_format(self, clip: vs.VideoNode, ref: vs.VideoNode) -> vs.VideoNode:
        return cast(Kernel, self.scaler).resample(clip, ref.format.id, ref, range=ref)

    def _finish_scale(
        self,
        clip: vs.VideoNode,
        input_clip: vs.VideoNode,
        width: int,
        height: int,
        shift: tuple[float, float] = (0, 0),
        copy_props: bool = False,
    ) -> vs.VideoNode:
        clip = super()._finish_scale(clip, input_clip, width, height, shift, copy_props=False)

        if clip.format != input_clip.format:
            clip = self._resample_to_format(clip, input_clip)

        if copy_props:
            return core.std.CopyFrameProps(clip, input_clip)

        return clip

    def _check_is_base_model(self) -> None:
        if "_model" in self.__class__.__dict__:
            return

        variants = _model_variants(self.__class__)

        if variants:
            example = f"{self.__class__.__name__}.{variants[0]}().scale(depth(clip, 32))"
            variant_list = "\n".join(f"  - {name}" for name in variants)

            hint = (
                f"{self.__class__.__name__} is a namespace, not a model. "
                f"Pick a variant, instantiate it, and call .scale(), e.g. {example}.\n"
                f"Available variants:\n{variant_list}"
            )
        else:
            hint = f"{self.__class__.__name__} has no model variants defined."

        raise CustomNotImplementedError(hint, self.__class__)

    @property
    def _model_dir(self) -> str:
        return self.__class__.__qualname__.split(".")[0].lower()


class _BaseLvsfuncLuma(_LvsfuncRgbModel):
    def preprocess_clip(self, clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        return super().preprocess_clip(get_y(clip), **kwargs)

    def _finish_scale(
        self,
        clip: vs.VideoNode,
        input_clip: vs.VideoNode,
        width: int,
        height: int,
        shift: tuple[float, float] = (0, 0),
        copy_props: bool = False,
    ) -> vs.VideoNode:
        if input_clip.format.color_family == vs.YUV:
            scaled_chroma = self.scaler.scale(input_clip, clip.width, clip.height)
            clip = join(clip, scaled_chroma, prop_src=scaled_chroma)

            logger.debug("%s: Chroma planes have been scaled accordingly", self)

        return super()._finish_scale(clip, input_clip, width, height, shift, copy_props)


def _get_onnx_model(
    model: _LvsfuncRgbModel,
    *,
    package_name: str = "lvsfunc",
    func_except: FuncExcept | None = None,
) -> SPath:
    model_cls = type(model)
    func = func_except or f"{model_cls.__name__}._get_onnx_model"

    if (model_name := model_cls.__dict__.get("_model")) is None:
        raise FileWasNotFoundError(
            f"The model {model_cls.__name__} does not define a _model filename.",
            func,
        )

    root = SPath(str(pkg_resources.files(package_name))) / "models" / "shaders"
    path = root / model._model_dir / f"{model_name}.onnx"

    if not path.exists() or not path.is_file():
        raise FileWasNotFoundError(
            f"The model {model_name}.onnx was not found in the {root / model._model_dir} directory! "
            "You may need to reinstall this package or install the missing model.",
            func,
        )

    return path
