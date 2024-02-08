from pathlib import Path
from typing import Callable

from stgpytools import (CustomValueError, DependencyNotFoundError,
                        FileWasNotFoundError, SPath, SPathLike)
from vssource import source
from vstools import Keyframes, core, get_prop, replace_ranges, vs

__all__: list[str] = [
    "splice_ncs"
]


def splice_nc(
    clip: vs.VideoNode, nc: SPathLike | vs.VideoNode | None,
    episode_kf: Keyframes | SPathLike | None = None,
    source_func: Callable[[vs.VideoNode], vs.VideoNode] = source,  # type:ignore[assignment]
) -> vs.VideoNode:
    """
    Helper to splice an episode's NCs into the episode.

    This function will try to automatically match keyframes to splice the NC in the right places.
    To do this, it requires a list of scene changes. If the user does not pass a Keyframes object
    or a path to a keyframe file, it will generate them on the spot.

    This function requires the following plugins:

        * VapourSynth-VMAF `<https://github.com/HomeOfVapourSynthEvolution/VapourSynth-VMAF>

    :param clip:            Clip to splice the NC into.
    :param nc:              The NC, either as an SPathLike or a VideoNode to allow for pre-processing.
                            None is a no-op intended to faciliate for-looping. Default: None.
    :param episode_kf:      Optional Keyframes object of the episode, or an SPathLike pointing to a keyframe file.
                            If None, will generate Keyframes. These are used to help find frame ranges.
                            Default: None.
    :param source_func:     The source function to index the NCs. Default: `vssource.source`.

    :return:                Clip with NCs spliced in.
    """

    if nc is None:
        return clip

    import warnings
    warnings.warn("lvsfunc.splice_nc: This function is still experimental! Please be careful when using it!")

    if not hasattr(core, "vmaf"):
        raise DependencyNotFoundError(
            splice_nc, "VapourSynth-VMAF `<https://github.com/HomeOfVapourSynthEvolution/VapourSynth-VMAF>`_"
        )

    if isinstance(nc, (str, Path, SPath)):
        nc_clip = source_func(SPath(nc))  # type:ignore[arg-type]
    elif isinstance(nc, vs.VideoNode):
        nc_clip = nc
    else:
        raise CustomValueError(f"\"nc\" must be an \"SPathLike\" or \"VideoNode\", not \"{type(nc)}\"", splice_nc)

    ep_kf = _get_keyframes(clip, episode_kf)
    nc_kf = _get_keyframes(nc_clip)

    first, last = _get_start_end_frames(ep_kf, nc_kf, clip, nc_clip)

    if first > 0:
        nc_clip = nc_clip.std.BlankClip(length=first - 1) + nc_clip

    return replace_ranges(clip, nc_clip, [(first, last)])


def _get_keyframes(clip: vs.VideoNode, kf: Keyframes | SPathLike | None = None) -> Keyframes:
    if isinstance(kf, Keyframes):
        return kf

    if isinstance(kf, (str, Path, SPath)) and not (kf_path := SPath(kf)).exists():
        raise FileWasNotFoundError(f"Could not find the keyframes file, \"{kf_path}\"!", splice_nc)
    elif kf is None:
        # ! TODO: figure out how to get a unique identifier that persists across runs
        from uuid import uuid4  # replace this ASAP :(
        kf_path = SPath(f"_keyframes/nc_{uuid4()}.txt")

    if not kf_path.exists():
        kf_read = Keyframes(Keyframes.from_clip(clip))
        kf_read.append(clip.num_frames - 1)
        kf_read.to_file(kf_path)

    return Keyframes.from_file(kf_path)


def _get_start_end_frames(ep_kf: Keyframes, nc_kf: Keyframes, clip: vs.VideoNode, nc_clip: vs.VideoNode) -> Keyframes:
    # TODO: double-check this logic

    # TODO: Add proper keyframe matching + extra verification heuristics
    # (since kfs can just not line up because credits sometimes)

    first_frame = nc_clip[0]
    last_frame = nc_clip[-1]

    first_res = dict[int, float]()
    last_res = dict[int, float]()

    for frame in ep_kf:
        first_res |= {frame: get_prop(clip[frame].vmaf.Metric(first_frame, 2), "float_ssim", float, func=splice_nc)}

    first_res = dict(sorted(first_res.items(), key=lambda item: item[1], reverse=True))
    first = list(first_res.keys())[0]

    for frame in [k - 1 for k in ep_kf if k > first and k <= (first + nc_clip.num_frames + 72)]:
        last_res |= {frame: get_prop(clip[frame].vmaf.Metric(last_frame, 2), "float_ssim", float, func=splice_nc)}

    last_res = dict(sorted(last_res.items(), key=lambda item: item[1], reverse=True))

    try:
        last = list(last_res.keys())[0]
    except IndexError:
        last = first + nc_clip.num_frames

    return Keyframes([first, last])
