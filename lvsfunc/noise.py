from __future__ import annotations

import warnings
from typing import Any

import vapoursynth as vs
from vskernels import Bicubic, Kernel, Matrix, get_kernel, get_prop
from vsutil import Dither, depth, get_depth, get_y, join, plane

from .util import check_variable

core = vs.core


__all__ = [
    'chickendream',
    # Deprecated
    'bm3d'
]


def bm3d(clip: vs.VideoNode, sigma: float | list[float] = 0.75,
         radius: int | list[int] | None = None, ref: vs.VideoNode | None = None,
         pre: vs.VideoNode | None = None, refine: int = 1, matrix_s: str = "709",
         basic_args: dict[str, Any] = {}, final_args: dict[str, Any] = {}) -> vs.VideoNode:
    """
    BM3D denoising filter using the CPU.

    .. warning::
        | This function has been deprecated! It will be removed in a future commit.

    Dependencies:

    * `VapourSynth-BM3D <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-BM3D>`_

    :param clip:            Clip to process.
    :param sigma:           Denoising strength for both basic and final estimations.
    :param radius:          Temporal radius for both basic and final estimations.
    :param ref:             Reference clip for the final estimation.
    :param pre:             Prefiltered clip for the basic estimation.
    :param refine:          Iteration of the final clip.
                            0 = basic estimation only
                            1 = basic + final estimation
                            n = basic + n final estimations
    :param matrix_s:        Color matrix of the Clip to process.
    :param basic_args:      Args to pass to the basic estimation.
    :param final_args:      Args to pass to the final estimation.

    :return:                Denoised clip.

    :raises ValueError:     Invalid number of sigma parameters were passed.
    :raises ValueError:     Invalid number of radii parameters were passed.
    """
    try:
        import vsdenoise
    except ModuleNotFoundError:
        raise ModuleNotFoundError("bm3d: missing dependency `vsdenoise`!")

    warnings.warn('lvsfunc.bm3d: deprecated in favor of vsdenoise.BM3D!', DeprecationWarning)

    vsd_bm3d = vsdenoise.BM3D(clip, sigma, radius, vsdenoise.Profile.NORMAL, pre, ref, refine)
    vsd_bm3d.basic_args |= basic_args
    vsd_bm3d.final_args |= final_args

    return vsd_bm3d.clip


def chickendream(clip: vs.VideoNode, sigma: float = 0.35,
                 rad: float = 0.025, res: int = 1024,
                 chroma: bool = False, seed: int = 42069,
                 matrix: Matrix | int | None = None,
                 kernel: Kernel | str = Bicubic(b=0, c=1/2), **chkdr_args: Any) -> vs.VideoNode:
    """
    Realistic film grain generator.

    .. warning::
        | This function is _incredibly_ slow! It may take multiple minutes to render your clip!
        | If you still want to use it, I highly recommend setting ``draft=True``!

    The generated grain is quite significant, but you can blend the output with the input to attenuate the effect.
    For this function to work at its best, the image must be in linear light and MUST be an SRGB or GRAY clip.

    Please check the `chickendream GitHub page <https://github.com/EleonoreMizo/chickendream>`_
    for a full list of parameters and additional information.

    :param clip:            Clip to process.
    :param sigma:           Radius of the gaussian kernel for the vision filter.
                            The larger the radius, the smoother the picture. Smallest values are more prone to aliasing.
                            0 is a special value indicating that a single-pixel rectangular filter should be used
                            instead of a gaussian. For grains with a small radius (standard use), this should be
                            the fastest option, visually equivalent to sigma = 0.3, offering an excellent quality
                            (minimum leaking between adjascent pixels).
                            Valid ranges are between 0 and 1.
    :param rad:             Average grain radius, in pixels.
                            The smaller the grains, the higher the picture fidelity (given a high enough res),
                            and the slower the processing.
                            Must be greater than 0.
    :param res:             Filter resolution, directly translating into output data bitdepth. Must be greater than 0.
                            1024 is equivalent to a 10-bit output. Keep in mind that the pixel values are linear.
                            The higher the resolution, the slower the algorithm. Large grains require a smaller res.
    :param chroma:          Whether to process chroma or not.
                            If you pass a GRAY clip yourself, this parameter will be ignored.
    :param seed:            Seed for the random generator. Defaults to 42069.
    :param matrix:          Enum for the matrix of the Clip to process.
                            See :py:attr:`lvsfunc.types.Matrix` for more info.
                            If not specified, gets matrix from the "_Matrix" prop of the clip unless it's an RGB clip,
                            in which case it stays as `None`.
    :param kernel:          py:class:`vskernels.Kernel` object used for conversions between YUV <-> RGB.
                            This can also be the string name of the kernel
                            (Default: py:class:`vskernels.Bicubic(b=0, c=1/2)`).
    :param chkdr_args:      Additional args to pass to chickendream.

    :return:                Grained clip in the given clip's format.
    """
    assert check_variable(clip, "chickendream")

    chkdr_args |= dict(sigma=sigma, rad=rad, seed=seed, res=res)

    if isinstance(kernel, str):
        kernel = get_kernel(kernel)()

    bit_depth = get_depth(clip)
    is_rgb, is_gray = (clip.format.color_family is f for f in (vs.RGB, vs.GRAY))

    clip_32 = depth(clip, 32, dither_type=Dither.ERROR_DIFFUSION)

    if is_gray or (is_rgb and chroma):
        return depth(core.chkdr.grain(clip_32.std.Limiter(), **chkdr_args), bit_depth)

    if matrix is None:
        matrix = get_prop(clip.get_frame(0), "_Matrix", int)

    targ_matrix = Matrix(matrix)

    if is_rgb:
        input_clip = clip_32
    elif chroma:
        input_clip = kernel.resample(clip_32, vs.RGBS, matrix_in=targ_matrix).std.Limiter()
        input_clip = core.fmtc.transfer(input_clip, transs="srgb", transd="linear")
    else:
        input_clip = get_y(clip_32)

    run_chkdr = core.chkdr.grain(input_clip, **chkdr_args)

    if is_rgb:
        return depth(run_chkdr, bit_depth)
    elif chroma:
        return depth(core.fmtc.transfer(run_chkdr, transs="linear", transd="srgb"), bit_depth)
    else:
        return depth(join([run_chkdr, plane(clip_32, 1), plane(clip_32, 2)]), bit_depth)
