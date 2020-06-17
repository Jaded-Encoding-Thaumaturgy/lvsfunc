"""
    Functions intended to be used to make comparisons between different sources
    or to be used to analyze something from a single clip.
"""
import math
import random
import warnings
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Any, Dict, List, Optional, Sequence, Set, Union

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
                            If specified a dict, the names will be overlayed on the clips using
                            ``vapoursynth.VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``vapoursynth.VideoNode.text.Text`` (Default: 7)
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

        `comp_clip = Comparer(...).clip` is the intended use in encoding scripts.
        """
        return self._compare()


class Stack(Comparer):
    """
    Stacks clips horizontally or vertically.

    Acts as a convenience combination function of ``vapoursynth.core.text.Text``
    and either ``vapoursynth.core.std.StackHorizontal`` or ``vapoursynth.core.std.StackVertical``.

    :param clips:           A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                            If specified a dict, the names will be overlayed on the clips using
                            ``vapoursynth.VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param direction:       Direction of the stack (Default: :py:attr:`lvsfunc.comparison.Direction.HORIZONTAL` )
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``vapoursynth.VideoNode.text.Text`` (Default: 7)
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
    From the VapourSynth documentation: Returns a clip with the frames from all clips interleaved.
    For example, Interleave(A=clip1, B=clip2) will return A.Frame 0, B.Frame 0, A.Frame 1, B.Frame 1, ...

    Acts as a convenience combination function of ``vapoursynth.core.text.Text``
    and ``vapoursynth.core.std.Interleave``.

    :param clips:           A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                            If specified a dict, the names will be overlayed on the clips using
                            ``vapoursynth.VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``vapoursynth.VideoNode.text.Text`` (Default: 7)
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
    Think of this as a 2-dimensional array of `0` or `1` with `0` representing an empty slot and `1` representing the
    next clip in the sequence.

    If `arrangement` is not specified, the function will attempt to fill a square with dimensions `n x n`
    where `n` is equivalent to ``math.ceil(math.sqrt(len(clips))``.::

        For example, for 3 clips, the automatic arrangement becomes:
        [
         [1, 1],
         [1, 0]
        ].

        For 7 clips, the automatic arrangement becomes:
        [
         [1, 1, 1],
         [1, 1, 1],
         [1, 0, 0]
        ].

        For custom arrangements, such as (for 4 clips):
        [
         [0, 1, 0, 1],
         [1],
         [0, 1]
        ],
        the rows will be auto-padded with `0` to be the same length.

    :param clips:           A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                            If specified a dict, the names will be overlayed on the clips using
                            ``vapoursynth.VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param arrangement:     2-dimension array (list of lists) of 0s and 1s representing a list of rows of clips(1)
                            or blank spaces(0) (Default: None)
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``vapoursynth.VideoNode.text.Text`` (Default: 7)
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

        if not all(len(row) == (max_length := max(len(row) for row in self.arrangement)) for row in self.arrangement):
            for row in self.arrangement:
                if len(row) != max_length:
                    diff = max_length - len(row)
                    for _ in range(diff):
                        row.append(0)  # padding all rows to the same length

        array_count = 0
        for list_ in self.arrangement:
            for elem in list_:
                if elem:
                    array_count += 1

        if array_count != self.num_clips:
            raise ValueError('specified arrangement has an invalid number of clips')

    def _compare(self) -> vs.VideoNode:
        clips = self._marked_clips()
        rows = [core.std.StackHorizontal([clips.pop(0) if elem else self.blank_clip for elem in row])
                for row in self.arrangement]
        return core.std.StackVertical(rows)

    def _auto_arrangement(self) -> List[List[int]]:
        dimension = 1 + math.isqrt(self.num_clips - 1)
        row = [1 for _ in range(dimension)]
        array = [row.copy() for _ in range(dimension)]

        num_blank_clips = dimension ** 2 - self.num_clips

        if num_blank_clips >= dimension:
            array.pop(-1)
            for i in range(1, num_blank_clips - dimension + 1):
                array[-1][-i] = 0
        else:
            for i in range(1, num_blank_clips + 1):
                array[-1][-i] = 0

        return array


class Split(Stack):
    """
    Split an unlimited amount of clips into one VideoNode with the same dimensions as the original clips.
    Handles odd-sized resolutions or resolutions that can't be evenly split by the amount of clips specified.

    The remaining pixel width/height (clip.dimension % number_of_clips) will be always given to the last clip specified.
    For example, five `104 x 200` clips will result in a `((20 x 200) * 4) + (24 x 200)` horiztonal stack of clips.

    :param clips:           A dict mapping names to clips or simply a sequence of clips in a tuple or a list.
                            If specified a dict, the names will be overlayed on the clips using
                            ``vapoursynth.VideoNode.text.Text``.
                            If given a simple sequence of clips, the `label_alignment` parameter will have no effect
                            and the clips will not be labeled.
                            The order of the clips in either a dict or a sequence will be kept in the comparison.
    :param direction:       Determines the axis to split the clips on
                            (Default: :py:attr:`lvsfunc.comparison.Direction.HORIZONTAL`)
    :param label_alignment: An integer from 1-9, corresponding to the positions of the keys on a numpad.
                            Only used if `clips` is a dict.
                            Determines where to place clip name using ``vapoursynth.VideoNode.text.Text`` (Default: 7)
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
    This can be disabled by setting `disable_resample` to True.

    Alias for this function is `lvsfunc.comp`.

    Dependencies: mvsfunc

    :param clip_a:              Clip to compare
    :param clip_b:              Second clip to compare
    :param frames:              List of frames to compare (Default: None)
    :param rand_total:          Number of random frames to pick (Default: None)
    :param force_resample:      Forcibly resamples the clip to RGB24 (Default: True)
    :param print_frame:         Print frame numbers (Default: True)
    :param mismatch:            Allow for clips with different formats and dimensions to be compared (Default: False)

    :return:                    Interleaved clip containing specified frames from clip_a and clip_b
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
                  make_diff: bool = False,
                  height: Optional[int] = None,
                  warn: bool = True) -> vs.VideoNode:
    """
    A simple wrapper that allows you to compare two clips by stacking them.
    You can stack an infinite amount of clips.

    Best to use when trying to match two sources frame-accurately, however by setting height to the source's
    height (or None), it can be used for comparing frames.

    Alias for this function is `lvsfunc.scomp`.

    :param clips:             Clips to compare
    :param make_diff:         Create and stack a diff (only works if two clips are given) (Default: False)
    :param height:            Output height, determined automatically if None (Default: None)
    :param warn:              Warns if the length of given clips don't align (Default: True)

    :return:                  Clip with clips stacked
    """
    if len(clips) < 2:
        raise ValueError("stack_compare: 'Too few clips supplied'")

    if len(clips) != 2 and make_diff:
        raise ValueError("stack_compare: 'You can only create a diff for two clips'")

    formats = set()
    for c in clips:
        if c.format is None:
            raise ValueError("stack_compare: 'Variable-format clips not supported'")
        formats.add(c.format.id)
    if len(formats) != 1:
        raise ValueError("stack_compare: 'The format of every clip must be equal'")

    if make_diff:
        diff = core.std.MakeDiff(clips[0], clips[1])
        diff = core.resize.Spline36(diff, get_w(576), 576).text.FrameNum(8)
        resize = [core.resize.Spline36(c, int(diff.width / 2), int(diff.height / 2)) for c in clips]
        resize[0], resize[1] = resize[0].text.Text("Clip A", 3), resize[1].text.Text("Clip B", 1)
        stack = core.std.StackVertical([core.std.StackHorizontal([resize[0], resize[1]]), diff])
    else:
        stack = core.std.StackHorizontal(clips)
    if warn:
        if len(set([c.num_frames for c in clips])) != 1:
            stack = core.text.Text(stack,
                                   "Clip Length Mismatch Detected!\nPlease make sure the lengths of all clips match!\n"
                                   + "".join(f"\nClip {i+1}: {c.num_frames} Frames" for i, c in enumerate(clips)), 2)
    return stack


def stack_planes(clip: vs.VideoNode,
                 stack_vertical: bool = False) -> vs.VideoNode:
    """
    Stacks the planes of a clip.

    :param clip:              Input clip
    :param stack_vertical:    Stack the planes vertically (Default: False)

    :return:                  Clip with stacked planes
    """

    planes = split(clip)
    subsampling = get_subsampling(clip)

    if subsampling == '420':
        if stack_vertical:
            stack = core.std.StackHorizontal([planes[1], planes[2]])
            return core.std.StackVertical([planes[0], stack])
        else:
            stack = core.std.StackVertical([planes[1], planes[2]])
            return core.std.StackHorizontal([planes[0], stack])
    elif subsampling == '444':
        return core.std.StackVertical(planes) if stack_vertical else core.std.StackHorizontal(planes)
    else:
        raise ValueError("stack_planes: 'Input clip must be in YUV format with 444 or 420 chroma subsampling'")


def tvbd_diff(tv: vs.VideoNode, bd: vs.VideoNode,
              thr: float = 72,
              return_array: bool = False) -> vs.VideoNode:
    """
    Creates a standard `stack_compare` between frames from two clips that have differences.
    Useful for making comparisons between TV and BD encodes, as well as clean and hardsubbed sources.

    There are two methods used here to find differences.
    If thr is below 1, PlaneStatsDiff is used to figure out the differences.
    Else, if thr is equal than or higher than 1, PlaneStatsMin/Max are used.

    Recommended is PlaneStatsMin/Max, as those seem to catch
    more outrageous differences more easily and not return
    too many starved frames.

    Note that this might catch artifacting as differences!
    Make sure you verify every frame with your own eyes!

    Alias for this function is `lvsfunc.diff`.

    :param tv:            TV clip
    :param bd:            BD clip
    :param thr:           Threshold, <= 1 uses PlaneStatsDiff, >1 uses Max/Min. Max is 128 (Default: 72)
    :param return_array:  Return frames as an interleaved comparison (using py:func:`lvsfunc.comparison.compare`)
                          (Default: False)
    """
    if thr > 128:
        raise ValueError("tvbd_diff: \"thr\" should neither be nor exceed 128!'")

    tv, bd = depth(tv, 8), depth(bd, 8)

    if thr <= 1:
        diff = core.std.PlaneStats(tv, bd)
        frames = [i for i, f in enumerate(diff.frames()) if get_prop(f, "PlaneStatsDiff", float) > thr]
    else:
        diff = core.std.MakeDiff(tv, bd).std.PlaneStats()
        if diff.format is None:
            raise ValueError("tvbd_diff: 'Variable-format clips not supported'")
        t = float if diff.format.sample_type == vs.FLOAT else int
        frames = [i for i, f in enumerate(diff.frames())
                  if get_prop(f, "PlaneStatsMin", t) <= thr
                  or get_prop(f, "PlaneStatsMax", t) >= 255 - thr]

    if not frames:
        raise ValueError("tvbd_diff: 'No differences found'")

    if return_array:
        return compare(tv.text.FrameNum().text.Text('Clip A', 9),
                       bd.text.FrameNum().text.Text('Clip B', 9),
                       frames)
    else:
        if thr <= 1:
            diff = core.std.MakeDiff(tv, bd)
        diff = core.resize.Spline36(diff, get_w(576), 576).text.FrameNum(8)
        tv = core.resize.Spline36(tv, int(diff.width / 2), int(diff.height / 2)).text.Text("Clip A", 3)
        bd = core.resize.Spline36(bd, int(diff.width / 2), int(diff.height / 2)).text.Text("Clip B", 3)
        stacked = core.std.StackVertical([core.std.StackHorizontal([tv, bd]), diff])
        return core.std.Splice([stacked[f] for f in frames])




def interleave(*clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for interleaving clips.

    :param clips: Clips for comparison (order is kept)

    :return: Returns an interleaved clip of all the clips specified
    """
    return Interleave(clips).clip


def split(**clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience funciton for splitting clips along the x-axis and then stacking (order is kept left to right).
    Accounts for odd-resolution clips by giving overflow columns to the last clip specified.

    :param clips: Keyword arguments of name=clip for all clips in the comparison.
                  All clips must have the same dimensions (width and height).
                  Clips will be labeled at the bottom with their `name`.
    :return: A clip with the same dimensions as any one of the input clips
             with all clips represented as individual vertical slices.
    """
    return Split(clips, label_alignment=2).clip


def stack_horizontal(*clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for stacking clips horizontally.

    :param clips: Clips for comparison (order is kept left to right)

    :return: Returns a horizontal stack of the clips
    """
    return Stack(clips).clip


def stack_vertical(*clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for stacking clips vertically.

    :param clips: Clips for comparison (order is kept top to bottom)

    :return: Returns a vertical stack of the clips
    """
    return Stack(clips, direction=Direction.VERTICAL).clip


def tile(**clips: vs.VideoNode) -> vs.VideoNode:
    """
    Small convenience function for tiling clips in a square pattern.

    :param clips: Keyword arguments of name=clip for all clips in the comparison.
                  All clips must have the same dimensions (width and height).
                  Clips will be labeled with their `name`.
                  If 3 clips are given, a 2x2 square with one blank slot will be returned.
                  If 5 clips are given, a 3x3 square with four blank slots will be returned.

    :return: A clip with all input clips automatically tiled most optimally into a square arrrangement.
    """
    return Tile(clips).clip
