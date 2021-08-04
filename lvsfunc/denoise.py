"""
    Denoising/Deblocking functions.
"""
from typing import Any, Dict, List, Optional, Tuple, Union, cast, Literal

import os.path as path
import vapoursynth as vs
import vsutil
from vsutil import depth

from .types import Matrix

core = vs.core


def bm3d(clip: vs.VideoNode, sigma: Union[float, List[float]] = 0.75,
         radius: Union[int, List[int], None] = None, ref: Optional[vs.VideoNode] = None,
         pre: Optional[vs.VideoNode] = None, refine: int = 1, matrix_s: str = "709",
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
    if clip.format is None:
        raise ValueError("bm3d: Variable format clips not supported")
    is_gray = clip.format.color_family == vs.GRAY

    def to_opp(clip: vs.VideoNode) -> vs.VideoNode:
        return clip.resize.Bicubic(format=vs.RGBS, matrix_in_s=matrix_s).bm3d.RGB2OPP(sample=1)

    def to_fullgray(clip: vs.VideoNode) -> vs.VideoNode:
        return vsutil.get_y(clip).resize.Point(format=vs.GRAYS, range_in=vsutil.Range.LIMITED, range=vsutil.Range.FULL)

    sigmal = [sigma] * 3 if not isinstance(sigma, list) else sigma + [sigma[-1]] * (3 - len(sigma))
    sigmal = [sigmal[0], 0, 0] if is_gray else sigmal
    is_gray = True if sigmal[1] == 0 and sigmal[2] == 0 else is_gray
    if len(sigmal) != 3:
        raise ValueError("bm3d: 'invalid number of sigma parameters supplied'")
    radiusl = [0, 0] if radius is None else [radius] * 2 if not isinstance(radius, list) \
        else radius + [radius[-1]] * (2 - len(radius))
    if len(radiusl) != 2:
        raise ValueError("bm3d: 'invalid number or radius parameters supplied'")

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

    den = vsutil.iterate(clip_in, final, refine)

    # boil everything back down to whatever input we had
    den = den.bm3d.OPP2RGB(sample=1).resize.Bicubic(format=clip.format.id, matrix_s=matrix_s) if not is_gray \
        else den.resize.Point(format=clip.format.replace(color_family=vs.GRAY, subsampling_w=0, subsampling_h=0).id,
                              range_in=vsutil.Range.FULL, range=vsutil.Range.LIMITED)
    # merge source chroma if it exists and we didn't denoise it
    den = core.std.ShufflePlanes([den, clip], planes=[0, 1, 2], colorfamily=vs.YUV) \
        if is_gray and clip.format.color_family == vs.YUV else den
    # sub clip luma back in if we only denoised chroma
    den = den if sigmal[0] != 0 else core.std.ShufflePlanes([clip, den], planes=[0, 1, 2], colorfamily=vs.YUV)

    return den


def autodb_dpir(clip: vs.VideoNode, edgevalue: int = 24,
                strength: Tuple[int, int, int] = (30, 50, 75),
                thrs: List[Tuple[float, float]] = [(2.0, 1.0), (3.0, 3.25), (5.0, 7.5)],
                matrix: Matrix = Matrix.BT709, debug: bool = False,
                device_type: Literal['cpu', 'cuda'] = 'cuda', device_index: int = 0, **kwargs: Any) -> vs.VideoNode:
    """
    A rewrite of fvsfunc.AutoDeblock that uses vspdir instead of dfttest to deblock.

    This function checks for differences between a frame and an edgemask with some processing done on it,
    and for differences between the current frame and the next frame.
    For frames where both thresholds are exceeded, it will perform deblocking at a specified strength.
    This will ideally be frames that show big temporal *and* spatial inconsistencies.

    Dependencies:

    * vs-dpir
    * rgsf

    :param clip:            Input clip
    :param edgevalue:       Remove edges from the edgemask that exceed this threshold
    :param strength:        DPIR strength values (higher is stronger)
    :param thrs:             Invididual thresholds, written as a List of (OrigDiff, NextFrameDiff)
    :param matrix:          Enum for the matrix of the input clip. See ``types.Matrix`` for more info
    :param device_type:     The device to use, can either be 'cpu' or 'cuda' if you have it.
    :param device_index:    The 'device_index' + 1º device of type 'device_type' in the system.
    :param debug:           Print calculations and how strong the denoising is.

    :return:                Deblocked clip
    """
    import torch
    import vsdpir as dpir

    assert clip.format

    def _eval_db(n: int, f: List[vs.VideoFrame]) -> vs.VideoNode:
        mode, i = 'unfiltered passthrough', None

        OrigDiff, YNextDiff = cast(float, f[1].props.OrigDiff), cast(float, f[2].props.YNextDiff)

        if f[0].props['_PictType'] == b'I':
            YNextDiff = (YNextDiff + OrigDiff) / 2

        if OrigDiff > thrs[2][0] and YNextDiff > thrs[2][1]:
            mode, i = 'strong deblocking', 2
        elif OrigDiff > thrs[1][0] and YNextDiff > thrs[1][1]:
            mode, i = 'medium deblocking', 1
        elif OrigDiff > thrs[0][0] and YNextDiff > thrs[0][1]:
            mode, i = 'weak deblocking', 0
        else:
            if debug:
                print_debug(n, f, mode)
            return f[0]

        if debug:
            print_debug(n, f, mode, thrs[i])

        img_L = dpir.frame_to_tensor(f[0])
        img_L = torch.cat((img_L, noise_level_maps[i]), dim=1)
        img_L = img_L.to(device)

        if img_L.shape[2] // 8 == 0 and img_L.shape[3] // 8 == 0:
            img_E = models[i](img_L)
        else:
            img_E = dpir.utils_model.test_mode(models[i], img_L, refield=64, mode=5)

        return dpir.tensor_to_frame(img_E, f[0])

    original_format = clip.format

    if not clip.format.color_family == vs.RGB:
        clip = depth(clip, 32).std.SetFrameProp('_Matrix', intval=matrix)
        clip = core.resize.Bicubic(clip, format=vs.RGBS)

    maxvalue = (1 << original_format.bits_per_sample) - 1
    orig = core.std.Prewitt(clip)
    orig = core.std.Expr(orig, f"x {edgevalue} >= {maxvalue} x ?")
    orig_d = orig.rgsf.RemoveGrain(2) \
        .std.Convolution(matrix=[1, 2, 1, 2, 4, 2, 1, 2, 1])

    difforig = core.std.PlaneStats(orig_d, orig, prop='Orig')
    diffnext = core.std.PlaneStats(orig, orig_d.std.DeleteFrames([0]), prop='YNext')
    
    torch_args = (1, 1, clip.height, clip.width)
    
    noise_level_maps = [torch.ones(*torch_args).mul_(torch.FloatTensor([s / 100])).float() for s in strength]

    device = torch.device(device_type, device_index)

    dpir_model_path = path.join(path.dirname(dpir.__file__), 'drunet_deblocking_color.pth')
    dpir_model = dpir.network_unet.UNetRes(
        in_nc=4, out_nc=3, nc=[64, 128, 256, 512], nb=4, act_mode='R',
        downsample_mode='strideconv', upsample_mode='convtranspose'
    )
    dpir_model.load_state_dict(torch.load(dpir_model_path), strict=True)

    for _, v in dpir_model.named_parameters():
        v.requires_grad = False

    models = [dpir_model.eval().to(device) for _ in range(3)]

    thrs = [[x / 219 for x in y] for y in thrs]

    deblock = core.std.ModifyFrame(clip, [clip, difforig, diffnext], _eval_db)

    return core.resize.Bicubic(deblock, format=original_format.id, matrix=matrix)


def print_debug(n: int, f: List[vs.VideoFrame], mode: str, thrs: List[Tuple[int, int]] = None):
    first_thr, second_thr = (f" (thrs: {thrs[0]})", f" (thrs: {thrs[1]})") if thrs is not None else ('', '')
    print(
        f'Frame {n}: {mode} / OrigDiff: {f[1].props.OrigDiff}' +
        first_thr + f'/ YNextDiff: {f[2].props.YNextDiff}' + second_thr
    )
