"""
    Various functions I make use of often and other people might be able to use too.
    Suggestions and fixes are always appreciated!
"""

import random
from functools import partial

import fvsfunc as fvf                           # https://github.com/Irrational-Encoding-Wizardry/fvsfunc
import havsfunc as haf                          # https://github.com/HomeOfVapourSynthEvolution/havsfunc
import kagefunc as kgf                          # https://github.com/Irrational-Encoding-Wizardry/kagefunc
import mvsfunc as mvf                           # https://github.com/HomeOfVapourSynthEvolution/mvsfunc
from nnedi3_rpow2 import *                      # https://github.com/darealshinji/vapoursynth-plugins/blob/master/scripts/nnedi3_rpow2.py
from nnedi3_resample import nnedi3_resample     # https://github.com/mawen1250/VapourSynth-script/blob/master/nnedi3_resample.py
from vsTAAmbk import TAAmbk                     # https://github.com/HomeOfVapourSynthEvolution/vsTAAmbk
from vsutil import *                            # https://github.com/Irrational-Encoding-Wizardry/vsutil

core = vs.core

"""
    optional dependencies: (http://www.vapoursynth.com/doc/pluginlist.html)
        * FFMS2
        * L-SMASH Source
        * d2vsource
        * waifu2x-caffe
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
        - nneedi3_clamp
        - transpose_aa
        - upscaled_sraa

    Deinterlacing:
        - deblend
        - decomb

    Denoising and Debanding:
        - quick_denoise (qden)

    Masking, Limiting, and Color Handling:
        - limit_dark
        - fix_cr_tint
        - wipe_row

    Miscellaneous:
        - source (src)
"""

#### Comparison and Analysis Functions

def compare(clip_a: vs.VideoNode, clip_b: vs.VideoNode,
            frames: List[int] = None,
            rand_total: int = None,
            force_resample: bool = True, print_frame: bool = True,
            mismatch: bool = False) -> vs.VideoNode:
    funcname = "compare"
    """
    Allows for the same frames from two different clips to be compared by putting them next to each other in a list.
    Clips are automatically resampled to 8bit YUV -> RGB24 to emulate how a monitor shows the frame.
    This can be disabled by setting `disable_resample` to True.

    Shorthand for this function is "comp".

    :param frames: int:               List of frames to compare
    :param rand_total: int:           Amount of random frames to pick
    :param force_resample: bool:      Forcibly resamples the clip to RGB24
    :param print_frame: bool:         Print frame numbers
    :param mismatch: bool:            Allow for clips with different formats and dimensions to be compared
    """
    def resample(clip):
        # Resampling to 8bit and RGB to properly display how it appears on your screen
        return fvf.Depth(mvf.ToRGB(clip), 8)

    # Error handling
    if frames and len(frames) > clip_a.num_frames:
        return error(funcname, 'More comparisons asked for than frames available')

    if force_resample:
        clip_a, clip_b = resample(clip_a), resample(clip_b)
    else:
        if clip_a.format.id != clip_b.format.id:
            return error(funcname, 'The format of both clips must be equal')

    if print_frame:
        clip_a, clip_b = clip_a.text.FrameNum(), clip_b.text.FrameNum()

    if frames is None:
        if not rand_total:
            # More comparisons for shorter clips so you can compare stuff like NCs more conveniently
            rand_total = int(clip_a.num_frames/1000) if clip_a.num_frames > 5000 else int(clip_a.num_frames/100)
        frames = sorted(random.sample(range(1, clip_a.num_frames-1), rand_total))

    frames_a = core.std.Splice([clip_a[f] for f in frames])
    frames_b = core.std.Splice([clip_b[f] for f in frames])
    return core.std.Interleave([frames_a, frames_b], mismatch=mismatch)


def stack_compare(*clips: vs.VideoNode,
                  width: int = None, height: int = 360,
                  stack_vertical: bool = False,
                  make_diff: bool = True,
                  warn: bool = True) -> vs.VideoNode:
    funcname = "stack_compare"
    """
    A simple wrapper that allows you to compare two clips by stacking them.
    You can stack an infinite amount of clips.

    Best to use when trying to match two sources frame-accurately, however by setting height to the source's
    height (or None), it can be used for comparing frames.

    Shorthand for this function is 'scomp'.

    :param stack_vertical: bool:    Stack frames vertically
    :param make_diff: bool:         Create and stack a diff (only works if two clips are given)
    :param warn: bool:              Prints the lengths of every given clip if lengths don't match
    """
    if len(clips) < 2:
        return error(funcname, 'Please select two or more clips to compare')

    if len(set([c.format.id for c in clips])) != 1:
        return error(funcname, 'The format of every clip must be equal')

    if len(clips) != 2 and make_diff:
        return error(funcname, 'You can only create a diff for two clips')

    height = fallback(height, clips[0].height)
    width = fallback(width, (get_w(height, aspect_ratio=clips[0].width / clips[0].height)))
    clips = [c.resize.Bicubic(width, height) for c in clips]
    if make_diff:
        diff = core.std.MakeDiff(get_y(clips[0]), get_y(clips[1])).resize.Bilinear(format=clips[0].format)
        clips.append(diff)

    stack = core.std.StackVertical(clips) if stack_vertical else core.std.StackHorizontal(clips)

    if warn:
        if len(set([c.num_frames for c in clips])) != 1:
            frame_counts = [c.num_frames for c in clips[:-1]] if make_diff else [c.num_frames for c in clips]
            stack = core.text.Text(stack, f"Lengths per clip (in given order): \n{frame_counts}")
    return stack


