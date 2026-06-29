from __future__ import annotations

import pytest
from jetpytools import CustomTypeError, CustomValueError
from vstools import FormatsMismatchError, core, get_w, vs

from lvsfunc.comparison import (
    Direction,
    Interleave,
    Split,
    Stack,
    Tile,
    compare,
    comparison_shots,
    diff_between_clips_stack,
    stack_compare,
)
from lvsfunc.exceptions import ClipsAndNamedClipsError


@pytest.mark.parametrize(
    ("direction", "is_axis", "is_way", "label"),
    [
        (Direction.HORIZONTAL, True, False, "horizontal"),
        (Direction.VERTICAL, True, False, "vertical"),
        (Direction.LEFT, False, True, "left"),
        (Direction.RIGHT, False, True, "right"),
        (Direction.UP, False, True, "up"),
        (Direction.DOWN, False, True, "down"),
    ],
)
def test_direction_axis_way_and_string_properties(
    direction: Direction,
    is_axis: bool,
    is_way: bool,
    label: str,
) -> None:
    assert direction.is_axis is is_axis
    assert direction.is_way is is_way
    assert direction.string == label


def test_comparer_requires_at_least_two_clips() -> None:
    clip = core.std.BlankClip()

    with pytest.raises(CustomValueError):
        Stack([clip])


@pytest.mark.parametrize("alignment", [0, 10])
def test_comparer_rejects_invalid_label_alignment(alignment: int) -> None:
    clip = core.std.BlankClip()

    with pytest.raises(CustomValueError):
        Stack([clip, clip], label_alignment=alignment)


def test_comparer_preserves_named_clip_order() -> None:
    first = core.std.BlankClip(width=640, height=360)
    second = core.std.BlankClip(width=640, height=360)

    comparer = Stack({"first": first, "second": second})

    assert comparer.clips == [first, second]
    assert comparer.names == ["first", "second"]


def test_comparer_rejects_unexpected_clips_type() -> None:
    class FakeClips:
        def __len__(self) -> int:
            return 2

    with pytest.raises(CustomTypeError, match="Unexpected type"):
        Stack(FakeClips())  # type: ignore[arg-type]


def test_stack_skips_whitespace_only_labels() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    result = Stack({"   ": clip, "named": clip}).clip

    assert (result.width, result.height) == (640, 180)


@pytest.mark.parametrize("height", [288, 540])
def test_diff_between_clips_stack_output_dimensions(height: int) -> None:
    clip = core.std.BlankClip(width=1920, height=1080)

    result = diff_between_clips_stack(clip, clip, height=height)
    scaled_width = get_w(height, mod=1)

    assert (result.width, result.height) == (scaled_width * 2, height * 3)


def test_diff_between_clips_stack_default_height() -> None:
    clip = core.std.BlankClip(width=1920, height=1080)

    default = diff_between_clips_stack(clip, clip)
    explicit = diff_between_clips_stack(clip, clip, height=288)

    assert (default.width, default.height) == (explicit.width, explicit.height)


def test_stack_horizontal_dimensions() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    result = Stack([clip, clip, clip]).clip

    assert (result.width, result.height) == (960, 180)


def test_stack_vertical_dimensions() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    result = Stack([clip, clip, clip], direction=Direction.VERTICAL).clip

    assert (result.width, result.height) == (320, 540)


def test_stack_horizontal_rejects_mismatched_heights() -> None:
    clip_a = core.std.BlankClip(width=320, height=180)
    clip_b = core.std.BlankClip(width=320, height=200)

    with pytest.raises(CustomValueError):
        Stack([clip_a, clip_b]).clip


def test_stack_vertical_rejects_mismatched_widths() -> None:
    clip_a = core.std.BlankClip(width=320, height=180)
    clip_b = core.std.BlankClip(width=640, height=180)

    with pytest.raises(CustomValueError):
        Stack([clip_a, clip_b], direction=Direction.VERTICAL).clip


def test_stack_convenience_method_stacks_positional_clips() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    result = Stack.stack(clip, clip, clip)

    assert (result.width, result.height) == (960, 180)


def test_split_convenience_method_stacks_positional_clips() -> None:
    clip = core.std.BlankClip(width=960, height=540, format=vs.YUV444P8)

    result = Split.stack(clip, clip, clip)

    assert (result.width, result.height) == (clip.width, clip.height)


def test_stack_vertical_convenience_method_stacks_named_clips() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    result = Stack.stack_vertical(first=clip, second=clip)

    assert (result.width, result.height) == (320, 360)


@pytest.mark.parametrize("method", [Stack.stack, Stack.stack_vertical, Split.stack])
def test_stack_convenience_methods_reject_mixed_positional_and_named_clips(method: object) -> None:
    clip = core.std.BlankClip(width=320, height=180)

    with pytest.raises(ClipsAndNamedClipsError):
        method(clip, named=clip)  # type: ignore[operator]


