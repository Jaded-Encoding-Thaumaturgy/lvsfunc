"""
    Functions intended to be used to make comparisons between different sources
    or to be used to analyze something from a single clip.
"""
import random
from typing import List, Optional

import vapoursynth as vs
from vsutil import depth, get_subsampling, get_w, split

core = vs.core


def compare(clip_a: vs.VideoNode, clip_b: vs.VideoNode,
            frames: Optional[List[int]] = None,
            rand_total: Optional[int] = None,
            force_resample: bool = True, print_frame: bool = True,
            mismatch: bool = False) -> vs.VideoNode:
    """
    Allows for the same frames from two different clips to be compared by interleaving them into a single clip.
    Clips are automatically resampled to 8 bit YUV -> RGB24 to emulate how a monitor shows the frame.
    This can be disabled by setting `disable_resample` to True.

    Alias for this function is `lvsfunc.comp`.

    Dependencies: mvsfunc

    :param clip_a:              Clip to compare
    :param clip_b:              Second clip to compare
    :param frames:              List of frames to compare (Default: None)
    :param rand_total:          Number of random frames to pick (Default: None)
    :param force_resample:      Forcibly resamples the clip to RGB24 (Default: True)
    :param print_frame:         Print frame numbers (Default: True)
    :param mismatch:            Allow for clips with different formats and dimensions to be compared (Default: False)

    :return:                    Interleaved clip containing specified frames from clip_a and clip_b
    """
    try:
        from mvsfunc import GetMatrix
    except ModuleNotFoundError:
        raise ModuleNotFoundError("compare: missing dependency 'mvsfunc'")

    def _resample(clip: vs.VideoNode) -> vs.VideoNode:
        # Resampling to 8 bit and RGB to properly display how it appears on your screen
        return depth(clip.resize.Point(format=vs.RGB24, matrix_in_s=GetMatrix(clip)), 8)

    # Error handling
    if frames and len(frames) > clip_a.num_frames:
        raise ValueError(f"compare: 'More comparisons requested than frames available'")

    if force_resample:
        clip_a, clip_b = _resample(clip_a), _resample(clip_b)
    else:
        if clip_a.format.id != clip_b.format.id:
            raise ValueError(f"compare: 'The format of both clips must be equal'")

    if print_frame:
        clip_a, clip_b = clip_a.text.FrameNum(), clip_b.text.FrameNum()

    if frames is None:
        if not rand_total:
            # More comparisons for shorter clips so you can compare stuff like NCs more conveniently
            rand_total = int(clip_a.num_frames / 1000) if clip_a.num_frames > 5000 else int(clip_a.num_frames / 100)
        frames = sorted(random.sample(range(1, clip_a.num_frames - 1), rand_total))

    frames_a = core.std.Splice([clip_a[f] for f in frames])
    frames_b = core.std.Splice([clip_b[f] for f in frames])
    return core.std.Interleave([frames_a, frames_b], mismatch=mismatch)


def stack_compare(*clips: vs.VideoNode,
                  make_diff: bool = False,
                  height: Optional[int] = None,
                  warn: bool = True) -> vs.VideoNode:
    """
    A simple wrapper that allows you to compare two clips by stacking them.
    You can stack an infinite amount of clips.

    Best to use when trying to match two sources frame-accurately, however by setting height to the source's
    height (or None), it can be used for comparing frames.

    Alias for this function is `lvsfunc.scomp`.

    :param clips:             Clips to compare
    :param make_diff:         Create and stack a diff (only works if two clips are given) (Default: False)
    :param height:            Output height, determined automatically if None (Default: None)
    :param warn:              Warns if the length of given clips don't align (Default: True)

    :return:                  Clip with clips stacked
    """
    if len(clips) < 2:
        raise ValueError(f"stack_compare: 'Too few clips supplied'")

    if len(clips) != 2 and make_diff:
        raise ValueError(f"stack_compare: 'You can only create a diff for two clips'")

    if len(set([c.format.id for c in clips])) != 1:
        raise ValueError(f"stack_compare: 'The format of every clip must be equal'")

    if make_diff:
        diff = core.std.MakeDiff(clips[0], clips[1])
        diff = core.resize.Spline36(diff, get_w(576), 576).text.FrameNum(8)
        resize = [core.resize.Spline36(c, diff.width / 2, diff.height / 2) for c in clips]
        resize[0], resize[1] = resize[0].text.Text("Clip A", 3), resize[1].text.Text("Clip B", 1)
        stack = core.std.StackVertical([core.std.StackHorizontal([resize[0], resize[1]]), diff])
    else:
        stack = core.std.StackHorizontal(clips)
    if warn:
        if len(set([c.num_frames for c in clips])) != 1:
            stack = core.text.Text(stack, f"Clip Length Mismatch Detected! \nPlease make sure the lengths of all clips match!\n"+"".join(f"\nClip {i+1}: {c.num_frames} Frames" for i, c in enumerate(clips)), 2)
    return stack


