"""
    Various functions I make use of often and other people might be able to use too.
    Suggestions and fixes are always appreciated!
"""

from functools import partial
import random

import fvsfunc as fvf  # https://github.com/Irrational-Encoding-Wizardry/fvsfunc
import havsfunc as hvf  # https://github.com/HomeOfVapourSynthEvolution/havsfunc
import kagefunc as kgf  # https://github.com/Irrational-Encoding-Wizardry/kagefunc
import mvsfunc as mvf  # https://github.com/HomeOfVapourSynthEvolution/mvsfunc
from nnedi3_rpow2 import \
    nnedi3_rpow2  # https://github.com/darealshinji/vapoursynth-plugins/blob/master/scripts/nnedi3_rpow2.py
from vsTAAmbk import TAAmbk  # https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk
from vsutil import *  # https://github.com/Irrational-Encoding-Wizardry/vsutil

core = vs.core

# optional dependencies: (http://www.vapoursynth.com/doc/pluginlist.html)
#     waifu2x-caffe
#     L-SMASH Source
#     d2vsource
#     FFMS2

# TODO: Write function that only masks px of a certain color/threshold of colors


def compare(clip_a: vs.VideoNode, clip_b: vs.VideoNode, frames: int = None,
            rand_frames: bool = False, rand_total: int = None,
            force_resample: bool = False) -> vs.VideoNode:
    """
    Allows for the same frames from two different clips to be compared by putting them next to each other in a list.
    Shorthand for this function is "comp".

    :rand_frames: bool: Pick random frames from the given clips
    :rand_total: int: Amount of random frames to pick
    :param force_resample: bool: Force resample the second clip to match the first.

    """
    if force_resample:
        clip_b = clip_b.resize.Bicubic(clip_a.width, clip_a.height, format=clip_a.format)
    elif clip_a.format.id != clip_b.format.id:
        raise ValueError('compare: The format of both clips must be equal')

    if rand_frames:
        if rand_total is None:
            # More comparisons for shorter clips so you can compare stuff like NCs more conveniently
            rand_total = int(clip_a.num_frames/1000) if clip_a.num_frames > 5000 else int(clip_a.num_frames/100)
        frames = sorted(random.sample(range(1, clip_a.num_frames-1), rand_total))
    elif frames is None:
        raise ValueError('compare: No frames given')

    pairs = (clip_a[frame] + clip_b[frame] for frame in frames)
    return sum(pairs, next(pairs))


def stack_compare(*clips: vs.VideoNode, width: int = None, height: int = None,
                  stack_vertical: bool = False) -> vs.VideoNode:
    """
    A simple wrapper that allows you to compare two clips by stacking them.
    You can stack an infinite amount of clips.

    Best to use when trying to match two sources frame-accurately, however by setting height to the source's
    height (or None), it can be used for comparing frames.

    Shorthand for this function is 'scomp'.

    """
    if len(set([c.format.id for c in clips])) != 1:
        raise ValueError('stack_compare: The format of every clip must be equal')

    height = fallback(height, clips[0].height)
    width = fallback(width, (get_w(height, aspect_ratio=clips[0].width / clips[0].height)))
    clips = [c.resize.Bicubic(width, height) for c in clips]

    return core.std.StackVertical(clips) if stack_vertical else core.std.StackHorizontal(clips)


# TO-DO: Apply descale based on average error in a frame range rather than on a per-frame basis
#        in order to prevent visible differences. Chances are if a couple of frames in a cut can't
#        be descaled, all of them are no good.
def conditional_descale(clip: vs.VideoNode, height: int,
                        b: float = 1 / 3, c: float = 1 / 3,
                        threshold: float = 0.003,
                        w2x: bool = False) -> vs.VideoNode:
    """
    Descales and reupscales a clip. If the difference exceeds the threshold, the frame will not be descaled.
    If it does not exceed the threshold, the frame will upscaled using either nnedi3_rpow2 or waifu2x-caffe.

    Useful for bad BDs that have additional post-processing done on some scenes, rather than all of them.

    Currently only works with bicubic, and has no native 1080p masking.
    Consider scenefiltering OP/EDs with a different descale function instead.

    The code for _get_error was mostly taken from kageru's Made in Abyss script.
    Special thanks to Lypheo for holding my hand as this was written.

    :param height: int:  Target descaled height.
    :param w2x: bool:  Whether or not to use waifu2x-caffe upscaling. (Default value = False)

    """
    def _get_error(clip, height, b, c):
        descale = core.descale.Debicubic(clip, get_w(height), height, b=b, c=c)
        upscale = core.resize.Bicubic(descale, clip.width, clip.height, filter_param_a=b, filter_param_b=c)
        diff = core.std.PlaneStats(upscale, clip)
        return descale, diff

    def _diff(n, f, clip, descaled, threshold):
        if f.props.PlaneStatsDiff > threshold:
            return clip
        else:
            return descaled

    if get_depth(clip) != 32:
        clip = fvf.Depth(clip, 32, dither_type='none')

    y, u, v = kgf.split(clip)
    descaled, diff = _get_error(y, height=height, b=b, c=c)

    if w2x:
        descaled = core.caffe.Waifu2x(descaled, noise=-1, scale=2, model=6, cudnn=True, processor=0,  tta=False)
    else:
        descaled = nnedi3_rpow2(descaled)

    descaled = descaled.resize.Bicubic(clip.width, clip.height, format=clip.format)

    descaled = descaled.std.SetFrameProp("_descaled", intval=1)
    clip = clip.std.SetFrameProp("_descaled", intval=0)

    f_eval = core.std.FrameEval(clip, partial(_diff, clip=clip, descaled=descaled, threshold=threshold),  diff)

    return kgf.join([f_eval, u, v])


