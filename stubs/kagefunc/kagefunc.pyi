# flake8: noqa

import typing

import vapoursynth as vs


def kirsch(src: vs.VideoNode) -> vs.VideoNode: ...
def retinex_edgemask(src: vs.VideoNode, sigma: typing.Union[float, typing.Sequence[float]] = 1.0) -> vs.VideoNode: ...
def squaremask(clip: vs.VideoNode, width: int, height: int, offset_x: int, offset_y: int) -> vs.VideoNode: ...
