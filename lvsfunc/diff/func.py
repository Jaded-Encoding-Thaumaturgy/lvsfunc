from __future__ import annotations

import warnings
from collections.abc import Callable, Iterable, Sequence
from itertools import groupby
from typing import Literal

from jetpytools import (
    CustomRuntimeError,
    CustomValueError,
    FileIsADirectoryError,
    FilePermissionError,
    FileWasNotFoundError,
    FuncExceptT,
    Sentinel,
    SPath,
    SPathLike,
)
from vskernels import Catrom
from vsrgtools import box_blur
from vstools import (
    FrameRangesN,
    PlanesT,
    VSFunctionNoArgs,
    check_ref_clip,
    clip_async_render,
    core,
    get_prop,
    merge_clip_props,
    normalize_ranges,
    vs,
)

from .enum import DiffMode
from .exceptions import CustomOSError, NoDifferencesFoundError
from .strategies import DiffStrategy, PlaneStatsDiff
from .types import CallbacksT

__all__: list[str] = [
    "FindDiff",
    "remove_isolated_frames",
]


def remove_isolated_frames(frames: Iterable[int], thr: int = 1) -> Iterable[int]:
    """
    Remove isolated frames (frames with no adjacent frames) from the list of frames.

    Args:
        frames: The list of frames to remove isolated frames from.
        thr: The number of frames to consider adjacent. Default: 1.

    Returns:
        The list of frames with isolated frames removed.
    """

    frames_set = set(frames)

    return [f for f in frames if (f - thr in frames_set) or (f + thr in frames_set)]


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

    diff_ranges: FrameRangesN
    """Ranges of frames that are different between the two clips."""

    def __init__(
        self,
        strategies: DiffStrategy | Sequence[DiffStrategy] | None = None,
        mode: DiffMode = DiffMode.ANY,
        pre_process: VSFunctionNoArgs | Literal[False] | None = (lambda clip: box_blur(clip).std.Crop(8, 8, 8, 8)),
        exclusion_ranges: FrameRangesN | None = None,
        func_except: FuncExceptT | None = None,
    ) -> None:
        """
        Find differences between two clips using various comparison methods.

        This class is useful for:

            - Identifying frames that differ significantly between two versions of a video
            - Detecting scene changes or cuts
            - Comparing IVTC patterns between different IVTC'd sources

        Example usage:

        .. code-block:: python

            from lvsfunc import DiffMode, FindDiff, PlaneAvgFloatDiff

            # Assume clip_a and clip_b are your input clips
            diff_finder = FindDiff(
                strategies=PlaneAvgFloatDiff(0.005, planes=0),
            ).get_diff(clip_a, clip_b)

        Custom preprocessing example:

        .. code-block:: python

            # Crop the borders of the clips before processing.
            diff_finder = FindDiff(
                pre_process=lambda c: c.std.Crop(top=10, bottom=10, left=10, right=10),
            ).get_diff(clip_a, clip_b)


        Args:
            strategies: The strategy or strategies to use for comparison.
                See each strategy's class documentation for more information.
                Default: ``PlaneStatsDiff``.
            mode: The mode to use for combining results from multiple strategies.
                Default: ``DiffMode.ANY``.
            pre_process: The pre-processing function to use for the comparison.
                A callable, ``False`` to skip, or the default box blur with an 8px crop.
            exclusion_ranges: Ranges to exclude from the comparison.
                These frames will still be processed, but not outputted.

        Raises:
            ValueError: No strategies were passed.
        """

        self._func_except = func_except or self.__class__.__name__
        self.mode = DiffMode(mode)

        if strategies is None:
            self.strategies = [PlaneStatsDiff()]
        elif not isinstance(strategies, Sequence):
            self.strategies = [strategies]
        else:
            self.strategies = list(strategies)

        if not self.strategies:
            raise CustomValueError("You must pass at least one strategy!", self._func_except)

        for i, strategy in enumerate(self.strategies):
            if not isinstance(strategy, DiffStrategy):
                self.strategies[i] = strategy()  # type: ignore

        if callable(pre_process):
            self.pre_process = pre_process
        else:
            self.pre_process = False

        self.exclusion_ranges = exclusion_ranges or []

        self.diff_ranges = []
        self._diff_frames: list[int] | None = None
        self._processed_clip: vs.VideoNode | None = None

    def find_diff(
        self: FindDiff,
        src: vs.VideoNode,
        ref: vs.VideoNode,
        force: bool = False,
        error_on_no_diff: bool = True,
        frames_post_process: Callable[[Iterable[int]], Iterable[int]] | None = remove_isolated_frames,
    ) -> FindDiff:
        """
        Find the differences between two clips and store the results.

        The ranges will be accessible through the ``diff_ranges`` attribute.
        If you have already found the differences, the method will return the current instance,
        unless ``force=True``, in which case the current results will be cleared and the
        differences will be recalculated.

        Args:
            src: Source clip.
            ref: Reference clip.
            force: Recompute even when results already exist.
            error_on_no_diff: Raise when no differences are found. Default: ``True``.
            frames_post_process: Post-filter for differing frame numbers.
                Default: :func:`remove_isolated_frames`.

        Returns:
            This ``FindDiff`` instance.

        Raises:
            NoDifferencesFoundError: No differences were found and ``error_on_no_diff`` is ``True``.
        """

        if not force and self._diff_frames:
            return self

        self._diff_frames = None
        self.diff_ranges = []

        src, ref = self._validate_inputs(src, ref)
        self._process(src, ref, frames_post_process)

        if error_on_no_diff and not self._diff_frames:
            raise NoDifferencesFoundError(
                "No differences found!",
                self._func_except,
                reason=self.diff_ranges,
            )

        return self

    def get_diff(
        self: FindDiff,
        src: vs.VideoNode,
        ref: vs.VideoNode,
        names: tuple[str | None, str | None] = (None, None),
        frames_post_process: Callable[[Iterable[int]], Iterable[int]] | None = remove_isolated_frames,
    ) -> vs.VideoNode:
        """
        Get a processed clip highlighting the differences between two clips.

        If ``find_diff`` has not been run yet, this method runs it first.

        Args:
            src: Source clip.
            ref: Reference clip.
            names: Labels for the stacked comparison. ``None`` uses each clip's ``Name`` prop,
                then ``"Src"`` / ``"Ref"``. Default: ``(None, None)``.
            frames_post_process: Post-filter for differing frame numbers.
                Default: :func:`remove_isolated_frames`.

        Returns:
            A clip highlighting differences between ``src`` and ``ref``.

        Raises:
            NoDifferencesFoundError: No differences were found.
            ValueError: ``names`` is not a length-2 tuple of strings.
        """

        self.find_diff(src, ref, frames_post_process=frames_post_process)

        if len(names) != 2:
            raise CustomValueError("Names must be a tuple of two strings!", self._func_except, names)

        new_names = list[str]()

        for i, name in enumerate(names):
            if name is None:
                name = get_prop(
                    ref if i else src,
                    "Name",
                    str,
                    default="Ref" if i else "Src",
                    func=self.get_diff,
                )

            new_names.append(name)

        assert self._processed_clip is not None

        diff_clip = core.std.MakeDiff(src, ref).text.FrameNum(9)

        a_scaled, b_scaled = (Catrom().scale(c, width=c.width // 2, height=c.height // 2) for c in (src, ref))

        a_scaled = merge_clip_props(a_scaled, self._processed_clip)

        stack_srcref = core.std.StackHorizontal(
            [
                a_scaled.text.Text(new_names[0], 3),
                b_scaled.text.Text(new_names[1], 1),
            ]
        )

        stack_diff = core.std.StackVertical([stack_srcref, diff_clip])

        out_diff = self.get_clip_frames(stack_diff)

        out_diff = core.std.StackVertical(
            [
                out_diff.std.Crop(bottom=out_diff.height - stack_srcref.height),
                out_diff.std.Crop(top=stack_srcref.height)
                .text.Text(text="Differences found:", alignment=8)
                .text.FrameNum(alignment=7),
            ]
        )

        return out_diff.std.SetFrameProps(Name=f"diff clip ({new_names})", fd_diffRanges=str(self.diff_ranges))

    def get_diff_full(
        self: FindDiff,
        src: vs.VideoNode,
        ref: vs.VideoNode,
        frames_post_process: Callable[[Iterable[int]], Iterable[int]] | None = remove_isolated_frames,
    ) -> tuple[vs.VideoNode, vs.VideoNode, vs.VideoNode]:
        """
        Get processed clips of the source, reference, and their difference.

        If ``find_diff`` has not been run yet, this method runs it first.

        Args:
            src: Source clip.
            ref: Reference clip.
            frames_post_process: Post-filter for differing frame numbers.
                Default: :func:`remove_isolated_frames`.

        Returns:
            ``(src, ref, diff)`` limited to differing frames.

        Raises:
            NoDifferencesFoundError: No differences were found.
        """

        self.find_diff(src, ref, frames_post_process=frames_post_process)

        assert self._processed_clip is not None

        diff_clip = core.std.MakeDiff(src, ref).text.FrameNum(9)

        src_diff = self.get_clip_frames(src)
        ref_diff = self.get_clip_frames(ref)

        diff_clip = self.get_clip_frames(diff_clip).text.FrameNum(alignment=7)

        return (src_diff, ref_diff, diff_clip)

    def get_clip_frames(
        self,
        clip: vs.VideoNode,
    ) -> vs.VideoNode:
        """
        Get a clip of the frames that are different between the two clips.

        Args:
            clip: The clip to get the frames from.

        Returns:
            A clip of the frames that are different between the two clips.

        Raises:
            NoDifferencesFoundError: ``find_diff`` has not been run, or no differences were found.
        """

        if not self._diff_frames:
            err_msg = "You have not looked for differences yet! Please run `find_diff` first."

            if isinstance(self._diff_frames, list) and not self._diff_frames:
                err_msg = f"No differences found! ({self._diff_frames=})"

            raise NoDifferencesFoundError(
                err_msg,
                self.get_clip_frames,
                reason=self._diff_frames,
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

        Args:
            output_path: File path to write.

        Returns:
            The written file path.

        Raises:
            NoDifferencesFoundError: ``find_diff`` has not been run yet.
            FileIsADirectoryError: ``output_path`` is a directory.
            FilePermissionError: The file cannot be written.
            CustomOSError: An OS error occurred while writing.
            CustomRuntimeError: An unexpected error occurred while writing.
            FileWasNotFoundError: The file was not created.
        """

        if not self.diff_ranges:
            raise NoDifferencesFoundError(
                "You have not found the differences yet! Please run `find_diff` first.",
                self.to_file,
                reason=self.diff_ranges,
            )

        sfile = SPath(output_path)

        if sfile.is_dir():
            raise FileIsADirectoryError(
                "Failed to save frame ranges! Output path is a directory!",
                self.to_file,
                reason=sfile,
            )

        franges = "\n".join(f"{start}-{end}" for start, end in self.diff_ranges)  # type: ignore

        try:
            sfile.write_text(franges)
        except PermissionError as e:
            raise FilePermissionError(
                "Failed to save frame ranges! Insufficient permissions!",
                self.to_file,
                reason=e,
            )
        except OSError as e:
            raise CustomOSError(
                "Failed to save frame ranges! OS error (disk full, invalid path, etc.)!",
                self.to_file,
                reason=e,
            )
        except Exception as e:
            raise CustomRuntimeError(
                "Failed to save frame ranges!",
                self.to_file,
                reason=e,
            )

        if not sfile.exists():
            raise FileWasNotFoundError(
                "Failed to save frame ranges! File was not found!",
                self.to_file,
                reason=sfile,
            )

        return sfile

    def from_file(self, input_path: SPathLike) -> FrameRangesN:
        """
        Load the frame ranges from a file.

        The file must follow this format:

        .. code-block:: text

            1-10
            21-30
            etc.

        Args:
            input_path: File path to read.

        Returns:
            Parsed frame ranges.

        Raises:
            FileWasNotFoundError: The file does not exist.
            FilePermissionError: The file cannot be read.
            CustomOSError: An OS error occurred while reading.
            CustomValueError: The file is empty or malformed.
        """

        sfile = SPath(input_path)

        if not sfile.exists():
            raise FileWasNotFoundError(
                "Failed to load frame ranges! File was not found!",
                self.from_file,
                sfile,
            )

        try:
            content = sfile.read_text()
        except PermissionError as e:
            raise FilePermissionError(
                "Failed to load frame ranges! Insufficient permissions!",
                self.from_file,
                e,
            )
        except OSError as e:
            raise CustomOSError(
                "Failed to load frame ranges! OS error (disk full, invalid path, etc.)!",
                self.from_file,
                e,
            )
        except Exception as e:
            raise CustomOSError(
                "Failed to load frame ranges! Unexpected error!",
                self.from_file,
                e,
            )

        if not (content := content.strip()):
            raise CustomValueError(
                "Failed to load frame ranges! File is empty!",
                self.from_file,
                reason=sfile,
            )

        self.diff_ranges = []

        for line in content.splitlines():
            if not (line := line.strip()):
                continue

            parts = line.split("-")

            if len(parts) != 2 or not all(x.strip().isdigit() for x in parts):
                raise CustomValueError(
                    'Failed to load frame ranges! Invalid format in file! Expected "start-end" per line.',
                    self.from_file,
                    reason=sfile,
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

    def _process(
        self,
        src: vs.VideoNode,
        ref: vs.VideoNode,
        frames_post_process: Callable[[Iterable[int]], Iterable[int]] | None = None,
    ) -> None:
        self._processed_clip = src

        callbacks: CallbacksT = []

        for strategy in self.strategies:
            if not isinstance(strategy, DiffStrategy):
                strategy = strategy()  # type: ignore

            processed_clip, cb = strategy.process(src=self._processed_clip, ref=ref)
            self._processed_clip = processed_clip
            callbacks += cb

        self._find_frames(callbacks, frames_post_process)

    def _find_frames(
        self,
        callbacks: CallbacksT,
        frames_post_process: Callable[[Iterable[int]], Iterable[int]] | None = None,
    ) -> None:
        """Get the frames that are different between two clips."""

        assert isinstance(self._processed_clip, vs.VideoNode)

        frames_render = clip_async_render(
            self._processed_clip,
            None,
            "Finding differences between clips...",
            lambda n, f: Sentinel.check(n, self.mode.check_result([cb(f) for cb in callbacks])),
        )

        self._diff_frames = list(Sentinel.filter(frames_render))
        self._diff_frames.sort()

        if self.exclusion_ranges:
            self.exclusion_ranges = normalize_ranges(self._processed_clip, self.exclusion_ranges)

            excluded = {frame for start, stop in self.exclusion_ranges for frame in range(start, stop + 1)}

            self._diff_frames = [f for f in self._diff_frames if f not in excluded]

        if frames_post_process is not None:
            self._diff_frames = list(frames_post_process(self._diff_frames))

        self.diff_ranges = list(self._to_ranges(self._diff_frames))

    @staticmethod
    def _to_ranges(iterable: list[int]) -> Iterable[tuple[int, int]]:
        iterable = sorted(set(iterable))

        for _, group in groupby(enumerate(iterable), lambda t: t[1] - t[0]):
            groupl = list(group)
            yield groupl[0][1], groupl[-1][1]
