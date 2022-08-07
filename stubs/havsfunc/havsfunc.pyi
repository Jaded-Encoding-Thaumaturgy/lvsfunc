# flake8: noqa

from typing import Any, Mapping, Optional, Union

import vapoursynth as vs


def QTGMC(
    Input: vs.VideoNode, Preset: str = 'Slower',
    TR0: Optional[int] = None, TR1: Optional[int] = None, TR2: Optional[int] = None,
    Rep0: Optional[int] = None, Rep1: int = 0, Rep2: Optional[int] = None,
    EdiMode: Optional[str] = None, RepChroma: bool = True, NNSize: Optional[int] = None,
    NNeurons: Optional[int] = None, EdiQual: int = 1, EdiMaxD: Optional[int] = None,
    ChromaEdi: str = '', EdiExt: Optional[vs.VideoNode] = None, Sharpness: Optional[float] = None,
    SMode: Optional[int] = None, SLMode: Optional[int] = None, SLRad: Optional[int] = None,
    SOvs: int = 0, SVThin: float = 0.0, Sbb: Optional[int] = None, SrchClipPP: Optional[int] = None,
    SubPel: Optional[int] = None, SubPelInterp: int = 2, BlockSize: Optional[int] = None,
    Overlap: Optional[int] = None, Search: Optional[int] = None, SearchParam: Optional[int] = None, 
    elSearch: Optional[int] = None, ChromaMotion: Optional[bool] = None, TrueMotion: bool = False,
    Lambda: Optional[int] = None, LSAD: Optional[int] = None, PNew: Optional[int] = None,
    PLevel: Optional[int] = None, GlobalMotion: bool = True, DCT: int = 0, ThSAD1: int = 640,
    ThSAD2: int = 256, ThSCD1: int = 180, ThSCD2: int = 98, SourceMatch: int = 0,
    MatchPreset: Optional[str] = None, MatchEdi: Optional[str] = None, MatchPreset2: Optional[str] = None,
    MatchEdi2: Optional[str] = None, MatchTR2: int = 1, MatchEnhance: float = 0.5, Lossless: int = 0,
    NoiseProcess: Optional[int] = None, EZDenoise: Optional[float] = None, EZKeepGrain: Optional[float] = None,
    NoisePreset: str = 'Fast', Denoiser: Optional[str] = None, FftThreads: int = 1, DenoiseMC: Optional[bool] = None,
    NoiseTR: Optional[int] = None, Sigma: Optional[float] = None, ChromaNoise: bool = False,
    ShowNoise: Union[bool, float] = 0.0, GrainRestore: Optional[float] = None, NoiseRestore: Optional[float] = None,
    NoiseDeint: Optional[str] = None, StabilizeNoise: Optional[bool] = None, InputType: int = 0,
    ProgSADMask: Optional[float] = None, FPSDivisor: int = 1, ShutterBlur: int = 0, ShutterAngleSrc: float = 180.0,
    ShutterAngleOut: float = 180.0, SBlurLimit: int = 4, Border: bool = False, Precise: Optional[bool] = None,
    Tuning: str = 'None', ShowSettings: bool = False, GlobalNames: str = 'QTGMC', PrevGlobals: str = 'Replace',
    ForceTR: int = 0, Str: float = 2.0, Amp: float = 0.0625, FastMA: bool = False, ESearchP: bool = False,
    RefineMotion: bool = False, TFF: Optional[bool] = None, nnedi3_args: Mapping[str, Any] = {},
    eedi3_args: Mapping[str, Any] = {}, opencl: bool = False, device: Optional[int] = None,
) -> vs.VideoNode:
    ...
