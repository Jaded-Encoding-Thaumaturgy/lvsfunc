import warnings
from typing import Any

import numpy as np
from jetpytools import CustomValueError
from vstools import VariableFormatError, check_variable, core, vs

__all__: list[str] = []


class ModelNumpyHandling:
    """A class to inherite from to handle numpy array conversion and handling."""

    def _clip_to_numpy(self, clip: vs.VideoNode) -> np.ndarray[Any, Any]:
        """
        Convert a given vs.VideoNode into a numpy array for model processing.

        :param clip:    The clip to convert.
        :return:        The clip converted into a numpy array.
        """

        try:
            check_variable(clip, self._clip_to_numpy)
        except VariableFormatError as e:
            raise CustomValueError("You must pass a clip with a constant format and resolution.", self._clip_to_numpy) from e

        assert clip.format is not None

        dtype = np.uint16 if clip.format.bits_per_sample > 8 else np.uint8
        np_array = []

        max_height = clip.height
        max_width = clip.width

        for i in range(clip.num_frames):
            frame = clip.get_frame(i)
            frame_array = []

            for plane in range(clip.format.num_planes):
                plane_data = np.frombuffer(frame.get_read_ptr(plane), dtype=dtype)

                height = frame.height >> (plane if clip.format.subsampling_h else 0)
                width = frame.width >> (plane if clip.format.subsampling_w else 0)
                expected_size = height * width

                if plane_data.size != expected_size:
                    warnings.warn(
                        f'Resizing array of size {plane_data.size} to match expected size {expected_size}.',
                        UserWarning
                    )
                    plane_data = np.resize(plane_data, expected_size)

                padded_array = np.zeros((max_height, max_width), dtype=dtype)
                padded_array[:height, :width] = plane_data.reshape(height, width)

                frame_array.append(padded_array)

            np_array.append(np.stack(frame_array, axis=-1))

        return np.stack(np_array, axis=0)

    def _numpy_to_clip(self, np_array: np.ndarray[Any, Any], format: vs.VideoFormat) -> vs.VideoNode:
        """
        Convert a given numpy array back into a vs.VideoNode.

        :param np_array:    The numpy array to convert.
        :param format:      The format of the resulting clip.

        :return:            The numpy array converted back into a VideoNode.
        """

        num_frames, height, width, num_planes = np_array.shape
        clip = core.std.BlankClip(length=num_frames, width=width, height=height, format=format.id)
        for n in range(num_frames):
            frame = clip.get_frame(n)
            for plane in range(num_planes):
                                    np.copyto(np.asarray(frame.get_write_array(plane)), np_array[n, :, :, plane])  # type: ignore[attr-defined]  # type: ignore[attr-defined]
        return clip

    def _replace_array_section(
        self,
        target_array: np.ndarray[Any, Any],
        replacement_array: np.ndarray[Any, Any],
        section: tuple[int, int, int, int]
    ) -> np.ndarray[Any, Any]:
        """
        Replace a section of the target array with the replacement array.

        :param target_array:        The target numpy array to be modified.
        :param replacement_array:   The replacement numpy array.
        :param start_idx:           The starting index (frame, height, width, plane) for the replacement.

        :return:                    The modified numpy array.
        """

        slices = tuple(slice(start, start + size) for start, size in zip(section, replacement_array.shape))
        target_array[slices] = replacement_array

        return target_array
