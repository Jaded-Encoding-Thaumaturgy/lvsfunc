import vapoursynth as vs
import vsTAAmbk as taa  # https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk
import fvsfunc as fvf  # https://github.com/Irrational-Encoding-Wizardry/fvsfunc
import mvsfunc as mvf  # https://github.com/HomeOfVapourSynthEvolution/mvsfunc
import havsfunc as haf  # https://github.com/HomeOfVapourSynthEvolution/havsfunc
import mimetypes
import os
import re

core = vs.core

# TO-DO: Write function that only masks px of a certain color/threshold of colors


def compare(clip_a: vs.VideoNode, clip_b: vs.VideoNode, frames: int, mark=False, mark_a=' Clip A ', mark_b=' Clip B ', fontsize=57):
    """
    Allows for two frames to be compared by putting them next to each other in a list.
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
    Compares two frames by stacking.
    Best to use when trying to match two sources frame-accurately, however by setting height to the source's
    height (or None), it can be used for comparing frames.
    """
    if len(set([c.format.id for c in clips])) != 1:
        raise ValueError('stack_compare: The format of every clip must be equal')

    if height is None:
        height = fallback(height, clips[0].height)
    if width is None:
        width = getw(height, ar=clips[0].width / clips[0].height)

    clips = [c.resize.Bicubic(width, height) for c in clips]
    return core.std.StackVertical(clips) if stack_vertical else core.std.StackHorizontal(clips)


def transpose_aa(clip: vs.VideoNode, eedi3=False):
    """
    Script written by Zastin and modified by me. Useful for shows like Yuru Camp with bad lineart problems.
    If Eedi3=False, it will use Nnedi3 instead.
    """
    srcY = get_y(clip)
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


def NnEedi3(src: vs.VideoNode, strength=1, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, nsize=3, nns=3, qual=1):
    """
    Script written by Zastin. What it does is clamp the "change" done by eedi3 to the "change" of nnedi3. This should
    fix every issue created by eedi3. For example: https://i.imgur.com/hYVhetS.jpg
    """
    clip = get_y(src)
    if clip.format.bits_per_sample != 16:
        clip = fvf.Depth(clip, 16)
    thr = strength * 256

    strong = taa.TAAmbk(clip, aatype='Eedi3', alpha=alpha, beta=beta, gamma=gamma, nrad=nrad, mdis=mdis, mtype=0)
    weak = taa.TAAmbk(clip, aatype='Nnedi3', nsize=nsize, nns=nns, qual=qual, mtype=0)
    expr = 'x z - y z - * 0 < y x y {l} + min y {l} - max ?'.format(l=thr)
    aa = core.std.Expr([strong, weak, clip], expr)
    mask = clip.std.Prewitt().std.Binarize(50 >> 8).std.Maximum().std.Convolution([1] * 9)
    merged = core.std.MaskedMerge(clip, aa, mask)
    return clip if src.format.color_family == vs.GRAY else core.std.ShufflePlanes([clip, src], [0, 1, 2], vs.YUV)


def quick_denoise(clip: vs.VideoNode, mode='knlm', bm3d=True, sigma=3, h=1.0, refine_motion=True, sbsize=16, resample=True):
    """
    Wrapper for generic denoising. Denoising is done by BM3D with a given denoisers being used for ref. Returns the denoised clip used
    as ref if BM3D=False.

    Mode 1 = KNLMeansCL
    Mode 2 = SMDegrain
    Mode 3 = DFTTest

    Will be removed eventuallyTM.
    """
    if resample:
        if clip.format.bits_per_sample != 16:
            clip = fvf.Depth(clip, 16)
    clipY = core.std.ShufflePlanes(clip, 0, vs.GRAY)

    if mode in [1, 'knlm']:
        denoiseY = clipY.knlm.KNLMeansCL(d=3, a=2, h=h)
    elif mode in [2, 'SMD', 'SMDegrain']:
        denoiseY = haf.SMDegrain(clipY, prefilter=3, RefineMotion=refine_motion)
    elif mode in [3, 'DFT', 'dfttest']:
        denoiseY = clipY.dfttest.DFTTest(sigma=4.0, tbsize=1, sbsize=sbsize, sosize=sbsize*0.75)
    else:
        raise ValueError('denoise: unknown mode')

    if bm3d:
        denoisedY = mvf.BM3D(clipY, sigma=sigma, psample=0, radius1=1, ref=denoiseY)
    elif bm3d is False:
        denoisedY = denoiseY

    if clip.format.color_family is vs.GRAY:
        return denoisedY
    else:
        srcU = clip.std.ShufflePlanes(1, vs.GRAY)
        srcV = clip.std.ShufflePlanes(2, vs.GRAY)
        merged = core.std.ShufflePlanes([denoisedY, srcU, srcV], 0, vs.YUV)
        return merged


def source(file: str, force_lsmas=False) -> vs.VideoNode:
    """
    Quick general import wrapper that automatically matches various sources with an appropriate indexing filter.
    """
    if file.startswith("file:///"):
        file = file[8::]

    if force_lsmas:
        return core.lsmas.LWLibavSource(file)

    if file.endswith(".d2v"):
        clip = core.d2v.Source(file)
    elif is_image(file):
        clip = core.imwri.Read(file)
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

# Helper functions written by other people (aka kageru lol):
def getw(h, ar=16 / 9, only_even=True):
    """
    returns width for image (taken from kagefunc)
    """
    w = h * ar
    w = int(round(w))
    if only_even:
        w = w // 2 * 2
    return w


def fallback(value, fallback_value):
    """
    Returns a value or the fallback if the value is None.haf
    """
    return fallback_value if value is None else value


def get_y(clip: vs.VideoNode) -> vs.VideoNode:
    """
    Returns the first plane of a video clip.
    """
    return clip.std.ShufflePlanes(0, vs.GRAY)


def is_image(filename: str) -> bool:
    """
    Returns true if a filename refers to an image.
    """
    return mimetypes.types_map.get(os.path.splitext(filename)[-1], "").startswith("image/")
