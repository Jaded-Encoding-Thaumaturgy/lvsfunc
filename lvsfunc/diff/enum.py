from __future__ import annotations

from vstools import CustomIntEnum

__all__: list[str] = [
    'DiffMode',
    'VMAFFeature',
    'ButteraugliNorm',
]


class DiffMode(CustomIntEnum):
    """Different supported difference finding methods."""

    ANY = 0
    """Get the difference if any of the methods detect it."""

    ALL = 1
    """Get the difference only if all methods detect it."""

    MAJORITY = 2
    """Get the difference if more than half of the methods detect it."""

    ONE_OR_MORE = 3
    """Get the difference if at least one method detects it."""

    MOST = 4
    """Get the difference if at least 75% of the methods detect it."""

    def check_result(self, results: list[bool]) -> bool:
        """
        Check if the results match the mode requirements.

        :param results:     List of boolean results from different diff methods

        :return:            True if results match the mode requirements, False otherwise
        """

        if not results:
            return False

        total = len(results)
        true_count = sum(results)

        match self:
            case DiffMode.ANY | DiffMode.ONE_OR_MORE:
                return any(results)
            case DiffMode.ALL:
                return all(results)
            case DiffMode.MAJORITY:
                return true_count > total / 2
            case DiffMode.MOST:
                return true_count >= total * 0.75


class VMAFFeature(CustomIntEnum):
    """Different supported VMAF features."""

    ALL = -1
    """Use all features."""

    PSNR = 0
    """Use the PSNR feature."""

    PSNR_HVS = 1
    """Use the PSNR-HVS feature."""

    SSIM = 2
    """Use the SSIM feature."""

    MS_SSIM = 3
    """Use the MS-SSIM feature."""

    CIEDE2000 = 4
    """Use the CIEDE2000 feature."""

    @classmethod
    def _missing_(cls, value: str | int) -> VMAFFeature | None:
        """
        Handle string inputs by mapping them to enum members.

        :param value:   String or integer value to convert
        :return:        Matching enum member or None
        """
        if isinstance(value, str):
            value = value.upper().replace('-', '_')
            try:
                return cls[value]
            except KeyError:
                pass
        return None

    @property
    def prop(self) -> str:
        """Get the property name for the feature."""

        return {
            VMAFFeature.PSNR: 'psnr_y',
            VMAFFeature.PSNR_HVS: 'psnr_hvs',
            VMAFFeature.SSIM: 'float_ssim',
            VMAFFeature.MS_SSIM: 'float_ms_ssim',
            VMAFFeature.CIEDE2000: 'ciede2000',
        }[self]


class ButteraugliNorm(CustomIntEnum):
    """Different supported Butteraugli norms."""

    ALL = -1
    """Use all norms."""

    TWO_NORM = 0
    """Use the 2-norm."""

    THREE_NORM = 1
    """Use the 3-norm."""

    INF_NORM = 2
    """Use the infinity norm."""

    @property
    def prop(self) -> str:
        """Get the property name for the norm."""

        props = {
            ButteraugliNorm.TWO_NORM: '_BUTTERAUGLI_2Norm',
            ButteraugliNorm.THREE_NORM: '_BUTTERAUGLI_3Norm',
            ButteraugliNorm.INF_NORM: '_BUTTERAUGLI_INFNorm',
        }

        if self == ButteraugliNorm.ALL:
            return list(props.values())

        return props[self]
