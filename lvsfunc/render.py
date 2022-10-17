from __future__ import annotations

from concurrent.futures import Future
from functools import partial
from threading import Condition
from typing import BinaryIO, Callable, TextIO

from vstools import InvalidColorFamilyError, core, get_prop, get_render_progress, vs

from .types import SceneChangeMode

RenderCallback = Callable[[int, vs.VideoFrame], None]


__all__ = [
    'clip_async_render',
    'find_scene_changes',
    'finish_frame',
    'RenderContext',
]


class RenderContext:
    """Contains info on the current render operation."""

    clip: vs.VideoNode
    queued: int
    frames: dict[int, vs.VideoFrame]
    frames_rendered: int
    timecodes: list[float]
    condition: Condition

    def __init__(self, clip: vs.VideoNode, queued: int) -> None:
        self.clip = clip
        self.queued = queued
        self.frames = {}
        self.frames_rendered = 0
        self.timecodes = [0.0]
        self.condition = Condition()


def finish_frame(outfile: BinaryIO | None, timecodes: TextIO | None, ctx: RenderContext) -> None:
    """
    Output a frame.

    :param outfile:   Output IO handle for Y4MPEG.
    :param timecodes: Output IO handle for timecodesv2.
    :param ctx:       Rendering context.
    """
    if timecodes:
        timecodes.write(f"{round(ctx.timecodes[ctx.frames_rendered]*1000):d}\n")
    if outfile is None:
        return

    f = ctx.frames[ctx.frames_rendered]

    outfile.write("FRAME\n".encode("utf-8"))

    f._writelines(outfile.write)


def clip_async_render(clip: vs.VideoNode,
                      outfile: BinaryIO | None = None,
                      timecodes: TextIO | None = None,
                      progress: str | None = "Rendering clip...",
                      callback: RenderCallback | list[RenderCallback] | None = None) -> list[float]:
    """
    Render a clip by requesting frames asynchronously using clip.get_frame_async.

    You must provide a callback with frame number and frame object.

    This is mostly a re-implementation of VideoNode.output, but a little bit slower since it's pure python.
    You only really need this when you want to render a clip while operating on each frame in order
    or you want timecodes without using vspipe.

    :param clip:                        Clip to render.
    :param outfile:                     Y4MPEG render output BinaryIO handle. If None, no Y4M output is performed.
                                        Use :py:func:`sys.stdout.buffer` for stdout. (Default: None)
    :param timecodes:                   Timecode v2 file TextIO handle. If None, timecodes will not be written.
    :param progress:                    String to use for render progress display.
                                        If empty or ``None``, no progress display.
    :param callback:                    Single or list of callbacks to be performed. The callbacks are called.
                                        when each sequential frame is output, not when each frame is done.
                                        Must have signature ``Callable[[int, vs.VideoNode], None]``
                                        See :py:func:`lvsfunc.comparison.diff` for a use case (Default: None).

    :return:                            List of timecodes from rendered clip.

    :raises ValueError:                 Variable format clip is passed.
    :raises InvalidColorFamilyError:    Non-YUV or GRAY clip is passed.
    :raises ValueError:                 "What have you done?"
    """
    cbl = [] if callback is None else callback if isinstance(callback, list) else [callback]

    if progress:
        p = get_render_progress()
        task = p.add_task(progress, total=clip.num_frames)

        def _progress_cb(n: int, f: vs.VideoFrame) -> None:
            p.update(task, advance=1)

        cbl.append(_progress_cb)

    ctx = RenderContext(clip, core.num_threads)

    bad_timecodes: bool = False

    def cb(f: Future[vs.VideoFrame], n: int) -> None:
        ctx.frames[n] = f.result()
        nn = ctx.queued

        while ctx.frames_rendered in ctx.frames:
            nonlocal timecodes
            nonlocal bad_timecodes

            frame = ctx.frames[ctx.frames_rendered]
            # if a frame is missing timing info, clear timecodes because they're worthless
            if ("_DurationNum" not in frame.props or "_DurationDen" not in frame.props) and not bad_timecodes:
                bad_timecodes = True
                if timecodes:
                    timecodes.seek(0)
                    timecodes.truncate()
                    timecodes = None
                ctx.timecodes = []
                print("clip_async_render: frame missing duration information, discarding timecodes")
            elif not bad_timecodes:
                ctx.timecodes.append(ctx.timecodes[-1]
                                     + get_prop(frame, "_DurationNum", int)
                                     / get_prop(frame, "_DurationDen", int))
            finish_frame(outfile, timecodes, ctx)
            [cb(ctx.frames_rendered, ctx.frames[ctx.frames_rendered]) for cb in cbl]
            del ctx.frames[ctx.frames_rendered]  # tfw no infinite memory
            ctx.frames_rendered += 1

        # enqueue a new frame
        if nn < clip.num_frames:
            ctx.queued += 1
            cbp = partial(cb, n=nn)
            clip.get_frame_async(nn).add_done_callback(cbp)  # type: ignore

        ctx.condition.acquire()
        ctx.condition.notify()
        ctx.condition.release()

    if outfile:
        if clip.format is None:
            raise ValueError("clip_async_render: 'Cannot render a variable format clip to y4m!'")

        InvalidColorFamilyError.check(
            clip, (vs.YUV, vs.GRAY), clip_async_render,
            message='Can only render to y4m clips with {correct} color family, not {wrong}!'
        )

        if clip.format.color_family == vs.GRAY:
            y4mformat = "mono"
        else:
            match (clip.format.subsampling_w, clip.format.subsampling_h):
                case (1, 1): y4mformat = "420"
                case (1, 0): y4mformat = "422"
                case (0, 0): y4mformat = "444"
                case (2, 2): y4mformat = "410"
                case (2, 0): y4mformat = "411"
                case (0, 1): y4mformat = "440"
                case _: raise ValueError("clip_async_render: 'What have you done?'")

        y4mformat = f"{y4mformat}p{clip.format.bits_per_sample}" if clip.format.bits_per_sample > 8 else y4mformat

        header = f"YUV4MPEG2 C{y4mformat} W{clip.width} H{clip.height} " \
            f"F{clip.fps.numerator}:{clip.fps.denominator} Ip A0:0\n"
        outfile.write(header.encode("utf-8"))

    if timecodes:
        timecodes.write("# timestamp format v2\n")

    ctx.condition.acquire()

    # seed threads
    if progress:
        p.start()
    try:
        for n in range(min(clip.num_frames, core.num_threads)):
            cbp = partial(cb, n=n)  # lambda won't bind the int immediately
            clip.get_frame_async(n).add_done_callback(cbp)  # type: ignore

        while ctx.frames_rendered != clip.num_frames:
            ctx.condition.wait()
    finally:
        if progress:
            p.stop()

    return ctx.timecodes  # might as well


