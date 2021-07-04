
import os
from typing import Any, Optional

import vapoursynth as vs
from vsutil import is_image

from .misc import get_matrix

core = vs.core

# List of containers that are better off being indexed externally


annoying_formats = ['.iso', '.ts', '.vob']


def source(file: str, ref: Optional[vs.VideoNode] = None,
           force_lsmas: bool = False,
           mpls: bool = False, mpls_playlist: int = 0, mpls_angle: int = 0,
           **index_args: Any) -> vs.VideoNode:
    """
    Generic clip import function.
    Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced.
    It also automatically determines if an image has been imported.
    You can set its fps using 'fpsnum' and 'fpsden', or using a reference clip with 'ref'.

    Alias for this function is `lvsfunc.src`.

    Dependencies:
    * ffms2
    * L-SMASH-Works (optional: m2ts sources or when forcing lsmas)
    * d2vsource (optional: d2v sources)
    * dgdecodenv (optional: dgi sources)
    * VapourSynth-ReadMpls (optional: mpls sources)

    :param file:              Input file
    :param ref:               Use another clip as reference for the clip's format,
                              resolution, and framerate (Default: None)
    :param force_lsmas:       Force files to be imported with L-SMASH (Default: False)
    :param mpls:              Load in a mpls file (Default: False)
    :param mpls_playlist:     Playlist number, which is the number in mpls file name (Default: 0)
    :param mpls_angle:        Angle number to select in the mpls playlist (Default: 0)
    :param kwargs:            Arguments passed to the indexing filter

    :return:                  Vapoursynth clip representing input file
    """

    # TODO: find a way to NOT have to rely on a million elif's
    if file.startswith('file:///'):
        file = file[8::]

    # Error handling for some file types
    if file.endswith('.mpls') and mpls is False:
        raise ValueError("source: 'Set \"mpls = True\" and pass a path to the base Blu-ray directory for this kind of file'")  # noqa: E501
    if os.path.splitext(file)[1].lower() in annoying_formats:
        raise ValueError("source: 'Use an external indexer like d2vwitch or DGIndexNV for this kind of file'")  # noqa: E501

    if force_lsmas:
        clip = core.lsmas.LWLibavSource(file, **index_args)

    elif mpls:
        mpls_in = core.mpls.Read(file, mpls_playlist, mpls_angle)
        clip = core.std.Splice([core.lsmas.LWLibavSource(mpls_in['clip'][i], **index_args)
                                for i in range(mpls_in['count'])])

    elif file.endswith('.d2v'):
        clip = core.d2v.Source(file, **index_args)
    elif file.endswith('.dgi'):
        clip = core.dgdecodenv.DGSource(file, **index_args)
    elif is_image(file):
        clip = core.imwri.Read(file, **index_args)
    else:
        if file.endswith('.m2ts'):
            clip = core.lsmas.LWLibavSource(file, **index_args)
        else:
            clip = core.ffms2.Source(file, **index_args)

    if ref:
        if ref.format is None:
            raise ValueError("source: 'Variable-format clips not supported.'")
        clip = core.std.AssumeFPS(clip, fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)
        clip = core.resize.Bicubic(clip, width=ref.width, height=ref.height,
                                   format=ref.format.id, matrix=get_matrix(ref))
        if is_image(file):
            clip = clip * (ref.num_frames - 1)

    return clip
