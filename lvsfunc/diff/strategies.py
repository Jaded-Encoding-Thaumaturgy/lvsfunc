from abc import ABC, abstractmethod

from vskernels import Catrom
from vstools import (CustomRuntimeError, CustomValueError,
                     DependencyNotFoundError, FuncExceptT, Matrix, PlanesT,
                     VSFunction, core, get_prop, merge_clip_props,
                     normalize_planes, vs)

from .enum import ButteraugliNorm, VMAFFeature
from .types import CallbacksT

__all__: list[str] = [
    'PlaneAvgDiff',
    'VMAFDiff',
    'ButteraugliDiff',
]


class DiffStrategy(ABC):
    """Base abstract class for diff strategies."""

    def __init__(
        self,
        threshold: float,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None
    ) -> None:
        """
        Initialize the diff strategy.

        :param threshold:       The threshold to use for the comparison.
        :param planes:          The planes to compare.
        :param func_except:     The function exception to use for the comparison.
        """

        self.threshold = threshold
        self.planes = planes
        self._func_except = func_except or self.__class__.__name__

    @abstractmethod
    def process(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, CallbacksT]:
        """
        Process the difference between two clips.

        :param src:             The source clip to compare.
        :param ref:             The reference clip to compare.

        :return:                A tuple containing the processed clip and callbacks.
        """

        ...


class PlaneAvgDiff(DiffStrategy):
    """Strategy for comparing clips using PlaneAvg."""

    def __init__(
        self,
        threshold: float = 0.005,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None
    ) -> None:
        """
        Initialize the PlaneAvg strategy.

        Dependencies:

            - vapoursynth-zip (https://github.com/dnjulek/vapoursynth-zip)

        :param threshold:       The threshold to use for the comparison.
                                Higher will catch more differences.
        :param planes:          The planes to compare.
        :param func_except:     The function exception to use for the comparison.
        """

        super().__init__(threshold, planes, func_except)
        self._check_vszip_version()

    def process(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, CallbacksT]:
        """Process the difference between two clips using PlaneAvg."""

        self.threshold = max(0, min(1, self.threshold))

        ps_comp = src.vszip.PlaneAverage(
            [0], ref, planes=normalize_planes(src, self.planes), prop='fd_ps'
        )

        def _check_diff(f: vs.VideoFrame) -> bool:
            diff = get_prop(f, 'fd_psDiff', (list, float), default=0)

            if isinstance(diff, float):
                return diff >= self.threshold

            return any(float(x) >= self.threshold for x in diff)

        callbacks = CallbacksT([_check_diff])

        return ps_comp.std.SetFrameProps(fd_thr=self.threshold), callbacks

    def _check_vszip_version(self) -> None:
        if hasattr(core, 'vszip'):
            return

        raise DependencyNotFoundError(
            self._func_except, 'vszip <https://github.com/dnjulek/vapoursynth-zip>',
        )


class VMAFDiff(DiffStrategy):
    """Strategy for comparing clips using VMAF."""

    def __init__(
        self,
        threshold: float = 0.999,
        feature: VMAFFeature | list[VMAFFeature] = VMAFFeature.SSIM,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None
    ) -> None:
        """
        Initialize the VMAF strategy.

        Dependencies:

            - VapourSynth-VMAF (https://github.com/HomeOfVapourSynthEvolution/VapourSynth-VMAF)

        :param threshold:       The threshold to use for the comparison.
                                Lower will catch more differences.
        :param feature:         The VMAF feature(s) to use for comparison.
                                See :py:class:`lvsfunc.diff.enum.VMAFFeature` for more information.
        :param planes:          The planes to compare.
        :param func_except:     The function exception to use for the comparison.
        """

        super().__init__(threshold, planes, func_except)
        self.feature = [feature] if isinstance(feature, VMAFFeature) else feature
        self._check_vmaf_version()

    def process(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, CallbacksT]:
        """Process the difference between two clips using VMAF."""

        self.threshold = max(0, min(1, self.threshold))

        features = [
            f for feature in self.feature
            for f in ([f for f in VMAFFeature if f.value >= 0]
                      if feature == VMAFFeature.ALL else [feature])
        ]

        if not features:
            raise CustomValueError("You must specify at least one VMAF feature!", self.process, self.feature)

        vmaf_clips = [core.vmaf.Metric(src, ref, feature=feature) for feature in features]
        vmaf_clip = merge_clip_props(*vmaf_clips)

        callbacks = CallbacksT(
            [lambda f: get_prop(f, feature.prop, (float, int), default=100)
             <= self.threshold for feature in features]
        )

        return vmaf_clip.std.SetFrameProps(fd_thr=self.threshold), callbacks

    def _check_vmaf_version(self) -> None:
        if hasattr(core, 'vmaf'):
            return

        raise DependencyNotFoundError(
            self._func_except, 'vmaf <https://github.com/HomeOfVapourSynthEvolution/VapourSynth-VMAF>'
        )


