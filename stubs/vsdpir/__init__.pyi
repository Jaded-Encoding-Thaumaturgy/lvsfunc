import vapoursynth as vs

from typing import Optional

def DPIR(clip: vs.VideoNode, strength: Optional[float] = None, task: str = 'denoise',
         device_type: str = 'cuda', device_index: int = 0) -> vs.VideoNode: ...
