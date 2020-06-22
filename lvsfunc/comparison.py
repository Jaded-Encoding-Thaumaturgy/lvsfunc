"""
    Functions intended to be used to make comparisons between different sources
    or to be used to analyze something from a single clip.
"""
import math
import random
import warnings
from abc import ABC, abstractmethod
from enum import IntEnum
from itertools import zip_longest
from typing import Any, Dict, Iterator, List, Optional, Sequence, Set, Union

import vapoursynth as vs
import vsutil

from .util import get_prop

core = vs.core


class Direction(IntEnum):
    """
    Enum to simplify direction argument.
    """
    HORIZONTAL = 0
    VERTICAL = 1


class Comparer(ABC):
    """
    Base class for comparison functions.

    :param clips:           A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                            If given a dict, the names will be overlayed on the clips using
                            ``VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``VideoNode.text.Text`` (Default: 7)
    """
    def __init__(self,
                 clips: Union[Dict[str, vs.VideoNode], Sequence[vs.VideoNode]],
                 /,
                 *,
                 label_alignment: int = 7
                 ) -> None:
        if len(clips) < 2:
            raise ValueError("Comparer: compare functions must be used on at least 2 clips")
        if label_alignment not in list(range(1, 10)):
            raise ValueError("Comparer: `label_alignment` must be an integer from 1 to 9")
        if not isinstance(clips, (dict, Sequence)):
            raise ValueError(f"Comparer: unexpected type {type(clips)} for `clips` argument")

        self.clips: List[vs.VideoNode] = list(clips.values()) if isinstance(clips, dict) else list(clips)
        self.names: Optional[List[str]] = list(clips.keys()) if isinstance(clips, dict) else None

        self.label_alignment = label_alignment

        self.num_clips = len(clips)

        widths: Set[int] = {clip.width for clip in self.clips}
        self.width: Optional[int] = w if (w := widths.pop()) != 0 and len(widths) == 0 else None

        heights: Set[int] = {clip.height for clip in self.clips}
        self.height: Optional[int] = h if (h := heights.pop()) != 0 and len(heights) == 0 else None

        formats: Set[Optional[str]] = {getattr(clip.format, 'name', None) for clip in self.clips}
        self.format: Optional[str] = formats.pop() if len(formats) == 1 else None

    def _marked_clips(self) -> List[vs.VideoNode]:
        """
        If a `name` is only space characters, `'   '`, for example, the name will not be overlayed on the clip.
        """
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
        Returns the comparison as a single VideoNode for further manipulation or attribute inspection.

        ``comp_clip = Comparer(...).clip`` is the intended use in encoding scripts.
        """
        return self._compare()


class Stack(Comparer):
    """
    Stacks clips horizontally or vertically.

    Acts as a convenience combination function of ``vapoursynth.core.text.Text``
    and either ``vapoursynth.core.std.StackHorizontal`` or ``vapoursynth.core.std.StackVertical``.

    :param clips:           A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                            If given a dict, the names will be overlayed on the clips using
                            ``VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param direction:       Direction of the stack (Default: :py:attr:`lvsfunc.comparison.Direction.HORIZONTAL`)
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``VideoNode.text.Text`` (Default: 7)
    """

    def __init__(self,
                 clips: Union[Dict[str, vs.VideoNode], Sequence[vs.VideoNode]],
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
                raise ValueError("Stack: StackHorizontal requires that all clips be the same height")
            return core.std.StackHorizontal(self._marked_clips())

        if not self.width:
            raise ValueError("Stack: StackVertical requires that all clips be the same width")
        return core.std.StackVertical(self._marked_clips())


class Interleave(Comparer):
    """
    From the VapourSynth documentation: `Returns a clip with the frames from all clips interleaved.
    For example, Interleave(A=clip1, B=clip2) will return A.Frame 0, B.Frame 0, A.Frame 1, B.Frame 1, ...`

    Acts as a convenience combination function of ``vapoursynth.core.text.Text``
    and ``vapoursynth.core.std.Interleave``.

    :param clips:           A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                            If given a dict, the names will be overlayed on the clips using
                            ``VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``VideoNode.text.Text`` (Default: 7)
    """

    def __init__(self,
                 clips: Union[Dict[str, vs.VideoNode], Sequence[vs.VideoNode]],
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

    :param clips:           A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                            If given a dict, the names will be overlayed on the clips using
                            ``VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param arrangement:     2-dimension array (list of lists) of 0s and 1s representing a list of rows of clips(`1`)
                            or blank spaces(`0`) (Default: ``None``)
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``VideoNode.text.Text`` (Default: 7)
    """

    def __init__(self,
                 clips: Union[Dict[str, vs.VideoNode], Sequence[vs.VideoNode]],
                 /,
                 *,
                 arrangement: Optional[List[List[int]]] = None,
                 label_alignment: int = 7
                 ) -> None:
        super().__init__(clips, label_alignment=label_alignment)

        if not self.width or not self.height:
            raise ValueError("Tile: all clip widths, and heights must be the same")

        if arrangement is None:
            self.arrangement = self._auto_arrangement()
        else:
            is_one_dim = len(arrangement) < 2 or all(len(row) == 1 for row in arrangement)
            if is_one_dim:
                raise ValueError("Tile: use Stack instead if the array is one dimensional")
            self.arrangement = arrangement

        self.blank_clip = core.std.BlankClip(clip=self.clips[0], keep=1)

        max_length = max(map(len, self.arrangement))
        self.arrangement = [row + [0] * (max_length - len(row)) for row in self.arrangement]

        array_count = sum(map(sum, self.arrangement))

        if array_count != self.num_clips:
            raise ValueError('specified arrangement has an invalid number of clips')

    def _compare(self) -> vs.VideoNode:
        clips = self._marked_clips()
        rows = [core.std.StackHorizontal([clips.pop(0) if elem else self.blank_clip for elem in row])
                for row in self.arrangement]
        return core.std.StackVertical(rows)

    def _auto_arrangement(self) -> List[List[int]]:
        def _grouper(iterable, n, fillvalue=None) -> Iterator:
            args = [iter(iterable)] * n
            return zip_longest(*args, fillvalue=fillvalue)

        dimension = 1 + math.isqrt(self.num_clips - 1)
        return list(map(list, _grouper([1] * self.num_clips, dimension, 0)))


