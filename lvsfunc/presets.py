# from typing import Any

# from vsdenoise import MotionMode, Prefilter, SADMode, SearchMode

__all__: list[str] = [
    # 'MVLightPreset',
]


# MVLightPreset: dict[str, Any] = dict(
#     block_size=16, overlap=8,
#     range_conversion=4.0,
#     sad_mode=SADMode.SPATIAL,
#     search=SearchMode.DIAMOND,
#     motion=MotionMode.SAD,
#     prefilter=Prefilter.DFTTEST(
#         sloc=[(0.0, 1.0), (0.2, 4.0), (0.35, 12.0), (1.0, 24.0)],
#         ssystem=1, planes=0
#     ),
#     planes=None
# )
"""
Light's MVTools preset.

Please set parameters such as tr, thSAD, etc. manually.
Make sure to always check that this preset gives you the results you want,
and don't blindly apply it.
"""
