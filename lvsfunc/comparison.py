from __future__ import annotations

import math
import random
import warnings
from abc import ABC, abstractmethod
from itertools import groupby, zip_longest
from typing import Callable, Iterable, Iterator, Literal, Sequence, overload

from vskernels import Catrom, Kernel, KernelT, Point
from vstools import (CustomError, CustomNotImplementedError, CustomTypeError,
                     CustomValueError, Direction, FormatsMismatchError,
                     LengthMismatchError, Matrix, Sentinel, T,
                     VariableFormatError, check_variable_format,
                     check_variable_resolution, clip_async_render, core, depth,
                     get_prop, get_subsampling, get_w, merge_clip_props, mod2,
                     vs)

from .exceptions import ClipsAndNamedClipsError

__all__ = [
    'compare',
    'Comparer',
    'comparison_shots',
    'find_diff', 'diff',
    'Interleave',
    'Split',
    'stack_compare',
    'Stack',
    'Tile',
    'diff_between_clips_stack',
]


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

    def __init__(
        self, clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /, *, label_alignment: int = 7,
    ) -> None:
        if len(clips) < 2:
            raise CustomValueError(
                "Compare functions must be used on at least 2 clips!", self.__class__
            )

        if label_alignment not in list(range(1, 10)):
            raise CustomValueError(
                "`label_alignment` must be an integer from 1 to 9!", self.__class__
            )

        if not isinstance(clips, (dict, Sequence)):
            raise CustomTypeError(
                f"Unexpected type {type(clips)} for `clips` argument!", self.__class__
            )

        self.clips = list(clips.values()) if isinstance(clips, dict) else list(clips)
        self.names = list(clips.keys()) if isinstance(clips, dict) else None

        self.label_alignment = label_alignment

        self.num_clips = len(clips)

        widths = {clip.width for clip in self.clips}
        heights = {clip.height for clip in self.clips}
        formats = {getattr(clip.format, "name", None) for clip in self.clips}

        self.width = w if (w := widths.pop()) != 0 and len(widths) == 0 else None
        self.height = h if (h := heights.pop()) != 0 and len(heights) == 0 else None
        self.format = formats.pop() if len(formats) == 1 else None

    def _marked_clips(self) -> list[vs.VideoNode]:
        """If a `name` is only space characters, `'   '`, for example, the name will not be overlaid on the clip."""

        if self.names:
            return [
                clip.text.Text(text=name, alignment=self.label_alignment) if name.strip()
                else clip for clip, name in zip(self.clips, self.names)
            ]

        return self.clips.copy()

    @abstractmethod
    def _compare(self) -> vs.VideoNode:
        raise CustomNotImplementedError(
            "This function or method has not been implemented yet!", self.__class__
        )

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

    def __init__(
        self, clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /, *, direction: Direction = Direction.HORIZONTAL,
        label_alignment: int = 7,
    ) -> None:
        self.direction = direction

        super().__init__(clips, label_alignment=label_alignment)

    def _compare(self) -> vs.VideoNode:
        if self.direction == Direction.HORIZONTAL:
            if not self.height:
                raise CustomValueError(
                    "StackHorizontal requires that all clips be the same height!",
                    self.__class__,
                )

            return core.std.StackHorizontal(self._marked_clips())

        if not self.width:
            raise CustomValueError(
                "StackVertical requires that all clips be the same width!",
                self.__class__,
            )

        return core.std.StackVertical(self._marked_clips())

    @classmethod
    def stack(cls, *clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
        if clips and namedclips:
            raise ClipsAndNamedClipsError(cls.stack)

        return cls(clips if clips else namedclips).clip

    @classmethod
    def stack_vertical(
        cls, *clips: vs.VideoNode, **namedclips: vs.VideoNode
    ) -> vs.VideoNode:
        if clips and namedclips:
            raise ClipsAndNamedClipsError(cls.stack)

        return cls(clips if clips else namedclips, direction=Direction.VERTICAL).clip


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

    def __init__(
        self, clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /, *, label_alignment: int = 7,
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

    def __init__(
        self, clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /, *, arrangement: list[list[int]] | None = None,
        label_alignment: int = 7,
    ) -> None:
        super().__init__(clips, label_alignment=label_alignment)

        if not self.width or not self.height:
            raise CustomValueError(
                "All clip widths and heights must be the same!", self.__class__
            )

        if arrangement is None:
            self.arrangement = self._auto_arrangement()
        else:
            is_one_dim = len(arrangement) < 2 or all(
                len(row) == 1 for row in arrangement
            )
            if is_one_dim:
                raise CustomValueError(
                    "Use Stack instead if the array is one dimensional!", self.__class__
                )
            self.arrangement = arrangement

        self.blank_clip = core.std.BlankClip(clip=self.clips[0], keep=1)

        max_length = max(map(len, self.arrangement))

        self.arrangement = [
            row + [0] * (max_length - len(row)) for row in self.arrangement
        ]

        array_count = sum(map(sum, self.arrangement))  # type:ignore[arg-type]

        LengthMismatchError.check(
            self.__class__,
            array_count,
            self.num_clips,
            message="Specified arrangement has an invalid number of clips!",
        )

    def _compare(self) -> vs.VideoNode:
        clips = self._marked_clips()

        rows = [
            core.std.StackHorizontal(
                [clips.pop(0) if elem else self.blank_clip for elem in row]
            )
            for row in self.arrangement
        ]

        return core.std.StackVertical(rows)

    def _auto_arrangement(self) -> list[list[int]]:
        def _grouper(
            iterable: Iterable[T], n: int, fillvalue: T | None = None
        ) -> Iterator[tuple[T, ...]]:
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

    def __init__(
        self, clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /, *, direction: Direction = Direction.HORIZONTAL,
        label_alignment: int = 7,
    ) -> None:
        super().__init__(clips, direction=direction, label_alignment=label_alignment)

        self._smart_crop()

    def _smart_crop(self) -> None:  # has to alter self.clips to send clips to _marked_clips() in Stack's _compare()
        """Crops self.clips in place accounting for odd resolutions."""

        if not self.width or not self.height:
            raise CustomValueError(
                "All clips must have same width and height!", self.__class__
            )

        breaks_subsampling = (
            self.direction == Direction.HORIZONTAL
            and (
                ((self.width // self.num_clips) % 2)
                or ((self.width % self.num_clips) % 2)
            )
        ) or (
            self.direction == Direction.VERTICAL
            and (
                ((self.height // self.num_clips) % 2)
                or ((self.height % self.num_clips) % 2)
            )
        )

        is_subsampled = not all(
            get_subsampling(clip) in ("444", None) for clip in self.clips
        )

        if breaks_subsampling and is_subsampled:
            raise CustomValueError(
                "Resulting cropped width or height violates subsampling rules! "
                "Consider resampling to YUV444 or RGB before attempting to crop!",
                self.__class__,
            )

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

        raise CustomValueError("Unknown direction", self.__class__)

    @classmethod
    def stack(cls, *clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
        if clips and namedclips:
            raise ClipsAndNamedClipsError(cls.stack)

        return cls(clips if clips else namedclips, label_alignment=2).clip


def compare(
    clip_a: vs.VideoNode, clip_b: vs.VideoNode,
    frames: list[int] | None = None,
    rand_total: int | None = None,
    force_resample: bool = True,
    print_frame: bool = True,
    mismatch: bool = False,
) -> vs.VideoNode:
    """
    Compare the same frames from two different clips by interleaving them into a single clip.

    Clips are automatically resampled to 8 bit YUV -> RGB24 to emulate how a monitor shows the frame.
    This can be disabled by setting `force_resample` to ``False``.

    This is not recommended over setting multiple outputs and checking between those,
    but in the event that is unavailable to you, this function may be useful.

    Alias for this function is ``lvsfunc.comp``.

    :param clip_a:                      Clip to compare.
    :param clip_b:                      Second clip to compare.
    :param frames:                      List of frames to compare (Default: ``None``).
    :param rand_total:                  Number of random frames to pick (Default: ``None``).
    :param force_resample:              Forcibly resamples the clip to RGB24 (Default: ``True``).
    :param print_frame:                 Print frame numbers (Default: ``True``).
    :param mismatch:                    Allow for clips with different formats and dimensions
                                        to be compared (Default: ``False``).

    :return:                            Interleaved clip containing specified frames from `clip_a` and `clip_b`.

    :raises VariableResolutionError:    One of the given clips is of a variable resolution.
    :raises ValueError:                 More comparisons requested than frames available.
    :raises VariableFormatError:        `mismatch` is False and one of the given clips is of a variable resolution.
    :raises FormatsMismatchError:       `mismatch` is False and format of given clips don't match.
    """

    def _resample(clip: vs.VideoNode) -> vs.VideoNode:
        # Resampling to 8 bit and RGB to properly display how it appears on your screen
        return Catrom.resample(
            clip, vs.RGB24, None, Matrix.from_video(clip), dither_type="error_diffusion"
        )

    check_variable_resolution(clip_a, compare)
    check_variable_resolution(clip_b, compare)

    # Error handling
    if frames and len(frames) > clip_a.num_frames:
        raise CustomValueError(
            "More comparisons requested than frames available!",
            compare,
            reason=f"{len(frames)} > {clip_a.num_frames}",
        )

    if force_resample:
        clip_a, clip_b = _resample(clip_a), _resample(clip_b)
    elif mismatch is False:
        assert check_variable_format(clip_a, compare)
        assert check_variable_format(clip_b, compare)

        FormatsMismatchError.check(compare, clip_a, clip_b)

    if print_frame:
        clip_a = clip_a.text.Text("Clip A").text.FrameNum(alignment=9)
        clip_b = clip_b.text.Text("Clip B").text.FrameNum(alignment=9)

    if frames is None:
        if not rand_total:
            # More comparisons for shorter clips so you can compare stuff like NCs more conveniently
            rand_total = (
                int(clip_a.num_frames / 1000)
                if clip_a.num_frames > 5000
                else int(clip_a.num_frames / 100)
            )

        frames = sorted(random.sample(range(1, clip_a.num_frames - 1), rand_total))

    frames_a = core.std.Splice([clip_a[f] for f in frames]).std.AssumeFPS(fpsnum=1, fpsden=1)
    frames_b = core.std.Splice([clip_b[f] for f in frames]).std.AssumeFPS(fpsnum=1, fpsden=1)

    return core.std.Interleave([frames_a, frames_b], mismatch=mismatch)


def stack_compare(*clips: vs.VideoNode, height: int | None = None) -> vs.VideoNode:
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
        raise CustomValueError("You must pass at least two clips", stack_compare, f"{len(clips)} < 2")

    clipa, clipb = clips

    if not height:
        height = 288
    elif height > clipa.height / 2:
        import warnings

        warnings.warn(
            f"stack_compare: 'Given 'height' ({height}) is bigger than clipa's height {clipa.height}!' "
            "Will be using clipa's height instead."
        )
        height = int(clipa.height / 2)

    scaled_width = get_w(height, mod=1)

    diff = Catrom.scale(
        clipa.std.MakeDiff(clipb), scaled_width * 2, height * 2
    ).text.FrameNum(8)

    resized = [
        Catrom.scale(clipa, scaled_width, height).text.Text("Clip A", 3),
        Catrom.scale(clipb, scaled_width, height).text.Text("Clip B", 1),
    ]

    return Stack([Stack(resized).clip, diff], direction=Direction.VERTICAL).clip


@overload
def find_diff(
    *clips: vs.VideoNode,
    thr: float = ...,
    height: int = ...,
    interleave: bool = ...,
    return_ranges: Literal[True] = True,
    avg_thr: float | Literal[True] = True,
    exclusion_ranges: Sequence[int | tuple[int, int]] | None = ...,
    diff_func: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] = ...,
    msg: str = ...,
    plane: int = ...,
    **namedclips: vs.VideoNode,
) -> tuple[vs.VideoNode, list[tuple[int, int]]]:
    ...


@overload
def find_diff(
    *clips: vs.VideoNode,
    thr: float = ...,
    height: int = ...,
    interleave: bool = ...,
    return_ranges: Literal[False],
    avg_thr: float | Literal[True] = True,
    exclusion_ranges: Sequence[int | tuple[int, int]] | None = ...,
    diff_func: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] = ...,
    msg: str = ...,
    plane: int = ...,
    **namedclips: vs.VideoNode,
) -> vs.VideoNode:
    ...


def find_diff(
    *clips: vs.VideoNode,
    thr: float = 96,
    height: int = 288,
    interleave: bool = False,
    return_ranges: bool = False,
    avg_thr: float | Literal[True] = True,
    exclusion_ranges: Sequence[int | tuple[int, int]] | None = None,
    diff_func: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] = lambda a,
    b: core.std.MakeDiff(a, b),
    msg: str = "Diffing clips...",
    plane: int = 0,
    **namedclips: vs.VideoNode,
) -> vs.VideoNode | tuple[vs.VideoNode, list[tuple[int, int]]]:
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
    :param avg_thr:             Threshold of additional average diff check.
                                True to automatically calculate based on thr.
    :param exclusion_ranges:    Excludes a list of frame ranges from difference checking output (but not processing).
    :param diff_func:           Function for calculating diff in PlaneStatsMin/Max mode.
    :param msg:                 Message for the progress bar. Defaults to "Diffing clips...".
                                Useful if you're using `diff` for some other process.
    :param plane:               Plane to diff. Defaults to luma.

    :return:                    Either an interleaved clip of the differences between the two clips
                                or a stack of both input clips on top of MakeDiff clip.
                                Furthermore, the function will print the ranges of all the diffs found.

    :raises ClipsAndNamedClipsError: Both positional and named clips are given.
    :raises ValueError:         More or less than two clips are given.
    :raises ValueError:         ``thr`` is 128 or higher.
    :raises VariableFormatError: One of the clips is of a variable format.
    :raises LengthMismatchError: The given clips are of different lengths.
    :raises StopIteration:      No differences are found.
    """

    from vstools import plane as vst_plane

    if clips and namedclips:
        raise ClipsAndNamedClipsError(find_diff)

    if (clips and len(clips) != 2) or (namedclips and len(namedclips) != 2):
        raise CustomValueError("Must pass exactly 2 `clips` or `namedclips`!", find_diff)

    if abs(thr) > 128:
        raise CustomValueError("`thr` must be between [-128, 128]!", find_diff, thr)
    if avg_thr is True:
        avg_thr = max(0.012, (128 - thr) * 0.000046875 + 0.0105) if thr > 1 else 0.0

    if clips and not all([c.format for c in clips]):
        raise VariableFormatError(find_diff)
    elif namedclips and not all([nc.format for nc in namedclips.values()]):  # noqa
        raise VariableFormatError(find_diff)

    def _to_ranges(iterable: list[int]) -> Iterable[tuple[int, int]]:
        iterable = sorted(set(iterable))
        for _, group in groupby(enumerate(iterable), lambda t: t[1] - t[0]):
            groupl = list(group)
            yield groupl[0][1], groupl[-1][1]

    if clips:
        a, b = (
            depth(vst_plane(clips[0], plane), 8),
            depth(vst_plane(clips[1], plane), 8),
        )
    elif namedclips:
        nc = list(namedclips.values())
        a, b = depth(vst_plane(nc[0], plane), 8), depth(vst_plane(nc[1], plane), 8)

    assert isinstance(a, vs.VideoNode)
    assert isinstance(b, vs.VideoNode)

    LengthMismatchError.check(find_diff, a.num_frames, b.num_frames)

    callbacks = []

    if thr <= 1:
        callbacks.append(lambda f: get_prop(f, "PlaneStatsDiff", float) > thr)

        diff_clip = merge_clip_props(a.std.MakeDiff(b), a.std.PlaneStats(b))
    else:
        diff_clip = diff_func(a, b).std.PlaneStats()

        typ = (
            float
            if diff_clip.format and diff_clip.format.sample_type == vs.FLOAT
            else int
        )

        callbacks.append(
            lambda f: get_prop(f, "PlaneStatsMin", typ) <= thr
            or get_prop(f, "PlaneStatsMax", typ) >= 255 - thr > thr
        )

        if avg_thr > 0.0:
            diff_clip = merge_clip_props(diff_clip, a.std.PlaneStats(b, None, "PAVG"))

            callbacks.append(lambda f: get_prop(f, "PAVGDiff", float) > avg_thr)

    frames_render = clip_async_render(
        diff_clip,
        None,
        msg,
        lambda n, f: Sentinel.check(n, any(cb(f) for cb in callbacks)),
    )

    frames = list(Sentinel.filter(frames_render))

    if not frames:
        raise CustomError["StopIteration"]("No differences found!", find_diff)  # type: ignore[index]

    frames.sort()

    if exclusion_ranges:
        r: list[int] = []
        for e in exclusion_ranges:
            if isinstance(e, int):
                e = (e, e)
            start, end = e[0], e[1] + 1
            r += list(range(start, end))
        frames = [f for f in frames if f not in r]

    if clips:
        name_a, name_b = "Clip A", "Clip B"
    else:
        name_a, name_b = namedclips.keys()

    if interleave:
        a, b = a.text.FrameNum(9), b.text.FrameNum(9)
        comparison = Interleave(
            {
                f"{name_a}": core.std.Splice([a[f] for f in frames]),
                f"{name_b}": core.std.Splice([b[f] for f in frames]),
            }
        ).clip
    else:
        comparison = diff_between_clips_stack(
            core.std.Splice([a[f] for f in frames]),
            core.std.Splice([b[f] for f in frames]),
            height
        )

    if return_ranges:
        return comparison, list(_to_ranges(frames))
    else:
        return comparison


def diff_between_clips_stack(clip_a: vs.VideoNode, clip_b: vs.VideoNode, height: int = 288) -> vs.VideoNode:

    if clip_a.format != clip_b.format:
        raise CustomValueError(
            f'Clips are not of the same format! {clip_a.format.name} != {clip_b.format.name}',
            diff_between_clips_stack,
        )

    if clip_a.num_frames != clip_b.num_frames:
        warnings.warn(
            'diff_between_clips_stack: "Clips are not of the same length! This function will only compare the frames that are present in both clips."',
            UserWarning,
        )

        if clip_a.num_frames > clip_b.num_frames:
            clip_a = clip_a[:clip_b.num_frames]
        else:
            clip_b = clip_b[:clip_a.num_frames]

    scaled_width = get_w(height, mod=1)

    diff_clip = core.std.MakeDiff(clip_a, clip_b)
    diff_clip = diff_clip.resize.Bicubic(width=scaled_width * 2, height=height * 2).text.FrameNum(9)

    a, b = (
        c.resize.Spline36(width=scaled_width, height=height).text.FrameNum(9)
        for c in (clip_a, clip_b)
    )

    diff_stack = Stack({ "Clip A": a, "Clip B": b }).clip
    diff_clip = diff_clip.text.Text(text="diff", alignment=8)

    return Stack((diff_stack, diff_clip), direction=Direction.VERTICAL).clip


def comparison_shots(
    *clips: vs.VideoNode,
    left: int = 0,
    right: int = 0,
    top: int = 0,
    bottom: int = 0,
    height: int | None = None,
    kernel: KernelT = Point,
    **namedclips: vs.VideoNode,
) -> vs.VideoNode:
    """
    Convenience function that crops all the given clips, optionally upscales them,
    and stacks them to allow the user to see multiple filters side-by-side.

    This is intended more so to create comparisons to use in guides, papers,
    maybe an example to stick in a cheeky comment somewhere. Current name pending™.
    Alias for this function is ``lvsfunc.cshots``.

    I suggest you get the crops using vspreview's built-in crop helper (found under `misc`).
    You can then pass the left/right/top/bottom arguments to this function.
    If the crops result in a very small image, you can upscale it using `height`.

    :param clips:       Clips for comparison (order is kept left to right).
    :param namedclips:  Keyword arguments of `name=clip` for all clips in the comparison.
                        Clips will be labeled at the top left with their `name`.
    :param left:        Left crop. Can't be negative.
    :param right:       Right crop. Can't be negative.
    :param top:         Top crop. Can't be negative.
    :param bottom:      Bottom crop. Can't be negative.
    :param height:      Height to upscale the clips to. If `None`, do not upscale.
                        If equal to or lesser than 10, multiply the height by the given amount.
                        Default: None.
    :param kernel:      Kernel used for upscaling the clips if applicable. Default: Point.

    :return:            A horizontal stack of the `clips`/`namedclips`, cropped and upscaled as specified.

    :raises ClipsAndNamedClipsError:    Both positional and named clips are given.
    """

    if clips and namedclips:
        raise ClipsAndNamedClipsError(comparison_shots)

    kernel = Kernel.ensure_obj(kernel, comparison_shots)

    if clips:
        clips = tuple([c.std.Crop(left, right, top, bottom) for c in clips])
    elif namedclips:
        namedclips = {
            k: v.std.Crop(left, right, top, bottom) for k, v in namedclips.items()
        }

    if height is None:
        return Stack(
            clips if clips else namedclips, direction=Direction.HORIZONTAL
        ).clip
    elif height <= 10:
        height = mod2(clips[0].height * height)

    if clips:
        clips = tuple([kernel.scale(c, get_w(height), height) for c in clips])
    elif namedclips:
        namedclips = {
            k: kernel.scale(v, get_w(height), height) for k, v in namedclips.items()
        }

    return Stack(clips if clips else namedclips, direction=Direction.HORIZONTAL).clip


@overload
def diff(
    *clips: vs.VideoNode,
    thr: float = ...,
    height: int = ...,
    interleave: bool = ...,
    return_ranges: Literal[True] = True,
    avg_thr: float | Literal[True] = True,
    exclusion_ranges: Sequence[int | tuple[int, int]] | None = ...,
    diff_func: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] = ...,
    msg: str = ...,
    plane: int = ...,
    **namedclips: vs.VideoNode,
) -> tuple[vs.VideoNode, list[tuple[int, int]]]:
    ...


@overload
def diff(
    *clips: vs.VideoNode,
    thr: float = ...,
    height: int = ...,
    interleave: bool = ...,
    return_ranges: Literal[False],
    avg_thr: float | Literal[True] = True,
    exclusion_ranges: Sequence[int | tuple[int, int]] | None = ...,
    diff_func: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] = ...,
    msg: str = ...,
    plane: int = ...,
    **namedclips: vs.VideoNode,
) -> vs.VideoNode:
    ...


def diff(
    *clips: vs.VideoNode,
    thr: float = 96,
    height: int = 288,
    interleave: bool = False,
    return_ranges: bool = False,
    avg_thr: float | Literal[True] = True,
    exclusion_ranges: Sequence[int | tuple[int, int]] | None = None,
    diff_func: Callable[[vs.VideoNode, vs.VideoNode], vs.VideoNode] = lambda a,
    b: core.std.MakeDiff(a, b),
    msg: str = "Diffing clips...",
    plane: int = 0,
    **namedclips: vs.VideoNode,
) -> vs.VideoNode | tuple[vs.VideoNode, list[tuple[int, int]]]:
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
    :param avg_thr:             Threshold of additional average diff check.
                                True to automatically calculate based on thr.
    :param exclusion_ranges:    Excludes a list of frame ranges from difference checking output (but not processing).
    :param diff_func:           Function for calculating diff in PlaneStatsMin/Max mode.
    :param msg:                 Message for the progress bar. Defaults to "Diffing clips...".
                                Useful if you're using `diff` for some other process.
    :param plane:               Plane to diff. Defaults to luma.

    :return:                    Either an interleaved clip of the differences between the two clips
                                or a stack of both input clips on top of MakeDiff clip.
                                Furthermore, the function will print the ranges of all the diffs found.

    :raises ClipsAndNamedClipsError: Both positional and named clips are given.
    :raises ValueError:         More or less than two clips are given.
    :raises ValueError:         ``thr`` is 128 or higher.
    :raises VariableFormatError: One of the clips is of a variable format.
    :raises LengthMismatchError: The given clips are of different lengths.
    :raises StopIteration:      No differences are found.
    """

    import warnings

    warnings.warn('`diff` is deprecated, use `find_diff` instead!', DeprecationWarning)

    return find_diff(
        *clips, thr=thr, height=height, interleave=interleave, return_ranges=return_ranges, avg_thr=avg_thr,
        exclusion_ranges=exclusion_ranges,diff_func=diff_func, msg=msg, plane=plane, **namedclips
    )
