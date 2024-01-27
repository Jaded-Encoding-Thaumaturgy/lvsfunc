from datetime import datetime
from math import ceil
from pathlib import Path
from random import randint
from typing import cast

from vskernels import Kernel, KernelT, Lanczos
from vssource import source
from vstools import (CustomTypeError, CustomValueError,
                     DependencyNotFoundError, FieldBased, FuncExceptT, Matrix,
                     MatrixT, SPath, SPathLike, clip_async_render, core, get_y,
                     vs)

__all__: list[str] = [
    "export_png",
    "get_random_frames"
]


def export_png(
    src: SPathLike | list[SPathLike] | vs.VideoNode,
    frames: list[int] = [],
    filename: str = "%d.png",
    dur: float = 5.0,
    luma_only: bool = False,
    matrix: MatrixT | None = None,
    kernel: KernelT = Lanczos(3),
    show_clip: bool = False,
    func_except: FuncExceptT | None = None
) -> list[SPath] | vs.VideoNode:
    """
    Export a VideoNode (either passed as-is or obtained from a (list of) paths) to a PNG image.

    This is mainly useful for collection datasets. If you want a consistent list of random frames,
    for example for lq vs. hq training, it's recommended you run `get_random_frames` first
    and pass those results to two calls of `export_png`.

    :param src:         The clip(s) to process.
                        If a VideoNode is passed, it will be simply use that.
                        If a path or a list of paths is passed, it will index them
                        and create one VideoNode out of them.
    :param frames:      A list of frames to export. If None or an empty list is passed,
                        picks a random frame for every `dur` seconds the clip lasts.
                        Default: empty list.
    :param filename:    The output filename. Must have \"%d\" in it.
                        The string will be formatted. `num` is the frame number.
                        The suffix will automatically be changed to `.png`.
                        Default: %d.png
    :param dur:         The amount of seconds for the random frame ranges. A value of 10 equals 10 seconds.
                        If no frames are passed, it will grab a random frame every `dur` seconds.
                        Default: 5.0 seconds.
    :param luma_only:   Only process the luma of a clip. This may yield better results
                        since the chroma from consumer-grade video is typically very poor quality,
                        and may interfere with certain training methods more than it helps.
                        Default: False.
    :param matrix:      Matrix of the input clip. If None, will try to get it from the clip.
                        Default: None.
    :param kernel:      The Kernel used to resample the image to RGB if necessary.
                        Default: Lanczos (3 taps).
    :param show_clip:   Return the clip early to check if it's a valid clip.
                        This is strictly used for previewing.
                        Default: False.
    :param func_except: Function returned for custom error handling.

    :return:            List of SPath objects pointing to every image exported.
    """

    func = func_except or export_png

    if not hasattr(core, "fpng"):
        raise DependencyNotFoundError(func, "vsfpng `<https://github.com/Mikewando/vsfpng>`_")

    if r"%d" not in filename:
        raise CustomValueError(r"Your filename MUST have \"%d\" in it!", func)

    if isinstance(src, (str, Path, SPath)):
        src = [src]

    if isinstance(src, vs.VideoNode):
        clip = cast(vs.VideoNode, src)
    elif isinstance(src, list):
        clip = core.std.Splice([source(SPath(s), matrix=matrix) for s in src], mismatch=True)

    clip = FieldBased.PROGRESSIVE.apply(clip)

    if show_clip:
        return clip

    frames = get_random_frames(clip, frames, dur, func)
    proc_clip = core.std.Splice([clip[f] for f in frames])

    matrix = Matrix.from_param_or_video(matrix, proc_clip)
    kernel = Kernel.ensure_obj(kernel, func)

    proc_clip = kernel.resample(get_y(proc_clip) if luma_only else proc_clip, vs.RGB24, matrix_in=matrix)

    return _render(proc_clip, filename, func)


def _render(clip: vs.VideoNode, filename: str, func: FuncExceptT) -> list[SPath]:
    if callable(func):
        func = func.__name__

    parent = SPath(f"bin/{datetime.now().strftime('%Y-%m-%d/%H_%M_%S_%f')}"[:-3])
    out_filename = parent / SPath(filename).with_suffix(".png")
    out_filename.parent.mkdir(parents=True, exist_ok=True)

    clip = clip.fpng.Write(filename=out_filename)

    def _return_framenum(iter: int, _: vs.VideoFrame) -> str:
        # Looks like `format` acts strange with this string. Oh well.
        return SPath(out_filename.to_str().replace(r"%d", str(iter)))

    return clip_async_render(clip, None, f"{func}: Dumping pngs to \"{parent}\"...", _return_framenum)


def get_random_frames(
    clip: vs.VideoNode, frames: list[int] | int | float = [],
    dur: float = 5.0, func_except: FuncExceptT | None = None
) -> list[int]:
    """
    Get a list of frames to grab per range of frames, indicated by `dur`.

    If a list of frames is already passed, that will be treated as an early exit.

    :param clip:        Clip to get the random frames from.
    :param frames:      An optional list of frames to gather. Acts primarily as an early exit for other functions.
                        If an int or float is passed, it will be turned into a list and truncated if necessary.
                        Default: empty list.
    :param dur:         The amount of seconds for the ranges. A value of 10.0 equals 10 seconds.
                        If no frames are passed, it will grab a random frame every `dur` seconds.
                        Default: 5.0 seconds.
    :param func_except: Function returned for custom error handling.

    :return:            A list of random frame numbers.
    """

    func = func_except or get_random_frames

    if isinstance(frames, (int, float)):
        frames = [int(frames)]
    elif not isinstance(frames, list):
        raise CustomTypeError(f"\"frames\" must be a \"{type(list)}\", not \"{type(frames)}\"!", func)

    if frames:
        return frames

    start_frame = 0

    while start_frame < clip.num_frames:
        end_frame = min(start_frame + ceil(clip.fps * dur), clip.num_frames)

        frames.append(randint(start_frame, end_frame - 1))

        start_frame = end_frame

    return frames
