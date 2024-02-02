from math import ceil
from random import randint
from typing import Any

from vskernels import Kernel, KernelT, Lanczos
from vstools import (CustomTypeError, FieldBased, SPathLike,
                     FuncExceptT, Matrix, MatrixT, SPath,
                     clip_async_render, core, vs)

__all__: list[str] = [
    "export_frames",
    "get_random_frames"
]


def export_frames(
    clip: vs.VideoNode,
    frames: list[int] | int | None = None,
    filename: SPathLike = SPath("bin/%d.png"),
    dur: float = 5.0,
    matrix: MatrixT | None = None,
    kernel: KernelT = Lanczos(3),
    func_except: FuncExceptT | None = None,
    **kwargs: Any
) -> list[SPath]:
    """
    Export random or specific frames from a VideoNode as a PNG image.

    If you want to export the same frames from multiple clips, for example for lq vs. hq training,
    it's recommended you run `get_random_frames` first and pass the results to two different `export_frames` calls.

    Example usage:

    .. code-block:: python

        # Export the same frames from two clips to create a dataset for model training
        >>> frames = get_random_frames(hq_clip)
        >>> ...
        >>> export_frames(hq_clip, frames, "lq/%d.png)
        >>> export_frames(lq_clip, frames, "hq/%d.png)

    This function will use the `vsfpng` plugin if it has been installed.
    You can download it here: `<https://github.com/Mikewando/vsfpng>`_.
    If it can't find it, this function will fall back to `imwri.Write`.

    :param clip:        The clip to process.
    :param frames:      A list of frames to export. If None or an empty list is passed,
                        picks a random frame for every `dur` seconds the clip lasts.
                        Default: None.
    :param filename:    The output filename. The suffix will automatically be changed to `.png`.
                        "%d" will be subsituted with the frame number. The filename will ALWAYS have a frame number!
                        Default: Output in a "bin" directory, The frame number will be appended if necessary.
    :param dur:         The amount of seconds for the random frame ranges. A value of 10 equals 10 seconds.
                        If no frames are passed, it will grab a random frame every `dur` seconds.
                        Default: 5.0 seconds.
    :param matrix:      Matrix of the input clip. If None, will try to get it from the input clip. Default: None.
    :param kernel:      The Kernel used to resample the image to RGB if necessary. Default: Lanczos (3 taps).
    :param func_except: Function returned for custom error handling.
                        This should only be set by VS package developers.
    :param kwargs:      Keyword arguments to pass on to the png writer (vsfpng or imwri).

    :return:            List of SPath objects pointing to every exported image.
    """

    func = func_except or export_frames

    clip = FieldBased.PROGRESSIVE.apply(clip)

    frames = get_random_frames(clip, dur, frames, func)
    proc_clip = core.std.Splice([clip[f] for f in frames])

    matrix = Matrix.from_param_or_video(matrix, proc_clip)
    kernel = Kernel.ensure_obj(kernel, func)

    proc_clip = kernel.resample(proc_clip, vs.RGB24, matrix_in=matrix)

    return _render(proc_clip, filename, func, **kwargs)


def _render(clip: vs.VideoNode, filename: SPathLike, func: FuncExceptT, **kwargs: Any) -> list[SPath]:
    if callable(func):
        func = func.__name__

    if r"%d" not in str(filename):
        sfilename = SPath(filename)
        filename = f"{sfilename.stem}_%d{sfilename.suffix}"

    out_filename = SPath(filename).with_suffix(".png")
    out_filename.parent.mkdir(parents=True, exist_ok=True)

    if hasattr(core, "fpng"):
        clip = clip.fpng.Write(filename=out_filename, **kwargs)
    else:
        clip = clip.imwri.Write(filename=out_filename, **kwargs)

    def _return_framenum(iter: int, _: vs.VideoFrame) -> str:
        # Looks like `format` acts strange with this string. Oh well.
        return SPath(out_filename.to_str().replace(r"%d", str(iter)))

    return clip_async_render(clip, None, f"{func}: Dumping pngs to \"{out_filename.parent}\"...", _return_framenum)


def get_random_frames(
    clip: vs.VideoNode, dur: float = 5.0,
    _frames: list[int] | int | None = None,
    func_except: FuncExceptT | None = None
) -> list[int]:
    """
    Get a list of random frames to grab per range of frames, indicated by `dur`.

    If a list of frames is already passed, this function will perform an early exit.
    This function is primarily useful for other functions that may call this function,
    and should generally not be used by regular users.

    :param clip:        Clip to get the random frames from.
    :param dur:         The amount of seconds for the ranges. A value of 10.0 equals 10 seconds.
                        If no frames are passed, it will grab a random frame every `dur` seconds.
                        Default: 5.0 seconds.
    :param _frames:     An optional list of frames to gather. Acts primarily as an early exit for other functions.
                        If an int or float is passed, it will be turned into a list and truncated if necessary.
                        This parameter should generally be ignored by regular users.
                        Default: None.
    :param func_except: Function returned for custom error handling.
                        This should only be set by VS package developers.

    :return:            A list of random frame numbers.
    """

    func = func_except or get_random_frames

    if _frames is None:
        _frames = list[int]()
    elif isinstance(_frames, (int, float)):
        _frames = [int(_frames)]
    elif not isinstance(_frames, list):
        raise CustomTypeError(f"\"_frames\" must be a list or int, not \"{type(_frames).__name__}\"!", func)

    if _frames:
        return _frames

    start_frame = 0

    while start_frame < clip.num_frames:
        end_frame = min(start_frame + ceil(clip.fps * dur), clip.num_frames)

        _frames.append(randint(start_frame, end_frame - 1))

        start_frame = end_frame

    return _frames
