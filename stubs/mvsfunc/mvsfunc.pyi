# flake8: noqa

import typing

import vapoursynth as vs

Profiles = typing.Literal["fast", "lc", "np", "high", "vn"]


def BM3D(input: vs.VideoNode, sigma: typing.Optional[typing.Union[float, typing.List[float]]] = None, radius1: typing.Optional[int] = None, radius2: typing.Optional[int] = None, profile1: typing.Optional[Profiles] = None, profile2: typing.Optional[Profiles] = None,
         refine: typing.Optional[int] = None, pre: typing.Optional[vs.VideoNode] = None, ref: typing.Optional[vs.VideoNode] = None, psample: typing.Optional[typing.Literal[0, 1]] = None,
         matrix: typing.Union[int, str, None] = None, full: typing.Optional[bool] = None,
         output: typing.Optional[typing.Literal[0, 1, 2]] = None, css: typing.Optional[str] = None, depth: typing.Optional[int] = None, sample: typing.Optional[typing.Literal[0, 1]] = None,
         dither: typing.Union[int, str, None] = None, useZ: typing.Optional[bool] = None, prefer_props: typing.Optional[bool] = None, ampo: typing.Optional[float] = None, ampn: typing.Optional[float] = None, dyn: typing.Optional[int] = None, staticnoise: typing.Optional[int] = None,
         cu_kernel: typing.Optional[str] = None, cu_taps: typing.Optional[int] = None, cu_a1: typing.Optional[float] = None, cu_a2: typing.Optional[float] = None, cu_cplace: typing.Optional[str] = None,
         cd_kernel: typing.Optional[str] = None, cd_taps: typing.Optional[int] = None, cd_a1: typing.Optional[float] = None, cd_a2: typing.Optional[float] = None, cd_cplace: typing.Optional[str] = None,
         block_size1: typing.Optional[int] = None, block_step1: typing.Optional[int] = None, group_size1: typing.Optional[int] = None, bm_range1: typing.Optional[int] = None, bm_step1: typing.Optional[int] = None, ps_num1: typing.Optional[int] = None, ps_range1: typing.Optional[int] = None, ps_step1: typing.Optional[int] = None, th_mse1: typing.Optional[float] = None, hard_thr: typing.Optional[float] = None,
         block_size2: typing.Optional[int] = None, block_step2: typing.Optional[int] = None, group_size2: typing.Optional[int] = None, bm_range2: typing.Optional[int] = None, bm_step2: typing.Optional[int] = None, ps_num2: typing.Optional[int] = None, ps_range2: typing.Optional[int] = None, ps_step2: typing.Optional[int] = None, th_mse2: typing.Optional[float] = None) -> vs.VideoNode: ...

def GetMatrix(clip: vs.VideoNode, matrix: typing.Optional[typing.Literal[0, "RGB", 1, "709", "bt709", 2, "Unspecified", 4, "FCC", 5, "bt470bg", 6, "601", "smpte170m", 7, "240", "smpte240m", 8, "YCgCo", "YCoCg", 9, "2020", "bt2020nc", 10, "2020cl", "bt2020c", 100, "OPP", "opponent"]] = None,
              dIsRGB: typing.Optional[bool] = None, id: bool = False
              ) -> typing.Union[str, int]: ...
