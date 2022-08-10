from __future__ import annotations

import warnings
from functools import partial
from math import ceil
from typing import Any, Callable, cast

import vapoursynth as vs
import vsaa
from vsaa import Eedi3SR, Nnedi3SS, SingleRater, SuperSampler
from vskernels import Bicubic, Box, Catrom, Point
from vsscale import GenericScaler, ssim_downsample
from vsutil import depth, fallback, get_depth, get_y, join, plane, scale_value

from .util import check_variable

core = vs.core


__all__ = [
    'based_aa',
    # Deprecated
    'taa',
    'clamp_aa',
    'nneedi3_clamp',
    'nnedi3', 'eedi3',
    'transpose_aa',
    'upscaled_sraa', 'sraa',
]


def clamp_aa(src: vs.VideoNode, weak: vs.VideoNode, strong: vs.VideoNode, strength: float = 1) -> vs.VideoNode:
    """
    Clamp stronger AAs to weaker AAs.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    Useful for clamping :py:func:`lvsfunc.aa.upscaled_sraa` or :py:func:`lvsfunc.aa.eedi3`
    to :py:func:`lvsfunc.aa.nnedi3` for a strong but more precise AA.

    Original function written by `Zastin <https://github.com/kgrabs>`_, modified by LightArrowsEXE.

    :param src:         Non-AA'd source clip.
    :param weak:        Weakly-AA'd clip (eg: :py:func:`lvsfunc.aa.nnedi3`).
    :param strong:      Strongly-AA'd clip (eg: :py:func:`lvsfunc.aa.eedi3`).
    :param strength:    Clamping strength (Default: 1).

    :return:            Clip with clamped anti-aliasing.
    """

    warnings.warn('lvsfunc.clamp_aa: deprecated in favor of vsaa.clamp_aa!', DeprecationWarning)

    return vsaa.clamp_aa(src, weak, strong, strength)


def taa(clip: vs.VideoNode, aafun: Callable[[vs.VideoNode], vs.VideoNode] | SingleRater) -> vs.VideoNode:
    """
    Perform transpose AA.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    Example for nnedi3cl: taa(clip, nnedi3(opencl=True))

    :param clip:        Clip to process.
    :param aafun:       Antialiasing function.

    :return:            Antialiased clip.
    """

    warnings.warn('lvsfunc.taa: deprecated in favor of vsaa.transpose_aa!', DeprecationWarning)

    if isinstance(aafun, SingleRater):
        aafunc = aafun
    else:
        class _TempAA(SingleRater):
            def _interpolate(self, clip: vs.VideoNode, double_y: bool, **kwargs: Any) -> vs.VideoNode:
                return aafun(clip, **kwargs)  # type: ignore

        aafunc = _TempAA()

    return vsaa.transpose_aa(clip, aafunc)


def nnedi3(opencl: bool = False, **override: Any) -> Callable[[vs.VideoNode], vs.VideoNode]:
    """
    Generate nnedi3 antialiaser.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    Dependencies:

    * `VapourSynth-nnedi3 <https://github.com/dubhater/VapourSynth-nnedi3>`_
    * `VapourSynth-NNEDI3CL <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-NNEDI3CL>`_

    :param opencl:          Use OpenCL (Default: False).
    :param override:        nnedi3 parameter overrides.

    :return:                Configured nnedi3 function.
    """
    nnedi3_args: dict[str, Any] = dict(field=0, dh=True, nsize=3, nns=3, qual=1)
    nnedi3_args.update(override)

    warnings.warn('lvsfunc.nnedi3: deprecated in favor of vsaa.Nnedi3!', DeprecationWarning)

    return partial(vsaa.Nnedi3(**nnedi3_args, opencl=opencl)._interpolate, double_y=True)


def eedi3(opencl: bool = False, **override: Any) -> Callable[[vs.VideoNode], vs.VideoNode]:
    """
    Generate eedi3 antialiaser.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    Dependencies:

    * `VapourSynth-EEDI3 <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3>`_

    :param opencl:          Use OpenCL (Default: False).
    :param override:        eedi3 parameter overrides.

    :return:                Configured eedi3 function.
    """
    eedi3_args: dict[str, Any] = dict(field=0, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20)
    eedi3_args.update(override)

    warnings.warn('lvsfunc.eedi3: deprecated in favor of vsaa.Eedi3!', DeprecationWarning)

    return partial(vsaa.Eedi3(**eedi3_args, opencl=opencl)._interpolate, double_y=True)