class Split(Stack):
    """
    Split an unlimited amount of clips into one VideoNode with the same dimensions as the original clips.
    Handles odd-sized resolutions or resolutions that can't be evenly split by the amount of clips specified.

    The remaining pixel width/height (``clip.dimension % number_of_clips``)
    will be always given to the last clip specified.
    For example, five `104 x 200` clips will result in a `((20 x 200) * 4) + (24 x 200)` horiztonal stack of clips.

    :param clips:           A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                            If given a dict, the names will be overlayed on the clips using
                            ``VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param direction:       Determines the axis to split the clips on
                            (Default: :py:attr:`lvsfunc.comparison.Direction.HORIZONTAL`)
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``VideoNode.text.Text`` (Default: 7)
    """

    def __init__(self,
                 clips: Union[Dict[str, vs.VideoNode], Sequence[vs.VideoNode]],
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
            raise ValueError("Split: all clips must have same width and height")

        breaks_subsampling = ((self.direction == Direction.HORIZONTAL and (((self.width // self.num_clips) % 2)
                                                                           or ((self.width % self.num_clips) % 2)))
                              or (self.direction == Direction.VERTICAL and (((self.height // self.num_clips) % 2)
                                                                            or ((self.height % self.num_clips) % 2))))

        is_subsampled = not all(vsutil.get_subsampling(clip) in ('444', None) for clip in self.clips)

        if breaks_subsampling and is_subsampled:
            raise ValueError("Split: resulting cropped width or height violates subsampling rules; "
                             "consider resampling to YUV444 or RGB before attempting to crop")

        if self.direction == Direction.HORIZONTAL:
            crop_width, overflow = divmod(self.width, self.num_clips)

            for key, clip in enumerate(self.clips):
                left_crop = crop_width * key
                right_crop = crop_width * (self.num_clips - 1 - key)

                if key != (self.num_clips - 1):
                    right_crop += overflow

                self.clips[key] = clip.std.Crop(left=left_crop, right=right_crop)

        elif self.direction == Direction.VERTICAL:
            crop_height, overflow = divmod(self.height, self.num_clips)

            for key, clip in enumerate(self.clips):
                top_crop = crop_height * key
                bottom_crop = crop_height * (self.num_clips - 1 - key)

                if key != (self.num_clips - 1):
                    bottom_crop += overflow

                self.clips[key] = clip.std.Crop(top=top_crop, bottom=bottom_crop)


def compare(clip_a: vs.VideoNode, clip_b: vs.VideoNode,
            frames: Optional[List[int]] = None,
            rand_total: Optional[int] = None,
            force_resample: bool = True, print_frame: bool = True,
            mismatch: bool = False) -> vs.VideoNode:
    """
    Allows for the same frames from two different clips to be compared by interleaving them into a single clip.
    Clips are automatically resampled to 8 bit YUV -> RGB24 to emulate how a monitor shows the frame.
    This can be disabled by setting `force_resample` to ``False``.

    Alias for this function is `lvsfunc.comp`.

    Dependencies: mvsfunc

    :param clip_a:         Clip to compare
    :param clip_b:         Second clip to compare
    :param frames:         List of frames to compare (Default: ``None``)
    :param rand_total:     Number of random frames to pick (Default: ``None``)
    :param force_resample: Forcibly resamples the clip to RGB24 (Default: ``True``)
    :param print_frame:    Print frame numbers (Default: ``True``)
    :param mismatch:       Allow for clips with different formats and dimensions to be compared (Default: ``False``)

    :return:               Interleaved clip containing specified frames from `clip_a` and `clip_b`
    """
    try:
        from mvsfunc import GetMatrix
    except ModuleNotFoundError:
        raise ModuleNotFoundError("compare: missing dependency 'mvsfunc'")

    def _resample(clip: vs.VideoNode) -> vs.VideoNode:
        # Resampling to 8 bit and RGB to properly display how it appears on your screen
        return vsutil.depth(clip.resize.Point(format=vs.RGB24, matrix_in_s=str(GetMatrix(clip))), 8)

    # Error handling
    if frames and len(frames) > clip_a.num_frames:
        raise ValueError("compare: 'More comparisons requested than frames available'")

    if force_resample:
        clip_a, clip_b = _resample(clip_a), _resample(clip_b)
    else:
        if clip_a.format is None or clip_b.format is None:
            raise ValueError("compare: 'Variable-format clips not supported'")
        if clip_a.format.id != clip_b.format.id:
            raise ValueError("compare: 'The format of both clips must be equal'")

    if print_frame:
        clip_a, clip_b = clip_a.text.FrameNum(), clip_b.text.FrameNum()

    if frames is None:
        if not rand_total:
            # More comparisons for shorter clips so you can compare stuff like NCs more conveniently
            rand_total = int(clip_a.num_frames / 1000) if clip_a.num_frames > 5000 else int(clip_a.num_frames / 100)
        frames = sorted(random.sample(range(1, clip_a.num_frames - 1), rand_total))

    frames_a = core.std.Splice([clip_a[f] for f in frames])
    frames_b = core.std.Splice([clip_b[f] for f in frames])
    return core.std.Interleave([frames_a, frames_b], mismatch=mismatch)


def stack_compare(*clips: vs.VideoNode,
                  make_diff: bool = True,
                  height: int = 288,
                  warn: Any = None
                  ) -> vs.VideoNode:
    """
    A simple wrapper that allows you to compare two clips by stacking them.

    Best to use when trying to match two sources frame-accurately.
    Alias for this function is `lvsfunc.scomp`.

    :param clips:     Clips to compare
    :param make_diff: Create and stack a diff (only works if two clips are given) (Default: ``True``)
    :param height:    Height in px to rescale clips to if `make_diff` is ``True``
                      (MakeDiff clip will be twice this resolution) (Default: 288)
    :param warn:      Unused parameter kept for backward compatibility

    :return:          Clip with `clips` stacked
    """
    if not make_diff:
        warnings.warn('stack_compare has been deprecated in favor of `lvsfunc.comparison.Stack` '
                      'if not using `make_diff`', DeprecationWarning)
        return core.std.StackHorizontal(clips)

    if len(clips) != 2:
        raise ValueError("stack_compare: `make_diff` only works for exactly 2 clips")

    clipa, clipb = clips[0:2]
    scaled_width = vsutil.get_w(height, only_even=False)

    diff = core.std.MakeDiff(clipa=clipa, clipb=clipb)
    diff = diff.resize.Spline36(width=scaled_width * 2, height=height * 2).text.FrameNum(8)
    resized = [clips[0].resize.Spline36(width=scaled_width, height=height).text.Text('Clip A', 3),
               clips[1].resize.Spline36(width=scaled_width, height=height).text.Text('Clip B', 1)]

    return Stack([Stack(resized).clip, diff], direction=Direction.VERTICAL).clip


def stack_planes(clip: vs.VideoNode, /, stack_vertical: bool = False) -> vs.VideoNode:
    """
    Stacks the planes of a clip.
    For 4:2:0 subsampled clips, the two half-sized planes will be stacked in the opposite direction specified
    (vertical by default),
    then stacked with the full-sized plane in the direction specified (horizontal by default).

    :param clip:           Input clip (must be in YUV or RGB planar format)
    :param stack_vertical: Stack the planes vertically (Default: ``False``)

    :return:               Clip with stacked planes
    """
    if clip.format is None:
        raise ValueError("stack_planes: variable-format clips not allowed")
    if clip.format.num_planes != 3:
        raise ValueError("stack_planes: input clip must be in YUV or RGB planar format")

    split_planes = vsutil.split(clip)

    if clip.format.color_family == vs.ColorFamily.YUV:
        planes: Dict[str, vs.VideoNode] = {'Y': split_planes[0], 'U': split_planes[1], 'V': split_planes[2]}
    elif clip.format.color_family == vs.ColorFamily.RGB:
        planes = {'R': split_planes[0], 'G': split_planes[1], 'B': split_planes[2]}
    else:
        raise ValueError(f"stack_planes: unexpected color family {clip.format.color_family.name}")

    direction: Direction = Direction.HORIZONTAL if not stack_vertical else Direction.VERTICAL

    if vsutil.get_subsampling(clip) in ('444', None):
        return Stack(planes, direction=direction).clip

    elif vsutil.get_subsampling(clip) == '420':
        subsample_direction: Direction = Direction.HORIZONTAL if stack_vertical else Direction.VERTICAL
        y_plane = planes.pop('Y').text.Text(text='Y')
        subsampled_planes = Stack(planes, direction=subsample_direction).clip

        return Stack([y_plane, subsampled_planes], direction=direction).clip

    else:
        raise ValueError(f"stack_planes: unexpected subsampling {vsutil.get_subsampling(clip)}")


def tvbd_diff(tv: vs.VideoNode, bd: vs.VideoNode,
              thr: float = 72,
              height: int = 288,
              return_array: bool = False) -> vs.VideoNode:
    """
    Creates a standard :py:class:`lvsfunc.comparison.Stack` between frames from two clips that have differences.
    Useful for making comparisons between TV and BD encodes, as well as clean and hardsubbed sources.

    There are two methods used here to find differences.
    If `thr` is below 1, PlaneStatsDiff is used to figure out the differences.
    Else, if `thr` is equal than or higher than 1, PlaneStatsMin/Max are used.

    Recommended is PlaneStatsMin/Max, as those seem to catch
    more outrageous differences more easily and not return
    too many starved frames.

    Note that this might catch artifacting as differences!
    Make sure you verify every frame with your own eyes!

    Alias for this function is `lvsfunc.diff`.

    :param tv:            TV clip
    :param bd:            BD clip
    :param thr:           Threshold, <= 1 uses PlaneStatsDiff, >1 uses Max/Min.
                          Value must be below 128 (Default: 72)
    :param height:        Height in px to downscale clips to if `return_array` is ``False``
                          (MakeDiff clip will be twice this resolution) (Default: 288)
    :param return_array:  Return frames as an interleaved comparison (using :py:class:`lvsfunc.comparison.Interleave`)
                          (Default: ``False``)
    """
    if thr >= 128:
        raise ValueError("tvbd_diff: `thr` must be below 128")

    if None in (tv.format, bd.format):
        raise ValueError("tvbd_diff: variable-format clips not supported")

    tv, bd = vsutil.depth(tv, 8), vsutil.depth(bd, 8)

    if thr <= 1:
        frames = [i for i, f in enumerate(core.std.PlaneStats(tv, bd).frames())
                  if get_prop(f, 'PlaneStatsDiff', float) > thr]
        diff = core.std.MakeDiff(tv, bd)
    else:
        diff = core.std.MakeDiff(tv, bd).std.PlaneStats()
        if diff.format is None:
            raise ValueError("tvbd_diff: variable-format clips not supported")  # this is for mypy
        t = float if diff.format.sample_type == vs.SampleType.FLOAT else int
        frames = [i for i, f in enumerate(diff.frames())
                  if get_prop(f, 'PlaneStatsMin', t) <= thr or get_prop(f, 'PlaneStatsMax', t) >= 255 - thr]

    if not frames:
        raise ValueError("tvbd_diff: no differences found")

    if return_array:
        tv, bd = tv.text.FrameNum(9), bd.text.FrameNum(9)
        return Interleave({'TV': core.std.Splice([tv[f] for f in frames]),
                           'BD': core.std.Splice([bd[f] for f in frames])}).clip

    else:
        scaled_width = vsutil.get_w(height, only_even=False)
        diff = diff.resize.Spline36(width=scaled_width * 2, height=height * 2).text.FrameNum(9)
        tv, bd = (c.resize.Spline36(width=scaled_width, height=height).text.FrameNum(9) for c in (tv, bd))

        tvbd_stack = Stack({'TV': core.std.Splice([tv[f] for f in frames]),
                            'BD': core.std.Splice([bd[f] for f in frames])}).clip
        diff = diff.text.Text(text='diff', alignment=8)
        diff = core.std.Splice([diff[f] for f in frames])
        return Stack((tvbd_stack, diff), direction=Direction.VERTICAL).clip


def interleave(*clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for interleaving clips.

    :param clips: Clips for comparison (order is kept)

    :return: Returns an interleaved clip of all the `clips` specified
    """
    return Interleave(clips).clip


def split(**clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience funciton for splitting clips along the x-axis and then stacking (order is kept left to right).
    Accounts for odd-resolution clips by giving overflow columns to the last clip specified.

    :param clips: Keyword arguments of `name=clip` for all clips in the comparison.
                  All clips must have the same dimensions (width and height).
                  Clips will be labeled at the bottom with their `name`.
    :return: A clip with the same dimensions as any one of the input clips
             with all `clips` represented as individual vertical slices.
    """
    return Split(clips, label_alignment=2).clip


def stack_horizontal(*clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for stacking clips horizontally.

    :param clips: Clips for comparison (order is kept left to right)

    :return: Returns a horizontal stack of the `clips`
    """
    return Stack(clips).clip


def stack_vertical(*clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for stacking clips vertically.

    :param clips: Clips for comparison (order is kept top to bottom)

    :return: Returns a vertical stack of the `clips`
    """
    return Stack(clips, direction=Direction.VERTICAL).clip


def tile(**clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for tiling clips in a rectangular pattern.

    :param clips: Keyword arguments of `name=clip` for all clips in the comparison.
                  All clips must have the same dimensions (width and height).
                  Clips will be labeled with their `name`.
                  If 3 clips are given, a 2x2 square with one blank slot will be returned.
                  If 7 clips are given, a 3x3 square with two blank slots will be returned.

    :return: A clip with all input `clips` automatically tiled most optimally into a rectangular arrrangement.
    """
    return Tile(clips).clip
