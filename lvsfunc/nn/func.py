import warnings

import numpy as np
from vsexprtools import norm_expr
from vstools import (CustomValueError, FuncExceptT, FunctionUtil, SPath,
                     SPathLike, clip_async_render, core, fallback, get_depth,
                     initialize_clip, vs)

from .util import get_format_from_npy

__all__: list[str] = [
    'prepare_clip_for_npy', 'finalize_clip_from_npy',
    'clip_to_npy', 'npy_to_clip',
]


def prepare_clip_for_npy(clip: vs.VideoNode, func_except: FuncExceptT | None = None) -> vs.VideoNode:
    """
    Prepare a clip for exporting to numpy files.

    This involves dithering up to 32-bit float and normalizing the UV ranges to [0, 1] if present.
    This should be used before exporting frames to numpy files.

    :param clip:            The input video clip to process.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                The processed clip.
    """

    return _process_clip_for_npy(clip, fallback(func_except, prepare_clip_for_npy), 'prepare')


def finalize_clip_from_npy(clip: vs.VideoNode, func_except: FuncExceptT | None = None) -> vs.VideoNode:
    """
    Finalize a clip obtained from numpy files.

    This involves denormalizing the UV ranges to the original range if present.
    This should be used after loading frames from numpy files.

    :param clip:            The input video clip to process.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                The processed clip.
    """

    return _process_clip_for_npy(clip, fallback(func_except, finalize_clip_from_npy), 'finalize')


def _process_clip_for_npy(clip: vs.VideoNode, func_except: FuncExceptT | None, operation: str) -> vs.VideoNode:
    func = FunctionUtil(clip, fallback(func_except, _process_clip_for_npy), None, (vs.GRAY, vs.YUV), 32)

    if not func.chroma_planes:
        return func.work_clip

    return norm_expr(func.work_clip, 'x 0.5 +' if operation == 'prepare' else 'x 0.5 -', func.chroma_planes)


def clip_to_npy(src: vs.VideoNode, out_dir: SPathLike = 'bin/') -> list[SPath]:
    """
    Export frames from a VideoNode to numpy array files.

    This function is intended to be used to help with preparing training data for neural networks.

    The function will not overwrite existing files,
    and instead increments the next filename by 1.

    :param src:                         The input video clip.
    :param out_dir:                     The directory to save the numpy arrays.
                                        Default: "bin/".

    :return:                            A list of paths to the exported numpy arrays.

    :raises RuntimeWarning:             If any frames failed to process.
    """

    func = FunctionUtil(src, clip_to_npy, None, vs.YUV)

    proc_clip = func.work_clip

    out_dir = SPath(out_dir)
    out_dir.mkdir(511, True, True)

    next_name = max((int(f.stem) for f in out_dir.glob('*.npy')), default=0) + 1

    if not (total_frames := len(proc_clip)):
        return []

    try:
        from tqdm import tqdm
        pbar = tqdm(total=total_frames, unit='frame', desc=f'Dumping numpy arrays to {out_dir}...')
    except ImportError:
        pbar = None

    def _update_progress(filename: str | None = None):
        if not pbar:
            return

        pbar.update(1)

        if filename:
            pbar.set_postfix({'Current file': filename}, refresh=True)

    exported_files = []

    def _process_frame(n: int, frame: vs.VideoFrame):
        nonlocal next_name

        try:
            frame_data = np.array([(
                np.asarray(frame[0]),
                np.asarray(frame[1]) if frame.format.num_planes > 1 else None,
                np.asarray(frame[2]) if frame.format.num_planes > 1 else None
            )], dtype=[('Y', object), ('U', object), ('V', object)])

            filename = f'{next_name:05d}.npy'
            file_path = out_dir / filename

            np.save(file_path, frame_data, allow_pickle=False)

            next_name += 1

            _update_progress(filename)

            exported_files.append(file_path)

            return filename
        except Exception as e:
            print(f'Error processing frame {n} ({str(e)})')

            _update_progress()

            return None

    proc_frames = clip_async_render(proc_clip, callback=_process_frame)

    if pbar:
        pbar.close()

    if failed_frames := [f for f in proc_frames if f is None]:
        warnings.warn(
            f'export_frames_to_npy: {len(failed_frames)} frames failed to process ({failed_frames}).',
            RuntimeWarning
        )

    return exported_files


def npy_to_clip(
    file_paths: list[SPathLike] | SPathLike = [],
    ref: vs.VideoNode | None = None,
    func_except: FuncExceptT | None = None
) -> vs.VideoNode:
    """
    Read numpy files and convert them to a VapourSynth clip.

    :param file_paths:      The list of numpy files to convert to a clip.
                            If a directory is provided, all .npy files in the directory will be used.
                            If a single file is provided, it will be used instead.
    :param ref:             A reference video clip to get props from.
                            If None, props will be guessed.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                The clip.
    """

    func = fallback(func_except, npy_to_clip)

    if not isinstance(file_paths, list):
        file_paths = SPath(file_paths)

        if file_paths.is_dir():
            file_paths = list(file_paths.glob("*.npy"))
        else:
            file_paths = [file_paths]

    if not file_paths:
        raise CustomValueError("No files provided", func)

    file_paths = sorted(file_paths, key=lambda x: int(x.stem))

    first_frame = np.load(file_paths[0], allow_pickle=False)[0]
    height, width = first_frame['Y'].shape

    fmt = get_format_from_npy(first_frame)

    blank_clip = core.std.BlankClip(None, width, height, fmt, length=len(file_paths), keep=True)

    def _read_frame(n: int, f: vs.VideoFrame) -> vs.VideoNode:
        loaded_frame = np.load(file_paths[n], allow_pickle=False)[0]

        fout = f.copy()

        for plane in range(f.format.num_planes):
            plane_data = loaded_frame[f.format.name[plane]]
            np.copyto(np.asarray(fout[plane]), plane_data)

        return fout

    proc_clip = blank_clip.std.ModifyFrame(blank_clip, _read_frame)

    if ref is not None:
        return initialize_clip(proc_clip, ref)

    return initialize_clip(proc_clip, get_depth(proc_clip), func=func)
