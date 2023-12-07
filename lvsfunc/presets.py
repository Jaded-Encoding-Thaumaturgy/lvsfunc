from vsdenoise import MotionMode, MVToolsPreset, Prefilter, SADMode, SearchMode

__all__: list[str] = [
    "MVLightPreset",
]


MVLightPreset = MVToolsPreset(
    block_size=16, overlap=8, range_conversion=3.5,
    sad_mode=(SADMode.ADAPTIVE_SPATIAL_MIXED, SADMode.ADAPTIVE_SATD_MIXED),
    search=SearchMode.DIAMOND, motion=MotionMode.HIGH_SAD,
    prefilter=Prefilter.DFTTEST(
        slocation=[(0.0, 1.0), (0.4, 3.2), (0.45, 40.0), (1.0, 48.0)],
        ssystem=1, planes=0
    )
)
"""Light's MVTools preset."""
