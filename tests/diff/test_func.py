from __future__ import annotations

from collections.abc import Iterable

import pytest
from jetpytools import CustomValueError, FileIsADirectoryError, FilePermissionError, FileWasNotFoundError, SPath
from vstools import core

from lvsfunc.diff.exceptions import NoDifferencesFoundError
from lvsfunc.diff.func import FindDiff, remove_isolated_frames

from .helpers import StubStrategy


@pytest.mark.parametrize(
    ("frames", "thr", "expected"),
    [
        # No isolated frames
        ([1, 2, 3], 1, [1, 2, 3]),
        # Isolated frames
        ([1, 5], 1, []),
        ([1, 3], 1, []),
        # Adjacent frames
        ([1, 3], 2, [1, 3]),
        ([0, 2, 4], 2, [0, 2, 4]),
        # Empty frames
        ([], 1, []),
    ],
)
def test_remove_isolated_frames(frames: list[int], thr: int, expected: list[int]) -> None:
    assert list(remove_isolated_frames(frames, thr)) == expected


@pytest.mark.parametrize(
    ("frames", "expected"),
    [
        # Unique frames with gaps
        ([1, 2, 3, 5, 7, 8], [(1, 3), (5, 5), (7, 8)]),
        # Single frame
        ([5], [(5, 5)]),
        # Unsorted and duplicate frames
        ([3, 1, 2, 2], [(1, 3)]),
        # Empty frames
        ([], []),
    ],
)
def test_to_ranges(frames: list[int], expected: list[tuple[int, int]]) -> None:
    assert list(FindDiff._to_ranges(frames)) == expected


def test_find_diff_requires_strategy() -> None:
    with pytest.raises(CustomValueError):
        FindDiff([])


def test_from_file_errors_on_empty_content(tmp_path: SPath) -> None:
    path = tmp_path / "test.txt"
    path.write_text("")

    fd = FindDiff(StubStrategy(), pre_process=False)

    with pytest.raises(CustomValueError):
        fd.from_file(path)


@pytest.mark.parametrize(
    ("content"),
    [
        "1-2-3",
        "test",
        "1-test",
    ],
)
def test_from_file_errors_on_invalid_content(tmp_path: SPath, content: str) -> None:
    path = tmp_path / "test.txt"
    path.write_text(content)

    fd = FindDiff(StubStrategy(), pre_process=False)

    with pytest.raises(CustomValueError):
        fd.from_file(path)


def test_from_file_skips_empty_lines(tmp_path: SPath) -> None:
    path = tmp_path / "test.txt"
    path.write_text("1-10\n\n21-30\n")

    fd = FindDiff(StubStrategy(), pre_process=False)

    assert fd.from_file(path) == [(1, 10), (21, 30)]


def test_to_file_requires_diff_ranges() -> None:
    fd = FindDiff(StubStrategy(), pre_process=False)

    with pytest.raises(NoDifferencesFoundError):
        fd.to_file("test.txt")


def test_to_file_errors_on_directory(tmp_path: SPath) -> None:
    (tmp_path / "test.txt").mkdir()

    fd = FindDiff(StubStrategy(), pre_process=False)
    fd.diff_ranges = [(1, 10)]

    with pytest.raises(FileIsADirectoryError):
        fd.to_file(tmp_path / "test.txt")


def test_to_file_errors_on_permission_error(tmp_path: SPath) -> None:
    (tmp_path / "test.txt").touch()
    (tmp_path / "test.txt").chmod(0o000)

    fd = FindDiff(StubStrategy(), pre_process=False)
    fd.diff_ranges = [(1, 10)]

    with pytest.raises(FilePermissionError):
        fd.to_file(tmp_path / "test.txt")


@pytest.mark.parametrize(
    ("diff_ranges"),
    [
        [(1, 10), (21, 30)],
        [(1, 10)],
        [(1, 10), (21, 30), (41, 50)],
    ],
)
def test_to_file_roundtrips(tmp_path: SPath, diff_ranges: list[tuple[int, int]]) -> None:
    path = tmp_path / "ranges.txt"

    fd = FindDiff(StubStrategy(), pre_process=False)
    fd.diff_ranges = diff_ranges

    fd.to_file(path)

    new_fd = FindDiff(StubStrategy(), pre_process=False)
    assert new_fd.from_file(path) == fd.diff_ranges


def test_find_diff_raises_when_no_differences() -> None:
    src = core.std.BlankClip(length=25)

    fd = FindDiff(StubStrategy(), pre_process=False)

    with pytest.raises(NoDifferencesFoundError):
        fd.find_diff(src, src, frames_post_process=None)


