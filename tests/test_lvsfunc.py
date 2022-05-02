"""
    Tests to make sure lvsfunc functions return the expected values.
    A lot of methods were taken from vsutil.
"""
from __future__ import annotations

import contextlib
import os
import shutil
import subprocess
import time
import unittest
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List

import lvsfunc as lvf
import vapoursynth as vs
import vsutil

core = vs.core

__all__: List[str] = []


class LvsfuncTests(unittest.TestCase):
    # Common arguments
    # Filepaths and names
    tests_in_cwd: bool = 'tests' in os.getcwd()
    DEPS: str = "dependencies"

    if not tests_in_cwd:
        DEPS = f"tests/{DEPS}"

    output_clip_path: Path = Path(f'output')

    if not tests_in_cwd:
        output_clip_path = Path('tests') / output_clip_path

    output_clip_file = output_clip_path / Path("test_clip.mkv")
    output_clip_file_abs = output_clip_file.resolve()
    output_clip_idx =  output_clip_path / Path("test_clip.mkv.lwi")

    # Common values
    DEF_LENGTH: int = 100

    DEF_WIDTH: int = 160
    DEF_HEIGHT: int = 120

    COLOR_BLACK: List[int] = [0, 128, 128]
    COLOR_WHITE: List[int] = [255, 128, 128]

    # 16/9 256x144 clip
    SMALL_WIDTH: int = 256
    SMALL_HEIGHT: int = 144

    # 16/9 1024x576 clip
    MEDIUM_WIDTH: int = 1024
    MEDIUM_HEIGHT: int = 576

    # 16/9 1920x1080 clip
    BIG_WIDTH: int = 1920
    BIG_HEIGHT: int = 1080

    # 16/9 1920x1080 clip
    VBIG_WIDTH: int = 3840
    VBIG_HEIGHT: int = 2160

    # A bunch of blank clips with different (relatively) common formats
    DEF_VALUES: Dict[str, Any] = {
        'width': DEF_WIDTH, 'height': DEF_HEIGHT,
        'color': COLOR_BLACK, 'length': DEF_LENGTH,
        'fpsnum': 24000, 'fpsden': 1001
    }

    YUV420P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, **DEF_VALUES)
    YUV420P10_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P10, **DEF_VALUES)
    YUV420P16_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P16, **DEF_VALUES)
    YUV420PS_CLIP: vs.VideoNode = vsutil.depth(YUV420P8_CLIP, 32, dither_type=vsutil.Dither.NONE)

    YUV444P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV444P8, **DEF_VALUES)
    YUV444P10_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV444P10, **DEF_VALUES)
    YUV444P16_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV444P16, **DEF_VALUES)
    YUV444PS_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV444PS, **DEF_VALUES)

    RGB24_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.RGB24)
    RGBS_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.RGBS)

    YUV422P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV422P8, **DEF_VALUES)
    YUV410P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV410P8, **DEF_VALUES)
    YUV411P8_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV411P8, **DEF_VALUES)
    YUV440P8_CLIP = core.std.BlankClip(format=vs.YUV440P8, **DEF_VALUES)

    del DEF_VALUES['color']

    GRAY8_CLIP = core.std.BlankClip(format=vs.GRAY8, **DEF_VALUES)
    GRAY16_CLIP = core.std.BlankClip(format=vs.GRAY16, **DEF_VALUES)
    GRAYS_CLIP = core.std.BlankClip(format=vs.GRAYS, **DEF_VALUES)

    # Specific colourspaces, transfers, and primaries
    BT709_CLIP = core.std.SetFrameProps(YUV420P8_CLIP,
                                        _Matrix=lvf.types.Matrix.BT709,
                                        _Transfer=lvf.types.Matrix.BT709,
                                        _Primaries=lvf.types.Matrix.BT709)
    BT470BG_CLIP = core.std.SetFrameProps(YUV420P8_CLIP,
                                          _Matrix=lvf.types.Matrix.BT470BG,
                                          _Transfer=lvf.types.Matrix.BT470BG,
                                          _Primaries=lvf.types.Matrix.BT470BG)
    BT2020NC_CLIP = core.std.SetFrameProps(YUV420P8_CLIP,
                                          _Matrix=lvf.types.Matrix.BT2020NC,
                                          _Transfer=lvf.types.Matrix.BT2020NC,
                                          _Primaries=lvf.types.Matrix.BT2020NC)


    # Other kinds of blank clips
    SMALLER_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=SMALL_WIDTH, height=SMALL_HEIGHT)
    MEDIUM_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=MEDIUM_WIDTH, height=MEDIUM_HEIGHT)
    BIGGER_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=BIG_WIDTH, height=BIG_HEIGHT)
    VERYBIG_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=VBIG_WIDTH, height=VBIG_HEIGHT)

    BLACK_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=COLOR_BLACK, **DEF_VALUES)
    WHITE_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=COLOR_WHITE, **DEF_VALUES)

    VARIABLE_FORMAT_CLIP: vs.VideoNode = core.std.Interleave([YUV420P8_CLIP, YUV444P8_CLIP], mismatch=True)

    # 30p clips for deinterlacing functions
    BLACK_SAMPLE_CLIP_30p: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=MEDIUM_WIDTH,
                                                             height=MEDIUM_HEIGHT, color=COLOR_BLACK,
                                                             length=DEF_LENGTH, fpsnum=30000, fpsden=1001)
    BLACK_SAMPLE_CLIP_30p = core.std.SetFieldBased(BLACK_SAMPLE_CLIP_30p, value=2)
    WHITE_SAMPLE_CLIP_30p: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=MEDIUM_WIDTH,
                                                             height=MEDIUM_HEIGHT, color=COLOR_WHITE,
                                                             length=DEF_LENGTH, fpsnum=30000, fpsden=1001)
    BLACK_SAMPLE_CLIP_30p = core.std.SetFieldBased(WHITE_SAMPLE_CLIP_30p, value=2)

    # Coloured clips
    BLUE_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=[0, 255, 0],
                                                        width=MEDIUM_HEIGHT, height=MEDIUM_HEIGHT)
    GREEN_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=[128, 0, 0],
                                                         width=MEDIUM_HEIGHT, height=MEDIUM_HEIGHT)
    RED_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=[0, 0, 255],
                                                       width=MEDIUM_HEIGHT, height=MEDIUM_HEIGHT)
    YELLOW_SAMPLE_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, color=[255, 0, 255],
                                                          width=MEDIUM_HEIGHT, height=MEDIUM_HEIGHT)

    # Additional dependencies
    ASS_FILE: str = os.path.abspath(f"{DEPS}/lvsfunc_test.ass")
    PNG_FILE: str = os.path.abspath(f"{DEPS}/lvsfunc_test.png")
    SHADER_FILE: str = os.path.abspath(f"{DEPS}/FSRCNNX_x2_16-0-4-1.glsl")

    # Basic assertions
    def assert_same_dimensions(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same width and height.
        """
        self.assertEqual(a.height, b.height, f"Same height expected, was {a.height} and {b.height}.")
        self.assertEqual(a.width, b.width, f"Same width expected, was {a.width} and {b.width}.")

    def assert_same_format(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same format (but not necessarily size).
        """
        assert a.format
        assert b.format

        self.assertEqual(a.format.id, b.format.id, f"Same format expected, was {a.format.id} and {b.format.id}.")

    def assert_same_bitdepth(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same number of bits per sample.
        """
        assert a.format
        assert b.format

        self.assertEqual(a.format.bits_per_sample, b.format.bits_per_sample,
                         f"Same depth expected, was {a.format.bits_per_sample} "
                         f"and {b.format.bits_per_sample}.")

    def assert_same_length(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same length.
        """
        self.assertEqual(len(a), len(b),
                         f"Same number of frames expected, was {len(a)} and {len(b)}.")

    def assert_same_metadata(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same height, width, format, depth, and length.
        """
        self.assert_same_format(a, b)
        self.assert_same_dimensions(a, b)
        self.assert_same_length(a, b)

    def assert_returns_callable(self, func: Any) -> None:
        """
        Assert that the function returns a callable.
        """
        try:
            assert callable(func)
        except AssertionError:
            raise ValueError(f"Expected function to return a callable, was {type(func)}.")

    def assert_same_frame(self, a: vs.VideoNode, b: vs.VideoNode, frameno: int = 0) -> None:
        """
        Assert that two frames are identical. Only the first frame of the arguments is used.
        """
        diff = core.std.PlaneStats(a, b)
        frame = diff.get_frame(frameno)
        self.assertEqual(frame.props.PlaneStatsDiff, 0,
                         f"Same frame expected, was {frame.props.PlaneStatsDiff}.")

    def assert_same_framerate(self, a: vs.VideoNode, b: vs.VideoNode) -> None:
        """
        Assert that two clips have the same framenum and frameden.
        """
        self.assertEqual(a.fps, b.fps, f"Same framerate expected, was {a.fps} and {b.fps}.")

    def assert_not_same_frame(self, a: vs.VideoNode, b: vs.VideoNode, frameno: int = 0) -> None:
        """
        Assert that two frames are NOT identical. Only the first frame of the arguments is used.
        """
        diff = core.std.PlaneStats(a, b)
        frame = diff.get_frame(frameno)
        self.assertNotEqual(frame.props.PlaneStatsDiff, 0,
                            f"Different frame expected, was {frame.props.PlaneStatsDiff}.")

    def assert_length(self, clip: vs.VideoNode, length: int) -> None:
        """
        Assert that a clip is a certain length.
        """
        try:
            assert len(clip) == length
        except AssertionError:
            raise ValueError(f"Expected clip to have a length of {length}, was {len(clip)}")

    def assert_framerate(self, clip: vs.VideoNode, fps: Fraction) -> None:
        """
        Assert that a clip has a certain framerate.
        """
        try:
            assert clip.fps == fps
        except AssertionError:
            raise ValueError(f"Expected clip to have a framerate of {fps}, was {clip.fps}.")

    def assert_variable_format(self, clip: vs.VideoNode) -> None:
        """
        Assert that a clip is of a variable format.
        """
        try:
            assert clip.format is None
        except AssertionError:
            assert clip.format
            raise ValueError(f"Expected clip to have a variable format, was {clip.format.id}.")

    def assert_variable_dimensions(self, clip: vs.VideoNode) -> None:
        """
        Assert that a clip has a variable width or height.
        """
        try:
            assert 0 in (clip.width, clip.height)
        except AssertionError:
            raise ValueError(f"Expected clip to have variable dimensions, was {clip.width} and {clip.height}.")

    def assert_dimensions(self, clip: vs.VideoNode, width: int, height: int) -> None:
        """
        Assert that a clip has a specific width and height.
        """
        self.assertEqual(clip.width, width)
        self.assertEqual(clip.height, height)

    def assert_runs(self, clip: vs.VideoNode) -> None:
        """
        Assert that a clip returns a frame.
        """
        try:
            assert clip.get_frame(0)
        except AssertionError:
            raise ValueError("Expected for clip to return a frame.")

    def assert_prop(self, clip: vs.VideoNode, prop: str, ptype: Any) -> None:
        """
        Assert that a clip stores a specific prop.
        """
        try:
            assert lvf.util.get_prop(clip.get_frame(0), prop, ptype)
        except AssertionError:
            raise ValueError(f"Expected clip to have {prop} property.")

    def assert_prop_value(self, clip: vs.VideoNode, prop: str, ptype: Any, value: Any) -> None:
        """
        Assert that a prop has the specific value.
        """
        try:
            prop = lvf.util.get_prop(clip.get_frame(0), prop, ptype)
            assert prop == value
        except AssertionError:
            raise ValueError(f"Expected clip to have {prop} property.")

    def assert_file_exists(self, path: str | Path) -> None:
        """
        Assert that a file exists.
        """
        if isinstance(path, str):
            path = Path(path)

        try:
            assert path.exists()
        except AssertionError:
            raise AssertionError(f"{path} does not exist!")

    def create_clip(self, width: int = 1280, height: int = 720,
                    ext: str | None = None, timer: float = 2.5) -> None:
        """
        Create a test clip using ffmpeg.
        """
        output_clip_name = Path(str(self.output_clip_file).replace('mkv', ext)) if ext \
            else self.output_clip_file

        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                subprocess.Popen([
                    'ffmpeg', '-f', 'lavfi', '-i',
                    f'testsrc=duration=1:size={width}x{height}:rate=24000/1001',
                    output_clip_name
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

        time.sleep(timer)  # Allow it time to cleanly generate the clip

    def clean_output_clip(self) -> None:
        """
        Delete the test clip generated by ffmpeg.
        """
        try:
            os.rename(self.output_clip_file_abs, self.output_clip_file_abs)
            shutil.rmtree(self.output_clip_path.resolve())
        except OSError as e:
            raise PermissionError(e)


    def final_cleanup(self) -> None:
        """
        Run after unit tests. Cleans up any remaining test files that may remain.
        """
        self.clean_output_clip()


# lvsfunc.aa
class LvsfuncTestAa(LvsfuncTests):
    def test_clamp_aa(self) -> None:
        clip = lvf.aa.clamp_aa(src=self.YUV420P8_CLIP, weak=self.YUV420P8_CLIP, strong=self.YUV420P8_CLIP)
        self.assert_runs(clip)

    def test_taa(self) -> None:
        clip = lvf.aa.taa(clip=self.YUV420P8_CLIP, aafun=lvf.aa.nnedi3())
        self.assert_runs(clip)

    def test_nnedi3(self) -> None:
        func = lvf.aa.nnedi3()
        self.assert_returns_callable(func)

    def test_eedi3(self) -> None:
        func = lvf.aa.eedi3()
        self.assert_returns_callable(func)

    def test_nneedi3_clamp(self) -> None:
        clip = lvf.aa.nneedi3_clamp(clip=self.YUV420P8_CLIP)
        self.assert_runs(clip)

    def test_transpose_aa(self) -> None:
        clip = lvf.aa.transpose_aa(clip=self.YUV420P8_CLIP)
        self.assert_runs(clip)

    def test_upscaled_sraa(self) -> None:
        clip = lvf.aa.upscaled_sraa(clip=self.YUV420P8_CLIP)
        self.assert_runs(clip)

        clip_down = lvf.aa.upscaled_sraa(clip=self.YUV420P8_CLIP, width=self.SMALL_WIDTH, height=self.SMALL_HEIGHT)
        self.assert_dimensions(clip_down, width=self.SMALL_WIDTH, height=self.SMALL_HEIGHT)

    def test_based_aa(self) -> None:
        clip = lvf.aa.based_aa(self.YUV420P8_CLIP, shader_file=self.SHADER_FILE)
        self.assert_runs(clip)


# lvsfunc.comparison
class LvsfuncTestComparison(LvsfuncTests):
    def test_compare(self) -> None:
        clip = lvf.comparison.compare(clip_a=self.BLACK_SAMPLE_CLIP, clip_b=self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_same_format(clip, self.RGB24_CLIP)

        clip_no_resample = lvf.comparison.compare(clip_a=self.YUV420P8_CLIP, clip_b=self.YUV420P8_CLIP,
                                                  force_resample=False, print_frame=False)
        self.assert_same_format(clip_no_resample, self.YUV420P8_CLIP)
        self.assert_same_frame(clip_no_resample, self.BLACK_SAMPLE_CLIP, 0)

        clip_mismatch = lvf.comparison.compare(clip_a=self.YUV420P8_CLIP, clip_b=self.YUV420P10_CLIP,
                                               force_resample=False, mismatch=True)
        self.assert_variable_format(clip_mismatch)

    def test_stack_compare(self) -> None:
        clip = lvf.comparison.stack_compare(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, 1024, 864)

    def test_stack_planes(self) -> None:
        clip = lvf.comparison.stack_planes(self.YUV420P8_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, int(self.DEF_WIDTH / 2 + self.DEF_WIDTH), self.DEF_HEIGHT)
        self.assert_same_format(clip, self.GRAY8_CLIP)

        clip_vert = lvf.comparison.stack_planes(self.YUV420P8_CLIP, stack_vertical=True)
        self.assert_dimensions(clip_vert, self.DEF_WIDTH, int(self.DEF_HEIGHT / 2 + self.DEF_HEIGHT))

        clip_444 = lvf.comparison.stack_planes(self.YUV444P8_CLIP)
        self.assert_dimensions(clip_444, self.DEF_WIDTH * 3, self.DEF_HEIGHT)

        clip_444_vert = lvf.comparison.stack_planes(self.YUV444P8_CLIP, stack_vertical=True)
        self.assert_dimensions(clip_444_vert, self.DEF_WIDTH, self.DEF_HEIGHT * 3)

    def test_diff_hardsub_mask(self) -> None:
        clip = lvf.comparison.diff_hardsub_mask(self.YUV420P8_CLIP, self.YUV420P8_CLIP)
        self.assert_runs(clip)

    def test_diff(self) -> None:
        with open(os.devnull, 'w') as devnull:
            with contextlib.redirect_stdout(devnull):
                clip = lvf.comparison.diff(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
                clip_interleave = lvf.comparison.diff(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP,
                                                      interleave=True)
                clip_exclude = lvf.comparison.diff(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP,
                                                   exclusion_ranges=[(1, self.BLACK_SAMPLE_CLIP.num_frames)])

        self.assert_runs(clip)  # type:ignore[arg-type]
        self.assert_dimensions(clip, 1024, 864)  # type:ignore[arg-type]

        clip_text = self.BLACK_SAMPLE_CLIP.text.FrameNum(9).text.Text("Clip A")
        self.assert_same_frame(clip_interleave, clip_text, 0)  # type:ignore[arg-type]

        self.assert_length(clip_exclude, 1)  # type:ignore[arg-type]

    def test_interleave(self) -> None:
        clip = lvf.comparison.interleave(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_same_frame(clip, self.BLACK_SAMPLE_CLIP, 0)

    def test_split(self) -> None:
        clip = lvf.comparison.split(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_tile(self) -> None:
        clip = lvf.comparison.tile(
            self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP, self.BLACK_SAMPLE_CLIP,
            self.WHITE_SAMPLE_CLIP, self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP,
            self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP, self.BLACK_SAMPLE_CLIP,
        )
        self.assert_runs(clip)
        self.assert_dimensions(clip, self.DEF_WIDTH * 3, self.DEF_HEIGHT * 3)

    def test_stack_vertical(self) -> None:
        clip = lvf.comparison.stack_vertical(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, self.DEF_WIDTH, self.DEF_HEIGHT * 2)

    def test_stack_horizontal(self) -> None:
        clip = lvf.comparison.stack_horizontal(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, self.DEF_WIDTH * 2, self.DEF_HEIGHT)


# lvsfunc.deblock
class LvsfuncTestDeblock(LvsfuncTests):
    MOD8_WIDTH = 128
    MOD8_HEIGHT = 72

    MOD8_YUV_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.YUV420P8, width=MOD8_WIDTH, height=MOD8_HEIGHT)
    MOD8_RGB_CLIP: vs.VideoNode = core.std.BlankClip(format=vs.RGB24, width=MOD8_WIDTH, height=MOD8_HEIGHT)

    def test_vsdpir(self) -> None:
        clip = lvf.deblock.vsdpir(self.MOD8_YUV_CLIP, matrix=lvf.types.Matrix.BT709)
        self.assert_runs(clip)

        clip_rgb = lvf.deblock.vsdpir(self.MOD8_RGB_CLIP)
        self.assert_same_format(clip_rgb, self.RGB24_CLIP)

        clip_444 = lvf.deblock.vsdpir(self.YUV420P16_CLIP, i444=True, matrix=lvf.types.Matrix.BT709)
        self.assert_same_format(clip_444, self.YUV444P16_CLIP)

    def test_autodb_dpir(self) -> None:
        input_clip = core.std.SetFrameProps(self.MOD8_YUV_CLIP, _PictType=b'I')

        clip = lvf.deblock.autodb_dpir(input_clip, matrix=lvf.types.Matrix.BT709)
        self.assert_runs(clip)

        # clip_props = lvf.deblock.autodb_dpir(input_clip, write_props=True, matrix=lvf.types.Matrix.BT709)
        # self.assert_prop(clip_props, 'Adb_EdgeValRefDiff', float)  # This errors and idk why


# lvsfunc.dehalo
class LvsfuncTestDehalo(LvsfuncTests):
    def test_bidehalo(self) -> None:
        clip = lvf.dehalo.bidehalo(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_masked_dha(self) -> None:
        clip = lvf.dehalo.masked_dha(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_fine_dehalo(self) -> None:
        clip = lvf.dehalo.fine_dehalo(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)


# lvsfunc.dehardsub
class LvsfuncTestDehardsub(LvsfuncTests):
    ...


# lvsfunc.deinterlace
class LvsfuncTestDeinterlace(LvsfuncTests):
    def create_pulldown_clip(self) -> vs.VideoNode:
        """
        .. warning::
            This function has not been properly implemented yet!

        Create a test 3:2 pulldown clip.
        """
        clip = lvf.comparison.interleave(blue=self.BLUE_SAMPLE_CLIP,
                                         green=self.GREEN_SAMPLE_CLIP,
                                         red=self.RED_SAMPLE_CLIP,
                                         yellow=self.YELLOW_SAMPLE_CLIP)
        clip = core.std.AssumeFPS(clip, self.BLACK_SAMPLE_CLIP)[2::]
        clip = core.std.SeparateFields(clip, tff=True)
        clip = core.std.SelectEvery(clip, cycle=8, offsets=[0, 1, 2, 3, 2, 5, 4, 7, 6, 7])
        clip = core.std.DoubleWeave(clip, tff=True)[2::]

        return clip

    def test_sivtc(self) -> None:
        clip = lvf.deinterlace.sivtc(self.BLACK_SAMPLE_CLIP_30p)

        self.assert_runs(clip)
        self.assert_length(clip, 80)
        self.assert_framerate(clip, Fraction(24000, 1001))

        clip_no_dec = lvf.deinterlace.sivtc(self.BLACK_SAMPLE_CLIP_30p, decimate=False)
        self.assert_length(clip_no_dec, 200)
        self.assert_framerate(clip_no_dec, Fraction(60000, 1001))

    def test_seek_cycle(self) -> None:
        clip = lvf.deinterlace.seek_cycle(self.MEDIUM_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, 1344, 776)

    # def test_tivtc_vfr(self) -> None:
    """
    Currently broken!
    """
    #     iclip = core.std.SetFieldBased(self.BLACK_SAMPLE_CLIP, 2)
    #     return ...

    #     with open(os.devnull, 'w') as devnull:
    #         with contextlib.redirect_stdout(devnull):
    #             clip = lvf.deinterlace.tivtc_vfr(iclip)

    #     self.assert_runs(clip)

    #     shutil.rmtree(Path('.ivtc'))

    def test_ivtc_credits(self) -> None:
        clip = lvf.deinterlace.ivtc_credits(self.BLACK_SAMPLE_CLIP_30p, frame_ref=0)
        self.assert_runs(clip)
        self.assert_length(clip, 80)
        self.assert_framerate(clip, Fraction(24000, 1001))


# lvsfunc.denoise
class LvsfuncTestDenoise(LvsfuncTests):
    def test_bm3d(self) -> None:
        clip = lvf.denoise.bm3d(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)


# lvsfunc.fun
class LvsfuncTestFun(LvsfuncTests):
    def test_minecrafity(self) -> None:
        clip = lvf.fun.minecraftify(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)


# lvsfunc.kernels
class LvsfuncTestKernels(LvsfuncTests):
    def test_get_all_kernels(self) -> None:
        kernels = lvf.kernels.get_all_kernels()
        # TODO: Assert that every object in array inherits from a Kernel object.
        self.assertIsInstance(kernels, list, f"Expected to return a list, instead returned {type(kernels)}")

    def test_get_kernel(self) -> None:
        kernel = lvf.kernels.get_kernel("catrom")
        self.assertEqual(kernel, lvf.kernels.Catrom)

    # TODO: Generic test that loops over every Kernel class?


# lvsfunc.mask
class LvsfuncTestMask(LvsfuncTests):
    def test_detail_mask(self) -> None:
        mask = lvf.mask.detail_mask(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(mask)

    def test_detail_mask_neo(self) -> None:
        mask = lvf.mask.detail_mask_neo(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(mask)

    def test_halo_mask(self) -> None:
        mask = lvf.mask.halo_mask(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(mask)

    def test_range_mask(self) -> None:
        mask = lvf.mask.range_mask(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(mask)

    def test_mt_xxpand_multi(self) -> None:
        masks = lvf.mask.mt_xxpand_multi(self.BLACK_SAMPLE_CLIP)
        self.assertIsInstance(masks, list)

        for mask in masks:
            self.assert_runs(mask)

    def test_BoundingBox(self) -> None:
        mask = lvf.mask.BoundingBox((0, 0), (self.DEF_WIDTH, self.DEF_HEIGHT)).get_mask(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(mask)
        self.assert_same_frame(mask, vsutil.get_y(self.WHITE_SAMPLE_CLIP), 0)  # `get_mask` outputs a GRAY clip


# lvsfunc.misc
class LvsfuncTestMisc(LvsfuncTests):
    def test_source(self) -> None:
        self.output_clip_path.mkdir(parents=True, exist_ok=True)

        self.create_clip(timer=1.5)
        clip = lvf.misc.source(str(self.output_clip_file), force_lsmas=True)

        self.assert_runs(clip)
        self.assert_file_exists(self.output_clip_file_abs)
        self.assert_file_exists(self.output_clip_idx.resolve())

        del clip

        self.clean_output_clip()

    def test_shift_tint(self) -> None:
        clip = lvf.misc.shift_tint(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_limit_dark(self) -> None:
        clip = lvf.misc.limit_dark(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_wipe_row(self) -> None:
        clip = lvf.misc.wipe_row(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_colored_clips(self) -> None:
        clips = lvf.misc.colored_clips(amount=5)
        self.assertIsInstance(clips, list)

        for clip in clips:
            self.assert_runs(clip)

    def test_unsharpen(self) -> None:
        clip = lvf.misc.unsharpen(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)

    def test_overlay_sign(self) -> None:
        input_clip = core.resize.Bicubic(self.YUV420P8_CLIP, width=1920, height=1080,
                                         matrix=1, matrix_in=1,
                                         transfer=1, transfer_in=1,
                                         primaries=1, primaries_in=1)

        clip = lvf.misc.overlay_sign(input_clip, self.PNG_FILE)
        self.assert_runs(clip)


# lvsfunc.recon
class LvsfuncTestRecon(LvsfuncTests):
    def test_chroma_reconstruct(self) -> None:
        clip = lvf.recon.chroma_reconstruct(self.BLACK_SAMPLE_CLIP)
        clip_i444 = lvf.recon.chroma_reconstruct(self.BLACK_SAMPLE_CLIP, i444=True)

        self.assert_runs(clip)
        self.assert_same_format(clip_i444, self.YUV444P8_CLIP)


# lvsfunc.scale
class LvsfuncTestScale(LvsfuncTests):
    # def test_descale(self) -> None:
    #     # Create test clip because it throws an error with any of my generated blank clips???
    #     self.output_clip_path.mkdir(parents=True, exist_ok=True)

    #     self.create_clip(width=self.BIG_WIDTH, height=self.BIG_HEIGHT)
    #     input_clip = lvf.misc.source(str(self.output_clip_file))

    #     clip = lvf.scale.descale(input_clip, width=1280, height=720)
    #     clip_down = lvf.scale.descale(input_clip, width=1280, height=720, upscaler=None)

    #     self.assert_runs(clip)
    #     self.assert_dimensions(clip, self.BIG_WIDTH, self.BIG_HEIGHT)
    #     self.assert_dimensions(clip_down, self.MEDIUM_WIDTH, self.MEDIUM_HEIGHT)

    #     del clip
    #     del clip_down

    #     self.clean_output_clip()

    def test_ssim_downsample(self) -> None:
        clip = lvf.scale.ssim_downsample(self.MEDIUM_SAMPLE_CLIP, height=486)
        self.assert_runs(clip)
        self.assert_dimensions(clip, 864, 486)
        self.assert_same_format(clip, self.YUV420PS_CLIP)


    def test_comparative_descale(self) -> None:
        clip = lvf.scale.comparative_descale(self.BIGGER_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, 1280, 720)

    def test_comparative_restore(self) -> None:
        clip = lvf.scale.comparative_descale(self.BIGGER_SAMPLE_CLIP)
        clip = lvf.scale.comparative_restore(clip, height=self.BIG_HEIGHT)
        self.assert_runs(clip)
        self.assert_dimensions(clip, self.BIG_WIDTH, self.BIG_HEIGHT)


# lvsfunc.util
class LvsfuncTestUtil(LvsfuncTests):
    def test_pick_repair(self) -> None:
        repair = lvf.util.pick_repair(self.YUV420P8_CLIP)
        self.assert_returns_callable(repair)

    def test_pick_removegrain(self) -> None:
        repair = lvf.util.pick_removegrain(self.YUV420P8_CLIP)
        self.assert_returns_callable(repair)

    def test_get_prop(self) -> None:
        prop = lvf.util.get_prop(self.YUV420P8_CLIP.get_frame(0), '_DurationDen', int)
        self.assertIsInstance(prop, int)

    def test_normalize_ranges(self) -> None:
        ranges: List[lvf.types.Range] = [(None, 20), 1, (60, None), -1]
        nranges = lvf.util.normalize_ranges(self.BLACK_SAMPLE_CLIP, ranges)
        self.assertEqual(nranges, [(0, 20), (1, 1), (60, 99), (98, 98)])

    def test_replace_ranges(self) -> None:
        clip_a = lvf.util.replace_ranges(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP, [(0, 1)])
        clip_b = lvf.util.replace_ranges(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP, [(None, None)])
        clip_c = lvf.util.replace_ranges(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP, [(80, None)])
        clip_d = lvf.util.replace_ranges(self.BLACK_SAMPLE_CLIP, self.WHITE_SAMPLE_CLIP, [(80, -1)])

        self.assert_runs(clip_a)
        self.assert_same_frame(clip_a, self.WHITE_SAMPLE_CLIP, 0)
        self.assert_same_frame(clip_b, self.WHITE_SAMPLE_CLIP, 50)
        self.assert_same_frame(clip_c, self.WHITE_SAMPLE_CLIP, 80)
        self.assert_same_frame(clip_d, self.BLACK_SAMPLE_CLIP, 99)

    def test_scale_thresh(self) -> None:
        value_p8 = lvf.util.scale_thresh(thresh=0.5, clip=self.BLACK_SAMPLE_CLIP)
        value_p16 = lvf.util.scale_thresh(thresh=0.5, clip=self.YUV420P16_CLIP)

        self.assertEqual(value_p8, 128)
        self.assertEqual(value_p16, 32768)

        # TODO: Figured out how it works with float?

    def test_scale_peak(self) -> None:
        peak_p16 = lvf.util.scale_peak(value=128, peak=255 << 8)
        peak_ps = lvf.util.scale_peak(value=128, peak=1)

        self.assertEqual(peak_p16, 32768)
        self.assertEqual(round(peak_ps, 2), 0.5)  # Rounding because of float imprecisions

    def test_force_mod(self) -> None:
        value = lvf.util.force_mod(x=150, mod=4)
        self.assertEqual(value, 152)

    def test_clamp_values(self) -> None:
        value_positive = lvf.util.clamp_values(x=500, max_val=255, min_val=0)
        value_negative = lvf.util.clamp_values(x=-500, max_val=255, min_val=0)

        self.assertEqual(value_positive, 255)
        self.assertEqual(value_negative, 0)

    def test_get_neutral_value(self) -> None:
        neutral_p16_yuv = lvf.util.get_neutral_value(self.YUV420P8_CLIP, chroma=True)
        neutral_p16_y = lvf.util.get_neutral_value(self.YUV420P8_CLIP, chroma=False)

        neutral_ps_yuv = lvf.util.get_neutral_value(self.YUV420PS_CLIP, chroma=True)
        neutral_ps_y = lvf.util.get_neutral_value(self.YUV420PS_CLIP, chroma=False)

        self.assertEqual(neutral_p16_yuv, 128)
        self.assertEqual(neutral_p16_y, 128)

        self.assertEqual(neutral_ps_yuv, 0)
        self.assertEqual(neutral_ps_y, 0.5)

    def test_padder(self) -> None:
        clip = lvf.util.padder(self.BLACK_SAMPLE_CLIP)
        self.assert_runs(clip)
        self.assert_dimensions(clip, width=224, height=184)

    def test_get_matrix(self) -> None:
        matrix_rgb = lvf.util.get_matrix(self.RGB24_CLIP)
        matrix_big = lvf.util.get_matrix(self.BIGGER_SAMPLE_CLIP)
        matrix_sml = lvf.util.get_matrix(self.SMALLER_SAMPLE_CLIP)
        matrix_uhd = lvf.util.get_matrix(self.VERYBIG_SAMPLE_CLIP)

        self.assertEqual(matrix_rgb, 0)
        self.assertEqual(matrix_big, 1)
        self.assertEqual(matrix_sml, 5)
        self.assertEqual(matrix_uhd, 9)


_not_implemented: List[str] = [
    'lvsfunc.deblock.autodb_dpir (write_props=True)',
    'lvsfunc.dehardsub.bounded_dehardsub',
    'lvsfunc.dehardsub.get_all_masks',
    'lvsfunc.dehardsub.hardsub_mask',
    'lvsfunc.dehardsub.HardsubASS',
    'lvsfunc.dehardsub.HardsubLine',
    'lvsfunc.dehardsub.HardsubLineFade',
    'lvsfunc.dehardsub.HardsubMask',
    'lvsfunc.dehardsub.HardsubSign',
    'lvsfunc.dehardsub.HardsubSignFade',
    'lvsfunc.dehardsub.HardsubSignKgf',
    'lvsfunc.deinterlace.tivtc_vfr',
    'lvsfunc.mask.DeferredMask',
    'lvsfunc.misc.allow_variable',
    'lvsfunc.misc.chroma_injector',
    'lvsfunc.misc.frames_since_bookmark',
    'lvsfunc.misc.load_bookmarks',
    'lvsfunc.render.clip_async_render',
    'lvsfunc.render.find_scene_changes',
    'lvsfunc.render.finish_frame',
    'lvsfunc.render.get_render_progress',
    'lvsfunc.scale.descale_detail_mask',
    'lvsfunc.scale.descale',
    'lvsfunc.scale.gamma2linear',
    'lvsfunc.scale.linear2gamma',
    'lvsfunc.util.check_variable',
    'lvsfunc.util.get_coefs',
    'lvsfunc.util.quick_resample'
]


if __name__ == '__main__':
    print("\nRunning lvsfunc unit tests..."
          "\n----------------------------------------------------------------------\n",
          "\nThe following functions have not been implemented yet:")

    for f in _not_implemented:
        print("    * ", f)

    print(f"\nTotal unimplemented: {len(_not_implemented)}\n")

    unittest.main(verbosity=2)
    LvsfuncTests().final_cleanup()
