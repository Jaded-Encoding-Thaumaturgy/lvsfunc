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

"""
    optional dependencies: (http://www.vapoursynth.com/doc/pluginlist.html)
        * waifu2x-caffe
        * L-SMASH Source
        * d2vsource
        * FFMS2
"""

"""
    List of functions sorted by category:

    Comparison and Analysis:
        - compare (comp)
        - stack_compare (scomp)
        - stack_planes
        - tvbd_diff

    Scaling and Resizing:
        - conditional_descale (cond_desc)
        - smart_descale
        - test_descale

    Antialiasing:
        - transpose_aa
        - upscaled_sraa
        - nneedi3_clamp

    Deinterlacing:
        - deblend

    Denoising and Debanding:
        - quick_denoise (qden)

    Masking, Limiting, and Color Handling:
        - limit_dark
        - fix_cr_tint
        - wipe_row

    Miscellaneous:
        - source (src)
"""

# TODO: Write function that only masks px of a certain color/threshold of colors

#### Comparison and Analysis Functions


def compare(clip_a: vs.VideoNode, clip_b: vs.VideoNode,
            frames: List[int] = None,
            rand_frames: bool = False, rand_total: int = None,
            disable_resample: bool = False) -> vs.VideoNode:
    """
    Allows for the same frames from two different clips to be compared by putting them next to each other in a list.
    Clips are automatically resampled to 8bit YUV -> RGB24 to emulate how a monitor shows the frame.
    This can be disabled by setting `disable_resample` to True.

    Shorthand for this function is "comp".

    :frames: int:               List of frames to compare.
    :rand_frames: bool:         Pick random frames from the given clips.
    :rand_total: int:           Amount of random frames to pick.
    :disable_resample: bool:    Disable forcibly resampling clips from 8bit YUV -> RGB24.
    """
    def resample(clip):
        # Resampling to 8bit and RGB to properly display how it appears on your screen
        return mvf.ToRGB(fvf.Depth(clip, 8))

    # Error handling
    if frames is not None:
        if len(frames) > clip_a.num_frames:
            raise ValueError('compare: More comparisons asked for than frames available')

    if disable_resample is False:
        clip_a, clip_b = resample(clip_a), resample(clip_b)
    else:
        if clip_a.format.id != clip_b.format.id:
            raise ValueError('compare: The format of both clips must be equal')

    if frames is None:
        rand_frames = True

    if rand_frames:
        if rand_total is None:
            # More comparisons for shorter clips so you can compare stuff like NCs more conveniently
            rand_total = int(clip_a.num_frames/1000) if clip_a.num_frames > 5000 else int(clip_a.num_frames/100)
        frames = sorted(random.sample(range(1, clip_a.num_frames-1), rand_total))

    pairs = (clip_a[frame] + clip_b[frame] for frame in frames)
    return sum(pairs, next(pairs))


def stack_compare(*clips: vs.VideoNode,
                  width: int = None, height: int = None,
                  stack_vertical: bool = False,
                  make_diff: bool = False) -> vs.VideoNode:
    """
    A simple wrapper that allows you to compare two clips by stacking them.
    You can stack an infinite amount of clips.

    Best to use when trying to match two sources frame-accurately, however by setting height to the source's
    height (or None), it can be used for comparing frames.

    Shorthand for this function is 'scomp'.

    :stack_vertical: bool: Stack frames vertically
    :diff: bool: Create and stack a diff (only works if two clips are given)
    """
    if len(set([c.format.id for c in clips])) != 1:
        raise ValueError('stack_compare: The format of every clip must be equal')

    if len(clips) != 2 and make_diff:
        raise ValueError('stack_compare: You need to compare two clips for diff!')

    height = fallback(height, clips[0].height)
    width = fallback(width, (get_w(height, aspect_ratio=clips[0].width / clips[0].height)))
    clips = [c.resize.Bicubic(width, height) for c in clips]
    if make_diff:
        diff = core.std.MakeDiff(get_y(clips[0]), get_y(clips[1])).resize.Bilinear(format=clips[0].format)
        clips.append(diff)
    return core.std.StackVertical(clips) if stack_vertical else core.std.StackHorizontal(clips)


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


def tvbd_diff(tv, bd, threshold=51):
    """
    Creates a standard `compare` between frames from two clips that have differences.
    Useful for making comparisons between TV and BD encodes.

    Note that this might catch artifacting as differences! Use your eyes.

    :param threshold: int:  Threshold for PlaneStatsMin.
    """
    diff = core.std.MakeDiff(get_y(tv), get_y(bd)).resize.Point(format=tv.format)
    diff = core.std.PlaneStats(diff)
    try:
        frames = [i for i,f in enumerate(diff.frames()) if f.props["PlaneStatsMin"] <= threshold]
        return compare(tv, bd, frames)
    except StopIteration:
        raise ValueError('tvbd_diff: No frames with differences returned')

