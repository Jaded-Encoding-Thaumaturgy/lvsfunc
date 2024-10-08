import numpy as np
from vstools import (FuncExceptT, InvalidVideoFormatError, core, depth,
                     fallback, get_video_format, vs)

from ..exceptions import NumpyArrayLoadError

__all__: list[str] = [
    'get_format_from_npy',
]


def get_format_from_npy(frame_data: np.ndarray, func_except: FuncExceptT | None = None) -> vs.VideoFormat:
    """
    Guess the format based on heuristics from the numpy array data.

    Input is assumed to be a numpy array with the following structure:
    [Y, U, V] where U and V can be None.

    If every array has the same shape, it's assumed to be YUV 4:4:4.
    If you output RGB data, you may have to convert it back.

    If the array has only one plane, it's assumed to be GRAY.

    :param frame_data:      The numpy array data to guess the format from.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                The guessed format.
    """

    func = fallback(func_except, get_format_from_npy)

    if not isinstance(frame_data, np.ndarray):
        raise NumpyArrayLoadError(f"Unsupported data type: {type(frame_data)}", func)

    num_planes = frame_data.shape[0] if frame_data.ndim > 2 else 1
    y_data = frame_data[0] if num_planes > 1 else frame_data

    bit_depth = 32 if y_data.dtype == np.float32 else y_data.itemsize * 8

    if num_planes == 1:
        return get_video_format(depth(core.std.BlankClip(format=vs.GRAY8, keep=True), bit_depth))

    y_shape = y_data.shape
    u_shape = frame_data[1].shape

    subsampling_map = {
        (1, 1): vs.YUV444P8,
        (1, 2): vs.YUV422P8,
        (2, 2): vs.YUV420P8
    }

    y_ratio = (y_shape[0] // u_shape[0], y_shape[1] // u_shape[1])
    subsampling = subsampling_map.get(y_ratio)

    if not subsampling:
        raise InvalidVideoFormatError(f'Unknown subsampling! {y_shape=}, {u_shape=}', func)

    try:
        return get_video_format(depth(core.std.BlankClip(format=subsampling, keep=True), bit_depth))
    except AttributeError:
        raise InvalidVideoFormatError(f'Unsupported format: {subsampling=} {bit_depth=}', func)
