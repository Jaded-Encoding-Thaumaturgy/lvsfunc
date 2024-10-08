import warnings

import numpy as np
from vsexprtools import norm_expr
from vskernels import Kernel, KernelT, Point
from vstools import (CustomValueError, FileWasNotFoundError, FuncExceptT,
                     FunctionUtil, SPath, SPathLike, clip_async_render, core,
                     fallback, vs)

from ..exceptions import NumpyArrayLoadError
from .util import get_format_from_npy

__all__: list[str] = [
    'clip_to_npy', 'npy_to_clip',
]


def clip_to_npy(
    src: vs.VideoNode, out_dir: SPathLike = 'bin/',
    export_npz: bool = False,
    kernel: KernelT = Point,
    func_except: FuncExceptT | None = None
) -> list[SPath]:
    """
    Export frames from a VideoNode to numpy array files.

    This function is intended to be used to help with preparing training data for neural networks.

    This works by upsampling the given clip to YUV444PS (unless GRAY is given) using the given kernel.

    The function will not overwrite existing files,
    and instead increments the next filename by 1.

    :param src:                         The input video clip.
    :param out_dir:                     The directory to save the numpy arrays.
                                        Default: "bin/".
    :param export_npz:                  If True, export the numpy arrays as a single .npz file.
                                        Default: False.
    :param kernel:                      Kernel used for resampling if not YUV 444 or GRAY.
                                        Defaults to Point, as that can be up-and-downscaled without loss.
    :param func_except:                 Function returned for custom error handling.
                                        This should only be set by VS package developers.

    :return:                            A list of paths to the exported numpy arrays or the path to the .npz file.

    :raises RuntimeWarning:             If any frames failed to process.
    """

    func = FunctionUtil(src, func_except or clip_to_npy, None, (vs.GRAY, vs.YUV), 32)

    kernel = Kernel.ensure_obj(kernel, func.func)

    proc_clip = kernel.resample(func.work_clip, vs.YUV444PS) if func.work_clip.format.color_family == vs.YUV else func.work_clip
    proc_clip = norm_expr(proc_clip, 'x 0.5 +', func.chroma_pplanes)

    out_dir = SPath(out_dir)
    out_dir.mkdir(511, True, True)

    next_name = max((int(f.stem) for f in out_dir.glob('*.npy')), default=0) + 1

    if not (total_frames := len(proc_clip)):
        return []

    try:
        from tqdm import tqdm  # type:ignore[import-untyped]

        pbar = tqdm(total=total_frames, unit='frame', desc=f'Dumping numpy arrays to {out_dir}/...')
    except ImportError:
        pbar = None

    def _update_progress() -> None:
        if not pbar:
            return

        pbar.update(1)

    exported_files = []
    frame_data_dict = {}

    def _process_frame(n: int, frame: vs.VideoFrame) -> str | None:
        nonlocal next_name

        try:
            cfamily = frame.format.color_family

            frame_data = np.stack([np.asarray(frame[i]) for i in range(frame.format.num_planes)])

            if cfamily == vs.GRAY:
                frame_data = frame_data.squeeze(0)

            filename = f'{next_name:06d}'

            if export_npz:
                frame_data_dict[filename] = frame_data
            else:
                file_path = out_dir / f'{filename}.npy'
                np.save(file_path, frame_data)
                exported_files.append(file_path)

            next_name += 1
            _update_progress()
            return filename

        except Exception as e:
            print(f'Error processing frame {n}: {e}')
            print(f'Frame format: {frame.format}')
            print(f'Frame dimensions: {frame.width}x{frame.height}')
            _update_progress()

            return None

    proc_frames = clip_async_render(proc_clip, callback=_process_frame)

    if pbar:
        pbar.close()

    if failed_frames := [f for f in proc_frames if f is None]:
        warnings.warn(
            f'clip_to_npy: {len(failed_frames)} frames failed to process.',
            RuntimeWarning
        )

    if not export_npz:
        return exported_files

    npz_path = out_dir / 'frames.npz'
    np.savez_compressed(npz_path, **frame_data_dict)

    return [npz_path]


