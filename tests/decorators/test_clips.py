from __future__ import annotations

from typing import Any

import pytest
from vstools import core, vs

from lvsfunc.decorators.clips import finalize_clips, initialize_inputs


@pytest.fixture
def blank_clip() -> vs.VideoNode:
    return core.std.BlankClip()


def test_initialize_inputs_initializes_every_clip_argument(
    monkeypatch: pytest.MonkeyPatch,
    blank_clip: vs.VideoNode,
) -> None:
    initialized: list[vs.VideoNode] = []

    def track_init(clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        initialized.append(clip)
        return clip

    monkeypatch.setattr("lvsfunc.decorators.clips.initialize_clip", track_init)

    @initialize_inputs
    def process(src: vs.VideoNode, count: int, ref: vs.VideoNode) -> vs.VideoNode:
        return src

    other = core.std.BlankClip()
    process(blank_clip, 2, ref=other)

    assert initialized == [blank_clip, other]


def test_initialize_inputs_supports_partial_decorator_syntax(
    monkeypatch: pytest.MonkeyPatch,
    blank_clip: vs.VideoNode,
) -> None:
    seen_bits: list[int | None] = []

    def track_init(clip: vs.VideoNode, *, bits: int | None = 32, **kwargs: Any) -> vs.VideoNode:
        seen_bits.append(bits)
        return clip

    monkeypatch.setattr("lvsfunc.decorators.clips.initialize_clip", track_init)

    @initialize_inputs(bits=16)
    def process(clip: vs.VideoNode) -> vs.VideoNode:
        return clip

    process(blank_clip)

    assert seen_bits == [16]


def test_finalize_clips_finalizes_single_return_clip(
    monkeypatch: pytest.MonkeyPatch,
    blank_clip: vs.VideoNode,
) -> None:
    finalized: list[vs.VideoNode] = []

    def track_finalize(clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        finalized.append(clip)
        return clip

    monkeypatch.setattr("lvsfunc.decorators.clips.finalize_clip", track_finalize)

    @finalize_clips
    def process(clip: vs.VideoNode) -> vs.VideoNode:
        return clip

    result = process(blank_clip)

    assert result is blank_clip
    assert finalized == [blank_clip]


def test_finalize_clips_finalizes_returned_tuple(
    monkeypatch: pytest.MonkeyPatch,
    blank_clip: vs.VideoNode,
) -> None:
    finalized: list[vs.VideoNode] = []

    def track_finalize(clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        finalized.append(clip)
        return clip

    monkeypatch.setattr("lvsfunc.decorators.clips.finalize_clip", track_finalize)

    other = core.std.BlankClip()

    @finalize_clips
    def process(_: vs.VideoNode) -> tuple[vs.VideoNode, vs.VideoNode]:
        return blank_clip, other

    process(core.std.BlankClip())

    assert finalized == [blank_clip, other]


def test_finalize_clips_finalizes_returned_list(
    monkeypatch: pytest.MonkeyPatch,
    blank_clip: vs.VideoNode,
) -> None:
    finalized: list[vs.VideoNode] = []

    def track_finalize(clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        finalized.append(clip)
        return clip

    monkeypatch.setattr("lvsfunc.decorators.clips.finalize_clip", track_finalize)

    other = core.std.BlankClip()

    @finalize_clips
    def process(_: vs.VideoNode) -> list[vs.VideoNode]:
        return [blank_clip, other]

    process(core.std.BlankClip())

    assert finalized == [blank_clip, other]


def test_finalize_clips_leaves_non_clip_return_values_untouched(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def track_finalize(clip: vs.VideoNode, **kwargs: Any) -> vs.VideoNode:
        raise AssertionError("finalize_clip should not be called")

    monkeypatch.setattr("lvsfunc.decorators.clips.finalize_clip", track_finalize)

    @finalize_clips
    def process(_: vs.VideoNode) -> int:
        return 42

    assert process(core.std.BlankClip()) == 42


def test_finalize_clips_supports_partial_decorator_syntax(
    monkeypatch: pytest.MonkeyPatch,
    blank_clip: vs.VideoNode,
) -> None:
    seen_bits: list[Any] = []

    def track_finalize(clip: vs.VideoNode, *, bits: Any = 10, **kwargs: Any) -> vs.VideoNode:
        seen_bits.append(bits)
        return clip

    monkeypatch.setattr("lvsfunc.decorators.clips.finalize_clip", track_finalize)

    @finalize_clips(bits=16)
    def process(clip: vs.VideoNode) -> vs.VideoNode:
        return clip

    process(blank_clip)

    assert seen_bits == [16]