def stack_planes(clip: vs.VideoNode,
                 stack_vertical: bool = False) -> vs.VideoNode:
    funcname = "stack_planes"
    """
    Stacks the planes of a clip.

    :param stack_vertical: bool:    Stack the planes vertically
    """

    y, u, v = kgf.split(clip)
    subsampling = get_subsampling(clip)

    if subsampling == '420':
        if stack_vertical:
            u_v = core.std.StackHorizontal([u, v])
            return core.std.StackVertical([y, u_v])
        else:
            u_v = core.std.StackVertical([u, v])
            return core.std.StackHorizontal([y, u_v])
    elif subsampling == '444':
        return core.std.StackVertical([y, u, v]) if stack_vertical else core.std.StackHorizontal([y, u, v])
    else:
        return error(funcname, 'input clip must be in YUV format with 444 or 420 chroma subsampling')


def tvbd_diff(tv: vs.VideoNode, bd: vs.VideoNode,
              thr: float = 72,
              return_array: bool = False) -> vs.VideoNode:
    funcname = "tvbd_diff"
    """
    Creates a standard `compare` between frames from two clips that have differences.
    Useful for making comparisons between TV and BD encodes, as well as clean and hardsubbed sources.

    There are two methods used here to find differences.
    If thr is below 1, PlaneStatsDiff is used to figure out the differences.
    Else, if thr is equal than or higher than 1, PlaneStatsMin/Max are used.

    Recommended is PlaneStatsMin/Max, as those seem to catch
    more outrageous differences more easily and not return
    too many starved frames.

    Note that this might catch artifacting as differences!
    Make sure you verify every frame with your own eyes!

    :param thr: float:          Threshold. <= 1 uses PlaneStatsDiff, >1 uses Max/Min. Max is 128
    :param return_array: bool:  Return frames as an array comparison (using "compare")
    """
    if thr > 128:
        return error(funcname, '"thr" should not be or exceed 128!')

    bd = core.resize.Bicubic(bd, format=tv.format)

    try:
        if thr <= 1:
            diff = core.std.PlaneStats(tv, bd)
            frames = [i for i,f in enumerate(diff.frames()) if f.props["PlaneStatsDiff"] > thr]
        else:
            diff = core.std.MakeDiff(tv, bd).std.PlaneStats()
            frames = [i for i,f in enumerate(diff.frames()) if f.props["PlaneStatsMin"] <= thr or f.props["PlaneStatsMax"] >= 255 - thr]
    except:
        return error(funcname, 'No differences found')

    if return_array:
        return compare(tv.text.FrameNum().text.Text('TV', 9),
                           bd.text.FrameNum().text.Text('BD', 9),
                           frames)
    else:
        if thr <= 1:
            diff = core.std.MakeDiff(tv, bd)
        diff = core.resize.Spline36(diff, get_w(576), 576).text.FrameNum(8)
        tv, bd = core.resize.Spline36(tv, diff.width/2, diff.height/2), core.resize.Spline36(bd, diff.width/2, diff.height/2)
        tv, bd = tv.text.Text("TV source", 3), bd.text.Text("BD source", 1)
        stacked = core.std.StackVertical([core.std.StackHorizontal([tv, bd]), diff])
        return core.std.Splice([stacked[f] for f in frames])


#### Scaling and Resizing Functions

def conditional_descale(clip: vs.VideoNode, height: int,
                        kernel: str = 'bicubic',
                        b: float = 1 / 3, c: float = 1 / 3,
                        taps: int = 4,
                        threshold: float = 0.003,
                        upscaler: str = None) -> vs.VideoNode:
    funcname = "conditional_descale"
    """
    Descales and reupscales a clip. If the difference exceeds the threshold, the frame will not be descaled.
    If it does not exceed the threshold, the frame will upscaled using either nnedi3_rpow2 or waifu2x-caffe.

    Useful for bad BDs that have additional post-processing done on some scenes, rather than all of them.

    Currently only works with bicubic, and has no native 1080p masking.
    Consider scenefiltering OP/EDs with a different descale function instead.

    The code for _get_error was mostly taken from kageru's Made in Abyss script.
    Special thanks to Lypheo for holding my hand as this was written.

    :param height: int:                   Target descale height
    :param threshold: float:              Threshold for deciding to descale or leave the original frame
    :param upscaler: str:                 What scaler is used to upscale (options: nnedi3_rpow2 (default), upscaled_sraa, waifu2x)
    :param replacement_clip: videoNode    A clip to replace frames that were not descaled with.
    """
    def _get_error(clip, height, kernel, b, c, taps):
        descale = fvf.Resize(clip, get_w(height), height,  kernel=kernel, a1=b, a2=c, taps=taps, invks=True)
        upscale = fvf.Resize(clip, clip.width, clip.height,  kernel=kernel, a1=b, a2=c, taps=taps)
        diff = core.std.PlaneStats(upscale, clip)
        return descale, diff

    def _diff(n, f, clip_a, clip_b, threshold):
        return clip_a if f.props.PlaneStatsDiff > threshold else clip_b

    if get_depth(clip) != 32:
        clip = fvf.Depth(clip, 32, dither_type='none')

    planes = kgf.split(clip)
    descaled, diff = _get_error(planes[0], height=height, kernel=kernel, b=b, c=c, taps=taps)

    upscaler = upscaler or "nnedi3_rpow2"
    if upscaler in ['nnedi3_rpow2', 'nnedi3', 'nn3_rp2']:
        planes[0] = nnedi3_rpow2(descaled).resize.Spline36(clip.width, clip.height)
    elif upscaler in ['nnedi3_resample', 'nn3_res']:
        planes[0] = nnedi3_resample(descaled, clip.width, clip.height, kernel='gauss', invks=True, invkstaps=2, taps=1, a1=32, nns=4, qual=2, pscrn=4)
    elif upscaler in ['upscaled_sraa', 'up_sraa', 'sraa']:
        planes[0] = upscaled_sraa(descaled, h=clip.height, sharp_downscale=False).resize.Spline36(clip.width)
    elif upscaler in ['waifu2x', 'w2x']:
        planes[0] = core.caffe.Waifu2x(descaled, noise=-1, scale=2, model=6, cudnn=True, processor=0,  tta=False).resize.Spline36(clip.width, clip.height)
    else:
        return error(funcname, f'"{upscaler}" is not a valid option for "upscaler". Please pick either "nnedi3_rpow2", "nnedi3_resample", "upscaled_sraa", or "waifu2x"')

    descaled = kgf.join(planes).resize.Spline36(format=clip.format)
    descaled = descaled.std.SetFrameProp("_descaled", intval=1)
    clip = clip.std.SetFrameProp("_descaled", intval=0)

    return core.std.FrameEval(clip, partial(_diff, clip_a=clip, clip_b=descaled, threshold=threshold),  diff)


