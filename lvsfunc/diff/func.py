from __future__ import annotations

import warnings
from itertools import groupby
from typing import Iterable, Literal, Self, Sequence, TypeVar

from jetpytools import (CustomRuntimeError, FileIsADirectoryError,
                        FilePermissionError, FileWasNotFoundError, SPath,
                        SPathLike)
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

    diff_ranges: FrameRangesN = []
    """Ranges of frames that are different between the two clips."""

    def __init__(
        self,
        strategies: DiffStrategy | Sequence[DiffStrategy] = [PlaneAvgDiff],
        mode: DiffMode = DiffMode.ANY,
        pre_process: VSFunctionNoArgs | Literal[False] = lambda x: box_blur(x).std.Crop(8, 8, 8, 8),
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

        :raise CustomValueError:    If you don't pass any strategies.
        """

        self._func_except = func_except or self.__class__.__name__
        self.mode = DiffMode(mode)

        self.strategies = [strategies] if not isinstance(strategies, Sequence) else list(strategies)

        if not self.strategies:
            raise CustomValueError('You must pass at least one strategy!', self._func_except)

        self.pre_process = pre_process if callable(pre_process) else None

        self.exclusion_ranges = exclusion_ranges or []

        self._diff_frames: list[int] | None = None
        self._processed_clip: vs.VideoNode | None = None

    def find_diff(
        self: TFindDiff,
        src: vs.VideoNode, ref: vs.VideoNode,
        force: bool = False
    ) -> Self:
        """
        Find the differences between two clips and store the results.

        The ranges will be accessible through the `diff_ranges` attribute.
        If you have already found the differences, the method will return the current instance,
        unless `force` is True, in which case the current results will be cleared.

        :param src:                     The source clip to compare.
        :param ref:                     The reference clip to compare.
        :param force:                   If True, force the method to find differences
                                        even if they have already been found.
                                        This will clear the current results.

        :return:                        The current instance of FindDiff.

        :raise CustomStopIteration:     If no differences are found.
        """

        if not force and self._diff_frames:
            return self

        self._diff_frames = None
        self.diff_ranges = []

        self._validate_inputs(src, ref)
        self._process(src, ref)

        return self

    def get_diff(
        self: TFindDiff,
        src: vs.VideoNode, ref: vs.VideoNode,
        names: tuple[str, str] = ('src', 'ref')
    ) -> vs.VideoNode:
        """
        Get a processed clip highlighting the differences between two clips.

        If you haven't run `find_diff` yet, the method will do so automatically.

        :param src:                     The source clip to compare.
        :param ref:                     The reference clip to compare.
        :param diff_height:             The height of each output clip (diff will be double this height).
                                        Default: 288.
        :param names:                   The names of the clips. Default: ('Src', 'Ref').

        :return:                        A clip highlighting the differences between the source and reference clips.

        :raise CustomStopIteration:     If no differences are found.
        :raise CustomValueError:        If `names` is not a tuple of two strings.
        """

        self.find_diff(src, ref)

        if not isinstance(names, tuple):
            names = ('src', 'ref')
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

        out_diff = self.get_clip_frames(stack_diff)

        return out_diff.std.SetFrameProps(fd_diffRanges=str(self.diff_ranges))

    def get_clip_frames(self, clip: vs.VideoNode) -> vs.VideoNode:
        """
        Get a clip of the frames that are different between the two clips.

        :param clip:                    The clip to get the frames from.

        :return:                        A clip of the frames that are different between the two clips.

        :raises CustomRuntimeError:     If you haven't run `find_diff` yet.
        """

        if not self._diff_frames:
            raise CustomRuntimeError(
                'You have not found the differences yet! Please run `find_diff` first.',
                self.get_clip_frames, self._diff_frames,
            )

        return core.std.Splice([clip[f] for f in self._diff_frames])

    def to_file(self, output_path: SPathLike) -> SPath:
        """
        Save the frame ranges to a file.

        Frames will be saved in the format:

        .. code-block:: text

            1-10
            21-30
            etc.

        :param output_path:             The path to save the differences to.

        :return:                        The path to the file.

        :raise CustomRuntimeError:      If you haven't run `find_diff` yet.
        :raise FileIsADirectoryError:   If the output path is a directory.
        :raise CustomRuntimeError:      If you don't have permission to write to the file.
        :raise CustomOSError:           If there's an OS error (disk full, invalid path, etc.).
        :raise CustomRuntimeError:      If there's an unexpected error.
        :raise FileWasNotFoundError:    If the file was not found after it was supposed to be written.
        """

        if not self.diff_ranges:
            raise CustomRuntimeError(
                'You have not found the differences yet! Please run `find_diff` first.',
                self.to_file, self.diff_ranges,
            )

        sfile = SPath(output_path)

        if sfile.is_dir():
            raise FileIsADirectoryError(
                'Failed to save frame ranges! Output path is a directory!',
                self.to_file, sfile,
            )

        franges = '\n'.join(f'{start}-{end}' for start, end in self.diff_ranges)

        try:
            sfile.write_text(franges)
        except PermissionError as e:
            raise FilePermissionError(
                'Failed to save frame ranges! Insufficient permissions!',
                self.to_file, e,
            )
        except OSError as e:
            raise CustomError['OSError'](
                'Failed to save frame ranges! OS error (disk full, invalid path, etc.)!',
                self.to_file, e,
            )
        except Exception as e:
            raise CustomRuntimeError(
                'Failed to save frame ranges!',
                self.to_file, e,
            )

        if not sfile.exists():
            raise FileWasNotFoundError(
                'Failed to save frame ranges! File was not found!',
                self.to_file, sfile,
            )

        return sfile

    def from_file(self, input_path: SPathLike) -> list[tuple[int, int]]:
        """
        Load the frame ranges from a file.

        The file must follow this format:

        .. code-block:: text

            1-10
            21-30
            etc.

        :param input_path:              The path to load the frame ranges from.

        :return:                        The frame ranges.

        :raise CustomValueError:        If the file is empty or the format is invalid.
        :raise FileWasNotFoundError:    If the file was not found.
        :raise FilePermissionError:     If you don't have permission to read the file.
        """

        sfile = SPath(input_path)

        if not sfile.exists():
            raise FileWasNotFoundError(
                'Failed to load frame ranges! File was not found!',
                self.from_file, sfile,
            )

        try:
            content = sfile.read_text()
        except PermissionError as e:
            raise FilePermissionError(
                'Failed to load frame ranges! Insufficient permissions!',
                self.from_file, e,
            )

        if not (content := content.strip()):
            raise CustomValueError(
                'Failed to load frame ranges! File is empty!',
                self.from_file, sfile,
            )

        for line in content.splitlines():
            if not (line := line.strip()):
                continue

            parts = line.split('-')

            if len(parts) != 2 or not all(x.strip().isdigit() for x in parts):
                raise CustomValueError(
                    'Failed to load frame ranges! Invalid format in file! Expected "start-end" per line.',
                    self.from_file, sfile,
                )

            start, end = map(int, parts)

            self.diff_ranges.append((start, end))

        return self.diff_ranges

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

        self.diff_ranges = list(self._to_ranges(self._diff_frames))

    @staticmethod
    def _to_ranges(iterable: list[int]) -> Iterable[tuple[int, int]]:
        iterable = sorted(set(iterable))

        for _, group in groupby(enumerate(iterable), lambda t: t[1] - t[0]):
            groupl = list(group)
            yield groupl[0][1], groupl[-1][1]


TFindDiff = TypeVar('TFindDiff', bound='FindDiff')
