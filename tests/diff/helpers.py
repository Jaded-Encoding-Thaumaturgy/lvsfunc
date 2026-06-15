from __future__ import annotations

from vstools import vs

from lvsfunc.diff.strategies import DiffStrategy
from lvsfunc.diff.types import CallbacksT

__all__: list[str] = [
    "StubStrategy",
]


class StubStrategy(DiffStrategy):
    """Stub strategy for testing."""

    def __init__(self) -> None:
        super().__init__(0)

    def process(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, CallbacksT]:
        del ref
        return src, []