#### Scaling and Resizing Functions

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


def smart_descale(clip: vs.VideoNode,
                   res: List[int],
                   b: float = 1/3, c: float = 1/3,
                   thresh1: float = 0.03, thresh2: float = 0.7,
                   no_mask: float = False,
                   show_mask: bool = False, show_dmask: bool = False,
                   single_rate_upscale: bool = False, rfactor: float = 1.5):
    """
    A descaling function that compares relative errors between multiple resolutions and descales accordingly.
    Most of this code was leveraged from kageru's Made in Abyss script.
    As this is an incredibly complex function, I will offer only minimal support.
    For more information and comments I suggest you check out the original script:
        https://git.kageru.moe/kageru/vs-scripts/src/branch/master/abyss1.py


    res: List[int]:             A list of resolutions to descale to. For example: [900, 871, 872, 877]
    thresh1: float:             Threshold for when a frame will be descaled.
    thresh2: float:             Threshold for when a frame will not be descaled.
    single_rate_upscale: bool:  Use upscaled_sraa to upscale the frames
    rfactor: float:             rfactor for upscaled_sraa
    """
    def _descaling(clip: vs.VideoNode, h: int, b: float, c: float):
        """Descale and return a tuple of descaled clip and diff mask between that and the original."""
        down = clip.descale.Debicubic(get_w(h), h, b, c)
        up = down.resize.Bicubic(clip.width, clip.height, filter_param_a=b, filter_param_b=c)
        diff = core.std.Expr([clip, up], 'x y - abs').std.PlaneStats()
        return down, diff

    def _select(n, y, debic_list, single_rate_upscale, rfactor, f):
        """This simply descales to each of those and selects the most appropriate for each frame."""
        errors = [x.props.PlaneStatsAverage for x in f]
        y_deb = debic_list[errors.index(min(errors))]
        dmask = core.std.Expr([y, y_deb.resize.Bicubic(clip.width, clip.height)], 'x y - abs 0.025 > 1 0 ?').std.Maximum().std.SetFrameProp("_descaled_resolution", intval=y_deb.height)

        if single_rate_upscale is True:
            up = upscaled_sraa(y_deb, rfactor, h=clip.height).resize.Bicubic(clip.width, clip.height)
        else:
            up = fvf.Depth(nnedi3_rpow2(fvf.Depth(y_deb, 16), nns=4, correct_shift=True, width=clip.width, height=clip.height), 32)
        return core.std.ClipToProp(up, dmask)

    def _square():
        top = core.std.BlankClip(length=len(y), format=vs.GRAYS, height=4, width=10, color=[1])
        side = core.std.BlankClip(length=len(y), format=vs.GRAYS, height=2, width=4, color=[1])
        center = core.std.BlankClip(length=len(y), format=vs.GRAYS, height=2, width=2, color=[0])
        t1 = core.std.StackHorizontal([side, center, side])
        return core.std.StackVertical([top, t1, top])

    def _restore_original(n, f, clip: vs.VideoNode, orig: vs.VideoNode, thresh_a: float, thresh_b: float):
        """Just revert the entire scaling if the difference is too big. This should catch the 1080p scenes (like the entire ED)."""
        if f.props.PlaneStatsAverage < thresh_a:
            return clip.std.SetFrameProp("_descaled", intval=1)
        elif f.props.PlaneStatsAverage > thresh_b:
            return orig.std.SetFrameProp("_descaled", intval=0)
        return core.std.Merge(clip, orig, (f.props.PlaneStatsAverage - thresh_a) * 20).std.SetFrameProp("_descaled", intval=2)

    og = clip
    clip32 = fvf.Depth(clip, 32)
    if one_plane(clip32):
        y = get_y(clip32)
    else:
        y, u, v = split(clip32)

    # TO-DO: Allow arbitrary integers to be tested rather than enforce a range
    debic_listp = [_descaling(y, h, b, c) for h in res]
    debic_list = [a[0] for a in debic_listp]
    debic_props = [a[1] for a in debic_listp]

    y_deb = core.std.FrameEval(y, partial(_select, y=y, debic_list=debic_list,
                                                  single_rate_upscale=single_rate_upscale, rfactor=rfactor), prop_src=debic_props)
    # TO-DO: It returns a frame size error here for whatever reason. Need to figure out what causes it and fix it
    dmask = core.std.PropToClip(y_deb)
    if show_dmask:
        return dmask
    # TO-DO: Figure out how to make it properly round depending on resolution (although this would usually be 1080p anyway)
    line = core.std.StackHorizontal([_square()]*192)
    full_squares = core.std.StackVertical([line]*108)

    artifacts = core.misc.Hysteresis(dmask.resize.Bicubic(clip32.width, clip32.height, _format=vs.GRAYS),
                                     core.std.Expr([get_y(clip32).tcanny.TCanny(sigma=3), full_squares], 'x y min'))

    ret_raw = kgf.retinex_edgemask(fvf.Depth(clip, 16))
    ret = ret_raw.std.Binarize(30).rgvs.RemoveGrain(3)

    mask = core.std.Expr([ret.resize.Point(_format=vs.GRAYS), kgf.iterate(artifacts, core.std.Maximum, 3)], 'x y -').std.Binarize(0.4)

    mask = mask.std.Inflate().std.Convolution(matrix=[1]*9).std.Convolution(matrix=[1]*9)
    if show_mask:
        return mask

    y = core.std.MaskedMerge(y, y_deb, mask)
    merged = join([y, u, v]) if not one_plane(og) else y
    merged = fvf.Depth(merged, get_depth(og))
    if no_mask:
        return merged

    dmask = dmask.std.PlaneStats() # TO-DO: It returns a frame size error here for whatever reason. Need to figure out what causes it and fix it
    return merged.std.FrameEval(partial(_restore_original, clip=merged, orig=og, thresh_a=thresh1, thresh_b=thresh2), prop_src=dmask)#.std.SetFrameProp("_descaled_resolution", intval=y_deb.height)


