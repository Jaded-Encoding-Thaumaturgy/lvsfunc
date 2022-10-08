from __future__ import annotations

from typing import Any

from vskernels import Catrom, Kernel, KernelT
from vstools import DitherType, Matrix, check_variable, core, depth, get_depth, get_prop, get_y, join, plane, vs

__all__ = [
    'chickendream'
]


def chickendream(clip: vs.VideoNode, sigma: float = 0.35,
                 rad: float = 0.025, res: int = 1024,
                 chroma: bool = False,
                 luma_scaling: float = 10,
                 seed: int = 42069,
                 show_mask: bool = False,
                 draft: bool = True,
                 matrix: Matrix | int | None = None,
                 kernel: KernelT = Catrom,
                 **chkdr_args: Any) -> vs.VideoNode:
    """
    Realistic film grain generator.

    .. warning::
        | This function is _incredibly_ slow! It may take multiple minutes to render your clip!
        | If you still want to use it, I highly recommend setting ``draft=True``!

    The generated grain is quite significant, but you can blend the output with the input to attenuate the effect.
    For this function to work at its best, the image must be in linear light and MUST be an SRGB or GRAY clip.

    Please check out the `chickendream GitHub page <https://github.com/EleonoreMizo/chickendream>`_
    for a full list of parameters and additional information.

    Dependencies:

    * `chickendream <https://github.com/EleonoreMizo/chickendream>`_

    Optional Dependencies:

    * `adaptivegrain <https://github.com/Irrational-Encoding-Wizardry/adaptivegrain>_` (luma_scaling > 0)

    :param clip:            Input clip.
    :param sigma:           Radius of the gaussian kernel for the vision filter.
                            The larger the radius, the smoother the picture. Smallest values are more prone to aliasing.
                            0 is a special value indicating that a single-pixel rectangular filter should be used
                            instead of a gaussian. For grains with a small radius (standard use), this should be
                            the fastest option, visually equivalent to sigma = 0.3, offering an excellent quality
                            (minimum leaking between adjascent pixels).

                            Valid ranges are between 0 and 1.
                            This is implicitly set to 0 if `draft=True`.
    :param rad:             Average grain radius, in pixels.
                            The smaller the grains, the higher the picture fidelity (given a high enough res),
                            and the slower the processing.
                            Must be greater than 0.
    :param res:             Filter resolution, directly translates into the output data bitdepth.
                            Must be greater than 0.

                            1024 is equivalent to a 10-bit output. Keep in mind that the pixel values are linear.

                            The higher the resolution, the slower the algorithm. Large grains require a smaller res.
    :param chroma:          Whether to process chroma or not.
                            If you pass a GRAY clip, this parameter will be ignored.
    :param luma_scaling:    Scaling for the luma mask. Setting this to 0 will disable it.
    :param seed:            Seed for the random generator. Defaults to 42069.
    :param show_mask:       Return the luma mask. Default: False.
    :param draft:           Enables the draft mode, much faster to render, but only gives meaningful results
                            for a small subset of the parameter combinations.
                            Implicitely sets sigma to 0, and works correctly with the same conditions (low rad and dev).

                            This is the recommended modus for graining,
                            as there is a massive speed increase associated with this setting.

                            Set to `False` to disable and go back to significantly-slower-but-more-accurate graining.
    :param matrix:          Enum for the matrix of the input clip to process.
                            See :py:attr:`lvsfunc.types.Matrix` for more info.

                            If not specified, gets matrix from the "_Matrix" prop of the clip unless it's an RGB clip,
                            in which case it stays as `None`.
    :param kernel:          py:class:`vskernels.Kernel` object used for conversions between YUV <-> RGB.
                            This can also be the string name of the kernel
                            (Default: py:class:`vskernels.Catrom`).
    :param chkdr_args:      Additional args to pass to chickendream.

    :return:                Grained clip in the input clip's format.
    """
    assert check_variable(clip, "chickendream")

    chkdr_args |= dict(sigma=sigma, rad=rad, seed=seed, res=res, draft=draft)

    if luma_scaling > 0:
        adap_mask = clip.std.PlaneStats().adg.Mask(luma_scaling)
    else:
        adap_mask = clip.std.BlankClip(keep=True).std.Invert()

    if show_mask:
        return adap_mask

    kernel = Kernel.ensure_obj(kernel)

    bit_depth = get_depth(clip)
    is_rgb, is_gray = (clip.format.color_family is f for f in (vs.RGB, vs.GRAY))

    clip_32 = depth(clip, 32, dither_type=DitherType.ERROR_DIFFUSION)

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
        out_clip = depth(run_chkdr, bit_depth)
    elif chroma:
        out_clip = depth(core.fmtc.transfer(run_chkdr, transs="linear", transd="srgb"), bit_depth)
    else:
        out_clip = depth(join([run_chkdr, plane(clip_32, 1), plane(clip_32, 2)]), bit_depth)

    return core.std.MaskedMerge(clip, out_clip, adap_mask)
