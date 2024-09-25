import random
from typing import Any, Callable

from vstools import (CustomRuntimeError, CustomValueError, core, depth,
                     get_prop, vs)

__all__: list[str] = [
    'get_random_frame_nums',
    'get_random_frames',

    'get_smart_random_frame_nums',
    'get_smart_random_frames'
]


def get_random_frame_nums(clip: vs.VideoNode, interval: int = 120, seed: int | None = None) -> list[int]:
    """
    Get a list of random frames numbers from a clip.

    It will grab a random frame from every `interval` frames.

    :param clip:        Clip to get the random frames from.
    :param interval:    The amount of frames for each chunk.
                        It will grab a random frame from every `interval` frames.
                        Default: 120 frames.
    :param seed:        Seed for the random number generator.
                        Default: None.

    :return:            A list of random frame numbers.
    """

    if seed is not None:
        random.seed(seed)

    return [
        random.randint(i * interval, min((i + 1) * interval - 1, clip.num_frames - 1))
        for i in range((clip.num_frames + interval - 1) // interval)
    ]


def get_random_frames(clip: vs.VideoNode, interval: int = 120, seed: int | None = None) -> vs.VideoNode:
    """
    Get random frames from a clip spliced together into a new clip.

    It will grab a random frame from every `interval` frames.

    :param clip:        Clip to get the random frames from.
    :param interval:    The amount of frames for each chunk.
                        It will grab a random frame from every `interval` frames.
                        Default: 120 frames.
    :param seed:        Seed for the random number generator.
                        Default: None.

    :return:            A clip with random frames from the input clip.
    """

    return core.std.Splice([clip[num] for num in get_random_frame_nums(clip, interval, seed)])


def get_smart_random_frame_nums(
    clip: vs.VideoNode,
    interval: int = 120, max_retries: int = 10,
    solid_threshold: int = 2, similarity_threshold: float = 0.02,
    strict: bool = False, seed: int | None = None,
) -> list[int]:
    """
    Get smart random frame numbers from a clip.

    This function selects random frame numbers from a clip, avoiding solid colors and similar consecutive frames.
    It divides the clip into intervals and attempts to select a suitable frame number from each interval.

    The function uses the following criteria to select frames:

        1. Avoids frames that are solid colors (determined by `solid_threshold`).
        2. Avoids frames too similar to the previous frame (determined by `similarity_threshold`).
        3. Attempts to select a frame from each interval.
        4. If a suitable frame isn't found in an interval after `max_retries`, moves to the next.

    All values provided are assumed to be 8-bit values.

    If `strict` is True, raises an error if no suitable frame is found in any interval
    after max retries. If False (default), falls back to a random frame from the interval.

    :param clip:                    Clip to get the random frame numbers from.
    :param interval:                The amount of frames for each chunk. Default: 120 frames.
    :param max_retries:             Maximum number of retries before picking a random frame. Default: 10.
    :param solid_threshold:         Threshold for determining if a frame is a solid color. Default: 2.
    :param similarity_threshold:    Threshold for determining if frames are too similar. Default: 0.95.
    :param strict:                  Whether to raise an error if a suitable frame cannot be found. Default: False.
    :param seed:                    Seed for the random number generator. Default: None.

    :return:                        A list of intelligently selected random frame numbers from the input clip.

    :raises CustomValueError:       If `interval` is less than or equal to 0.
    :raises CustomValueError:       If `max_retries` is less than 0.
    :raises CustomRuntimeError:     If `strict` is True and a suitable frame cannot be found after max_retries.
    """

    if interval <= 0:
        raise CustomValueError("'interval' must be greater than 0!", get_smart_random_frame_nums)

    if max_retries < 0:
        raise CustomValueError("'max_retries' must be greater than or equal to 0!", get_smart_random_frame_nums)

    solid_threshold = max(0, min(solid_threshold, 255))
    similarity_threshold = max(0, min(similarity_threshold, 1))

    # Set the random seed if provided
    if seed is not None:
        random.seed(seed)

    def _check_solid_color(frame: vs.VideoNode) -> tuple[bool, int]:
        min_value = get_prop(frame, 'PlaneStatsMin', int)
        max_value = get_prop(frame, 'PlaneStatsMax', int)

        is_solid = (max_value - min_value) <= solid_threshold

        return is_solid, min_value

    def _check_frame_similarity(frame1: vs.VideoNode, frame2: vs.VideoNode) -> tuple[bool, float]:
        frame_diff = core.std.PlaneStats(frame1, frame2)
        diff_value = get_prop(frame_diff, 'PlaneStatsDiff', float, None, 0)

        return diff_value <= similarity_threshold, diff_value

    def _select_smart_frame(start: int, end: int, prev_frame: vs.VideoNode | None) -> int:
        segment_length = end - start + 1
        actual_retries = min(max_retries, segment_length)
        tried_frames = set()

        for _ in range(actual_retries):
            frame_num = random.randint(start, end)

            while frame_num in tried_frames:
                frame_num = random.randint(start, end)

            tried_frames.add(frame_num)

            frame = clip[frame_num]

            is_solid, _ = _check_solid_color(frame)
            is_valid_frame = not is_solid
            is_similar_to_prev, _ = (False, 0.0) if prev_frame is None \
                else _check_frame_similarity(prev_frame, frame)

            if is_valid_frame and not is_similar_to_prev:
                return frame_num

        if strict:
            _raise_strict_error(
                start, end, actual_retries, tried_frames, prev_frame, clip,
                _check_solid_color, _check_frame_similarity
            )

        # If we couldn't find a suitable frame after max_retries, just return a random frame number
        return random.randint(start, end)

    clip = depth(clip, 8).std.PlaneStats()

    frame_nums = []

    num_intervals = (clip.num_frames + interval - 1) // interval

    prev_frame = None

    for interval_index in range(num_intervals):
        interval_start = interval_index * interval
        interval_end = min(interval_start + interval - 1, clip.num_frames - 1)

        if interval_start > interval_end:
            continue

        frame_num = _select_smart_frame(interval_start, interval_end, prev_frame)
        frame_nums.append(frame_num)

        prev_frame = core.std.Limiter(clip[frame_num])

    return frame_nums


def _raise_strict_error(
    start: int, end: int, actual_retries: int,
    tried_frames: set[int], prev_frame: vs.VideoNode | None,
    clip: vs.VideoNode,
    is_solid_color: Callable[[vs.VideoNode], tuple[bool, int]],
    frames_too_similar: Callable[[vs.VideoNode, vs.VideoNode], tuple[bool, float]]
) -> None:
    attempts = []
    for frame_num in tried_frames:
        frame = clip[frame_num]
        is_solid, solid_value = is_solid_color(frame)
        is_similar, similarity_value = (False, 0.0) if prev_frame is None \
            else frames_too_similar(prev_frame, frame)

        attempts.append({
            'frame_num': frame_num,
            'solid_value': solid_value,
            'similarity_value': similarity_value,
            'is_solid': is_solid,
            'is_similar': is_similar,
            'status': 'Failed' if is_solid or is_similar else 'Succeeded'
        })

    def format_attempt(a: dict[str, Any]) -> str:
        return (
            f"Frame {a['frame_num']}: "
            f"{'Solid' if a['is_solid'] else 'Not solid'} (color diff: {a['solid_value']}), "
            f"{'Similar' if a['is_similar'] else 'Not similar'} (prev frame diff: {a['similarity_value']:.2f})"
        )

    raise CustomRuntimeError(
        f"Could not find a suitable frame after {actual_retries} retries in the interval {start}-{end}!",
        get_smart_random_frame_nums,
        reason="\nReason:\n\nAttempts:\n" + '\n'.join(f"  - {format_attempt(a)}" for a in attempts) + "\n\n"
    )


def get_smart_random_frames(
    clip: vs.VideoNode,
    interval: int = 120,
    max_retries: int = 10,
    solid_threshold: int = 2,
    similarity_threshold: float = 0.02,
    strict: bool = False,
    seed: int | None = None
) -> vs.VideoNode:
    """
    Get smart random frames from a clip spliced together into a new clip.

    This function selects random frames from a clip, avoiding solid colors and similar consecutive frames.
    It uses the same criteria as get_smart_random_frame_nums to select frames.

    :param clip:                    Clip to get the random frames from.
    :param interval:                The amount of frames for each chunk. Default: 120 frames.
    :param max_retries:             Maximum number of retries before picking a random frame. Default: 10.
    :param solid_threshold:         Threshold for determining if a frame is a solid color. Default: 2.
    :param similarity_threshold:    Threshold for determining if frames are too similar. Default: 0.02.
    :param strict:                  Whether to raise an error if a suitable frame cannot be found. Default: False.
    :param seed:                    Seed for the random number generator. Default: None.

    :return:                        A clip with intelligently selected random frames from the input clip.

    :raises CustomValueError:       If `interval` is less than or equal to 0.
    :raises CustomValueError:       If `max_retries` is less than 0.
    :raises CustomRuntimeError:     If `strict` is True and a suitable frame cannot be found after max_retries.
    """

    frame_nums = get_smart_random_frame_nums(
        clip, interval, max_retries, solid_threshold, similarity_threshold, strict, seed
    )

    return core.std.Splice([clip[num] for num in frame_nums])
