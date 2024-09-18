from random import randint

from vstools import core, vs

__all__: list[str] = [
    "get_random_frame_nums",
    "get_random_frames"
]


def get_random_frame_nums(clip: vs.VideoNode, interval: int = 120) -> list[int]:
    """
    Get a list of random frames numbers from a clip.

    It will grab a random frame from every `interval` frames.

    :param clip:        Clip to get the random frames from.
    :param interval:    The amount of frames for each chunk.
                        It will grab a random frame from every `interval` frames.
                        Default: 120 frames.

    :return:            A list of random frame numbers.
    """

    return [
        randint(i * interval, min((i + 1) * interval - 1, clip.num_frames - 1))
        for i in range((clip.num_frames + interval - 1) // interval)
    ]


def get_random_frames(clip: vs.VideoNode, interval: int = 120) -> vs.VideoNode:
    """
    Get random frames from a clip spliced together into a new clip.

    It will grab a random frame from every `interval` frames.

    :param clip:        Clip to get the random frames from.
    :param interval:    The amount of frames for each chunk.
                        It will grab a random frame from every `interval` frames.
                        Default: 120 frames.

    :return:            A clip with random frames from the input clip.
    """

    return core.std.Splice([clip[num] for num in get_random_frame_nums(clip, interval)])
