
import os
from abc import ABC, abstractmethod
from io import BufferedReader
from itertools import accumulate
from pathlib import Path
from subprocess import run, call, DEVNULL
from typing import Any, Callable, List, Optional, Tuple, Union, cast

import vapoursynth as vs
from pyparsedvd import vts_ifo
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


class DVDIndexer(ABC):
    """Abstract DVD indexer interface."""
    path: Union[Path, str]
    vps_indexer: Callable[..., vs.VideoNode]
    ext: str

    def __init__(self, path: Union[Path, str], vps_indexer: Callable[..., vs.VideoNode], ext: str) -> None:
        self.path = path
        self.vps_indexer = vps_indexer  # type: ignore
        self.ext = ext
        super().__init__()

    @abstractmethod
    def get_cmd(self, files: List[Path], output: Path) -> List[Any]:
        """Returns the indexer command"""
        raise NotImplementedError

    def _check_path(self) -> None:
        try:
            call(self.path, stderr=DEVNULL, stdout=DEVNULL)
        except FileNotFoundError as file_not_found:
            raise FileNotFoundError(f'DVDIndexer: `{self.path}` was not found!') from file_not_found


class D2VWitch(DVDIndexer):
    """Built-in d2vwitch indexer"""
    def __init__(self, path: Union[Path, str] = 'd2vwitch',
                 vps_indexer: Callable[..., vs.VideoNode] = core.d2v.Source, ext: str = '.d2v') -> None:
        super().__init__(path, vps_indexer, ext)

    def get_cmd(self, files: List[Path], output: Path) -> List[Any]:
        self._check_path()
        return [self.path, '--output', output, *files]


class DGIndexNV(DVDIndexer):
    """Built-in DGIndexNV indexer"""
    def __init__(self, path: Union[Path, str] = 'DGIndexNV',
                 vps_indexer: Callable[..., vs.VideoNode] = core.dgdecodenv.DGSource, ext: str = '.dgi') -> None:
        super().__init__(path, vps_indexer, ext)

    def get_cmd(self, files: List[Path], output: Path) -> List[Any]:
        self._check_path()
        return [self.path, '-i', ','.join(map(str, files)), '-o', output, '-h']


def dvd_source(vob_folder: Union[Path, str], idx: DVDIndexer = D2VWitch(), ifo_file: Optional[Union[Path, str]] = None,
               extra: bool = False, **kwargs: Any) -> Tuple[List[vs.VideoNode], List[List[int]]]:
    """Concat .vob DVD files and trim them per titles using the .ifo file as reference.

    :param vob_folder:      Folder with .vob files.
    :param idx:             DVD indexer to be used.
    :param ifo_file:        Optional IFO file path. If not specified, will search 'VTS_01_0.IFO'.
    :param extra:           Adds the splash screen and BD Menu to the return clips.
    :kwargs:                Arguments passed to the indexing filter.
    :return:                Returns a tuple of trimmed clips per title and the chapter frame numbers.
    """
    vob_folder = Path(vob_folder)

    # Index vob files using idx
    vob_files = sorted(vob_folder.glob('*.vob'))

    if not vob_files:
        raise FileNotFoundError('dvd_source: No VOBs found!')

    if not (output := Path(vob_files[0].with_suffix(idx.ext))).exists():
        run(idx.get_cmd(vob_files, output), check=True, text=True, encoding='utf-8')

    all_titles = idx.vps_indexer(str(output), **kwargs)

    # Parse IFO info
    if not ifo_file:
        ifo_file = vob_folder / 'VTS_01_0.IFO'
    with open(ifo_file, 'rb') as file:
        pgci = vts_ifo.load_vts_pgci(cast(BufferedReader, file))

    chapters_frames: List[List[int]] = []
    for prog in pgci.program_chains:
        dvd_fps_s = [pb_time.fps for pb_time in prog.playback_times]
        if all(dvd_fps_s[0] == dvd_fps for dvd_fps in dvd_fps_s):
            fps = vts_ifo.FRAMERATE[dvd_fps_s[0]]
        else:
            raise ValueError('dvd_source: No VFR allowed!')

        raw_fps = 30 if fps.numerator == 30000 else 25

        # Convert in frames
        chapters_frames.append([0] + [
            pb_time.frames
            + (pb_time.hours * 3600 + pb_time.minutes * 60 + pb_time.seconds) * raw_fps
            for pb_time in prog.playback_times]
        )

    chapters_frames = [
        list(accumulate(chapter_frames))
        for chapter_frames in chapters_frames
    ]

    durations = list(accumulate([0] + [frame[-1] for frame in chapters_frames]))

    # Remove splash screen and DVD Menu
    clip = all_titles[-durations[-1]:]

    # Trim per title
    clips = [clip[s:e] for s, e in zip(durations[:-1], durations[1:])]

    if extra:
        clips.insert(0, all_titles[:-durations[-1]])

    return clips, chapters_frames


def trim_clips_per_chapters(clips: List[vs.VideoNode], chapters_frames: List[List[int]]) -> List[List[vs.VideoNode]]:
    """Trim the ouputs of `dvd_source` by chapter.

    :param clips:               List of title clips.
    :param chapters_frames:     Chapter frames.
    :return:                    Returns the titles trimmed by chapter.
    """
    return [[clip[start:end] for start, end in zip(chapter_frames[:-1], chapter_frames[1:])]
            for clip, chapter_frames in zip(clips, chapters_frames)]
