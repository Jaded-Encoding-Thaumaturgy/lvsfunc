from __future__ import annotations

import colorsys
import io
import json
import random
import re
import shutil
import subprocess as sp
import warnings
from functools import partial
from tempfile import NamedTemporaryFile
from typing import overload, Any

from stgpytools import DependencyNotFoundError, FileWasNotFoundError
from vstools import (CustomIndexError, CustomTypeError, CustomValueError,
                     FrameRangeN, FrameRangesN, FuncExceptT, Keyframes,
                     KwargsT, SPath, SPathLike, check_variable_resolution,
                     core, get_h, get_prop, get_w, vs)

__all__ = [
    'colored_clips',
    'convert_rfs',
    'get_match_centers_scaling',
    'get_packet_sizes',
    'get_packet_scene_stats',
    'get_file_from_path_or_clip',
]


def colored_clips(
    amount: int, max_hue: int = 300, rand: bool = True, seed: Any | None = None, **kwargs: Any
) -> list[vs.VideoNode]:
    """
    Return a list of BlankClips with unique colors in sequential or random order.

    The colors will be evenly spaced by hue in the HSL colorspace.

    Useful maybe for comparison functions or just for getting multiple uniquely colored BlankClips for testing purposes.

    Will always return a pure red clip in the list as this is the RGB equivalent of the lowest HSL hue possible (0).

    Written by `Dave <https://github.com/OrangeChannel>`_.

    :param amount:          Number of VideoNodes to return.
    :param max_hue:         Maximum hue (0 < hue <= 360) in degrees to generate colors from (uses the HSL color model).
                            Setting this higher than ``315`` will result in the clip colors looping back towards red
                            and is not recommended for visually distinct colors.
                            If the `amount` of clips is higher than the `max_hue` expect there to be identical
                            or visually similar colored clips returned (Default: 300)
    :param rand:            Randomizes order of the returned list (Default: True).
    :param seed:            Bytes-like object passed to ``random.seed`` which allows for consistent randomized order.
                            of the resulting clips (Default: None)
    :param kwargs:          Arguments passed to :py:func:`vapoursynth.core.std.BlankClip` (Default: keep=1).

    :return:                List of uniquely colored clips in sequential or random order.

    :raises ValueError:     ``amount`` is less than 2.
    :raises ValueError:     ``max_hue`` is not between 0–360.
    """
    if amount < 2:
        raise CustomIndexError("`amount` must be at least 2!", colored_clips)
    if not (0 < max_hue <= 360):
        raise CustomValueError("`max_hue` must be greater than 0 and less than 360 degrees!", colored_clips)

    blank_clip_args: dict[str, Any] = {'keep': 1, **kwargs}

    hues = [i * max_hue / (amount - 1) for i in range(amount - 1)] + [max_hue]

    hls_color_list = [colorsys.hls_to_rgb(h / 360, 0.5, 1) for h in hues]
    rgb_color_list = [[int(f * 255) for f in color] for color in hls_color_list]

    if rand:
        shuffle = random.shuffle if seed is None else random.Random(seed).shuffle
        shuffle(rgb_color_list)

    return [core.std.BlankClip(color=color, **blank_clip_args) for color in rgb_color_list]


def convert_rfs(rfs_string: str) -> FrameRangesN:
    """
    A utility function to convert `ReplaceFramesSimple`-styled ranges to `replace_ranges`-styled ranges.

    This function accepts the RFS ranges as a string only. This is in line with how RFS handles them.
    The string will be validated before it's passed on. As with all framerange-related functions,
    the more ranges you have, the slower the function will become.

    This function works with both '[x y]' and 'x' styles of frame numbering.
    If no frames could be found, it will simply return an empty list.

    :param rfs_string:      A string representing frame ranges, as you would for ReplaceFramesSimple.

    :return:                A FrameRangesN list containing frame ranges as accepted by `replace_ranges`.
                            If no frames are found, it will simply return an empty list.

    :raises ValueError:     Invalid input string is passed.
    """
    rfs_string = str(rfs_string).strip()

    if not set(rfs_string).issubset('0123456789[] '):
        raise CustomValueError('Invalid characters were found in the input string.', convert_rfs)

    matches = re.findall(r'\[(\s*?\d+\s\d+\s*?)\]|(\d+)', rfs_string)
    ranges = list[FrameRangeN]()

    if not matches:
        return ranges

    for match in [next(y for y in x if y) for x in matches]:
        try:
            ranges += [int(match)]
        except ValueError:
            ranges += [tuple(int(x) for x in str(match).strip().split(' '))]  # type:ignore[list-item]

    return ranges