# TO-DO: Fix smart_descale failing on specific resolutions for unknown reasons
#        Fix smart_descale not returning the frameprop with the height it was descaled to

def smart_descale(clip: vs.VideoNode,
                  res: List[int],
                  b: float = 1/3, c: float = 1/3,
                  thresh1: float = 0.03, thresh2: float = 0.7,
                  no_mask: float = False,
                  show_mask: bool = False, show_dmask: bool = False,
                  sraa_upscale: bool = False, rfactor: float = 1.5,
                  sraa_sharp: bool = False) -> vs.VideoNode:
    funcname = "smart_descale"
    """
    Original function written by kageru and modified into a general function by me.
    For more information and comments I suggest you check out the original script:
        https://git.kageru.moe/kageru/vs-scripts/src/branch/master/abyss1.py

    A descaling function that compares relative errors between multiple resolutions and descales accordingly.
    Most of this code was leveraged from kageru's Made in Abyss script.
    As this is an incredibly complex function, I will offer only minimal support.

    :param res: List[int]:             A list of resolutions to descale to. For example: [900, 871, 872, 877]
    :param thresh1: float:             Threshold for when a frame will be descaled.
    :param thresh2: float:             Threshold for when a frame will not be descaled.
    :param sraa_upscale: bool:         Use upscaled_sraa to upscale the frames (warning: very slow!)
    :param rfactor: float:             Image enlargement factor for upscaled_sraa
    """
    def _descaling(clip: vs.VideoNode, h: int, b: float, c: float):
        # Descale and return a tuple of descaled clip and diff mask between that and the original.
        down = clip.descale.Debicubic(get_w(h), h, b, c)
        up = down.resize.Bicubic(clip.width, clip.height, filter_param_a=b, filter_param_b=c)
        diff = core.std.Expr([clip, up], 'x y - abs').std.PlaneStats()
        return down, diff

    def _select(n, y, debic_list, sraa_upscale, rfactor, f):
        # This simply descales to each of those and selects the most appropriate for each frame.
        errors = [x.props.PlaneStatsAverage for x in f]
        y_deb = debic_list[errors.index(min(errors))]
        dmask = core.std.Expr([y, y_deb.resize.Bicubic(clip.width, clip.height)], 'x y - abs 0.025 > 1 0 ?').std.Maximum().std.SetFrameProp("_descaled_resolution", intval=y_deb.height)

        if sraa_upscale:
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
        # Just revert the entire scaling if the difference is too big. This should catch the 1080p scenes.
        if f.props.PlaneStatsAverage < thresh_a:
            return clip.std.SetFrameProp("_descaled", intval=1)
        elif f.props.PlaneStatsAverage > thresh_b:
            return orig.std.SetFrameProp("_descaled", intval=0)
        return core.std.Merge(clip, orig, (f.props.PlaneStatsAverage - thresh_a) * 20).std.SetFrameProp("_descaled", intval=2)

    # Error handling
    if len(res) < 2:
        return error(funcname, 'This function requires more than two resolutions to descale to')


    og = clip
    clip32 = fvf.Depth(clip, 32)
    if one_plane(clip32):
        y = get_y(clip32)
    else:
        y, u, v = split(clip32)

    debic_listp = [_descaling(y, h, b, c) for h in res]
    debic_list = [a[0] for a in debic_listp]
    debic_props = [a[1] for a in debic_listp]

    y_deb = core.std.FrameEval(y, partial(_select, y=y, debic_list=debic_list,
                                                  sraa_upscale=sraa_upscale, rfactor=rfactor), prop_src=debic_props)
    # TO-DO: It returns a frame size error here for whatever reason. Need to figure out what causes it and fix it
    dmask = core.std.PropToClip(y_deb)
    if show_dmask:
        return dmask
    # TO-DO: Figure out how to make it properly round depending on resolution (although this should usually be 1080p anyway)
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


