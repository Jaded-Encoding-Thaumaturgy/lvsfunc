import vapoursynth as vs
core = vs.core
import vsTAAmbk as taa # https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk
import fvsfunc as fvf # https://github.com/Irrational-Encoding-Wizardry/fvsfunc

"""
lvsfunc = Light's Vapoursynth Functions
Scripts I (stole) 'borrowed' from other people and modified to my own liking. If something breaks, blame them.
"""

def fix_eedi3(clip, strength=1, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, nsize=3, nns=3, qual=1):
    """
    Script stolen from Zastin. What it does is clamp the "change" done by eedi3 to the "change" of nnedi3. This should
    fix every issue created by eedi3, like for example this: https://i.imgur.com/hYVhetS.jpg
    
    Tested on Hanabi by Zastin, should work fine for everything else. Supposedly, at least.
    """
    
    if clip.format.bits_per_sample != 16:
        clip =  fvf.Depth(clip, 16)
    bits = clip.format.bits_per_sample - 8
    thr = strength * (1 >> bits)
    strong = taa.TAAmbk(clip, aatype='Eedi3', alpha=alpha, beta=beta, gamma=gamma, nrad=nrad, mdis=mdis, mtype=0)
    weak = taa.TAAmbk(clip, aatype='Nnedi3', nsize=nsize, nns=nns, qual=qual, mtype=0)
    expr = 'x z - y z - * 0 < y x y {l} + min y {l} - max ?'.format(l=thr)
    if clip.format.num_planes > 1:
        expr = [expr, '']
    aa = core.std.Expr([strong, weak, clip], expr)
    mask = clip.std.Prewitt(planes=0).std.Binarize(50 >> bits, planes=0).std.Maximum(planes=0).std.Convolution([1]*9, planes=0)
    return clip.std.MaskedMerge(aa, mask, planes=0)

    
    
def compare(clips, frames, match_clips=True):
    """
    Script stolen from XEL8o9 and slightly modified by me. Grabs a given frame from two clips for easier comparison.
    Intended order is [src, filtered].
    
    Example use:
    lvf.compare([src, filtered], [10, 20, 30, 40, 50], match_clips=True)
    """
    if len(clips) < 2:
        raise ValueError('compare: There must be at least two clips')
    width = clips[0].width
    height = clips[0].height
    for i in range(0, len(clips)):
        if clips[i].format.bits_per_sample != 16:
            clips[i] = fvf.Depth(clips[i], 16)
    final = None
    for frame in frames:
        newClip = core.std.Trim(clips[0], frame, frame)
        for i in range(1, len(clips)):
            nextFrame = core.std.Trim(clips[i], frame, frame)
            if nextFrame.width != width or nextFrame.height != height:
                if match_clips:
                    nextFrame = core.resize.Spline36(nextFrame, width, height)
                else:
                    raise ValueError('compare: The dimensions of each clip must be equal')
            newClip += nextFrame
        if final == None:
            final = newClip
        else:
            final += newClip
    return final

    
    
def super_aa(clip, mode=1):
    """
    Script stolen from Zastin and modified by me. Was originally written to deal with Yuru Camp's odd lineart, 
    but can be used for other sources with botched lineart.
    
    Mode 1 = Nnedi3 
    Mode 2 = Eedi3
    """
    if clip.format.bits_per_sample != 16:
        clip = fvf.Depth(clip, 16)
    clip_copy = clip
    clip = clip.std.ShufflePlanes(0, vs.GRAY)
    if mode == 1:
        def aa(clip):
            w, h = clip.width, clip.height
            clip = clip.std.Transpose()
            clip = clip.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            clip = clip.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            clip = clip.resize.Spline36(h, w, src_top=.5)
            clip = clip.std.Transpose()
            clip = clip.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            clip = clip.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            clip = clip.resize.Spline36(w, h, src_top=.5)
            return clip
    elif mode == 2:
        def aa(clip):
            w, h = clip.width, clip.height
            clip = clip.std.Transpose()
            clip = clip.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            clip = clip.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            clip = clip.resize.Spline36(h, w, src_top=.5)
            clip = clip.std.Transpose()
            clip = clip.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            clip = clip.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            clip = clip.resize.Spline36(w, h, src_top=.5)
            return clip
    else:
        raise ValueError('super_aa: Unknown mode')
    
    def csharp(flt, src):
        blur = core.std.Convolution(flt, [1]*9)
        return core.std.Expr([flt,src,blur], 'x y < x x + z - x max y min x x + z - x min y max ?')

    aaclip = aa(clip)
    aaclip = csharp(aaclip, clip).rgvs.Repair(clip, 13)

    if clip_copy.format.color_family == vs.GRAY:
        return aaclip
    elif clip_copy.format.color_family != vs.GRAY:
        srcU = clip_copy.std.ShufflePlanes(1, vs.GRAY)
        srcV = clip_copy.std.ShufflePlanes(2, vs.GRAY)
        merged = core.std.ShufflePlanes([aaclip, srcU, srcV], [0, 0, 0], vs.YUV)
        return merged
