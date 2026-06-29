from __future__ import annotations

import math
import random
import warnings
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Sequence
from itertools import zip_longest
from typing import Any

from jetpytools import CustomIntEnum, CustomNotImplementedError, CustomTypeError, CustomValueError, mod2
from typing_extensions import deprecated
from vskernels import Catrom, Kernel, KernelLike, Point
from vstools import (
    FormatsMismatchError,
    LengthMismatchError,
    Matrix,
    MismatchRefError,
    UnsupportedSubsamplingError,
    check_variable_format,
    check_variable_resolution,
    core,
    get_subsampling,
    get_w,
    vs,
)

from .exceptions import ClipsAndNamedClipsError

__all__ = [
    "Comparer",
    "Direction",
    "Interleave",
    "Split",
    "Stack",
    "Tile",
    "compare",
    "comparison_shots",
    "diff_between_clips_stack",
    "stack_compare",
]


class Direction(CustomIntEnum):
    """Enum to simplify the direction argument."""

    HORIZONTAL = 0
    VERTICAL = 1

    LEFT = 2
    RIGHT = 3
    UP = 4
    DOWN = 5

    @property
    def is_axis(self) -> bool:
        """Whether the Direction represents an axis (horizontal/vertical)."""

        return self <= self.VERTICAL

    @property
    def is_way(self) -> bool:
        """Whether the Direction is one of the 4 arrow directions."""

        return self > self.VERTICAL

    @property
    def string(self) -> str:
        """A string representation of the Direction."""

        return self._name_.lower()