class ButteraugliDiff(DiffStrategy):
    """Strategy for comparing clips using Butteraugli."""

    def __init__(
        self,
        threshold: float = 2.0,
        intensity_multiplier: float = 80.0,
        norm_mode: ButteraugliNorm | list[ButteraugliNorm] = ButteraugliNorm.TWO_NORM,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None
    ) -> None:
        """
        Initialize the Butteraugli strategy.

        Dependencies:
            - vship (https://github.com/Line-fr/Vship) (GPU)
            - vapoursynth-julek-plugin (https://github.com/dnjulek/vapoursynth-julek-plugin) (CPU)

        :param threshold:               The threshold to use for the comparison.
                                        Lower will catch more differences.
        :param intensity_multiplier:    Controls sensitivity of the Butteraugli metric.
                                        Higher values make it more sensitive to differences.
        :param norm_mode:               Which norm to use for the comparison.
                                        See :py:class:`lvsfunc.diff.enum.ButteraugliNorm` for more information.
        :param planes:                  The planes to compare.
        :param func_except:             The function exception to use for the comparison.
        """

        super().__init__(threshold, planes, func_except)
        self.intensity_multiplier = intensity_multiplier
        self.norm_mode = norm_mode

        if not isinstance(self.norm_mode, list):
            self.norm_mode = [self.norm_mode]

    def process(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, CallbacksT]:
        """Process the difference between two clips using Butteraugli."""

        plugin, intensity_param = self._get_plugin()

        src_matrix = Matrix.from_video(src)

        # We have to resample to RGB ourselves because the plugin doesn't do it
        if intensity_param == 'intensity_target':
            src, ref = self._to_rgb(src), self._to_rgb(ref)
            self.norm_mode = [ButteraugliNorm.JULEK]
        else:
            self.norm_mode = [x for x in self.norm_mode if x != ButteraugliNorm.JULEK]

            if not self.norm_mode:
                self.norm_mode = [ButteraugliNorm.TWO_NORM]

        ba_clip = plugin(src, ref, **{intensity_param: self.intensity_multiplier})
        props = [norm.prop for norm in self.norm_mode]

        callbacks = CallbacksT([
            lambda f: any(get_prop(f, prop, (float, int), default=0) >= self.threshold for prop in props)
        ])

        # Get the matrix from source back to prevent it from being set to RGB in the return clip
        return src_matrix.apply(ba_clip).std.SetFrameProps(fd_thr=self.threshold), callbacks

    def _get_plugin(self) -> tuple[VSFunction, str]:
        if hasattr(core, 'vship'):
            try:
                core.vship.GpuInfo()
                return core.vship.BUTTERAUGLI, 'intensity_multiplier'
            except vs.Error as e:
                if 'Device' in str(e):
                    if hasattr(core, 'julek'):
                        return core.julek.Butteraugli, 'intensity_target'

                    raise CustomRuntimeError('No GPU detected!', self.process, str(e))

        if hasattr(core, 'julek'):
            return core.julek.Butteraugli, 'intensity_target'

        raise DependencyNotFoundError(
            self._func_except, 'vship <https://github.com/Line-fr/Vship> (GPU) or '
            'vapoursynth-julek-plugin <https://github.com/dnjulek/vapoursynth-julek-plugin> (CPU)',
        )

    def _to_rgb(self, clip: vs.VideoNode) -> vs.VideoNode:
        return Catrom.resample(clip, vs.RGBS, matrix_in=Matrix.from_param_or_video(1, clip))