def npy_to_clip(
    file_paths: list[SPathLike] | SPathLike = [],
    ref: vs.VideoNode | None = None,
    kernel: KernelT = Point,
    func_except: FuncExceptT | None = None
) -> vs.VideoNode:
    """
    Load frames from numpy files (.npy or .npz) into a VapourSynth clip.

    This function assumes it's used in tandem with `clip_to_npy`.

    We use modifyframe to assign the numpy array to frames.
    This helps with memory usage as we don't need to keep all the frames in memory at once
    (which can make loading many frames impractical).

    :param file_paths:      Path to a directory containing .npy files, a single .npz file,
                            or a list of .npy file paths.
    :param ref:             Optional reference clip for format.
    :param kernel:          Kernel used for resampling if ref is passed.
                            Defaults to Point, as that can be up-and-downscaled without loss.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                VapourSynth clip created from the numpy files.
    """

    func = fallback(func_except, npy_to_clip)
    kernel = Kernel.ensure_obj(kernel, func)

    paths = [SPath(file_paths)] if not isinstance(file_paths, list) else [SPath(x) for x in file_paths]
    is_npz = False

    if not paths:
        raise FileWasNotFoundError('No files provided!', func)

    if paths[0].is_dir():
        if npy_files := list(paths[0].glob('*.npy')):
            paths = npy_files
        elif npz_files := list(paths[0].glob('*.npz')):
            paths = npz_files
            is_npz = True
        else:
            raise FileWasNotFoundError('No .npy or .npz files found in the given directory!', func)
    elif paths[0].suffix == '.npz':
        is_npz = True

    if not is_npz:
        try:
            paths = sorted(paths, key=lambda x: int(x.stem) if x.stem.isdigit() else float('inf'))
        except ValueError as e:
            if 'invalid literal for int() with base 10' in str(e):
                raise CustomValueError(
                    'Error sorting paths: File names must be valid integers!', func,
                    '[\n    ' + '\n    '.join([x.stem for x in paths if not x.stem.isdigit()]) + '\n]'
                )
            else:
                raise
        except Exception as e:
            raise CustomValueError(f'Error sorting paths! {str(e)}', func)

    if is_npz:
        npz_data = np.load(paths[0])
        first_key = list(npz_data.keys())[0]
        first_frame = npz_data[first_key]
    else:
        first_frame = np.load(paths[0])

    if first_frame.ndim < 2:
        raise NumpyArrayLoadError(
            f'Invalid frame shape: {first_frame.shape}. Expected at least 2 dimensions.', func
        )

    try:
        height, width = first_frame.shape[-2:]
    except ValueError as e:
        raise CustomValueError(e, func)

    fmt = get_format_from_npy(first_frame)

    clip_length = len(npz_data.keys()) if is_npz else len(paths)
    blank_clip = core.std.BlankClip(None, width, height, fmt, length=clip_length, keep=True)

    def _read_frame(n: int, f: vs.VideoFrame) -> vs.VideoFrame:
        if is_npz:
            loaded_frame = npz_data[list(npz_data.keys())[n]]
        else:
            loaded_frame = np.load(paths[n])

        fout = f.copy()

        if loaded_frame.ndim < 2:
            raise NumpyArrayLoadError(
                f'Invalid frame shape at index {n}: {loaded_frame.shape}. Expected at least 2 dimensions.', func
            )

        if loaded_frame.ndim == 2:
            np.copyto(np.asarray(fout[0]), loaded_frame)
        elif loaded_frame.ndim == 3:
            if loaded_frame.shape[0] == 3:
                for i in range(len(fout)):
                    np.copyto(np.asarray(fout[i]), loaded_frame[i])
            else:
                raise NumpyArrayLoadError(
                    f'Unexpected frame shape: {loaded_frame.shape}. Expected (channels, height, width)', func
                )
        else:
            raise NumpyArrayLoadError(
                f'Invalid frame dimensions: {loaded_frame.ndim}. Expected 2 (GRAY) or 3 (YUV)', func
            )

        return fout

    proc_clip = blank_clip.std.ModifyFrame(blank_clip, _read_frame)
    proc_clip = kernel.resample(proc_clip, fmt)

    func = FunctionUtil(proc_clip, func, None, (vs.GRAY, vs.YUV), 32)
    out = norm_expr(func.work_clip, 'x 0.5 -', func.chroma_pplanes)

    if ref is not None:
        out = kernel.resample(out, ref)

    return out
