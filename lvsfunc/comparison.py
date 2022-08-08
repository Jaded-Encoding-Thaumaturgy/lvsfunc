from __future__ import annotations

import math
import random
import warnings
from abc import ABC, abstractmethod
from itertools import groupby, zip_longest
from typing import Any, Callable, Iterable, Iterator, Literal, Sequence, TypeVar, overload

import vapoursynth as vs
from vskernels import Catrom, get_matrix, get_prop
from vsutil import depth, get_subsampling, get_w
from vsutil import split as split_planes

from .dehardsub import hardsub_mask
from .exceptions import ClipsAndNamedClipsError, InvalidFormatError, NotEqualFormatsError, VariableFormatError
from .render import clip_async_render
from .types import Direction
from .util import check_variable, check_variable_format, check_variable_resolution

core = vs.core

__all__ = [
    'compare', 'comp',
    'Comparer',
    'diff_hardsub_mask',
    'diff',
    'Interleave',
    'interleave',
    'Split',
    'split',
    'stack_compare', 'scomp',
    'stack_horizontal',
    'stack_planes',
    'stack_vertical',
    'Stack',
    'Tile',
    'tile',
]

T = TypeVar('T')


class Comparer(ABC):
    """
    Base class for comparison functions.

    :param clips:               A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                                If given a dict, the names will be overlaid on the clips
                                using :py:func:`vapoursynth.core.text.Text`.
                                If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                                and the clips will not be labeled.
                                The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param label_alignment:     An integer from 1-9, corresponding to the positions of the keys on a numpad.
                                Only used if `clips` is a dict.
                                Determines where to place clip name using :py:func:`vapoursynth.core.text.Text`
                                (Default: 7).

    :raises ValueError:         Less than two clips passed.
    :raises ValueError:         `label_alignment` is not between 1–9.
    :raises ValueError:         Unexpected type passed to `clips`.
    """

    def __init__(self,
                 clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
                 /,
                 *,
                 label_alignment: int = 7
                 ) -> None:
        if len(clips) < 2:
            raise ValueError("Comparer: Compare functions must be used on at least 2 clips!")
        if label_alignment not in list(range(1, 10)):
            raise ValueError("Comparer: `label_alignment` must be an integer from 1 to 9!")
        if not isinstance(clips, (dict, Sequence)):
            raise TypeError(f"Comparer: Unexpected type {type(clips)} for `clips` argument!")

        self.clips = list(clips.values()) if isinstance(clips, dict) else list(clips)
        self.names = list(clips.keys()) if isinstance(clips, dict) else None

        self.label_alignment = label_alignment

        self.num_clips = len(clips)

        widths = {clip.width for clip in self.clips}
        self.width = w if (w := widths.pop()) != 0 and len(widths) == 0 else None

        heights = {clip.height for clip in self.clips}
        self.height = h if (h := heights.pop()) != 0 and len(heights) == 0 else None

        formats = {getattr(clip.format, 'name', None) for clip in self.clips}
        self.format = formats.pop() if len(formats) == 1 else None

    def _marked_clips(self) -> list[vs.VideoNode]:
        """If a `name` is only space characters, `'   '`, for example, the name will not be overlaid on the clip."""
        if self.names:
            return [clip.text.Text(text=name, alignment=self.label_alignment) if name.strip() else clip
                    for clip, name in zip(self.clips, self.names)]
        else:
            return self.clips.copy()

    @abstractmethod
    def _compare(self) -> vs.VideoNode:
        raise NotImplementedError

    @property
    def clip(self) -> vs.VideoNode:
        """
        Return the comparison as a single VideoNode for further manipulation or attribute inspection.

        ``comp_clip = Comparer(...).clip`` is the intended use in encoding scripts.
        """
        return self._compare()


