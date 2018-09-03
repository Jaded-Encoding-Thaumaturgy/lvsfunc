import vapoursynth as vs
core = vs.core
import vsTAAmbk as taa
import fvsfunc as fvf

"""
lvsfunc = Light's Vapoursynth Functions

Scripts I (stole) 'borrowed' from other people. If something breaks, I'll blame them.
"""

def fix_eedi3(clip, strength=1, alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, nsize=3, nns=3, qual=1):
    """
    Script stolen from Zastin. What it does is clamp the "change" done by eedi3 to the "change" of nnedi3. This should
    fix every issue created by eedi3, like for example this: https://i.imgur.com/hYVhetS.jpg
    
    Tested on Fireworks by Zastin, should work fine for everything else. Supposedly, at least.
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