# TO-DO: Apply descale based on average error in a frame range rather than on a per-frame basis
#        in order to prevent visible differences. Chances are if a couple of frames in a cut can't
#        be descaled, all of them are no good.


def test_descale(clip: vs.VideoNode,
                 height: int,
                 kernel: str = 'bicubic',
                 b: float = 1 / 3, c: float = 1 / 3,
                 taps: int = 3,
                 show_error: bool = True) -> vs.VideoNode:
    funcname = "test_descale"
    """
    Generic function to test descales with.
    Descales and reupscales a given clip, allowing you to compare the two easily.

    When comparing, it is recommended to do atleast a 4x zoom using Nearest Neighbor.
    I also suggest using 'compare', as that will make comparison a lot easier.

    Some of this code was leveraged from DescaleAA, and it also uses functions
    available in fvsfunc.

    :param height: int:         Target descaled height.
    :param kernel: str:         Descale kernel - 'bicubic'(default), 'bilinear', 'lanczos', 'spline16', or 'spline36'
    :param b: float:            B-param for bicubic kernel. (Default value = 1 / 3)
    :param c: float:            C-param for bicubic kernel. (Default value = 1 / 3)
    :param taps: int:           Taps param for lanczos kernel. (Default value = 43)
    :param show_error: bool:    Show diff between the original clip and the reupscaled clip
    """

    clip_y = get_y(clip)

    desc = fvf.Resize(clip_y, get_w(height), height,
                      kernel=kernel, a1=b, a2=c, taps=taps,
                      invks=True)
    upsc = fvf.Resize(desc, clip.width, clip.height,
                      kernel=kernel, a1=b, a2=c, taps=taps)
    upsc = core.std.PlaneStats(clip_y, upsc)

    if clip is vs.GRAY:
        return core.text.FrameProps(upsc, "PlaneStatsDiff") if show_error else upsc
    merge = core.std.ShufflePlanes([upsc, clip], planes=[0, 1, 2], colorfamily=vs.YUV)
    return core.text.FrameProps(merge, "PlaneStatsDiff") if show_error else merge


# TO-DO: Write a function that checks every possible combination of B and C in bicubic
#        and returns a list of the results. Possibly return all the frames in order of
#        smallest difference to biggest. Not reliable, but maybe useful as starting point.


# TO-DO: Write "multi_descale", a function that allows you to descale a frame twice,
#        like for example when the CGI in a show is handled in a different resolution
#        than the drawn animation.


#### Antialiasing functions

def nneedi3_clamp(clip: vs.VideoNode, strength: int = 1,
                  mask: vs.VideoNode = None,
                  ret_mask: bool = False, show_mask: bool = False,
                  opencl: bool = False) -> vs.VideoNode:
    funcname = "nneedi3_clamp"
    """
    Script written by Zastin. What it does is clamp the "change" done by eedi3 to the "change" of nnedi3.
    This should fix every issue created by eedi3. For example: https://i.imgur.com/hYVhetS.jpg

    :param strength:            Set threshold strength
    :param mask:                Allows for user to use their own mask
    :param ret_mask: bool:      Replace default mask with a retinex edgemask
    :param show_mask: bool:     Return mask
    :param opencl: bool:        Opencl acceleration
    """
    bits = clip.format.bits_per_sample - 8
    thr = strength * (1 >> bits)
    strong = TAAmbk(clip, aatype='Eedi3', alpha=0.25, beta=0.5, gamma=40, nrad=2, mdis=20, mtype=0,
                    opencl=opencl)
    weak = TAAmbk(clip, aatype='Nnedi3', nsize=3, nns=3, qual=1, mtype=0, opencl=opencl)
    expr = 'x z - y z - * 0 < y x y {0} + min y {0} - max ?'.format(thr)

    if clip.format.num_planes > 1:
        expr = [expr, '']
    aa = core.std.Expr([strong, weak, clip], expr)

    if mask:
        merged = clip.std.MaskedMerge(aa, mask, planes=0)
    elif ret_mask:
        mask = kgf.retinex_edgemask(clip, 1).std.Binarize()
        merged = clip.std.MaskedMerge(aa, mask, planes=0)
    else:
        mask = clip.std.Prewitt(planes=0).std.Binarize(planes=0).std.Maximum(planes=0).std.Convolution([1] * 9, planes=0)
        mask = get_y(mask)
        merged = clip.std.MaskedMerge(aa, mask, planes=0)

    if show_mask:
        return mask
    return merged if clip.format.color_family == vs.GRAY else core.std.ShufflePlanes([merged, clip], [0, 1, 2], vs.YUV)