class Stack(Comparer):
    """
    Stacks clips horizontally or vertically.

    Acts as a convenience combination function of :py:func:`vapoursynth.core.text.Text`
    and either :py:func:`vapoursynth.core.std.StackHorizontal` or :py:func:`vapoursynth.core.std.StackVertical`.

    :param clips:               A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                                If given a dict, the names will be overlaid on the clips using
                                :py:func:`vapoursynth.core.text.Text`.
                                If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                                and the clips will not be labeled.
                                The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param direction:           Direction of the stack (Default: :py:attr:`lvsfunc.comparison.Direction.HORIZONTAL`).
    :param label_alignment:     An integer from 1-9, corresponding to the positions of the keys on a numpad.
                                Only used if `clips` is a dict.
                                Determines where to place clip name using :py:func:`vapoursynth.core.text.Text`
                                (Default: 7).

    :raises ValueError:         Clips are not the same height for StackHorizontal.
    :raises ValueError:         Clips are not the same width for StackVertical.
    """

    def __init__(self,
                 clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
                 /,
                 *,
                 direction: Direction = Direction.HORIZONTAL,
                 label_alignment: int = 7
                 ) -> None:
        self.direction = direction
        super().__init__(clips, label_alignment=label_alignment)

    def _compare(self) -> vs.VideoNode:
        if self.direction == Direction.HORIZONTAL:
            if not self.height:
                raise ValueError("Stack: StackHorizontal requires that all clips be the same height!")
            return core.std.StackHorizontal(self._marked_clips())

        if not self.width:
            raise ValueError("Stack: StackVertical requires that all clips be the same width!")
        return core.std.StackVertical(self._marked_clips())


class Interleave(Comparer):
    """
    Returns a clip with the frames from all clips interleaved.

    For example, Interleave(A=clip1, B=clip2) will return A.Frame 0, B.Frame 0, A.Frame 1, B.Frame 1, ...

    Acts as a convenience combination function of :py:func:`vapoursynth.core.text.Text`
    and :py:func:`vapoursynth.core.std.Interleave`.

    :param clips:               A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                                If given a dict, the names will be overlaid on the clips using
                                :py:func:`vapoursynth.core.text.Text`.
                                If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                                and the clips will not be labeled.
                                The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param label_alignment:     An integer from 1-9, corresponding to the positions of the keys on a numpad.
                                Only used if `clips` is a dict.
                                Determines where to place clip name using :py:func:`vapoursynth.core.text.Text`
                                (Default: 7).
    """

    def __init__(self,
                 clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
                 /,
                 *,
                 label_alignment: int = 7
                 ) -> None:
        super().__init__(clips, label_alignment=label_alignment)

    def _compare(self) -> vs.VideoNode:
        return core.std.Interleave(self._marked_clips(), extend=True, mismatch=True)


