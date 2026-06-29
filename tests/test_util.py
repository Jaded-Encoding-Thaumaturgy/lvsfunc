from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from jetpytools import CustomIndexError, CustomValueError
from vstools import vs

from lvsfunc.util import colored_clips, set_vs_affinity, sloc_curve_to_graph


def _mock_cpu_count(monkeypatch: pytest.MonkeyPatch, logical_count: int, physical_count: int) -> None:
    def fake_cpu_count(*, logical: bool = True) -> int:
        return logical_count if logical else physical_count

    monkeypatch.setattr("lvsfunc.util.cpu_count", fake_cpu_count)


def _mock_virtual_memory(monkeypatch: pytest.MonkeyPatch, total_bytes: int) -> None:
    monkeypatch.setattr("lvsfunc.util.virtual_memory", lambda: MagicMock(total=total_bytes))


@pytest.fixture
def set_affinity_calls(monkeypatch: pytest.MonkeyPatch) -> list[tuple[list[int], int]]:
    calls: list[tuple[list[int], int]] = []
    mock_core = MagicMock()
    mock_core.set_affinity = lambda threads, cache_limit_mb: calls.append((list(threads), cache_limit_mb))
    monkeypatch.setattr("lvsfunc.util.core", mock_core)
    return calls


@pytest.mark.parametrize("amount", [0, 1, -1])
def test_colored_clips_requires_at_least_two_outputs(amount: int) -> None:
    with pytest.raises(CustomIndexError):
        colored_clips(amount)


@pytest.mark.parametrize("max_hue", [0, -1, 361])
def test_colored_clips_rejects_hue_outside_valid_range(max_hue: int) -> None:
    with pytest.raises(CustomValueError):
        colored_clips(3, max_hue=max_hue)


def test_colored_clips_applies_blank_clip_arguments() -> None:
    clips = colored_clips(4, rand=False, width=640, height=360, length=12)

    assert len(clips) == 4
    assert all(clip.width == 640 for clip in clips)
    assert all(clip.height == 360 for clip in clips)
    assert all(clip.num_frames == 12 for clip in clips)


def test_colored_clips_seed_reproduces_the_same_sequence() -> None:
    first = colored_clips(8, seed=1234)
    second = colored_clips(8, seed=1234)

    first_frames = [clip.get_frame(0) for clip in first]
    second_frames = [clip.get_frame(0) for clip in second]

    assert [bytes(frame[0]) for frame in first_frames] == [bytes(frame[0]) for frame in second_frames]


def test_colored_clips_without_randomization_starts_with_red() -> None:
    clip = colored_clips(3, rand=False, format=vs.RGB24)[0]
    frame = clip.get_frame(0)

    assert tuple(int(frame[plane][0, 0]) for plane in range(3)) == (255, 0, 0)


def test_sloc_curve_to_graph_returns_matplotlib_figure() -> None:
    from vsdenoise import DFTTest

    fig = sloc_curve_to_graph(DFTTest.SLocation([(0.0, 4.0), (0.5, 16.0), (1.0, 32.0)]), title="test")

    ax = fig.axes[0]

    assert ax.get_title() == "test"
    assert len(ax.lines) == 1
    assert len(ax.collections) == 1


@pytest.mark.parametrize("threads", [-1, 0])
def test_set_vs_affinity_auto_detects_smt_affinity(
    monkeypatch: pytest.MonkeyPatch,
    set_affinity_calls: list[tuple[list[int], int]],
    threads: int,
) -> None:
    _mock_cpu_count(monkeypatch, logical_count=16, physical_count=8)
    _mock_virtual_memory(monkeypatch, 64 * 1024**3)

    set_vs_affinity(threads=threads)

    assert set_affinity_calls == [([0, 2, 4, 6, 8, 10, 12, 14], 48 * 1024)]


def test_set_vs_affinity_uses_contiguous_cores_without_smt(
    monkeypatch: pytest.MonkeyPatch,
    set_affinity_calls: list[tuple[list[int], int]],
) -> None:
    _mock_cpu_count(monkeypatch, logical_count=8, physical_count=8)
    _mock_virtual_memory(monkeypatch, 64 * 1024**3)

    set_vs_affinity()

    assert set_affinity_calls == [(list(range(8)), 48 * 1024)]


def test_set_vs_affinity_caps_auto_threads_at_eight(
    monkeypatch: pytest.MonkeyPatch,
    set_affinity_calls: list[tuple[list[int], int]],
) -> None:
    _mock_cpu_count(monkeypatch, logical_count=32, physical_count=16)
    _mock_virtual_memory(monkeypatch, 64 * 1024**3)

    set_vs_affinity()

    assert set_affinity_calls == [([0, 2, 4, 6, 8, 10, 12, 14], 48 * 1024)]


@pytest.mark.parametrize(
    ("logical_count", "physical_count", "threads", "expected_affinity"),
    [
        (16, 8, 4, [0, 2, 4, 6]),
        (8, 8, 4, [0, 1, 2, 3]),
    ],
)
def test_set_vs_affinity_honors_explicit_thread_count(
    monkeypatch: pytest.MonkeyPatch,
    set_affinity_calls: list[tuple[list[int], int]],
    logical_count: int,
    physical_count: int,
    threads: int,
    expected_affinity: list[int],
) -> None:
    _mock_cpu_count(monkeypatch, logical_count, physical_count)
    _mock_virtual_memory(monkeypatch, 64 * 1024**3)

    set_vs_affinity(threads=threads)

    assert set_affinity_calls == [(expected_affinity, 48 * 1024)]


@pytest.mark.parametrize(
    ("total_bytes", "expected_cache_mb"),
    [
        (8 * 1024**3, 6 * 1024),
        (16 * 1024**3, 12 * 1024),
        (64 * 1024**3, 48 * 1024),
    ],
)
def test_set_vs_affinity_auto_detects_cache_limit(
    monkeypatch: pytest.MonkeyPatch,
    set_affinity_calls: list[tuple[list[int], int]],
    total_bytes: int,
    expected_cache_mb: int,
) -> None:
    _mock_cpu_count(monkeypatch, logical_count=8, physical_count=4)
    _mock_virtual_memory(monkeypatch, total_bytes)

    set_vs_affinity(cache_limit_mb=-1)

    assert set_affinity_calls[0][1] == expected_cache_mb


def test_set_vs_affinity_uses_explicit_cache_limit(
    monkeypatch: pytest.MonkeyPatch,
    set_affinity_calls: list[tuple[list[int], int]],
) -> None:
    _mock_cpu_count(monkeypatch, logical_count=8, physical_count=4)
    _mock_virtual_memory(monkeypatch, 64 * 1024**3)

    set_vs_affinity(cache_limit_mb=4096)

    assert set_affinity_calls[0][1] == 4096
