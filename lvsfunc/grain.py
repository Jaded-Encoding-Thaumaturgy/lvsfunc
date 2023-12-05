from tempfile import NamedTemporaryFile
from warnings import warn

from stgpytools import CustomImportError, DependencyNotFoundError, MismatchRefError, SPath
from vstools import Keyframes, find_prop_rfs, merge_clip_props, vs


__all__: list[str] = [
    "dynamic_scene_adaptive_grain"
]


def dynamic_scene_adaptive_grain(
    grain_dark: vs.VideoNode,
    grain_bright: vs.VideoNode,
    ref: vs.VideoNode | None = None,
    keyframes: Keyframes | None = None,
    thr: float = 0.55,
) -> vs.VideoNode:
    """
    Dynamically swap between grained clips depending on the average luminosity of the scene.

    This function may help reduce overall filesize by applying a weaker grained clip on brighter scenes,
    which should hopefully reduce the amount of graining applied on the clip overall.
    As such, it's recommended you use dynamic grain on darker scenes, and static on brighter ones with this function.

    Threshold must be between 0 and 1. If it's not, it will simply return the appropriate clip.
    The returned clip will have the props, so you can use this to further tweak it.

    This function is intended for graining, but it can theoretically be used for other purposes.

    :param grain_dark:      The clip with graining applied for dark scenes.
    :param grain_bright:    The clip with graining applied for bright scenes.
    :param ref:             An optional reference clip. It's highly advised you pass one, as this clip will be used
                            for keyframe generation if necessary, as well as for collecting scene averages.
                            If None, it will use `grain_bright` as a ref clip. Default: None
    :param keyframes:       A keyframes object. This is used to pick frames to get the stats from.
                            If None is passed, it will create a temporary file in the TEMPDIR
                            and generate keyframes using the `ref` clip.
                            Default: None.
    :param thr:             Threshold used to decide which clip to pick.
                            Lower values will result in more scenes being replaced with `grain_bright`,
                            and vice versa for `grain_dark`. Default: 0.55.

    :return:                Clip with different types of graining applied based on the scene's luminosity.
    """
    try:
        from stgfunc import SceneAverageStats
    except ModuleNotFoundError:
        raise DependencyNotFoundError(dynamic_scene_adaptive_grain, "stgfunc")
    except ImportError:
        raise CustomImportError(dynamic_scene_adaptive_grain, "stgfunc")

    MismatchRefError.check(dynamic_scene_adaptive_grain, grain_dark, grain_bright)

    if thr <= 0:
        return grain_dark
    elif thr >= 1:
        return grain_bright

    if ref is None:
        warn("dynamic_scene_adaptive_grain: \"It's highly advised you pass a ref clip!\"")

        ref = grain_bright

    if keyframes is None:
        with NamedTemporaryFile(delete=False) as tmp:
            tmp_file = SPath(tmp.name)

        if tmp_file.exists():
            keyframes = Keyframes.from_file(tmp_file)
        else:
            keyframes = Keyframes.from_clip(ref)

    ref = SceneAverageStats(ref, keyframes, "SceneStatsGrain")

    grain = find_prop_rfs(
        grain_dark.std.SetFrameProps(SceneGrain="dark"),
        grain_bright.std.SetFrameProps(SceneGrain="bright"),
        "SceneStatsGrainAverage", ">=", thr, ref
    )

    return merge_clip_props(grain, ref)
