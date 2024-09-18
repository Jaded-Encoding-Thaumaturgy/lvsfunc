import io
import json
import shutil
import subprocess as sp
import warnings
from functools import partial
from tempfile import NamedTemporaryFile
from typing import overload

from stgpytools import DependencyNotFoundError
from vstools import (CustomValueError, FuncExceptT, Keyframes, SPath,
                     SPathLike, core, fallback, vs)

from ..util import get_file_from_clip

__all__ = [
    'get_packet_sizes',
    'get_packet_scene_stats',
]


@overload
def get_packet_sizes(
    clip: vs.VideoNode,
    src_file: SPathLike | None = None,
    out_file: SPathLike | None = None,
    keyframes: Keyframes | None = None,
    offset: int = 0,
    return_packet_sizes: bool = False,
    func_except: FuncExceptT | None = None
) -> vs.VideoNode:
    ...


@overload
def get_packet_sizes(  # type:ignore[misc]
    clip: vs.VideoNode,
    src_file: SPathLike | None = None,
    out_file: SPathLike | None = None,
    keyframes: Keyframes | None = None,
    offset: int = 0,
    return_packet_sizes: bool = True,
    func_except: FuncExceptT | None = None
) -> list[int]:
    ...


def get_packet_sizes(
    clip: vs.VideoNode,
    src_file: SPathLike | None = None,
    out_file: SPathLike | None = None,
    keyframes: Keyframes | None = None,
    offset: int = 0,
    return_packet_sizes: bool = False,
    func_except: FuncExceptT | None = None
) -> vs.VideoNode | list[int]:
    """
    A simple function to read and add frame packet sizes as frame props.

    "Packet sizes" are the size of individual frames. These can be used to calculate the average bitrate of a clip
    or a scene, and to process certain frames differently depending on how much bitrate is allocated to specific
    sections.

    If `out_file` is set, the results will be written to a file. This file will be read in subsequent calls to save
    time. This is useful when you're working with a large clip and you don't want to call ffprobe every time you
    refresh the preview.

    If a Keyframes object is passed, additional scene-based frame props will be added. These are the min, max, and
    average packet sizes of a scene based on these Keyframes.

    If a non-zero `offset` is set, the function will trim the list of packet sizes to match. Negative values will
    instead set the packet sizes for the first `offset` frames to -1. This is intended to be used with trimmed clips.

    Dependencies:

    * `ffprobe <https://ffmpeg.org/download.html>`_

    :param clip:                    Clip to add the properties to.
    :param src_file:                The path to the original file that was indexed.
                                    If None, tries to read the `idx_filepath` property from `clip`.
                                    Will throw an error if it can't find either.
                                    This parameter is ignored if `out_file` is set and a file can be read.
    :param out_file:                Output file for packet sizes. If set, the results will be written to that file,
                                    and also read from that file in subsequent calls. This saves us from having to
                                    call ffprobe every time you refresh the preview.
    :param keyframes:               A Keyframes object to identify scene changes. If set, scene-based metrics will
                                    be calculated and added as frame props alongside the `pkt_size` frame prop.
    :param offset:                  Offset to trim or duplicate the list of packet sizes. This is useful when you're
                                    working with a trimmed clip. Should be the same value as your trim at the start
                                    of the clip. Negative values will set the packet sizes for the first `offset`
                                    frames to -1 instead.
    :param return_packet_sizes:     If set to True, the function will return the packet sizes as a list of integers.
                                    To get the scene-based stats, you will need to pass this list to the
                                    `get_packet_scene_stats` function along with a Keyframes object.
                                    Default: False.
    :param func_except:             Function returned for custom error handling.
                                    This should only be set by VS package developers.

    :return:                        Input clip with `pkt_size` frame props added, with optionally scene-based packet
                                    stats frame props added on top. if `return_packet_sizes` is set to True, it will
                                    return the packet sizes as a list of integers instead.
    """

    func = fallback(func_except, get_packet_sizes)

    if out_file is not None and SPath(out_file).exists():
        with open(out_file, "r+") as f:
            pkt_sizes = [int(pkt) for pkt in f.readlines()]
    else:
        sfile = get_file_from_clip(clip, src_file, func_except=func)
        pkt_sizes = _get_frames(sfile, func)  # type:ignore[arg-type]

    if out_file is not None and not (sout := SPath(out_file)).exists():
        print(f"Writing packet sizes to \"{sout.absolute()}\"...")

        sout.parent.mkdir(parents=True, exist_ok=True)
        sout.write_text("\n".join([str(pkt) for pkt in pkt_sizes]), "utf-8", newline="\n")

    if offset < 0:
        pkt_sizes = [-1] * -offset + pkt_sizes
    elif offset > 0:
        pkt_sizes = pkt_sizes[offset:]

    if return_packet_sizes:
        return pkt_sizes

    def _set_sizes_props(n: int, clip: vs.VideoNode, pkt_sizes: list[int]) -> vs.VideoNode:
        if (pkt_size := pkt_sizes[n]) < 0:
            warnings.warn(f"{func}: \"Frame {n} bitrate could not be determined!\"")

        return clip.std.SetFrameProps(pkt_size=pkt_size)

    if not keyframes:
        return clip.std.FrameEval(partial(_set_sizes_props, clip=clip, pkt_sizes=pkt_sizes))

    def _set_scene_stats(n: int, clip: vs.VideoNode, stats: list[dict[str, int]]) -> vs.VideoNode:
        if (pkt_size := pkt_sizes[n]) < 0:
            warnings.warn(f"{func}: \"Frame {n} bitrate could not be determined!\"")

        try:
            return clip.std.SetFrameProps(pkt_size=pkt_size, **stats[n])
        except Exception:
            warnings.warn(f"{func}: \"Could not find stats for a section... (Frame: {n})\"")

            return clip.std.SetFrameProps(
                pkt_scene_avg_size=-1,
                pkt_scene_max_size=-1,
                pkt_scene_min_size=-1
            )

    stats = get_packet_scene_stats(keyframes, pkt_sizes)

    return clip.std.FrameEval(partial(_set_scene_stats, clip=clip, stats=stats))


