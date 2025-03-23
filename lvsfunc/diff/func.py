from __future__ import annotations

import warnings
from itertools import groupby
from typing import Iterable, Sequence, TypeVar

from vskernels import Bicubic
from vsrgtools import box_blur
from vstools import (CustomError, CustomValueError, FrameRangesN, FuncExceptT,
                     PlanesT, Sentinel, VSFunctionNoArgs, check_ref_clip,
                     clip_async_render, core, merge_clip_props,
                     normalize_franges, vs)

from .enum import DiffMode
from .strategies import DiffStrategy, PlaneAvgDiff
from .types import CallbacksT


class FindDiff:
    """Find the differences between two clips."""

    strategies: list[DiffStrategy]
    """List of diff strategies to use for comparison."""

    pre_process: VSFunctionNoArgs | bool
    """Pre-processing function or flag indicating whether to use default pre-processing."""

    exclusion_ranges: FrameRangesN
    """Ranges of frames to exclude from the comparison."""

    planes: PlanesT
    """Planes to consider in the comparison."""

    diff_clips: list[vs.VideoNode]
    """List of difference clips generated during comparison."""

    callbacks: CallbacksT
    """List of callback functions for each comparison method."""

    def __init__(
        self,
        strategies: DiffStrategy | Sequence[DiffStrategy] = [PlaneAvgDiff],
        mode: DiffMode = DiffMode.ANY,
        pre_process: VSFunctionNoArgs | bool = True,
        exclusion_ranges: Sequence[int | tuple[int, int]] | None = None,
        func_except: FuncExceptT | None = None
    ) -> None:
        """
        Find differences between two clips using various comparison methods.

        This class is useful for:

            - Identifying frames that differ significantly between two versions of a video
            - Detecting scene changes or cuts
            - Comparing IVTC patterns between different IVTC'd sources

        Example usage:

        .. code-block:: python

            from lvsfunc import DiffMode, FindDiff, PlaneAvgDiff

            # Assume clip_a and clip_b are your input clips
            diff_finder = FindDiff(
                strategies=PlaneAvgDiff(0.005, planes=0),
            ).get_diff(clip_a, clip_b)

        Custom preprocessing example:

        .. code-block:: python

            # Crop the borders of the clips before processing.
            diff_finder = FindDiff(
                pre_process=lambda c: c.std.Crop(top=10, bottom=10, left=10, right=10)
            ).get_diff(clip_a, clip_b)

        :param strategies:          The strategy or strategies to use for comparison.
                                    See each strategy's class documentation for more information.
                                    Default: PlaneAvgDiff.
        :param mode:                The mode to use for combining results from multiple strategies.
                                    Default: DiffMode.ANY.
        :param pre_process:         The pre-processing function to use for the comparison.
                                    If True, use box_blur. If False, skip pre-processing.
                                    Default: True.
        :param exclusion_ranges:    Ranges to exclude from the comparison.
                                    These frames will still be processed, but not outputted.
        :param func_except:         The function exception to use for the comparison.
        """

        self._func_except = func_except or self.__class__.__name__
        self.mode = DiffMode(mode)

        self.strategies = [strategies] if not isinstance(strategies, Sequence) else list(strategies)

        if not self.strategies:
            raise CustomValueError('You must pass at least one strategy!', self._func_except)

        self.pre_process = pre_process if callable(pre_process) else (box_blur if pre_process is True else None)

        self.exclusion_ranges = exclusion_ranges or []

        self._diff_frames: list[int] | None = None
        self._diff_ranges: list[tuple[int, int]] | None = None
        self._processed_clip: vs.VideoNode | None = None

    def get_diff(
        self: TFindDiff,
        src: vs.VideoNode, ref: vs.VideoNode,
        names: tuple[str, str] = ('src', 'ref')
    ) -> vs.VideoNode:
        """
        Get a processed clip highlighting the differences between two clips.

        :param clip_a:          The source clip to compare.
        :param clip_b:          The reference clip to compare.
        :param diff_height:     The height of each output clip (diff will be double this height).
                                Default: 288.
        :param names:           The names of the clips. Default: ('Src', 'Ref').

        :return:                A clip highlighting the differences between the source and reference clips.
        """

        src, ref = self._validate_inputs(src, ref)
        prep_src, prep_ref = self._prepare_clips(src, ref)

        self._process(prep_src, prep_ref)

        if not isinstance(names, tuple):
            names = (names, names)
        elif len(names) != 2:
            raise CustomValueError("Names must be a tuple of two strings!", self.get_diff_clip, names)

        diff_clip = core.std.MakeDiff(src, ref).text.FrameNum(9)

        a, b = (Bicubic.scale(c, width=c.width // 2, height=c.height // 2) for c in (src, ref))
        a = merge_clip_props(a, self._processed_clip)

        stack_srcref = core.std.StackHorizontal([
            a.text.Text(names[0], 7), b.text.Text(names[1], 7),
        ])

        stack_diff = core.std.StackVertical([
            stack_srcref, diff_clip.text.Text(text='Differences found:', alignment=8),
        ])

        out_diff = core.std.Splice([stack_diff[f] for f in self._diff_frames])

        return out_diff.std.SetFrameProps(fd_diffRanges=str(self._diff_ranges))

    def _validate_inputs(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, vs.VideoNode]:
        check_ref_clip(src, ref, self._func_except)

        if src.num_frames == ref.num_frames:
            return src, ref

        warnings.warn(
            f"{self._func_except}: 'The number of frames of the clips don't match! "
            f"({src.num_frames=}, {ref.num_frames=})\n"
            "The function will still work, but your clips may be synced incorrectly!'"
        )

        min_frames = min(src.num_frames, ref.num_frames)
        return src[:min_frames], ref[:min_frames]

    def _prepare_clips(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, vs.VideoNode]:
        if callable(self.pre_process):
            return self.pre_process(src), self.pre_process(ref)

        return src, ref

    def _process(self, src: vs.VideoNode, ref: vs.VideoNode) -> None:
        self._processed_clip = src

        callbacks: CallbacksT = []

        for strategy in self.strategies:
            if not isinstance(strategy, DiffStrategy):
                strategy = strategy()

            processed_clip, cb = strategy.process(src=self._processed_clip, ref=ref)
            self._processed_clip = processed_clip
            callbacks += cb

        self._find_frames(callbacks)

    def _find_frames(self, callbacks: CallbacksT) -> None:
        """Get the frames that are different between two clips."""

        assert isinstance(self._processed_clip, vs.VideoNode)

        frames_render = clip_async_render(
            self._processed_clip, None, "Finding differences between clips...",
            lambda n, f: Sentinel.check(n, self.mode.check_result([cb(f) for cb in callbacks])),
        )

        self._diff_frames = list(Sentinel.filter(frames_render))

        if not self._diff_frames:
            raise CustomError['StopIteration']('No differences found!', self._func_except)  # type: ignore[index]

        self._diff_frames.sort()

        if self.exclusion_ranges:
            excluded = set(
                frame
                for range_ in normalize_franges(self.exclusion_ranges)
                for frame in range(range_[0], range_[-1] + 1)
            )

            self._diff_frames = [f for f in self._diff_frames if f not in excluded]

        self._diff_ranges = list(self._to_ranges(self._diff_frames))

    @staticmethod
    def _to_ranges(iterable: list[int]) -> Iterable[tuple[int, int]]:
        iterable = sorted(set(iterable))

        for _, group in groupby(enumerate(iterable), lambda t: t[1] - t[0]):
            groupl = list(group)
            yield groupl[0][1], groupl[-1][1]


TFindDiff = TypeVar('TFindDiff', bound='FindDiff')
