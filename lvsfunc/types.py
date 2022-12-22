from __future__ import annotations

from vstools import CustomIntEnum

__all__ = [
    'SceneChangeMode',
    'x265_me_map',
]


class SceneChangeMode(CustomIntEnum):
    """Size type for :py:func:`lvsfunc.render.find_scene_changes`."""

    WWXD = 0
    SCXVID = 1
    WWXD_SCXVID_UNION = 2
    WWXD_SCXVID_INTERSECTION = 3


x265_me_map: list[str] = [
    "dia", "hex", "umh", "star", "sea", "full"
]
