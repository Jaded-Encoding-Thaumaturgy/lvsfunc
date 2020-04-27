"""
    Miscellaneous functions and wrappers that didn't really have a place in any other submodules.
"""
from functools import partial
from typing import List, Optional, Tuple, Union

import kagefunc as kgf
import mvsfunc as mvf
from vsutil import get_depth, is_image

import vapoursynth as vs

from . import util

core = vs.core


def source(file: str, ref: vs.VideoNode = None,
           force_lsmas: bool = False,
           mpls: bool = False,  mpls_playlist: int = 0, mpls_angle: int = 0) -> vs.VideoNode:
    funcname = "source"
    """
    Generic clip import function.
    Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced.
    It also automatically determines if an image has been imported.
    You can set its fps using 'fpsnum' and 'fpsden', or using a reference clip with 'ref'.

    :param file: str:               OS absolute file location
    :param ref: vs.VideoNode:       Use another clip as reference for the clip's format, resolution, and framerate
    :param force_lsmas: bool:       Force files to be imported with L-SMASH
    :param mpls: bool:              Load in a mpls file
    :param mpls_playlist: int:     Playlist number, which is the number in mpls file name
    :param mpls_angle: int:        Angle number to select in the mpls playlist
    """
    # TODO: Consider adding kwargs for additional options,
    #       find a way to NOT have to rely on a million elif's
    if file.startswith('file:///'):
        file = file[8::]

    # Error handling for some file types
    if file.endswith('.mpls') and mpls is False:
        raise ValueError(f"{funcname}: 'Please set \"mpls = True\" and give a path to the base Blu-ray directory when trying to load in mpls files'")
    if file.endswith('.vob') or file.endswith('.ts'):
        raise ValueError(f"{funcname}: 'Please index VOB and TS files with d2v before importing them'")

    if force_lsmas:
        return core.lsmas.LWLibavSource(file)

    elif mpls:
        mpls = core.mpls.Read(file, mpls_playlist)
        clip = core.std.Splice([core.lsmas.LWLibavSource(mpls['clip'][i]) for i in range(mpls['count'])])

    elif file.endswith('.d2v'):
        clip = core.d2v.Source(file)
    elif file.endswith('.dgi'):
        clip = core.dgdecodenv.DGSource(file)
    elif is_image(file):
        clip = core.imwri.Read(file)
    else:
        if file.endswith('.m2ts'):
            clip = core.lsmas.LWLibavSource(file)
        else:
            clip = core.ffms2.Source(file)

    if ref:
        clip = core.std.AssumeFPS(clip, fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)
        clip = core.resize.Bicubic(clip, width=ref.width, height=ref.height, format=ref.format, matrix_s=mvf.GetMatrix(ref))
        if is_image(file):
            clip = clip*(ref.num_frames-1)
    return clip


def replace_ranges(clip_a: vs.VideoNode,
                   clip_b: vs.VideoNode,
                   ranges: List[Union[int, Tuple[int, int]]]) -> vs.VideoNode:
    funcname = "replace_ranges"
    """
    Written by Louis.
    A replacement for ReplaceFramesSimple that uses ints and tuples rather than a string.
    Frame ranges are inclusive.

    :param clip_a: vs.VideoNode:                        Original clip
    :param clip_b: vs.VideoNode:                        Replacement clip
    :param ranges: List[Union[int, Tuple[int, int]]]:   Ranges to replace clip_a (original clip) with clip_b (replacement clip).
                                                        Integer values in the list indicate single frames,
                                                        Tuple values indicate inclusive ranges.
    """
    out = clip_a
    for r in ranges:
        if type(r) is tuple:
            start, end = r
            if start == 0:
                if end == out.num_frames -1:
                    raise ValueError(f"{funcname}: 'Please don't be stupid'")
                out = clip_b[: end + 1] + out[end + 1 :]
            elif end == out.num_frames - 1:
                out = out[:start] + clip_b[start :]
            else:
                out = out[:start] + clip_b[start : end + 1] + out[end + 1 :]
        else:
            out = out[:r] + clip_b[r] + out[r + 1 :]
    return out