def get_match_centers_scaling(
    clip: vs.VideoNode,
    target_width: int | None = None,
    target_height: int | None = 720,
    func_except: FuncExceptT | None = None
) -> KwargsT:
    """
    Convenience function to calculate the native resolution for sources that were upsampled
    using the "match centers" model as opposed to the more common "match edges" models.

    While match edges will align the edges of the outermost pixels in the target image,
    match centers will instead align the *centers* of the outermost pixels.

    Here's a visual example for a 3x1 image upsampled to 7x1:

        * Match edges:

    +-------------+-------------+-------------+
    |      ·      |      ·      |      ·      |
    +-------------+-------------+-------------+
    ↓                                         ↓
    +-----+-----+-----+-----+-----+-----+-----+
    |  ·  |  ·  |  ·  |  ·  |  ·  |  ·  |  ·  |
    +-----+-----+-----+-----+-----+-----+-----+

        * Match centers:

    +-----------------+-----------------+-----------------+
    |        ·        |        ·        |        ·        |
    +-----------------+-----------------+-----------------+
             ↓                                   ↓
          +-----+-----+-----+-----+-----+-----+-----+
          |  ·  |  ·  |  ·  |  ·  |  ·  |  ·  |  ·  |
          +-----+-----+-----+-----+-----+-----+-----+

    For a more detailed explanation, refer to this page: `<https://entropymine.com/imageworsener/matching/>`.

    The formula for calculating values we can use during desampling is simple:

    * width: clip.width * (target_width - 1) / (clip.width - 1)
    * height: clip.height * (target_height - 1) / (clip.height - 1)

    Example usage:

    .. code-block:: python

        >>> from vodesfunc import DescaleTarget
        >>> ...
        >>> native_res = get_match_centers_scaling(src, 1280, 720)
        >>> rescaled = DescaleTarget(kernel=Catrom, upscaler=Waifu2x, downscaler=Hermite(linear=True), **native_res)

    The output is meant to be passed to `vodesfunc.DescaleTarget` as keyword arguments,
    but it may also apply to other functions that require similar parameters.

    :param clip:            The clip to base the calculations on.
    :param target_width:    Target width for the descale. This should probably be equal to the base width.
                            If not provided, this value is calculated using the `target_height`.
                            Default: None.
    :param target_height:   Target height for the descale. This should probably be equal to the base height.
                            If not provided, this value is calculated using the `target_width`.
                            Default: 720.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                A dictionary with the keys, {width, height, base_width, base_height},
                            which can be passed directly to `vodesfunc.DescaleTarget` or similar functions.
    """

    func = func_except or get_match_centers_scaling

    if target_width is None and target_height is None:
        raise CustomValueError("Either `target_width` or `target_height` must be a positive integer.", func)

    if target_width is not None and (not isinstance(target_width, int) or target_width <= 0):
        raise CustomValueError("`target_width` must be a positive integer or None.", func)

    if target_height is not None and (not isinstance(target_height, int) or target_height <= 0):
        raise CustomValueError("`target_height` must be a positive integer or None.", func)

    check_variable_resolution(clip, func)

    if target_height is None:
        target_height = get_h(target_width, clip, 1)

    elif target_width is None:
        target_width = get_w(target_height, clip, 1)

    width = clip.width * (target_width - 1) / (clip.width - 1)
    height = clip.height * (target_height - 1) / (clip.height - 1)

    return KwargsT(width=width, height=height, base_width=target_width, base_height=target_height)


@overload
def get_packet_sizes(
    clip: vs.VideoNode,
    filepath: SPathLike | None = None,
    out_file: SPathLike | None = None,
    keyframes: Keyframes | None = None,
    offset: int = 0,
    return_packet_sizes: bool = False,
    func_except: FuncExceptT | None = None
) -> vs.VideoNode:
    ...


@overload
def get_packet_sizes(
    clip: vs.VideoNode,
    filepath: SPathLike | None = None,
    out_file: SPathLike | None = None,
    keyframes: Keyframes | None = None,
    offset: int = 0,
    return_packet_sizes: bool = True,
    func_except: FuncExceptT | None = None
) -> list[int]:
    ...


def get_packet_sizes(
    clip: vs.VideoNode,
    filepath: SPathLike | None = None,
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
    :param filepath:                The path to the original file that was indexed.
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

    func = func_except or get_packet_sizes

    if out_file is not None and SPath(out_file).exists():
        with open(out_file, "r+") as f:
            pkt_sizes = [int(pkt) for pkt in f.readlines()]
    else:
        sfile = get_file_from_path_or_clip(clip, filepath, func)
        pkt_sizes = _get_frames(sfile, func)

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


def get_file_from_path_or_clip(
    clip: vs.VideoNode, file: SPathLike | None, func: FuncExceptT | None = None
) -> SPath:
    func = func or get_file_from_path_or_clip

    if file and not isinstance(file, vs.VideoNode):
        if not (sfile := SPath(file)).exists():
            raise FileWasNotFoundError(f"Could not find the file, \"{sfile}\"!", func)

        return sfile

    try:
        file = get_prop(clip, "idx_filepath", str, func=func)
    except Exception:
        raise CustomTypeError("Could not find the prop, \"idx_filepath\"!", func)

    if not (sfile := SPath(file)).exists():
        raise FileWasNotFoundError(f"Could not find the file, \"{sfile}\"!", func)

    return sfile