class Tile(Comparer):
    """
    Tiles clips in a mosaic manner, filling rows first left-to-right, then stacking.

    The arrangement of the clips can be specified with the `arrangement` parameter.
    Rows are specified as lists of ints inside of a larger list specifying the order of the rows.
    Think of this as a 2-dimensional array of 0s and 1s with `0` representing an empty slot and `1` representing the
    next clip in the sequence.

    If `arrangement` is not specified, the function will attempt to fill a square with dimensions `n x n`
    where `n` is equivalent to ``math.ceil(math.sqrt(len(clips))``. The bottom rows will be dropped if empty. ::

        # For example, for 3 clips, the automatic arrangement becomes:
        [
         [1, 1],
         [1, 0]
        ]

        # For 10 clips, the automatic arrangement becomes:
        [
         [1, 1, 1, 1],
         [1, 1, 1, 1],
         [1, 1, 0, 0]
        ]

        # For custom arrangements, such as (for 4 clips):
        [
         [0, 1, 0, 1],
         [1],
         [0, 1]
        ]
        # the rows will be auto-padded with 0's to be the same length.

    :param clips:               A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                                If given a dict, the names will be overlaid on the clips using
                                :py:func:`vapoursynth.core.text.Text`.
                                If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                                and the clips will not be labeled.
                                The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param arrangement:         2-dimension array (list of lists) of 0s and 1s
                                representing a list of rows of clips(`1`) or blank spaces(`0`) (Default: ``None``)
    :param label_alignment:     An integer from 1-9, corresponding to the positions of the keys on a numpad.
                                Only used if `clips` is a dict.
                                Determines where to place clip name using :py:func:`vapoursynth.core.text.Text`
                                (Default: 7).

    :raises ValueError:         Clip heights and widths don't match.
    :raises ValueError:         Array is one-dimensional and you should be using
                                :py:class:`lvsfunc.comparison.Stack` instead.
    :raises ValueError:         Specified arrangement has an invalid number of clips.
    """

    def __init__(self,
                 clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
                 /,
                 *,
                 arrangement: list[list[int]] | None = None,
                 label_alignment: int = 7
                 ) -> None:
        super().__init__(clips, label_alignment=label_alignment)

        if not self.width or not self.height:
            raise ValueError("Tile: All clip widths and heights must be the same!")

        if arrangement is None:
            self.arrangement = self._auto_arrangement()
        else:
            is_one_dim = len(arrangement) < 2 or all(len(row) == 1 for row in arrangement)
            if is_one_dim:
                raise ValueError("Tile: Use Stack instead if the array is one dimensional!")
            self.arrangement = arrangement

        self.blank_clip = core.std.BlankClip(clip=self.clips[0], keep=1)

        max_length = max(map(len, self.arrangement))
        self.arrangement = [row + [0] * (max_length - len(row)) for row in self.arrangement]

        array_count = sum(map(sum, self.arrangement))  # type:ignore[arg-type]

        if array_count != self.num_clips:
            raise ValueError('Tile: Specified arrangement has an invalid number of clips!')

    def _compare(self) -> vs.VideoNode:
        clips = self._marked_clips()
        rows = [core.std.StackHorizontal([clips.pop(0) if elem else self.blank_clip for elem in row])
                for row in self.arrangement]
        return core.std.StackVertical(rows)

    def _auto_arrangement(self) -> list[list[int]]:
        def _grouper(iterable: Iterable[T], n: int, fillvalue: T | None = None) -> Iterator[tuple[T, ...]]:
            args = [iter(iterable)] * n
            return zip_longest(*args, fillvalue=fillvalue)

        dimension = 1 + math.isqrt(self.num_clips - 1)
        return [list(x) for x in _grouper([1] * self.num_clips, dimension, 0)]