def find_scene_changes(clip: vs.VideoNode, mode: SceneChangeMode = SceneChangeMode.WWXD) -> list[int]:
    """
    Generate a list of scene changes (keyframes).

    Dependencies:

    * `vapoursynth-wwxd <https://github.com/dubhater/vapoursynth-wwxd>`_
    * `vapoursynth-scxvid <https://github.com/dubhater/vapoursynth-scxvid>`_ (Optional: scxvid mode)

    :param clip:            Clip to search for scene changes. Will be rendered in its entirety.
    :param mode:            Scene change detection mode:.

                            * WWXD: Use wwxd
                            * SCXVID: Use scxvid
                            * WWXD_SCXVID_UNION: Union of wwxd and sxcvid (must be detected by at least one)
                            * WWXD_SCXVID_INTERSECTION: Intersection of wwxd and scxvid (must be detected by both)

    :return:                List of scene changes.

    :raises ValueError:     Invalid ``mode`` gets passed.
    """
    frames = []
    clip = clip.resize.Bilinear(640, 360, format=vs.YUV420P8)

    if mode in (SceneChangeMode.WWXD, SceneChangeMode.WWXD_SCXVID_UNION, SceneChangeMode.WWXD_SCXVID_INTERSECTION):
        clip = clip.wwxd.WWXD()
    if mode in (SceneChangeMode.SCXVID, SceneChangeMode.WWXD_SCXVID_UNION, SceneChangeMode.WWXD_SCXVID_INTERSECTION):
        clip = clip.scxvid.Scxvid()

    def _cb(n: int, f: vs.VideoFrame) -> None:
        match mode:
            case SceneChangeMode.WWXD:
                if get_prop(f, "Scenechange", int) == 1:
                    frames.append(n)
            case SceneChangeMode.SCXVID:
                if get_prop(f, "Scenechange", int) == 1:
                    frames.append(n)
            case SceneChangeMode.WWXD_SCXVID_UNION:
                if get_prop(f, "Scenechange", int) == 1 or get_prop(f, "_SceneChangePrev", int) == 1:
                    frames.append(n)
            case SceneChangeMode.WWXD_SCXVID_INTERSECTION:
                if get_prop(f, "Scenechange", int) == 1 and get_prop(f, "_SceneChangePrev", int) == 1:
                    frames.append(n)
            case _: raise ValueError("find_scene_changes: 'Invalid `mode` passed!'")

    clip_async_render(clip, progress="Detecting scene changes...", callback=_cb)

    return sorted(frames)
