from __future__ import annotations

from typing import Any

from vskernels import Bilinear, Kernel, KernelT, Lanczos
from vstools import (CustomStrEnum, CustomTypeError, CustomValueError,
                     FuncExceptT, Matrix, MatrixT, SPath, SPathLike,
                     clip_async_render, core, fallback, vs)

from .nn import clip_to_npy
from .random import get_random_frames

__all__: list[str] = [
    'ExportFrames', 'export_frames',
]


class ExportFrames(CustomStrEnum):
    PNG: ExportFrames = 'png'  # type:ignore
    JPEG: ExportFrames = 'jpeg'  # type:ignore
    JPG: ExportFrames = 'jpg'  # type:ignore
    WEBP: ExportFrames = 'webp'  # type:ignore
    AVIF: ExportFrames = 'avif'  # type:ignore
    BMP: ExportFrames = 'bmp'  # type:ignore
    GIF: ExportFrames = 'gif'  # type:ignore
    HEIC: ExportFrames = 'heic'  # type:ignore
    JXL: ExportFrames = 'jxl'  # type:ignore
    PPM: ExportFrames = 'ppm'  # type:ignore
    PGM: ExportFrames = 'pgm'  # type:ignore
    PBM: ExportFrames = 'pbm'  # type:ignore
    PNM: ExportFrames = 'pnm'  # type:ignore
    TGA: ExportFrames = 'tga'  # type:ignore
    TIFF: ExportFrames = 'tiff'  # type:ignore
    NPY: ExportFrames = 'npy'  # type:ignore
    NPZ: ExportFrames = 'npz'  # type:ignore

    def __call__(
        self, clip: vs.VideoNode,
        filename: SPathLike = "bin/%d.png",
        kernel: KernelT = Bilinear,
        matrix: MatrixT | None = None,
        func_except: FuncExceptT | None = None,
        **kwargs: Any
    ) -> list[SPath]:
        """
        Export all frames from a VideoNode as images.

        If exporting the same frames from multiple clips (e.g., for lq vs. hq training),
        it's recommended to use `get_random_frames` first to get a clip of random frames,
        and pass that here instead.

        If you're exporting to PNG, this function will use the `vsfpng` plugin if installed,
        otherwise falling back to `imwri.Write`.

        :param clip:            The input clip to process.
        :param filename:        Output filename pattern. Must include "%d" for frame number substitution.
        :param kernel:          Kernel for resampling, if necessary. Default: Bilinear.
        :param matrix:          Color matrix of the input clip. Attempts to detect if None.
        :param func_except:     Function returned for custom error handling.
                                This should only be set by VS package developers.
        :param kwargs:          Additional arguments to pass to the underlying writer.

        :return:                List of SPath objects pointing to exported images.
        """

        func = func_except or self.__class__

        kernel = Kernel.ensure_obj(kernel, func)
        matrix = Matrix.from_param_or_video(matrix, clip, False, func)

        self._is_np = self in (ExportFrames.NPY, ExportFrames.NPZ)

        if not self._is_np:
            clip = kernel.resample(clip, vs.RGB24, matrix_in=matrix)

        sfile = self._check_sfile(filename, func)

        return self._render_frames(clip, sfile, **kwargs)

    def _check_sfile(self, file: SPathLike, func: FuncExceptT) -> SPath:
        """Validate the output file path."""

        sfile = SPath(file)

        if not self._is_np and '%d' not in sfile.to_str():
            raise CustomTypeError("Filename must include '%d' for frame number substitution!", func)

        sfile.get_folder().mkdir(parents=True, exist_ok=True)

        if list(sfile.get_folder().glob("*")):
            input(
                f'ExportFrames: Files found in \"{sfile.parent}\". They may be overwritten. '
                'Press Enter to continue or Ctrl+C to abort...'
            )

        return sfile

    def _render_frames(self, clip: vs.VideoNode, out_file: SPath, **kwargs: Any) -> list[SPath]:
        """Render the frames to a PNG file using the vsfpng plugin, or fallback to imwri.Write."""

        if self._is_np:
            return clip_to_npy(clip, out_file.parent.to_str(), export_npz=self == ExportFrames.NPZ, **kwargs)

        if self is ExportFrames.PNG and hasattr(core, "fpng"):
            writer = Lanczos.resample(clip, vs.RGB24).fpng.Write(out_file.to_str(), **kwargs)
        else:
            writer = clip.imwri.Write(self.value, out_file.to_str(), **kwargs)

        clip_async_render(writer)

        return list(out_file.parent.glob("*.png"))


def export_frames(
    clip: vs.VideoNode,
    frames: list[int] | int | None = None,
    filename: SPathLike = SPath("bin/%d.png"),
    dur: float = 5.0,
    matrix: MatrixT | None = None,
    kernel: KernelT = Lanczos(3),
    func_except: FuncExceptT | None = None,
    **kwargs: Any
) -> list[SPath]:
    """
    Export random or specific frames from a VideoNode as PNG images.

    :param clip:        The input clip to process.
    :param filename:    Output filename pattern. Must include "%d" for frame number substitution.
    :param matrix:      Color matrix of the input clip. Attempts to detect if None.
    :param kernel:      Resampling kernel for RGB conversion if necessary.
    :param func_except: Custom error handling function (for package developers).

    :return:            List of SPath objects pointing to exported images.
    """

    import warnings

    warnings.warn(
        'export_frames: This function is deprecated and will be removed '
        'in a future version. Use ExportFrames with get_random_frames instead!',
        DeprecationWarning
    )

    func = fallback(func_except, export_frames)

    if frames is None:
        frames_clip = get_random_frames(clip)
    else:
        if isinstance(frames, int):
            frames = [frames]

        try:
            frames_clip = core.std.Splice([clip[f] for f in sorted(frames)])
        except vs.Error:
            raise CustomValueError("Invalid frame numbers provided!", func)

    return ExportFrames.PNG(frames_clip, filename, matrix, func, **kwargs)
