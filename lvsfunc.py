"""
    Various functions I make use of often and other people might be able to use too. Suggestions and fixes are always appreciated!
"""

import vapoursynth as vs
import kagefunc as kgf # https://github.com/Irrational-Encoding-Wizardry/kagefunc
import vsutil # https://github.com/Irrational-Encoding-Wizardry/vsutil
core = vs.core

# TO-DO: Write function that only masks px of a certain color/threshold of colors


def compare(clip_a: vs.VideoNode, clip_b: vs.VideoNode, frames: int, mark=False, mark_a=' Clip A ', mark_b=' Clip B ', fontsize=57):
    """
    Allows for the same frames from two different clips to be compared by putting them next to each other in a list.

    Shorthand for this function is "comp".
    """
    if clip_a.format.id != clip_b.format.id:
        raise ValueError('compare: The format of both clips must be equal')

    if mark:
        style = f'sans-serif,{fontsize},&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,3,1,7,10,10,10,1'
        margins = [10, 0, 10, 0]
        clip_a = core.sub.Subtitle(clip_a, mark_a, style=style, margins=margins)
        clip_b = core.sub.Subtitle(clip_b, mark_b, style=style, margins=margins)

    pairs = (clip_a[frame] + clip_b[frame] for frame in frames)
    return sum(pairs, next(pairs))


def stack_compare(*clips: vs.VideoNode, width=None, height=None, stack_vertical=False):
    """
    A simple wrapper that allows you to compare two clips by stacking them.
    You can stack an infinite amount of clips.

    Best to use when trying to match two sources frame-accurately, however by setting height to the source's
    height (or None), it can be used for comparing frames.

    Shorthand for this function is "scomp".
    """
    if len(set([c.format.id for c in clips])) != 1:
        raise ValueError('stack_compare: The format of every clip must be equal')

    if height is None:
        height = vsutil.fallback(height, clips[0].height)
    if width is None:
        width = vsutil.get_w(height, aspect_ratio=clips[0].width / clips[0].height)

    clips = [c.resize.Bicubic(width, height) for c in clips]
    return core.std.StackVertical(clips) if stack_vertical else core.std.StackHorizontal(clips)


def conditional_descale(src, height, b=1/3, c=1/3, threshold=0.003, w2x=False):
    """

        Descales and reupscales a clip. If the difference exceeds the threshold, the frame will not be descaled.
        If it does not exceed the threshold, the frame will upscaled using either nnedi3_rpow2 or waifu2x-caffe.

        Useful for bad BDs that have additional post-processing done on some scenes, rather than all of them.

        Currently only works with bicubic, and has no native 1080p masking.
        Consider scenefiltering OP/EDs with a different descale function instead.

        The code for _get_error was mostly taken from kageru's Made in Abyss script.
        Special thanks to Lypheo for holding my hand as this was written.
    """
    import functools
    import fvsfunc as fvf  # https://github.com/Irrational-Encoding-Wizardry/fvsfunc

    if vsutil.get_depth(src) != 32:
        src = fvf.Depth(src, 32)
    y, u, v = kgf.split(src)
    descale = _get_error(y, height=height, b=b, c=c)
    eval = core.std.FrameEval(src, functools.partial(_diff, src=src, descaled=descale[0], threshold=threshold, w2x=w2x), descale[1])
    return kgf.join([eval, u, v])


def _get_error(src, height, b, c):
    descale = core.descale.Debicubic(src, vsutil.get_w(height), height, b=b, c=c)
    upscale = core.resize.Bicubic(descale, src.width, src.height, filter_param_a=b, filter_param_b=c)
    diff = core.std.PlaneStats(upscale, src)
    return descale, diff


def _diff(n, f, src, descaled, threshold=0.003, w2x=False):
    from nnedi3_rpow2 import nnedi3_rpow2 # https://github.com/darealshinji/vapoursynth-plugins/blob/master/scripts/nnedi3_rpow2.py

    if f.props.PlaneStatsDiff > threshold:
        return src
    else:
        if w2x:
            return core.caffe.Waifu2x(descaled, noise=-1, scale=2, model=6, cudnn=True, processor=0, tta=False).resize.Bicubic(src.width, src.height, format=src.format)
        else:
            return nnedi3_rpow2(descaled).resize.Bicubic(src.width, src.height, format=src.format)