def transpose_aa(clip: vs.VideoNode, eedi3: bool = False) -> vs.VideoNode:
    """
    Function written by Zastin and modified by me.
    Performs anti-aliasing over a clip by using Nnedi3, transposing, using Nnedi3 again, and transposing a final time.
    This results in overall stronger anti-aliasing.
    Useful for shows like Yuru Camp with bad lineart problems.

    :param eedi3: bool:  When true, uses eedi3 instead. (Default value = False)

    """
    src_y = get_y(clip)

    if eedi3:
        def _aa(src_y):
            src_y = src_y.std.Transpose()
            src_y = src_y.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            src_y = src_y.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            src_y = src_y.resize.Spline36(clip.height, clip.width, src_top=.5)
            src_y = src_y.std.Transpose()
            src_y = src_y.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            src_y = src_y.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            src_y = src_y.resize.Spline36(clip.width, clip.height, src_top=.5)
            return src_y
    else:
        def _aa(src_y):
            src_y = src_y.std.Transpose()
            src_y = src_y.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            src_y = src_y.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            src_y = src_y.resize.Spline36(clip.height, clip.width, src_top=.5)
            src_y = src_y.std.Transpose()
            src_y = src_y.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            src_y = src_y.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            src_y = src_y.resize.Spline36(clip.width, clip.height, src_top=.5)
            return src_y

    def _csharp(flt, src):
        blur = core.std.Convolution(flt, [1] * 9)
        return core.std.Expr([flt, src, blur], 'x y < x x + z - x max y min x x + z - x min y max ?')

    aaclip = _aa(src_y)
    aaclip = _csharp(aaclip, src_y).rgvs.Repair(src_y, 13)

    return aaclip if clip.format.color_family is vs.GRAY else core.std.ShufflePlanes([aaclip, clip], [0, 1, 2], vs.YUV)


def nneedi3_clamp(clip: vs.VideoNode, mask: vs.VideoNode=None, strong_mask: bool = False, show_mask: bool = False,
                  opencl: bool = False, strength=1, alpha: float = 0.25, beta: float = 0.5, gamma=40, nrad=2, mdis=20,
                  nsize=3, nns=3, qual=1) -> vs.VideoNode:
    """
    Script written by Zastin. What it does is clamp the "change" done by eedi3 to the "change" of nnedi3.
    This should fix every issue created by eedi3. For example: https://i.imgur.com/hYVhetS.jpg

    :param mask:  Allows for user to use their own mask. (Default value = None)
    :param strong_mask: bool:  Whether or not to use a binarized kgf.retinex_edgemask
                               to replace more lineart with nnedi3. (Default value = False)
    :param show_mask: bool:  Whether or not to return the mask instead of the processed clip. (Default value = False)
    :param opencl: bool:  Allows TAAmbk to use opencl acceleration when anti-aliasing. (Default value = False)
    :param strength:  (Default value = 1)
    :param alpha: float:  (Default value = 0.25)
    :param beta: float:  (Default value = 0.5)
    :param gamma:  (Default value = 40)
    :param nrad:  (Default value = 2)
    :param mdis:  (Default value = 20)
    :param nsize:  (Default value = 3)
    :param nns:  (Default value = 3)
    :param qual:  (Default value = 1)

    """
    bits = clip.format.bits_per_sample - 8
    thr = strength * (1 >> bits)
    strong = TAAmbk(clip, aatype='Eedi3', alpha=alpha, beta=beta, gamma=gamma, nrad=nrad, mdis=mdis, mtype=0,
                    opencl=opencl)
    weak = TAAmbk(clip, aatype='Nnedi3', nsize=nsize, nns=nns, qual=qual, mtype=0, opencl=opencl)
    expr = 'x z - y z - * 0 < y x y {0} + min y {0} - max ?'.format(thr)

    if clip.format.num_planes > 1:
        expr = [expr, '']
    aa = core.std.Expr([strong, weak, clip], expr)

    if mask is not None:
        merged = clip.std.MaskedMerge(aa, mask, planes=0)
    elif strong_mask:
        mask = kgf.retinex_edgemask(clip, 1).std.Binarize()
        merged = clip.std.MaskedMerge(aa, mask, planes=0)
    else:
        mask = clip.std.Prewitt(planes=0).std.Binarize(planes=0).std.Maximum(planes=0).std.Convolution([1] * 9,
                                                                                                       planes=0)
        mask = get_y(mask)
        merged = clip.std.MaskedMerge(aa, mask, planes=0)

    if show_mask:
        return mask

    return merged if clip.format.color_family == vs.GRAY else core.std.ShufflePlanes([merged, clip], [0, 1, 2], vs.YUV)


