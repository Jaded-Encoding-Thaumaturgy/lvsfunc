import vapoursynth as vs

from . import network_unet, utils_model

from typing import Optional

def DPIR(clip: vs.VideoNode, strength: Optional[float] = None, task: str = 'denoise',
         device_type: str = 'cuda', device_index: int = 0) -> vs.VideoNode: ...

def frame_to_tensor(f: vs.VideoFrame) -> torch.Tensor: ...
def tensor_to_frame(t: torch.Tensor, f: vs.VideoFrame) -> vs.VideoFrame: ...
