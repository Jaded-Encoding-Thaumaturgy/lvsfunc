# flake8: noqa

from typing import Any, Mapping

import vapoursynth as vs


def QTGMC(
    Input: vs.VideoNode, Preset: str = 'Slower',
    TR0: int | None = None, TR1: int | None = None, TR2: int | None = None,
    Rep0: int | None = None, Rep1: int = 0, Rep2: int | None = None,
    EdiMode: str | None = None, RepChroma: bool = True, NNSize: int | None = None,
    NNeurons: int | None = None, EdiQual: int = 1, EdiMaxD: int | None = None,
    ChromaEdi: str = '', EdiExt: vs.VideoNode | None = None, Sharpness: float | None = None,
    SMode: int | None = None, SLMode: int | None = None, SLRad: int | None = None,
    SOvs: int = 0, SVThin: float = 0.0, Sbb: int | None = None, SrchClipPP: int | None = None,
    SubPel: int | None = None, SubPelInterp: int = 2, BlockSize: int | None = None,
    Overlap: int | None = None, Search: int | None = None, SearchParam: int | None = None,
    elSearch: int | None = None, ChromaMotion: bool | None = None, TrueMotion: bool = False,
    Lambda: int | None = None, LSAD: int | None = None, PNew: int | None = None,
    PLevel: int | None = None, GlobalMotion: bool = True, DCT: int = 0, ThSAD1: int = 640,
    ThSAD2: int = 256, ThSCD1: int = 180, ThSCD2: int = 98, SourceMatch: int = 0,
    MatchPreset: str | None = None, MatchEdi: str | None = None, MatchPreset2: str | None = None,
    MatchEdi2: str | None = None, MatchTR2: int = 1, MatchEnhance: float = 0.5, Lossless: int = 0,
    NoiseProcess: int | None = None, EZDenoise: float | None = None, EZKeepGrain: float | None = None,
    NoisePreset: str = 'Fast', Denoiser: str | None = None, FftThreads: int = 1, DenoiseMC: bool | None = None,
    NoiseTR: int | None = None, Sigma: float | None = None, ChromaNoise: bool = False,
    ShowNoise: bool | float = 0.0, GrainRestore: float | None = None, NoiseRestore: float | None = None,
    NoiseDeint: str | None = None, StabilizeNoise: bool | None = None, InputType: int = 0,
    ProgSADMask: float | None = None, FPSDivisor: int = 1, ShutterBlur: int = 0, ShutterAngleSrc: float = 180.0,
    ShutterAngleOut: float = 180.0, SBlurLimit: int = 4, Border: bool = False, Precise: bool | None = None,
    Tuning: str = 'None', ShowSettings: bool = False, GlobalNames: str = 'QTGMC', PrevGlobals: str = 'Replace',
    ForceTR: int = 0, Str: float = 2.0, Amp: float = 0.0625, FastMA: bool = False, ESearchP: bool = False,
    RefineMotion: bool = False, TFF: bool | None = None, nnedi3_args: Mapping[str, Any] = {},
    eedi3_args: Mapping[str, Any] = {}, opencl: bool = False, device: int | None = None,
) -> vs.VideoNode:
    ...