def test_find_diff_no_raise_when_error_disabled() -> None:
    src = core.std.BlankClip(length=25)

    fd = FindDiff(StubStrategy(), pre_process=False)
    fd.find_diff(src, src, error_on_no_diff=False)

    assert fd.diff_ranges == []


def test_find_diff_builds_ranges(monkeypatch: pytest.MonkeyPatch) -> None:
    src = core.std.BlankClip(length=25)
    frames = [5, 6, 7]

    monkeypatch.setattr("lvsfunc.diff.func.clip_async_render", lambda *_args, **_kwargs: frames)

    fd = FindDiff(StubStrategy(), pre_process=False)
    fd.find_diff(src, src, frames_post_process=None)

    assert fd._diff_frames == frames
    assert fd.diff_ranges == [(5, 7)]


def test_find_diff_applies_exclusion_ranges(monkeypatch: pytest.MonkeyPatch) -> None:
    src = core.std.BlankClip(length=25)
    frames = list(range(5, 20))

    monkeypatch.setattr("lvsfunc.diff.func.clip_async_render", lambda *_args, **_kwargs: frames)

    fd = FindDiff(StubStrategy(), exclusion_ranges=[(10, 15)], pre_process=False)
    fd.find_diff(src, src, frames_post_process=None)

    assert fd._diff_frames == [5, 6, 7, 8, 9, 16, 17, 18, 19]
    assert fd.diff_ranges == [(5, 9), (16, 19)]


def test_find_diff_applies_frame_post_processor(monkeypatch: pytest.MonkeyPatch) -> None:
    clip = core.std.BlankClip(length=20)
    observed: list[list[int]] = []

    monkeypatch.setattr("lvsfunc.diff.func.clip_async_render", lambda *_args, **_kwargs: [8, 2, 5, 11, 14, 21])

    def _keep_odd_frames(frames: Iterable[int]) -> Iterable[int]:
        values = list(frames)

        filtered = [frame for frame in values if frame % 2]

        observed.append(filtered)

        return filtered

    finder = FindDiff(StubStrategy(), pre_process=False)
    finder.find_diff(clip, clip, frames_post_process=_keep_odd_frames)

    assert observed == [[5, 11, 21]]
    assert finder.diff_ranges == [(5, 5), (11, 11), (21, 21)]


def test_find_diff_reuses_cached_result_unless_forced(monkeypatch: pytest.MonkeyPatch) -> None:
    clip = core.std.BlankClip(length=20)
    renders = 0

    def render(*_args: object, **_kwargs: object) -> list[int]:
        nonlocal renders
        renders += 1

        return [4, 5]

    monkeypatch.setattr("lvsfunc.diff.func.clip_async_render", render)

    finder = FindDiff(StubStrategy(), pre_process=False)
    finder.find_diff(clip, clip, frames_post_process=None)
    finder.find_diff(clip, clip, frames_post_process=None)

    assert renders == 1

    finder.find_diff(clip, clip, force=True, frames_post_process=None)

    assert renders == 2


def test_find_diff_truncates_mismatched_clips_before_processing(monkeypatch: pytest.MonkeyPatch) -> None:
    src = core.std.BlankClip(length=12)
    ref = core.std.BlankClip(length=7)
    processed_lengths: list[int] = []

    def render(clip: object, *_args: object, **_kwargs: object) -> list[int]:
        processed_lengths.append(clip.num_frames)  # type: ignore[attr-defined]
        return [1, 2]

    monkeypatch.setattr("lvsfunc.diff.func.clip_async_render", render)

    finder = FindDiff(StubStrategy(), pre_process=False)

    with pytest.warns(UserWarning, match="number of frames"):
        finder.find_diff(src, ref, frames_post_process=None)

    assert processed_lengths == [7]


def test_get_clip_frames_returns_only_detected_frames() -> None:
    clip = core.std.BlankClip(length=20)
    finder = FindDiff(StubStrategy(), pre_process=False)
    finder._diff_frames = [1, 4, 9]

    result = finder.get_clip_frames(clip)

    assert result.num_frames == 3
    assert (result.width, result.height) == (clip.width, clip.height)


def test_from_file_replaces_previous_ranges(tmp_path: SPath) -> None:
    ranges_file = tmp_path / "ranges.txt"
    ranges_file.write_text("3-4\n8-10\n")

    finder = FindDiff(StubStrategy(), pre_process=False)
    finder.diff_ranges = [(100, 200)]

    assert finder.from_file(ranges_file) == [(3, 4), (8, 10)]


def test_from_file_rejects_missing_file(tmp_path: SPath) -> None:
    finder = FindDiff(StubStrategy(), pre_process=False)

    with pytest.raises(FileWasNotFoundError):
        finder.from_file(tmp_path / "missing.txt")