def edgefixer(clip: vs.VideoNode,
              left: Optional[List[int]] = None, right: Optional[List[int]] = None,
              top: Optional[List[int]] = None, bottom: Optional[List[int]] = None,
              radius: Optional[List[int]] = None,
              full_range: bool = False) -> vs.VideoNode:
    """
    A wrapper for ContinuityFixer (https://github.com/MonoS/VS-ContinuityFixer).

    Fixes the issues with over- and undershoot that it may create when fixing the edges,
    and adds what are in my opinion "more sane" ways of handling the parameters and given values.

    ...If possible, you should be using bbmod instead, though.

    :param left: List[int]:        Amount of pixels to fix. Extends to right, top, and bottom
    :param radius: List[int]:      Radius for edgefixing
    :param full_range: bool:       Does not run the expression over the clip to fix over/undershoot
    """

    if left is None:
        left = 0
    if right is None:
        right = left
    if top is None:
        top = left
    if bottom is None:
        bottom = top

    ef = core.edgefixer.ContinuityFixer(clip, left, top, right, bottom, radius)
    return ef if full_range else core.std.Limiter(ef, 16, [235,240])


def fix_cr_tint(clip: vs.VideoNode, value: int = 128) -> vs.VideoNode:
    funcname = "fix_cr_tint"
    """
    Tries to forcibly fix Crunchyroll's green tint by adding pixel values

    :param value: int:  Values added to every pixel
    """
    if get_depth(clip) != 16:
        clip = util.resampler(clip, 16)
    return core.std.Expr(clip, f'x {value} +')


def limit_dark(clip: vs.VideoNode, filtered: vs.VideoNode,
               threshold: float = .25, threshold_range: int = None) -> vs.VideoNode:
    funcname = "limit_dark"
    """
    Replaces frames in a clip with a filtered clip when the frame's darkness exceeds the threshold.
    This way you can run lighter (or heavier) filtering on scenes that are almost entirely dark.

    There is one caveat, however: You can get scenes where every other frame is filtered
    rather than the entire scene. Please do take care to avoid that if possible.

    threshold: float:       Threshold for frame averages to be filtered
    threshold_range: int:   Threshold for a range of frame averages to be filtered
    """
    def _diff(n, f, clip, filtered, threshold, threshold_range):
        if threshold_range:
            return filtered if threshold_range <= f.props.PlaneStatsAverage <= threshold else clip
        else:
            return clip if f.props.PlaneStatsAverage > threshold else filtered

    if threshold_range and threshold_range > threshold:
        raise ValueError(f"{funcname}: '\"threshold_range\" ({threshold_range}) must be a lower value than \"threshold\" ({threshold})'")

    avg = core.std.PlaneStats(clip)
    return core.std.FrameEval(clip, partial(_diff, clip=clip, filtered=filtered, threshold=threshold, threshold_range=threshold_range), avg)


def wipe_row(clip: vs.VideoNode, secondary: vs.VideoNode = None,
             width: int = 1, height: int = 1,
             offset_x: int = 0, offset_y: int = 0,
             width2: Optional[int] = None, height2: Optional[int] = None,
             offset_x2: int = 0, offset_y2: Optional[int] = None,
             show_mask: bool = False) -> vs.VideoNode:
    funcname = "wipe_row"
    """
    Simple function to wipe a row with a blank clip.
    You can also give it a different clip to replace a row with.

    if width2, height2, etc. are given, it will merge the two masks.

    :param secondary: vs.VideoNode:     Appoint a different clip to replace wiped rows with
    """
    secondary = secondary or core.std.BlankClip(clip)

    sqmask = kgf.squaremask(clip, width, height, offset_x, offset_y)
    if width2 and height2:
        sqmask2 = kgf.squaremask(clip, width2, height2, offset_x2, offset_y - 1 if offset_y2 is None else offset_y2)
        sqmask = core.std.Expr([sqmask, sqmask2], "x y +")

    if show_mask:
        return sqmask
    return core.std.MaskedMerge(clip, secondary, sqmask)


# TODO: Write function that only masks px of a certain color/threshold of colors.
#       Think the magic wand tool in various image-editing programs.


# Aliases
src = source
rfs = replace_ranges