@pytest.mark.parametrize("count", [2, 3, 5, 10])
def test_tile_auto_arrangement_creates_a_large_enough_grid(count: int) -> None:
    clip = core.std.BlankClip(width=320, height=180)
    tile = Tile([clip] * count)

    columns = tile.clip.width // clip.width
    rows = tile.clip.height // clip.height

    assert columns * rows >= count
    assert sum(map(sum, tile.arrangement)) == count


def test_tile_pads_custom_arrangement_and_sets_dimensions() -> None:
    clip = core.std.BlankClip(width=320, height=180)
    tile = Tile([clip, clip, clip], arrangement=[[1, 0, 1], [1]])

    assert tile.clip.width == 960
    assert tile.clip.height == 360
    assert sum(map(sum, tile.arrangement)) == 3
    assert len({len(row) for row in tile.arrangement}) == 1


@pytest.mark.parametrize("arrangement", [[[1, 1]], [[1], [1]]])
def test_tile_rejects_one_dimensional_arrangement(arrangement: list[list[int]]) -> None:
    clip = core.std.BlankClip(width=320, height=180)

    with pytest.raises(CustomValueError):
        Tile([clip, clip], arrangement=arrangement)


def test_tile_rejects_mismatched_clip_dimensions() -> None:
    clip_a = core.std.BlankClip(width=320, height=180)
    clip_b = core.std.BlankClip(width=640, height=180)

    with pytest.raises(CustomValueError, match="widths and heights"):
        Tile([clip_a, clip_b])


def test_tile_rejects_arrangement_with_wrong_number_of_slots() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    with pytest.raises(Exception):
        Tile([clip, clip, clip], arrangement=[[1, 1], [0, 0]])


@pytest.mark.parametrize(
    ("direction", "expected_sizes"),
    [
        (Direction.HORIZONTAL, [(320, 540), (320, 540), (320, 540)]),
        (Direction.VERTICAL, [(960, 180), (960, 180), (960, 180)]),
    ],
)
def test_split_preserves_total_dimensions(
    direction: Direction,
    expected_sizes: list[tuple[int, int]],
) -> None:
    clip = core.std.BlankClip(width=960, height=540, format=vs.YUV420P8)

    split = Split([clip, clip, clip], direction=direction)

    assert [(part.width, part.height) for part in split.clips] == expected_sizes
    assert (split.clip.width, split.clip.height) == (960, 540)


def test_split_assigns_odd_dimension_remainder_to_last_clip() -> None:
    clip = core.std.BlankClip(width=101, height=60, format=vs.YUV444P8)

    split = Split([clip, clip, clip], direction=Direction.HORIZONTAL)

    assert [part.width for part in split.clips] == [33, 33, 35]
    assert (split.clip.width, split.clip.height) == (clip.width, clip.height)


def test_split_rejects_crops_that_break_chroma_subsampling() -> None:
    clip = core.std.BlankClip(width=100, height=60, format=vs.YUV420P8)

    with pytest.raises(CustomValueError, match="subsampling"):
        Split([clip, clip, clip], direction=Direction.HORIZONTAL)


def test_split_rejects_mismatched_clip_dimensions() -> None:
    clip_a = core.std.BlankClip(width=320, height=180)
    clip_b = core.std.BlankClip(width=640, height=180)

    with pytest.raises(CustomValueError, match="same width and height"):
        Split([clip_a, clip_b])


def test_split_rejects_non_axis_direction() -> None:
    clip = core.std.BlankClip(width=960, height=540, format=vs.YUV444P8)

    with pytest.raises(CustomValueError, match="Unknown direction"):
        Split([clip, clip, clip], direction=Direction.LEFT)


def test_interleave_frame_count() -> None:
    clip = core.std.BlankClip(width=320, height=180, length=5)

    result = Interleave([clip, clip, clip]).clip

    assert result.num_frames == 15
    assert (result.width, result.height) == (320, 180)


def test_compare_interleaves_only_requested_frames() -> None:
    clip_a = core.std.BlankClip(width=320, height=180, length=20)
    clip_b = core.std.BlankClip(width=320, height=180, length=20)

    result = compare(clip_a, clip_b, frames=[2, 7, 15], force_resample=False, print_frame=False, mismatch=True)

    assert result.num_frames == 6
    assert (result.width, result.height) == (320, 180)


def test_compare_resamples_and_labels_by_default() -> None:
    clip_a = core.std.BlankClip(width=320, height=180, length=10, format=vs.YUV420P8)
    clip_b = core.std.BlankClip(width=320, height=180, length=10, format=vs.YUV420P8)

    result = compare(clip_a, clip_b, frames=[2, 5])

    assert result.format.color_family == vs.RGB
    assert result.num_frames == 4


def test_compare_rejects_format_mismatch_without_mismatch_flag() -> None:
    yuv = core.std.BlankClip(width=320, height=180, format=vs.YUV420P8, length=5)
    rgb = core.std.BlankClip(width=320, height=180, format=vs.RGB24, length=5)

    with pytest.raises(FormatsMismatchError):
        compare(yuv, rgb, frames=[1], force_resample=False, print_frame=False)


def test_compare_rejects_more_requested_frames_than_available() -> None:
    clip = core.std.BlankClip(length=2)

    with pytest.raises(CustomValueError):
        compare(clip, clip, frames=[0, 1, 2], print_frame=False)


