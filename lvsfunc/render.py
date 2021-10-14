"""
Node rendering helpers.
"""
import struct
from abc import ABC
from concurrent.futures import Future
from enum import Enum, IntEnum
from functools import partial
from threading import Condition
from typing import (BinaryIO, Callable, Dict, Generic, List, Optional, TextIO,
                    TypeVar, Union)

import numpy as np
import vapoursynth as vs

from .progress import (BarColumn, FPSColumn, Progress, TextColumn,
                       TimeRemainingColumn)
from .util import get_prop

core = vs.core

RenderCallback = Callable[[int, vs.VideoFrame], None]
Node = TypeVar('Node', bound=Union[vs.VideoNode, vs.AudioNode])
Frame = TypeVar('Frame', bound=Union[vs.VideoFrame, vs.AudioFrame])


class RenderContext(Generic[Node, Frame], ABC):
    """
    Contains info on the current render operation.
    """
    node: Node
    queued: int
    frames: Dict[int, Frame]
    frames_rendered: int
    condition: Condition

    def __init__(self, node: Node, queued: int) -> None:
        self.node = node
        self.queued = queued
        self.frames = {}
        self.frames_rendered = 0
        self.condition = Condition()


class RenderContextVideo(RenderContext[vs.VideoNode, vs.VideoFrame]):
    """
    Contains info on the current render operation for video.
    """
    timecodes: List[float]

    def __init__(self, node: vs.VideoNode, queued: int) -> None:
        self.timecodes = [0.0]
        super().__init__(node, queued)


class RenderContextAudio(RenderContext[vs.AudioNode, vs.AudioFrame]):
    """
    Contains info on the current render operation for audio.
    """
    ...


def finish_frame_video(outfile: Optional[BinaryIO], timecodes: Optional[TextIO], ctx: RenderContextVideo) -> None:
    """
    Output a video frame.

    :param outfile:   Output IO handle for Y4MPEG
    :param timecodes: Output IO handle for timecodesv2
    :param ctx:       Rendering context
    """
    if timecodes:
        timecodes.write(f"{round(ctx.timecodes[ctx.frames_rendered]*1000):d}\n")
    if outfile is None:
        return

    f: vs.VideoFrame = ctx.frames[ctx.frames_rendered]

    outfile.write("FRAME\n".encode("utf-8"))

    for i, p in enumerate(f.planes()):
        if f.get_stride(i) != p.width * f.format.bytes_per_sample:
            outfile.write(bytes(p))  # type: ignore
        else:
            outfile.write(p)  # type: ignore