# TO-DO: Improve test_descale. Get rid of all the if/else statements and replace with a faster, more robust setup if possible.

def test_descale(clip: vs.VideoNode,
                 height: int,
                 kernel: str = 'bicubic',
                 b: float = 1 / 3, c: float = 1 / 3,
                 taps: int = 3) -> vs.VideoNode:
    """
    Generic function to test descales with.
    Descales and reupscales a given clip, allowing you to compare the two easily.

    When comparing, it is recommended to do atleast a 4x zoom using Nearest Neighbor.
    I also suggest using 'compare', as that will make comparison a lot easier.

    Some of this code was leveraged from DescaleAA, and it also uses functions
    available in fvsfunc.

    :param height: int:  Target descaled height.
    :param kernel: str:  Descale kernel - 'bicubic'(default), 'bilinear', 'lanczos', 'spline16', or 'spline36'
    :param b: float:  B-param for bicubic kernel. (Default value = 1 / 3)
    :param c: float:  C-param for bicubic kernel. (Default value = 1 / 3)
    :param taps: int:  Taps param for lanczos kernel. (Default value = 43)

    """

    clip_y = get_y(clip)

    desc = fvf.Resize(clip_y, get_w(height), height,
                      kernel=kernel, a1=b, a2=c, taps=taps,
                      invks=True)
    upsc = fvf.Resize(desc, clip.width, clip.height,
                      kernel=kernel, a1=b, a2=c, taps=taps)

    return upsc if clip is vs.GRAY else core.std.ShufflePlanes([upsc, clip], planes=[0, 1, 2], colorfamily=vs.YUV)


#### Antialiasing functions

def transpose_aa(clip: vs.VideoNode, eedi3: bool = False) -> vs.VideoNode:
    """
    Function written by Zastin and modified by me.
    Performs anti-aliasing over a clip by using Nnedi3, transposing, using Nnedi3 again, and transposing a final time.
    This results in overall stronger anti-aliasing.
    Useful for shows like Yuru Camp with bad lineart problems.

    :param eedi3: bool:  When true, uses eedi3 instead. (Default value = False)

    """
    clip_y = get_y(clip)

    if eedi3:
        def _aa(clip_y):
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            clip_y = clip_y.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            clip_y = clip_y.resize.Spline36(clip.height, clip.width, src_top=.5)
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.eedi3m.EEDI3(0, 1, 0, 0.5, 0.2)
            clip_y = clip_y.znedi3.nnedi3(1, 0, 0, 3, 4, 2)
            return clip_y.resize.Spline36(clip.width, clip.height, src_top=.5)
    else:
        def _aa(clip_y):
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            clip_y = clip_y.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            clip_y = clip_y.resize.Spline36(clip.height, clip.width, src_top=.5)
            clip_y = clip_y.std.Transpose()
            clip_y = clip_y.nnedi3.nnedi3(0, 1, 0, 3, 3, 2)
            clip_y = clip_y.nnedi3.nnedi3(1, 0, 0, 3, 3, 2)
            return clip_y.resize.Spline36(clip.width, clip.height, src_top=.5)

    def _csharp(flt, clip):
        blur = core.std.Convolution(flt, [1] * 9)
        return core.std.Expr([flt, clip, blur], 'x y < x x + z - x max y min x x + z - x min y max ?')

    aaclip = _aa(clip_y)
    aaclip = _csharp(aaclip, clip_y).rgvs.Repair(clip_y, 13)

    return aaclip if clip.format.color_family is vs.GRAY else core.std.ShufflePlanes([aaclip, clip], [0, 1, 2], vs.YUV)


