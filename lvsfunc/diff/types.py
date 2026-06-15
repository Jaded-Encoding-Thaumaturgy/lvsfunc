from collections.abc import Callable

from vstools import vs

__all__: list[str] = [
    "CallbackT",
    "CallbacksT",
]


type CallbackT = Callable[[vs.VideoFrame], bool]
"""A callback function that takes a frame and returns a boolean value."""


type CallbacksT = list[CallbackT]
"""A list of callback functions."""
