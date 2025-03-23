
from typing import Callable, TypeAlias

from vstools import vs

__all__: list[str] = [
    'CallbackT',
    'CallbacksT',
]


CallbackT: TypeAlias = Callable[[vs.VideoFrame], bool]
"""A callback function that takes a frame and returns a boolean value."""


CallbacksT: TypeAlias = list[CallbackT]
"""A list of callback functions."""