def nneedi3_clamp(clip: vs.VideoNode, strength: float = 1,
                  mask: vs.VideoNode | None = None,
                  mthr: float = 0.25, opencl: bool = False) -> vs.VideoNode:
    """
    Clamp eedi3 to nnedi3 for the purpose of reducing eedi3 artifacts.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    This should fix `every issue created by eedi3 <https://i.imgur.com/hYVhetS.jpg>`_.

    Original function written by `Zastin <https://github.com/kgrabs>`_, modified by LightArrowsEXE.

    :param clip:                Clip to process.
    :param strength:            Set threshold strength for over/underflow value for clamping eedi3's result.
                                to nnedi3 +/- strength * 256 scaled to 8 bit (Default: 1)
    :param mask:                Clip to use for custom mask (Default: None).
    :param mthr:                Binarize threshold for the mask, scaled to float (Default: 0.25).
    :param opencl:              OpenCL acceleration (Default: False).

    :return:                    Antialiased clip.
    """

    warnings.warn('lvsfunc.nneedi3_clamp: deprecated in favor of vsaa.fine_aa!', DeprecationWarning)

    return vsaa.masked_clamp_aa(clip, strength, mthr, mask, opencl=opencl)


def transpose_aa(clip: vs.VideoNode, eedi3: bool = False, rep: int = 13) -> vs.VideoNode:
    """
    Tranpose and aa a clip multiple times using nnedi3/eedi3.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    This results in overall stronger anti-aliasing.
    Useful for shows like Yuru Camp with bad line-art problems.

    Original function written by `Zastin <https://github.com/kgrabs>`_, modified by LightArrowsEXE.

    Dependencies:

    * `RGSF <https://github.com/IFeelBloated/RGSF>`_ (optional: 32 bit clip)
    * `VapourSynth-EEDI3 <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3>`_
    * `VapourSynth-nnedi3 <https://github.com/dubhater/VapourSynth-nnedi3>`_
    * `znedi3 <https://github.com/sekrit-twc/znedi3>`_

    :param clip:      Clip to process.
    :param eedi3:     Use eedi3 for the interpolation (Default: False).
    :param rep:       Repair mode. Pass it 0 to not repair (Default: 13).

    :return:          Antialiased clip.
    """

    warnings.warn('lvsfunc.transpose_aa: deprecated in favor of vsaa.fine_aa!', DeprecationWarning)

    return vsaa.fine_aa(clip, True, vsaa.Eedi3() if eedi3 else vsaa.Nnedi3(), rep)


def upscaled_sraa(clip: vs.VideoNode,
                  rfactor: float = 1.5,
                  width: int | None = None, height: int | None = None,
                  supersampler: Callable[[vs.VideoNode, int, int], vs.VideoNode] | SuperSampler = Nnedi3SS(),
                  downscaler: Callable[[vs.VideoNode, int, int], vs.VideoNode] | None
                  = Bicubic(b=0, c=1/2).scale,
                  aafun: Callable[[vs.VideoNode], vs.VideoNode] | SingleRater = Eedi3SR()) -> vs.VideoNode:
    """
    Super-sampled single-rate AA for heavy aliasing and broken line-art.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    It works by super-sampling the clip, performing AA, and then downscaling again.
    Downscaling can be disabled by setting `downscaler` to `None`, returning the super-sampled luma clip.
    The dimensions of the downscaled clip can also be adjusted by setting `height` or `width`.
    Setting either `height` or `width` will also scale the chroma accordingly.

    Original function written by `Zastin <https://github.com/kgrabs>`_, modified by LightArrowsEXE.

    Alias for this function is ``lvsfunc.sraa``.

    Dependencies:

    * `VapourSynth-EEDI3 <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3>`_ (default aafun)
    * `VapourSynth-nnedi3 <https://github.com/dubhater/VapourSynth-nnedi3>`_ (default super-sampler and aafun)

    :param clip:            Clip to process.
    :param rfactor:         Image enlargement factor. 1.3..2 makes it comparable in strength to vsTAAmbk.
                            It is not recommended to go below 1.3 (Default: 1.5)
    :param width:           Target resolution width. If None, determined from `height`.
    :param height:          Target resolution height (Default: ``clip.height``).
    :param supersampler:    Super-sampler used for upscaling before AA (Default: nnedi3 super-sampler).
    :param downscaler:      Downscaler to use after super-sampling (Default: Bicubic(b=0, c=1/2).
    :param aafun:           Function used to antialias after super-sampling (Default: eedi3 with nnedi3 sclip).

    :return:                Antialiased clip.

    :raises ValueError:     ``rfactor`` is not above 1.
    """

    warnings.warn('lvsfunc.upscaled_sraa: deprecated in favor of vsaa.upscaled_sraa!', DeprecationWarning)

    if isinstance(supersampler, SuperSampler):
        ssfunc = supersampler
    else:
        ssfunc = cast(SuperSampler, GenericScaler(supersampler))

    if isinstance(aafun, SingleRater):
        aafunc = aafun
    else:
        class _TempAA(SingleRater):
            def _interpolate(self, clip: vs.VideoNode, double_y: bool, **kwargs: Any) -> vs.VideoNode:
                return aafun(clip, **kwargs)  # type: ignore

        aafunc = _TempAA()

    downfunc = GenericScaler(downscaler) if downscaler else Catrom()

    return vsaa.upscaled_sraa(
        clip, rfactor, width, height, ssfunc, aafunc, vsaa.AADirection.BOTH, downfunc
    )


