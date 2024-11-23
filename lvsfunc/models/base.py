import importlib.resources as pkg_resources
from dataclasses import dataclass
from typing import Any, Literal, SupportsFloat
from warnings import warn

from vsexprtools import expr_func
from vskernels import Catrom, Point
from vsscale import autoselect_backend
from vstools import (ColorRange, CustomValueError, DependencyNotFoundError,
                     FileWasNotFoundError, FunctionUtil, Matrix, SPath, depth,
                     get_peak_value, inject_self, iterate, join,
                     normalize_planes, split, vs)

__all__: list[str] = []


@dataclass
class Base1xModel:
    """Base class for 1x models to reconstruct high-frequency information."""

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

    _model_filename = ''
    """
    Filename of the model. If it contains a slash, it will be treated as a relative path.

    For example:

    ```python
        >>> class ExampleModel(Base1xModel):
        ...     _model_filename = "./example_model_fp32.onnx"
        ...
        >>> ExampleModel.apply(clip)
    ```
    """

    def __str__(self) -> str:
        return self.__class__.__name__

    @inject_self
    def apply(self, clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        """
        Apply the model to the clip.

        :param clip:        The clip to apply the model to.
        :param kwargs:      Additional keyword arguments.

        :return:            The processed clip.

        :raises DependencyNotFoundError:    If vsmlrt is not installed.
        :raises FileWasNotFoundError:       If the model is not found.
        :raises CustomValueError:           If the model is not a valid model.
        """

        if not self._model_filename:
            raise CustomValueError("Model path not set! You may need to use a subclass!", self)

        self._initialize(clip, kwargs)

        processed = self._apply_model(self._func.work_clip, clip)
        return self._func.return_clip(processed)

    def _initialize(self, clip: vs.VideoNode, kwargs: dict[str, Any] = {}) -> None:
        """Initialize the model with the given kwargs and clip."""

        self._set_kwargs(kwargs)
        self._set_model_path()
        self._set_func(clip)

    def _set_kwargs(self, kwargs: dict[str, Any]) -> None:
        """Set the keyword arguments."""

        self._kwargs = kwargs
        self._fp16 = self._kwargs.pop('fp16', False)

    def _set_func(self, clip: vs.VideoNode) -> None:
        """Set the function util."""

        matrix = self._kwargs.pop('matrix', None)
        bitdepth = 16 if self._fp16 else 32
        color_range = ColorRange.from_param_or_video(self._kwargs.pop('color_range', None), clip)

        self._matrix = Matrix.from_param_or_video(matrix, clip)
        self._planes = normalize_planes(clip, self._kwargs.pop('planes', None))

        # Pre-resample using the same method I use during training.
        proc_clip = self._scale_based_on_planes(clip)

        self._func = FunctionUtil(proc_clip.std.Limiter(), str(self), None, vs.RGB, bitdepth, range_in=color_range)

    def _scale_based_on_planes(self, clip: vs.VideoNode) -> vs.VideoNode:
        """Scale the clip based on the planes."""

        res_kwargs = dict(matrix_in=self._matrix)
        res_kwargs |= dict(format=vs.RGB48 if self._fp16 else vs.RGBS)

        return Point.resample(clip, **res_kwargs)

    def _apply_model(self, proc_clip: vs.VideoNode, ref: vs.VideoNode | None = None) -> vs.VideoNode:
        """Apply the model to the clip."""

        try:
            from vsmlrt import inference
        except ImportError:
            raise DependencyNotFoundError("vsmlrt", self._func.func)

        if self.backend is None:
            self.backend = autoselect_backend(fp16=self._fp16)

        processed = iterate(
            proc_clip, inference, self._kwargs.pop('iterations', 1),
            self._model_path, self.overlap, self.tilesize, self.backend
        )

        if ref is not None and ref.format.color_family != vs.RGB:
            processed = Point(linear=True).resample(processed, ref, matrix=self._matrix)

        processed = self._select_planes(processed, ref)

        return processed

    def _select_planes(self, processed: vs.VideoNode, ref: vs.VideoNode | None = None) -> vs.VideoNode:
        """Select the planes of the clip to return."""

        if ref is None or (self._planes is None or self._planes == [0, 1, 2]):
            return processed

        # TODO: Figure out a smarter way to do this because holy shit this is bad
        if self._planes == [0]:
            return join(processed, ref)

        if self._planes == [1, 2]:
            return join(ref, processed)

        # TODO: Especially this part is ugly holy SHIIITTT
        clip_y, clip_u, clip_v = split(processed)
        ref_y, ref_u, ref_v = split(ref)

        planes_map = {
            (1,): [ref_y, clip_u, ref_v],
            (2,): [ref_y, ref_u, clip_v],
            (0, 1): [clip_y, clip_u, ref_v],
            (0, 2): [clip_y, ref_u, clip_v],
        }

        return join(planes_map.get(tuple(self._planes), processed))

    def _set_model_path(self) -> None:
        """Set the path of the model."""

        if any(x in self._model_filename for x in ['/', '\\']):
            model_path = SPath(self._model_filename)
        else:
            model_path = get_models_path() / str(self).lower() / self._model_filename

        if not model_path.exists():
            raise FileWasNotFoundError(
                "Could not find model file! Please update lvsfunc.", str(self),
                dict(filename=model_path.name, path=model_path.parent)
            )

        self._model_path = model_path

        if not self._fp16:
            return

        new_path = model_path.with_name(model_path.stem.replace('_fp32', '_fp16') + '.onnx')

        if new_path.exists():
            self._model_path = new_path
            return

        warn(f'{self}: Could not find fp16 model! Using fp32 model instead.', stacklevel=2)
        self._fp16 = False


class Base1xModelWithStrength(Base1xModel):
    """Base class for 1x models to reconstruct high-frequency information with strength control."""

    def _initialize_strength(
        self, clip: vs.VideoNode, strength: SupportsFloat | vs.VideoNode = 10.0
    ) -> vs.VideoNode:
        self._strength_clip = strength

        if isinstance(strength, (float, int)):
            self._set_strength_clip(clip, strength)
        elif isinstance(strength, vs.VideoNode):
            self._norm_str_clip(clip)

        return self._strength_clip

    def _set_strength_clip(self, clip: vs.VideoNode, strength: float) -> None:
        norm_strength = strength / 100.0 * get_peak_value(16 if self._fp16 else 32)

        self._strength_clip = expr_func(
            [clip.std.BlankClip(format=vs.GRAYH if self._fp16 else vs.GRAYS, keep=True)],
            f"x {norm_strength} +"
        )

    def _norm_str_clip(self, clip: vs.VideoNode) -> None:
        str_clip = self._strength_clip

        if str_clip.format.color_family != vs.GRAY:
            raise ValueError("Strength clip must be GRAY")

        if str_clip.format.id == vs.GRAY8:
            str_clip = expr_func(str_clip, 'x 255 /', vs.GRAYH if self._fp16 else vs.GRAYS)
        elif self._fp16 and str_clip.format.id != vs.GRAYH:
            str_clip = depth(str_clip, 16, vs.FLOAT)

        if str_clip.width != clip.width or str_clip.height != clip.height:
            str_clip = Catrom.scale(str_clip, clip.width, clip.height)

        if str_clip.num_frames != clip.num_frames:
            raise ValueError("Strength clip must have the same number of frames as the input clip")

        self._strength_clip = str_clip

    def _should_process(self, strength: SupportsFloat | vs.VideoNode | None | Literal[False] = False) -> bool:
        if hasattr(self, '_strength_clip'):
            return self._strength_clip is not False

        return (strength is None) or not (isinstance(strength, (int, float)) and strength <= 0.0)


def get_models_path() -> SPath:
    """Get the path of the models."""

    import lvsfunc

    return SPath(pkg_resources.files(lvsfunc)) / 'models' / 'shaders'
