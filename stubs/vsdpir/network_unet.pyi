from typings import Optional, List

class UNetRes(nn.Module):
    def __init__(self, in_nc=Optional[int], out_nc=Optional[int], nc=Optional[List[int]], nb=Optional[int], act_mode=Optional[str], downsample_mode=Optional[str], upsample_mode=Optional[str]): ...
