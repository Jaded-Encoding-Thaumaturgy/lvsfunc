from __future__ import annotations

import pytest
from jetpytools import CustomValueError, FileIsADirectoryError, FilePermissionError, SPath
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
