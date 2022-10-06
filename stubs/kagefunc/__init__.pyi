# flake8: noqa

from typing import Sequence

import vapoursynth as vs


def kirsch(src: vs.VideoNode) -> vs.VideoNode: ...


def retinex_edgemask(src: vs.VideoNode, sigma: float | Sequence[float] = 1.0) -> vs.VideoNode: ...


def squaremask(clip: vs.VideoNode, width: int, height: int, offset_x: int, offset_y: int) -> vs.VideoNode: ...


def hardsubmask_fades(
    clip: vs.VideoNode, ref: vs.VideoNode, expand_n: int = 8, highpass: int = 5000
) -> vs.VideoNode: ...


def hardsubmask(clip: vs.VideoNode, ref: vs.VideoNode, expand_n: int | None = None) -> vs.VideoNode: ...


def crossfade(clipa: vs.VideoNode, clipb: vs.VideoNode, duration: int) -> vs.VideoNode: ...
