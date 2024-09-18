import numpy as np
from vstools import (CustomRuntimeError, FuncExceptT, InvalidVideoFormatError,
                     core, depth, fallback, get_video_format, vs)

__all__: list[str] = [
    'get_format_from_npz',
]


def get_format_from_npz(frame_data: np.ndarray, func_except: FuncExceptT | None = None) -> vs.VideoFormat:
    """
    Guess the format based on heuristics from the numpy array data.

    Input is assumed to be a numpy array with the following structure:

        [
            ('Y', np.ndarray),
            ('U', np.ndarray | None),
            ('V', np.ndarray | None)
        ]

    If every array has the same shape, it's assumed to be YUV 4:4:4.
    If you output RGB data, you may have to convert it back.

    If the U and V arrays are None, it's assumed to be GRAY.

    :param frame_data:      The numpy array data to guess the format from.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                The guessed format.
    """

    func = fallback(func_except, get_format_from_npz)

    y_data, u_data, v_data = frame_data['Y'], frame_data['U'], frame_data['V']

    bit_depth = 32 if y_data.dtype == np.float32 else y_data.itemsize * 8
    sample_type = vs.FLOAT if bit_depth == 32 else vs.INTEGER

    if (u_data is None) != (v_data is None):
        raise CustomRuntimeError('U and V planes must both be present or both be None', func)

    if u_data is None or v_data is None:
        return get_video_format(
            depth(core.std.BlankClip(format=vs.GRAY8, keep=True), bit_depth, sample_type=sample_type)
        )

    y_shape, u_shape, v_shape = y_data.shape, u_data.shape, v_data.shape

    if u_shape != v_shape:
        raise InvalidVideoFormatError('U and V planes must have the same shape', func)

    if y_shape == u_shape:
        subsampling = vs.YUV444P8
    elif u_shape[0] == y_shape[0] and u_shape[1] == y_shape[1] // 2:
        subsampling = vs.YUV422P8
    elif u_shape[0] == y_shape[0] // 2 and u_shape[1] == y_shape[1] // 2:
        subsampling = vs.YUV420P8
    else:
        raise InvalidVideoFormatError(f'Unknown subsampling! {y_shape=}, {u_shape=}, {v_shape=}', func)

    try:
        # TODO: Figure out smarter way to get the exact format directly
        # If only a str overload existed for get_video_format...
        return get_video_format(
            depth(core.std.BlankClip(format=subsampling, keep=True), bit_depth, sample_type=sample_type)
        )
    except AttributeError:
        raise InvalidVideoFormatError(f'Unsupported format: {subsampling=} {sample_type=} {bit_depth=}', func)
