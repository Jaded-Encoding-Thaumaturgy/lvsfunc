import warnings

import numpy as np
from vsexprtools import norm_expr
from vstools import (CustomValueError, FileWasNotFoundError, FuncExceptT,
                     FunctionUtil, SPath, SPathLike, clip_async_render, core,
                     fallback, get_depth, initialize_clip, vs)

from ..exceptions import NumpyArrayLoadError
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


def clip_to_npy(src: vs.VideoNode, out_dir: SPathLike = 'bin/', export_npz: bool = False) -> list[SPath]:
    """
    Export frames from a VideoNode to numpy array files.

    This function is intended to be used to help with preparing training data for neural networks.

    The function will not overwrite existing files,
    and instead increments the next filename by 1.

    :param src:                         The input video clip.
    :param out_dir:                     The directory to save the numpy arrays.
                                        Default: "bin/".
    :param export_npz:                  If True, export the numpy arrays as a single .npz file.
                                        Default: False.

    :return:                            A list of paths to the exported numpy arrays or the path to the .npz file.

    :raises RuntimeWarning:             If any frames failed to process.
    """

    func = FunctionUtil(src, clip_to_npy, None, (vs.GRAY, vs.YUV), 32)

    proc_clip = func.work_clip

    out_dir = SPath(out_dir)
    out_dir.mkdir(511, True, True)

    next_name = max((int(f.stem) for f in out_dir.glob('*.npy')), default=0) + 1

    if not (total_frames := len(proc_clip)):
        return []

    try:
        from tqdm import tqdm  # type:ignore[import-untyped]
        pbar = tqdm(total=total_frames, unit='frame', desc=f'Dumping numpy arrays to {out_dir}...')
    except ImportError:
        pbar = None

    def _update_progress(filename: str | None = None) -> None:
        if not pbar:
            return

        pbar.update(1)

        if filename:
            pbar.set_postfix({'Current file': filename}, refresh=True)

    exported_files = []
    frame_data_dict = {}

    def _process_frame(n: int, frame: vs.VideoFrame) -> str | None:
        nonlocal next_name

        try:
            color_family = frame.format.color_family

            if color_family == vs.YUV:
                frame_data = {f'plane_{i}': np.asarray(frame[i]) for i in range(frame.format.num_planes)}
            elif color_family == vs.GRAY:
                frame_data = {'plane_0': np.asarray(frame[0])}
            else:
                raise CustomValueError(f"Unsupported color family: {color_family}", func.func)

            filename = f'{next_name:05d}'

            if export_npz:
                frame_data_dict[filename] = frame_data
            else:
                file_path = out_dir / f'{filename}.npy'

                np.save(file_path, frame_data)

                exported_files.append(file_path)

            next_name += 1

            _update_progress(filename)

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
    np.savez_compressed(npz_path, **frame_data_dict, allow_pickle=True)

    return [npz_path]