def quick_denoise(clip: vs.VideoNode, sigma=4, cmode='knlm', ref: vs.VideoNode = None, **kwargs) -> vs.VideoNode:
    """
    A rewrite of my old 'quick_denoise'. I still hate it, but whatever.
    This will probably be removed in a future commit.

    This wrapper is used to denoise both the luma and chroma using various denoisers of your choosing.
    If you wish to use just one denoiser,
    you're probably better off using that specific filter rather than this wrapper.

    BM3D is used for denoising the luma.

    Special thanks to kageru for helping me out with some ideas and pointers.

    :param sigma:  Denoising strength for BM3D. (Default value = 4)
    :param cmode:  Chroma modes:
                     1 - Use knlmeans for denoising the chroma (default)
                     2 - Use tnlmeans for denoising the chroma
                     3 - Use dfttest for denoising the chroma (requires setting 'sbsize' in kwargs)
                     4 - Use SMDegrain for denoising the chroma
    :param ref: vs.VideoNode:  Optional reference clip to replace BM3D's basic estimate. (Default value = None)

    """
    y, u, v = kgf.split(clip)
    if cmode in [1, 'knlm']:
        den_u = u.knlm.KNLMeansCL(d=3, a=2, **kwargs)
        den_v = v.knlm.KNLMeansCL(d=3, a=2, **kwargs)
    elif cmode in [2, 'tnlm']:
        den_u = u.tnlm.TNLMeans(ax=2, ay=2, az=2, **kwargs)
        den_v = v.tnlm.TNLMeans(ax=2, ay=2, az=2, **kwargs)
    elif cmode in [3, 'dft']:
        if 'sbsize' in kwargs:
            den_u = u.dfttest.DFTTest(sosize=kwargs['sbsize'] * 0.75, **kwargs)
            den_v = v.dfttest.DFTTest(sosize=kwargs['sbsize'] * 0.75, **kwargs)
        else:
            raise ValueError('quick_denoise: \'sbsize\' not specified')
    elif cmode in [4, 'smd']:
        den_u = hvf.SMDegrain(u, prefilter=3, **kwargs)
        den_v = hvf.SMDegrain(v, prefilter=3, **kwargs)
    else:
        raise ValueError('quick_denoise: unknown mode')

    den_y = mvf.BM3D(y, sigma=sigma, psample=0, radius1=1, ref=ref)
    return core.std.ShufflePlanes([den_y, den_u, den_v], 0, vs.YUV)


def stack_planes(clip: vs.VideoNode, stack_vertical: bool = False) -> vs.VideoNode:
    """Stacks the planes of a clip."""

    y, u, v = kgf.split(clip)
    subsampling = get_subsampling(clip)

    if subsampling is '420':
        if stack_vertical:
            u_v = core.std.StackHorizontal([u, v])
            return core.std.StackVertical([y, u_v])
        else:
            u_v = core.std.StackVertical([u, v])
            return core.std.StackHorizontal([y, u_v])
    elif subsampling is '444':
        return core.std.StackVertical([y, u, v]) if stack_vertical else core.std.StackHorizontal([y, u, v])
    else:
        raise TypeError('stack_planes: input clip must be in YUV format with 444 or 420 chroma subsampling')


# TODO: fix test_descale ?

