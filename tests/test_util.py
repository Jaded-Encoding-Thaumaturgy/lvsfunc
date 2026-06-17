from __future__ import annotations

import pytest
from jetpytools import CustomIndexError, CustomValueError
from vstools import vs

from lvsfunc.util import colored_clips


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


def test_colored_clips_without_randomisation_starts_with_red() -> None:
    clip = colored_clips(3, rand=False, format=vs.RGB24)[0]
    frame = clip.get_frame(0)

    assert tuple(int(frame[plane][0, 0]) for plane in range(3)) == (255, 0, 0)