class Comparer(ABC):
    """
    Base class for comparison functions.

    Args:
        clips: A dict mapping names to clips, or a sequence of clips in a tuple or list.
            If given a dict, the names will be overlaid on the clips using
            :py:func:`vapoursynth.core.text.Text`.
            If given a simple sequence of clips, ``label_alignment`` has no effect and the clips
            will not be labeled.
            The order of the clips in either a dict or a sequence will be kept in the comparison.
        label_alignment: An integer from 1–9, corresponding to the positions of the keys on a numpad.
            Only used if ``clips`` is a dict.
            Determines where to place clip names using :py:func:`vapoursynth.core.text.Text`.
            Default: 7.

    Raises:
        ValueError: Fewer than two clips were passed, or ``label_alignment`` is not between 1–9.
        TypeError: Unexpected type passed to ``clips``.
    """

    def __init__(
        self,
        clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /,
        *,
        label_alignment: int = 7,
    ) -> None:
        if len(clips) < 2:
            raise CustomValueError("Compare functions must be used on at least 2 clips!", self.__class__)

        if label_alignment not in list(range(1, 10)):
            raise CustomValueError("`label_alignment` must be an integer from 1 to 9!", self.__class__)

        if not isinstance(clips, (dict, Sequence)):
            raise CustomTypeError(f"Unexpected type {type(clips)} for `clips` argument!", self.__class__)

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
        """If a `name` consists of only whitespace characters, `'   '`, for example, omit it."""

        if self.names:
            return [
                clip.text.Text(text=name, alignment=self.label_alignment) if name.strip() else clip
                for clip, name in zip(self.clips, self.names)
            ]

        return self.clips.copy()

    @abstractmethod
    def _compare(self) -> vs.VideoNode:
        raise CustomNotImplementedError("This function or method has not been implemented yet!", self.__class__)

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

    Acts as a convenience combination of :py:func:`vapoursynth.core.text.Text`
    and either :py:func:`vapoursynth.core.std.StackHorizontal`
    or :py:func:`vapoursynth.core.std.StackVertical`.

    Args:
        clips: See :class:`Comparer`.
        direction: Stack direction. Default: ``Direction.HORIZONTAL``.
        label_alignment: See :class:`Comparer`.

    Raises:
        ValueError: Clips lack a common height (horizontal stack) or width (vertical stack).
    """

    def __init__(
        self,
        clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /,
        *,
        direction: Direction = Direction.HORIZONTAL,
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
                (x.width for x in self.clips),
            )

        return core.std.StackVertical(self._marked_clips())

    @classmethod
    def stack(cls, *clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
        """
        Stack clips horizontally.

        Args:
            clips: See :class:`Comparer`.
            namedclips: See :class:`Comparer`.

        Returns:
            A horizontally stacked clip.

        Raises:
            ClipsAndNamedClipsError: Both positional and named clips are given.
        """

        if clips and namedclips:
            raise ClipsAndNamedClipsError(cls.stack)

        return cls(clips or namedclips).clip

    @classmethod
    def stack_vertical(cls, *clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
        """
        Stack clips vertically.

        Args:
            clips: See :class:`Comparer`.
            namedclips: See :class:`Comparer`.

        Returns:
            A vertically stacked clip.

        Raises:
            ClipsAndNamedClipsError: Both positional and named clips are given.
        """

        if clips and namedclips:
            raise ClipsAndNamedClipsError(cls.stack)

        return cls(clips or namedclips, direction=Direction.VERTICAL).clip


class Interleave(Comparer):
    """
    Interleave frames from the given clips.

    For example, ``Interleave(A=clip1, B=clip2)`` will return
    ``A.Frame 0, B.Frame 0, A.Frame 1, B.Frame 1, ...``.

    Acts as a convenience combination of :py:func:`vapoursynth.core.text.Text`
    and :py:func:`vapoursynth.core.std.Interleave`.

    Args:
        clips: A dict mapping names to clips, or a sequence of clips in a tuple or list.
            If a dict is passed, the keys' names are overlaid on the clips using :py:func:`vapoursynth.core.text.Text`.
            If a sequence is passed, ``label_alignment`` has no effect and the clips are not labeled.
            The order of the clips is preserved.
        label_alignment: An integer from 1–9, corresponding to the positions of the keys on a numpad.
            Only used if ``clips`` is a dict. Determines where to place clip name using
            :py:func:`vapoursynth.core.text.Text`. Default: ``7``.
    """

    def __init__(
        self,
        clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /,
        *,
        label_alignment: int = 7,
    ) -> None:
        super().__init__(clips, label_alignment=label_alignment)

    def _compare(self) -> vs.VideoNode:
        return core.std.Interleave(self._marked_clips(), extend=True, mismatch=True)


class Tile(Comparer):
    """
    Tiles clips in a mosaic manner, filling rows first left-to-right, then stacking.

    The arrangement of the clips can be specified with the ``arrangement`` parameter.
    Rows are specified as lists of ints within a larger list that specifies row order.
    Think of this as a 2D array of ``0`` and ``1`` values, where ``0`` represents an empty slot
    and ``1`` represents the next clip in the sequence.

    If ``arrangement`` is not specified, the function will attempt to fill a square with
    dimensions ``n x n``, where ``n`` is ``1 + math.isqrt(len(clips) - 1)``.
    The bottom rows will be dropped if empty.

    Example auto-layouts:

    .. code-block:: text

        # For 3 clips:
        [
            [1, 1],
            [1, 0],
        ]

        # For 10 clips:
        [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 0, 0],
        ]

        # Custom arrangement (4 clips); remaining rows are automatically padded with 0s:
        [
            [0, 1, 0, 1],
            [1],
            [0, 1],
        ]

    Args:
        clips: See :class:`Comparer`.
        arrangement: 2D array of ``0`` and ``1`` values representing blank spaces and clips per row.
            Default: ``None`` (auto-square layout).
        label_alignment: See :class:`Comparer`.

    Raises:
        ValueError: Clip heights and widths don't match.
        ValueError: Array is one-dimensional; use :class:`Stack` instead.
        ValueError: Specified arrangement has an invalid number of clips.
    """

    def __init__(
        self,
        clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /,
        *,
        arrangement: list[list[int]] | None = None,
        label_alignment: int = 7,
    ) -> None:
        super().__init__(clips, label_alignment=label_alignment)

        if not self.width or not self.height:
            raise CustomValueError("All clip widths and heights must be the same!", self.__class__)

        if arrangement is None:
            self.arrangement = self._auto_arrangement()
        else:
            is_one_dim = len(arrangement) < 2 or all(len(row) == 1 for row in arrangement)
            if is_one_dim:
                raise CustomValueError("Use Stack instead if the array is one dimensional!", self.__class__)
            self.arrangement = arrangement

        self.blank_clip = core.std.BlankClip(clip=self.clips[0], keep=1)

        max_length = max(map(len, self.arrangement))

        self.arrangement = [row + [0] * (max_length - len(row)) for row in self.arrangement]

        array_count = sum(map(sum, self.arrangement))

        LengthMismatchError.check(
            self.__class__,
            array_count,
            self.num_clips,
            message="Specified arrangement has an invalid number of clips!",
        )

    def _compare(self) -> vs.VideoNode:
        clips = self._marked_clips()

        rows = [
            core.std.StackHorizontal([clips.pop(0) if elem else self.blank_clip for elem in row])
            for row in self.arrangement
        ]

        return core.std.StackVertical(rows)

    def _auto_arrangement(self) -> list[list[int]]:
        def _grouper(iterable: Iterable[Any], n: int, fillvalue: Any | None = None) -> Iterator[tuple[Any, ...]]:
            args = [iter(iterable)] * n
            return zip_longest(*args, fillvalue=fillvalue)

        dimension = 1 + math.isqrt(self.num_clips - 1)

        return [list(x) for x in _grouper([1] * self.num_clips, dimension, 0)]


class Split(Stack):
    """
    Split an unlimited amount of clips into one VideoNode with the same dimensions as the
    original clips.

    Handles odd-sized resolutions or resolutions that can't be evenly split by the amount of
    clips specified.

    The remaining pixel width/height (``clip.dimension % number_of_clips``)
    will always be given to the last clip specified.
    For example, five ``104 x 200`` clips will result in a
    ``((20 x 200) * 4) + (24 x 200)`` horizontal stack of clips.

    Horizontal split layout (five ``104 x 200`` clips):

    .. code-block:: text

        original frame (104px wide)

        ┌──────────────────────────────────┐
        │                                  │
        │            104 x 200             │
        │                                  │
        └──────────────────────────────────┘

                          |
                          v

        ┌──────┬──────┬──────┬──────┬──────┐
        │  1   │  2   │  3   │  4   │  5   │   stacked side-by-side
        │ (20) │ (20) │ (20) │ (20) │ (24) │   px wide per slice
        └──────┴──────┴──────┴──────┴──────┘

            remainder width goes to the last clip

    Args:
        clips: See :class:`Comparer`.
        direction: Axis to split on. Default: ``Direction.HORIZONTAL``.
        label_alignment: See :class:`Comparer`.

    Raises:
        ValueError: Clip heights and widths don't match.
        UnsupportedSubsamplingError: Resulting cropped width or height violates subsampling rules.
    """

    def __init__(
        self,
        clips: dict[str, vs.VideoNode] | Sequence[vs.VideoNode],
        /,
        *,
        direction: Direction = Direction.HORIZONTAL,
        label_alignment: int = 7,
    ) -> None:
        super().__init__(clips, direction=direction, label_alignment=label_alignment)

        self._smart_crop()

    def _smart_crop(
        self,
    ) -> None:  # has to alter self.clips to send clips to _marked_clips() in Stack's _compare()
        """Crops self.clips in place accounting for odd resolutions."""

        if not self.width or not self.height:
            raise CustomValueError("All clips must have same width and height!", self.__class__)

        breaks_subsampling = (
            self.direction == Direction.HORIZONTAL
            and (((self.width // self.num_clips) % 2) or ((self.width % self.num_clips) % 2))
        ) or (
            self.direction == Direction.VERTICAL
            and (((self.height // self.num_clips) % 2) or ((self.height % self.num_clips) % 2))
        )

        is_subsampled = not all(get_subsampling(clip) in ("444", None) for clip in self.clips)

        if breaks_subsampling and is_subsampled:
            raise UnsupportedSubsamplingError(
                self.__class__.__name__,
                self.clips,
                correct=(vs.YUV444P8, vs.RGB24),
                message="Resulting cropped width or height violates subsampling rules! "
                "Consider resampling to YUV444 or RGB before attempting to crop!",
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

            case _:
                raise CustomValueError("Unknown direction", self.__class__)

    @classmethod
    def stack(cls, *clips: vs.VideoNode, **namedclips: vs.VideoNode) -> vs.VideoNode:
        if clips and namedclips:
            raise ClipsAndNamedClipsError(cls.stack)

        return cls(clips or namedclips, label_alignment=2).clip


def compare(
    clip_a: vs.VideoNode,
    clip_b: vs.VideoNode,
    frames: list[int] | None = None,
    rand_total: int | None = None,
    force_resample: bool = True,
    print_frame: bool = True,
    mismatch: bool = False,
) -> vs.VideoNode:
    """
    Compare the same frames from two different clips by interleaving them into a single clip.

    Clips are automatically resampled to 8 bit YUV -> RGB24 to emulate how a monitor shows the frame.
    This can be disabled by setting ``force_resample`` to ``False``.

    This is not recommended over setting multiple outputs and checking between those,
    but in the event that is unavailable to you, this function may be useful.

    Alias for this function is ``lvsfunc.comp``.

    Args:
        clip_a: Clip to compare.
        clip_b: Second clip to compare.
        frames: List of frames to compare. Default: ``None``.
        rand_total: Number of random frames to pick. Default: ``None``.
        force_resample: Forcibly resamples the clips to RGB24. Default: ``True``.
        print_frame: Print frame numbers. Default: ``True``.
        mismatch: Allow clips with different formats and dimensions to be compared.
            Default: ``False``.

    Returns:
        Interleaved clip containing specified frames from ``clip_a`` and ``clip_b``.

    Raises:
        VariableResolutionError: One of the given clips has variable resolution.
        ValueError: More comparisons were requested than frames are available.
        VariableFormatError: ``mismatch`` is ``False`` and one of the clips has variable format.
        FormatsMismatchError: ``mismatch`` is ``False`` and the clip formats differ.
    """

    def _resample(clip: vs.VideoNode) -> vs.VideoNode:
        # Resampling to 8 bit and RGB to properly display how it appears on your screen
        return Catrom().resample(clip, vs.RGB24, None, Matrix.from_video(clip), dither_type="error_diffusion")

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
            rand_total = int(clip_a.num_frames / 1000) if clip_a.num_frames > 5000 else int(clip_a.num_frames / 100)

        frames = sorted(random.sample(range(1, clip_a.num_frames - 1), rand_total))

    frames_a = core.std.Splice([clip_a[f] for f in frames]).std.AssumeFPS(fpsnum=1, fpsden=1)
    frames_b = core.std.Splice([clip_b[f] for f in frames]).std.AssumeFPS(fpsnum=1, fpsden=1)

    return core.std.Interleave([frames_a, frames_b], mismatch=mismatch)


def stack_compare(
    *clips: vs.VideoNode,
    height: int | None = None,
    kernel: KernelLike = Catrom,
    **namedclips: vs.VideoNode,
) -> vs.VideoNode:
    """
    Compare two clips by stacking them with a diff clip underneath.

    ┌─────────────┬─────────────┐
    │  clip A     │  clip B     │  <- scaled to `scaled_width x height`
    ├─────────────┴─────────────┤
    │       Difference clip     │  <- scaled to `scaled_width x 2 x height x 2`
    │                           │
    └───────────────────────────┘

    Best to use when trying to match two sources frame-accurately.

    Args:
        clips: Two clips to compare, passed positionally.
        height: Height in px for the source clips. The diff clip uses twice this resolution.
            Default: 288.
        kernel: Kernel used to scale the source clips. The diff always uses Catrom.
        namedclips: Two clips as keyword arguments; names are used as labels. Only used when
            ``clips`` is not given.

    Returns:
        Clip with the sources stacked above a difference clip.

    Raises:
        ClipsAndNamedClipsError: Both positional and named clips are given.
        ValueError: Fewer or more than two clips are given.
        MismatchRefError: The clips do not share the same format.
    """

    if clips and namedclips:
        raise ClipsAndNamedClipsError(stack_compare)

    if clips:
        if len(clips) != 2:
            raise CustomValueError("Must pass exactly 2 clips!", stack_compare)

        clip_a, clip_b = clips
        name_a, name_b = "Clip A", "Clip B"
    elif namedclips:
        if len(namedclips) != 2:
            raise CustomValueError("Must pass exactly 2 named clips!", stack_compare)

        name_a, name_b = tuple(namedclips.keys())
        clip_a, clip_b = tuple(namedclips.values())
    else:
        raise CustomValueError("Must pass exactly 2 clips!", stack_compare)

    MismatchRefError.check(stack_compare, clip_a, clip_b)

    if not height:
        height = 288

    if height > clip_a.height / 2:
        warnings.warn(
            f"stack_compare: Given 'height' ({height}) is bigger than the first clip's height ({clip_a.height})! "
            "Will be using half the clip height instead.",
            UserWarning,
            stacklevel=2,
        )

        height = int(clip_a.height / 2)

    scaler = Kernel.ensure_obj(kernel, stack_compare)
    scaled_width = get_w(height, mod=1)

    diff_clip = Catrom().scale(clip_a.std.MakeDiff(clip_b), scaled_width * 2, height * 2).text.FrameNum(9)
    diff_clip = diff_clip.text.Text(text="Difference", alignment=8)

    scaled = [scaler.scale(clip, scaled_width, height).text.FrameNum(9) for clip in (clip_a, clip_b)]

    return Stack(
        (
            Stack({name_a: scaled[0], name_b: scaled[1]}).clip,
            diff_clip,
        ),
        direction=Direction.VERTICAL,
    ).clip


@deprecated("Use stack_compare instead.", category=DeprecationWarning, stacklevel=2)
def diff_between_clips_stack(*clips: vs.VideoNode, height: int = 288, **namedclips: vs.VideoNode) -> vs.VideoNode:
    """
    Make a stacked diff between two clips.

    .. deprecated:: Use :py:func:`stack_compare` instead.
    """

    if clips:
        return stack_compare(*clips, height=height)

    return stack_compare(height=height, **namedclips)  # type: ignore[arg-type]


def comparison_shots(
    *clips: vs.VideoNode,
    left: int = 0,
    right: int = 0,
    top: int = 0,
    bottom: int = 0,
    height: int | None = None,
    kernel: KernelLike = Point,
    **namedclips: vs.VideoNode,
) -> vs.VideoNode:
    """
    Convenience function that crops all the given clips, optionally upscales them,
    and stacks them to allow the user to see multiple filters side-by-side.

    This is intended more so to create comparisons to use in guides, papers,
    maybe an example to stick in a cheeky comment somewhere. Current name pending™.
    Alias for this function is ``lvsfunc.cshots``.

    I suggest you get the crops using vsview's built-in crop helper.
    You can then pass the ``left``/``right``/``top``/``bottom`` arguments to this function.
    If the crops result in a very small image, you can upscale it using ``height``.

    .. code-block:: text

        ┌────────┬────────┬────────┐
        │ clip A │ clip B │ clip C │   <- cropped, optionally upscaled
        └────────┴────────┴────────┘

    Args:
        clips: Clips for comparison (order is kept left to right).
        namedclips: Keyword arguments of ``name=clip`` for all clips in the comparison.
            Clips will be labeled at the top left with their name.
        left: Left crop. Can't be negative.
        right: Right crop. Can't be negative.
        top: Top crop. Can't be negative.
        bottom: Bottom crop. Can't be negative.
        height: Height to upscale the clips to. ``None`` does not upscale.
            If equal to or lesser than 10, multiply the height by the given amount.
            Default: ``None``.
        kernel: Kernel used for upscaling the clips if applicable. Default: Point.

    Returns:
        A horizontal stack of the ``clips``/``namedclips``, cropped and upscaled as specified.

    Raises:
        ClipsAndNamedClipsError: Both positional and named clips are given.
    """

    if clips and namedclips:
        raise ClipsAndNamedClipsError(comparison_shots)

    kernel = Kernel.ensure_obj(kernel, comparison_shots)

    if clips:
        clips = tuple([c.std.Crop(left, right, top, bottom) for c in clips])
    elif namedclips:
        namedclips = {k: v.std.Crop(left, right, top, bottom) for k, v in namedclips.items()}

    if height is None:
        return Stack(clips or namedclips, direction=Direction.HORIZONTAL).clip
    elif height <= 10:
        source = clips[0] if clips else next(iter(namedclips.values()))
        height = mod2(source.height * height)

    if clips:
        clips = tuple([kernel.scale(c, get_w(height), height) for c in clips])
    elif namedclips:
        namedclips = {k: kernel.scale(v, get_w(height), height) for k, v in namedclips.items()}

    return Stack(clips or namedclips, direction=Direction.HORIZONTAL).clip
