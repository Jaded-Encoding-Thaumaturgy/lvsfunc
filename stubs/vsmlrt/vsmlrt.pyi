import enum
import typing
import vapoursynth as vs

class Backend:
    class ORT_CPU:
        num_streams: int
        verbosity: int
        fp16: bool
    class ORT_CUDA:
        device_id: int
        cudnn_benchmark: bool
        num_streams: int
        verbosity: int
        fp16: bool
    class OV_CPU:
        fp16: bool
    class TRT:
        max_shapes: typing.Optional[typing.Tuple[int, int]]
        opt_shapes: typing.Optional[typing.Tuple[int, int]]
        fp16: bool
        device_id: int
        workspace: int
        verbose: bool
        use_cuda_graph: bool
        num_streams: int
        use_cublas: bool
        static_shape: bool

backendT = typing.Union[
    Backend.OV_CPU,
    Backend.ORT_CPU,
    Backend.ORT_CUDA,
    Backend.TRT
]
class DPIRModel(enum.IntEnum):
    drunet_gray: int
    drunet_color: int
    drunet_deblocking_grayscale: int
    drunet_deblocking_color: int

def DPIR(clip: vs.VideoNode, strength: typing.Optional[typing.Union[typing.SupportsFloat, vs.VideoNode]], tiles: typing.Optional[typing.Union[int, typing.Tuple[int, int]]] = ..., tilesize: typing.Optional[typing.Union[int, typing.Tuple[int, int]]] = ..., overlap: typing.Optional[typing.Union[int, typing.Tuple[int, int]]] = ..., model: typing.Literal[0, 1, 2, 3] = ..., backend: backendT = ...) -> vs.VideoNode: ...
