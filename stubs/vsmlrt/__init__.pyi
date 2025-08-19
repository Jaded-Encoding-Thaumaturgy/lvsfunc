import enum
from dataclasses import dataclass
from typing import Literal, SupportsFloat

import vapoursynth as vs

models_path: str

class Backend:
    @dataclass(frozen=False)
    class ORT_CPU:
        num_streams: int = 1
        verbosity: int = 2
        fp16: bool = False

    @dataclass(frozen=False)
    class ORT_CUDA:
        device_id: int = 0
        cudnn_benchmark: bool = True
        num_streams: int = 1
        verbosity: int = 2
        fp16: bool = False

    @dataclass(frozen=False)
    class OV_CPU:
        fp16: bool = False

    @dataclass(frozen=False)
    class TRT:
        max_shapes: tuple[int, int] | None = ...
        opt_shapes: tuple[int, int] | None = ...
        fp16: bool = ...

        device_id: int = ...
        workspace: int = ...
        verbose: bool = ...
        use_cuda_graph: bool = ...
        num_streams: int = ...
        use_cublas: bool = ...
        static_shape: bool = ...
        tf32: bool = ...
        log: bool = ...

        _channels: int = ...

backendT = Backend.OV_CPU | Backend.ORT_CPU | Backend.ORT_CUDA | Backend.TRT

@enum.unique
class DPIRModel(enum.IntEnum):
    drunet_gray: int = ...
    drunet_color: int = ...
    drunet_deblocking_grayscale: int = ...
    drunet_deblocking_color: int = ...

def DPIR(
    clip: vs.VideoNode,
    strength: SupportsFloat | vs.VideoNode | None,
    tiles: int | tuple[int, int] | None = ...,
    tilesize: int | tuple[int, int] | None = ...,
    overlap: int | tuple[int, int] | None = ...,
    model: Literal[0, 1, 2, 3] = ...,
    backend: backendT = ...,
) -> vs.VideoNode: ...
def calc_tilesize(
    tiles: int | tuple[int, int] | None,
    tilesize: int | tuple[int, int] | None,
    width: int,
    height: int,
    multiple: int,
    overlap_w: int,
    overlap_h: int,
) -> tuple[tuple[int, int], tuple[int, int]]: ...
def init_backend(
    backend: backendT, channels: int, trt_max_shapes: tuple[int, int]
) -> backendT: ...
def inference(
    clips: list[vs.VideoNode],
    network_path: str,
    overlap: tuple[int, int],
    tilesize: tuple[int, int],
    backend: backendT,
) -> vs.VideoNode: ...