def upscaled_sraa(clip: vs.VideoNode,
                  rfactor: float = 1.5,
                  rep: int = None,
                  h: int = None,
                  sharp_downscale: bool = True) -> vs.VideoNode:
    """
    Another AA written by Zastin and slightly modified by me.
    Performs an upscaled single-rate AA to deal with heavy aliasing.

    Useful for Web rips, where the source quality is not good enough to descale,
    but you still want to deal with some bad aliasing and lineart.

    :param rfactor: float:  Image enlargement factor. 1.5..2 makes it comparable to vsTAAmbk.
                            It is not recommended to go below 1.5.
    :param rep: int:        Repair mode.
    :param h: int:          Set custom height. Width and aspect ratio are auto-calculated.
    """
    planes = split(clip)

    nnargs = dict(nsize=0, nns=4, qual=2)
    eeargs = dict(alpha=0.2, beta=0.6, gamma=40, nrad=2, mdis=20) #taa defaults are 0.5, 0.2, 20, 3, 30

    ssw = round( clip.width  * rfactor )
    ssh = round( clip.height * rfactor )

    while ssw % 2:
        ssw += 1
    while ssh % 2:
        ssh += 1

    if h:
        w = get_w(h, aspect_ratio=clip.width / clip.height)
    else:
        w, h = clip.width, clip.height

    #Nnedi3 upscale from source height to source height * rounding (Default 1.5)
    up_y = core.nnedi3.nnedi3(planes[0], 0, 1, 0, **nnargs)
    up_y = core.resize.Spline36(up_y, height=ssh, src_top=.5)
    up_y = core.std.Transpose(up_y)
    up_y = core.nnedi3.nnedi3(up_y, 0, 1, 0, **nnargs)
    up_y = core.resize.Spline36(up_y, height=ssw, src_top=.5)

    #Single-rate AA
    aa_y = core.eedi3m.EEDI3(up_y, 0, 0, 0, **eeargs, sclip=core.nnedi3.nnedi3(up_y, 0, 0, 0, **nnargs))
    aa_y = core.std.Transpose(aa_y)
    aa_y = core.eedi3m.EEDI3(aa_y, 0, 0, 0, **eeargs, sclip=core.nnedi3.nnedi3(aa_y, 0, 0, 0, **nnargs))

    #Back to source clip height or given height
    scaled = core.fmtc.resample(aa_y, w, h, kernel='gauss', invks=True, invkstaps=2, taps=1, a1=32) if sharp_downscale else core.resize.Spline36(aa_y, w, h)

    if rep:
        scaled = core.rgvs.Repair(scaled, planes[0].resize.Spline36(w, h), rep)

    if one_plane(clip):
        return scaled
    else:
        try:
            return join([scaled, planes[1], planes[2]])
        except:
            if get_subsampling(clip) is "420":
                planes[1], planes[2] = [core.resize.Bicubic(p, w / 2, h / 2, src_left=.25 * (1 - clip.width / w )) for p in planes[1:]]
                return join([scaled, planes[1], planes[2]])
            elif get_subsampling(clip) is "444":
                planes[1], planes[2] = [core.resize.Bicubic(p, w, h) for p in planes[1:]]
                return join([scaled, planes[1], planes[2]])
            else:
                raise ValueError(f'upscaled_sraa: Failed to return a \'{get_subsampling(clip)}\' clip. Please use either a 420, 444, or GRAY clip!')


def nneedi3_clamp(clip: vs.VideoNode,
                  mask: vs.VideoNode=None, strong_mask: bool = False, show_mask: bool = False,
                  opencl: bool = False,
                  strength=1,
                  alpha: float = 0.25, beta: float = 0.5, gamma=40,
                  nrad=2, mdis=20,
                  nsize=3, nns=3,
                  qual=1) -> vs.VideoNode:
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


#### Deinterlacing