def stack_planes(clip: vs.VideoNode,
                 stack_vertical: bool = False) -> vs.VideoNode:
    """
    Stacks the planes of a clip.

    :param clip:              Input clip
    :param stack_vertical:    Stack the planes vertically (Default: False)

    :return:                  Clip with stacked planes
    """

    planes = split(clip)
    subsampling = get_subsampling(clip)

    if subsampling == '420':
        if stack_vertical:
            stack = core.std.StackHorizontal([planes[1], planes[2]])
            return core.std.StackVertical([planes[0], stack])
        else:
            stack = core.std.StackVertical([planes[1], planes[2]])
            return core.std.StackHorizontal([planes[0], stack])
    elif subsampling == '444':
        return core.std.StackVertical(planes) if stack_vertical else core.std.StackHorizontal(planes)
    else:
        raise ValueError(f"stack_planes: 'Input clip must be in YUV format with 444 or 420 chroma subsampling'")


def tvbd_diff(tv: vs.VideoNode, bd: vs.VideoNode,
              thr: float = 72,
              return_array: bool = False) -> vs.VideoNode:
    """
    Creates a standard `stack_compare` between frames from two clips that have differences.
    Useful for making comparisons between TV and BD encodes, as well as clean and hardsubbed sources.

    There are two methods used here to find differences.
    If thr is below 1, PlaneStatsDiff is used to figure out the differences.
    Else, if thr is equal than or higher than 1, PlaneStatsMin/Max are used.

    Recommended is PlaneStatsMin/Max, as those seem to catch
    more outrageous differences more easily and not return
    too many starved frames.

    Note that this might catch artifacting as differences!
    Make sure you verify every frame with your own eyes!

    Alias for this function is `lvsfunc.diff`.

    :param tv:            TV clip
    :param bd:            BD clip
    :param thr:           Threshold, <= 1 uses PlaneStatsDiff, >1 uses Max/Min. Max is 128 (Default: 72)
    :param return_array:  Return frames as an interleaved comparison (using py:func:`lvsfunc.comparison.compare`) (Default: False)
    """
    if thr > 128:
        raise ValueError(f"tvbd_diff: \"thr\" should neither be nor exceed 128!'")

    tv, bd = depth(tv, 8), depth(bd, 8)

    if thr <= 1:
        diff = core.std.PlaneStats(tv, bd)
        frames = [i for i, f in enumerate(diff.frames()) if f.props["PlaneStatsDiff"] > thr]
    else:
        diff = core.std.MakeDiff(tv, bd).std.PlaneStats()
        frames = [i for i, f in enumerate(diff.frames()) if f.props["PlaneStatsMin"] <= thr or f.props["PlaneStatsMax"] >= 255 - thr]

    if not frames:
        raise ValueError(f"tvbd_diff: 'No differences found'")

    if return_array:
        return compare(tv.text.FrameNum().text.Text('Clip A', 9),
                       bd.text.FrameNum().text.Text('Clip B', 9),
                       frames)
    else:
        if thr <= 1:
            diff = core.std.MakeDiff(tv, bd)
        diff = core.resize.Spline36(diff, get_w(576), 576).text.FrameNum(8)
        tv, bd = core.resize.Spline36(tv, diff.width / 2, diff.height / 2), core.resize.Spline36(bd, diff.width / 2, diff.height / 2)
        tv, bd = tv.text.Text("Clip A", 3), bd.text.Text("Clip B", 1)
        stacked = core.std.StackVertical([core.std.StackHorizontal([tv, bd]), diff])
        return core.std.Splice([stacked[f] for f in frames])


# TODO: Write a comparison function that displays parts of clips side-by-side, similar to a slider.
#       It should theoretically accept an infinite amount of clips
#       and accurately split the width among all clips.
#       Odd-resolution clips will also need to be taken into account.