def transpose_aa(clip: vs.VideoNode, eedi3: bool = False) -> vs.VideoNode:
    funcname = "transpose_aa"
    """
    Function written by Zastin and modified by me.
    Performs anti-aliasing over a clip by using Nnedi3, transposing, using Nnedi3 again, and transposing a final time.
    This results in overall stronger anti-aliasing.
    Useful for shows like Yuru Camp with bad lineart problems.

    :param eedi3: bool:     Use eedi3 for the interpolation instead

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
                  h: int = None, ar = None,
                  sharp_downscale: bool = False) -> vs.VideoNode:
    funcname = "upscaled_sraa"
    """
    Another AA written by Zastin and modified by me.
    Performs an upscaled single-rate AA to deal with heavy aliasing.
    Useful for Web rips, where the source quality is not good enough to descale,
    but you still want to deal with some bad aliasing and lineart.
    :param rfactor: float:  Image enlargement factor. 1.3..2 makes it comparable in strength to vsTAAmbk
                            It is not recommended to go below 1.3
    :param rep: int:        Repair mode
    :param h: int:          Set custom height. Width and aspect ratio are auto-calculated
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
        if not ar:
            ar = clip.width / clip.height
        w = get_w(h, aspect_ratio=ar)
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
            if get_subsampling(clip) == "420":
                planes[1], planes[2] = [core.resize.Bicubic(p, w / 2, h / 2, src_left=.25 * (1 - clip.width / w )) for p in planes[1:]]
                return join([scaled, planes[1], planes[2]])
            elif get_subsampling(clip) == "444":
                planes[1], planes[2] = [core.resize.Bicubic(p, w, h) for p in planes[1:]]
                return join([scaled, planes[1], planes[2]])
            else:
                return error(funcname, f"Please use either a 420, 444, or GRAY clip rather than a '{get_subsampling(clip)}' clip")


#### Deinterlacing