def test_descale(clip: vs.VideoNode, height: int, kernel: str = 'bicubic', b: float = 1 / 3, c: float = 1 / 3,
                 taps: int = 4) -> vs.VideoNode:
    """
    Generic function to test descales with.
    Descales and reupscales a given clip, allowing you to compare the two easily.

    When comparing, it is recommended to do atleast a 4x zoom using Nearest Neighbor.
    I also suggest using 'compare', as that will make comparison a lot easier.

    :param height: int:  Target descaled height.
    :param kernel: str:  Descale kernel - 'bicubic'(default), 'bilinear', 'lanczos', 'spline16', or 'spline36'
    :param b: float:  B-param for bicubic kernel. (Default value = 1 / 3)
    :param c: float:  C-param for bicubic kernel. (Default value = 1 / 3)
    :param taps: int:  Taps param for lanczos kernel. (Default value = 4)

    """
    y, u, v = kgf.split(clip)
    if kernel is 'bicubic':
        descaled = core.descale.Debicubic(y, get_w(height), height, b=b, c=c)
        upscaled = core.resize.Bicubic(descaled, y.width, y.height, filter_param_a=b, filter_param_b=c)
    elif kernel is 'bilinear':
        descaled = core.descale.Debilinear(y, get_w(height), height)
        upscaled = core.resize.Bilinear(descaled, get_w(height), height)
    elif kernel is 'lanczos':
        descaled = core.descale.Delanczos(y, get_w(height), height, taps=taps)
        upscaled = core.resize.Lanczos(descaled, y.width, y.height, filter_param_a=taps)
    elif kernel is 'spline16':
        descaled = core.descale.Despline16(y, get_w(height), height)
        upscaled = core.resize.Spline16(descaled, get_w(height), height)
    elif kernel is 'spline36':
        descaled = core.descale.Despline36(y, get_w(height), height)
        upscaled = core.resize.Spline36(descaled, get_w(height), height)
    else:
        raise ValueError('test_descale: unknown kernel')

    return kgf.join([upscaled, u, v])


def source(file: str, force_lsmas: bool = False, ref=None, fpsnum: int = None, fpsden: int = None) -> vs.VideoNode:
    """
    Generic clip import function.
    Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced.
    It also automatically determines if an image has been imported.
    You can set its fps using 'fpsnum' and 'fpsden', or using a reference clip with 'ref'.

    :param file: str:  OS absolute file location.

    """
    if file.startswith('file:///'):
        file = file[8::]

    if force_lsmas:
        return core.lsmas.LWLibavSource(file)

    if file.endswith('.d2v'):
        clip = core.d2v.Source(file)
    elif is_image(file):
        clip = core.imwri.Read(file)
        if ref is not None:
            clip = core.std.AssumeFPS(clip, fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)
        elif None not in [fpsnum, fpsden]:
            clip = core.std.AssumeFPS(clip, fpsnum=fpsnum, fpsden=fpsden)
    else:
        if file.endswith('.m2ts'):
            clip = core.lsmas.LWLibavSource(file)
        else:
            clip = core.ffms2.Source(file)

    return clip


def deblend(clip, rep: int = 12):
    """
    A simple filter to fix deblending for interlaced video with an AABBA blending pattern, where A is a normal frame and B is a blended frame.
    Assuming there's a constant pattern of frames (labeled A, B, C, CD, and DA), blending can be fixed by calculating the C frame and fix CD. DA can then be dropped due to it being an interlaced frame.

    However, doing this will result in some of the artifacting being added to the deblended frame. We can mitigate this by repairing the frame with the non-blended frame before it.
    For simplicity, repair=12 is used for now, however this can be changed by the user.

    For more information, please refer to this blogpost by torchlight:
    https://mechaweaponsvidya.wordpress.com/2012/09/13/adventures-in-deblending/
    """

    blends_a = range(2, clip.num_frames-1, 5)
    blends_b = range(3, clip.num_frames-1, 5)
    expr = ["z a 2 / - y x 2 / - +"]

    def deblend(n, clip, rep):
    # Thanks Myaa, motbob and kageru!
        if n%5 in [0, 1, 4]:
            return clip
        else:
            if n in blends_a:
                c, cd, da, a = clip[n-1], clip[n], clip[n+1], clip[n+2]
                debl = core.std.Expr([c, cd, da, a], expr)
                return core.rgvs.Repair(debl, c, rep)
            else:
                return clip

    debl = core.std.FrameEval(clip, partial(deblend, clip=clip, rep=rep))
    return core.std.DeleteFrames(debl, blends_b).std.AssumeFPS(fpsnum=24000, fpsden=1001)


# Aliases
src = source
comp = compare
scomp = stack_compare
qden = quick_denoise
denoise = quick_denoise  # for backwards compatibility
NnEedi3 = nneedi3_clamp  # for backwards compatibility
cond_desc = conditional_descale
