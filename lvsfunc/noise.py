from __future__ import annotations

from typing import Any, Dict, List

import vapoursynth as vs
from vsutil import Dither, Range, depth, get_depth, get_y, iterate, join, plane

from .kernels import Bicubic, Kernel, get_kernel
from .types import Matrix
from .util import check_variable, get_prop

core = vs.core


__all__: List[str] = [
    'bm3d',
    'chickendream'
]


def bm3d(clip: vs.VideoNode, sigma: float | List[float] = 0.75,
         radius: int | List[int] | None = None, ref: vs.VideoNode | None = None,
         pre: vs.VideoNode | None = None, refine: int = 1, matrix_s: str = "709",
         basic_args: Dict[str, Any] = {}, final_args: Dict[str, Any] = {}) -> vs.VideoNode:
    """
    A wrapper function for the BM3D denoiser.

    Dependencies:

    * VapourSynth-BM3D

    :param clip:            Input clip
    :param sigma:           Denoising strength for both basic and final estimations
    :param radius:          Temporal radius for both basic and final estimations
    :param ref:             Reference clip for the final estimation
    :param pre:             Prefiltered clip for the basic estimation
    :param refine:          Iteration of the final clip.
                            0 = basic estimation only
                            1 = basic + final estimation
                            n = basic + n final estimations
    :param matrix_s:        Color matrix of the input clip
    :param basic_args:      Args to pass to the basic estimation
    :param final_args:      Args to pass to the final estimation

    :return:                Denoised clip
    """
    check_variable(clip, "bm3d")
    assert clip.format

    is_gray = clip.format.color_family == vs.GRAY

    def to_opp(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.resize.Bicubic(format=vs.RGBS, matrix_in_s=matrix_s).bm3d.RGB2OPP(sample=1)

    def to_fullgray(clip: vs.VideoNode) -> vs.VideoNode:
        return get_y(clip).resize.Point(format=vs.GRAYS, range_in=Range.LIMITED, range=Range.FULL)

    sigmal = [sigma] * 3 if not isinstance(sigma, list) else sigma + [sigma[-1]]*(3-len(sigma))
    sigmal = [sigmal[0], 0, 0] if is_gray else sigmal
    is_gray = True if sigmal[1] == 0 and sigmal[2] == 0 else is_gray

    if len(sigmal) != 3:
        raise ValueError("bm3d: 'invalid number of sigma parameters supplied!'")

    radiusl = [0, 0] if radius is None else [radius] * 2 if not isinstance(radius, list) \
        else radius + [radius[-1]]*(2-len(radius))

    if len(radiusl) != 2:
        raise ValueError("bm3d: 'invalid number or radius parameters supplied!'")

    if sigmal[0] == 0 and sigmal[1] == 0 and sigmal[2] == 0:
        return clip

    pre = pre if pre is None else to_opp(pre) if not is_gray else to_fullgray(pre)

    def basic(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.bm3d.Basic(sigma=sigmal, ref=pre, matrix=100, **basic_args) if radiusl[0] < 1 \
            else clip.bm3d.VBasic(sigma=sigmal, ref=pre, radius=radiusl[0], matrix=100, **basic_args) \
            .bm3d.VAggregate(radius=radiusl[0], sample=1)

    clip_in = to_opp(clip) if not is_gray else to_fullgray(clip)
    refv = basic(clip_in) if ref is None else to_opp(ref) if not is_gray else to_fullgray(ref)

    def final(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.bm3d.Final(sigma=sigmal, ref=refv, matrix=100, **final_args) if radiusl[1] < 1 \
            else clip.bm3d.VFinal(sigma=sigmal, ref=refv, radius=radiusl[1], matrix=100, **final_args) \
            .bm3d.VAggregate(radius=radiusl[1], sample=1)

    den = iterate(clip_in, final, refine)

    # boil everything back down to whatever input we had
    den = den.bm3d.OPP2RGB(sample=1).resize.Bicubic(format=clip.format.id, matrix_s=matrix_s) if not is_gray \
        else den.resize.Point(format=clip.format.replace(color_family=vs.GRAY, subsampling_w=0, subsampling_h=0).id,
                              range_in=Range.FULL, range=Range.LIMITED)
    # merge source chroma if it exists and we didn't denoise it
    den = core.std.ShufflePlanes([den, clip], planes=[0, 1, 2], colorfamily=vs.YUV) \
        if is_gray and clip.format.color_family == vs.YUV else den
    # sub clip luma back in if we only denoised chroma
    den = den if sigmal[0] != 0 else core.std.ShufflePlanes([clip, den], planes=[0, 1, 2], colorfamily=vs.YUV)

    return den


def chickendream(clip: vs.VideoNode, sigma: float = 0.35,
                 rad: float = 0.025, res: int = 1024,
                 chroma: bool = False, seed: int = 42069,
                 matrix: Matrix | int | None = None,
                 kernel: Kernel | str = Bicubic(b=0, c=0.5), **chkdr_args: Any) -> vs.VideoNode:
    """
    A wrapper around the graining plugin, `chickendream`,
    a plug-in that implements a realistic film grain generator.

    .. warning::
        | This function is _incredibly_ slow! It may take multiple minutes to render your clip!
        | If you still want to use it, I highly recommend setting ``draft=True``!

    The generated grain is quite significant, but you can blend the output with the input to attenuate the effect.
    For this function to work at its best, the image must be in linear light and MUST be an SRGB or GRAY clip.

    Please check the `chickendream GitHub page <https://github.com/EleonoreMizo/chickendream>`_
    for a full list of parameters and additional information.

    :param clip:            Input clip.
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
    :param matrix:          Enum for the matrix of the input clip. See ``types.Matrix`` for more info.
                            If not specified, gets matrix from the "_Matrix" prop of the clip unless it's an RGB clip,
                            in which case it stays as `None`.
    :param kernel:          `Kernel` object used for conversions between YUV <-> RGB.
    :param chkdr_args:      Additional args to pass to chickendream.

    :return:                Grained clip in the given clip's format.
    """
    check_variable(clip, "chickendream")
    assert clip.format

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