def transpose_aa(clip: vs.VideoNode, eedi3=False):
    """
    Function written by Zastin and modified by me.
    Performs anti-aliasing over a clip by using nnedi3, transposing, using nnedi3 again, and transposing a final time.
    This results in overall stronger aliasing.
    Useful for shows like Yuru Camp with bad lineart problems.

    If Eedi3=False, it will use Nnedi3 instead.
    """
    srcY = vsutil.get_y(clip)
    height, width = clip.height, clip.width

    if eedi3:
        def aa(srcY):
            srcY = srcY.std.Transpose()
            srcY = srcY.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            srcY = srcY.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            srcY = srcY.resize.Spline36(height, width, src_top=.5)
            srcY = srcY.std.Transpose()
            srcY = srcY.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            srcY = srcY.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            srcY = srcY.resize.Spline36(width, height, src_top=.5)
            return srcY
    else:
        def aa(srcY):
            srcY = srcY.std.Transpose()
            srcY = srcY.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            srcY = srcY.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            srcY = srcY.resize.Spline36(height, width, src_top=.5)
            srcY = srcY.std.Transpose()
            srcY = srcY.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            srcY = srcY.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            srcY = srcY.resize.Spline36(width, height, src_top=.5)
            return srcY

    def csharp(flt, src):
        blur = core.std.Convolution(flt, [1] * 9)
        return core.std.Expr([flt, src, blur], 'x y < x x + z - x max y min x x + z - x min y max ?')

    aaclip = aa(srcY)
    aaclip = csharp(aaclip, srcY).rgvs.Repair(srcY, 13)

    return aaclip if clip.format.color_family is vs.GRAY else core.std.ShufflePlanes([aaclip, clip], [0, 1, 2], vs.YUV)


def NnEedi3(clip: vs.VideoNode, mask=None, strong_mask=False, show_mask=False, opencl=False, strength=1, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, nsize=3, nns=3, qual=1):
    """
    Script written by Zastin. What it does is clamp the "change" done by eedi3 to the "change" of nnedi3.
    This should fix every issue created by eedi3. For example: https://i.imgur.com/hYVhetS.jpg

    "mask" allows for you to use your own mask.
    "strong_mask" uses a binarized kgf.retinex_edgemask to replace more lineart with nnedi3.
    """
    import vsTAAmbk as taa  # https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk

    bits = clip.format.bits_per_sample - 8
    thr = strength * (1 >> bits)
    strong = taa.TAAmbk(clip, aatype='Eedi3', alpha=alpha, beta=beta, gamma=gamma, nrad=nrad, mdis=mdis, mtype=0, opencl=opencl)
    weak = taa.TAAmbk(clip, aatype='Nnedi3', nsize=nsize, nns=nns, qual=qual, mtype=0, opencl=opencl)
    expr = 'x z - y z - * 0 < y x y {l} + min y {l} - max ?'.format(l=thr)
    if clip.format.num_planes > 1:
        expr = [expr, '']
    aa = core.std.Expr([strong, weak, clip], expr)

    if mask is not None:
        merged = clip.std.MaskedMerge(aa, mask, planes=0)
    elif strong_mask:
        mask = kgf.retinex_edgemask(clip, 1).std.Binarize()
        merged = clip.std.MaskedMerge(aa, mask, planes=0)
    else:
        mask = clip.std.Prewitt(planes=0).std.Binarize(planes=0).std.Maximum(planes=0).std.Convolution([1]*9, planes=0)
        mask = vsutil.get_y(mask)
        merged = clip.std.MaskedMerge(aa, mask, planes=0)

    if show_mask:
        return mask

    return merged if clip.format.color_family == vs.GRAY else core.std.ShufflePlanes([merged, clip], [0, 1, 2], vs.YUV)


