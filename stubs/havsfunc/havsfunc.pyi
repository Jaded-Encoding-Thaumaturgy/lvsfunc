# flake8: noqa

import typing

import vapoursynth as vs


def SMDegrain(input: vs.VideoNode, tr: typing.Literal[1, 2, 3] = 2, thSAD: int = 300, thSADC: typing.Optional[int] = None, RefineMotion: bool = False,
              contrasharp: typing.Union[bool, int, None] = None, CClip: typing.Optional[vs.VideoNode] = None, interlaced: bool = False, tff: typing.Optional[bool] = None,
              plane: int = 4, Globals: int = 0, pel: typing.Optional[typing.Literal[1, 2, 4]] = None, subpixel: typing.Literal[0, 1, 2] = 2, prefilter: typing.Union[int, vs.VideoNode] = -1,
              mfilter: typing.Optional[vs.VideoNode] = None, blksize: typing.Optional[typing.Literal[4, 8, 16, 32]] = None, overlap: typing.Optional[int] = None, search: int = 4,
              truemotion: typing.Optional[bool] = None, MVglobal: typing.Optional[bool] = None, dct: int = 0, limit: int = 255, limitc: typing.Optional[int] = None,
              thSCD1: int = 400, thSCD2: int = 130, chroma: bool = True, hpad: typing.Optional[int] = None, vpad: typing.Optional[int] = None,
              Str: float = 1.0, Amp: float = 0.0625) -> vs.VideoNode: ...


def QTGMC(clip: vs.VideoNode, *args: typing.Any, **kwargs: typing.Any) -> vs.VideoNode: ...

def DitherLumaRebuild(src: vs.VideoNode, s0: float = 2.0, c: float = 0.0625, chroma: bool = True) -> vs.VideoNode: ...
