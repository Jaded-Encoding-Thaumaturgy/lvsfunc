# flake8: noqa

import typing

import vapoursynth as vs

core = vs.core


# this api is absolutely horrifying and doesn't make sense but it does what it does
def TAAmbk(clip: vs.VideoNode, aatype: typing.Union[str, int] = 1, aatypeu: typing.Union[str, int, None] = None, aatypev: typing.Union[str, int, None] = None, preaa: typing.Literal[0, 1, 2, -1] = 0, strength: float = 0.0, cycle: int = 0, mtype: typing.Optional[typing.Literal[0, 1, 2, 3]] = None, mclip: typing.Optional[vs.VideoNode] = None, mthr: typing.Union[float, int, typing.List[typing.Union[float, int]], typing.Tuple[typing.Union[float, int], ...], None] = None, mlthresh: typing.Union[float, int, typing.List[typing.Union[float, int]], typing.Tuple[typing.Union[float, int], ...], None] = None, mpand: typing.Union[float, int, typing.List[typing.Union[float, int]], typing.Tuple[typing.Union[float, int], ...]] = (0, 0), txtmask: typing.Union[float, int] = 0, txtfade: typing.Union[int, typing.List[int], typing.Tuple[int, ...]] = 0, thin: typing.Literal[0, 1] = 0, dark: float = 0.0, sharp: typing.Union[float, int] = 0, aarepair: int = 0, postaa: typing.Optional[bool] = None, src: typing.Optional[vs.VideoNode] = None, stabilize: typing.Literal[0, 1, 2, 3] = 0, down8: bool = True, showmask: typing.Literal[-1, 0, 1, 2, 3] = 0, opencl: bool =False, opencl_device: int = -1, **kwargs: typing.Any) -> vs.VideoNode: ...