def quick_denoise(src: vs.VideoNode, sigma=4, cmode='knlm', ref=None, **kwargs):
    """
        A rewrite of my old 'quick_denoise'. I still hate it, but whatever.
        This will probably be removed in a future commit.

        This wrapper is used to denoise both the luma and chroma using various denoisers of your choosing.
        If you wish to use just one denoiser, you're probably better off using that specific filter rather than this wrapper.

        Chroma Modes (cmode):
            1 - Use knlmeans for denoising the chroma
            2 - Use tnlmeans for denoising the chroma
            3 - Use dfttest for denoising the chroma
            4 - Use SMDegrain for denoising the chroma

        BM3D is used for denoising the luma. Denoising strenght is set with "sigma".

        Special thanks to kageru for helping me out with some ideas and pointers.
    """
    import havsfunc as hvf  # https://github.com/HomeOfVapourSynthEvolution/havsfunc
    import mvsfunc as mvf  # https://github.com/HomeOfVapourSynthEvolution/mvsfunc

    Y, U, V = kgf.split(src)

    if cmode in [1, 'knlm']:
        denU = U.knlm.KNLMeansCL(d=3, a=2, **kwargs)
        denV = V.knlm.KNLMeansCL(d=3, a=2, **kwargs)
    elif cmode in [2, 'tnlm']:
        denU = U.tnlm.TNLMeans(ax=2, ay=2, az=2, **kwargs)
        denV = V.tnlm.TNLMeans(ax=2, ay=2, az=2, **kwargs)
    elif cmode in [3, 'dft']:
        denU = U.dfttest.DFTTest(sosize=sbsize*0.75, **kwargs)
        denV = V.dfttest.DFTTest(sosize=sbsize*0.75, **kwargs)
    elif cmode in [4, 'smd']:
        denU = hvf.SMDegrain(U, prefilter=3, **kwargs)
        denV = hvf.SMDegrain(V, prefilter=3, **kwargs)
    else:
        raise ValueError('quick_denoise: unknown mode')

    denY = mvf.BM3D(Y, sigma=sigma, psample=0, radius1=1, ref=ref)
    return core.std.ShufflePlanes([denY, denU, denV], 0, vs.YUV)


def stack_planes(src, stack_vertical=False):
    """
    Stacks the planes of a clip.
    """
    Y, U, V = kgf.split(src)
    subsampling = vsutil.get_subsampling(src)

    if subsampling is "420":
        if stack_vertical:
            UV = core.std.StackHorizontal([U, V])
            return core.std.StackVertical([Y, UV])
        else:
            UV = core.std.StackVertical([U, V])
            return core.std.StackHorizontal([Y, UV])
    elif subsampling is "444":
         return core.std.StackVertical([Y, U, V]) if stack_vertical else core.std.StackHorizontal([Y, U, V])


def test_descale(src, height, kernel='bicubic', b=1/3, c=1/3, taps=4):
    """
    Generic function to test descales with.
    Descales and reupscales a given clip, allowing you to compare the two easily.

    When comparing, it is recommended to do atleast a 4x zoom using Nearest Neighbor.
    I also suggest using "compare", as that will make comparison a lot easier.
    """
    y, u, v = kgf.split(src)
    if kernel is 'bicubic':
        descaled = core.descale.Debicubic(y, vsutil.get_w(height), height, b=b, c=c)
        upscaled = core.resize.Bicubic(descaled, y.width, y.height, filter_param_a=b, filter_param_b=c)
    elif kernel is 'bilinear':
        descaled = core.descale.Debilinear(y, vsutil.get_w(height), height)
        upscaled = core.resize.Bilinear(descaled, vsutil.get_w(height), height)
    elif kernel is 'lanczos':
        descaled = core.descale.Delanczos(y, vsutil.get_w(height), height, taps=taps)
        upscaled = core.resize.Lanczos(descaled, y.width, y.height, filter_param_a=taps)
    elif kernel is 'spline16':
        descaled = core.descale.Despline16(y, width, height)
        upscaled = core.resize.Spline16(descaled, vsutil.get_w(height), height)
    elif kernel is 'spline36':
        descaled = core.descale.Despline36(y, width, height)
        upscaled = core.resize.Spline36(descaled, vsutil.get_w(height), height)
    else:
        raise ValueError('test_descale: unknown kernel')

    return kgf.join([upscaled, u, v])


def source(file: str, force_lsmas=False, src=None, fpsnum=None, fpsden=None) -> vs.VideoNode:
    """
    Generic clip import function.
    Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced.
    It also automatically determines if an image has been imported. You can set its fps using "fpsnum" and "fpsden", or using a reference clip with "src".
    """
    if file.startswith("file:///"):
        file = file[8::]

    if force_lsmas:
        return core.lsmas.LWLibavSource(file)

    if file.endswith(".d2v"):
        clip = core.d2v.Source(file)
    elif vsutil.is_image(file):
        clip = core.imwri.Read(file)
        if src is not None:
            clip = core.std.AssumeFPS(clip, fpsnum=src.fps.numerator, fpsden=src.fps.denominator)
        elif None not in [fpsnum, fpsden]:
            clip = core.std.AssumeFPS(clip, fpsnum=fpsnum, fpsden=fpsden)
    else:
        if file.endswith(".m2ts"):
            clip = core.lsmas.LWLibavSource(file)
        else:
            clip = core.ffms2.Source(file)

    return clip


# Aliasses
src = source
comp = compare
scomp = stack_compare
qden = quick_denoise
denoise = quick_denoise # (backwards compatibility, will be removed later)

