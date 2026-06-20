import importlib.resources as pkg_resources
import warnings
from logging import getLogger
from typing import Any

from jetpytools import CustomNotImplementedError, FileNotExistsError, FileWasNotFoundError, FuncExcept, SPath, SPathLike
from vskernels import Catrom, KernelLike, ScalerLike
from vsscale.onnx import BackendLike, BaseOnnxScalerRGB
from vstools import depth, get_y, join, vs

__all__: list[str] = [
    "_LvsfuncRgbModel",
    "_model_variants",
    "_shader_path",
]

logger = getLogger(__name__)


def _model_variants(cls: type) -> tuple[str, ...]:
    variants = []

    for member in cls.__subclasses__():
        if member.__name__ == cls.__name__:
            break

        if not isinstance(member, type) or not issubclass(member, _LvsfuncRgbModel):
            continue

        if "Base" in member.__name__:
            continue

        if member.__name__.startswith("_"):
            continue

        variants.append(member.__name__)

    return sorted(variants)


def _shader_path(subdir: str, filename: str) -> SPath:
    root = SPath(str(pkg_resources.files("lvsfunc"))) / "models" / "shaders"

    return root / subdir / filename


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
            kernel: Base kernel to be used for certain scaling/shifting operations. Defaults to Point.
            scaler: Scaler used for scaling operations. Defaults to kernel.
            shifter: Kernel used for shifting operations. Defaults to kernel.
            **kwargs: Additional arguments.
        """

        self._check_is_base_model()

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

    def apply(self, clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        """
        Apply the model to the clip.

        :param clip:        The clip to process.
        :param kwargs:      Additional keyword arguments.

        :return:            The processed clip.
        """

        warnings.warn(
            f"{self.__class__.__qualname__}.apply() is deprecated; "
            f"use {self.__class__.__qualname__}().scale(depth(clip, 32)) instead.",
            DeprecationWarning,
        )

        return depth(self.scale(clip, **kwargs), clip)

    def _check_is_base_model(self) -> None:
        if hasattr(self, "_model"):
            return

        variants = _model_variants(self.__class__.__base__)

        if variants:
            print(variants)
            example = f"{self.__class__.__name__}.{variants[0]}().scale(depth(clip, 32))"

            hint = (
                f"{self.__class__.__name__} is a namespace, not a model. "
                f"Pick a variant, instantiate it, and call .scale(), e.g. {example}. "
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

            logger.debug("%s: Chroma planes has been scaled accordingly", self)

        return super()._finish_scale(clip, input_clip, width, height, shift, copy_props)


def _get_onnx_model(
    model: _LvsfuncRgbModel,
    *,
    package_name: str = "lvsfunc",
    func_except: FuncExcept | None = None,
) -> SPath:
    func = func_except or _get_onnx_model

    root = SPath(str(pkg_resources.files(package_name))) / "models" / "shaders"

    try:
        return root / model._model_dir / f"{model._model}.onnx"
    except FileNotExistsError:
        raise FileWasNotFoundError(
            f"The model {model.__class__.__name__.lower()} was not found  in the {model._model_dir} directory!", func
        )