def deblend(clip, rep: int = None):
    """
    A simple function to fix deblending for interlaced video with an AABBA blending pattern, where A is a normal frame and B is a blended frame.
    Assuming there's a constant pattern of frames (labeled A, B, C, CD, and DA in this function), blending can be fixed by calculating the C frame by getting halves of CD and DA, and using that to fix up CD.
    DA can then be dropped due to it being an interlaced frame.

    However, doing this will result in some of the artifacting being added to the deblended frame. We can mitigate this by repairing the frame with the non-blended frame before it.

    For more information, please refer to this blogpost by torchlight:
    https://mechaweaponsvidya.wordpress.com/2012/09/13/adventures-in-deblending/
    """

    blends_a = range(2, clip.num_frames-1, 5)
    blends_b = range(3, clip.num_frames-1, 5)
    expr_cd = ["z a 2 / - y x 2 / - +"]

    def deblend(n, clip, rep):
    # Thanks Myaa, motbob and kageru!
        if n%5 in [0, 1, 4]:
            return clip
        else:
            if n in blends_a:
                c, cd, da, a = clip[n-1], clip[n], clip[n+1], clip[n+2]
                debl = core.std.Expr([c, cd, da, a], expr_cd)
                return core.rgvs.Repair(debl, c, rep) if rep else debl
                # To-DO: Add decimation bool and proper DA frame deblending
            else:
                return clip

    debl = core.std.FrameEval(clip, partial(deblend, clip=clip, rep=rep))
    return core.std.DeleteFrames(debl, blends_b).std.AssumeFPS(fpsnum=24000, fpsden=1001)


#### Denoising and Debanding


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


#### Masking, Limiting, and Colors


def limit_dark(clip: vs.VideoNode, filtered: vs.VideoNode,
               threshold: int = .25, threshold_range: int = None) -> vs.VideoNode:
    """
    Replaces frames in a clip with a filtered clip when the frame's darkness exceeds the threshold.
    This way you can run lighter (or heavier) filtering on scenes that are almost entirely dark.

    There is one caveat, however: You can get scenes where every other frame is filtered
    rather than the entire scene. Please do take care to avoid that if possible.

    threshold: int:         Threshold for frame averages to be filtered
    threshold_range: int:   Threshold for a range of frame averages to be filtered
    """
    def _diff(n, f, clip, filtered, threshold, threshold_range):
        if threshold_range:
            return filtered if threshold_range <= f.props.PlaneStatsAverage <= threshold else clip
        else:
            return clip if f.props.PlaneStatsAverage > threshold else filtered

    if threshold_range and threshold_range > threshold:
        raise ValueError('limit_dark: "threshold_range" must be a lower value than "threshold"!')

    avg = core.std.PlaneStats(clip)
    f_eval = core.std.FrameEval(clip, partial(_diff, clip=clip, filtered=filtered, threshold=threshold, threshold_range=threshold_range), avg)
    return f_eval


def fix_cr_tint(clip: vs.VideoNode, value: int=128) -> vs.VideoNode:
    if get_depth(clip) != 16:
        clip = fvf.Depth(clip, 16)

    return core.std.Expr(clip, f'x {value} +, x {value} +, x {value} +')


def wipe_row(clip: vs.VideoNode, secondary: vs.VideoNode=None,
             width: int=1, height: int=1,
             offset_x: int=0, offset_y: int=0,
             width2: Optional[int]=None, height2: Optional[int]=None,
             offset_x2: Optional[int]=None, offset_y2: Optional[int]=None,
             show_mask: bool=False) -> vs.VideoNode:
    """
    Simple function to wipe a row with a blank clip.
    You can also give it a different clip to replace a row with.

    if width2, height2, etc. are given, it will merge the two masks.
    """
    secondary = core.std.BlankClip(clip) if secondary is None else secondary

    sqmask = kgf.squaremask(clip, width, height, offset_x, offset_y)
    if (width2    is not None and
        height2   is not None and
        offset_x2 is not None and
        offset_y2 is not None):
        sqmask2 = kgf.squaremask(clip, width2, height2, offset_x2, offset_y2)
        sqmask = core.std.Expr([sqmask, sqmask2], "x y +")

    if show_mask:
        return sqmask
    return core.std.MaskedMerge(clip, secondary, sqmask)


#### Miscellaneous


def source(file: str,
           force_lsmas: bool = False,
           ref=None,
           fpsnum: int = None, fpsden: int = None) -> vs.VideoNode:
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


# Helper funcs

def one_plane(clip):
    """
    Checks if the source clip is a single plane.
    """
    return clip.format.num_planes == 1


# Aliases
src = source
comp = compare
scomp = stack_compare
qden = quick_denoise
cond_desc = conditional_descale