def get_packet_scene_stats(keyframes: Keyframes, packet_sizes: list[int]) -> list[dict[str, float]]:
    """
    Get basic scene-based stats from packet sizes and keyframes.

    :param keyframes:       Keyframes object. This is used to determine where scenes start and end.
    :param packet_sizes:    Individual sizes for every frame.

    :return:                list of dictionaries containing scene-based packet size stats.
    """

    stats = list[dict[str, float]]()

    no_stats_backup = (0.0, 0.0)

    try:
        for start, end in zip(keyframes, keyframes[1:]):
            pkt_scenes = packet_sizes[start:end]

            total_pkt_size = sum(pkt_scenes)

            avg_pkt_size = total_pkt_size / (len(pkt_scenes) or 1)
            max_pkt_size = max(pkt_scenes or no_stats_backup)
            min_pkt_size = min(pkt_scenes or no_stats_backup)

            for _ in pkt_scenes:
                stats += [dict(
                    pkt_scene_avg_size=avg_pkt_size,
                    pkt_scene_max_size=max_pkt_size,
                    pkt_scene_min_size=min_pkt_size
                )]
    except ValueError as e:
        raise CustomValueError("Some kind of error occurred!", get_packet_scene_stats, str(e))

    return stats


def _get_frames(sfile: SPath, func: FuncExceptT) -> list[int]:
    if not shutil.which("ffprobe"):
        raise DependencyNotFoundError(func, "ffprobe", "Could not find {package}! Make sure it's in your PATH!")

    proc = sp.Popen(
        [
            "ffprobe", "-hide_banner", "-show_frames", "-show_streams", "-threads", str(core.num_threads),
            "-loglevel", "quiet", "-print_format", "json", "-select_streams", "v:0",
            sfile
        ],
        stdout=sp.PIPE
    )

    with NamedTemporaryFile("a+", delete=False) as tempfile:
        stempfile = SPath(tempfile.name)

        assert proc.stdout

        for line in io.TextIOWrapper(proc.stdout, "utf-8"):
            tempfile.write(line)

    with open(stempfile) as f:
        data = dict(json.load(f))

    frames = data.get("frames", {})

    if not frames:
        raise CustomValueError(f"No frames found in file, \"{sfile}\"! Your file may be corrupted!", func)

    return [int(dict(frame).get("pkt_size", -1)) for frame in frames]