class Split(Stack):
    """
    Split an unlimited amount of clips into one VideoNode with the same dimensions as the original clips.

    Handles odd-sized resolutions or resolutions that can't be evenly split by the amount of clips specified.

    The remaining pixel width/height (``clip.dimension % number_of_clips``)
    will be always given to the last clip specified.
    For example, five `104 x 200` clips will result in a `((20 x 200) * 4) + (24 x 200)` horizontal stack of clips.

    :param clips:               A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                                If given a dict, the names will be overlaid on the clips using
                                :py:func:`vapoursynth.core.text.Text`.
                                If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                                and the clips will not be labeled.
                                The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param direction:           Determines the axis to split the clips on.
                                (Default: :py:attr:`lvsfunc.comparison.Direction.HORIZONTAL`)
    :param label_alignment:     An integer from 1-9, corresponding to the positions of the keys on a numpad.
                                Only used if `clips` is a dict.
                                Determines where to place clip name using :py:func:`vapoursynth.core.text.Text`
                                (Default: 7).

    :raises ValueError:         Clip heights and widths don't match.
    :raises ValueError:         Resulting cropped width or height violates subsampling rules.
    """

    def __init__(self,
                 clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
                 /,
                 *,
                 direction: Direction = Direction.HORIZONTAL,
                 label_alignment: int = 7
                 ) -> None:
        super().__init__(clips, direction=direction, label_alignment=label_alignment)
        self._smart_crop()

    def _smart_crop(self) -> None:  # has to alter self.clips to send clips to _marked_clips() in Stack's _compare()
        """Crops self.clips in place accounting for odd resolutions."""
        if not self.width or not self.height:
            raise ValueError("Split: All clips must have same width and height!")

        breaks_subsampling = ((self.direction == Direction.HORIZONTAL and (((self.width // self.num_clips) % 2)
                                                                           or ((self.width % self.num_clips) % 2)))
                              or (self.direction == Direction.VERTICAL and (((self.height // self.num_clips) % 2)
                                                                            or ((self.height % self.num_clips) % 2))))

        is_subsampled = not all(get_subsampling(clip) in ('444', None) for clip in self.clips)

        if breaks_subsampling and is_subsampled:
            raise ValueError("Split: Resulting cropped width or height violates subsampling rules! "
                             "Consider resampling to YUV444 or RGB before attempting to crop!")

        match self.direction:
            case Direction.HORIZONTAL:
                crop_width, overflow = divmod(self.width, self.num_clips)

                for key, clip in enumerate(self.clips):
                    left_crop = crop_width * key
                    right_crop = crop_width * (self.num_clips - 1 - key)

                    if key != (self.num_clips - 1):
                        right_crop += overflow

                    self.clips[key] = clip.std.Crop(left=left_crop, right=right_crop)
            case Direction.VERTICAL:
                crop_height, overflow = divmod(self.height, self.num_clips)

                for key, clip in enumerate(self.clips):
                    top_crop = crop_height * key
                    bottom_crop = crop_height * (self.num_clips - 1 - key)

                    if key != (self.num_clips - 1):
                        bottom_crop += overflow

                    self.clips[key] = clip.std.Crop(top=top_crop, bottom=bottom_crop)


def compare(clip_a: vs.VideoNode, clip_b: vs.VideoNode,
            frames: list[int] | None = None,
            rand_total: int | None = None,
            force_resample: bool = True, print_frame: bool = True,
            mismatch: bool = False) -> vs.VideoNode:
    """
    Compare the same frames from two different clips by interleaving them into a single clip.

    Clips are automatically resampled to 8 bit YUV -> RGB24 to emulate how a monitor shows the frame.
    This can be disabled by setting `force_resample` to ``False``.

    This is not recommended over setting multiple outputs and checking between those,
    but in the event that is unavailable to you, this function may be useful.

    Alias for this function is ``lvsfunc.comp``.

    :param clip_a:          Clip to compare.
    :param clip_b:          Second clip to compare.
    :param frames:          List of frames to compare (Default: ``None``).
    :param rand_total:      Number of random frames to pick (Default: ``None``).
    :param force_resample:  Forcibly resamples the clip to RGB24 (Default: ``True``).
    :param print_frame:     Print frame numbers (Default: ``True``).
    :param mismatch:        Allow for clips with different formats and dimensions to be compared (Default: ``False``).

    :return:                Interleaved clip containing specified frames from `clip_a` and `clip_b`.

    :raises ValueError:     More comparisons requested than frames available.
    :raises NotEqualFormatsError:
                            Format of given clips don't match.
    """
    def _resample(clip: vs.VideoNode) -> vs.VideoNode:
        # Resampling to 8 bit and RGB to properly display how it appears on your screen
        return core.resize.Bicubic(clip, format=vs.RGB24, matrix_in=get_matrix(clip),
                                   dither_type='error_diffusion')

    check_variable_resolution(clip_a, "compare")
    check_variable_resolution(clip_b, "compare")

    # Error handling
    if frames and len(frames) > clip_a.num_frames:
        raise ValueError("compare: 'More comparisons requested than frames available!'")

    if force_resample:
        clip_a, clip_b = _resample(clip_a), _resample(clip_b)
    elif mismatch is False:
        assert check_variable_format(clip_a, "compare")
        assert check_variable_format(clip_b, "compare")

        if clip_a.format.id != clip_b.format.id:
            raise NotEqualFormatsError("compare")

    if print_frame:
        clip_a = clip_a.text.Text("Clip A").text.FrameNum(alignment=9)
        clip_b = clip_b.text.Text("Clip B").text.FrameNum(alignment=9)

    if frames is None:
        if not rand_total:
            # More comparisons for shorter clips so you can compare stuff like NCs more conveniently
            rand_total = int(clip_a.num_frames / 1000) if clip_a.num_frames > 5000 else int(clip_a.num_frames / 100)
        frames = sorted(random.sample(range(1, clip_a.num_frames - 1), rand_total))

    frames_a = core.std.Splice([clip_a[f] for f in frames]).std.AssumeFPS(fpsnum=1, fpsden=1)
    frames_b = core.std.Splice([clip_b[f] for f in frames]).std.AssumeFPS(fpsnum=1, fpsden=1)
    return core.std.Interleave([frames_a, frames_b], mismatch=mismatch)


def stack_compare(*clips: vs.VideoNode,
                  height: int | None = None) -> vs.VideoNode:
    """
    Compare two clips by stacking them.

    Best to use when trying to match two sources frame-accurately.
    Alias for this function is ``lvsfunc.scomp``.


    :param clips:           Clips to compare.
    :param height:          Height in px to rescale clips to.
                            (MakeDiff clip will be twice this resolution).
                            This function will not scale above the first clip's height (Default: 288).

    :return:                Clip with `clips` stacked.

    :raises ValueError:     More or less than 2 clips are given.
    """
    if len(clips) != 2:
        raise ValueError(f"stack_compare: You must pass at least two clips, not {len(clips)}.")

    clipa, clipb = clips

    if not height:
        height = 288
    elif height > clipa.height / 2:
        warnings.warn(f"stack_compare: 'Given 'height' ({height}) is bigger than clipa's height {clipa.height}!' "
                      "Will be using clipa's height instead.")
        height = int(clipa.height / 2)

    scaled_width = get_w(height, only_even=False)

    diff = core.std.MakeDiff(clipa=clipa, clipb=clipb)
    diff = Catrom().scale(diff, scaled_width * 2, height * 2).text.FrameNum(8)
    resized = [Catrom().scale(clipa, scaled_width, height).text.Text('Clip A', 3),
               Catrom().scale(clipb, scaled_width, height).text.Text('Clip B', 1)]

    return Stack([Stack(resized).clip, diff], direction=Direction.VERTICAL).clip


def stack_planes(clip: vs.VideoNode, /, stack_vertical: bool = False) -> vs.VideoNode:
    """
    Stacks the planes of a clip.

    For 4:2:0 subsampled clips, the two half-sized planes will be stacked in the opposite direction specified
    (vertical by default),
    then stacked with the full-sized plane in the direction specified (horizontal by default).

    :param clip:                    Clip to process (must be in YUV or RGB planar format).
    :param stack_vertical:          Stack the planes vertically (Default: ``False``).

    :return:                        Clip with stacked planes.

    :raises InvalidFormatError:     Clip is not YUV or RGB.
    :raises TypeError:              Clip is of an unexpected color family.
    :raises TypeError:              Clip returns an unexpected subsampling.
    """
    assert check_variable(clip, "stack_planes")

    if clip.format.num_planes != 3:
        raise InvalidFormatError("stack_planes", "{func}: Input clip must be of a YUV or RGB planar format!")

    yuv_planes = split_planes(clip)

    if clip.format.color_family == vs.ColorFamily.YUV:
        planes: dict[str, vs.VideoNode] = {'Y': yuv_planes[0], 'U': yuv_planes[1], 'V': yuv_planes[2]}
    elif clip.format.color_family == vs.ColorFamily.RGB:
        planes = {'R': yuv_planes[0], 'G': yuv_planes[1], 'B': yuv_planes[2]}
    else:
        raise TypeError(f"stack_planes: Unexpected color family: {clip.format.color_family.name}!")

    direction: Direction = Direction.HORIZONTAL if not stack_vertical else Direction.VERTICAL

    if get_subsampling(clip) in ('444', None):
        return Stack(planes, direction=direction).clip
    elif get_subsampling(clip) == '420':
        subsample_direction: Direction = Direction.HORIZONTAL if stack_vertical else Direction.VERTICAL
        y_plane = planes.pop('Y').text.Text(text='Y')
        subsampled_planes = Stack(planes, direction=subsample_direction).clip

        return Stack([y_plane, subsampled_planes], direction=direction).clip
    else:
        raise TypeError(f"stack_planes: Unexpected subsampling {get_subsampling(clip)}!")


def diff_hardsub_mask(a: vs.VideoNode, b: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
    """
    Diff func for :py:func:`lvsfunc.comparison.diff` to use a hardsub mask.

    This is kinda slow.

    :param a:   Clip A.
    :param b:   Clip B.

    :return:    Diff masked with :py:func:`lvsfunc.dehardsub.hardsub_mask`.
    """
    assert check_variable(a, "diff_hardsub_mask")
    assert check_variable(b, "diff_hardsub_mask")

    return core.std.MaskedMerge(core.std.MakeDiff(a, a), core.std.MakeDiff(a, b), hardsub_mask(a, b, **kwargs))


@overload
def diff(*clips: vs.VideoNode,
         thr: float = ...,
         height: int = ...,
         interleave: bool = ...,
         return_ranges: Literal[True] = True,
         exclusion_ranges: Sequence[int | tuple[int, int]] | None = ...,
         diff_func: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] = ...,
         **namedclips: vs.VideoNode) -> tuple[vs.VideoNode, list[tuple[int, int]]]:
    ...


@overload
def diff(*clips: vs.VideoNode,
         thr: float = ...,
         height: int = ...,
         interleave: bool = ...,
         return_ranges: Literal[False],
         exclusion_ranges: Sequence[int | tuple[int, int]] | None = ...,
         diff_func: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] = ...,
         **namedclips: vs.VideoNode) -> vs.VideoNode:
    ...


def diff(*clips: vs.VideoNode,
         thr: float = 96,
         height: int = 288,
         interleave: bool = False,
         return_ranges: bool = False,
         exclusion_ranges: Sequence[int | tuple[int, int]] | None = None,
         diff_func: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] = lambda a, b: core.std.MakeDiff(a, b),
         **namedclips: vs.VideoNode) -> vs.VideoNode | tuple[vs.VideoNode, list[tuple[int, int]]]:
    """
    Create a standard :py:class:`lvsfunc.comparison.Stack` between frames from two clips that have differences.

    Useful for making comparisons between TV and BD encodes, as well as clean and hardsubbed sources.

    There are two methods used here to find differences:
    If `thr` is below 1, PlaneStatsDiff is used to figure out the differences.
    Else, if `thr` is equal than or higher than 1, PlaneStatsMin/Max are used.

    Recommended is PlaneStatsMin/Max, as those seem to catch more outrageous differences
    without returning too many starved frames.

    Note that this might catch artifacting as differences!
    Make sure you verify every frame with your own eyes!

    Alias for this function is ``lvsfunc.diff``.

    :param clips:               Clips for comparison (order is kept).
    :param namedclips:          Keyword arguments of `name=clip` for all clips in the comparison.
                                Clips will be labeled at the top left with their `name`.
    :param thr:                 Threshold, <= 1 uses PlaneStatsDiff, > 1 uses Max/Min.
                                Higher values will catch more differences.
                                Value must be lower than 128
    :param height:              Height in px to downscale clips to if `interleave` is ``False``.
                                (MakeDiff clip will be twice this resolution)
    :param interleave:          Return clip as an interleaved comparison.
                                (using :py:class:`lvsfunc.comparison.Interleave`).
                                This will not return a diff clip
    :param return_ranges:       Return a list of ranges in addition to the comparison clip.
    :param exclusion_ranges:    Excludes a list of frame ranges from difference checking output (but not processing).
    :param diff_func:           Function for calculating diff in PlaneStatsMin/Max mode.

    :return:                    Either an interleaved clip of the differences between the two clips
                                or a stack of both input clips on top of MakeDiff clip.
                                Furthermore, the function will print the ranges of all the diffs found.

    :raises ClipsAndNamedClipsError:
                                Both positional and named clips are given.
    :raises ValueError:         More or less than two clips are given.
    :raises ValueError:         ``thr`` is 128 or higher.
    :raises VariableFormatError:
                                One of the clips is of a variable format.
    :raises StopIteration:      No differences are found.
    """
    if clips and namedclips:
        raise ClipsAndNamedClipsError("diff")

    if (clips and len(clips) != 2) or (namedclips and len(namedclips) != 2):
        raise ValueError("diff: Must pass exactly 2 `clips` or `namedclips`!")

    if thr >= 128:
        raise ValueError("diff: `thr` must be below 128!")

    if clips and not all([c.format for c in clips]):
        raise VariableFormatError("diff")
    elif namedclips and not all([nc.format for nc in namedclips.values()]):
        raise VariableFormatError("diff")

    def _to_ranges(iterable: list[int]) -> Iterable[tuple[int, int]]:
        iterable = sorted(set(iterable))
        for _, group in groupby(enumerate(iterable), lambda t: t[1] - t[0]):
            groupl = list(group)
            yield groupl[0][1], groupl[-1][1]

    if clips:
        a, b = depth(clips[0], 8), depth(clips[1], 8)
    elif namedclips:
        nc = list(namedclips.values())
        a, b = depth(nc[0], 8), depth(nc[1], 8)

    frames = []
    if thr <= 1:
        ps = core.std.PlaneStats(a, b)

        def _cb(n: int, f: vs.VideoFrame) -> None:
            if get_prop(f, 'PlaneStatsDiff', float) > thr:
                frames.append(n)

        clip_async_render(ps, progress="Diffing clips...", callback=_cb)
        diff = core.std.MakeDiff(a, b)
    else:
        diff = diff_func(a, b).std.PlaneStats()
        t = float if diff.format.sample_type == vs.FLOAT else int  # type:ignore[union-attr]

        def _cb(n: int, f: vs.VideoFrame) -> None:
            if get_prop(f, 'PlaneStatsMin', t) <= thr or get_prop(f, 'PlaneStatsMax', t) >= 255 - thr > thr:
                frames.append(n)

        clip_async_render(diff, progress="Diffing clips...", callback=_cb)

    if not frames:
        raise StopIteration("diff: No differences found!")

    frames.sort()

    if exclusion_ranges:
        r: list[int] = []
        for e in exclusion_ranges:
            if isinstance(e, int):
                e = (e, e)
            start, end = e[0], e[1]+1
            r += list(range(start, end))
        frames = [f for f in frames if f not in r]

    if clips:
        name_a, name_b = "Clip A", "Clip B"
    else:
        name_a, name_b = namedclips.keys()

    if interleave:
        a, b = a.text.FrameNum(9), b.text.FrameNum(9)
        comparison = Interleave({f'{name_a}': core.std.Splice([a[f] for f in frames]),
                                 f'{name_b}': core.std.Splice([b[f] for f in frames])}).clip
    else:
        scaled_width = get_w(height, only_even=False)
        diff = diff.resize.Spline36(width=scaled_width * 2, height=height * 2).text.FrameNum(9)
        a, b = (c.resize.Spline36(width=scaled_width, height=height).text.FrameNum(9) for c in (a, b))

        diff_stack = Stack({f'{name_a}': core.std.Splice([a[f] for f in frames]),
                            f'{name_b}': core.std.Splice([b[f] for f in frames])}).clip
        diff = diff.text.Text(text='diff', alignment=8)
        diff = core.std.Splice([diff[f] for f in frames])

        comparison = Stack((diff_stack, diff), direction=Direction.VERTICAL).clip

    if return_ranges:
        return comparison, list(_to_ranges(frames))
    else:
        return comparison


def interleave(*clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for interleaving clips.

    :param clips:       Clips for comparison (order is kept).
    :param namedclips:  Keyword arguments of `name=clip` for all clips in the comparison.
                        Clips will be labeled at the top left with their `name`.

    :return:            An interleaved clip of all the `clips`/`namedclips` specified.

    :raises ClipsAndNamedClipsError:
                        Both positional and named clips are given.
    """
    if clips and namedclips:
        raise ClipsAndNamedClipsError("interleave")
    return Interleave(clips if clips else namedclips).clip


def split(*clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for splitting clips along the x-axis and then stacking.

    Accounts for odd-resolution clips by giving overflow columns to the last clip specified.
    All clips must have the same dimensions (width and height).

    :param clips:       Clips for comparison (order is kept left to right).
    :param namedclips:  Keyword arguments of `name=clip` for all clips in the comparison.
                        Clips will be labeled at the bottom with their `name`.

    :return:            A clip with the same dimensions as any one of the input clips.
                        with all `clips`/`namedclips` represented as individual vertical slices.

    :raises ClipsAndNamedClipsError:
                        Both positional and named clips are given.
    """
    if clips and namedclips:
        raise ClipsAndNamedClipsError("split")
    return Split(clips if clips else namedclips, label_alignment=2).clip


def stack_horizontal(*clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for stacking clips horizontally.

    :param clips:       Clips for comparison (order is kept left to right).
    :param namedclips:  Keyword arguments of `name=clip` for all clips in the comparison.
                        Clips will be labeled at the top left with their `name`.

    :return:            A horizontal stack of the `clips`/`namedclips`.

    :raises ClipsAndNamedClipsError:
                        Both positional and named clips are given.
    """
    if clips and namedclips:
        raise ClipsAndNamedClipsError("stack_horizontal")
    return Stack(clips if clips else namedclips).clip


def stack_vertical(*clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for stacking clips vertically.

    :param clips:       Clips for comparison (order is kept top to bottom).
    :param namedclips:  Keyword arguments of `name=clip` for all clips in the comparison.
                        Clips will be labeled at the top left with their `name`.

    :return:            A vertical stack of the `clips`/`namedclips`.

    :raises ClipsAndNamedClipsError:
                        Both positional and named clips are given.
    """
    if clips and namedclips:
        raise ClipsAndNamedClipsError("stack_vertical")
    return Stack(clips if clips else namedclips, direction=Direction.VERTICAL).clip


def tile(*clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for tiling clips in a rectangular pattern.

    All clips must have the same dimensions (width and height).
    If 3 clips are given, a 2x2 square with one blank slot will be returned.
    If 6 clips are given, a 3x2 rectangle will be returned.

    :param clips:       Clips for comparison.
    :param namedclips:  Keyword arguments of `name=clip` for all clips in the comparison.
                        Clips will be labeled at the top left with their `name`.

    :return:            A clip with all input `clips`/`namedclips` automatically tiled most optimally
                        into a rectangular arrrangement.

    :raises ClipsAndNamedClipsError:
                        Both positional and named clips are given.
    """
    if clips and namedclips:
        raise ClipsAndNamedClipsError("tile")
    return Tile(clips if clips else namedclips).clip


# Aliases
comp = compare
scomp = stack_compare