def test_compare_uses_requested_random_sample(monkeypatch: pytest.MonkeyPatch) -> None:
    clip = core.std.BlankClip(length=20)
    observed: list[tuple[range, int]] = []

    def sample(population: range, amount: int) -> list[int]:
        observed.append((population, amount))

        return [8, 3]

    monkeypatch.setattr("lvsfunc.comparison.random.sample", sample)

    result = compare(clip, clip, rand_total=2, force_resample=False, print_frame=False)

    assert observed == [(range(1, 19), 2)]
    assert result.num_frames == 4


def test_compare_uses_auto_rand_total_for_short_clips(monkeypatch: pytest.MonkeyPatch) -> None:
    clip = core.std.BlankClip(length=200)
    observed: list[int] = []

    def sample(population: range, amount: int) -> list[int]:
        observed.append(amount)

        return [10, 20][:amount]

    monkeypatch.setattr("lvsfunc.comparison.random.sample", sample)

    result = compare(clip, clip, force_resample=False, print_frame=False, mismatch=True)

    assert observed == [2]
    assert result.num_frames == 4


def test_diff_between_clips_stack_truncates_to_shorter_clip() -> None:
    shorter = core.std.BlankClip(width=640, height=360, length=5)
    longer = core.std.BlankClip(width=640, height=360, length=8)

    with pytest.warns(UserWarning, match="not of the same length"):
        result = diff_between_clips_stack(shorter, longer, height=180)

    assert result.num_frames == 5


def test_diff_between_clips_stack_truncates_when_first_clip_is_longer() -> None:
    shorter = core.std.BlankClip(width=640, height=360, length=5)
    longer = core.std.BlankClip(width=640, height=360, length=8)

    with pytest.warns(UserWarning, match="not of the same length"):
        result = diff_between_clips_stack(longer, shorter, height=180)

    assert result.num_frames == 5


def test_diff_between_clips_stack_rejects_wrong_positional_clip_count() -> None:
    clip = core.std.BlankClip(width=640, height=360)

    with pytest.raises(CustomValueError, match="exactly 2"):
        diff_between_clips_stack(clip)


def test_diff_between_clips_stack_rejects_wrong_named_clip_count() -> None:
    clip = core.std.BlankClip(width=640, height=360)

    with pytest.raises(CustomValueError, match="exactly 2"):
        diff_between_clips_stack(a=clip)


def test_diff_between_clips_stack_rejects_mixed_call_styles() -> None:
    clip = core.std.BlankClip(width=640, height=360)

    with pytest.raises(ClipsAndNamedClipsError):
        diff_between_clips_stack(clip, clip, first=clip, second=clip)


def test_diff_between_clips_stack_rejects_format_mismatch() -> None:
    yuv = core.std.BlankClip(width=640, height=360, format=vs.YUV420P8)
    rgb = core.std.BlankClip(width=640, height=360, format=vs.RGB24)

    with pytest.raises(CustomValueError, match="same format"):
        diff_between_clips_stack(yuv, rgb)


def test_comparison_shots_applies_crop_before_stacking() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    result = comparison_shots(clip, clip, left=10, right=20, top=5, bottom=15)

    assert result.width == (320 - 10 - 20) * 2
    assert result.height == 180 - 5 - 15


def test_comparison_shots_multiplier_scales_cropped_height() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    result = comparison_shots(clip, clip, top=10, bottom=10, height=2)

    assert result.height == 320
    assert result.width % 2 == 0


def test_comparison_shots_named_clips_crop_and_scale() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    result = comparison_shots(a=clip, b=clip, top=10, bottom=10, height=2)

    assert result.height == 320
    assert result.width % 2 == 0


def test_comparison_shots_rejects_mixed_positional_and_named_clips() -> None:
    clip = core.std.BlankClip(width=320, height=180)

    with pytest.raises(ClipsAndNamedClipsError):
        comparison_shots(clip, a=clip, b=clip)


@pytest.mark.parametrize("count", [0, 1, 3])
def test_stack_compare_requires_exactly_two_clips(count: int) -> None:
    clip = core.std.BlankClip(width=640, height=360)

    with pytest.raises(CustomValueError):
        stack_compare(*([clip] * count))


def test_stack_compare_uses_default_height_when_not_given() -> None:
    clip = core.std.BlankClip(width=1920, height=1080)

    default = stack_compare(clip, clip)
    explicit = stack_compare(clip, clip, height=288)

    assert (default.width, default.height) == (explicit.width, explicit.height)


def test_stack_compare_caps_default_height_on_short_clips() -> None:
    clip = core.std.BlankClip(width=640, height=360)

    default = stack_compare(clip, clip)
    capped = stack_compare(clip, clip, height=180)

    assert (default.width, default.height) == (capped.width, capped.height)


def test_stack_compare_caps_requested_height() -> None:
    clip = core.std.BlankClip(width=640, height=360)

    with pytest.warns(UserWarning, match="bigger than clipa's height"):
        result = stack_compare(clip, clip, height=300)

    assert result.height == 540
