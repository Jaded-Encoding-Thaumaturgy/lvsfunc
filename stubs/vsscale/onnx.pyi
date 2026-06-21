from typing import Any

from jetpytools import SPathLike
from vskernels import KernelLike, Scaler, ScalerLike
from vsscale.mlrt import Backend
from vstools import vs

type BackendLike = type[Backend] | Backend

__all__ = ["Backend", "BackendLike", "BaseOnnxScalerRGB"]

class BaseOnnxScalerRGB:
    scaler: Scaler
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
        kernel: KernelLike = ...,
        scaler: ScalerLike | None = None,
        shifter: KernelLike | None = None,
        **kwargs: Any,
    ) -> None: ...
    def scale(
        self,
        clip: vs.VideoNode,
        width: int | None = None,
        height: int | None = None,
        shift: tuple[float, float] = (0, 0),
        **kwargs: Any,
    ) -> vs.VideoNode: ...
    def preprocess_clip(self, clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode: ...
    def _finish_scale(
        self,
        clip: vs.VideoNode,
        input_clip: vs.VideoNode,
        width: int,
        height: int,
        shift: tuple[float, float] = (0, 0),
        copy_props: bool = False,
    ) -> vs.VideoNode: ...