def deblend(clip: vs.VideoNode, rep: int = None) -> vs.VideoNode:
    funcname = "deblend"
    """
    A simple function to fix deblending for interlaced video with an AABBA blending pattern,
    where A is a normal frame and B is a blended frame.

    Assuming there's a constant pattern of frames (labeled A, B, C, CD, and DA in this function),
    blending can be fixed by calculating the C frame by getting halves of CD and DA, and using that
    to fix up CD. DA can then be dropped due to it being an interlaced frame.

    However, doing this will result in some of the artifacting being added to the deblended frame.
    We can mitigate this by repairing the frame with the non-blended frame before it.

    For more information, please refer to this blogpost by torchlight:
    https://mechaweaponsvidya.wordpress.com/2012/09/13/adventures-in-deblending/

    :param rep: int: Repair mode for the deblended frames
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


def decomb(src: vs.VideoNode,
           TFF: Optional[bool] = None,
           decimate: bool = True,
           vinv: bool = False,
           sharpen: bool = False, dir: str = 'v',
           rep: Optional[int] = None):
    funcname = "decomb"
    """
    Function written by Midlifecrisis from the WEEB AUTISM server, and slightly modified by me.

    This function does some aggressive filtering to get rid of the combing on a interlaced/telecined source.
    You can also allow it to decimate the clip, or keep it disabled if you wish to handle the decimating yourself.
    Vinverse can also be disabled, allowing for less aggressive decombing. Note that this means far more combing will be left over!

    :param TFF: bool:           Top-Field-First. Mandatory to set. Set to either "True" or False"
    :param decimate: bool:      Decimate the video after deinterlacing
    :param vinv: bool:          Use vinverse to get rid of additional combing
    :param sharpen: bool:       Unsharpen after deinterlacing
    :param dir: str:            Directional vector. 'v' = Vertical, 'h' = Horizontal
    :param rep: int:            Repair mode for repairing the decombed frame using the original src frame
    """
    if TFF is None:
        return error(funcname, '"TFF" has to be set to either "True" or "False"!')
    VFM_TFF = int(TFF)

    def pp(n, f, clip, pp):
        return pp if f.props._Combed == 1 else clip

    src = core.vivtc.VFM(src, order=VFM_TFF, mode=1)
    combmask = core.comb.CombMask(src, cthresh=1, mthresh=3)
    combmask = core.std.Maximum(combmask, threshold=250).std.Maximum(threshold=250).std.Maximum(threshold=250).std.Maximum(threshold=250)
    combmask = core.std.BoxBlur(combmask, hradius=2, vradius=2)

    qtgmc = haf.QTGMC(src, TFF=TFF, SourceMatch=3, Lossless=2, TR0=1, TR1=2, TR2=3, FPSDivisor=2)
    qtgmc_merged = core.std.MaskedMerge(src, qtgmc, combmask, first_plane=True)

    decombed = core.std.FrameEval(src, partial(pp, clip=src, pp=qtgmc_merged), src)

    decombed = decombed.vinverse.Vinverse() if vinv else decombed
    decombed = dir_unsharp(decombed, dir=dir) if sharpen else decombed
    decombed = core.rgvs.Repair(decombed, src, rep) if rep else decombed
    return core.vivtc.VDecimate(decombed) if decimate else decombed


def dir_deshimmer(clip: vs.VideoNode, TFF: bool = True,
                  dh: bool = False,
                  transpose: bool = True,
                  show_mask: bool = False) -> vs.VideoNode:
    funcname = "dir_deshimmer"
    """
    Directional deshimmering function

    Only works (in the few instances it does, anyway) for obvious horizontal and vertical shimmering.
    Odds of success are low. But if you're desperate, it's worth a shot.

    :param dh: bool:           Interpolate to double the height of given clip beforehand
    :param TFF: bool:          Top Field First. Set to False if TFF doesn't work
    :param transpose: bool:    Transpose the clip before attempting to deshimmer
    :param show_mask: bool:    Show nnedi3's mask
    """
    clip = core.std.Transpose(clip) if transpose else clip
    deshim = core.nnedi3.nnedi3(clip, field=TFF, dh=dh, show_mask=show_mask)
    return core.std.Transpose(deshim) if transpose else deshim


def dir_unsharp(clip: vs.VideoNode,
                strength: float = 1.0,
                dir: str = 'v',
                h: float = 3.4) -> vs.VideoNode:
    funcname = "dir_unsharp"
    """
    A diff'd directional unsharpening function.
    Special thanks to thebombzen and kageru for essentially writing the bulk of this.

    Performs one-dimensional sharpening as such: "Original + (Original - blurred) * Strength"

    This particular function is recommended for SD content, specifically after deinterlacing.

    :param strength: float:        Amount to multiply blurred clip with original clip by
    :param dir: str:               Directional vector. 'v' = Vertical, 'h' = Horizontal
    :param h: float:               Sigma for knlmeans, to prevent noise from getting sharpened
    """

    dir = dir.lower()
    if dir not in ['v', 'h']:
        return error(funcname, f'"dir" must be either "v" or "h", not {dir}')

    den = core.knlm.KNLMeansCL(clip, d=3, a=3, h=h)
    diff = core.std.MakeDiff(clip, den)

    blur_matrix = [1, 2, 1]
    blurred_clip = core.std.Convolution(den, matrix=blur_matrix, mode=dir)
    unsharp = core.std.Expr(clips=[den, blurred_clip], expr=['x y - ' + str(strength) + ' * x +', "", ""])
    return core.std.MergeDiff(unsharp, diff)


#### Denoising and Debanding

def quick_denoise(clip: vs.VideoNode,
                  ref: vs.VideoNode = None,
                  cmode: str = 'knlm',
                  sigma: float = 2,
                  **kwargs) -> vs.VideoNode:
    funcname = "quick_denoise"
    """
    A rewrite of my old 'quick_denoise'. I still hate it, but whatever.
    This will probably be removed in a future commit.

    This wrapper is used to denoise both the luma and chroma using various denoisers of your choosing.
    If you wish to use just one denoiser,
    you're probably better off using that specific filter rather than this wrapper.

    BM3D is used for denoising the luma.

    Special thanks to kageru for helping me out with some ideas and pointers.

    :param sigma:               Denoising strength for BM3D
    :param cmode:               Chroma denoising modes:
                                 1 - Use knlmeans for denoising the chroma
                                 2 - Use tnlmeans for denoising the chroma
                                 3 - Use dfttest for denoising the chroma (requires setting 'sbsize' in kwargs)
                                 4 - Use SMDegrain for denoising the chroma
    :param ref: vs.VideoNode:  Optional reference clip to replace BM3D's basic estimate

    """
    y, u, v = kgf.split(clip)
    cmode = cmode.lower()

    if cmode in [1, 'knlm', 'knlmeanscl']:
        den_u = u.knlm.KNLMeansCL(d=3, a=2, **kwargs)
        den_v = v.knlm.KNLMeansCL(d=3, a=2, **kwargs)
    elif cmode in [2, 'tnlm', 'tnlmeans']:
        den_u = u.tnlm.TNLMeans(ax=2, ay=2, az=2, **kwargs)
        den_v = v.tnlm.TNLMeans(ax=2, ay=2, az=2, **kwargs)
    elif cmode in [3, 'dft', 'dfttest']:
        if 'sbsize' in kwargs:
            den_u = u.dfttest.DFTTest(sosize=kwargs['sbsize'] * 0.75, **kwargs)
            den_v = v.dfttest.DFTTest(sosize=kwargs['sbsize'] * 0.75, **kwargs)
        else:
            return error(funcname, "'sbsize' not specified")
    elif cmode in [4, 'smd', 'smdegrain']:
        den_u = haf.SMDegrain(u, prefilter=3, **kwargs)
        den_v = haf.SMDegrain(v, prefilter=3, **kwargs)
    else:
        return error(funcname, 'unknown cmode')

    den_y = mvf.BM3D(y, sigma=sigma, psample=0, radius1=1, ref=ref)
    return core.std.ShufflePlanes([den_y, den_u, den_v], 0, vs.YUV)


#### Masking, Limiting, and Color Handling


def edgefixer(clip: vs.VideoNode,
              left: Optional[List[int]] = None, right: Optional[List[int]] = None,
              top: Optional[List[int]] = None, bottom: Optional[List[int]] = None,
              radius: Optional[List[int]] = None,
              full_range: bool = False) -> vs.VideoNode:
    """
    A wrapper for ContinuityFixer (https://github.com/MonoS/VS-ContinuityFixer).

    Fixes the issues with over- and undershoot that it may create when fixing the edges,
    and adds what are in my opinion "more sane" ways of handling the parameters and given values.

    :param left: List[int]:        Amount of pixels to fix. Extends to right, top, and bottom
    :param radius: List[int]:      Radius for edgefixing
    :param full_range: bool:       Does not run the expression over the clip to fix over/undershoot
    """

    if left is None:
        left = 0
    if right is None:
        right = left
    if top is None:
        top = left
    if bottom is None:
        bottom = top

    ef = core.edgefixer.ContinuityFixer(clip, left, top, right, bottom, radius)
    return ef if full_range else core.std.Expr(ef, "x 16 max 235 min")


def fix_cr_tint(clip: vs.VideoNode, value: int = 128) -> vs.VideoNode:
    funcname = "fix_cr_tint"
    """
    Tries to forcibly fix Crunchyroll's green tint by adding pixel values

    :param value: int:  Values added to every pixel
    """
    if get_depth(clip) != 16:
        clip = fvf.Depth(clip, 16)
    return core.std.Expr(clip, f'x {value} +')


def limit_dark(clip: vs.VideoNode, filtered: vs.VideoNode,
               threshold: float = .25, threshold_range: int = None) -> vs.VideoNode:
    funcname = "limit_dark"
    """
    Replaces frames in a clip with a filtered clip when the frame's darkness exceeds the threshold.
    This way you can run lighter (or heavier) filtering on scenes that are almost entirely dark.

    There is one caveat, however: You can get scenes where every other frame is filtered
    rather than the entire scene. Please do take care to avoid that if possible.

    threshold: float:       Threshold for frame averages to be filtered
    threshold_range: int:   Threshold for a range of frame averages to be filtered
    """
    def _diff(n, f, clip, filtered, threshold, threshold_range):
        if threshold_range:
            return filtered if threshold_range <= f.props.PlaneStatsAverage <= threshold else clip
        else:
            return clip if f.props.PlaneStatsAverage > threshold else filtered

    if threshold_range and threshold_range > threshold:
        return error(funcname, f'"threshold_range" ({threshold_range}) must be a lower value than "threshold" ({threshold})')

    avg = core.std.PlaneStats(clip)
    return core.std.FrameEval(clip, partial(_diff, clip=clip, filtered=filtered, threshold=threshold, threshold_range=threshold_range), avg)


def wipe_row(clip: vs.VideoNode, secondary: vs.VideoNode = None,
             width: int = 1, height: int = 1,
             offset_x: int = 0, offset_y: int = 0,
             width2: Optional[int] = None, height2: Optional[int] = None,
             offset_x2: int = 0, offset_y2: Optional[int] = None,
             show_mask: bool = False) -> vs.VideoNode:
    funcname = "wipe_row"
    """
    Simple function to wipe a row with a blank clip.
    You can also give it a different clip to replace a row with.

    if width2, height2, etc. are given, it will merge the two masks.

    :param secondary: vs.VideoNode:     Appoint a different clip to replace wiped rows with
    """
    secondary = secondary or core.std.BlankClip(clip)

    sqmask = kgf.squaremask(clip, width, height, offset_x, offset_y)
    if width2 and height2:
        sqmask2 = kgf.squaremask(clip, width2, height2, offset_x2, offset_y - 1 if offset_y2 is None else offset_y2)
        sqmask = core.std.Expr([sqmask, sqmask2], "x y +")

    if show_mask:
        return sqmask
    return core.std.MaskedMerge(clip, secondary, sqmask)


# TODO: Write function that only masks px of a certain color/threshold of colors.
#       Think the magic wand tool in various image-editing programs.


#### Miscellaneous

def source(file: str, ref: vs.VideoNode = None,
           force_lsmas: bool = False,
           mpls: bool = False,  mpls_playlist: int = 0, mpls_angle: int = 0) -> vs.VideoNode:
    funcname = "source"
    """
    Generic clip import function.
    Automatically determines if ffms2 or L-SMASH should be used to import a clip, but L-SMASH can be forced.
    It also automatically determines if an image has been imported.
    You can set its fps using 'fpsnum' and 'fpsden', or using a reference clip with 'ref'.

    :param file: str:               OS absolute file location
    :param ref: vs.VideoNode:       Use another clip as reference for the clip's format, resolution, and framerate
    :param force_lsmas: bool:       Force files to be imported with L-SMASH
    :param mpls: bool:              Load in a mpls file
    :param mpls_playlist: int:     Playlist number, which is the number in mpls file name
    :param mpls_angle: int:        Angle number to select in the mpls playlist
    """
    # TODO: Consider adding kwargs for additional options,
    #       find a way to NOT have to rely on a million elif's
    if file.startswith('file:///'):
        file = file[8::]

    # Error handling for some file types
    if file.endswith('.mpls') and mpls is False:
        return error(funcname, 'Please set \'mpls = True\' and give a path to the base Blu-ray directory when trying to load in mpls files')
    if file.endswith('.vob') or file.endswith('.ts'):
        return error(funcname, 'Please index VOB and TS files into d2v files before importing them')

    if force_lsmas:
        return core.lsmas.LWLibavSource(file)

    elif mpls:
        mpls = core.mpls.Read(file, mpls_playlist)
        clip = core.std.Splice([core.lsmas.LWLibavSource(mpls['clip'][i]) for i in range(mpls['count'])])

    elif file.endswith('.d2v'):
        clip = core.d2v.Source(file)
    elif file.endswith('.dgi'):
        clip = core.dgdecodenv.DGSource(file)
    elif is_image(file):
        clip = core.imwri.Read(file)
    else:
        if file.endswith('.m2ts'):
            clip = core.lsmas.LWLibavSource(file)
        else:
            clip = core.ffms2.Source(file)

    if ref:
        clip = core.std.AssumeFPS(clip, fpsnum=ref.fps.numerator, fpsden=ref.fps.denominator)
        clip = core.resize.Bicubic(clip, width=ref.width, height=ref.height, format=ref.format, matrix_s=mvf.GetMatrix(ref))
        if is_image(file):
            clip = clip*(ref.num_frames-1)
    return clip


# Experimental

from collections import namedtuple
from typing import Callable, List, Dict
import math

Resolution = namedtuple('Resolution', ['width', 'height'])
def smarter_descale(src: vs.VideoNode,
                    resolutions: List[int],
                    descaler: Optional[Callable[[vs.VideoNode, int, int], vs.VideoNode]] = None,
                    rescaler: Optional[Callable[[vs.VideoNode, int, int], vs.VideoNode]] = None,
                    upscaler: Optional[Callable[[vs.VideoNode, int, int], vs.VideoNode]] = None,
                    thr: float = 0.05,
                    rescale: bool = True, to_src: bool = False) -> vs.VideoNode:
    """
    An updated version of smart_descale, hence smart*er*_descale.
    Still in its experimental stage, and this is just a wrapper to also handle
    format conversions afterwards because x264 throws a fit otherwise.

    Example use:
        import functools
        import lvsfunc as lvf

        scaled = lvf.smarter_descale(src, range(840,849), functools.partial(core.descale.Debicubic, b=0, c=1/2), functools.partial(core.resize.Spline36))
        scaled.set_output()

    :param resolutions: List[int]:     A list of the resolutions to attempt to descale to. For example: "resolutions=[720, 810]"
                                        Range can help with easily getting a range of resolutions
    :param descaler:                   Descaler used. Default is descale.Bicubic
    :param rescaler:                   Rescaler used. Default is resize.Bicubic
    :param upscaler:                   Upscaler used. Default is resize.Bicubi.
    :param thr: float:                 Threshold for the descaling. Corrosponds directly to the same error rate as getscaler
    :param rescale: bool:              To rescale to the highest-given height and handle conversion for x264 fuckery. Default is True
    :param to_src: bool:               To upscale back to the src resolution with nnedi3_resample (inverse gauss)
    """

    descaler = descaler or core.descale.Debicubic
    rescaler = rescaler or core.resize.Bicubic
    upscaler = upscaler or core.resize.Spline36

    ScaleAttempt = namedtuple('ScaleAttempt', ['descaled', 'rescaled', 'resolution', 'diff'])
    src = fvf.Depth((get_y(src) if src.format.num_planes != 1 else src), 32) \
        .std.SetFrameProp('descaleResolution', intval=src.height)

    def perform_descale(height: int) -> ScaleAttempt:
        resolution = Resolution(get_w(height, src.width / src.height), height)
        descaled = descaler(src, resolution.width, resolution.height) \
            .std.SetFrameProp('descaleResolution', intval=height)
        rescaled = rescaler(descaled, src.width, src.height)
        diff = core.std.Expr([rescaled, src], 'x y - abs').std.PlaneStats()
        return ScaleAttempt(descaled, rescaled, resolution, diff)

    clips_by_resolution = {c.resolution.height: c for c in map(perform_descale, resolutions)}
    # If we pass a variable res clip as first argument to FrameEval, we’re also allowed to return one.
    variable_res_clip = core.std.Splice([
        core.std.BlankClip(src, length=len(src)-1), core.std.BlankClip(src, length=1, width=src.width + 1)
    ], mismatch=True)

    def select_descale(n: int, f: List[vs.VideoFrame]):
        # TODO: higher resolutions tend to be lower. compensate for that
        print(f)
        print()
        print([fr.props.PlaneStatsAverage for fr in f])
        best_res = max(f, key=lambda frame: math.log(src.height - frame.props.descaleResolution, 2) * round(1/frame.props.PlaneStatsAverage) ** 0.2)
        print('selected')
        print(clips_by_resolution)
        print(list(clips_by_resolution.keys()))
        print(best_res.props.descaleResolution)
        best_attempt = clips_by_resolution.get(best_res.props.descaleResolution)
        print('found')
        if threshold == 0:
            return best_attempt.descaled
        # No blending here because src and descaled have different resolutions.
        # The caller can use the frameProps to deal with that if they so desire.
        if best_res.props.PlaneStatsAverage > threshold:
            return src
        return best_attempt.descaled

    props = [c.diff for c in clips_by_resolution.values()]
    print(props)
    scaled = core.std.FrameEval(variable_res_clip, select_descale,
                                prop_src=props)

    if rescale:
        # You MUST set the output format again, or else x264/x265 will throw a hissy fit
        scaled = upscaler(scaled, get_w(resolutions.sort()[-1]), resolutions.sort()[-1], format=src.format)
        if to_src:
            # This is done after scaling up because else nn3_rs returns an error
            scaled = nnedi3_resample(scaled, src.width, src.height, kernel='gauss', invks=True, invkstaps=2, taps=1, a1=32, nns=4, qual=2, pscrn=4)
    return scaled


# Helper funcs

def one_plane(clip: vs.VideoNode) -> bool:
    return clip.format.num_planes == 1


def error(funcname: str, error_msg: str):
    # return errors in a slightly nicer way
    raise ValueError(f"{funcname}: {error_msg or 'An unknown error occured'}")


# Aliases
src = source
comp = compare
scomp = stack_compare
qden = quick_denoise
cond_desc = conditional_descale
sraa = upscaled_sraa
