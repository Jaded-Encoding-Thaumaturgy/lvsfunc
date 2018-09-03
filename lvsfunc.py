import vapoursynth as vs
core = vs.core
import vsTAAmbk as taa # https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk
import fvsfunc as fvf # https://github.com/Irrational-Encoding-Wizardry/fvsfunc

"""
lvsfunc = Light's Vapoursynth Functions

Scripts I (stole) 'borrowed' from other people. If something breaks, blame them.
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
	
	Changes:
		*Made it resample to float if clip(s) are not already float.
		*Made it return the clip instead of have a set_output() there by itself.
	"""
    if len(clips) < 2:
        raise ValueError('There must be at least two clips')
    width = clips[0].width
    height = clips[0].height
    if clips[0].format.bits_per_sample != 16:
        clips[0] = fvf.Depth(clips[0], 16)
    if clips[1].format.bits_per_sample != 16:
        clips[1] = fvf.Depth(clips[1], 16)
    final = None
    for frame in frames:
        newClip = core.std.Trim(clips[0], frame, frame)
        for i in range(1, len(clips)):
            nextFrame = core.std.Trim(clips[i], frame, frame)
            if nextFrame.width != width or nextFrame.height != height:
                if match_clips:
                    nextFrame = core.resize.Spline36(nextFrame, width, height)
                else:
                    raise ValueError('The dimensions of each clip must be equal')
            newClip += nextFrame
        if final == None:
            final = newClip
        else:
            final += newClip
    return final
