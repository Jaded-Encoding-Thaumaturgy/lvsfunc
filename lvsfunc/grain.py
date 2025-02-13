from vstools import (Keyframes, MismatchRefError, SceneAverageStats,
                     find_prop_rfs, get_script_path, merge_clip_props, vs)

__all__: list[str] = [
    'dynamic_scene_adaptive_grain'
]


def dynamic_scene_adaptive_grain(
    clip: vs.VideoNode,
    grain_dark: vs.VideoNode,
    grain_bright: vs.VideoNode,
    keyframes: Keyframes | None = None,
    thr: float = 0.55,
    key: str = "Grain",
) -> vs.VideoNode:
    """
    Dynamically swap between grained clips depending on the average luminosity of the scene.

    This function may help reduce overall filesize by applying a weaker grained clip on brighter scenes,
    which should hopefully reduce the amount of graining applied on the clip overall.
    As such, it's recommended you use dynamic grain on darker scenes, and static on brighter ones with this function.

    Threshold must be between 0 and 1. If it's not, it will simply return the appropriate clip.
    The returned clip will have the props, so you can use this to further tweak it.

    This function is intended for graining, but it can theoretically be used for other purposes.

    :param clip:            The clip used for metric gathering. It will be used for both keyframe generation
                            (if no keyframes are passed) as well as collecting scene averages.
    :param grain_dark:      The clip with graining applied for dark scenes.
    :param grain_bright:    The clip with graining applied for bright scenes.
    :param keyframes:       A keyframes object. This is used to pick frames to get the stats from.
                            If None is passed, it will generate keyframes for you using `clip`.
                            Default: None.
    :param thr:             Threshold used to decide which grained clip to pick.
                            Lower values will result in more scenes being replaced with `grain_bright`,
                            and vice versa for `grain_dark`. Default: 0.55.
    :param key:             The key for the property. Automatically capitalized. Default: "Grain".

    :return:                Clip with different types of graining applied based on the scene's luminosity.
    """

    MismatchRefError.check(dynamic_scene_adaptive_grain, grain_dark, grain_bright)

    if thr <= 0:
        return grain_dark
    if thr >= 1:
        return grain_bright

    keyframes = keyframes or Keyframes.unique(clip, get_script_path().stem)

    key = key.capitalize()

    sas = SceneAverageStats.from_clip(clip, keyframes, f"SceneStats{key}")

    grain = find_prop_rfs(
        grain_dark.std.SetFrameProps(SceneGrain="dark"),
        grain_bright.std.SetFrameProps(SceneGrain="bright"),
        f"SceneStats{key}Average", ">=", thr, sas
    )

    return merge_clip_props(grain, sas)
