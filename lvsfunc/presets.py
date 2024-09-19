from vsdenoise import MotionMode, MVToolsPreset, Prefilter, SADMode, SearchMode

__all__: list[str] = [
    'MVLightPreset',
]


MVLightPreset = MVToolsPreset(
    block_size=16, overlap=8,
    range_conversion=4.5,
    sad_mode=SADMode.SPATIAL.same_recalc,
    search=SearchMode.DIAMOND,
    motion=MotionMode.HIGH_SAD,
    prefilter=Prefilter.DFTTEST(
        sloc=[(0.0, 1.0), (0.4, 2.4), (0.45, 32.0), (1.0, 64.0)],
        ssystem=1, planes=None
    ),
    planes=None
)
"""Light's MVTools preset."""