def based_aa(clip: vs.VideoNode, shader_file: str = "FSRCNNX_x2_56-16-4-1.glsl",
             rfactor: float = 2.0, tff: bool = True,
             mask_thr: float = 60, show_mask: bool = False,
             lmask: vs.VideoNode | None = None, **eedi3_args: Any) -> vs.VideoNode:
    """
    Based anti-aliaser written by the based `Zastin <https://github.com/kgrabs>`_.

    This function relies on FSRCNNX being very sharp,
    and as such it very much acts like the main "AA" here.

    Original function written by `Zastin <https://github.com/kgrabs>`_, modified by LightArrowsEXE.

    Dependencies:

    * `VapourSynth-EEDI3 <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-EEDI3>`_
    * `vs-placebo <https://github.com/Lypheo/vs-placebo>`_

    :param clip:            Clip to process.
    :param shader_file:     Path to FSRCNNX shader file.
    :param rfactor:         Image enlargement factor.
    :param tff:             Top-Field-First if true, Bottom-Field-First if false.
    :param mask_thr:        Threshold for the edge mask binarisation.
                            Scaled internally to match bitdepth of clip.
    :param show_mask:       Output mask.
    :param eedi3_args:      Additional args to pass to eedi3.
    :param lmask:           Line mask clip to use for eedi3.

    :return:                AA'd clip or mask clip.

    :raises ValueError:     ``l_mask`` is passed and '`mask_thr` is higher than 255.
    """
    def _eedi3s(clip: vs.VideoNode, mclip: vs.VideoNode | None = None,
                **eedi3_kwargs: Any) -> vs.VideoNode:
        edi_args: dict[str, Any] = {  # Eedi3 args for `eedi3s`
            'field': int(tff), 'alpha': 0.125, 'beta': 0.25, 'gamma': 40,
            'nrad': 2, 'mdis': 20,
            'vcheck': 2, 'vthresh0': 12, 'vthresh1': 24, 'vthresh2': 4
        }
        edi_args |= eedi3_kwargs

        out = core.eedi3m.EEDI3(clip, dh=False, sclip=clip, planes=0, **edi_args)

        if mclip:
            return core.std.Expr([clip, out, mclip], 'z y x ?')
        return out

    def _resize_mclip(mclip: vs.VideoNode,
                      width: int | None = None,
                      height: int | None = None
                      ) -> vs.VideoNode:
        iw, ih = mclip.width, mclip.height
        ow, oh = fallback(width, iw), fallback(height, ih)

        if (ow > iw and ow/iw != ow//iw) or (oh > ih and oh/ih != oh//ih):
            mclip = Point().scale(mclip, iw * ceil(ow / iw), ih * ceil(oh / ih))

        return Box(fulls=1, fulld=1).scale(mclip, ow, oh)

    assert check_variable(clip, "based_aa")

    aaw = (round(clip.width * rfactor) + 1) & ~1
    aah = (round(clip.height * rfactor) + 1) & ~1

    clip_y = get_y(clip)

    if not lmask:
        if mask_thr > 255:
            raise ValueError(f"based_aa: '`mask_thr` must be equal to or lower than 255 (current: {mask_thr})!'")

        mask_thr = scale_value(mask_thr, 8, get_depth(clip))

        lmask = clip_y.std.Prewitt().std.Binarize(mask_thr).std.Maximum().std.BoxBlur(0, 1, 1, 1, 1).std.Limiter()

    mclip_up = _resize_mclip(lmask, aaw, aah)

    if show_mask:
        return lmask

    aa = depth(clip_y, 16).std.Transpose()
    aa = join([aa] * 3).placebo.Shader(shader=shader_file, filter='box', width=aa.width * 2, height=aa.height * 2)
    aa = depth(aa, get_depth(clip_y))
    aa = ssim_downsample(get_y(aa), aah, aaw)
    aa = _eedi3s(aa, mclip=mclip_up.std.Transpose(), **eedi3_args).std.Transpose()
    aa = ssim_downsample(_eedi3s(aa, mclip=mclip_up, **eedi3_args), clip.width, clip.height)
    aa = depth(aa, get_depth(clip_y))

    aa_merge = core.std.MaskedMerge(clip_y, aa, lmask)

    if clip.format.num_planes == 1:
        return aa_merge
    return join([aa_merge, plane(clip, 1), plane(clip, 2)])


# Aliases
sraa = upscaled_sraa