def npy_to_clip(
    file_paths: list[SPathLike] | SPathLike = [],
    ref: vs.VideoNode | None = None,
    func_except: FuncExceptT | None = None
) -> vs.VideoNode:
    """
    Load frames from numpy files (.npy or .npz) into a VapourSynth clip.

    We use modifyframe to assign the numpy array to frames.
    This helps with memory usage as we don't need to keep all the frames in memory at once
    (which can make loading many frames impractical).

    :param file_paths:      Path to a directory containing .npy files, a single .npz file,
                            or a list of .npy file paths.
    :param ref:             Optional reference clip for format.
    :param func_except:     Function returned for custom error handling.
                            This should only be set by VS package developers.

    :return:                VapourSynth clip created from the numpy files.
    """

    func = fallback(func_except, npy_to_clip)
    paths = [SPath(file_paths)] if not isinstance(file_paths, list) else [SPath(x) for x in file_paths]
    is_npz = False

    if not paths:
        raise FileWasNotFoundError("No files provided!", func)

    if paths[0].is_dir():
        if npy_files := list(paths[0].glob("*.npy")):
            paths = npy_files
        elif npz_files := list(paths[0].glob("*.npz")):
            paths = npz_files
            is_npz = True
        else:
            raise FileWasNotFoundError("No .npy or .npz files found in the given directory!", func)
    elif paths[0].suffix == '.npz':
        is_npz = True

    if not is_npz:
        try:
            paths = sorted(paths, key=lambda x: int(x.stem) if x.stem.isdigit() else float('inf'))
        except ValueError as e:
            if "invalid literal for int() with base 10" in str(e):
                raise CustomValueError("Error sorting paths: File names must be valid integers!", func)
            else:
                raise
        except Exception as e:
            raise CustomValueError(f"Error sorting paths! {str(e)}", func)

    if is_npz:
        npz_data = np.load(paths[0], allow_pickle=True)
        first_key = list(npz_data.keys())[0]
        first_frame = npz_data[first_key]

        if isinstance(first_frame, np.ndarray) and first_frame.shape == ():
            first_frame = first_frame.item()
    else:
        first_frame = np.load(paths[0], allow_pickle=True).item()

    if isinstance(first_frame, dict):
        plane_0_missing = 'plane_0' not in first_frame
        plane_0_not_array = not isinstance(first_frame['plane_0'], np.ndarray)
        plane_0_low_dim = first_frame['plane_0'].ndim < 2

        if plane_0_missing or plane_0_not_array or plane_0_low_dim:
            error_message = "Invalid frame data structure."

            if plane_0_missing:
                error_message += " 'plane_0' is missing from the frame dictionary."
            elif plane_0_not_array:
                error_message += " 'plane_0' is not a numpy array."
            elif plane_0_low_dim:
                error_message += " 'plane_0' has less than 2 dimensions."

            raise NumpyArrayLoadError(error_message, func)

        height, width = first_frame['plane_0'].shape
    elif isinstance(first_frame, np.ndarray):
        if first_frame.ndim < 2:
            raise NumpyArrayLoadError(
                f"Invalid frame shape: {first_frame.shape}. Expected at least 2 dimensions.", func
            )

        height, width = first_frame.shape[:2]
    else:
        raise NumpyArrayLoadError(f"Unsupported frame data type: {type(first_frame)}", func)

    fmt = get_format_from_npy(first_frame)

    clip_length = len(npz_data.keys()) if is_npz else len(paths)
    blank_clip = core.std.BlankClip(
        None, width, height, fmt, length=clip_length, keep=True
    )

    def _read_frame(n: int, f: vs.VideoFrame) -> vs.VideoFrame:
        if is_npz:
            loaded_frame = npz_data[list(npz_data.keys())[n]]
            if isinstance(loaded_frame, np.ndarray) and loaded_frame.shape == ():
                loaded_frame = loaded_frame.item()
        else:
            loaded_frame = np.load(paths[n], allow_pickle=True).item()

        fout = f.copy()

        if isinstance(loaded_frame, np.ndarray):
            if loaded_frame.ndim < 2:
                raise NumpyArrayLoadError(
                    f"Invalid frame shape at index {n}: {loaded_frame.shape}. Expected at least 2 dimensions.", func
                )

            np.copyto(np.asarray(fout[0]), loaded_frame)
        elif isinstance(loaded_frame, dict):
            for plane in range(f.format.num_planes):
                plane_key = f'plane_{plane}'

                if plane_key not in loaded_frame or loaded_frame[plane_key].ndim < 2:
                    raise NumpyArrayLoadError(
                        f"Invalid frame data structure at index {n}. '{plane_key}' "
                        "is missing or has less than 2 dimensions.", func
                    )

                np.copyto(np.asarray(fout[plane]), loaded_frame[plane_key])
        else:
            raise CustomValueError(f"Unsupported frame data type at index {n}: {type(loaded_frame)}", func)

        return fout

    proc_clip = blank_clip.std.ModifyFrame(blank_clip, _read_frame)

    return initialize_clip(proc_clip, ref or get_depth(proc_clip), func=func)  # type:ignore[arg-type]
