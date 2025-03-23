from abc import ABC, abstractmethod

from vstools import (
    DependencyNotFoundError,CustomValueError, FuncExceptT, Matrix, PlanesT, core, get_nvidia_version, get_prop, merge_clip_props,
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
        threshold: float = 1.0,
        intensity_multiplier: float = 80.0,
        norm_mode: ButteraugliNorm | list[ButteraugliNorm] = ButteraugliNorm.TWO_NORM,
        planes: PlanesT = None,
        func_except: FuncExceptT | None = None
    ) -> None:
        """
        Initialize the Butteraugli strategy.

        Dependencies:
            - vship (https://github.com/Line-fr/Vship) (GPU)

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
        self._check_vship_version()

    def process(self, src: vs.VideoNode, ref: vs.VideoNode) -> tuple[vs.VideoNode, CallbacksT]:
        """Process the difference between two clips using Butteraugli."""

        self.threshold = max(0, min(1, self.threshold))

        ba_clip = src.vship.BUTTERAUGLI(ref, intensity_multiplier=self.intensity_multiplier, distmap=0)

        props = (
            [self.norm_mode.prop] if isinstance(self.norm_mode, ButteraugliNorm)
            else [norm.prop for norm in self.norm_mode]
        )

        callbacks = CallbacksT([
            lambda f: any(get_prop(f, prop, (float, int), default=0) >= self.threshold for prop in props)
        ])

        # For some reason it sets Matrix.RGB...
        ba_clip = Matrix.from_video(src).apply(ba_clip)

        return ba_clip.std.SetFrameProps(fd_thr=self.threshold), callbacks

    def _check_vship_version(self) -> None:
        if not get_nvidia_version():
            raise DependencyNotFoundError(
                self._func_except, 'nvidia', 'You must have a NVIDIA GPU to use Butteraugli!'
            )

        if hasattr(core, 'vship'):
            return

        raise DependencyNotFoundError(
            self._func_except, 'vship <https://github.com/Line-fr/Vship>',
        )