def finish_frame_audio(outfile: BinaryIO, ctx: RenderContextAudio, _24bit: bool = False) -> None:
    """
    Output an audio frame.

    :param outfile: Output IO handle for WAVE or WAVE64
    :param ctx:     Rendering context
    :param _24bit:  If bitdepth is 24.
    """
    f = ctx.frames[ctx.frames_rendered]

    # For some reason f[i] is faster than list(f) or just passing f to stack
    data = np.stack([f[i] for i in range(f.num_channels)], axis=1)

    if _24bit:
        if data.ndim == 1:
            # Convert to a 2D array with a single column
            data.shape += (1, )
        # Data values are stored in 32 bits so we must convert them to 24 bits
        # Then by shifting first 0 bits, then 8, then 16, the resulting output is 24 bit little-endian.
        data = ((data // 2 ** 8).reshape(data.shape + (1, )) >> np.array([0, 8, 16]))
        outfile.write(data.ravel().astype(np.uint8).tobytes())
    else:
        outfile.write(data.ravel().view(np.int8).tobytes())


def clip_async_render(clip: vs.VideoNode,
                      outfile: Optional[BinaryIO] = None,
                      timecodes: Optional[TextIO] = None,
                      progress: Optional[str] = "Rendering clip...",
                      callback: Union[RenderCallback, List[RenderCallback], None] = None) -> List[float]:
    """
    Render a clip by requesting frames asynchronously using clip.get_frame_async,
    providing for callback with frame number and frame object.

    This is mostly a re-implementation of VideoNode.output, but a little bit slower since it's pure python.
    You only really need this when you want to render a clip while operating on each frame in order
    or you want timecodes without using vspipe.

    :param clip:      Clip to render.
    :param outfile:   Y4MPEG render output BinaryIO handle. If None, no Y4M output is performed.
                      Use ``sys.stdout.buffer`` for stdout. (Default: None)
    :param timecodes: Timecode v2 file TextIO handle. If None, timecodes will not be written.
    :param progress:  String to use for render progress display.
                      If empty or ``None``, no progress display.
    :param callback:  Single or list of callbacks to be preformed. The callbacks are called
                      when each sequential frame is output, not when each frame is done.
                      Must have signature ``Callable[[int, vs.VideoNode], None]``
                      See :py:func:`lvsfunc.comparison.diff` for a use case (Default: None).

    :return:          List of timecodes from rendered clip.
    """
    cbl = [] if callback is None else callback if isinstance(callback, list) else [callback]

    if progress:
        p = get_render_progress()
        task = p.add_task(progress, total=clip.num_frames)

        def _progress_cb(n: int, f: vs.VideoFrame) -> None:
            p.update(task, advance=1)

        cbl.append(_progress_cb)

    ctx = RenderContextVideo(clip, core.num_threads)

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
            finish_frame_video(outfile, timecodes, ctx)
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
        if clip.format.color_family not in (vs.YUV, vs.GRAY):
            raise ValueError("clip_async_render: 'Can only render YUV and GRAY clips to y4m!'")
        if clip.format.color_family == vs.GRAY:
            y4mformat = "mono"
        else:
            ss = (clip.format.subsampling_w, clip.format.subsampling_h)
            if ss == (1, 1):
                y4mformat = "420"
            elif ss == (1, 0):
                y4mformat = "422"
            elif ss == (0, 0):
                y4mformat = "444"
            elif ss == (2, 2):
                y4mformat = "410"
            elif ss == (2, 0):
                y4mformat = "411"
            elif ss == (0, 1):
                y4mformat = "440"
            else:
                raise ValueError("clip_async_render: 'What have you done'")

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


class WaveFormat(IntEnum):
    """
    WAVE form wFormatTag IDs
    Complete list is in mmreg.h in Windows 10 SDK.
    """
    PCM = 0x0001
    IEEE_FLOAT = 0x0003
    EXTENSIBLE = 0xFFFE


class WaveHeader(IntEnum):
    """
    Wave headers
    """
    WAVE = 0
    WAVE64 = 1
    AUTO = 2


WAVE_RIFF_TAG = b'RIFF'
WAVE_WAVE_TAG = b'WAVE'
WAVE_FMT_TAG = b'fmt '
WAVE_DATA_TAG = b'data'

WAVE64_RIFF_UUID = (0x72, 0x69, 0x66, 0x66, 0x2E, 0x91, 0xCF, 0x11, 0xA5, 0xD6, 0x28, 0xDB, 0x04, 0xC1, 0x00, 0x00)
WAVE64_WAVE_UUID = (0x77, 0x61, 0x76, 0x65, 0xF3, 0xAC, 0xD3, 0x11, 0x8C, 0xD1, 0x00, 0xC0, 0x4F, 0x8E, 0xDB, 0x8A)
WAVE64_FMT_UUID = (0x66, 0x6D, 0x74, 0x20, 0xF3, 0xAC, 0xD3, 0x11, 0x8C, 0xD1, 0x00, 0xC0, 0x4F, 0x8E, 0xDB, 0x8A)
WAVE64_DATA_UUID = (0x64, 0x61, 0x74, 0x61, 0xF3, 0xAC, 0xD3, 0x11, 0x8C, 0xD1, 0x00, 0xC0, 0x4F, 0x8E, 0xDB, 0x8A)
WAVE_FMT_EXTENSIBLE_SUBFORMAT = (
    (WaveFormat.PCM, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x80, 0x00, 0x00, 0xAA, 0x00, 0x38, 0x9B, 0x71),
    (WaveFormat.IEEE_FLOAT, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x80, 0x00, 0x00, 0xAA, 0x00, 0x38, 0x9B, 0x71)
)


def audio_async_render(audio: vs.AudioNode,
                       outfile: BinaryIO,
                       header: WaveHeader = WaveHeader.AUTO,
                       progress: Optional[str] = "Rendering audio...") -> None:
    """
    Render an audio by requesting frames asynchronously using audio.get_frame_async.

    Implementation-like of VideoNode.output for an AudioNode that isn't in the Cython side yet.

    :param audio:       Audio to render.
    :param outfile:     Render output BinaryIO handle.
    :param header:      Kind of Wave header.
                        WaveHeader.AUTO adds a Wave64 header if the audio

                        * Has more than 2 channels
                        * Has a bitdepth > 16
                        * Has more than 44100 samples

    :param progress:    String to use for render progress display.
                        If empty or ``None``, no progress display.
    """
    if progress:
        p = get_render_progress()
        task = p.add_task(progress, total=audio.num_frames)

    ctx = RenderContextAudio(audio, core.num_threads)

    def cb(f: Future[vs.AudioFrame], n: int) -> None:
        ctx.frames[n] = f.result()
        nn = ctx.queued

        while ctx.frames_rendered in ctx.frames:
            finish_frame_audio(outfile, ctx, audio.bits_per_sample == 24)

            if progress:
                p.update(task, advance=1)

            del ctx.frames[ctx.frames_rendered]  # tfw no infinite memory
            ctx.frames_rendered += 1

        # enqueue a new frame
        if nn < audio.num_frames:
            ctx.queued += 1
            cbp = partial(cb, n=nn)
            audio.get_frame_async(nn).add_done_callback(cbp)  # type: ignore

        ctx.condition.acquire()
        ctx.condition.notify()
        ctx.condition.release()

    bytes_per_output_sample = (audio.bits_per_sample + 7) // 8
    block_align = audio.num_channels * bytes_per_output_sample
    bytes_per_second = audio.sample_rate * block_align
    data_size = audio.num_samples * block_align

    if header == WaveHeader.AUTO:
        conditions = (audio.num_channels > 2, audio.bits_per_sample > 16, audio.num_samples > 44100)
        header_func, use_w64 = (_w64_header, 1) if any(conditions) else (_wav_header, 0)
    else:
        use_w64 = int(header)
        header_func = (_wav_header, _w64_header)[header]

    outfile.write(header_func(audio, bytes_per_second, block_align, data_size))

    ctx.condition.acquire()

    # seed threads
    if progress:
        p.start()
    try:
        for n in range(min(audio.num_frames, core.num_threads)):
            cbp = partial(cb, n=n)  # lambda won't bind the int immediately
            audio.get_frame_async(n).add_done_callback(cbp)  # type: ignore

        while ctx.frames_rendered != audio.num_frames:
            ctx.condition.wait()
    finally:
        # Determine file size and place the value at the correct position
        # at the beginning of the file
        size = outfile.tell()
        if use_w64:
            outfile.seek(16)
            outfile.write(struct.pack('<Q', size))
        else:
            outfile.seek(4)
            outfile.write(struct.pack('<I', size - 8))
        if progress:
            p.stop()


def _wav_header(audio: vs.AudioNode, bps: int, block_align: int, data_size: int) -> bytes:
    header = WAVE_RIFF_TAG
    # Add 4 bytes for the length later
    header += b'\x00\x00\x00\x00'
    header += WAVE_WAVE_TAG

    header += WAVE_FMT_TAG
    format_tag = WaveFormat.IEEE_FLOAT if audio.sample_type == vs.FLOAT else WaveFormat.PCM

    fmt_chunk_data = struct.pack(
        '<HHIIHH', format_tag, audio.num_channels, audio.sample_rate,
        bps, block_align, audio.bits_per_sample
    )
    header += struct.pack('<I', len(fmt_chunk_data))
    header += fmt_chunk_data

    if len(header) + data_size > 0xFFFFFFFE:
        raise ValueError('Data exceeds wave file size limit')

    header += WAVE_DATA_TAG
    header += struct.pack('<I', data_size)
    return header


def _w64_header(audio: vs.AudioNode, bps: int, block_align: int, data_size: int) -> bytes:
    # RIFF-GUID
    header = bytes(WAVE64_RIFF_UUID)
    # Add 8 bytes for the length later
    header += b'\x00\x00\x00\x00\x00\x00\x00\x00'
    # WAVE-GUID
    header += bytes(WAVE64_WAVE_UUID)
    # FMT-GUID
    fmt_guid = bytes(WAVE64_FMT_UUID)
    header += fmt_guid

    # We only support WAVEFORMATEXTENSIBLE for WAVE64 header
    format_tag = WaveFormat.EXTENSIBLE

    # cb_size should be 22 for WAVEFORMATEXTENSIBLE with PCM
    cb_size = 22
    fmt_chunk_data = struct.pack(
        '<HHIIHHHHI', format_tag, audio.num_channels, audio.sample_rate,
        bps, block_align, audio.bits_per_sample, cb_size,
        audio.bits_per_sample,  # valid bit per sample
        audio.channel_layout
    )
    # Add the subformat GUID, first 2 bytes have format type, 1 being PCM
    fmt_chunk_data += bytes(WAVE_FMT_EXTENSIBLE_SUBFORMAT[audio.sample_type])

    # Add the FMT size
    # Length of the FMT-GUID + length of FMT data and 8 for the bytes themself
    header += struct.pack('<Q', len(fmt_guid) + 8 + len(fmt_chunk_data))
    header += fmt_chunk_data

    # # Finally write the header
    # outfile.write(header)

    # DATA-GUID
    data_uuid = bytes(WAVE64_DATA_UUID)
    header += data_uuid
    header += struct.pack('<Q', data_size + len(data_uuid) + 8)
    return header


def get_render_progress() -> Progress:
    return Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TextColumn("{task.percentage:>3.02f}%"),
        FPSColumn(),
        TimeRemainingColumn(),
    )


class SceneChangeMode(Enum):
    WWXD = 0
    SCXVID = 1
    WWXD_SCXVID_UNION = 2
    WWXD_SCXVID_INTERSECTION = 3


def find_scene_changes(clip: vs.VideoNode, mode: SceneChangeMode = SceneChangeMode.WWXD) -> List[int]:
    """
    Generate a list of scene changes (keyframes).

    Dependencies:

    * vapoursynth-wwxd
    * vapoursynth-scxvid (Optional: scxvid mode)

    :param clip:   Clip to search for scene changes. Will be rendered in its entirety.
    :param mode:   Scene change detection mode:

                   * WWXD: Use wwxd
                   * SCXVID: Use scxvid
                   * WWXD_SCXVID_UNION: Union of wwxd and sxcvid (must be detected by at least one)
                   * WWXD_SCXVID_INTERSECTION: Intersection of wwxd and scxvid (must be detected by both)

    :return:       List of scene changes.
    """
    frames = []
    clip = clip.resize.Bilinear(640, 360, format=vs.YUV420P8)

    if mode in (SceneChangeMode.WWXD, SceneChangeMode.WWXD_SCXVID_UNION, SceneChangeMode.WWXD_SCXVID_INTERSECTION):
        clip = clip.wwxd.WWXD()
    if mode in (SceneChangeMode.SCXVID, SceneChangeMode.WWXD_SCXVID_UNION, SceneChangeMode.WWXD_SCXVID_INTERSECTION):
        clip = clip.scxvid.Scxvid()

    def _cb(n: int, f: vs.VideoFrame) -> None:
        if mode == SceneChangeMode.WWXD:
            if get_prop(f, "Scenechange", int) == 1:
                frames.append(n)
        elif mode == SceneChangeMode.SCXVID:
            if get_prop(f, "_SceneChangePrev", int) == 1:
                frames.append(n)
        elif mode == SceneChangeMode.WWXD_SCXVID_UNION:
            if get_prop(f, "Scenechange", int) == 1 or get_prop(f, "_SceneChangePrev", int) == 1:
                frames.append(n)
        elif mode == SceneChangeMode.WWXD_SCXVID_INTERSECTION:
            if get_prop(f, "Scenechange", int) == 1 and get_prop(f, "_SceneChangePrev", int) == 1:
                frames.append(n)

    clip_async_render(clip, progress="Detecting scene changes...", callback=_cb)

    return sorted(frames)
