"""
Dumb le funny xddd functions.

These are not intended to be used in any release whatsoever.
If you *do* use them, I sincerely hope it's for an April Fools encode.

These functions are undocumented and will never be full features. Probably.
Don't tell louis this exists though, else I'm a dead man.
"""
from __future__ import annotations

from typing import List

import vapoursynth as vs

from .kernels import Point
from .util import check_variable_resolution, force_mod

core = vs.core

__all__: List[str] = [
    'minecraftify'
]


def minecraftify(clip: vs.VideoNode, div: float = 64.0, mod: int | None = None) -> vs.VideoNode:
    """
    Transform your clip into a Minecraft.

    Idea from Meme-Maji's Kobayashi memery (love you vardë).

    :param clip:    Clip to process.
    :param div:     How much to divide the clip's resolution with.
    :param mod:     Force the downscaled clip to be MOD# compliant.

    :return:        A Minecraft.
    """
    check_variable_resolution(clip, "minecraftify")

    ow, oh = round(clip.width/div), round(clip.height/div)

    if mod is not None:
        ow, oh = force_mod(ow, mod), force_mod(oh, mod)

    i444 = core.resize.Bicubic(clip, format=vs.YUV444PS)
    down = Point().scale(i444, ow, oh)
    return Point().scale(down, clip.width, clip.height)
