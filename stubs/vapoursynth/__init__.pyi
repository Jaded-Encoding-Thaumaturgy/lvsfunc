# Stop pep8 from complaining (hopefully)
# NOQA

# Ignore Flake Warnings
# flake8: noqa

# Ignore coverage
# (No coverage)

# From https://gist.github.com/pylover/7870c235867cf22817ac5b096defb768
# noinspection PyPep8
# noinspection PyPep8Naming
# noinspection PyTypeChecker
# noinspection PyAbstractClass
# noinspection PyArgumentEqualDefault
# noinspection PyArgumentList
# noinspection PyAssignmentToLoopOrWithParameter
# noinspection PyAttributeOutsideInit
# noinspection PyAugmentAssignment
# noinspection PyBroadException
# noinspection PyByteLiteral
# noinspection PyCallByClass
# noinspection PyChainedComparsons
# noinspection PyClassHasNoInit
# noinspection PyClassicStyleClass
# noinspection PyComparisonWithNone
# noinspection PyCompatibility
# noinspection PyDecorator
# noinspection PyDefaultArgument
# noinspection PyDictCreation
# noinspection PyDictDuplicateKeys
# noinspection PyDocstringTypes
# noinspection PyExceptClausesOrder
# noinspection PyExceptionInheritance
# noinspection PyFromFutureImport
# noinspection PyGlobalUndefined
# noinspection PyIncorrectDocstring
# noinspection PyInitNewSignature
# noinspection PyInterpreter
# noinspection PyListCreation
# noinspection PyMandatoryEncoding
# noinspection PyMethodFirstArgAssignment
# noinspection PyMethodMayBeStatic
# noinspection PyMethodOverriding
# noinspection PyMethodParameters
# noinspection PyMissingConstructor
# noinspection PyMissingOrEmptyDocstring
# noinspection PyNestedDecorators
# noinspection PynonAsciiChar
# noinspection PyNoneFunctionAssignment
# noinspection PyOldStyleClasses
# noinspection PyPackageRequirements
# noinspection PyPropertyAccess
# noinspection PyPropertyDefinition
# noinspection PyProtectedMember
# noinspection PyRaisingNewStyleClass
# noinspection PyRedeclaration
# noinspection PyRedundantParentheses
# noinspection PySetFunctionToLiteral
# noinspection PySimplifyBooleanCheck
# noinspection PySingleQuotedDocstring
# noinspection PyStatementEffect
# noinspection PyStringException
# noinspection PyStringFormat
# noinspection PySuperArguments
# noinspection PyTrailingSemicolon
# noinspection PyTupleAssignmentBalance
# noinspection PyTupleItemAssignment
# noinspection PyUnboundLocalVariable
# noinspection PyUnnecessaryBackslash
# noinspection PyUnreachableCode
# noinspection PyUnresolvedReferences
# noinspection PyUnusedLocal
# noinspection ReturnValueFromInit


from abc import abstractmethod
from ctypes import Structure, c_void_p
from enum import IntEnum
from fractions import Fraction
from inspect import Signature
from types import MappingProxyType, TracebackType
from typing import (TYPE_CHECKING, Any, BinaryIO, Callable, ContextManager,
                    Dict, Generic, Iterator, Literal, MutableMapping,
                    NamedTuple, NoReturn, Optional, Protocol, Sequence, Tuple,
                    Type, TypedDict, TypeVar, Union, overload,
                    runtime_checkable)

__all__ = [
    # Versioning
    '__version__', '__api_version__', 'PluginVersion',

    # Enums and constants
    'MessageType',
        'MESSAGE_TYPE_DEBUG', 'MESSAGE_TYPE_INFORMATION', 'MESSAGE_TYPE_WARNING',
        'MESSAGE_TYPE_CRITICAL', 'MESSAGE_TYPE_FATAL',

    'FilterMode',
        'fmParallel', 'fmParallelRequests', 'fmUnordered', 'fmFrameState',

    'CoreCreationFlags',
        'ccfEnableGraphInspection', 'ccfDisableAutoLoading', 'ccfDisableLibraryUnloading',

    'MediaType',
        'VIDEO', 'AUDIO',

    'ColorFamily',
        'UNDEFINED', 'GRAY', 'RGB', 'YUV',

    'ColorRange',
        'RANGE_FULL', 'RANGE_LIMITED',

    'SampleType',
        'INTEGER', 'FLOAT',

    'PresetFormat',
        'GRAY',
        'GRAY8', 'GRAY9', 'GRAY10', 'GRAY12', 'GRAY14', 'GRAY16', 'GRAY32', 'GRAYH', 'GRAYS',
        'RGB',
        'RGB24', 'RGB27', 'RGB30', 'RGB36', 'RGB42', 'RGB48', 'RGBH', 'RGBS',
        'YUV',
        'YUV410P8',
        'YUV411P8',
        'YUV420P8', 'YUV420P9', 'YUV420P10', 'YUV420P12', 'YUV420P14', 'YUV420P16',
        'YUV422P8', 'YUV422P9', 'YUV422P10', 'YUV422P12', 'YUV422P14', 'YUV422P16',
        'YUV440P8',
        'YUV444P8', 'YUV444P9', 'YUV444P10', 'YUV444P12', 'YUV444P14', 'YUV444P16', 'YUV444PH', 'YUV444PS',
        'NONE',

    'AudioChannels',
        'FRONT_LEFT', 'FRONT_RIGHT', 'FRONT_CENTER',
        'BACK_LEFT', 'BACK_RIGHT', 'BACK_CENTER',
        'SIDE_LEFT', 'SIDE_RIGHT',
        'TOP_CENTER',

        'TOP_FRONT_LEFT', 'TOP_FRONT_RIGHT', 'TOP_FRONT_CENTER',
        'TOP_BACK_LEFT', 'TOP_BACK_RIGHT', 'TOP_BACK_CENTER',

        'WIDE_LEFT', 'WIDE_RIGHT',

        'SURROUND_DIRECT_LEFT', 'SURROUND_DIRECT_RIGHT',

        'FRONT_LEFT_OF_CENTER', 'FRONT_RIGHT_OF_CENTER',

        'STEREO_LEFT', 'STEREO_RIGHT',

        'LOW_FREQUENCY', 'LOW_FREQUENCY2',

    'ChromaLocation',
        'CHROMA_TOP_LEFT', 'CHROMA_TOP',
        'CHROMA_LEFT', 'CHROMA_CENTER',
        'CHROMA_BOTTOM_LEFT', 'CHROMA_BOTTOM',

    'FieldBased',
        'FIELD_PROGRESSIVE', 'FIELD_TOP', 'FIELD_BOTTOM',

    'MatrixCoefficients',
        'MATRIX_RGB', 'MATRIX_BT709', 'MATRIX_UNSPECIFIED', 'MATRIX_FCC',
        'MATRIX_BT470_BG', 'MATRIX_ST170_M', 'MATRIX_YCGCO', 'MATRIX_BT2020_NCL', 'MATRIX_BT2020_CL',
        'MATRIX_CHROMATICITY_DERIVED_NCL', 'MATRIX_CHROMATICITY_DERIVED_CL', 'MATRIX_ICTCP',

    'TransferCharacteristics',
        'TRANSFER_BT709', 'TRANSFER_UNSPECIFIED', 'TRANSFER_BT470_M', 'TRANSFER_BT470_BG', 'TRANSFER_BT601',
        'TRANSFER_ST240_M', 'TRANSFER_LINEAR', 'TRANSFER_LOG_100', 'TRANSFER_LOG_316', 'TRANSFER_IEC_61966_2_4',
        'TRANSFER_IEC_61966_2_1', 'TRANSFER_BT2020_10', 'TRANSFER_BT2020_12', 'TRANSFER_ST2084', 'TRANSFER_ARIB_B67',

    'ColorPrimaries', 'PRIMARIES_BT709', 'PRIMARIES_UNSPECIFIED',
        'PRIMARIES_BT470_M', 'PRIMARIES_BT470_BG', 'PRIMARIES_ST170_M', 'PRIMARIES_ST240_M', 'PRIMARIES_FILM',
        'PRIMARIES_BT2020', 'PRIMARIES_ST428', 'PRIMARIES_ST431_2', 'PRIMARIES_ST432_1', 'PRIMARIES_EBU3213_E',

    # Environment SubSystem
    'Environment', 'EnvironmentData',

    'EnvironmentPolicy',

    'EnvironmentPolicyAPI',
    'register_policy', 'has_policy',
    'register_on_destroy', 'unregister_on_destroy',

    'get_current_environment',

    'VideoOutputTuple',
    'clear_output', 'clear_outputs', 'get_outputs', 'get_output',

    # Logging
    'LogHandle', 'Error',

    # Functions
    'FuncData', 'Func', 'FramePtr',
    'Plugin', 'Function',

    # Formats
    'VideoFormat', 'ChannelLayout',

    # Frames
    'RawFrame', 'VideoFrame', 'AudioFrame',
    'FrameProps',

    # Nodes
    'RawNode', 'VideoNode', 'AudioNode',

    'Core', '_CoreProxy', 'core',

    # Inspection API [UNSTABLE API]
    # '_try_enable_introspection'
]


###
# Typing

T = TypeVar('T')
S = TypeVar('S')

SingleAndSequence = Union[T, Sequence[T]]


@runtime_checkable
class SupportsString(Protocol):
    @abstractmethod
    def __str__(self) -> str:
        ...


DataType = Union[str, bytes, bytearray, SupportsString]

_VapourSynthMapValue = Union[
    SingleAndSequence[int],
    SingleAndSequence[float],
    SingleAndSequence[DataType],
    SingleAndSequence['VideoNode'],
    SingleAndSequence['VideoFrame'],
    SingleAndSequence['AudioNode'],
    SingleAndSequence['AudioFrame'],
    SingleAndSequence['VSMapValueCallback[Any]']
]

BoundVSMapValue = TypeVar('BoundVSMapValue', bound=_VapourSynthMapValue)

VSMapValueCallback = Callable[..., BoundVSMapValue]


class _Future(Generic[T]):
    def set_result(self, value: T) -> None: ...

    def set_exception(self, exception: BaseException) -> None: ...

    def result(self) -> T: ...

    def exception(self) -> Union[NoReturn, None]: ...

###
# Typed dicts


class _VideoFormatInfo(TypedDict):
    id: int
    name: str
    color_family: 'ColorFamily'
    sample_type: 'SampleType'
    bits_per_sample: int
    bytes_per_sample: int
    subsampling_w: int
    subsampling_h: int
    num_planes: int


###
# VapourSynth Versioning


class VapourSynthVersion(NamedTuple):
    release_major: int
    release_minor: int


class VapourSynthAPIVersion(NamedTuple):
    api_major: int
    api_minor: int


__version__: VapourSynthVersion
__api_version__: VapourSynthAPIVersion


###
# Plugin Versioning


class PluginVersion(NamedTuple):
    major: int
    minor: int


###
# VapourSynth Enums and Constants


class MessageType(IntEnum):
    MESSAGE_TYPE_DEBUG: 'MessageType'
    MESSAGE_TYPE_INFORMATION: 'MessageType'
    MESSAGE_TYPE_WARNING: 'MessageType'
    MESSAGE_TYPE_CRITICAL: 'MessageType'
    MESSAGE_TYPE_FATAL: 'MessageType'


MESSAGE_TYPE_DEBUG: Literal[MessageType.MESSAGE_TYPE_DEBUG]
MESSAGE_TYPE_INFORMATION: Literal[MessageType.MESSAGE_TYPE_INFORMATION]
MESSAGE_TYPE_WARNING: Literal[MessageType.MESSAGE_TYPE_WARNING]
MESSAGE_TYPE_CRITICAL: Literal[MessageType.MESSAGE_TYPE_CRITICAL]
MESSAGE_TYPE_FATAL: Literal[MessageType.MESSAGE_TYPE_FATAL]


class FilterMode(IntEnum):
    fmParallel: 'FilterMode'
    fmParallelRequests: 'FilterMode'
    fmUnordered: 'FilterMode'
    fmFrameState: 'FilterMode'


fmParallel: Literal[FilterMode.fmParallel]
fmParallelRequests: Literal[FilterMode.fmParallelRequests]
fmUnordered: Literal[FilterMode.fmUnordered]
fmFrameState: Literal[FilterMode.fmFrameState]


class CoreCreationFlags(IntEnum):
    ccfEnableGraphInspection: 'CoreCreationFlags'
    ccfDisableAutoLoading: 'CoreCreationFlags'
    ccfDisableLibraryUnloading: 'CoreCreationFlags'


ccfEnableGraphInspection: Literal[CoreCreationFlags.ccfEnableGraphInspection]
ccfDisableAutoLoading: Literal[CoreCreationFlags.ccfDisableAutoLoading]
ccfDisableLibraryUnloading: Literal[CoreCreationFlags.ccfDisableLibraryUnloading]


class MediaType(IntEnum):
    VIDEO: 'MediaType'
    AUDIO: 'MediaType'


VIDEO: Literal[MediaType.VIDEO]
AUDIO: Literal[MediaType.AUDIO]


class ColorFamily(IntEnum):
    UNDEFINED: 'ColorFamily'
    GRAY: 'ColorFamily'
    RGB: 'ColorFamily'
    YUV: 'ColorFamily'


UNDEFINED: Literal[ColorFamily.UNDEFINED]
GRAY: Literal[ColorFamily.GRAY]
RGB: Literal[ColorFamily.RGB]
YUV: Literal[ColorFamily.YUV]


class ColorRange(IntEnum):
    RANGE_FULL: 'ColorRange'
    RANGE_LIMITED: 'ColorRange'


RANGE_FULL: Literal[ColorRange.RANGE_FULL]
RANGE_LIMITED: Literal[ColorRange.RANGE_LIMITED]


class SampleType(IntEnum):
    INTEGER: 'SampleType'
    FLOAT: 'SampleType'


INTEGER: Literal[SampleType.INTEGER]
FLOAT: Literal[SampleType.FLOAT]


class PresetFormat(IntEnum):
    NONE: 'PresetFormat'

    GRAY8: 'PresetFormat'
    GRAY9: 'PresetFormat'
    GRAY10: 'PresetFormat'
    GRAY12: 'PresetFormat'
    GRAY14: 'PresetFormat'
    GRAY16: 'PresetFormat'
    GRAY32: 'PresetFormat'

    GRAYH: 'PresetFormat'
    GRAYS: 'PresetFormat'

    YUV420P8: 'PresetFormat'
    YUV422P8: 'PresetFormat'
    YUV444P8: 'PresetFormat'
    YUV410P8: 'PresetFormat'
    YUV411P8: 'PresetFormat'
    YUV440P8: 'PresetFormat'

    YUV420P9: 'PresetFormat'
    YUV422P9: 'PresetFormat'
    YUV444P9: 'PresetFormat'

    YUV420P10: 'PresetFormat'
    YUV422P10: 'PresetFormat'
    YUV444P10: 'PresetFormat'

    YUV420P12: 'PresetFormat'
    YUV422P12: 'PresetFormat'
    YUV444P12: 'PresetFormat'

    YUV420P14: 'PresetFormat'
    YUV422P14: 'PresetFormat'
    YUV444P14: 'PresetFormat'

    YUV420P16: 'PresetFormat'
    YUV422P16: 'PresetFormat'
    YUV444P16: 'PresetFormat'

    YUV444PH: 'PresetFormat'
    YUV444PS: 'PresetFormat'

    RGB24: 'PresetFormat'
    RGB27: 'PresetFormat'
    RGB30: 'PresetFormat'
    RGB36: 'PresetFormat'
    RGB42: 'PresetFormat'
    RGB48: 'PresetFormat'

    RGBH: 'PresetFormat'
    RGBS: 'PresetFormat'


NONE: Literal[PresetFormat.NONE]

GRAY8: Literal[PresetFormat.GRAY8]
GRAY9: Literal[PresetFormat.GRAY9]
GRAY10: Literal[PresetFormat.GRAY10]
GRAY12: Literal[PresetFormat.GRAY12]
GRAY14: Literal[PresetFormat.GRAY14]
GRAY16: Literal[PresetFormat.GRAY16]
GRAY32: Literal[PresetFormat.GRAY32]

GRAYH: Literal[PresetFormat.GRAYH]
GRAYS: Literal[PresetFormat.GRAYS]

YUV420P8: Literal[PresetFormat.YUV420P8]
YUV422P8: Literal[PresetFormat.YUV422P8]
YUV444P8: Literal[PresetFormat.YUV444P8]
YUV410P8: Literal[PresetFormat.YUV410P8]
YUV411P8: Literal[PresetFormat.YUV411P8]
YUV440P8: Literal[PresetFormat.YUV440P8]

YUV420P9: Literal[PresetFormat.YUV420P9]
YUV422P9: Literal[PresetFormat.YUV422P9]
YUV444P9: Literal[PresetFormat.YUV444P9]

YUV420P10: Literal[PresetFormat.YUV420P10]
YUV422P10: Literal[PresetFormat.YUV422P10]
YUV444P10: Literal[PresetFormat.YUV444P10]

YUV420P12: Literal[PresetFormat.YUV420P12]
YUV422P12: Literal[PresetFormat.YUV422P12]
YUV444P12: Literal[PresetFormat.YUV444P12]

YUV420P14: Literal[PresetFormat.YUV420P14]
YUV422P14: Literal[PresetFormat.YUV422P14]
YUV444P14: Literal[PresetFormat.YUV444P14]

YUV420P16: Literal[PresetFormat.YUV420P16]
YUV422P16: Literal[PresetFormat.YUV422P16]
YUV444P16: Literal[PresetFormat.YUV444P16]

YUV444PH: Literal[PresetFormat.YUV444PH]
YUV444PS: Literal[PresetFormat.YUV444PS]

RGB24: Literal[PresetFormat.RGB24]
RGB27: Literal[PresetFormat.RGB27]
RGB30: Literal[PresetFormat.RGB30]
RGB36: Literal[PresetFormat.RGB36]
RGB42: Literal[PresetFormat.RGB42]
RGB48: Literal[PresetFormat.RGB48]

RGBH: Literal[PresetFormat.RGBH]
RGBS: Literal[PresetFormat.RGBS]


class AudioChannels(IntEnum):
    FRONT_LEFT: 'AudioChannels'
    FRONT_RIGHT: 'AudioChannels'
    FRONT_CENTER: 'AudioChannels'
    LOW_FREQUENCY: 'AudioChannels'
    BACK_LEFT: 'AudioChannels'
    BACK_RIGHT: 'AudioChannels'
    FRONT_LEFT_OF_CENTER: 'AudioChannels'
    FRONT_RIGHT_OF_CENTER: 'AudioChannels'
    BACK_CENTER: 'AudioChannels'
    SIDE_LEFT: 'AudioChannels'
    SIDE_RIGHT: 'AudioChannels'
    TOP_CENTER: 'AudioChannels'
    TOP_FRONT_LEFT: 'AudioChannels'
    TOP_FRONT_CENTER: 'AudioChannels'
    TOP_FRONT_RIGHT: 'AudioChannels'
    TOP_BACK_LEFT: 'AudioChannels'
    TOP_BACK_CENTER: 'AudioChannels'
    TOP_BACK_RIGHT: 'AudioChannels'
    STEREO_LEFT: 'AudioChannels'
    STEREO_RIGHT: 'AudioChannels'
    WIDE_LEFT: 'AudioChannels'
    WIDE_RIGHT: 'AudioChannels'
    SURROUND_DIRECT_LEFT: 'AudioChannels'
    SURROUND_DIRECT_RIGHT: 'AudioChannels'
    LOW_FREQUENCY2: 'AudioChannels'


FRONT_LEFT: Literal[AudioChannels.FRONT_LEFT]
FRONT_RIGHT: Literal[AudioChannels.FRONT_RIGHT]
FRONT_CENTER: Literal[AudioChannels.FRONT_CENTER]
LOW_FREQUENCY: Literal[AudioChannels.LOW_FREQUENCY]
BACK_LEFT: Literal[AudioChannels.BACK_LEFT]
BACK_RIGHT: Literal[AudioChannels.BACK_RIGHT]
FRONT_LEFT_OF_CENTER: Literal[AudioChannels.FRONT_LEFT_OF_CENTER]
FRONT_RIGHT_OF_CENTER: Literal[AudioChannels.FRONT_RIGHT_OF_CENTER]
BACK_CENTER: Literal[AudioChannels.BACK_CENTER]
SIDE_LEFT: Literal[AudioChannels.SIDE_LEFT]
SIDE_RIGHT: Literal[AudioChannels.SIDE_RIGHT]
TOP_CENTER: Literal[AudioChannels.TOP_CENTER]
TOP_FRONT_LEFT: Literal[AudioChannels.TOP_FRONT_LEFT]
TOP_FRONT_CENTER: Literal[AudioChannels.TOP_FRONT_CENTER]
TOP_FRONT_RIGHT: Literal[AudioChannels.TOP_FRONT_RIGHT]
TOP_BACK_LEFT: Literal[AudioChannels.TOP_BACK_LEFT]
TOP_BACK_CENTER: Literal[AudioChannels.TOP_BACK_CENTER]
TOP_BACK_RIGHT: Literal[AudioChannels.TOP_BACK_RIGHT]
STEREO_LEFT: Literal[AudioChannels.STEREO_LEFT]
STEREO_RIGHT: Literal[AudioChannels.STEREO_RIGHT]
WIDE_LEFT: Literal[AudioChannels.WIDE_LEFT]
WIDE_RIGHT: Literal[AudioChannels.WIDE_RIGHT]
SURROUND_DIRECT_LEFT: Literal[AudioChannels.SURROUND_DIRECT_LEFT]
SURROUND_DIRECT_RIGHT: Literal[AudioChannels.SURROUND_DIRECT_RIGHT]
LOW_FREQUENCY2: Literal[AudioChannels.LOW_FREQUENCY2]


class ChromaLocation(IntEnum):
    CHROMA_LEFT: 'ChromaLocation'
    CHROMA_CENTER: 'ChromaLocation'
    CHROMA_TOP_LEFT: 'ChromaLocation'
    CHROMA_TOP: 'ChromaLocation'
    CHROMA_BOTTOM_LEFT: 'ChromaLocation'
    CHROMA_BOTTOM: 'ChromaLocation'


CHROMA_LEFT: Literal[ChromaLocation.CHROMA_LEFT]
CHROMA_CENTER: Literal[ChromaLocation.CHROMA_CENTER]
CHROMA_TOP_LEFT: Literal[ChromaLocation.CHROMA_TOP_LEFT]
CHROMA_TOP: Literal[ChromaLocation.CHROMA_TOP]
CHROMA_BOTTOM_LEFT: Literal[ChromaLocation.CHROMA_BOTTOM_LEFT]
CHROMA_BOTTOM: Literal[ChromaLocation.CHROMA_BOTTOM]


class FieldBased(IntEnum):
    FIELD_PROGRESSIVE: 'FieldBased'
    FIELD_TOP: 'FieldBased'
    FIELD_BOTTOM: 'FieldBased'


FIELD_PROGRESSIVE: Literal[FieldBased.FIELD_PROGRESSIVE]
FIELD_TOP: Literal[FieldBased.FIELD_TOP]
FIELD_BOTTOM: Literal[FieldBased.FIELD_BOTTOM]


class MatrixCoefficients(IntEnum):
    MATRIX_RGB: 'MatrixCoefficients'
    MATRIX_BT709: 'MatrixCoefficients'
    MATRIX_UNSPECIFIED: 'MatrixCoefficients'
    MATRIX_FCC: 'MatrixCoefficients'
    MATRIX_BT470_BG: 'MatrixCoefficients'
    MATRIX_ST170_M: 'MatrixCoefficients'
    MATRIX_YCGCO: 'MatrixCoefficients'
    MATRIX_BT2020_NCL: 'MatrixCoefficients'
    MATRIX_BT2020_CL: 'MatrixCoefficients'
    MATRIX_CHROMATICITY_DERIVED_NCL: 'MatrixCoefficients'
    MATRIX_CHROMATICITY_DERIVED_CL: 'MatrixCoefficients'
    MATRIX_ICTCP: 'MatrixCoefficients'


MATRIX_RGB: Literal[MatrixCoefficients.MATRIX_RGB]
MATRIX_BT709: Literal[MatrixCoefficients.MATRIX_BT709]
MATRIX_UNSPECIFIED: Literal[MatrixCoefficients.MATRIX_UNSPECIFIED]
MATRIX_FCC: Literal[MatrixCoefficients.MATRIX_FCC]
MATRIX_BT470_BG: Literal[MatrixCoefficients.MATRIX_BT470_BG]
MATRIX_ST170_M: Literal[MatrixCoefficients.MATRIX_ST170_M]
MATRIX_YCGCO: Literal[MatrixCoefficients.MATRIX_YCGCO]
MATRIX_BT2020_NCL: Literal[MatrixCoefficients.MATRIX_BT2020_NCL]
MATRIX_BT2020_CL: Literal[MatrixCoefficients.MATRIX_BT2020_CL]
MATRIX_CHROMATICITY_DERIVED_NCL: Literal[MatrixCoefficients.MATRIX_CHROMATICITY_DERIVED_NCL]
MATRIX_CHROMATICITY_DERIVED_CL: Literal[MatrixCoefficients.MATRIX_CHROMATICITY_DERIVED_CL]
MATRIX_ICTCP: Literal[MatrixCoefficients.MATRIX_ICTCP]


class TransferCharacteristics(IntEnum):
    TRANSFER_BT709: 'TransferCharacteristics'
    TRANSFER_UNSPECIFIED: 'TransferCharacteristics'
    TRANSFER_BT470_M: 'TransferCharacteristics'
    TRANSFER_BT470_BG: 'TransferCharacteristics'
    TRANSFER_BT601: 'TransferCharacteristics'
    TRANSFER_ST240_M: 'TransferCharacteristics'
    TRANSFER_LINEAR: 'TransferCharacteristics'
    TRANSFER_LOG_100: 'TransferCharacteristics'
    TRANSFER_LOG_316: 'TransferCharacteristics'
    TRANSFER_IEC_61966_2_4: 'TransferCharacteristics'
    TRANSFER_IEC_61966_2_1: 'TransferCharacteristics'
    TRANSFER_BT2020_10: 'TransferCharacteristics'
    TRANSFER_BT2020_12: 'TransferCharacteristics'
    TRANSFER_ST2084: 'TransferCharacteristics'
    TRANSFER_ARIB_B67: 'TransferCharacteristics'


TRANSFER_BT709: Literal[TransferCharacteristics.TRANSFER_BT709]
TRANSFER_UNSPECIFIED: Literal[TransferCharacteristics.TRANSFER_UNSPECIFIED]
TRANSFER_BT470_M: Literal[TransferCharacteristics.TRANSFER_BT470_M]
TRANSFER_BT470_BG: Literal[TransferCharacteristics.TRANSFER_BT470_BG]
TRANSFER_BT601: Literal[TransferCharacteristics.TRANSFER_BT601]
TRANSFER_ST240_M: Literal[TransferCharacteristics.TRANSFER_ST240_M]
TRANSFER_LINEAR: Literal[TransferCharacteristics.TRANSFER_LINEAR]
TRANSFER_LOG_100: Literal[TransferCharacteristics.TRANSFER_LOG_100]
TRANSFER_LOG_316: Literal[TransferCharacteristics.TRANSFER_LOG_316]
TRANSFER_IEC_61966_2_4: Literal[TransferCharacteristics.TRANSFER_IEC_61966_2_4]
TRANSFER_IEC_61966_2_1: Literal[TransferCharacteristics.TRANSFER_IEC_61966_2_1]
TRANSFER_BT2020_10: Literal[TransferCharacteristics.TRANSFER_BT2020_10]
TRANSFER_BT2020_12: Literal[TransferCharacteristics.TRANSFER_BT2020_12]
TRANSFER_ST2084: Literal[TransferCharacteristics.TRANSFER_ST2084]
TRANSFER_ARIB_B67: Literal[TransferCharacteristics.TRANSFER_ARIB_B67]


class ColorPrimaries(IntEnum):
    PRIMARIES_BT709: 'ColorPrimaries'
    PRIMARIES_UNSPECIFIED: 'ColorPrimaries'
    PRIMARIES_BT470_M: 'ColorPrimaries'
    PRIMARIES_BT470_BG: 'ColorPrimaries'
    PRIMARIES_ST170_M: 'ColorPrimaries'
    PRIMARIES_ST240_M: 'ColorPrimaries'
    PRIMARIES_FILM: 'ColorPrimaries'
    PRIMARIES_BT2020: 'ColorPrimaries'
    PRIMARIES_ST428: 'ColorPrimaries'
    PRIMARIES_ST431_2: 'ColorPrimaries'
    PRIMARIES_ST432_1: 'ColorPrimaries'
    PRIMARIES_EBU3213_E: 'ColorPrimaries'


PRIMARIES_BT709: Literal[ColorPrimaries.PRIMARIES_BT709]
PRIMARIES_UNSPECIFIED: Literal[ColorPrimaries.PRIMARIES_UNSPECIFIED]
PRIMARIES_BT470_M: Literal[ColorPrimaries.PRIMARIES_BT470_M]
PRIMARIES_BT470_BG: Literal[ColorPrimaries.PRIMARIES_BT470_BG]
PRIMARIES_ST170_M: Literal[ColorPrimaries.PRIMARIES_ST170_M]
PRIMARIES_ST240_M: Literal[ColorPrimaries.PRIMARIES_ST240_M]
PRIMARIES_FILM: Literal[ColorPrimaries.PRIMARIES_FILM]
PRIMARIES_BT2020: Literal[ColorPrimaries.PRIMARIES_BT2020]
PRIMARIES_ST428: Literal[ColorPrimaries.PRIMARIES_ST428]
PRIMARIES_ST431_2: Literal[ColorPrimaries.PRIMARIES_ST431_2]
PRIMARIES_ST432_1: Literal[ColorPrimaries.PRIMARIES_ST432_1]
PRIMARIES_EBU3213_E: Literal[ColorPrimaries.PRIMARIES_EBU3213_E]


###
# VapourSynth Environment SubSystem


class EnvironmentData:
    def __init__(self) -> NoReturn: ...


class EnvironmentPolicy:
    def on_policy_registered(self, special_api: 'EnvironmentPolicyAPI') -> None: ...

    def on_policy_cleared(self) -> None: ...

    @abstractmethod
    def get_current_environment(self) -> Union[EnvironmentData, None]: ...

    @abstractmethod
    def set_environment(self, environment: Union[EnvironmentData, None]) -> Union[EnvironmentData, None]: ...

    def is_alive(self, environment: EnvironmentData) -> bool: ...


class EnvironmentPolicyAPI:
    def __init__(self) -> NoReturn: ...

    def wrap_environment(self, environment_data: EnvironmentData) -> 'Environment': ...

    def create_environment(self, flags: int = 0) -> EnvironmentData: ...

    def set_logger(self, env: EnvironmentData, logger: Callable[[int, str], None]) -> None: ...

    def get_vapoursynth_api(self, version: int) -> c_void_p: ...

    def get_core_ptr(self, environment_data: EnvironmentData) -> c_void_p: ...

    def destroy_environment(self, env: EnvironmentData) -> None: ...

    def unregister_policy(self) -> None: ...


def register_policy(policy: EnvironmentPolicy) -> None:
    ...


if not TYPE_CHECKING:
    def _try_enable_introspection(version: int = None): ...


def has_policy() -> bool:
    ...


def register_on_destroy(callback: Callable[..., None]) -> None:
    ...


def unregister_on_destroy(callback: Callable[..., None]) -> None:
    ...


class Environment:
    env: EnvironmentData

    def __init__(self) -> NoReturn: ...

    @property
    def alive(self) -> bool: ...

    @property
    def single(self) -> bool: ...

    @classmethod
    def is_single(cls) -> bool: ...

    @property
    def env_id(self) -> int: ...

    @property
    def active(self) -> bool: ...

    def copy(self) -> 'Environment': ...

    def use(self) -> ContextManager[None]: ...

    def __eq__(self, other: 'Environment') -> bool: ...  # type: ignore[override]

    def __repr__(self) -> str: ...


def get_current_environment() -> Environment:
    ...


class Local:
    def __getattr__(self, key: str) -> Any: ...

    # Even though object does have set/del methods, typecheckers will treat them differently
    # when they are not explicit; for example by raising a member not found warning.

    def __setattr__(self, key: str, value: Any) -> None: ...

    def __delattr__(self, key: str) -> None: ...


class VideoOutputTuple(NamedTuple):
    clip: 'VideoNode'
    alpha: Union['VideoNode', None]
    alt_output: Literal[0, 1, 2]


class Error(Exception):
    ...


def clear_output(index: int = 0) -> None:
    ...


def clear_outputs() -> None:
    ...


def get_outputs() -> MappingProxyType[int, Union[VideoOutputTuple, 'AudioNode']]:
    ...


def get_output(index: int = 0) -> Union[VideoOutputTuple, 'AudioNode']:
    ...


class FuncData:
    def __init__(self) -> NoReturn: ...

    def __call__(self, **kwargs: _VapourSynthMapValue) -> _VapourSynthMapValue: ...


class Func:
    def __init__(self) -> NoReturn: ...

    def __call__(self, **kwargs: _VapourSynthMapValue) -> _VapourSynthMapValue: ...


class FramePtr:
    def __init__(self) -> NoReturn: ...


class VideoFormat:
    id: int
    name: str
    color_family: ColorFamily
    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    subsampling_w: int
    subsampling_h: int
    num_planes: int

    def __init__(self) -> NoReturn: ...

    def _as_dict(self) -> _VideoFormatInfo: ...

    def replace(
        self, *,
        color_family: Union[ColorFamily, None] = None,
        sample_type: Union[SampleType, None] = None,
        bits_per_sample: Union[int, None] = None,
        subsampling_w: Union[int, None] = None,
        subsampling_h: Union[int, None] = None
    ) -> 'VideoFormat': ...

    @overload
    def __eq__(self, other: 'VideoFormat') -> bool: ...  # type: ignore[misc]

    @overload
    def __eq__(self, other: Any) -> Literal[False]: ...


class FrameProps(MutableMapping[str, _VapourSynthMapValue]):
    def __init__(self) -> NoReturn: ...

    def setdefault(
        self, key: str, default: _VapourSynthMapValue = 0
    ) -> _VapourSynthMapValue: ...

    def copy(self) -> MutableMapping[str, _VapourSynthMapValue]: ...

    # Since we're inheriting from the MutableMapping abstract class,
    # we *have* to specify that we have indeed created these methods.
    # If we don't, mypy will complain that we're working with abstract methods.

    def __setattr__(self, name: str, value: _VapourSynthMapValue) -> None: ...

    def __getattr__(self, name: str) -> _VapourSynthMapValue: ...

    def __delattr__(self, name: str) -> None: ...

    def __setitem__(self, name: str, value: _VapourSynthMapValue) -> None: ...

    def __getitem__(self, name: str) -> _VapourSynthMapValue: ...

    def __delitem__(self, name: str) -> None: ...

    def __iter__(self) -> Iterator[str]: ...

    def __len__(self) -> int: ...


class ChannelLayout(int):
    def __init__(self) -> NoReturn: ...

    def __contains__(self, layout: AudioChannels) -> bool: ...

    def __iter__(self) -> Iterator[AudioChannels]: ...

    @overload
    def __eq__(self, other: 'ChannelLayout') -> bool: ...  # type: ignore[misc]

    @overload
    def __eq__(self, other: Any) -> Literal[False]: ...

    def __len__(self) -> int: ...


class audio_view(memoryview):  # type: ignore[misc]
    @property
    def shape(self) -> tuple[int]: ...

    @property
    def strides(self) -> tuple[int]: ...

    @property
    def ndim(self) -> Literal[1]: ...

    @property
    def obj(self) -> FramePtr: ...  # type: ignore[override]

    def __getitem__(self, index: int) -> int | float: ...  # type: ignore[override]

    def __setitem__(self, index: int, other: int | float) -> None: ...  # type: ignore[override]

    def tolist(self) -> list[int | float]: ...  # type: ignore[override]


class video_view(memoryview):  # type: ignore[misc]
    @property
    def shape(self) -> tuple[int, int]: ...

    @property
    def strides(self) -> tuple[int, int]: ...

    @property
    def ndim(self) -> Literal[2]: ...

    @property
    def obj(self) -> FramePtr: ...  # type: ignore[override]

    def __getitem__(self, index: Tuple[int, int]) -> int | float: ...  # type: ignore[override]

    def __setitem__(self, index: Tuple[int, int], other: int | float) -> None: ...  # type: ignore[override]

    def tolist(self) -> list[int | float]: ...  # type: ignore[override]


class RawFrame:
    def __init__(self) -> NoReturn: ...

    @property
    def closed(self) -> bool: ...

    def close(self) -> None: ...

    def copy(self: 'SelfFrame') -> 'SelfFrame': ...

    @property
    def props(self) -> FrameProps: ...

    @props.setter
    def props(self, new_props: MappingProxyType[str, _VapourSynthMapValue]) -> None: ...

    def get_write_ptr(self, plane: int) -> c_void_p: ...

    def get_read_ptr(self, plane: int) -> c_void_p: ...

    def get_stride(self, plane: int) -> int: ...

    @property
    def readonly(self) -> bool: ...

    def __enter__(self: 'SelfFrame') -> 'SelfFrame': ...

    def __exit__(
        self, exc_type: Union[Type[BaseException], None],
        exc_value: Union[BaseException, None],
        traceback: Union[TracebackType, None],
    ) -> Union[bool, None]: ...

    def __getitem__(self, index: int) -> memoryview: ...

    def __len__(self) -> int: ...


SelfFrame = TypeVar('SelfFrame', bound=RawFrame)


class VideoFrame(RawFrame):
    format: VideoFormat
    width: int
    height: int

    def readchunks(self) -> Iterator[video_view]: ...

    def __getitem__(self, index: int) -> video_view: ...


class AudioFrame(RawFrame):
    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    channel_layout: int
    num_channels: int

    @property
    def channels(self) -> ChannelLayout: ...

    def __getitem__(self, index: int) -> audio_view: ...


# implementation: adg

class _Plugin_adg_Core_Bound(Plugin):
    """This class implements the module definitions for the "adg" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Mask(self, clip: 'VideoNode', luma_scaling: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_adg_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "adg" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Mask(self, luma_scaling: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: akarin

class _Plugin_akarin_Core_Bound(Plugin):
    """This class implements the module definitions for the "akarin" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Cambi(self, clip: 'VideoNode', window_size: Optional[int] = None, topk: Optional[float] = None, tvi_threshold: Optional[float] = None, scores: Optional[int] = None, scaling: Optional[float] = None) -> 'VideoNode': ...
    def DLISR(self, clip: 'VideoNode', scale: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...
    def DLVFX(self, clip: 'VideoNode', op: int, scale: Optional[float] = None, strength: Optional[float] = None, output_depth: Optional[int] = None, num_streams: Optional[int] = None, model_dir: Optional[DataType] = None) -> 'VideoNode': ...
    def Expr(self, clips: SingleAndSequence['VideoNode'], expr: SingleAndSequence[DataType], format: Optional[int] = None, opt: Optional[int] = None, boundary: Optional[int] = None) -> 'VideoNode': ...
    def PropExpr(self, clips: SingleAndSequence['VideoNode'], dict: VSMapValueCallback[_VapourSynthMapValue]) -> 'VideoNode': ...
    def Select(self, clip_src: SingleAndSequence['VideoNode'], prop_src: SingleAndSequence['VideoNode'], expr: SingleAndSequence[DataType]) -> 'VideoNode': ...
    def Text(self, clips: SingleAndSequence['VideoNode'], text: DataType, alignment: Optional[int] = None, scale: Optional[int] = None, prop: Optional[DataType] = None, strict: Optional[int] = None, vspipe: Optional[int] = None) -> 'VideoNode': ...
    def Tmpl(self, clips: SingleAndSequence['VideoNode'], prop: SingleAndSequence[DataType], text: SingleAndSequence[DataType]) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_akarin_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "akarin" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Cambi(self, window_size: Optional[int] = None, topk: Optional[float] = None, tvi_threshold: Optional[float] = None, scores: Optional[int] = None, scaling: Optional[float] = None) -> 'VideoNode': ...
    def DLISR(self, scale: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...
    def DLVFX(self, op: int, scale: Optional[float] = None, strength: Optional[float] = None, output_depth: Optional[int] = None, num_streams: Optional[int] = None, model_dir: Optional[DataType] = None) -> 'VideoNode': ...
    def Expr(self, expr: SingleAndSequence[DataType], format: Optional[int] = None, opt: Optional[int] = None, boundary: Optional[int] = None) -> 'VideoNode': ...
    def PropExpr(self, dict: VSMapValueCallback[_VapourSynthMapValue]) -> 'VideoNode': ...
    def Select(self, prop_src: SingleAndSequence['VideoNode'], expr: SingleAndSequence[DataType]) -> 'VideoNode': ...
    def Text(self, text: DataType, alignment: Optional[int] = None, scale: Optional[int] = None, prop: Optional[DataType] = None, strict: Optional[int] = None, vspipe: Optional[int] = None) -> 'VideoNode': ...
    def Tmpl(self, prop: SingleAndSequence[DataType], text: SingleAndSequence[DataType]) -> 'VideoNode': ...

# end implementation


# implementation: assrender

class _Plugin_assrender_Core_Bound(Plugin):
    """This class implements the module definitions for the "assrender" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def FrameProp(self, clip: 'VideoNode', prop: Optional[DataType] = None, style: Optional[DataType] = None, vfr: Optional[DataType] = None, hinting: Optional[int] = None, scale: Optional[float] = None, line_spacing: Optional[float] = None, frame_width: Optional[int] = None, frame_height: Optional[int] = None, dar: Optional[float] = None, sar: Optional[float] = None, set_default_storage_size: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None, left: Optional[int] = None, right: Optional[int] = None, charset: Optional[DataType] = None, debuglevel: Optional[int] = None, fontdir: Optional[DataType] = None, srt_font: Optional[DataType] = None, colorspace: Optional[DataType] = None) -> 'VideoNode': ...
    def Subtitle(self, clip: 'VideoNode', text: SingleAndSequence[DataType], style: Optional[DataType] = None, start: Optional[SingleAndSequence[int]] = None, end: Optional[SingleAndSequence[int]] = None, vfr: Optional[DataType] = None, hinting: Optional[int] = None, scale: Optional[float] = None, line_spacing: Optional[float] = None, frame_width: Optional[int] = None, frame_height: Optional[int] = None, dar: Optional[float] = None, sar: Optional[float] = None, set_default_storage_size: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None, left: Optional[int] = None, right: Optional[int] = None, charset: Optional[DataType] = None, debuglevel: Optional[int] = None, fontdir: Optional[DataType] = None, srt_font: Optional[DataType] = None, colorspace: Optional[DataType] = None) -> 'VideoNode': ...
    def TextSub(self, clip: 'VideoNode', file: DataType, vfr: Optional[DataType] = None, hinting: Optional[int] = None, scale: Optional[float] = None, line_spacing: Optional[float] = None, frame_width: Optional[int] = None, frame_height: Optional[int] = None, dar: Optional[float] = None, sar: Optional[float] = None, set_default_storage_size: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None, left: Optional[int] = None, right: Optional[int] = None, charset: Optional[DataType] = None, debuglevel: Optional[int] = None, fontdir: Optional[DataType] = None, srt_font: Optional[DataType] = None, colorspace: Optional[DataType] = None) -> 'VideoNode': ...

class _Plugin_assrender_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "assrender" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def FrameProp(self, prop: Optional[DataType] = None, style: Optional[DataType] = None, vfr: Optional[DataType] = None, hinting: Optional[int] = None, scale: Optional[float] = None, line_spacing: Optional[float] = None, frame_width: Optional[int] = None, frame_height: Optional[int] = None, dar: Optional[float] = None, sar: Optional[float] = None, set_default_storage_size: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None, left: Optional[int] = None, right: Optional[int] = None, charset: Optional[DataType] = None, debuglevel: Optional[int] = None, fontdir: Optional[DataType] = None, srt_font: Optional[DataType] = None, colorspace: Optional[DataType] = None) -> 'VideoNode': ...
    def Subtitle(self, text: SingleAndSequence[DataType], style: Optional[DataType] = None, start: Optional[SingleAndSequence[int]] = None, end: Optional[SingleAndSequence[int]] = None, vfr: Optional[DataType] = None, hinting: Optional[int] = None, scale: Optional[float] = None, line_spacing: Optional[float] = None, frame_width: Optional[int] = None, frame_height: Optional[int] = None, dar: Optional[float] = None, sar: Optional[float] = None, set_default_storage_size: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None, left: Optional[int] = None, right: Optional[int] = None, charset: Optional[DataType] = None, debuglevel: Optional[int] = None, fontdir: Optional[DataType] = None, srt_font: Optional[DataType] = None, colorspace: Optional[DataType] = None) -> 'VideoNode': ...
    def TextSub(self, file: DataType, vfr: Optional[DataType] = None, hinting: Optional[int] = None, scale: Optional[float] = None, line_spacing: Optional[float] = None, frame_width: Optional[int] = None, frame_height: Optional[int] = None, dar: Optional[float] = None, sar: Optional[float] = None, set_default_storage_size: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None, left: Optional[int] = None, right: Optional[int] = None, charset: Optional[DataType] = None, debuglevel: Optional[int] = None, fontdir: Optional[DataType] = None, srt_font: Optional[DataType] = None, colorspace: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation


# implementation: average

class _Plugin_average_Core_Bound(Plugin):
    """This class implements the module definitions for the "average" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Mean(self, clips: Optional[SingleAndSequence[VideoNode]] = None, preset: Optional[int] = None, discard: Optional[int] = None) -> 'VideoNode': ...
    def Median(self, clips: Optional[SingleAndSequence[VideoNode]] = None) -> 'VideoNode': ...

class _Plugin_average_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "average" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Mean(self, preset: Optional[int] = None, discard: Optional[int] = None) -> 'VideoNode': ...
    def Median(self) -> 'VideoNode': ...

# end implementation


# implementation: avs

class _Plugin_avs_Core_Bound(Plugin):
    """This class implements the module definitions for the "avs" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def LoadPlugin(self, path: DataType) -> None: ...

# end implementation


# implementation: bas

class _Plugin_bas_Core_Bound(Plugin):
    """This class implements the module definitions for the "bas" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Source(self, source: DataType, track: Optional[int] = None, adjustdelay: Optional[int] = None, exactsamples: Optional[int] = None, enable_drefs: Optional[int] = None, use_absolute_path: Optional[int] = None, drc_scale: Optional[float] = None) -> 'AudioNode': ...

# end implementation


# implementation: bilateral

class _Plugin_bilateral_Core_Bound(Plugin):
    """This class implements the module definitions for the "bilateral" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Bilateral(self, input: 'VideoNode', ref: Optional['VideoNode'] = None, sigmaS: Optional[SingleAndSequence[float]] = None, sigmaR: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None, algorithm: Optional[SingleAndSequence[int]] = None, PBFICnum: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Gaussian(self, input: 'VideoNode', sigma: Optional[SingleAndSequence[float]] = None, sigmaV: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...

class _Plugin_bilateral_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "bilateral" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Bilateral(self, ref: Optional['VideoNode'] = None, sigmaS: Optional[SingleAndSequence[float]] = None, sigmaR: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None, algorithm: Optional[SingleAndSequence[int]] = None, PBFICnum: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Gaussian(self, sigma: Optional[SingleAndSequence[float]] = None, sigmaV: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...

# end implementation


# implementation: bilateralgpu

class _Plugin_bilateralgpu_Core_Bound(Plugin):
    """This class implements the module definitions for the "bilateralgpu" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Bilateral(self, clip: 'VideoNode', sigma_spatial: Optional[SingleAndSequence[float]] = None, sigma_color: Optional[SingleAndSequence[float]] = None, radius: Optional[SingleAndSequence[int]] = None, device_id: Optional[int] = None, num_streams: Optional[int] = None, use_shared_memory: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_bilateralgpu_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "bilateralgpu" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Bilateral(self, sigma_spatial: Optional[SingleAndSequence[float]] = None, sigma_color: Optional[SingleAndSequence[float]] = None, radius: Optional[SingleAndSequence[int]] = None, device_id: Optional[int] = None, num_streams: Optional[int] = None, use_shared_memory: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: bm3d

class _Plugin_bm3d_Core_Bound(Plugin):
    """This class implements the module definitions for the "bm3d" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Basic(self, input: 'VideoNode', ref: Optional['VideoNode'] = None, profile: Optional[DataType] = None, sigma: Optional[SingleAndSequence[float]] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, bm_step: Optional[int] = None, th_mse: Optional[float] = None, hard_thr: Optional[float] = None, matrix: Optional[int] = None) -> 'VideoNode': ...
    def Final(self, input: 'VideoNode', ref: 'VideoNode', profile: Optional[DataType] = None, sigma: Optional[SingleAndSequence[float]] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, bm_step: Optional[int] = None, th_mse: Optional[float] = None, matrix: Optional[int] = None) -> 'VideoNode': ...
    def OPP2RGB(self, input: 'VideoNode', sample: Optional[int] = None) -> 'VideoNode': ...
    def RGB2OPP(self, input: 'VideoNode', sample: Optional[int] = None) -> 'VideoNode': ...
    def VAggregate(self, input: 'VideoNode', radius: Optional[int] = None, sample: Optional[int] = None) -> 'VideoNode': ...
    def VBasic(self, input: 'VideoNode', ref: Optional['VideoNode'] = None, profile: Optional[DataType] = None, sigma: Optional[SingleAndSequence[float]] = None, radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, bm_step: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, ps_step: Optional[int] = None, th_mse: Optional[float] = None, hard_thr: Optional[float] = None, matrix: Optional[int] = None) -> 'VideoNode': ...
    def VFinal(self, input: 'VideoNode', ref: 'VideoNode', profile: Optional[DataType] = None, sigma: Optional[SingleAndSequence[float]] = None, radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, bm_step: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, ps_step: Optional[int] = None, th_mse: Optional[float] = None, matrix: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_bm3d_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "bm3d" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Basic(self, ref: Optional['VideoNode'] = None, profile: Optional[DataType] = None, sigma: Optional[SingleAndSequence[float]] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, bm_step: Optional[int] = None, th_mse: Optional[float] = None, hard_thr: Optional[float] = None, matrix: Optional[int] = None) -> 'VideoNode': ...
    def Final(self, ref: 'VideoNode', profile: Optional[DataType] = None, sigma: Optional[SingleAndSequence[float]] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, bm_step: Optional[int] = None, th_mse: Optional[float] = None, matrix: Optional[int] = None) -> 'VideoNode': ...
    def OPP2RGB(self, sample: Optional[int] = None) -> 'VideoNode': ...
    def RGB2OPP(self, sample: Optional[int] = None) -> 'VideoNode': ...
    def VAggregate(self, radius: Optional[int] = None, sample: Optional[int] = None) -> 'VideoNode': ...
    def VBasic(self, ref: Optional['VideoNode'] = None, profile: Optional[DataType] = None, sigma: Optional[SingleAndSequence[float]] = None, radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, bm_step: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, ps_step: Optional[int] = None, th_mse: Optional[float] = None, hard_thr: Optional[float] = None, matrix: Optional[int] = None) -> 'VideoNode': ...
    def VFinal(self, ref: 'VideoNode', profile: Optional[DataType] = None, sigma: Optional[SingleAndSequence[float]] = None, radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, bm_step: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, ps_step: Optional[int] = None, th_mse: Optional[float] = None, matrix: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: bm3dcpu

class _Plugin_bm3dcpu_Core_Bound(Plugin):
    """This class implements the module definitions for the "bm3dcpu" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def BM3D(self, clip: 'VideoNode', ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, chroma: Optional[int] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def BM3Dv2(self, clip: 'VideoNode', ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, chroma: Optional[int] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def VAggregate(self, clip: 'VideoNode', src: 'VideoNode', planes: SingleAndSequence[int]) -> 'VideoNode': ...

class _Plugin_bm3dcpu_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "bm3dcpu" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def BM3D(self, ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, chroma: Optional[int] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def BM3Dv2(self, ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, chroma: Optional[int] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def VAggregate(self, src: 'VideoNode', planes: SingleAndSequence[int]) -> 'VideoNode': ...

# end implementation


# implementation: bm3dcuda

class _Plugin_bm3dcuda_Core_Bound(Plugin):
    """This class implements the module definitions for the "bm3dcuda" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def BM3D(self, clip: 'VideoNode', ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[SingleAndSequence[int]] = None, ps_range: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, device_id: Optional[int] = None, fast: Optional[int] = None, extractor_exp: Optional[int] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def BM3Dv2(self, clip: 'VideoNode', ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[SingleAndSequence[int]] = None, ps_range: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, device_id: Optional[int] = None, fast: Optional[int] = None, extractor_exp: Optional[int] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def VAggregate(self, clip: 'VideoNode', src: 'VideoNode', planes: SingleAndSequence[int]) -> 'VideoNode': ...

class _Plugin_bm3dcuda_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "bm3dcuda" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def BM3D(self, ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[SingleAndSequence[int]] = None, ps_range: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, device_id: Optional[int] = None, fast: Optional[int] = None, extractor_exp: Optional[int] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def BM3Dv2(self, ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[SingleAndSequence[int]] = None, ps_range: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, device_id: Optional[int] = None, fast: Optional[int] = None, extractor_exp: Optional[int] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def VAggregate(self, src: 'VideoNode', planes: SingleAndSequence[int]) -> 'VideoNode': ...

# end implementation


# implementation: bm3dcuda_rtc

class _Plugin_bm3dcuda_rtc_Core_Bound(Plugin):
    """This class implements the module definitions for the "bm3dcuda_rtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def BM3D(self, clip: 'VideoNode', ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[SingleAndSequence[int]] = None, ps_range: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, device_id: Optional[int] = None, fast: Optional[int] = None, extractor_exp: Optional[int] = None, bm_error_s: Optional[SingleAndSequence[DataType]] = None, transform_2d_s: Optional[SingleAndSequence[DataType]] = None, transform_1d_s: Optional[SingleAndSequence[DataType]] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def BM3Dv2(self, clip: 'VideoNode', ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[SingleAndSequence[int]] = None, ps_range: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, device_id: Optional[int] = None, fast: Optional[int] = None, extractor_exp: Optional[int] = None, bm_error_s: Optional[SingleAndSequence[DataType]] = None, transform_2d_s: Optional[SingleAndSequence[DataType]] = None, transform_1d_s: Optional[SingleAndSequence[DataType]] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def VAggregate(self, clip: 'VideoNode', src: 'VideoNode', planes: SingleAndSequence[int]) -> 'VideoNode': ...

class _Plugin_bm3dcuda_rtc_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "bm3dcuda_rtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def BM3D(self, ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[SingleAndSequence[int]] = None, ps_range: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, device_id: Optional[int] = None, fast: Optional[int] = None, extractor_exp: Optional[int] = None, bm_error_s: Optional[SingleAndSequence[DataType]] = None, transform_2d_s: Optional[SingleAndSequence[DataType]] = None, transform_1d_s: Optional[SingleAndSequence[DataType]] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def BM3Dv2(self, ref: Optional['VideoNode'] = None, sigma: Optional[SingleAndSequence[float]] = None, block_step: Optional[SingleAndSequence[int]] = None, bm_range: Optional[SingleAndSequence[int]] = None, radius: Optional[int] = None, ps_num: Optional[SingleAndSequence[int]] = None, ps_range: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, device_id: Optional[int] = None, fast: Optional[int] = None, extractor_exp: Optional[int] = None, bm_error_s: Optional[SingleAndSequence[DataType]] = None, transform_2d_s: Optional[SingleAndSequence[DataType]] = None, transform_1d_s: Optional[SingleAndSequence[DataType]] = None, zero_init: Optional[int] = None) -> 'VideoNode': ...
    def VAggregate(self, src: 'VideoNode', planes: SingleAndSequence[int]) -> 'VideoNode': ...

# end implementation


# implementation: box

class _Plugin_box_Core_Bound(Plugin):
    """This class implements the module definitions for the "box" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Blur(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, hradius: Optional[int] = None, hpasses: Optional[int] = None, vradius: Optional[int] = None, vpasses: Optional[int] = None) -> 'VideoNode': ...
    def BlurV(self, clip: 'VideoNode', radius: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_box_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "box" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Blur(self, planes: Optional[SingleAndSequence[int]] = None, hradius: Optional[int] = None, hpasses: Optional[int] = None, vradius: Optional[int] = None, vpasses: Optional[int] = None) -> 'VideoNode': ...
    def BlurV(self, radius: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: bs

class _Plugin_bs_Core_Bound(Plugin):
    """This class implements the module definitions for the "bs" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def AudioSource(self, source: DataType, track: Optional[int] = None, adjustdelay: Optional[int] = None, exact: Optional[int] = None, enable_drefs: Optional[int] = None, use_absolute_path: Optional[int] = None, drc_scale: Optional[float] = None, cachepath: Optional[DataType] = None) -> 'AudioNode': ...
    def VideoSource(self, source: DataType, track: Optional[int] = None, variableformat: Optional[int] = None, threads: Optional[int] = None, seekpreroll: Optional[int] = None, exact: Optional[int] = None, enable_drefs: Optional[int] = None, use_absolute_path: Optional[int] = None, cachepath: Optional[DataType] = None, hwdevice: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation


# implementation: butteraugli

class _Plugin_butteraugli_Core_Bound(Plugin):
    """This class implements the module definitions for the "butteraugli" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def butteraugli(self, clipa: 'VideoNode', clipb: 'VideoNode', heatmap: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_butteraugli_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "butteraugli" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def butteraugli(self, clipb: 'VideoNode', heatmap: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: caffe

class _Plugin_caffe_Core_Bound(Plugin):
    """This class implements the module definitions for the "caffe" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Waifu2x(self, clip: 'VideoNode', noise: Optional[int] = None, scale: Optional[int] = None, block_w: Optional[int] = None, block_h: Optional[int] = None, model: Optional[int] = None, cudnn: Optional[int] = None, processor: Optional[int] = None, tta: Optional[int] = None, batch: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_caffe_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "caffe" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Waifu2x(self, noise: Optional[int] = None, scale: Optional[int] = None, block_w: Optional[int] = None, block_h: Optional[int] = None, model: Optional[int] = None, cudnn: Optional[int] = None, processor: Optional[int] = None, tta: Optional[int] = None, batch: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: cas

class _Plugin_cas_Core_Bound(Plugin):
    """This class implements the module definitions for the "cas" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CAS(self, clip: 'VideoNode', sharpness: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_cas_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "cas" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CAS(self, sharpness: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: ccd

class _Plugin_ccd_Core_Bound(Plugin):
    """This class implements the module definitions for the "ccd" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CCD(self, clip: 'VideoNode', threshold: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_ccd_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "ccd" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CCD(self, threshold: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: cf

class _Plugin_cf_Core_Bound(Plugin):
    """This class implements the module definitions for the "cf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ContinuityFixer(self, clip: 'VideoNode', left: Optional[SingleAndSequence[int]] = None, top: Optional[SingleAndSequence[int]] = None, right: Optional[SingleAndSequence[int]] = None, bottom: Optional[SingleAndSequence[int]] = None, radius: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_cf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "cf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ContinuityFixer(self, left: Optional[SingleAndSequence[int]] = None, top: Optional[SingleAndSequence[int]] = None, right: Optional[SingleAndSequence[int]] = None, bottom: Optional[SingleAndSequence[int]] = None, radius: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: chkdr

class _Plugin_chkdr_Core_Bound(Plugin):
    """This class implements the module definitions for the "chkdr" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def grain(self, clip: 'VideoNode', sigma: Optional[float] = None, res: Optional[int] = None, rad: Optional[float] = None, dev: Optional[float] = None, seed: Optional[int] = None, cf: Optional[int] = None, cp: Optional[int] = None, draft: Optional[int] = None, cpuopt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_chkdr_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "chkdr" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def grain(self, sigma: Optional[float] = None, res: Optional[int] = None, rad: Optional[float] = None, dev: Optional[float] = None, seed: Optional[int] = None, cf: Optional[int] = None, cp: Optional[int] = None, draft: Optional[int] = None, cpuopt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: comb

class _Plugin_comb_Core_Bound(Plugin):
    """This class implements the module definitions for the "comb" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CMaskedMerge(self, base: 'VideoNode', alt: 'VideoNode', mask: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def CombMask(self, clip: 'VideoNode', cthresh: Optional[int] = None, mthresh: Optional[int] = None, mi: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_comb_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "comb" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CMaskedMerge(self, alt: 'VideoNode', mask: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def CombMask(self, cthresh: Optional[int] = None, mthresh: Optional[int] = None, mi: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: ctmf

class _Plugin_ctmf_Core_Bound(Plugin):
    """This class implements the module definitions for the "ctmf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CTMF(self, clip: 'VideoNode', radius: Optional[int] = None, memsize: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_ctmf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "ctmf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CTMF(self, radius: Optional[int] = None, memsize: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: d2v

class _Plugin_d2v_Core_Bound(Plugin):
    """This class implements the module definitions for the "d2v" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ApplyRFF(self, clip: 'VideoNode', d2v: DataType) -> 'VideoNode': ...
    def Source(self, input: DataType, threads: Optional[int] = None, nocrop: Optional[int] = None, rff: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_d2v_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "d2v" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ApplyRFF(self, d2v: DataType) -> 'VideoNode': ...

# end implementation


# implementation: dct

class _Plugin_dct_Core_Bound(Plugin):
    """This class implements the module definitions for the "dct" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Filter(self, clip: 'VideoNode', factors: SingleAndSequence[float]) -> 'VideoNode': ...

class _Plugin_dct_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "dct" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Filter(self, factors: SingleAndSequence[float]) -> 'VideoNode': ...

# end implementation


# implementation: dctf

class _Plugin_dctf_Core_Bound(Plugin):
    """This class implements the module definitions for the "dctf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DCTFilter(self, clip: 'VideoNode', factors: SingleAndSequence[float], planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_dctf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "dctf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DCTFilter(self, factors: SingleAndSequence[float], planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: deblock

class _Plugin_deblock_Core_Bound(Plugin):
    """This class implements the module definitions for the "deblock" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Deblock(self, clip: 'VideoNode', quant: Optional[int] = None, aoffset: Optional[int] = None, boffset: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_deblock_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "deblock" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Deblock(self, quant: Optional[int] = None, aoffset: Optional[int] = None, boffset: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: descale

class _Plugin_descale_Core_Bound(Plugin):
    """This class implements the module definitions for the "descale" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Debicubic(self, src: 'VideoNode', width: int, height: int, b: Optional[float] = None, c: Optional[float] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Debilinear(self, src: 'VideoNode', width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Delanczos(self, src: 'VideoNode', width: int, height: int, taps: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Descale(self, src: 'VideoNode', width: int, height: int, kernel: Optional[DataType] = None, custom_kernel: Optional[VSMapValueCallback[_VapourSynthMapValue]] = None, taps: Optional[int] = None, b: Optional[float] = None, c: Optional[float] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Despline16(self, src: 'VideoNode', width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Despline36(self, src: 'VideoNode', width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Despline64(self, src: 'VideoNode', width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_descale_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "descale" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Debicubic(self, width: int, height: int, b: Optional[float] = None, c: Optional[float] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Debilinear(self, width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Delanczos(self, width: int, height: int, taps: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Descale(self, width: int, height: int, kernel: Optional[DataType] = None, custom_kernel: Optional[VSMapValueCallback[_VapourSynthMapValue]] = None, taps: Optional[int] = None, b: Optional[float] = None, c: Optional[float] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Despline16(self, width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Despline36(self, width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Despline64(self, width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, force: Optional[int] = None, force_h: Optional[int] = None, force_v: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: descale_getnative

class _Plugin_descale_getnative_Core_Bound(Plugin):
    """This class implements the module definitions for the "descale_getnative" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Debicubic(self, src: 'VideoNode', width: int, height: int, b: Optional[float] = None, c: Optional[float] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...
    def Debilinear(self, src: 'VideoNode', width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...
    def Delanczos(self, src: 'VideoNode', width: int, height: int, taps: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...
    def Despline16(self, src: 'VideoNode', width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...
    def Despline36(self, src: 'VideoNode', width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_descale_getnative_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "descale_getnative" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Debicubic(self, width: int, height: int, b: Optional[float] = None, c: Optional[float] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...
    def Debilinear(self, width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...
    def Delanczos(self, width: int, height: int, taps: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...
    def Despline16(self, width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...
    def Despline36(self, width: int, height: int, src_left: Optional[float] = None, src_top: Optional[float] = None, cache_size: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: dfttest

class _Plugin_dfttest_Core_Bound(Plugin):
    """This class implements the module definitions for the "dfttest" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, clip: 'VideoNode', ftype: Optional[int] = None, sigma: Optional[float] = None, sigma2: Optional[float] = None, pmin: Optional[float] = None, pmax: Optional[float] = None, sbsize: Optional[int] = None, smode: Optional[int] = None, sosize: Optional[int] = None, tbsize: Optional[int] = None, tmode: Optional[int] = None, tosize: Optional[int] = None, swin: Optional[int] = None, twin: Optional[int] = None, sbeta: Optional[float] = None, tbeta: Optional[float] = None, zmean: Optional[int] = None, f0beta: Optional[float] = None, nlocation: Optional[SingleAndSequence[int]] = None, alpha: Optional[float] = None, slocation: Optional[SingleAndSequence[float]] = None, ssx: Optional[SingleAndSequence[float]] = None, ssy: Optional[SingleAndSequence[float]] = None, sst: Optional[SingleAndSequence[float]] = None, ssystem: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_dfttest_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "dfttest" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, ftype: Optional[int] = None, sigma: Optional[float] = None, sigma2: Optional[float] = None, pmin: Optional[float] = None, pmax: Optional[float] = None, sbsize: Optional[int] = None, smode: Optional[int] = None, sosize: Optional[int] = None, tbsize: Optional[int] = None, tmode: Optional[int] = None, tosize: Optional[int] = None, swin: Optional[int] = None, twin: Optional[int] = None, sbeta: Optional[float] = None, tbeta: Optional[float] = None, zmean: Optional[int] = None, f0beta: Optional[float] = None, nlocation: Optional[SingleAndSequence[int]] = None, alpha: Optional[float] = None, slocation: Optional[SingleAndSequence[float]] = None, ssx: Optional[SingleAndSequence[float]] = None, ssy: Optional[SingleAndSequence[float]] = None, sst: Optional[SingleAndSequence[float]] = None, ssystem: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: dfttest2_avx2

class _Plugin_dfttest2_avx2_Core_Bound(Plugin):
    """This class implements the module definitions for the "dfttest2_avx2" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, clip: 'VideoNode', window: SingleAndSequence[float], sigma: SingleAndSequence[float], sigma2: float, pmin: float, pmax: float, filter_type: int, radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, zero_mean: Optional[int] = None, window_freq: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def RDFT(self, data: SingleAndSequence[float], shape: SingleAndSequence[int]) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_dfttest2_avx2_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "dfttest2_avx2" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, window: SingleAndSequence[float], sigma: SingleAndSequence[float], sigma2: float, pmin: float, pmax: float, filter_type: int, radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, zero_mean: Optional[int] = None, window_freq: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: dfttest2_cpu

class _Plugin_dfttest2_cpu_Core_Bound(Plugin):
    """This class implements the module definitions for the "dfttest2_cpu" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, clip: 'VideoNode', window: SingleAndSequence[float], sigma: SingleAndSequence[float], sigma2: float, pmin: float, pmax: float, filter_type: int, radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, zero_mean: Optional[int] = None, window_freq: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def RDFT(self, data: SingleAndSequence[float], shape: SingleAndSequence[int]) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_dfttest2_cpu_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "dfttest2_cpu" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, window: SingleAndSequence[float], sigma: SingleAndSequence[float], sigma2: float, pmin: float, pmax: float, filter_type: int, radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, zero_mean: Optional[int] = None, window_freq: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: dfttest2_cuda

class _Plugin_dfttest2_cuda_Core_Bound(Plugin):
    """This class implements the module definitions for the "dfttest2_cuda" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, clip: 'VideoNode', kernel: SingleAndSequence[DataType], radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, in_place: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...
    def RDFT(self, data: SingleAndSequence[float], shape: SingleAndSequence[int]) -> 'VideoNode': ...
    def ToSingle(self, data: SingleAndSequence[float]) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_dfttest2_cuda_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "dfttest2_cuda" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, kernel: SingleAndSequence[DataType], radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, in_place: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: dfttest2_nvrtc

class _Plugin_dfttest2_nvrtc_Core_Bound(Plugin):
    """This class implements the module definitions for the "dfttest2_nvrtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, clip: 'VideoNode', kernel: SingleAndSequence[DataType], radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, in_place: Optional[int] = None, device_id: Optional[int] = None, num_streams: Optional[int] = None) -> 'VideoNode': ...
    def RDFT(self, data: SingleAndSequence[float], shape: SingleAndSequence[int]) -> 'VideoNode': ...
    def ToSingle(self, data: SingleAndSequence[float]) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_dfttest2_nvrtc_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "dfttest2_nvrtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DFTTest(self, kernel: SingleAndSequence[DataType], radius: Optional[int] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, in_place: Optional[int] = None, device_id: Optional[int] = None, num_streams: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: dgdecodenv

class _Plugin_dgdecodenv_Core_Bound(Plugin):
    """This class implements the module definitions for the "dgdecodenv" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DGSource(self, source: DataType, i420: Optional[int] = None, deinterlace: Optional[int] = None, use_top_field: Optional[int] = None, use_pf: Optional[int] = None, ct: Optional[int] = None, cb: Optional[int] = None, cl: Optional[int] = None, cr: Optional[int] = None, rw: Optional[int] = None, rh: Optional[int] = None, fieldop: Optional[int] = None, show: Optional[int] = None, show2: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation


# implementation: dpid

class _Plugin_dpid_Core_Bound(Plugin):
    """This class implements the module definitions for the "dpid" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Dpid(self, clip: 'VideoNode', width: Optional[int] = None, height: Optional[int] = None, lambda_: Optional[SingleAndSequence[float]] = None, src_left: Optional[SingleAndSequence[float]] = None, src_top: Optional[SingleAndSequence[float]] = None, read_chromaloc: Optional[int] = None) -> 'VideoNode': ...
    def DpidRaw(self, clip: 'VideoNode', clip2: 'VideoNode', lambda_: Optional[SingleAndSequence[float]] = None, src_left: Optional[SingleAndSequence[float]] = None, src_top: Optional[SingleAndSequence[float]] = None, read_chromaloc: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_dpid_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "dpid" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Dpid(self, width: Optional[int] = None, height: Optional[int] = None, lambda_: Optional[SingleAndSequence[float]] = None, src_left: Optional[SingleAndSequence[float]] = None, src_top: Optional[SingleAndSequence[float]] = None, read_chromaloc: Optional[int] = None) -> 'VideoNode': ...
    def DpidRaw(self, clip2: 'VideoNode', lambda_: Optional[SingleAndSequence[float]] = None, src_left: Optional[SingleAndSequence[float]] = None, src_top: Optional[SingleAndSequence[float]] = None, read_chromaloc: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: eedi2

class _Plugin_eedi2_Core_Bound(Plugin):
    """This class implements the module definitions for the "eedi2" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def EEDI2(self, clip: 'VideoNode', field: int, mthresh: Optional[int] = None, lthresh: Optional[int] = None, vthresh: Optional[int] = None, estr: Optional[int] = None, dstr: Optional[int] = None, maxd: Optional[int] = None, map: Optional[int] = None, nt: Optional[int] = None, pp: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_eedi2_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "eedi2" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def EEDI2(self, field: int, mthresh: Optional[int] = None, lthresh: Optional[int] = None, vthresh: Optional[int] = None, estr: Optional[int] = None, dstr: Optional[int] = None, maxd: Optional[int] = None, map: Optional[int] = None, nt: Optional[int] = None, pp: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: eedi2cuda

class _Plugin_eedi2cuda_Core_Bound(Plugin):
    """This class implements the module definitions for the "eedi2cuda" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def AA2(self, clip: 'VideoNode', mthresh: Optional[int] = None, lthresh: Optional[int] = None, vthresh: Optional[int] = None, estr: Optional[int] = None, dstr: Optional[int] = None, maxd: Optional[int] = None, map: Optional[int] = None, nt: Optional[int] = None, pp: Optional[int] = None, num_streams: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...
    def BuildConfig(self) -> 'VideoNode': ...
    def EEDI2(self, clip: 'VideoNode', field: int, mthresh: Optional[int] = None, lthresh: Optional[int] = None, vthresh: Optional[int] = None, estr: Optional[int] = None, dstr: Optional[int] = None, maxd: Optional[int] = None, map: Optional[int] = None, nt: Optional[int] = None, pp: Optional[int] = None, num_streams: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...
    def Enlarge2(self, clip: 'VideoNode', mthresh: Optional[int] = None, lthresh: Optional[int] = None, vthresh: Optional[int] = None, estr: Optional[int] = None, dstr: Optional[int] = None, maxd: Optional[int] = None, map: Optional[int] = None, nt: Optional[int] = None, pp: Optional[int] = None, num_streams: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_eedi2cuda_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "eedi2cuda" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def AA2(self, mthresh: Optional[int] = None, lthresh: Optional[int] = None, vthresh: Optional[int] = None, estr: Optional[int] = None, dstr: Optional[int] = None, maxd: Optional[int] = None, map: Optional[int] = None, nt: Optional[int] = None, pp: Optional[int] = None, num_streams: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...
    def EEDI2(self, field: int, mthresh: Optional[int] = None, lthresh: Optional[int] = None, vthresh: Optional[int] = None, estr: Optional[int] = None, dstr: Optional[int] = None, maxd: Optional[int] = None, map: Optional[int] = None, nt: Optional[int] = None, pp: Optional[int] = None, num_streams: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...
    def Enlarge2(self, mthresh: Optional[int] = None, lthresh: Optional[int] = None, vthresh: Optional[int] = None, estr: Optional[int] = None, dstr: Optional[int] = None, maxd: Optional[int] = None, map: Optional[int] = None, nt: Optional[int] = None, pp: Optional[int] = None, num_streams: Optional[int] = None, device_id: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: eedi3m

class _Plugin_eedi3m_Core_Bound(Plugin):
    """This class implements the module definitions for the "eedi3m" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def EEDI3(self, clip: 'VideoNode', field: int, dh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, alpha: Optional[float] = None, beta: Optional[float] = None, gamma: Optional[float] = None, nrad: Optional[int] = None, mdis: Optional[int] = None, hp: Optional[int] = None, ucubic: Optional[int] = None, cost3: Optional[int] = None, vcheck: Optional[int] = None, vthresh0: Optional[float] = None, vthresh1: Optional[float] = None, vthresh2: Optional[float] = None, sclip: Optional['VideoNode'] = None, mclip: Optional['VideoNode'] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def EEDI3CL(self, clip: 'VideoNode', field: int, dh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, alpha: Optional[float] = None, beta: Optional[float] = None, gamma: Optional[float] = None, nrad: Optional[int] = None, mdis: Optional[int] = None, hp: Optional[int] = None, ucubic: Optional[int] = None, cost3: Optional[int] = None, vcheck: Optional[int] = None, vthresh0: Optional[float] = None, vthresh1: Optional[float] = None, vthresh2: Optional[float] = None, sclip: Optional['VideoNode'] = None, opt: Optional[int] = None, device: Optional[int] = None, list_device: Optional[int] = None, info: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_eedi3m_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "eedi3m" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def EEDI3(self, field: int, dh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, alpha: Optional[float] = None, beta: Optional[float] = None, gamma: Optional[float] = None, nrad: Optional[int] = None, mdis: Optional[int] = None, hp: Optional[int] = None, ucubic: Optional[int] = None, cost3: Optional[int] = None, vcheck: Optional[int] = None, vthresh0: Optional[float] = None, vthresh1: Optional[float] = None, vthresh2: Optional[float] = None, sclip: Optional['VideoNode'] = None, mclip: Optional['VideoNode'] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def EEDI3CL(self, field: int, dh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, alpha: Optional[float] = None, beta: Optional[float] = None, gamma: Optional[float] = None, nrad: Optional[int] = None, mdis: Optional[int] = None, hp: Optional[int] = None, ucubic: Optional[int] = None, cost3: Optional[int] = None, vcheck: Optional[int] = None, vthresh0: Optional[float] = None, vthresh1: Optional[float] = None, vthresh2: Optional[float] = None, sclip: Optional['VideoNode'] = None, opt: Optional[int] = None, device: Optional[int] = None, list_device: Optional[int] = None, info: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: f3kdb

class _Plugin_f3kdb_Core_Bound(Plugin):
    """This class implements the module definitions for the "f3kdb" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Deband(self, clip: 'VideoNode', range: Optional[int] = None, y: Optional[int] = None, cb: Optional[int] = None, cr: Optional[int] = None, grainy: Optional[int] = None, grainc: Optional[int] = None, sample_mode: Optional[int] = None, seed: Optional[int] = None, blur_first: Optional[int] = None, dynamic_grain: Optional[int] = None, opt: Optional[int] = None, dither_algo: Optional[int] = None, keep_tv_range: Optional[int] = None, output_depth: Optional[int] = None, random_algo_ref: Optional[int] = None, random_algo_grain: Optional[int] = None, random_param_ref: Optional[float] = None, random_param_grain: Optional[float] = None, preset: Optional[DataType] = None) -> 'VideoNode': ...

class _Plugin_f3kdb_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "f3kdb" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Deband(self, range: Optional[int] = None, y: Optional[int] = None, cb: Optional[int] = None, cr: Optional[int] = None, grainy: Optional[int] = None, grainc: Optional[int] = None, sample_mode: Optional[int] = None, seed: Optional[int] = None, blur_first: Optional[int] = None, dynamic_grain: Optional[int] = None, opt: Optional[int] = None, dither_algo: Optional[int] = None, keep_tv_range: Optional[int] = None, output_depth: Optional[int] = None, random_algo_ref: Optional[int] = None, random_algo_grain: Optional[int] = None, random_param_ref: Optional[float] = None, random_param_grain: Optional[float] = None, preset: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation


# implementation: ffms2

class _Plugin_ffms2_Core_Bound(Plugin):
    """This class implements the module definitions for the "ffms2" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def GetLogLevel(self) -> 'VideoNode': ...
    def Index(self, source: DataType, cachefile: Optional[DataType] = None, indextracks: Optional[SingleAndSequence[int]] = None, errorhandling: Optional[int] = None, overwrite: Optional[int] = None) -> 'VideoNode': ...
    def SetLogLevel(self, level: int) -> 'VideoNode': ...
    def Source(self, source: DataType, track: Optional[int] = None, cache: Optional[int] = None, cachefile: Optional[DataType] = None, fpsnum: Optional[int] = None, fpsden: Optional[int] = None, threads: Optional[int] = None, timecodes: Optional[DataType] = None, seekmode: Optional[int] = None, width: Optional[int] = None, height: Optional[int] = None, resizer: Optional[DataType] = None, format: Optional[int] = None, alpha: Optional[int] = None) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

# end implementation


# implementation: fft3dfilter

class _Plugin_fft3dfilter_Core_Bound(Plugin):
    """This class implements the module definitions for the "fft3dfilter" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def FFT3DFilter(self, clip: 'VideoNode', sigma: Optional[float] = None, beta: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None, bw: Optional[int] = None, bh: Optional[int] = None, bt: Optional[int] = None, ow: Optional[int] = None, oh: Optional[int] = None, kratio: Optional[float] = None, sharpen: Optional[float] = None, scutoff: Optional[float] = None, svr: Optional[float] = None, smin: Optional[float] = None, smax: Optional[float] = None, measure: Optional[int] = None, interlaced: Optional[int] = None, wintype: Optional[int] = None, pframe: Optional[int] = None, px: Optional[int] = None, py: Optional[int] = None, pshow: Optional[int] = None, pcutoff: Optional[float] = None, pfactor: Optional[float] = None, sigma2: Optional[float] = None, sigma3: Optional[float] = None, sigma4: Optional[float] = None, degrid: Optional[float] = None, dehalo: Optional[float] = None, hr: Optional[float] = None, ht: Optional[float] = None, ncpu: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_fft3dfilter_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "fft3dfilter" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def FFT3DFilter(self, sigma: Optional[float] = None, beta: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None, bw: Optional[int] = None, bh: Optional[int] = None, bt: Optional[int] = None, ow: Optional[int] = None, oh: Optional[int] = None, kratio: Optional[float] = None, sharpen: Optional[float] = None, scutoff: Optional[float] = None, svr: Optional[float] = None, smin: Optional[float] = None, smax: Optional[float] = None, measure: Optional[int] = None, interlaced: Optional[int] = None, wintype: Optional[int] = None, pframe: Optional[int] = None, px: Optional[int] = None, py: Optional[int] = None, pshow: Optional[int] = None, pcutoff: Optional[float] = None, pfactor: Optional[float] = None, sigma2: Optional[float] = None, sigma3: Optional[float] = None, sigma4: Optional[float] = None, degrid: Optional[float] = None, dehalo: Optional[float] = None, hr: Optional[float] = None, ht: Optional[float] = None, ncpu: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: fh

class _Plugin_fh_Core_Bound(Plugin):
    """This class implements the module definitions for the "fh" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def FieldHint(self, clip: 'VideoNode', ovr: Optional[DataType] = None, tff: Optional[int] = None, matches: Optional[DataType] = None) -> 'VideoNode': ...
    def Fieldhint(self, clip: 'VideoNode', ovr: Optional[DataType] = None, tff: Optional[int] = None, matches: Optional[DataType] = None) -> 'VideoNode': ...

class _Plugin_fh_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "fh" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def FieldHint(self, ovr: Optional[DataType] = None, tff: Optional[int] = None, matches: Optional[DataType] = None) -> 'VideoNode': ...
    def Fieldhint(self, ovr: Optional[DataType] = None, tff: Optional[int] = None, matches: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation


# implementation: flux

class _Plugin_flux_Core_Bound(Plugin):
    """This class implements the module definitions for the "flux" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def SmoothST(self, clip: 'VideoNode', temporal_threshold: Optional[int] = None, spatial_threshold: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def SmoothT(self, clip: 'VideoNode', temporal_threshold: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_flux_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "flux" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def SmoothST(self, temporal_threshold: Optional[int] = None, spatial_threshold: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def SmoothT(self, temporal_threshold: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: fmtc

class _Plugin_fmtc_Core_Bound(Plugin):
    """This class implements the module definitions for the "fmtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def bitdepth(self, clip: 'VideoNode', csp: Optional[int] = None, bits: Optional[int] = None, flt: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, dmode: Optional[int] = None, ampo: Optional[float] = None, ampn: Optional[float] = None, dyn: Optional[int] = None, staticnoise: Optional[int] = None, cpuopt: Optional[int] = None, patsize: Optional[int] = None, tpdfo: Optional[int] = None, tpdfn: Optional[int] = None, corplane: Optional[int] = None) -> 'VideoNode': ...
    def histluma(self, clip: 'VideoNode', full: Optional[int] = None, amp: Optional[int] = None) -> 'VideoNode': ...
    def matrix(self, clip: 'VideoNode', mat: Optional[DataType] = None, mats: Optional[DataType] = None, matd: Optional[DataType] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, coef: Optional[SingleAndSequence[float]] = None, csp: Optional[int] = None, col_fam: Optional[int] = None, bits: Optional[int] = None, singleout: Optional[int] = None, cpuopt: Optional[int] = None, planes: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...
    def matrix2020cl(self, clip: 'VideoNode', full: Optional[int] = None, csp: Optional[int] = None, bits: Optional[int] = None, cpuopt: Optional[int] = None) -> 'VideoNode': ...
    def nativetostack16(self, clip: 'VideoNode') -> 'VideoNode': ...
    def primaries(self, clip: 'VideoNode', rs: Optional[SingleAndSequence[float]] = None, gs: Optional[SingleAndSequence[float]] = None, bs: Optional[SingleAndSequence[float]] = None, ws: Optional[SingleAndSequence[float]] = None, rd: Optional[SingleAndSequence[float]] = None, gd: Optional[SingleAndSequence[float]] = None, bd: Optional[SingleAndSequence[float]] = None, wd: Optional[SingleAndSequence[float]] = None, prims: Optional[DataType] = None, primd: Optional[DataType] = None, wconv: Optional[int] = None, cpuopt: Optional[int] = None) -> 'VideoNode': ...
    def resample(self, clip: 'VideoNode', w: Optional[int] = None, h: Optional[int] = None, sx: Optional[SingleAndSequence[float]] = None, sy: Optional[SingleAndSequence[float]] = None, sw: Optional[SingleAndSequence[float]] = None, sh: Optional[SingleAndSequence[float]] = None, scale: Optional[float] = None, scaleh: Optional[float] = None, scalev: Optional[float] = None, kernel: Optional[SingleAndSequence[DataType]] = None, kernelh: Optional[SingleAndSequence[DataType]] = None, kernelv: Optional[SingleAndSequence[DataType]] = None, impulse: Optional[SingleAndSequence[float]] = None, impulseh: Optional[SingleAndSequence[float]] = None, impulsev: Optional[SingleAndSequence[float]] = None, taps: Optional[SingleAndSequence[int]] = None, tapsh: Optional[SingleAndSequence[int]] = None, tapsv: Optional[SingleAndSequence[int]] = None, a1: Optional[SingleAndSequence[float]] = None, a2: Optional[SingleAndSequence[float]] = None, a3: Optional[SingleAndSequence[float]] = None, a1h: Optional[SingleAndSequence[float]] = None, a2h: Optional[SingleAndSequence[float]] = None, a3h: Optional[SingleAndSequence[float]] = None, a1v: Optional[SingleAndSequence[float]] = None, a2v: Optional[SingleAndSequence[float]] = None, a3v: Optional[SingleAndSequence[float]] = None, kovrspl: Optional[SingleAndSequence[int]] = None, fh: Optional[SingleAndSequence[float]] = None, fv: Optional[SingleAndSequence[float]] = None, cnorm: Optional[SingleAndSequence[int]] = None, total: Optional[SingleAndSequence[float]] = None, totalh: Optional[SingleAndSequence[float]] = None, totalv: Optional[SingleAndSequence[float]] = None, invks: Optional[SingleAndSequence[int]] = None, invksh: Optional[SingleAndSequence[int]] = None, invksv: Optional[SingleAndSequence[int]] = None, invkstaps: Optional[SingleAndSequence[int]] = None, invkstapsh: Optional[SingleAndSequence[int]] = None, invkstapsv: Optional[SingleAndSequence[int]] = None, csp: Optional[int] = None, css: Optional[DataType] = None, planes: Optional[SingleAndSequence[float]] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, center: Optional[SingleAndSequence[int]] = None, cplace: Optional[DataType] = None, cplaces: Optional[DataType] = None, cplaced: Optional[DataType] = None, interlaced: Optional[int] = None, interlacedd: Optional[int] = None, tff: Optional[int] = None, tffd: Optional[int] = None, flt: Optional[int] = None, cpuopt: Optional[int] = None) -> 'VideoNode': ...
    def stack16tonative(self, clip: 'VideoNode') -> 'VideoNode': ...
    def transfer(self, clip: 'VideoNode', transs: Optional[SingleAndSequence[DataType]] = None, transd: Optional[SingleAndSequence[DataType]] = None, cont: Optional[float] = None, gcor: Optional[float] = None, bits: Optional[int] = None, flt: Optional[int] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, logceis: Optional[int] = None, logceid: Optional[int] = None, cpuopt: Optional[int] = None, blacklvl: Optional[float] = None, sceneref: Optional[int] = None, lb: Optional[float] = None, lw: Optional[float] = None, lws: Optional[float] = None, lwd: Optional[float] = None, ambient: Optional[float] = None, match: Optional[int] = None, gy: Optional[int] = None, debug: Optional[int] = None, sig_c: Optional[float] = None, sig_t: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_fmtc_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "fmtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def bitdepth(self, csp: Optional[int] = None, bits: Optional[int] = None, flt: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, dmode: Optional[int] = None, ampo: Optional[float] = None, ampn: Optional[float] = None, dyn: Optional[int] = None, staticnoise: Optional[int] = None, cpuopt: Optional[int] = None, patsize: Optional[int] = None, tpdfo: Optional[int] = None, tpdfn: Optional[int] = None, corplane: Optional[int] = None) -> 'VideoNode': ...
    def histluma(self, full: Optional[int] = None, amp: Optional[int] = None) -> 'VideoNode': ...
    def matrix(self, mat: Optional[DataType] = None, mats: Optional[DataType] = None, matd: Optional[DataType] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, coef: Optional[SingleAndSequence[float]] = None, csp: Optional[int] = None, col_fam: Optional[int] = None, bits: Optional[int] = None, singleout: Optional[int] = None, cpuopt: Optional[int] = None, planes: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...
    def matrix2020cl(self, full: Optional[int] = None, csp: Optional[int] = None, bits: Optional[int] = None, cpuopt: Optional[int] = None) -> 'VideoNode': ...
    def nativetostack16(self) -> 'VideoNode': ...
    def primaries(self, rs: Optional[SingleAndSequence[float]] = None, gs: Optional[SingleAndSequence[float]] = None, bs: Optional[SingleAndSequence[float]] = None, ws: Optional[SingleAndSequence[float]] = None, rd: Optional[SingleAndSequence[float]] = None, gd: Optional[SingleAndSequence[float]] = None, bd: Optional[SingleAndSequence[float]] = None, wd: Optional[SingleAndSequence[float]] = None, prims: Optional[DataType] = None, primd: Optional[DataType] = None, wconv: Optional[int] = None, cpuopt: Optional[int] = None) -> 'VideoNode': ...
    def resample(self, w: Optional[int] = None, h: Optional[int] = None, sx: Optional[SingleAndSequence[float]] = None, sy: Optional[SingleAndSequence[float]] = None, sw: Optional[SingleAndSequence[float]] = None, sh: Optional[SingleAndSequence[float]] = None, scale: Optional[float] = None, scaleh: Optional[float] = None, scalev: Optional[float] = None, kernel: Optional[SingleAndSequence[DataType]] = None, kernelh: Optional[SingleAndSequence[DataType]] = None, kernelv: Optional[SingleAndSequence[DataType]] = None, impulse: Optional[SingleAndSequence[float]] = None, impulseh: Optional[SingleAndSequence[float]] = None, impulsev: Optional[SingleAndSequence[float]] = None, taps: Optional[SingleAndSequence[int]] = None, tapsh: Optional[SingleAndSequence[int]] = None, tapsv: Optional[SingleAndSequence[int]] = None, a1: Optional[SingleAndSequence[float]] = None, a2: Optional[SingleAndSequence[float]] = None, a3: Optional[SingleAndSequence[float]] = None, a1h: Optional[SingleAndSequence[float]] = None, a2h: Optional[SingleAndSequence[float]] = None, a3h: Optional[SingleAndSequence[float]] = None, a1v: Optional[SingleAndSequence[float]] = None, a2v: Optional[SingleAndSequence[float]] = None, a3v: Optional[SingleAndSequence[float]] = None, kovrspl: Optional[SingleAndSequence[int]] = None, fh: Optional[SingleAndSequence[float]] = None, fv: Optional[SingleAndSequence[float]] = None, cnorm: Optional[SingleAndSequence[int]] = None, total: Optional[SingleAndSequence[float]] = None, totalh: Optional[SingleAndSequence[float]] = None, totalv: Optional[SingleAndSequence[float]] = None, invks: Optional[SingleAndSequence[int]] = None, invksh: Optional[SingleAndSequence[int]] = None, invksv: Optional[SingleAndSequence[int]] = None, invkstaps: Optional[SingleAndSequence[int]] = None, invkstapsh: Optional[SingleAndSequence[int]] = None, invkstapsv: Optional[SingleAndSequence[int]] = None, csp: Optional[int] = None, css: Optional[DataType] = None, planes: Optional[SingleAndSequence[float]] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, center: Optional[SingleAndSequence[int]] = None, cplace: Optional[DataType] = None, cplaces: Optional[DataType] = None, cplaced: Optional[DataType] = None, interlaced: Optional[int] = None, interlacedd: Optional[int] = None, tff: Optional[int] = None, tffd: Optional[int] = None, flt: Optional[int] = None, cpuopt: Optional[int] = None) -> 'VideoNode': ...
    def stack16tonative(self) -> 'VideoNode': ...
    def transfer(self, transs: Optional[SingleAndSequence[DataType]] = None, transd: Optional[SingleAndSequence[DataType]] = None, cont: Optional[float] = None, gcor: Optional[float] = None, bits: Optional[int] = None, flt: Optional[int] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, logceis: Optional[int] = None, logceid: Optional[int] = None, cpuopt: Optional[int] = None, blacklvl: Optional[float] = None, sceneref: Optional[int] = None, lb: Optional[float] = None, lw: Optional[float] = None, lws: Optional[float] = None, lwd: Optional[float] = None, ambient: Optional[float] = None, match: Optional[int] = None, gy: Optional[int] = None, debug: Optional[int] = None, sig_c: Optional[float] = None, sig_t: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: focus

class _Plugin_focus_Core_Bound(Plugin):
    """This class implements the module definitions for the "focus" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def SpatialSoften(self, clip: 'VideoNode', radius: Optional[int] = None, luma_threshold: Optional[float] = None, chroma_threshold: Optional[float] = None) -> 'VideoNode': ...
    def TemporalSoften(self, clip: 'VideoNode', radius: Optional[int] = None, luma_threshold: Optional[float] = None, chroma_threshold: Optional[float] = None, scenechange: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_focus_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "focus" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def SpatialSoften(self, radius: Optional[int] = None, luma_threshold: Optional[float] = None, chroma_threshold: Optional[float] = None) -> 'VideoNode': ...
    def TemporalSoften(self, radius: Optional[int] = None, luma_threshold: Optional[float] = None, chroma_threshold: Optional[float] = None, scenechange: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: focus2

class _Plugin_focus2_Core_Bound(Plugin):
    """This class implements the module definitions for the "focus2" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TemporalSoften2(self, clip: 'VideoNode', radius: Optional[int] = None, luma_threshold: Optional[int] = None, chroma_threshold: Optional[int] = None, scenechange: Optional[int] = None, mode: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_focus2_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "focus2" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TemporalSoften2(self, radius: Optional[int] = None, luma_threshold: Optional[int] = None, chroma_threshold: Optional[int] = None, scenechange: Optional[int] = None, mode: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: ftf

class _Plugin_ftf_Core_Bound(Plugin):
    """This class implements the module definitions for the "ftf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def FixFades(self, clip: 'VideoNode', mode: Optional[int] = None, threshold: Optional[float] = None, color: Optional[SingleAndSequence[float]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_ftf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "ftf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def FixFades(self, mode: Optional[int] = None, threshold: Optional[float] = None, color: Optional[SingleAndSequence[float]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: grad

class _Plugin_grad_Core_Bound(Plugin):
    """This class implements the module definitions for the "grad" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Curve(self, clip: 'VideoNode', fname: Optional[DataType] = None, ftype: Optional[int] = None, pmode: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_grad_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "grad" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Curve(self, fname: Optional[DataType] = None, ftype: Optional[int] = None, pmode: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: grain

class _Plugin_grain_Core_Bound(Plugin):
    """This class implements the module definitions for the "grain" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Add(self, clip: 'VideoNode', var: Optional[float] = None, uvar: Optional[float] = None, hcorr: Optional[float] = None, vcorr: Optional[float] = None, seed: Optional[int] = None, constant: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_grain_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "grain" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Add(self, var: Optional[float] = None, uvar: Optional[float] = None, hcorr: Optional[float] = None, vcorr: Optional[float] = None, seed: Optional[int] = None, constant: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: hist

class _Plugin_hist_Core_Bound(Plugin):
    """This class implements the module definitions for the "hist" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Classic(self, clip: 'VideoNode') -> 'VideoNode': ...
    def Color(self, clip: 'VideoNode') -> 'VideoNode': ...
    def Color2(self, clip: 'VideoNode') -> 'VideoNode': ...
    def Levels(self, clip: 'VideoNode', factor: Optional[float] = None) -> 'VideoNode': ...
    def Luma(self, clip: 'VideoNode') -> 'VideoNode': ...

class _Plugin_hist_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "hist" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Classic(self) -> 'VideoNode': ...
    def Color(self) -> 'VideoNode': ...
    def Color2(self) -> 'VideoNode': ...
    def Levels(self, factor: Optional[float] = None) -> 'VideoNode': ...
    def Luma(self) -> 'VideoNode': ...

# end implementation


# implementation: hqdn3d

class _Plugin_hqdn3d_Core_Bound(Plugin):
    """This class implements the module definitions for the "hqdn3d" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Hqdn3d(self, clip: 'VideoNode', lum_spac: Optional[float] = None, chrom_spac: Optional[float] = None, lum_tmp: Optional[float] = None, chrom_tmp: Optional[float] = None, restart_lap: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_hqdn3d_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "hqdn3d" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Hqdn3d(self, lum_spac: Optional[float] = None, chrom_spac: Optional[float] = None, lum_tmp: Optional[float] = None, chrom_tmp: Optional[float] = None, restart_lap: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: iccc

class _Plugin_iccc_Core_Bound(Plugin):
    """This class implements the module definitions for the "iccc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ICCConvert(self, clip: 'VideoNode', simulation_icc: DataType, display_icc: Optional[DataType] = None, soft_proofing: Optional[int] = None, simulation_intent: Optional[DataType] = None, display_intent: Optional[DataType] = None, gamut_warning: Optional[int] = None, black_point_compensation: Optional[int] = None, clut_size: Optional[int] = None) -> 'VideoNode': ...
    def ICCPlayback(self, clip: 'VideoNode', display_icc: Optional[DataType] = None, playback_csp: Optional[DataType] = None, gamma: Optional[float] = None, intent: Optional[DataType] = None, clut_size: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_iccc_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "iccc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ICCConvert(self, simulation_icc: DataType, display_icc: Optional[DataType] = None, soft_proofing: Optional[int] = None, simulation_intent: Optional[DataType] = None, display_intent: Optional[DataType] = None, gamut_warning: Optional[int] = None, black_point_compensation: Optional[int] = None, clut_size: Optional[int] = None) -> 'VideoNode': ...
    def ICCPlayback(self, display_icc: Optional[DataType] = None, playback_csp: Optional[DataType] = None, gamma: Optional[float] = None, intent: Optional[DataType] = None, clut_size: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: imwri

class _Plugin_imwri_Core_Bound(Plugin):
    """This class implements the module definitions for the "imwri" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Read(self, filename: SingleAndSequence[DataType], firstnum: Optional[int] = None, mismatch: Optional[int] = None, alpha: Optional[int] = None, float_output: Optional[int] = None, embed_icc: Optional[int] = None) -> 'VideoNode': ...
    def Write(self, clip: 'VideoNode', imgformat: DataType, filename: DataType, firstnum: Optional[int] = None, quality: Optional[int] = None, dither: Optional[int] = None, compression_type: Optional[DataType] = None, overwrite: Optional[int] = None, alpha: Optional['VideoNode'] = None) -> 'VideoNode': ...

class _Plugin_imwri_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "imwri" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Write(self, imgformat: DataType, filename: DataType, firstnum: Optional[int] = None, quality: Optional[int] = None, dither: Optional[int] = None, compression_type: Optional[DataType] = None, overwrite: Optional[int] = None, alpha: Optional['VideoNode'] = None) -> 'VideoNode': ...

# end implementation


# implementation: knlm

class _Plugin_knlm_Core_Bound(Plugin):
    """This class implements the module definitions for the "knlm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def KNLMeansCL(self, clip: 'VideoNode', d: Optional[int] = None, a: Optional[int] = None, s: Optional[int] = None, h: Optional[float] = None, channels: Optional[DataType] = None, wmode: Optional[int] = None, wref: Optional[float] = None, rclip: Optional['VideoNode'] = None, device_type: Optional[DataType] = None, device_id: Optional[int] = None, ocl_x: Optional[int] = None, ocl_y: Optional[int] = None, ocl_r: Optional[int] = None, info: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_knlm_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "knlm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def KNLMeansCL(self, d: Optional[int] = None, a: Optional[int] = None, s: Optional[int] = None, h: Optional[float] = None, channels: Optional[DataType] = None, wmode: Optional[int] = None, wref: Optional[float] = None, rclip: Optional['VideoNode'] = None, device_type: Optional[DataType] = None, device_id: Optional[int] = None, ocl_x: Optional[int] = None, ocl_y: Optional[int] = None, ocl_r: Optional[int] = None, info: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: libp2p

class _Plugin_libp2p_Core_Bound(Plugin):
    """This class implements the module definitions for the "libp2p" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Pack(self, clip: 'VideoNode') -> 'VideoNode': ...
    def Unpack(self, clip: 'VideoNode') -> 'VideoNode': ...

class _Plugin_libp2p_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "libp2p" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Pack(self) -> 'VideoNode': ...
    def Unpack(self) -> 'VideoNode': ...

# end implementation


# implementation: lsmas

class _Plugin_lsmas_Core_Bound(Plugin):
    """This class implements the module definitions for the "lsmas" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def LibavSMASHSource(self, source: DataType, track: Optional[int] = None, threads: Optional[int] = None, seek_mode: Optional[int] = None, seek_threshold: Optional[int] = None, dr: Optional[int] = None, fpsnum: Optional[int] = None, fpsden: Optional[int] = None, variable: Optional[int] = None, format: Optional[DataType] = None, decoder: Optional[DataType] = None, prefer_hw: Optional[int] = None, ff_loglevel: Optional[int] = None) -> 'VideoNode': ...
    def LWLibavSource(self, source: DataType, stream_index: Optional[int] = None, cache: Optional[int] = None, cachefile: Optional[DataType] = None, threads: Optional[int] = None, seek_mode: Optional[int] = None, seek_threshold: Optional[int] = None, dr: Optional[int] = None, fpsnum: Optional[int] = None, fpsden: Optional[int] = None, variable: Optional[int] = None, format: Optional[DataType] = None, decoder: Optional[DataType] = None, prefer_hw: Optional[int] = None, repeat: Optional[int] = None, dominance: Optional[int] = None, ff_loglevel: Optional[int] = None, cachedir: Optional[DataType] = None, soft_reset: Optional[int] = None) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

# end implementation


# implementation: median

class _Plugin_median_Core_Bound(Plugin):
    """This class implements the module definitions for the "median" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Median(self, clips: SingleAndSequence['VideoNode'], sync: Optional[int] = None, samples: Optional[int] = None, debug: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def MedianBlend(self, clips: SingleAndSequence['VideoNode'], low: Optional[int] = None, high: Optional[int] = None, closest: Optional[int] = None, sync: Optional[int] = None, samples: Optional[int] = None, debug: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def TemporalMedian(self, clip: 'VideoNode', radius: Optional[int] = None, debug: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_median_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "median" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Median(self, sync: Optional[int] = None, samples: Optional[int] = None, debug: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def MedianBlend(self, low: Optional[int] = None, high: Optional[int] = None, closest: Optional[int] = None, sync: Optional[int] = None, samples: Optional[int] = None, debug: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def TemporalMedian(self, radius: Optional[int] = None, debug: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: minsrp

class _Plugin_minsrp_Core_Bound(Plugin):
    """This class implements the module definitions for the "minsrp" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Sharp(self, clip: 'VideoNode', str: Optional[SingleAndSequence[float]] = None, mode: Optional[SingleAndSequence[int]] = None, linear: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_minsrp_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "minsrp" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Sharp(self, str: Optional[SingleAndSequence[float]] = None, mode: Optional[SingleAndSequence[int]] = None, linear: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: misc

class _Plugin_misc_Core_Bound(Plugin):
    """This class implements the module definitions for the "misc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def AverageFrames(self, clips: SingleAndSequence['VideoNode'], weights: SingleAndSequence[float], scale: Optional[float] = None, scenechange: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Hysteresis(self, clipa: 'VideoNode', clipb: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def SCDetect(self, clip: 'VideoNode', threshold: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_misc_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "misc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def AverageFrames(self, weights: SingleAndSequence[float], scale: Optional[float] = None, scenechange: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Hysteresis(self, clipb: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def SCDetect(self, threshold: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: morpho

class _Plugin_morpho_Core_Bound(Plugin):
    """This class implements the module definitions for the "morpho" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def BottomHat(self, clip: 'VideoNode', size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def Close(self, clip: 'VideoNode', size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def Dilate(self, clip: 'VideoNode', size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def Erode(self, clip: 'VideoNode', size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def Open(self, clip: 'VideoNode', size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def TopHat(self, clip: 'VideoNode', size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_morpho_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "morpho" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def BottomHat(self, size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def Close(self, size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def Dilate(self, size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def Erode(self, size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def Open(self, size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...
    def TopHat(self, size: Optional[int] = None, shape: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: mpeg2stinx

class _Plugin_mpeg2stinx_Core_Bound(Plugin):
    """This class implements the module definitions for the "mpeg2stinx" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def LutXYDiff(self, clip1: 'VideoNode', clip2: 'VideoNode') -> 'VideoNode': ...
    def Max(self, clip1: 'VideoNode', clip2: 'VideoNode') -> 'VideoNode': ...
    def Median3(self, clip1: 'VideoNode', clip2: 'VideoNode', clip3: 'VideoNode', process_chroma: Optional[int] = None) -> 'VideoNode': ...
    def Min(self, clip1: 'VideoNode', clip2: 'VideoNode') -> 'VideoNode': ...
    def Mpeg2Stinx(self, clip: 'VideoNode', mode: Optional[int] = None, sw: Optional[int] = None, sh: Optional[int] = None, contra: Optional[int] = None, blurv: Optional[float] = None, sstr: Optional[float] = None, scl: Optional[float] = None, dither: Optional[int] = None, order: Optional[int] = None, diffscl: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_mpeg2stinx_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "mpeg2stinx" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def LutXYDiff(self, clip2: 'VideoNode') -> 'VideoNode': ...
    def Max(self, clip2: 'VideoNode') -> 'VideoNode': ...
    def Median3(self, clip2: 'VideoNode', clip3: 'VideoNode', process_chroma: Optional[int] = None) -> 'VideoNode': ...
    def Min(self, clip2: 'VideoNode') -> 'VideoNode': ...
    def Mpeg2Stinx(self, mode: Optional[int] = None, sw: Optional[int] = None, sh: Optional[int] = None, contra: Optional[int] = None, blurv: Optional[float] = None, sstr: Optional[float] = None, scl: Optional[float] = None, dither: Optional[int] = None, order: Optional[int] = None, diffscl: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: mpls

class _Plugin_mpls_Core_Bound(Plugin):
    """This class implements the module definitions for the "mpls" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Read(self, bd_path: DataType, playlist: int, angle: Optional[int] = None) -> Tuple[Any, ...]: ...

# end implementation


# implementation: mv

class _Plugin_mv_Core_Bound(Plugin):
    """This class implements the module definitions for the "mv" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Analyse(self, super: 'VideoNode', blksize: Optional[int] = None, blksizev: Optional[int] = None, levels: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, pelsearch: Optional[int] = None, isb: Optional[int] = None, lambda_: Optional[int] = None, chroma: Optional[int] = None, delta: Optional[int] = None, truemotion: Optional[int] = None, lsad: Optional[int] = None, plevel: Optional[int] = None, global_: Optional[int] = None, pnew: Optional[int] = None, pzero: Optional[int] = None, pglobal: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, badsad: Optional[int] = None, badrange: Optional[int] = None, opt: Optional[int] = None, meander: Optional[int] = None, trymany: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, search_coarse: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def BlockFPS(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', num: Optional[int] = None, den: Optional[int] = None, mode: Optional[int] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Compensate(self, clip: 'VideoNode', super: 'VideoNode', vectors: 'VideoNode', scbehavior: Optional[int] = None, thsad: Optional[int] = None, fields: Optional[int] = None, time: Optional[float] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def Degrain1(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', thsad: Optional[int] = None, thsadc: Optional[int] = None, plane: Optional[int] = None, limit: Optional[int] = None, limitc: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Degrain2(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', thsad: Optional[int] = None, thsadc: Optional[int] = None, plane: Optional[int] = None, limit: Optional[int] = None, limitc: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Degrain3(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', thsad: Optional[int] = None, thsadc: Optional[int] = None, plane: Optional[int] = None, limit: Optional[int] = None, limitc: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def DepanAnalyse(self, clip: 'VideoNode', vectors: 'VideoNode', mask: Optional['VideoNode'] = None, zoom: Optional[int] = None, rot: Optional[int] = None, pixaspect: Optional[float] = None, error: Optional[float] = None, info: Optional[int] = None, wrong: Optional[float] = None, zerow: Optional[float] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def DepanCompensate(self, clip: 'VideoNode', data: 'VideoNode', offset: Optional[float] = None, subpixel: Optional[int] = None, pixaspect: Optional[float] = None, matchfields: Optional[int] = None, mirror: Optional[int] = None, blur: Optional[int] = None, info: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def DepanEstimate(self, clip: 'VideoNode', trust: Optional[float] = None, winx: Optional[int] = None, winy: Optional[int] = None, wleft: Optional[int] = None, wtop: Optional[int] = None, dxmax: Optional[int] = None, dymax: Optional[int] = None, zoommax: Optional[float] = None, stab: Optional[float] = None, pixaspect: Optional[float] = None, info: Optional[int] = None, show: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def DepanStabilise(self, clip: 'VideoNode', data: 'VideoNode', cutoff: Optional[float] = None, damping: Optional[float] = None, initzoom: Optional[float] = None, addzoom: Optional[int] = None, prev: Optional[int] = None, next: Optional[int] = None, mirror: Optional[int] = None, blur: Optional[int] = None, dxmax: Optional[float] = None, dymax: Optional[float] = None, zoommax: Optional[float] = None, rotmax: Optional[float] = None, subpixel: Optional[int] = None, pixaspect: Optional[float] = None, fitlast: Optional[int] = None, tzoom: Optional[float] = None, info: Optional[int] = None, method: Optional[int] = None, fields: Optional[int] = None) -> 'VideoNode': ...
    def Finest(self, super: 'VideoNode', opt: Optional[int] = None) -> 'VideoNode': ...
    def Flow(self, clip: 'VideoNode', super: 'VideoNode', vectors: 'VideoNode', time: Optional[float] = None, mode: Optional[int] = None, fields: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def FlowBlur(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', blur: Optional[float] = None, prec: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def FlowFPS(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', num: Optional[int] = None, den: Optional[int] = None, mask: Optional[int] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def FlowInter(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', time: Optional[float] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Mask(self, clip: 'VideoNode', vectors: 'VideoNode', ml: Optional[float] = None, gamma: Optional[float] = None, kind: Optional[int] = None, time: Optional[float] = None, ysc: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Recalculate(self, super: 'VideoNode', vectors: 'VideoNode', thsad: Optional[int] = None, smooth: Optional[int] = None, blksize: Optional[int] = None, blksizev: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, lambda_: Optional[int] = None, chroma: Optional[int] = None, truemotion: Optional[int] = None, pnew: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, opt: Optional[int] = None, meander: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def SCDetection(self, clip: 'VideoNode', vectors: 'VideoNode', thscd1: Optional[int] = None, thscd2: Optional[int] = None) -> 'VideoNode': ...
    def Super(self, clip: 'VideoNode', hpad: Optional[int] = None, vpad: Optional[int] = None, pel: Optional[int] = None, levels: Optional[int] = None, chroma: Optional[int] = None, sharp: Optional[int] = None, rfilter: Optional[int] = None, pelclip: Optional['VideoNode'] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_mv_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "mv" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Analyse(self, blksize: Optional[int] = None, blksizev: Optional[int] = None, levels: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, pelsearch: Optional[int] = None, isb: Optional[int] = None, lambda_: Optional[int] = None, chroma: Optional[int] = None, delta: Optional[int] = None, truemotion: Optional[int] = None, lsad: Optional[int] = None, plevel: Optional[int] = None, global_: Optional[int] = None, pnew: Optional[int] = None, pzero: Optional[int] = None, pglobal: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, badsad: Optional[int] = None, badrange: Optional[int] = None, opt: Optional[int] = None, meander: Optional[int] = None, trymany: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, search_coarse: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def BlockFPS(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', num: Optional[int] = None, den: Optional[int] = None, mode: Optional[int] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Compensate(self, super: 'VideoNode', vectors: 'VideoNode', scbehavior: Optional[int] = None, thsad: Optional[int] = None, fields: Optional[int] = None, time: Optional[float] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def Degrain1(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', thsad: Optional[int] = None, thsadc: Optional[int] = None, plane: Optional[int] = None, limit: Optional[int] = None, limitc: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Degrain2(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', thsad: Optional[int] = None, thsadc: Optional[int] = None, plane: Optional[int] = None, limit: Optional[int] = None, limitc: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Degrain3(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', thsad: Optional[int] = None, thsadc: Optional[int] = None, plane: Optional[int] = None, limit: Optional[int] = None, limitc: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def DepanAnalyse(self, vectors: 'VideoNode', mask: Optional['VideoNode'] = None, zoom: Optional[int] = None, rot: Optional[int] = None, pixaspect: Optional[float] = None, error: Optional[float] = None, info: Optional[int] = None, wrong: Optional[float] = None, zerow: Optional[float] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def DepanCompensate(self, data: 'VideoNode', offset: Optional[float] = None, subpixel: Optional[int] = None, pixaspect: Optional[float] = None, matchfields: Optional[int] = None, mirror: Optional[int] = None, blur: Optional[int] = None, info: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def DepanEstimate(self, trust: Optional[float] = None, winx: Optional[int] = None, winy: Optional[int] = None, wleft: Optional[int] = None, wtop: Optional[int] = None, dxmax: Optional[int] = None, dymax: Optional[int] = None, zoommax: Optional[float] = None, stab: Optional[float] = None, pixaspect: Optional[float] = None, info: Optional[int] = None, show: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def DepanStabilise(self, data: 'VideoNode', cutoff: Optional[float] = None, damping: Optional[float] = None, initzoom: Optional[float] = None, addzoom: Optional[int] = None, prev: Optional[int] = None, next: Optional[int] = None, mirror: Optional[int] = None, blur: Optional[int] = None, dxmax: Optional[float] = None, dymax: Optional[float] = None, zoommax: Optional[float] = None, rotmax: Optional[float] = None, subpixel: Optional[int] = None, pixaspect: Optional[float] = None, fitlast: Optional[int] = None, tzoom: Optional[float] = None, info: Optional[int] = None, method: Optional[int] = None, fields: Optional[int] = None) -> 'VideoNode': ...
    def Finest(self, opt: Optional[int] = None) -> 'VideoNode': ...
    def Flow(self, super: 'VideoNode', vectors: 'VideoNode', time: Optional[float] = None, mode: Optional[int] = None, fields: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def FlowBlur(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', blur: Optional[float] = None, prec: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def FlowFPS(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', num: Optional[int] = None, den: Optional[int] = None, mask: Optional[int] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def FlowInter(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', time: Optional[float] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Mask(self, vectors: 'VideoNode', ml: Optional[float] = None, gamma: Optional[float] = None, kind: Optional[int] = None, time: Optional[float] = None, ysc: Optional[int] = None, thscd1: Optional[int] = None, thscd2: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def Recalculate(self, vectors: 'VideoNode', thsad: Optional[int] = None, smooth: Optional[int] = None, blksize: Optional[int] = None, blksizev: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, lambda_: Optional[int] = None, chroma: Optional[int] = None, truemotion: Optional[int] = None, pnew: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, opt: Optional[int] = None, meander: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def SCDetection(self, vectors: 'VideoNode', thscd1: Optional[int] = None, thscd2: Optional[int] = None) -> 'VideoNode': ...
    def Super(self, hpad: Optional[int] = None, vpad: Optional[int] = None, pel: Optional[int] = None, levels: Optional[int] = None, chroma: Optional[int] = None, sharp: Optional[int] = None, rfilter: Optional[int] = None, pelclip: Optional['VideoNode'] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: mvsf

class _Plugin_mvsf_Core_Bound(Plugin):
    """This class implements the module definitions for the "mvsf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Analyse(self, super: 'VideoNode', blksize: Optional[int] = None, blksizev: Optional[int] = None, levels: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, pelsearch: Optional[int] = None, isb: Optional[int] = None, lambda_: Optional[float] = None, chroma: Optional[int] = None, delta: Optional[int] = None, truemotion: Optional[int] = None, lsad: Optional[float] = None, plevel: Optional[int] = None, global_: Optional[int] = None, pnew: Optional[int] = None, pzero: Optional[int] = None, pglobal: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, badsad: Optional[float] = None, badrange: Optional[int] = None, meander: Optional[int] = None, trymany: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, search_coarse: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def Analyze(self, super: 'VideoNode', blksize: Optional[int] = None, blksizev: Optional[int] = None, levels: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, pelsearch: Optional[int] = None, isb: Optional[int] = None, lambda_: Optional[float] = None, chroma: Optional[int] = None, delta: Optional[int] = None, truemotion: Optional[int] = None, lsad: Optional[float] = None, plevel: Optional[int] = None, global_: Optional[int] = None, pnew: Optional[int] = None, pzero: Optional[int] = None, pglobal: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, badsad: Optional[float] = None, badrange: Optional[int] = None, meander: Optional[int] = None, trymany: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, search_coarse: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def BlockFPS(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', num: Optional[int] = None, den: Optional[int] = None, mode: Optional[int] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Compensate(self, clip: 'VideoNode', super: 'VideoNode', vectors: 'VideoNode', scbehavior: Optional[int] = None, thsad: Optional[float] = None, fields: Optional[int] = None, time: Optional[float] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def Degrain1(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain10(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain11(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain12(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain13(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain14(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain15(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain16(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain17(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain18(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain19(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain2(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain20(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain21(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', mvbw21: 'VideoNode', mvfw21: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain22(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', mvbw21: 'VideoNode', mvfw21: 'VideoNode', mvbw22: 'VideoNode', mvfw22: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain23(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', mvbw21: 'VideoNode', mvfw21: 'VideoNode', mvbw22: 'VideoNode', mvfw22: 'VideoNode', mvbw23: 'VideoNode', mvfw23: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain24(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', mvbw21: 'VideoNode', mvfw21: 'VideoNode', mvbw22: 'VideoNode', mvfw22: 'VideoNode', mvbw23: 'VideoNode', mvfw23: 'VideoNode', mvbw24: 'VideoNode', mvfw24: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain3(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain4(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain5(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain6(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain7(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain8(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain9(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Finest(self, super: 'VideoNode') -> 'VideoNode': ...
    def Flow(self, clip: 'VideoNode', super: 'VideoNode', vectors: 'VideoNode', time: Optional[float] = None, mode: Optional[int] = None, fields: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def FlowBlur(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', blur: Optional[float] = None, prec: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def FlowFPS(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', num: Optional[int] = None, den: Optional[int] = None, mask: Optional[int] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def FlowInter(self, clip: 'VideoNode', super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', time: Optional[float] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Mask(self, clip: 'VideoNode', vectors: 'VideoNode', ml: Optional[float] = None, gamma: Optional[float] = None, kind: Optional[int] = None, time: Optional[float] = None, ysc: Optional[float] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Recalculate(self, super: 'VideoNode', vectors: 'VideoNode', thsad: Optional[float] = None, smooth: Optional[int] = None, blksize: Optional[int] = None, blksizev: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, lambda_: Optional[float] = None, chroma: Optional[int] = None, truemotion: Optional[int] = None, pnew: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, meander: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def SCDetection(self, clip: 'VideoNode', vectors: 'VideoNode', thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Super(self, clip: 'VideoNode', hpad: Optional[int] = None, vpad: Optional[int] = None, pel: Optional[int] = None, levels: Optional[int] = None, chroma: Optional[int] = None, sharp: Optional[int] = None, rfilter: Optional[int] = None, pelclip: Optional['VideoNode'] = None) -> 'VideoNode': ...

class _Plugin_mvsf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "mvsf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Analyse(self, blksize: Optional[int] = None, blksizev: Optional[int] = None, levels: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, pelsearch: Optional[int] = None, isb: Optional[int] = None, lambda_: Optional[float] = None, chroma: Optional[int] = None, delta: Optional[int] = None, truemotion: Optional[int] = None, lsad: Optional[float] = None, plevel: Optional[int] = None, global_: Optional[int] = None, pnew: Optional[int] = None, pzero: Optional[int] = None, pglobal: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, badsad: Optional[float] = None, badrange: Optional[int] = None, meander: Optional[int] = None, trymany: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, search_coarse: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def Analyze(self, blksize: Optional[int] = None, blksizev: Optional[int] = None, levels: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, pelsearch: Optional[int] = None, isb: Optional[int] = None, lambda_: Optional[float] = None, chroma: Optional[int] = None, delta: Optional[int] = None, truemotion: Optional[int] = None, lsad: Optional[float] = None, plevel: Optional[int] = None, global_: Optional[int] = None, pnew: Optional[int] = None, pzero: Optional[int] = None, pglobal: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, badsad: Optional[float] = None, badrange: Optional[int] = None, meander: Optional[int] = None, trymany: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, search_coarse: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def BlockFPS(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', num: Optional[int] = None, den: Optional[int] = None, mode: Optional[int] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Compensate(self, super: 'VideoNode', vectors: 'VideoNode', scbehavior: Optional[int] = None, thsad: Optional[float] = None, fields: Optional[int] = None, time: Optional[float] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def Degrain1(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain10(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain11(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain12(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain13(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain14(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain15(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain16(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain17(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain18(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain19(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain2(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain20(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain21(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', mvbw21: 'VideoNode', mvfw21: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain22(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', mvbw21: 'VideoNode', mvfw21: 'VideoNode', mvbw22: 'VideoNode', mvfw22: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain23(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', mvbw21: 'VideoNode', mvfw21: 'VideoNode', mvbw22: 'VideoNode', mvfw22: 'VideoNode', mvbw23: 'VideoNode', mvfw23: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain24(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', mvbw10: 'VideoNode', mvfw10: 'VideoNode', mvbw11: 'VideoNode', mvfw11: 'VideoNode', mvbw12: 'VideoNode', mvfw12: 'VideoNode', mvbw13: 'VideoNode', mvfw13: 'VideoNode', mvbw14: 'VideoNode', mvfw14: 'VideoNode', mvbw15: 'VideoNode', mvfw15: 'VideoNode', mvbw16: 'VideoNode', mvfw16: 'VideoNode', mvbw17: 'VideoNode', mvfw17: 'VideoNode', mvbw18: 'VideoNode', mvfw18: 'VideoNode', mvbw19: 'VideoNode', mvfw19: 'VideoNode', mvbw20: 'VideoNode', mvfw20: 'VideoNode', mvbw21: 'VideoNode', mvfw21: 'VideoNode', mvbw22: 'VideoNode', mvfw22: 'VideoNode', mvbw23: 'VideoNode', mvfw23: 'VideoNode', mvbw24: 'VideoNode', mvfw24: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain3(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain4(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain5(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain6(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain7(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain8(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Degrain9(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', mvbw2: 'VideoNode', mvfw2: 'VideoNode', mvbw3: 'VideoNode', mvfw3: 'VideoNode', mvbw4: 'VideoNode', mvfw4: 'VideoNode', mvbw5: 'VideoNode', mvfw5: 'VideoNode', mvbw6: 'VideoNode', mvfw6: 'VideoNode', mvbw7: 'VideoNode', mvfw7: 'VideoNode', mvbw8: 'VideoNode', mvfw8: 'VideoNode', mvbw9: 'VideoNode', mvfw9: 'VideoNode', thsad: Optional[SingleAndSequence[float]] = None, plane: Optional[int] = None, limit: Optional[SingleAndSequence[float]] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Finest(self) -> 'VideoNode': ...
    def Flow(self, super: 'VideoNode', vectors: 'VideoNode', time: Optional[float] = None, mode: Optional[int] = None, fields: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None, tff: Optional[int] = None) -> 'VideoNode': ...
    def FlowBlur(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', blur: Optional[float] = None, prec: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def FlowFPS(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', num: Optional[int] = None, den: Optional[int] = None, mask: Optional[int] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def FlowInter(self, super: 'VideoNode', mvbw: 'VideoNode', mvfw: 'VideoNode', time: Optional[float] = None, ml: Optional[float] = None, blend: Optional[int] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Mask(self, vectors: 'VideoNode', ml: Optional[float] = None, gamma: Optional[float] = None, kind: Optional[int] = None, time: Optional[float] = None, ysc: Optional[float] = None, thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Recalculate(self, vectors: 'VideoNode', thsad: Optional[float] = None, smooth: Optional[int] = None, blksize: Optional[int] = None, blksizev: Optional[int] = None, search: Optional[int] = None, searchparam: Optional[int] = None, lambda_: Optional[float] = None, chroma: Optional[int] = None, truemotion: Optional[int] = None, pnew: Optional[int] = None, overlap: Optional[int] = None, overlapv: Optional[int] = None, divide: Optional[int] = None, meander: Optional[int] = None, fields: Optional[int] = None, tff: Optional[int] = None, dct: Optional[int] = None) -> 'VideoNode': ...
    def SCDetection(self, vectors: 'VideoNode', thscd1: Optional[float] = None, thscd2: Optional[float] = None) -> 'VideoNode': ...
    def Super(self, hpad: Optional[int] = None, vpad: Optional[int] = None, pel: Optional[int] = None, levels: Optional[int] = None, chroma: Optional[int] = None, sharp: Optional[int] = None, rfilter: Optional[int] = None, pelclip: Optional['VideoNode'] = None) -> 'VideoNode': ...

# end implementation


# implementation: ncnn

class _Plugin_ncnn_Core_Bound(Plugin):
    """This class implements the module definitions for the "ncnn" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Model(self, clips: SingleAndSequence['VideoNode'], network_path: DataType, overlap: Optional[SingleAndSequence[int]] = None, tilesize: Optional[SingleAndSequence[int]] = None, device_id: Optional[int] = None, num_streams: Optional[int] = None, builtin: Optional[int] = None, builtindir: Optional[DataType] = None, fp16: Optional[int] = None, path_is_serialization: Optional[int] = None) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_ncnn_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "ncnn" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Model(self, network_path: DataType, overlap: Optional[SingleAndSequence[int]] = None, tilesize: Optional[SingleAndSequence[int]] = None, device_id: Optional[int] = None, num_streams: Optional[int] = None, builtin: Optional[int] = None, builtindir: Optional[DataType] = None, fp16: Optional[int] = None, path_is_serialization: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: neo_f3kdb

class _Plugin_neo_f3kdb_Core_Bound(Plugin):
    """This class implements the module definitions for the "neo_f3kdb" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Deband(self, clip: 'VideoNode', range: Optional[int] = None, y: Optional[int] = None, cb: Optional[int] = None, cr: Optional[int] = None, grainy: Optional[int] = None, grainc: Optional[int] = None, sample_mode: Optional[int] = None, seed: Optional[int] = None, blur_first: Optional[int] = None, dynamic_grain: Optional[int] = None, opt: Optional[int] = None, mt: Optional[int] = None, dither_algo: Optional[int] = None, keep_tv_range: Optional[int] = None, output_depth: Optional[int] = None, random_algo_ref: Optional[int] = None, random_algo_grain: Optional[int] = None, random_param_ref: Optional[float] = None, random_param_grain: Optional[float] = None, preset: Optional[DataType] = None, y_1: Optional[int] = None, cb_1: Optional[int] = None, cr_1: Optional[int] = None, y_2: Optional[int] = None, cb_2: Optional[int] = None, cr_2: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_neo_f3kdb_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "neo_f3kdb" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Deband(self, range: Optional[int] = None, y: Optional[int] = None, cb: Optional[int] = None, cr: Optional[int] = None, grainy: Optional[int] = None, grainc: Optional[int] = None, sample_mode: Optional[int] = None, seed: Optional[int] = None, blur_first: Optional[int] = None, dynamic_grain: Optional[int] = None, opt: Optional[int] = None, mt: Optional[int] = None, dither_algo: Optional[int] = None, keep_tv_range: Optional[int] = None, output_depth: Optional[int] = None, random_algo_ref: Optional[int] = None, random_algo_grain: Optional[int] = None, random_param_ref: Optional[float] = None, random_param_grain: Optional[float] = None, preset: Optional[DataType] = None, y_1: Optional[int] = None, cb_1: Optional[int] = None, cr_1: Optional[int] = None, y_2: Optional[int] = None, cb_2: Optional[int] = None, cr_2: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: nnedi3

class _Plugin_nnedi3_Core_Bound(Plugin):
    """This class implements the module definitions for the "nnedi3" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def nnedi3(self, clip: 'VideoNode', field: int, dh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, nsize: Optional[int] = None, nns: Optional[int] = None, qual: Optional[int] = None, etype: Optional[int] = None, pscrn: Optional[int] = None, opt: Optional[int] = None, int16_prescreener: Optional[int] = None, int16_predictor: Optional[int] = None, exp: Optional[int] = None, show_mask: Optional[int] = None, combed_only: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_nnedi3_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "nnedi3" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def nnedi3(self, field: int, dh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, nsize: Optional[int] = None, nns: Optional[int] = None, qual: Optional[int] = None, etype: Optional[int] = None, pscrn: Optional[int] = None, opt: Optional[int] = None, int16_prescreener: Optional[int] = None, int16_predictor: Optional[int] = None, exp: Optional[int] = None, show_mask: Optional[int] = None, combed_only: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: nnedi3cl

class _Plugin_nnedi3cl_Core_Bound(Plugin):
    """This class implements the module definitions for the "nnedi3cl" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def NNEDI3CL(self, clip: 'VideoNode', field: int, dh: Optional[int] = None, dw: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, nsize: Optional[int] = None, nns: Optional[int] = None, qual: Optional[int] = None, etype: Optional[int] = None, pscrn: Optional[int] = None, device: Optional[int] = None, list_device: Optional[int] = None, info: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_nnedi3cl_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "nnedi3cl" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def NNEDI3CL(self, field: int, dh: Optional[int] = None, dw: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, nsize: Optional[int] = None, nns: Optional[int] = None, qual: Optional[int] = None, etype: Optional[int] = None, pscrn: Optional[int] = None, device: Optional[int] = None, list_device: Optional[int] = None, info: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: noise

class _Plugin_noise_Core_Bound(Plugin):
    """This class implements the module definitions for the "noise" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Add(self, clip: 'VideoNode', var: Optional[float] = None, uvar: Optional[float] = None, type: Optional[int] = None, hcorr: Optional[float] = None, vcorr: Optional[float] = None, xsize: Optional[float] = None, ysize: Optional[float] = None, scale: Optional[float] = None, seed: Optional[int] = None, constant: Optional[int] = None, every: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_noise_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "noise" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Add(self, var: Optional[float] = None, uvar: Optional[float] = None, type: Optional[int] = None, hcorr: Optional[float] = None, vcorr: Optional[float] = None, xsize: Optional[float] = None, ysize: Optional[float] = None, scale: Optional[float] = None, seed: Optional[int] = None, constant: Optional[int] = None, every: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: ort

class _Plugin_ort_Core_Bound(Plugin):
    """This class implements the module definitions for the "ort" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Model(self, clips: SingleAndSequence['VideoNode'], network_path: DataType, overlap: Optional[SingleAndSequence[int]] = None, tilesize: Optional[SingleAndSequence[int]] = None, provider: Optional[DataType] = None, device_id: Optional[int] = None, num_streams: Optional[int] = None, verbosity: Optional[int] = None, cudnn_benchmark: Optional[int] = None, builtin: Optional[int] = None, builtindir: Optional[DataType] = None, fp16: Optional[int] = None, path_is_serialization: Optional[int] = None, use_cuda_graph: Optional[int] = None, fp16_blacklist_ops: Optional[SingleAndSequence[DataType]] = None) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_ort_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "ort" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Model(self, network_path: DataType, overlap: Optional[SingleAndSequence[int]] = None, tilesize: Optional[SingleAndSequence[int]] = None, provider: Optional[DataType] = None, device_id: Optional[int] = None, num_streams: Optional[int] = None, verbosity: Optional[int] = None, cudnn_benchmark: Optional[int] = None, builtin: Optional[int] = None, builtindir: Optional[DataType] = None, fp16: Optional[int] = None, path_is_serialization: Optional[int] = None, use_cuda_graph: Optional[int] = None, fp16_blacklist_ops: Optional[SingleAndSequence[DataType]] = None) -> 'VideoNode': ...

# end implementation


# implementation: ov

class _Plugin_ov_Core_Bound(Plugin):
    """This class implements the module definitions for the "ov" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def AvailableDevices(self) -> 'VideoNode': ...
    def Model(self, clips: SingleAndSequence['VideoNode'], network_path: DataType, overlap: Optional[SingleAndSequence[int]] = None, tilesize: Optional[SingleAndSequence[int]] = None, device: Optional[DataType] = None, builtin: Optional[int] = None, builtindir: Optional[DataType] = None, fp16: Optional[int] = None, config: Optional[VSMapValueCallback[_VapourSynthMapValue]] = None, path_is_serialization: Optional[int] = None, fp16_blacklist_ops: Optional[SingleAndSequence[DataType]] = None, dot_path: Optional[DataType] = None) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_ov_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "ov" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Model(self, network_path: DataType, overlap: Optional[SingleAndSequence[int]] = None, tilesize: Optional[SingleAndSequence[int]] = None, device: Optional[DataType] = None, builtin: Optional[int] = None, builtindir: Optional[DataType] = None, fp16: Optional[int] = None, config: Optional[VSMapValueCallback[_VapourSynthMapValue]] = None, path_is_serialization: Optional[int] = None, fp16_blacklist_ops: Optional[SingleAndSequence[DataType]] = None, dot_path: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation


# implementation: placebo

class _Plugin_placebo_Core_Bound(Plugin):
    """This class implements the module definitions for the "placebo" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Deband(self, clip: 'VideoNode', planes: Optional[int] = None, iterations: Optional[int] = None, threshold: Optional[float] = None, radius: Optional[float] = None, grain: Optional[float] = None, dither: Optional[int] = None, dither_algo: Optional[int] = None, log_level: Optional[int] = None) -> 'VideoNode': ...
    def Resample(self, clip: 'VideoNode', width: int, height: int, filter: Optional[DataType] = None, clamp: Optional[float] = None, blur: Optional[float] = None, taper: Optional[float] = None, radius: Optional[float] = None, param1: Optional[float] = None, param2: Optional[float] = None, sx: Optional[float] = None, sy: Optional[float] = None, antiring: Optional[float] = None, lut_entries: Optional[int] = None, cutoff: Optional[float] = None, sigmoidize: Optional[int] = None, sigmoid_center: Optional[float] = None, sigmoid_slope: Optional[float] = None, linearize: Optional[int] = None, trc: Optional[int] = None, log_level: Optional[int] = None) -> 'VideoNode': ...
    def Shader(self, clip: 'VideoNode', shader: Optional[DataType] = None, width: Optional[int] = None, height: Optional[int] = None, chroma_loc: Optional[int] = None, matrix: Optional[int] = None, trc: Optional[int] = None, linearize: Optional[int] = None, sigmoidize: Optional[int] = None, sigmoid_center: Optional[float] = None, sigmoid_slope: Optional[float] = None, lut_entries: Optional[int] = None, antiring: Optional[float] = None, filter: Optional[DataType] = None, clamp: Optional[float] = None, blur: Optional[float] = None, taper: Optional[float] = None, radius: Optional[float] = None, param1: Optional[float] = None, param2: Optional[float] = None, shader_s: Optional[DataType] = None, log_level: Optional[int] = None) -> 'VideoNode': ...
    def Tonemap(self, clip: 'VideoNode', src_csp: Optional[int] = None, dst_csp: Optional[int] = None, src_max: Optional[float] = None, src_min: Optional[float] = None, dst_max: Optional[float] = None, dst_min: Optional[float] = None, dynamic_peak_detection: Optional[int] = None, smoothing_period: Optional[float] = None, scene_threshold_low: Optional[float] = None, scene_threshold_high: Optional[float] = None, intent: Optional[int] = None, gamut_mode: Optional[int] = None, tone_mapping_function: Optional[int] = None, tone_mapping_mode: Optional[int] = None, tone_mapping_param: Optional[float] = None, tone_mapping_crosstalk: Optional[float] = None, use_dovi: Optional[int] = None, log_level: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_placebo_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "placebo" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Deband(self, planes: Optional[int] = None, iterations: Optional[int] = None, threshold: Optional[float] = None, radius: Optional[float] = None, grain: Optional[float] = None, dither: Optional[int] = None, dither_algo: Optional[int] = None, log_level: Optional[int] = None) -> 'VideoNode': ...
    def Resample(self, width: int, height: int, filter: Optional[DataType] = None, clamp: Optional[float] = None, blur: Optional[float] = None, taper: Optional[float] = None, radius: Optional[float] = None, param1: Optional[float] = None, param2: Optional[float] = None, sx: Optional[float] = None, sy: Optional[float] = None, antiring: Optional[float] = None, lut_entries: Optional[int] = None, cutoff: Optional[float] = None, sigmoidize: Optional[int] = None, sigmoid_center: Optional[float] = None, sigmoid_slope: Optional[float] = None, linearize: Optional[int] = None, trc: Optional[int] = None, log_level: Optional[int] = None) -> 'VideoNode': ...
    def Shader(self, shader: Optional[DataType] = None, width: Optional[int] = None, height: Optional[int] = None, chroma_loc: Optional[int] = None, matrix: Optional[int] = None, trc: Optional[int] = None, linearize: Optional[int] = None, sigmoidize: Optional[int] = None, sigmoid_center: Optional[float] = None, sigmoid_slope: Optional[float] = None, lut_entries: Optional[int] = None, antiring: Optional[float] = None, filter: Optional[DataType] = None, clamp: Optional[float] = None, blur: Optional[float] = None, taper: Optional[float] = None, radius: Optional[float] = None, param1: Optional[float] = None, param2: Optional[float] = None, shader_s: Optional[DataType] = None, log_level: Optional[int] = None) -> 'VideoNode': ...
    def Tonemap(self, src_csp: Optional[int] = None, dst_csp: Optional[int] = None, src_max: Optional[float] = None, src_min: Optional[float] = None, dst_max: Optional[float] = None, dst_min: Optional[float] = None, dynamic_peak_detection: Optional[int] = None, smoothing_period: Optional[float] = None, scene_threshold_low: Optional[float] = None, scene_threshold_high: Optional[float] = None, intent: Optional[int] = None, gamut_mode: Optional[int] = None, tone_mapping_function: Optional[int] = None, tone_mapping_mode: Optional[int] = None, tone_mapping_param: Optional[float] = None, tone_mapping_crosstalk: Optional[float] = None, use_dovi: Optional[int] = None, log_level: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: psm

class _Plugin_psm_Core_Bound(Plugin):
    """This class implements the module definitions for the "psm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def PlaneAverage(self, clip: 'VideoNode', value_exclude: SingleAndSequence[int], plane: Optional[int] = None, prop: Optional[DataType] = None) -> 'VideoNode': ...
    def PlaneMinMax(self, clip: 'VideoNode', minthr: Optional[float] = None, maxthr: Optional[float] = None, plane: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_psm_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "psm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def PlaneAverage(self, value_exclude: SingleAndSequence[int], plane: Optional[int] = None, prop: Optional[DataType] = None) -> 'VideoNode': ...
    def PlaneMinMax(self, minthr: Optional[float] = None, maxthr: Optional[float] = None, plane: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: rdvs

class _Plugin_rdvs_Core_Bound(Plugin):
    """This class implements the module definitions for the "rdvs" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DupBlocks(self, input: 'VideoNode', gmthreshold: Optional[int] = None, mthreshold: Optional[int] = None, noise: Optional[int] = None, noisy: Optional[int] = None, dist: Optional[int] = None, tolerance: Optional[int] = None, dmode: Optional[int] = None, pthreshold: Optional[int] = None, cthreshold: Optional[int] = None, grey: Optional[int] = None) -> 'VideoNode': ...
    def RestoreMotionBlocks(self, input: 'VideoNode', restore: 'VideoNode', neighbour: Optional['VideoNode'] = None, neighbour2: Optional['VideoNode'] = None, alternative: Optional['VideoNode'] = None, gmthreshold: Optional[int] = None, mthreshold: Optional[int] = None, noise: Optional[int] = None, noisy: Optional[int] = None, dist: Optional[int] = None, tolerance: Optional[int] = None, dmode: Optional[int] = None, pthreshold: Optional[int] = None, cthreshold: Optional[int] = None, grey: Optional[int] = None) -> 'VideoNode': ...
    def SCSelect(self, input: 'VideoNode', sceneBegin: 'VideoNode', sceneEnd: 'VideoNode', globalMotion: 'VideoNode', dfactor: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_rdvs_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "rdvs" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DupBlocks(self, gmthreshold: Optional[int] = None, mthreshold: Optional[int] = None, noise: Optional[int] = None, noisy: Optional[int] = None, dist: Optional[int] = None, tolerance: Optional[int] = None, dmode: Optional[int] = None, pthreshold: Optional[int] = None, cthreshold: Optional[int] = None, grey: Optional[int] = None) -> 'VideoNode': ...
    def RestoreMotionBlocks(self, restore: 'VideoNode', neighbour: Optional['VideoNode'] = None, neighbour2: Optional['VideoNode'] = None, alternative: Optional['VideoNode'] = None, gmthreshold: Optional[int] = None, mthreshold: Optional[int] = None, noise: Optional[int] = None, noisy: Optional[int] = None, dist: Optional[int] = None, tolerance: Optional[int] = None, dmode: Optional[int] = None, pthreshold: Optional[int] = None, cthreshold: Optional[int] = None, grey: Optional[int] = None) -> 'VideoNode': ...
    def SCSelect(self, sceneBegin: 'VideoNode', sceneEnd: 'VideoNode', globalMotion: 'VideoNode', dfactor: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: reduceflicker

class _Plugin_reduceflicker_Core_Bound(Plugin):
    """This class implements the module definitions for the "reduceflicker" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ReduceFlicker(self, clip: 'VideoNode', strength: Optional[int] = None, aggressive: Optional[int] = None, grey: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_reduceflicker_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "reduceflicker" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ReduceFlicker(self, strength: Optional[int] = None, aggressive: Optional[int] = None, grey: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: resize

class _Plugin_resize_Core_Bound(Plugin):
    """This class implements the module definitions for the "resize" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Bicubic(self, clip: 'VideoNode', width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Bilinear(self, clip: 'VideoNode', width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Bob(self, clip: 'VideoNode', filter: Optional[DataType] = None, tff: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Lanczos(self, clip: 'VideoNode', width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Point(self, clip: 'VideoNode', width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Spline16(self, clip: 'VideoNode', width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Spline36(self, clip: 'VideoNode', width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Spline64(self, clip: 'VideoNode', width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_resize_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "resize" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Bicubic(self, width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Bilinear(self, width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Bob(self, filter: Optional[DataType] = None, tff: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Lanczos(self, width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Point(self, width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Spline16(self, width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Spline36(self, width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...
    def Spline64(self, width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, matrix: Optional[int] = None, matrix_s: Optional[DataType] = None, transfer: Optional[int] = None, transfer_s: Optional[DataType] = None, primaries: Optional[int] = None, primaries_s: Optional[DataType] = None, range: Optional[int] = None, range_s: Optional[DataType] = None, chromaloc: Optional[int] = None, chromaloc_s: Optional[DataType] = None, matrix_in: Optional[int] = None, matrix_in_s: Optional[DataType] = None, transfer_in: Optional[int] = None, transfer_in_s: Optional[DataType] = None, primaries_in: Optional[int] = None, primaries_in_s: Optional[DataType] = None, range_in: Optional[int] = None, range_in_s: Optional[DataType] = None, chromaloc_in: Optional[int] = None, chromaloc_in_s: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, resample_filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, dither_type: Optional[DataType] = None, cpu_type: Optional[DataType] = None, prefer_props: Optional[int] = None, src_left: Optional[float] = None, src_top: Optional[float] = None, src_width: Optional[float] = None, src_height: Optional[float] = None, nominal_luminance: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: retinex

class _Plugin_retinex_Core_Bound(Plugin):
    """This class implements the module definitions for the "retinex" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def MSRCP(self, input: 'VideoNode', sigma: Optional[SingleAndSequence[float]] = None, lower_thr: Optional[float] = None, upper_thr: Optional[float] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, chroma_protect: Optional[float] = None) -> 'VideoNode': ...
    def MSRCR(self, input: 'VideoNode', sigma: Optional[SingleAndSequence[float]] = None, lower_thr: Optional[float] = None, upper_thr: Optional[float] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, restore: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_retinex_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "retinex" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def MSRCP(self, sigma: Optional[SingleAndSequence[float]] = None, lower_thr: Optional[float] = None, upper_thr: Optional[float] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, chroma_protect: Optional[float] = None) -> 'VideoNode': ...
    def MSRCR(self, sigma: Optional[SingleAndSequence[float]] = None, lower_thr: Optional[float] = None, upper_thr: Optional[float] = None, fulls: Optional[int] = None, fulld: Optional[int] = None, restore: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: rf

class _Plugin_rf_Core_Bound(Plugin):
    """This class implements the module definitions for the "rf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Replace(self, clip: 'VideoNode', clips: SingleAndSequence['VideoNode'], intervals: SingleAndSequence[DataType]) -> 'VideoNode': ...

class _Plugin_rf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "rf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Replace(self, clips: SingleAndSequence['VideoNode'], intervals: SingleAndSequence[DataType]) -> 'VideoNode': ...

# end implementation


# implementation: sangnom

class _Plugin_sangnom_Core_Bound(Plugin):
    """This class implements the module definitions for the "sangnom" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def SangNom(self, clip: 'VideoNode', order: Optional[int] = None, dh: Optional[int] = None, aa: Optional[SingleAndSequence[int]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_sangnom_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "sangnom" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def SangNom(self, order: Optional[int] = None, dh: Optional[int] = None, aa: Optional[SingleAndSequence[int]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: scd

class _Plugin_scd_Core_Bound(Plugin):
    """This class implements the module definitions for the "scd" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ApplyLog(self, clip: 'VideoNode', log: DataType) -> 'VideoNode': ...
    def Detect(self, clip: 'VideoNode', thresh: Optional[int] = None, interval_h: Optional[int] = None, interval_v: Optional[int] = None, log: Optional[DataType] = None) -> 'VideoNode': ...

class _Plugin_scd_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "scd" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ApplyLog(self, log: DataType) -> 'VideoNode': ...
    def Detect(self, thresh: Optional[int] = None, interval_h: Optional[int] = None, interval_v: Optional[int] = None, log: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation


# implementation: scrawl

class _Plugin_scrawl_Core_Bound(Plugin):
    """This class implements the module definitions for the "scrawl" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ClipInfo(self, clip: 'VideoNode', alignment: Optional[int] = None) -> 'VideoNode': ...
    def CoreInfo(self, clip: 'VideoNode', alignment: Optional[int] = None) -> 'VideoNode': ...
    def FrameNum(self, clip: 'VideoNode', alignment: Optional[int] = None) -> 'VideoNode': ...
    def FrameProps(self, clip: 'VideoNode', alignment: Optional[int] = None) -> 'VideoNode': ...
    def Text(self, clip: 'VideoNode', text: DataType, alignment: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_scrawl_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "scrawl" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ClipInfo(self, alignment: Optional[int] = None) -> 'VideoNode': ...
    def CoreInfo(self, alignment: Optional[int] = None) -> 'VideoNode': ...
    def FrameNum(self, alignment: Optional[int] = None) -> 'VideoNode': ...
    def FrameProps(self, alignment: Optional[int] = None) -> 'VideoNode': ...
    def Text(self, text: DataType, alignment: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: scxvid

class _Plugin_scxvid_Core_Bound(Plugin):
    """This class implements the module definitions for the "scxvid" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Scxvid(self, clip: 'VideoNode', log: Optional[DataType] = None, use_slices: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_scxvid_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "scxvid" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Scxvid(self, log: Optional[DataType] = None, use_slices: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: std

class _Plugin_std_Core_Bound(Plugin):
    """This class implements the module definitions for the "std" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def AddBorders(self, clip: 'VideoNode', left: Optional[int] = None, right: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None, color: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...
    def AssumeFPS(self, clip: 'VideoNode', src: Optional['VideoNode'] = None, fpsnum: Optional[int] = None, fpsden: Optional[int] = None) -> 'VideoNode': ...
    def AssumeSampleRate(self, clip: 'AudioNode', src: Optional['AudioNode'] = None, samplerate: Optional[int] = None) -> 'AudioNode': ...
    def AudioGain(self, clip: 'AudioNode', gain: Optional[SingleAndSequence[float]] = None) -> 'AudioNode': ...
    def AudioLoop(self, clip: 'AudioNode', times: Optional[int] = None) -> 'AudioNode': ...
    def AudioMix(self, clips: SingleAndSequence['AudioNode'], matrix: SingleAndSequence[float], channels_out: SingleAndSequence[int]) -> 'AudioNode': ...
    def AudioReverse(self, clip: 'AudioNode') -> 'AudioNode': ...
    def AudioSplice(self, clips: SingleAndSequence['AudioNode']) -> 'AudioNode': ...
    def AudioTrim(self, clip: 'AudioNode', first: Optional[int] = None, last: Optional[int] = None, length: Optional[int] = None) -> 'AudioNode': ...
    def AverageFrames(self, clips: SingleAndSequence['VideoNode'], weights: SingleAndSequence[float], scale: Optional[float] = None, scenechange: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Binarize(self, clip: 'VideoNode', threshold: Optional[SingleAndSequence[float]] = None, v0: Optional[SingleAndSequence[float]] = None, v1: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def BinarizeMask(self, clip: 'VideoNode', threshold: Optional[SingleAndSequence[float]] = None, v0: Optional[SingleAndSequence[float]] = None, v1: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def BlankAudio(self, clip: Optional['AudioNode'] = None, channels: Optional[SingleAndSequence[int]] = None, bits: Optional[int] = None, sampletype: Optional[int] = None, samplerate: Optional[int] = None, length: Optional[int] = None, keep: Optional[int] = None) -> 'AudioNode': ...
    def BlankClip(self, clip: Optional['VideoNode'] = None, width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, length: Optional[int] = None, fpsnum: Optional[int] = None, fpsden: Optional[int] = None, color: Optional[SingleAndSequence[float]] = None, keep: Optional[int] = None, varsize: Optional[int] = None, varformat: Optional[int] = None) -> 'VideoNode': ...
    def BoxBlur(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, hradius: Optional[int] = None, hpasses: Optional[int] = None, vradius: Optional[int] = None, vpasses: Optional[int] = None) -> 'VideoNode': ...
    def Cache(self, clip: 'VideoNode', size: Optional[int] = None, fixed: Optional[int] = None, make_linear: Optional[int] = None) -> 'VideoNode': ...
    def ClipToProp(self, clip: 'VideoNode', mclip: 'VideoNode', prop: Optional[DataType] = None) -> 'VideoNode': ...
    def Convolution(self, clip: 'VideoNode', matrix: SingleAndSequence[float], bias: Optional[float] = None, divisor: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None, saturate: Optional[int] = None, mode: Optional[DataType] = None) -> 'VideoNode': ...
    def CopyFrameProps(self, clip: 'VideoNode', prop_src: 'VideoNode') -> 'VideoNode': ...
    def Crop(self, clip: 'VideoNode', left: Optional[int] = None, right: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None) -> 'VideoNode': ...
    def CropAbs(self, clip: 'VideoNode', width: int, height: int, left: Optional[int] = None, top: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None) -> 'VideoNode': ...
    def CropRel(self, clip: 'VideoNode', left: Optional[int] = None, right: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None) -> 'VideoNode': ...
    def Deflate(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, threshold: Optional[float] = None) -> 'VideoNode': ...
    def DeleteFrames(self, clip: 'VideoNode', frames: SingleAndSequence[int]) -> 'VideoNode': ...
    def DoubleWeave(self, clip: 'VideoNode', tff: Optional[int] = None) -> 'VideoNode': ...
    def DuplicateFrames(self, clip: 'VideoNode', frames: SingleAndSequence[int]) -> 'VideoNode': ...
    def Expr(self, clips: SingleAndSequence['VideoNode'], expr: SingleAndSequence[DataType], format: Optional[int] = None) -> 'VideoNode': ...
    def FlipHorizontal(self, clip: 'VideoNode') -> 'VideoNode': ...
    def FlipVertical(self, clip: 'VideoNode') -> 'VideoNode': ...
    def FrameEval(self, clip: 'VideoNode', eval: VSMapValueCallback[_VapourSynthMapValue], prop_src: Optional[SingleAndSequence[VideoNode]] = None, clip_src: Optional[SingleAndSequence[VideoNode]] = None) -> 'VideoNode': ...
    def FreezeFrames(self, clip: 'VideoNode', first: Optional[SingleAndSequence[int]] = None, last: Optional[SingleAndSequence[int]] = None, replacement: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Inflate(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, threshold: Optional[float] = None) -> 'VideoNode': ...
    def Interleave(self, clips: SingleAndSequence['VideoNode'], extend: Optional[int] = None, mismatch: Optional[int] = None, modify_duration: Optional[int] = None) -> 'VideoNode': ...
    def Invert(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def InvertMask(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Levels(self, clip: 'VideoNode', min_in: Optional[SingleAndSequence[float]] = None, max_in: Optional[SingleAndSequence[float]] = None, gamma: Optional[SingleAndSequence[float]] = None, min_out: Optional[SingleAndSequence[float]] = None, max_out: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Limiter(self, clip: 'VideoNode', min: Optional[SingleAndSequence[float]] = None, max: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def LoadAllPlugins(self, path: DataType) -> None: ...
    def LoadPlugin(self, path: DataType, altsearchpath: Optional[int] = None, forcens: Optional[DataType] = None, forceid: Optional[DataType] = None) -> None: ...
    def Loop(self, clip: 'VideoNode', times: Optional[int] = None) -> 'VideoNode': ...
    def Lut(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, lut: Optional[SingleAndSequence[int]] = None, lutf: Optional[SingleAndSequence[float]] = None, function: Optional[VSMapValueCallback[_VapourSynthMapValue]] = None, bits: Optional[int] = None, floatout: Optional[int] = None) -> 'VideoNode': ...
    def Lut2(self, clipa: 'VideoNode', clipb: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, lut: Optional[SingleAndSequence[int]] = None, lutf: Optional[SingleAndSequence[float]] = None, function: Optional[VSMapValueCallback[_VapourSynthMapValue]] = None, bits: Optional[int] = None, floatout: Optional[int] = None) -> 'VideoNode': ...
    def MakeDiff(self, clipa: 'VideoNode', clipb: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def MakeFullDiff(self, clipa: 'VideoNode', clipb: 'VideoNode') -> 'VideoNode': ...
    def MaskedMerge(self, clipa: 'VideoNode', clipb: 'VideoNode', mask: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, first_plane: Optional[int] = None, premultiplied: Optional[int] = None) -> 'VideoNode': ...
    def Maximum(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, threshold: Optional[float] = None, coordinates: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Median(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Merge(self, clipa: 'VideoNode', clipb: 'VideoNode', weight: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...
    def MergeDiff(self, clipa: 'VideoNode', clipb: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def MergeFullDiff(self, clipa: 'VideoNode', clipb: 'VideoNode') -> 'VideoNode': ...
    def Minimum(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, threshold: Optional[float] = None, coordinates: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def ModifyFrame(self, clip: 'VideoNode', clips: SingleAndSequence['VideoNode'], selector: VSMapValueCallback[_VapourSynthMapValue]) -> 'VideoNode': ...
    def PEMVerifier(self, clip: 'VideoNode', upper: Optional[SingleAndSequence[float]] = None, lower: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...
    def PlaneStats(self, clipa: 'VideoNode', clipb: Optional['VideoNode'] = None, plane: Optional[int] = None, prop: Optional[DataType] = None) -> 'VideoNode': ...
    def PreMultiply(self, clip: 'VideoNode', alpha: 'VideoNode') -> 'VideoNode': ...
    def Prewitt(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, scale: Optional[float] = None) -> 'VideoNode': ...
    def PropToClip(self, clip: 'VideoNode', prop: Optional[DataType] = None) -> 'VideoNode': ...
    def RemoveFrameProps(self, clip: 'VideoNode', props: Optional[SingleAndSequence[DataType]] = None) -> 'VideoNode': ...
    def Reverse(self, clip: 'VideoNode') -> 'VideoNode': ...
    def SelectEvery(self, clip: 'VideoNode', cycle: int, offsets: SingleAndSequence[int], modify_duration: Optional[int] = None) -> 'VideoNode': ...
    def SeparateFields(self, clip: 'VideoNode', tff: Optional[int] = None, modify_duration: Optional[int] = None) -> 'VideoNode': ...
    def SetAudioCache(self, clip: 'AudioNode', mode: Optional[int] = None, fixedsize: Optional[int] = None, maxsize: Optional[int] = None, maxhistory: Optional[int] = None) -> None: ...
    def SetFieldBased(self, clip: 'VideoNode', value: int) -> 'VideoNode': ...
    def SetFrameProp(self, clip: 'VideoNode', prop: DataType, intval: Optional[SingleAndSequence[int]] = None, floatval: Optional[SingleAndSequence[float]] = None, data: Optional[SingleAndSequence[DataType]] = None) -> 'VideoNode': ...
    def SetFrameProps(self, clip: 'VideoNode', **kwargs: _VapourSynthMapValue) -> 'VideoNode': ...
    def SetMaxCPU(self, cpu: DataType) -> DataType: ...
    def SetVideoCache(self, clip: 'VideoNode', mode: Optional[int] = None, fixedsize: Optional[int] = None, maxsize: Optional[int] = None, maxhistory: Optional[int] = None) -> None: ...
    def ShuffleChannels(self, clips: SingleAndSequence['AudioNode'], channels_in: SingleAndSequence[int], channels_out: SingleAndSequence[int]) -> 'AudioNode': ...
    def ShufflePlanes(self, clips: SingleAndSequence['VideoNode'], planes: SingleAndSequence[int], colorfamily: int) -> 'VideoNode': ...
    def Sobel(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, scale: Optional[float] = None) -> 'VideoNode': ...
    def Splice(self, clips: SingleAndSequence['VideoNode'], mismatch: Optional[int] = None) -> 'VideoNode': ...
    def SplitChannels(self, clip: 'AudioNode') -> SingleAndSequence['AudioNode']: ...
    def SplitPlanes(self, clip: 'VideoNode') -> SingleAndSequence['VideoNode']: ...
    def StackHorizontal(self, clips: SingleAndSequence['VideoNode']) -> 'VideoNode': ...
    def StackVertical(self, clips: SingleAndSequence['VideoNode']) -> 'VideoNode': ...
    def TestAudio(self, channels: Optional[SingleAndSequence[int]] = None, bits: Optional[int] = None, isfloat: Optional[int] = None, samplerate: Optional[int] = None, length: Optional[int] = None) -> 'AudioNode': ...
    def Transpose(self, clip: 'VideoNode') -> 'VideoNode': ...
    def Trim(self, clip: 'VideoNode', first: Optional[int] = None, last: Optional[int] = None, length: Optional[int] = None) -> 'VideoNode': ...
    def Turn180(self, clip: 'VideoNode') -> 'VideoNode': ...

class _Plugin_std_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "std" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def AddBorders(self, left: Optional[int] = None, right: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None, color: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...
    def AssumeFPS(self, src: Optional['VideoNode'] = None, fpsnum: Optional[int] = None, fpsden: Optional[int] = None) -> 'VideoNode': ...
    def AverageFrames(self, weights: SingleAndSequence[float], scale: Optional[float] = None, scenechange: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Binarize(self, threshold: Optional[SingleAndSequence[float]] = None, v0: Optional[SingleAndSequence[float]] = None, v1: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def BinarizeMask(self, threshold: Optional[SingleAndSequence[float]] = None, v0: Optional[SingleAndSequence[float]] = None, v1: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def BlankClip(self, width: Optional[int] = None, height: Optional[int] = None, format: Optional[int] = None, length: Optional[int] = None, fpsnum: Optional[int] = None, fpsden: Optional[int] = None, color: Optional[SingleAndSequence[float]] = None, keep: Optional[int] = None, varsize: Optional[int] = None, varformat: Optional[int] = None) -> 'VideoNode': ...
    def BoxBlur(self, planes: Optional[SingleAndSequence[int]] = None, hradius: Optional[int] = None, hpasses: Optional[int] = None, vradius: Optional[int] = None, vpasses: Optional[int] = None) -> 'VideoNode': ...
    def Cache(self, size: Optional[int] = None, fixed: Optional[int] = None, make_linear: Optional[int] = None) -> 'VideoNode': ...
    def ClipToProp(self, mclip: 'VideoNode', prop: Optional[DataType] = None) -> 'VideoNode': ...
    def Convolution(self, matrix: SingleAndSequence[float], bias: Optional[float] = None, divisor: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None, saturate: Optional[int] = None, mode: Optional[DataType] = None) -> 'VideoNode': ...
    def CopyFrameProps(self, prop_src: 'VideoNode') -> 'VideoNode': ...
    def Crop(self, left: Optional[int] = None, right: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None) -> 'VideoNode': ...
    def CropAbs(self, width: int, height: int, left: Optional[int] = None, top: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None) -> 'VideoNode': ...
    def CropRel(self, left: Optional[int] = None, right: Optional[int] = None, top: Optional[int] = None, bottom: Optional[int] = None) -> 'VideoNode': ...
    def Deflate(self, planes: Optional[SingleAndSequence[int]] = None, threshold: Optional[float] = None) -> 'VideoNode': ...
    def DeleteFrames(self, frames: SingleAndSequence[int]) -> 'VideoNode': ...
    def DoubleWeave(self, tff: Optional[int] = None) -> 'VideoNode': ...
    def DuplicateFrames(self, frames: SingleAndSequence[int]) -> 'VideoNode': ...
    def Expr(self, expr: SingleAndSequence[DataType], format: Optional[int] = None) -> 'VideoNode': ...
    def FlipHorizontal(self) -> 'VideoNode': ...
    def FlipVertical(self) -> 'VideoNode': ...
    def FrameEval(self, eval: VSMapValueCallback[_VapourSynthMapValue], prop_src: Optional[SingleAndSequence[VideoNode]] = None, clip_src: Optional[SingleAndSequence[VideoNode]] = None) -> 'VideoNode': ...
    def FreezeFrames(self, first: Optional[SingleAndSequence[int]] = None, last: Optional[SingleAndSequence[int]] = None, replacement: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Inflate(self, planes: Optional[SingleAndSequence[int]] = None, threshold: Optional[float] = None) -> 'VideoNode': ...
    def Interleave(self, extend: Optional[int] = None, mismatch: Optional[int] = None, modify_duration: Optional[int] = None) -> 'VideoNode': ...
    def Invert(self, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def InvertMask(self, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Levels(self, min_in: Optional[SingleAndSequence[float]] = None, max_in: Optional[SingleAndSequence[float]] = None, gamma: Optional[SingleAndSequence[float]] = None, min_out: Optional[SingleAndSequence[float]] = None, max_out: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Limiter(self, min: Optional[SingleAndSequence[float]] = None, max: Optional[SingleAndSequence[float]] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Loop(self, times: Optional[int] = None) -> 'VideoNode': ...
    def Lut(self, planes: Optional[SingleAndSequence[int]] = None, lut: Optional[SingleAndSequence[int]] = None, lutf: Optional[SingleAndSequence[float]] = None, function: Optional[VSMapValueCallback[_VapourSynthMapValue]] = None, bits: Optional[int] = None, floatout: Optional[int] = None) -> 'VideoNode': ...
    def Lut2(self, clipb: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, lut: Optional[SingleAndSequence[int]] = None, lutf: Optional[SingleAndSequence[float]] = None, function: Optional[VSMapValueCallback[_VapourSynthMapValue]] = None, bits: Optional[int] = None, floatout: Optional[int] = None) -> 'VideoNode': ...
    def MakeDiff(self, clipb: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def MakeFullDiff(self, clipb: 'VideoNode') -> 'VideoNode': ...
    def MaskedMerge(self, clipb: 'VideoNode', mask: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, first_plane: Optional[int] = None, premultiplied: Optional[int] = None) -> 'VideoNode': ...
    def Maximum(self, planes: Optional[SingleAndSequence[int]] = None, threshold: Optional[float] = None, coordinates: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Median(self, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Merge(self, clipb: 'VideoNode', weight: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...
    def MergeDiff(self, clipb: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def MergeFullDiff(self, clipb: 'VideoNode') -> 'VideoNode': ...
    def Minimum(self, planes: Optional[SingleAndSequence[int]] = None, threshold: Optional[float] = None, coordinates: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def ModifyFrame(self, clips: SingleAndSequence['VideoNode'], selector: VSMapValueCallback[_VapourSynthMapValue]) -> 'VideoNode': ...
    def PEMVerifier(self, upper: Optional[SingleAndSequence[float]] = None, lower: Optional[SingleAndSequence[float]] = None) -> 'VideoNode': ...
    def PlaneStats(self, clipb: Optional['VideoNode'] = None, plane: Optional[int] = None, prop: Optional[DataType] = None) -> 'VideoNode': ...
    def PreMultiply(self, alpha: 'VideoNode') -> 'VideoNode': ...
    def Prewitt(self, planes: Optional[SingleAndSequence[int]] = None, scale: Optional[float] = None) -> 'VideoNode': ...
    def PropToClip(self, prop: Optional[DataType] = None) -> 'VideoNode': ...
    def RemoveFrameProps(self, props: Optional[SingleAndSequence[DataType]] = None) -> 'VideoNode': ...
    def Reverse(self) -> 'VideoNode': ...
    def SelectEvery(self, cycle: int, offsets: SingleAndSequence[int], modify_duration: Optional[int] = None) -> 'VideoNode': ...
    def SeparateFields(self, tff: Optional[int] = None, modify_duration: Optional[int] = None) -> 'VideoNode': ...
    def SetFieldBased(self, value: int) -> 'VideoNode': ...
    def SetFrameProp(self, prop: DataType, intval: Optional[SingleAndSequence[int]] = None, floatval: Optional[SingleAndSequence[float]] = None, data: Optional[SingleAndSequence[DataType]] = None) -> 'VideoNode': ...
    def SetFrameProps(self, **kwargs: Any) -> 'VideoNode': ...
    def SetVideoCache(self, mode: Optional[int] = None, fixedsize: Optional[int] = None, maxsize: Optional[int] = None, maxhistory: Optional[int] = None) -> None: ...
    def ShufflePlanes(self, planes: SingleAndSequence[int], colorfamily: int) -> 'VideoNode': ...
    def Sobel(self, planes: Optional[SingleAndSequence[int]] = None, scale: Optional[float] = None) -> 'VideoNode': ...
    def Splice(self, mismatch: Optional[int] = None) -> 'VideoNode': ...
    def SplitPlanes(self) -> SingleAndSequence['VideoNode']: ...
    def StackHorizontal(self) -> 'VideoNode': ...
    def StackVertical(self) -> 'VideoNode': ...
    def Transpose(self) -> 'VideoNode': ...
    def Trim(self, first: Optional[int] = None, last: Optional[int] = None, length: Optional[int] = None) -> 'VideoNode': ...
    def Turn180(self) -> 'VideoNode': ...

class _Plugin_std_AudioNode_Bound(Plugin):
    """This class implements the module definitions for the "std" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def AssumeSampleRate(self, src: Optional['AudioNode'] = None, samplerate: Optional[int] = None) -> 'AudioNode': ...
    def AudioGain(self, gain: Optional[SingleAndSequence[float]] = None) -> 'AudioNode': ...
    def AudioLoop(self, times: Optional[int] = None) -> 'AudioNode': ...
    def AudioMix(self, matrix: SingleAndSequence[float], channels_out: SingleAndSequence[int]) -> 'AudioNode': ...
    def AudioReverse(self) -> 'AudioNode': ...
    def AudioSplice(self) -> 'AudioNode': ...
    def AudioTrim(self, first: Optional[int] = None, last: Optional[int] = None, length: Optional[int] = None) -> 'AudioNode': ...
    def BlankAudio(self, channels: Optional[SingleAndSequence[int]] = None, bits: Optional[int] = None, sampletype: Optional[int] = None, samplerate: Optional[int] = None, length: Optional[int] = None, keep: Optional[int] = None) -> 'AudioNode': ...
    def SetAudioCache(self, mode: Optional[int] = None, fixedsize: Optional[int] = None, maxsize: Optional[int] = None, maxhistory: Optional[int] = None) -> None: ...
    def ShuffleChannels(self, channels_in: SingleAndSequence[int], channels_out: SingleAndSequence[int]) -> 'AudioNode': ...
    def SplitChannels(self) -> SingleAndSequence['AudioNode']: ...

# end implementation


# implementation: surfaceblur

class _Plugin_surfaceblur_Core_Bound(Plugin):
    """This class implements the module definitions for the "surfaceblur" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def surfaceblur(self, input: 'VideoNode', threshold: Optional[float] = None, radius: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_surfaceblur_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "surfaceblur" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def surfaceblur(self, threshold: Optional[float] = None, radius: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: svp1

class _Plugin_svp1_Core_Bound(Plugin):
    """This class implements the module definitions for the "svp1" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Analyse(self, clip: 'VideoNode', sdata: int, src: 'VideoNode', opt: DataType) -> 'VideoNode': ...
    def Super(self, clip: 'VideoNode', opt: DataType) -> 'VideoNode': ...

class _Plugin_svp1_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "svp1" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Analyse(self, sdata: int, src: 'VideoNode', opt: DataType) -> 'VideoNode': ...
    def Super(self, opt: DataType) -> 'VideoNode': ...

# end implementation


# implementation: svp2

class _Plugin_svp2_Core_Bound(Plugin):
    """This class implements the module definitions for the "svp2" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def SmoothFps(self, clip: 'VideoNode', super: 'VideoNode', sdata: int, vectors: 'VideoNode', vdata: int, opt: DataType, src: Optional['VideoNode'] = None, fps: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_svp2_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "svp2" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def SmoothFps(self, super: 'VideoNode', sdata: int, vectors: 'VideoNode', vdata: int, opt: DataType, src: Optional['VideoNode'] = None, fps: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: tcanny

class _Plugin_tcanny_Core_Bound(Plugin):
    """This class implements the module definitions for the "tcanny" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TCanny(self, clip: 'VideoNode', sigma: Optional[SingleAndSequence[float]] = None, sigma_v: Optional[SingleAndSequence[float]] = None, t_h: Optional[float] = None, t_l: Optional[float] = None, mode: Optional[int] = None, op: Optional[int] = None, scale: Optional[float] = None, opt: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_tcanny_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "tcanny" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TCanny(self, sigma: Optional[SingleAndSequence[float]] = None, sigma_v: Optional[SingleAndSequence[float]] = None, t_h: Optional[float] = None, t_l: Optional[float] = None, mode: Optional[int] = None, op: Optional[int] = None, scale: Optional[float] = None, opt: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: tdm

class _Plugin_tdm_Core_Bound(Plugin):
    """This class implements the module definitions for the "tdm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def IsCombed(self, clip: 'VideoNode', cthresh: Optional[int] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, chroma: Optional[int] = None, mi: Optional[int] = None, metric: Optional[int] = None) -> 'VideoNode': ...
    def TDeintMod(self, clip: 'VideoNode', order: int, field: Optional[int] = None, mode: Optional[int] = None, length: Optional[int] = None, mtype: Optional[int] = None, ttype: Optional[int] = None, mtql: Optional[int] = None, mthl: Optional[int] = None, mtqc: Optional[int] = None, mthc: Optional[int] = None, nt: Optional[int] = None, minthresh: Optional[int] = None, maxthresh: Optional[int] = None, cstr: Optional[int] = None, athresh: Optional[int] = None, metric: Optional[int] = None, expand: Optional[int] = None, link: Optional[int] = None, show: Optional[int] = None, edeint: Optional['VideoNode'] = None, opt: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_tdm_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "tdm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def IsCombed(self, cthresh: Optional[int] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, chroma: Optional[int] = None, mi: Optional[int] = None, metric: Optional[int] = None) -> 'VideoNode': ...
    def TDeintMod(self, order: int, field: Optional[int] = None, mode: Optional[int] = None, length: Optional[int] = None, mtype: Optional[int] = None, ttype: Optional[int] = None, mtql: Optional[int] = None, mthl: Optional[int] = None, mtqc: Optional[int] = None, mthc: Optional[int] = None, nt: Optional[int] = None, minthresh: Optional[int] = None, maxthresh: Optional[int] = None, cstr: Optional[int] = None, athresh: Optional[int] = None, metric: Optional[int] = None, expand: Optional[int] = None, link: Optional[int] = None, show: Optional[int] = None, edeint: Optional['VideoNode'] = None, opt: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: tedgemask

class _Plugin_tedgemask_Core_Bound(Plugin):
    """This class implements the module definitions for the "tedgemask" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TEdgeMask(self, clip: 'VideoNode', threshold: Optional[SingleAndSequence[float]] = None, type: Optional[int] = None, link: Optional[int] = None, scale: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_tedgemask_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "tedgemask" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TEdgeMask(self, threshold: Optional[SingleAndSequence[float]] = None, type: Optional[int] = None, link: Optional[int] = None, scale: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: text

class _Plugin_text_Core_Bound(Plugin):
    """This class implements the module definitions for the "text" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ClipInfo(self, clip: 'VideoNode', alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...
    def CoreInfo(self, clip: Optional['VideoNode'] = None, alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...
    def FrameNum(self, clip: 'VideoNode', alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...
    def FrameProps(self, clip: 'VideoNode', props: Optional[SingleAndSequence[DataType]] = None, alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...
    def Text(self, clip: 'VideoNode', text: DataType, alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_text_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "text" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ClipInfo(self, alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...
    def CoreInfo(self, alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...
    def FrameNum(self, alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...
    def FrameProps(self, props: Optional[SingleAndSequence[DataType]] = None, alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...
    def Text(self, text: DataType, alignment: Optional[int] = None, scale: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: tivtc

class _Plugin_tivtc_Core_Bound(Plugin):
    """This class implements the module definitions for the "tivtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TDecimate(self, clip: 'VideoNode', mode: Optional[int] = None, cycleR: Optional[int] = None, cycle: Optional[int] = None, rate: Optional[float] = None, dupThresh: Optional[float] = None, vidThresh: Optional[float] = None, sceneThresh: Optional[float] = None, hybrid: Optional[int] = None, vidDetect: Optional[int] = None, conCycle: Optional[int] = None, conCycleTP: Optional[int] = None, ovr: Optional[DataType] = None, output: Optional[DataType] = None, input: Optional[DataType] = None, tfmIn: Optional[DataType] = None, mkvOut: Optional[DataType] = None, nt: Optional[int] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, debug: Optional[int] = None, display: Optional[int] = None, vfrDec: Optional[int] = None, batch: Optional[int] = None, tcfv1: Optional[int] = None, se: Optional[int] = None, chroma: Optional[int] = None, exPP: Optional[int] = None, maxndl: Optional[int] = None, m2PA: Optional[int] = None, denoise: Optional[int] = None, noblend: Optional[int] = None, ssd: Optional[int] = None, hint: Optional[int] = None, clip2: Optional['VideoNode'] = None, sdlim: Optional[int] = None, opt: Optional[int] = None, orgOut: Optional[DataType] = None) -> 'VideoNode': ...
    def TFM(self, clip: 'VideoNode', order: Optional[int] = None, field: Optional[int] = None, mode: Optional[int] = None, PP: Optional[int] = None, ovr: Optional[DataType] = None, input: Optional[DataType] = None, output: Optional[DataType] = None, outputC: Optional[DataType] = None, debug: Optional[int] = None, display: Optional[int] = None, slow: Optional[int] = None, mChroma: Optional[int] = None, cNum: Optional[int] = None, cthresh: Optional[int] = None, MI: Optional[int] = None, chroma: Optional[int] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, y0: Optional[int] = None, y1: Optional[int] = None, mthresh: Optional[int] = None, clip2: Optional['VideoNode'] = None, d2v: Optional[DataType] = None, ovrDefault: Optional[int] = None, flags: Optional[int] = None, scthresh: Optional[float] = None, micout: Optional[int] = None, micmatching: Optional[int] = None, trimIn: Optional[DataType] = None, hint: Optional[int] = None, metric: Optional[int] = None, batch: Optional[int] = None, ubsco: Optional[int] = None, mmsco: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_tivtc_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "tivtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TDecimate(self, mode: Optional[int] = None, cycleR: Optional[int] = None, cycle: Optional[int] = None, rate: Optional[float] = None, dupThresh: Optional[float] = None, vidThresh: Optional[float] = None, sceneThresh: Optional[float] = None, hybrid: Optional[int] = None, vidDetect: Optional[int] = None, conCycle: Optional[int] = None, conCycleTP: Optional[int] = None, ovr: Optional[DataType] = None, output: Optional[DataType] = None, input: Optional[DataType] = None, tfmIn: Optional[DataType] = None, mkvOut: Optional[DataType] = None, nt: Optional[int] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, debug: Optional[int] = None, display: Optional[int] = None, vfrDec: Optional[int] = None, batch: Optional[int] = None, tcfv1: Optional[int] = None, se: Optional[int] = None, chroma: Optional[int] = None, exPP: Optional[int] = None, maxndl: Optional[int] = None, m2PA: Optional[int] = None, denoise: Optional[int] = None, noblend: Optional[int] = None, ssd: Optional[int] = None, hint: Optional[int] = None, clip2: Optional['VideoNode'] = None, sdlim: Optional[int] = None, opt: Optional[int] = None, orgOut: Optional[DataType] = None) -> 'VideoNode': ...
    def TFM(self, order: Optional[int] = None, field: Optional[int] = None, mode: Optional[int] = None, PP: Optional[int] = None, ovr: Optional[DataType] = None, input: Optional[DataType] = None, output: Optional[DataType] = None, outputC: Optional[DataType] = None, debug: Optional[int] = None, display: Optional[int] = None, slow: Optional[int] = None, mChroma: Optional[int] = None, cNum: Optional[int] = None, cthresh: Optional[int] = None, MI: Optional[int] = None, chroma: Optional[int] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, y0: Optional[int] = None, y1: Optional[int] = None, mthresh: Optional[int] = None, clip2: Optional['VideoNode'] = None, d2v: Optional[DataType] = None, ovrDefault: Optional[int] = None, flags: Optional[int] = None, scthresh: Optional[float] = None, micout: Optional[int] = None, micmatching: Optional[int] = None, trimIn: Optional[DataType] = None, hint: Optional[int] = None, metric: Optional[int] = None, batch: Optional[int] = None, ubsco: Optional[int] = None, mmsco: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: tmap

class _Plugin_tmap_Core_Bound(Plugin):
    """This class implements the module definitions for the "tmap" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def tm(self, clip: 'VideoNode', source_peak: float, desat: Optional[float] = None, lin: Optional[int] = None, show_satmask: Optional[int] = None, show_clipped: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_tmap_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "tmap" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def tm(self, source_peak: float, desat: Optional[float] = None, lin: Optional[int] = None, show_satmask: Optional[int] = None, show_clipped: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: tonemap

class _Plugin_tonemap_Core_Bound(Plugin):
    """This class implements the module definitions for the "tonemap" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Hable(self, clip: 'VideoNode', exposure: Optional[float] = None, a: Optional[float] = None, b: Optional[float] = None, c: Optional[float] = None, d: Optional[float] = None, e: Optional[float] = None, f: Optional[float] = None, w: Optional[float] = None) -> 'VideoNode': ...
    def Mobius(self, clip: 'VideoNode', exposure: Optional[float] = None, transition: Optional[float] = None, peak: Optional[float] = None) -> 'VideoNode': ...
    def Reinhard(self, clip: 'VideoNode', exposure: Optional[float] = None, contrast: Optional[float] = None, peak: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_tonemap_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "tonemap" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Hable(self, exposure: Optional[float] = None, a: Optional[float] = None, b: Optional[float] = None, c: Optional[float] = None, d: Optional[float] = None, e: Optional[float] = None, f: Optional[float] = None, w: Optional[float] = None) -> 'VideoNode': ...
    def Mobius(self, exposure: Optional[float] = None, transition: Optional[float] = None, peak: Optional[float] = None) -> 'VideoNode': ...
    def Reinhard(self, exposure: Optional[float] = None, contrast: Optional[float] = None, peak: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: trt

class _Plugin_trt_Core_Bound(Plugin):
    """This class implements the module definitions for the "trt" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DeviceProperties(self, device_id: Optional[int] = None) -> 'VideoNode': ...
    def Model(self, clips: SingleAndSequence['VideoNode'], engine_path: DataType, overlap: Optional[SingleAndSequence[int]] = None, tilesize: Optional[SingleAndSequence[int]] = None, device_id: Optional[int] = None, use_cuda_graph: Optional[int] = None, num_streams: Optional[int] = None, verbosity: Optional[int] = None) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...

class _Plugin_trt_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "trt" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Model(self, engine_path: DataType, overlap: Optional[SingleAndSequence[int]] = None, tilesize: Optional[SingleAndSequence[int]] = None, device_id: Optional[int] = None, use_cuda_graph: Optional[int] = None, num_streams: Optional[int] = None, verbosity: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: ttmpsm

class _Plugin_ttmpsm_Core_Bound(Plugin):
    """This class implements the module definitions for the "ttmpsm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TTempSmooth(self, clip: 'VideoNode', maxr: Optional[int] = None, thresh: Optional[SingleAndSequence[int]] = None, mdiff: Optional[SingleAndSequence[int]] = None, strength: Optional[int] = None, scthresh: Optional[float] = None, fp: Optional[int] = None, pfclip: Optional['VideoNode'] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_ttmpsm_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "ttmpsm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TTempSmooth(self, maxr: Optional[int] = None, thresh: Optional[SingleAndSequence[int]] = None, mdiff: Optional[SingleAndSequence[int]] = None, strength: Optional[int] = None, scthresh: Optional[float] = None, fp: Optional[int] = None, pfclip: Optional['VideoNode'] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: vcfreq

class _Plugin_vcfreq_Core_Bound(Plugin):
    """This class implements the module definitions for the "vcfreq" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Blur(self, clip: 'VideoNode', line: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None) -> 'VideoNode': ...
    def F1Quiver(self, clip: 'VideoNode', filter: SingleAndSequence[int], morph: Optional[int] = None, custom: Optional[int] = None, test: Optional[int] = None, strow: Optional[int] = None, nrows: Optional[int] = None, gamma: Optional[float] = None) -> 'VideoNode': ...
    def F2Quiver(self, *args: '_VapourSynthMapValue', **kwargs: '_VapourSynthMapValue') -> 'VideoNode': ...
    def Sharp(self, clip: 'VideoNode', line: Optional[int] = None, wn: Optional[float] = None, x: Optional[int] = None, y: Optional[int] = None, fr: Optional[int] = None, scale: Optional[float] = None) -> 'VideoNode': ...

class _Plugin_vcfreq_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "vcfreq" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Blur(self, line: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None) -> 'VideoNode': ...
    def F1Quiver(self, filter: SingleAndSequence[int], morph: Optional[int] = None, custom: Optional[int] = None, test: Optional[int] = None, strow: Optional[int] = None, nrows: Optional[int] = None, gamma: Optional[float] = None) -> 'VideoNode': ...
    def F2Quiver(self, *args: '_VapourSynthMapValue', **kwargs: '_VapourSynthMapValue') -> 'VideoNode': ...
    def Sharp(self, line: Optional[int] = None, wn: Optional[float] = None, x: Optional[int] = None, y: Optional[int] = None, fr: Optional[int] = None, scale: Optional[float] = None) -> 'VideoNode': ...

# end implementation


# implementation: vcmod

class _Plugin_vcmod_Core_Bound(Plugin):
    """This class implements the module definitions for the "vcmod" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Amplitude(self, *args: '_VapourSynthMapValue', **kwargs: '_VapourSynthMapValue') -> 'VideoNode': ...
    def Fan(self, clip: 'VideoNode', span: Optional[int] = None, edge: Optional[int] = None, plus: Optional[int] = None, minus: Optional[int] = None, uv: Optional[int] = None) -> 'VideoNode': ...
    def GBlur(self, clip: 'VideoNode', ksize: Optional[int] = None, sd: Optional[float] = None) -> 'VideoNode': ...
    def Histogram(self, clip: 'VideoNode', clipm: Optional['VideoNode'] = None, type: Optional[int] = None, table: Optional[SingleAndSequence[int]] = None, mf: Optional[int] = None, window: Optional[int] = None, limit: Optional[int] = None) -> 'VideoNode': ...
    def MBlur(self, clip: 'VideoNode', type: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None) -> 'VideoNode': ...
    def Median(self, clip: 'VideoNode', maxgrid: Optional[int] = None, plane: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Neural(self, clip: 'VideoNode', txt: Optional[DataType] = None, fname: Optional[DataType] = None, tclip: Optional['VideoNode'] = None, xpts: Optional[int] = None, ypts: Optional[int] = None, tlx: Optional[int] = None, tty: Optional[int] = None, trx: Optional[int] = None, tby: Optional[int] = None, iter: Optional[int] = None, bestof: Optional[int] = None, wset: Optional[int] = None, rgb: Optional[int] = None) -> 'VideoNode': ...
    def SaltPepper(self, clip: 'VideoNode', planes: Optional[SingleAndSequence[int]] = None, tol: Optional[int] = None, avg: Optional[int] = None) -> 'VideoNode': ...
    def Variance(self, clip: 'VideoNode', lx: int, wd: int, ty: int, ht: int, fn: Optional[int] = None, uv: Optional[int] = None, xgrid: Optional[int] = None, ygrid: Optional[int] = None) -> 'VideoNode': ...
    def Veed(self, clip: 'VideoNode', str: Optional[int] = None, rad: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, plimit: Optional[SingleAndSequence[int]] = None, mlimit: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_vcmod_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "vcmod" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Amplitude(self, *args: '_VapourSynthMapValue', **kwargs: '_VapourSynthMapValue') -> 'VideoNode': ...
    def Fan(self, span: Optional[int] = None, edge: Optional[int] = None, plus: Optional[int] = None, minus: Optional[int] = None, uv: Optional[int] = None) -> 'VideoNode': ...
    def GBlur(self, ksize: Optional[int] = None, sd: Optional[float] = None) -> 'VideoNode': ...
    def Histogram(self, clipm: Optional['VideoNode'] = None, type: Optional[int] = None, table: Optional[SingleAndSequence[int]] = None, mf: Optional[int] = None, window: Optional[int] = None, limit: Optional[int] = None) -> 'VideoNode': ...
    def MBlur(self, type: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None) -> 'VideoNode': ...
    def Median(self, maxgrid: Optional[int] = None, plane: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Neural(self, txt: Optional[DataType] = None, fname: Optional[DataType] = None, tclip: Optional['VideoNode'] = None, xpts: Optional[int] = None, ypts: Optional[int] = None, tlx: Optional[int] = None, tty: Optional[int] = None, trx: Optional[int] = None, tby: Optional[int] = None, iter: Optional[int] = None, bestof: Optional[int] = None, wset: Optional[int] = None, rgb: Optional[int] = None) -> 'VideoNode': ...
    def SaltPepper(self, planes: Optional[SingleAndSequence[int]] = None, tol: Optional[int] = None, avg: Optional[int] = None) -> 'VideoNode': ...
    def Variance(self, lx: int, wd: int, ty: int, ht: int, fn: Optional[int] = None, uv: Optional[int] = None, xgrid: Optional[int] = None, ygrid: Optional[int] = None) -> 'VideoNode': ...
    def Veed(self, str: Optional[int] = None, rad: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, plimit: Optional[SingleAndSequence[int]] = None, mlimit: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: vcmove

class _Plugin_vcmove_Core_Bound(Plugin):
    """This class implements the module definitions for the "vcmove" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DeBarrel(self, clip: 'VideoNode', a: float, b: float, c: float, vhr: Optional[float] = None, pin: Optional[int] = None, yind: Optional[int] = None, ypin: Optional[int] = None, ya: Optional[float] = None, yb: Optional[float] = None, yc: Optional[float] = None, test: Optional[int] = None) -> 'VideoNode': ...
    def Quad2Rect(self, *args: '_VapourSynthMapValue', **kwargs: '_VapourSynthMapValue') -> 'VideoNode': ...
    def Rect2Quad(self, *args: '_VapourSynthMapValue', **kwargs: '_VapourSynthMapValue') -> 'VideoNode': ...
    def Rotate(self, clip: 'VideoNode', bkg: 'VideoNode', angle: float, dinc: Optional[float] = None, lx: Optional[int] = None, wd: Optional[int] = None, ty: Optional[int] = None, ht: Optional[int] = None, axx: Optional[int] = None, axy: Optional[int] = None, intq: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_vcmove_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "vcmove" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def DeBarrel(self, a: float, b: float, c: float, vhr: Optional[float] = None, pin: Optional[int] = None, yind: Optional[int] = None, ypin: Optional[int] = None, ya: Optional[float] = None, yb: Optional[float] = None, yc: Optional[float] = None, test: Optional[int] = None) -> 'VideoNode': ...
    def Quad2Rect(self, *args: '_VapourSynthMapValue', **kwargs: '_VapourSynthMapValue') -> 'VideoNode': ...
    def Rect2Quad(self, *args: '_VapourSynthMapValue', **kwargs: '_VapourSynthMapValue') -> 'VideoNode': ...
    def Rotate(self, bkg: 'VideoNode', angle: float, dinc: Optional[float] = None, lx: Optional[int] = None, wd: Optional[int] = None, ty: Optional[int] = None, ht: Optional[int] = None, axx: Optional[int] = None, axy: Optional[int] = None, intq: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: vfx

class _Plugin_vfx_Core_Bound(Plugin):
    """This class implements the module definitions for the "vfx" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Balloon(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, color: Optional[SingleAndSequence[int]] = None, opacity: Optional[float] = None, nhops: Optional[int] = None, rise: Optional[int] = None, sx: Optional[int] = None, fx: Optional[int] = None, fy: Optional[int] = None, light: Optional[int] = None, refl: Optional[float] = None, offset: Optional[float] = None, lx: Optional[int] = None, ly: Optional[int] = None) -> 'VideoNode': ...
    def Binoculars(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, sx: Optional[int] = None, sy: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, mag: Optional[int] = None, emag: Optional[int] = None) -> 'VideoNode': ...
    def Bubbles(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, sx: Optional[int] = None, sy: Optional[int] = None, farx: Optional[int] = None, floory: Optional[int] = None, rad: Optional[int] = None, rise: Optional[int] = None, life: Optional[int] = None, nbf: Optional[int] = None) -> 'VideoNode': ...
    def Conez(self, clip: 'VideoNode', bkg: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, vert: Optional[int] = None, prog: Optional[int] = None, top: Optional[int] = None, base: Optional[int] = None) -> 'VideoNode': ...
    def DiscoLights(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, life: Optional[int] = None, type: Optional[int] = None, nspots: Optional[int] = None, minrad: Optional[int] = None, dim: Optional[float] = None) -> 'VideoNode': ...
    def FiguredGlass(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, mag: Optional[float] = None, drop: Optional[int] = None) -> 'VideoNode': ...
    def Flashes(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, rmax: Optional[int] = None, ts: Optional[float] = None, tf: Optional[int] = None) -> 'VideoNode': ...
    def FlowerPot(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, rise: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, zoom: Optional[float] = None, color: Optional[int] = None) -> 'VideoNode': ...
    def Fog(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, fog: Optional[float] = None, efog: Optional[float] = None, vary: Optional[float] = None) -> 'VideoNode': ...
    def Lens(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, mag: Optional[float] = None, drop: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, erad: Optional[int] = None, emag: Optional[float] = None) -> 'VideoNode': ...
    def LineMagnifier(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, lwidth: Optional[int] = None, mag: Optional[float] = None, drop: Optional[int] = None, xy: Optional[int] = None, exy: Optional[int] = None, vert: Optional[int] = None) -> 'VideoNode': ...
    def Pool(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, wd: Optional[int] = None, ewd: Optional[int] = None, ht: Optional[int] = None, eht: Optional[int] = None, wavelen: Optional[int] = None, amp: Optional[int] = None, eamp: Optional[int] = None, speed: Optional[float] = None, espeed: Optional[float] = None, paint: Optional[int] = None, color: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Rain(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, type: Optional[int] = None, etype: Optional[int] = None, slant: Optional[int] = None, eslant: Optional[int] = None, opq: Optional[float] = None, box: Optional[int] = None, span: Optional[int] = None) -> 'VideoNode': ...
    def Rainbow(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, erad: Optional[int] = None, x: Optional[int] = None, ex: Optional[int] = None, y: Optional[int] = None, ey: Optional[int] = None, lx: Optional[int] = None, elx: Optional[int] = None, rx: Optional[int] = None, erx: Optional[int] = None) -> 'VideoNode': ...
    def RearViewMirror(self, clip: 'VideoNode', bclip: 'VideoNode', method: Optional[int] = None, mcx: Optional[int] = None, mcy: Optional[int] = None, mwd: Optional[int] = None, mht: Optional[int] = None, oval: Optional[int] = None, border: Optional[int] = None, cvx: Optional[float] = None, fov: Optional[float] = None, test: Optional[int] = None, dim: Optional[float] = None, q: Optional[int] = None, dots: Optional[int] = None) -> 'VideoNode': ...
    def Ripple(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, wavelen: Optional[int] = None, speed: Optional[float] = None, espeed: Optional[float] = None, poolx: Optional[int] = None, pooly: Optional[int] = None, wd: Optional[int] = None, ht: Optional[int] = None, origin: Optional[int] = None, xo: Optional[int] = None, yo: Optional[int] = None, amp: Optional[int] = None, eamp: Optional[int] = None, ifr: Optional[int] = None, dfr: Optional[int] = None) -> 'VideoNode': ...
    def Rockets(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, life: Optional[float] = None, interval: Optional[float] = None, lx: Optional[int] = None, rx: Optional[int] = None, y: Optional[int] = None, rise: Optional[int] = None, target: Optional[int] = None, tx: Optional[int] = None, ty: Optional[int] = None) -> 'VideoNode': ...
    def Snow(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, density: Optional[int] = None, big: Optional[int] = None, fall: Optional[int] = None, drift: Optional[int] = None) -> 'VideoNode': ...
    def SnowStorm(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, type: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Sparkler(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, color: Optional[int] = None) -> 'VideoNode': ...
    def SpotLight(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, rgb: Optional[SingleAndSequence[int]] = None, dim: Optional[float] = None) -> 'VideoNode': ...
    def SunFlower(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, color: Optional[int] = None, gravity: Optional[float] = None, persistance: Optional[float] = None) -> 'VideoNode': ...
    def Swirl(self, clip: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, q: Optional[int] = None, dir: Optional[int] = None, grow: Optional[int] = None, steady: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_vfx_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "vfx" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Balloon(self, sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, color: Optional[SingleAndSequence[int]] = None, opacity: Optional[float] = None, nhops: Optional[int] = None, rise: Optional[int] = None, sx: Optional[int] = None, fx: Optional[int] = None, fy: Optional[int] = None, light: Optional[int] = None, refl: Optional[float] = None, offset: Optional[float] = None, lx: Optional[int] = None, ly: Optional[int] = None) -> 'VideoNode': ...
    def Binoculars(self, sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, sx: Optional[int] = None, sy: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, mag: Optional[int] = None, emag: Optional[int] = None) -> 'VideoNode': ...
    def Bubbles(self, sf: Optional[int] = None, ef: Optional[int] = None, sx: Optional[int] = None, sy: Optional[int] = None, farx: Optional[int] = None, floory: Optional[int] = None, rad: Optional[int] = None, rise: Optional[int] = None, life: Optional[int] = None, nbf: Optional[int] = None) -> 'VideoNode': ...
    def Conez(self, bkg: 'VideoNode', sf: Optional[int] = None, ef: Optional[int] = None, vert: Optional[int] = None, prog: Optional[int] = None, top: Optional[int] = None, base: Optional[int] = None) -> 'VideoNode': ...
    def DiscoLights(self, sf: Optional[int] = None, ef: Optional[int] = None, life: Optional[int] = None, type: Optional[int] = None, nspots: Optional[int] = None, minrad: Optional[int] = None, dim: Optional[float] = None) -> 'VideoNode': ...
    def FiguredGlass(self, sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, mag: Optional[float] = None, drop: Optional[int] = None) -> 'VideoNode': ...
    def Flashes(self, sf: Optional[int] = None, ef: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, rmax: Optional[int] = None, ts: Optional[float] = None, tf: Optional[int] = None) -> 'VideoNode': ...
    def FlowerPot(self, sf: Optional[int] = None, ef: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, rise: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, zoom: Optional[float] = None, color: Optional[int] = None) -> 'VideoNode': ...
    def Fog(self, sf: Optional[int] = None, ef: Optional[int] = None, fog: Optional[float] = None, efog: Optional[float] = None, vary: Optional[float] = None) -> 'VideoNode': ...
    def Lens(self, sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, mag: Optional[float] = None, drop: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, erad: Optional[int] = None, emag: Optional[float] = None) -> 'VideoNode': ...
    def LineMagnifier(self, sf: Optional[int] = None, ef: Optional[int] = None, lwidth: Optional[int] = None, mag: Optional[float] = None, drop: Optional[int] = None, xy: Optional[int] = None, exy: Optional[int] = None, vert: Optional[int] = None) -> 'VideoNode': ...
    def Pool(self, sf: Optional[int] = None, ef: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, wd: Optional[int] = None, ewd: Optional[int] = None, ht: Optional[int] = None, eht: Optional[int] = None, wavelen: Optional[int] = None, amp: Optional[int] = None, eamp: Optional[int] = None, speed: Optional[float] = None, espeed: Optional[float] = None, paint: Optional[int] = None, color: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Rain(self, sf: Optional[int] = None, ef: Optional[int] = None, type: Optional[int] = None, etype: Optional[int] = None, slant: Optional[int] = None, eslant: Optional[int] = None, opq: Optional[float] = None, box: Optional[int] = None, span: Optional[int] = None) -> 'VideoNode': ...
    def Rainbow(self, sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, erad: Optional[int] = None, x: Optional[int] = None, ex: Optional[int] = None, y: Optional[int] = None, ey: Optional[int] = None, lx: Optional[int] = None, elx: Optional[int] = None, rx: Optional[int] = None, erx: Optional[int] = None) -> 'VideoNode': ...
    def RearViewMirror(self, bclip: 'VideoNode', method: Optional[int] = None, mcx: Optional[int] = None, mcy: Optional[int] = None, mwd: Optional[int] = None, mht: Optional[int] = None, oval: Optional[int] = None, border: Optional[int] = None, cvx: Optional[float] = None, fov: Optional[float] = None, test: Optional[int] = None, dim: Optional[float] = None, q: Optional[int] = None, dots: Optional[int] = None) -> 'VideoNode': ...
    def Ripple(self, sf: Optional[int] = None, ef: Optional[int] = None, wavelen: Optional[int] = None, speed: Optional[float] = None, espeed: Optional[float] = None, poolx: Optional[int] = None, pooly: Optional[int] = None, wd: Optional[int] = None, ht: Optional[int] = None, origin: Optional[int] = None, xo: Optional[int] = None, yo: Optional[int] = None, amp: Optional[int] = None, eamp: Optional[int] = None, ifr: Optional[int] = None, dfr: Optional[int] = None) -> 'VideoNode': ...
    def Rockets(self, sf: Optional[int] = None, ef: Optional[int] = None, life: Optional[float] = None, interval: Optional[float] = None, lx: Optional[int] = None, rx: Optional[int] = None, y: Optional[int] = None, rise: Optional[int] = None, target: Optional[int] = None, tx: Optional[int] = None, ty: Optional[int] = None) -> 'VideoNode': ...
    def Snow(self, sf: Optional[int] = None, ef: Optional[int] = None, density: Optional[int] = None, big: Optional[int] = None, fall: Optional[int] = None, drift: Optional[int] = None) -> 'VideoNode': ...
    def SnowStorm(self, sf: Optional[int] = None, ef: Optional[int] = None, type: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def Sparkler(self, sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, color: Optional[int] = None) -> 'VideoNode': ...
    def SpotLight(self, sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, rgb: Optional[SingleAndSequence[int]] = None, dim: Optional[float] = None) -> 'VideoNode': ...
    def SunFlower(self, sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, ex: Optional[int] = None, ey: Optional[int] = None, color: Optional[int] = None, gravity: Optional[float] = None, persistance: Optional[float] = None) -> 'VideoNode': ...
    def Swirl(self, sf: Optional[int] = None, ef: Optional[int] = None, rad: Optional[int] = None, x: Optional[int] = None, y: Optional[int] = None, q: Optional[int] = None, dir: Optional[int] = None, grow: Optional[int] = None, steady: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: vivtc

class _Plugin_vivtc_Core_Bound(Plugin):
    """This class implements the module definitions for the "vivtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def VDecimate(self, clip: 'VideoNode', cycle: Optional[int] = None, chroma: Optional[int] = None, dupthresh: Optional[float] = None, scthresh: Optional[float] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, clip2: Optional['VideoNode'] = None, ovr: Optional[DataType] = None, dryrun: Optional[int] = None) -> 'VideoNode': ...
    def VFM(self, clip: 'VideoNode', order: int, field: Optional[int] = None, mode: Optional[int] = None, mchroma: Optional[int] = None, cthresh: Optional[int] = None, mi: Optional[int] = None, chroma: Optional[int] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, y0: Optional[int] = None, y1: Optional[int] = None, scthresh: Optional[float] = None, micmatch: Optional[int] = None, micout: Optional[int] = None, clip2: Optional['VideoNode'] = None) -> 'VideoNode': ...

class _Plugin_vivtc_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "vivtc" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def VDecimate(self, cycle: Optional[int] = None, chroma: Optional[int] = None, dupthresh: Optional[float] = None, scthresh: Optional[float] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, clip2: Optional['VideoNode'] = None, ovr: Optional[DataType] = None, dryrun: Optional[int] = None) -> 'VideoNode': ...
    def VFM(self, order: int, field: Optional[int] = None, mode: Optional[int] = None, mchroma: Optional[int] = None, cthresh: Optional[int] = None, mi: Optional[int] = None, chroma: Optional[int] = None, blockx: Optional[int] = None, blocky: Optional[int] = None, y0: Optional[int] = None, y1: Optional[int] = None, scthresh: Optional[float] = None, micmatch: Optional[int] = None, micout: Optional[int] = None, clip2: Optional['VideoNode'] = None) -> 'VideoNode': ...

# end implementation


# implementation: vmaf

class _Plugin_vmaf_Core_Bound(Plugin):
    """This class implements the module definitions for the "vmaf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CAMBI(self, clip: 'VideoNode', log_path: DataType, log_format: Optional[int] = None, window_size: Optional[int] = None, topk: Optional[float] = None, tvi_threshold: Optional[float] = None, max_log_contrast: Optional[int] = None, enc_width: Optional[int] = None, enc_height: Optional[int] = None) -> 'VideoNode': ...
    def Metric(self, reference: 'VideoNode', distorted: 'VideoNode', feature: SingleAndSequence[int]) -> 'VideoNode': ...
    def VMAF(self, reference: 'VideoNode', distorted: 'VideoNode', log_path: DataType, log_format: Optional[int] = None, model: Optional[SingleAndSequence[int]] = None, feature: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_vmaf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "vmaf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def CAMBI(self, log_path: DataType, log_format: Optional[int] = None, window_size: Optional[int] = None, topk: Optional[float] = None, tvi_threshold: Optional[float] = None, max_log_contrast: Optional[int] = None, enc_width: Optional[int] = None, enc_height: Optional[int] = None) -> 'VideoNode': ...
    def Metric(self, distorted: 'VideoNode', feature: SingleAndSequence[int]) -> 'VideoNode': ...
    def VMAF(self, distorted: 'VideoNode', log_path: DataType, log_format: Optional[int] = None, model: Optional[SingleAndSequence[int]] = None, feature: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: vscope

class _Plugin_vscope_Core_Bound(Plugin):
    """This class implements the module definitions for the "vscope" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Scope(self, clip: 'VideoNode', mode: Optional[DataType] = None, tickmarks: Optional[int] = None, side: Optional[DataType] = None, bottom: Optional[DataType] = None, corner: Optional[DataType] = None) -> 'VideoNode': ...

class _Plugin_vscope_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "vscope" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Scope(self, mode: Optional[DataType] = None, tickmarks: Optional[int] = None, side: Optional[DataType] = None, bottom: Optional[DataType] = None, corner: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation


# implementation: vsf

class _Plugin_vsf_Core_Bound(Plugin):
    """This class implements the module definitions for the "vsf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TextSub(self, clip: 'VideoNode', file: DataType, charset: Optional[int] = None, fps: Optional[float] = None, vfr: Optional[DataType] = None) -> 'VideoNode': ...
    def VobSub(self, clip: 'VideoNode', file: DataType) -> 'VideoNode': ...

class _Plugin_vsf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "vsf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TextSub(self, file: DataType, charset: Optional[int] = None, fps: Optional[float] = None, vfr: Optional[DataType] = None) -> 'VideoNode': ...
    def VobSub(self, file: DataType) -> 'VideoNode': ...

# end implementation


# implementation: vsfm

class _Plugin_vsfm_Core_Bound(Plugin):
    """This class implements the module definitions for the "vsfm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TextSubMod(self, clip: 'VideoNode', file: DataType, charset: Optional[int] = None, fps: Optional[float] = None, vfr: Optional[DataType] = None, accurate: Optional[int] = None) -> 'VideoNode': ...
    def VobSub(self, clip: 'VideoNode', file: DataType, accurate: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_vsfm_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "vsfm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TextSubMod(self, file: DataType, charset: Optional[int] = None, fps: Optional[float] = None, vfr: Optional[DataType] = None, accurate: Optional[int] = None) -> 'VideoNode': ...
    def VobSub(self, file: DataType, accurate: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: waifu2x

class _Plugin_waifu2x_Core_Bound(Plugin):
    """This class implements the module definitions for the "waifu2x" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Denoise(self, input: 'VideoNode', mode: Optional[int] = None, matrix: Optional[int] = None, full: Optional[int] = None, block_width: Optional[int] = None, block_height: Optional[int] = None, threads: Optional[int] = None) -> 'VideoNode': ...
    def Resize(self, input: 'VideoNode', width: Optional[int] = None, height: Optional[int] = None, shift_w: Optional[float] = None, shift_h: Optional[float] = None, subwidth: Optional[float] = None, subheight: Optional[float] = None, filter: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, subsample_w: Optional[int] = None, subsample_h: Optional[int] = None, chroma_loc_in: Optional[DataType] = None, chroma_loc_out: Optional[DataType] = None, matrix: Optional[int] = None, full: Optional[int] = None, block_width: Optional[int] = None, block_height: Optional[int] = None, threads: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_waifu2x_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "waifu2x" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Denoise(self, mode: Optional[int] = None, matrix: Optional[int] = None, full: Optional[int] = None, block_width: Optional[int] = None, block_height: Optional[int] = None, threads: Optional[int] = None) -> 'VideoNode': ...
    def Resize(self, width: Optional[int] = None, height: Optional[int] = None, shift_w: Optional[float] = None, shift_h: Optional[float] = None, subwidth: Optional[float] = None, subheight: Optional[float] = None, filter: Optional[DataType] = None, filter_param_a: Optional[float] = None, filter_param_b: Optional[float] = None, filter_uv: Optional[DataType] = None, filter_param_a_uv: Optional[float] = None, filter_param_b_uv: Optional[float] = None, subsample_w: Optional[int] = None, subsample_h: Optional[int] = None, chroma_loc_in: Optional[DataType] = None, chroma_loc_out: Optional[DataType] = None, matrix: Optional[int] = None, full: Optional[int] = None, block_width: Optional[int] = None, block_height: Optional[int] = None, threads: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: warp

class _Plugin_warp_Core_Bound(Plugin):
    """This class implements the module definitions for the "warp" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ABlur(self, clip: 'VideoNode', blur: Optional[int] = None, type: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def ASobel(self, clip: 'VideoNode', thresh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def AWarp(self, clip: 'VideoNode', mask: 'VideoNode', depth: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None, cplace: Optional[DataType] = None) -> 'VideoNode': ...
    def AWarpSharp2(self, clip: 'VideoNode', thresh: Optional[int] = None, blur: Optional[int] = None, type: Optional[int] = None, depth: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None, cplace: Optional[DataType] = None) -> 'VideoNode': ...

class _Plugin_warp_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "warp" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ABlur(self, blur: Optional[int] = None, type: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def ASobel(self, thresh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None) -> 'VideoNode': ...
    def AWarp(self, mask: 'VideoNode', depth: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None, cplace: Optional[DataType] = None) -> 'VideoNode': ...
    def AWarpSharp2(self, thresh: Optional[int] = None, blur: Optional[int] = None, type: Optional[int] = None, depth: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, opt: Optional[int] = None, cplace: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation


# implementation: warpsf

class _Plugin_warpsf_Core_Bound(Plugin):
    """This class implements the module definitions for the "warpsf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ABlur(self, clip: 'VideoNode', blur: Optional[int] = None, type: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def ASobel(self, clip: 'VideoNode', thresh: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def AWarp(self, clip: 'VideoNode', mask: 'VideoNode', depth: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

class _Plugin_warpsf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "warpsf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def ABlur(self, blur: Optional[int] = None, type: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def ASobel(self, thresh: Optional[float] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...
    def AWarp(self, mask: 'VideoNode', depth: Optional[SingleAndSequence[int]] = None, chroma: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None) -> 'VideoNode': ...

# end implementation


# implementation: wnnm

class _Plugin_wnnm_Core_Bound(Plugin):
    """This class implements the module definitions for the "wnnm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def VAggregate(self, clip: 'VideoNode', src: 'VideoNode', planes: SingleAndSequence[int], internal: Optional[int] = None) -> 'VideoNode': ...
    def Version(self) -> 'VideoNode': ...
    def WNNM(self, clip: 'VideoNode', sigma: Optional[SingleAndSequence[float]] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, radius: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, residual: Optional[int] = None, adaptive_aggregation: Optional[int] = None, rclip: Optional['VideoNode'] = None) -> 'VideoNode': ...
    def WNNMRaw(self, clip: 'VideoNode', sigma: Optional[SingleAndSequence[float]] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, radius: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, residual: Optional[int] = None, adaptive_aggregation: Optional[int] = None, rclip: Optional['VideoNode'] = None) -> 'VideoNode': ...

class _Plugin_wnnm_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "wnnm" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def VAggregate(self, src: 'VideoNode', planes: SingleAndSequence[int], internal: Optional[int] = None) -> 'VideoNode': ...
    def WNNM(self, sigma: Optional[SingleAndSequence[float]] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, radius: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, residual: Optional[int] = None, adaptive_aggregation: Optional[int] = None, rclip: Optional['VideoNode'] = None) -> 'VideoNode': ...
    def WNNMRaw(self, sigma: Optional[SingleAndSequence[float]] = None, block_size: Optional[int] = None, block_step: Optional[int] = None, group_size: Optional[int] = None, bm_range: Optional[int] = None, radius: Optional[int] = None, ps_num: Optional[int] = None, ps_range: Optional[int] = None, residual: Optional[int] = None, adaptive_aggregation: Optional[int] = None, rclip: Optional['VideoNode'] = None) -> 'VideoNode': ...

# end implementation


# implementation: wwxd

class _Plugin_wwxd_Core_Bound(Plugin):
    """This class implements the module definitions for the "wwxd" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def WWXD(self, clip: 'VideoNode') -> 'VideoNode': ...

class _Plugin_wwxd_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "wwxd" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def WWXD(self) -> 'VideoNode': ...

# end implementation


# implementation: xyvsf

class _Plugin_xyvsf_Core_Bound(Plugin):
    """This class implements the module definitions for the "xyvsf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TextSub(self, clip: 'VideoNode', file: DataType, charset: Optional[int] = None, fps: Optional[float] = None, vfr: Optional[DataType] = None, swapuv: Optional[int] = None) -> 'VideoNode': ...
    def VobSub(self, clip: 'VideoNode', file: DataType, swapuv: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_xyvsf_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "xyvsf" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def TextSub(self, file: DataType, charset: Optional[int] = None, fps: Optional[float] = None, vfr: Optional[DataType] = None, swapuv: Optional[int] = None) -> 'VideoNode': ...
    def VobSub(self, file: DataType, swapuv: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: yadifmod

class _Plugin_yadifmod_Core_Bound(Plugin):
    """This class implements the module definitions for the "yadifmod" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Yadifmod(self, clip: 'VideoNode', edeint: 'VideoNode', order: int, field: Optional[int] = None, mode: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

class _Plugin_yadifmod_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "yadifmod" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def Yadifmod(self, edeint: 'VideoNode', order: int, field: Optional[int] = None, mode: Optional[int] = None, opt: Optional[int] = None) -> 'VideoNode': ...

# end implementation


# implementation: znedi3

class _Plugin_znedi3_Core_Bound(Plugin):
    """This class implements the module definitions for the "znedi3" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def nnedi3(self, clip: 'VideoNode', field: int, dh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, nsize: Optional[int] = None, nns: Optional[int] = None, qual: Optional[int] = None, etype: Optional[int] = None, pscrn: Optional[int] = None, opt: Optional[int] = None, int16_prescreener: Optional[int] = None, int16_predictor: Optional[int] = None, exp: Optional[int] = None, show_mask: Optional[int] = None, x_nnedi3_weights_bin: Optional[DataType] = None, x_cpu: Optional[DataType] = None) -> 'VideoNode': ...

class _Plugin_znedi3_VideoNode_Bound(Plugin):
    """This class implements the module definitions for the "znedi3" VapourSynth plugin.\n\n*This class cannot be imported.*"""
    def nnedi3(self, field: int, dh: Optional[int] = None, planes: Optional[SingleAndSequence[int]] = None, nsize: Optional[int] = None, nns: Optional[int] = None, qual: Optional[int] = None, etype: Optional[int] = None, pscrn: Optional[int] = None, opt: Optional[int] = None, int16_prescreener: Optional[int] = None, int16_predictor: Optional[int] = None, exp: Optional[int] = None, show_mask: Optional[int] = None, x_nnedi3_weights_bin: Optional[DataType] = None, x_cpu: Optional[DataType] = None) -> 'VideoNode': ...

# end implementation



class RawNode:
    def __init__(self) -> NoReturn: ...

    def get_frame(self, n: int) -> RawFrame: ...

    @overload
    def get_frame_async(self, n: int, cb: None = None) -> _Future[RawFrame]: ...

    @overload
    def get_frame_async(self, n: int, cb: Callable[[Union[RawFrame, None], Union[Exception, None]], None]) -> None: ...

    def frames(
        self, prefetch: Union[int, None] = None, backlog: Union[int, None] = None, close: bool = False
    ) -> Iterator[RawFrame]: ...

    def set_output(self, index: int = 0) -> None: ...

    def is_inspectable(self, version: Union[int, None] = None) -> bool: ...

    if not TYPE_CHECKING:
        @property
        def _node_name(self) -> str: ...

        @property
        def _name(self) -> str: ...

        @property
        def _inputs(self) -> Dict[str, _VapourSynthMapValue]: ...

        @property
        def _timings(self) -> int: ...

        @property
        def _mode(self) -> FilterMode: ...

        @property
        def _dependencies(self): ...

    @overload
    def __eq__(self: 'SelfRawNode', other: 'SelfRawNode') -> bool: ...  # type: ignore[misc]

    @overload
    def __eq__(self, other: Any) -> Literal[False]: ...

    def __add__(self: 'SelfRawNode', other: 'SelfRawNode') -> 'SelfRawNode': ...

    def __radd__(self: 'SelfRawNode', other: 'SelfRawNode') -> 'SelfRawNode': ...

    def __mul__(self: 'SelfRawNode', other: int) -> 'SelfRawNode': ...

    def __rmul__(self: 'SelfRawNode', other: int) -> 'SelfRawNode': ...

    def __getitem__(self: 'SelfRawNode', index: Union[int, slice]) -> 'SelfRawNode': ...

    def __len__(self) -> int: ...


SelfRawNode = TypeVar('SelfRawNode', bound=RawNode)


class VideoNode(RawNode):
    format: Union[VideoFormat, None]

    width: int
    height: int

    fps_num: int
    fps_den: int

    fps: Fraction

    num_frames: int

    def set_output(
        self, index: int = 0, alpha: Union['VideoNode', None] = None, alt_output: Literal[0, 1, 2] = 0
    ) -> None: ...

    def output(
        self, fileobj: BinaryIO, y4m: bool = False, progress_update: Callable[[int, int], None] | None = None,
        prefetch: int = 0, backlog: int = -1
    ) -> None: ...

    def get_frame(self, n: int) -> VideoFrame: ...

    @overload  # type: ignore[override]
    def get_frame_async(self, n: int, cb: None = None) -> _Future[VideoFrame]: ...

    @overload
    def get_frame_async(self, n: int, cb: Callable[[Union[VideoFrame, None], Union[Exception, None]], None]) -> None: ...

    def frames(
        self, prefetch: Union[int, None] = None, backlog: Union[int, None] = None, close: bool = False
    ) -> Iterator[VideoFrame]: ...

    # instance_bound_VideoNode: adg
    @property
    def adg(self) -> _Plugin_adg_VideoNode_Bound:
        """Adaptive grain"""
    # end instance
    # instance_bound_VideoNode: akarin
    @property
    def akarin(self) -> _Plugin_akarin_VideoNode_Bound:
        """Akarin's Experimental Filters"""
    # end instance
    # instance_bound_VideoNode: assrender
    @property
    def assrender(self) -> _Plugin_assrender_VideoNode_Bound:
        """AssRender"""
    # end instance
    # instance_bound_VideoNode: average
    @property
    def average(self) -> _Plugin_average_VideoNode_Bound:
        """vs-average"""
    # end instance
    # instance_bound_VideoNode: bilateral
    @property
    def bilateral(self) -> _Plugin_bilateral_VideoNode_Bound:
        """Bilateral filter and Gaussian filter for VapourSynth."""
    # end instance
    # instance_bound_VideoNode: bilateralgpu
    @property
    def bilateralgpu(self) -> _Plugin_bilateralgpu_VideoNode_Bound:
        """Bilateral filter using CUDA"""
    # end instance
    # instance_bound_VideoNode: bm3d
    @property
    def bm3d(self) -> _Plugin_bm3d_VideoNode_Bound:
        """Implementation of BM3D denoising filter for VapourSynth."""
    # end instance
    # instance_bound_VideoNode: bm3dcpu
    @property
    def bm3dcpu(self) -> _Plugin_bm3dcpu_VideoNode_Bound:
        """BM3D algorithm implemented in AVX and AVX2 intrinsics"""
    # end instance
    # instance_bound_VideoNode: bm3dcuda
    @property
    def bm3dcuda(self) -> _Plugin_bm3dcuda_VideoNode_Bound:
        """BM3D algorithm implemented in CUDA"""
    # end instance
    # instance_bound_VideoNode: bm3dcuda_rtc
    @property
    def bm3dcuda_rtc(self) -> _Plugin_bm3dcuda_rtc_VideoNode_Bound:
        """BM3D algorithm implemented in CUDA (NVRTC)"""
    # end instance
    # instance_bound_VideoNode: box
    @property
    def box(self) -> _Plugin_box_VideoNode_Bound:
        """AVX2-optimized boxfilter"""
    # end instance
    # instance_bound_VideoNode: butteraugli
    @property
    def butteraugli(self) -> _Plugin_butteraugli_VideoNode_Bound:
        """modified version of Google's butteraugli"""
    # end instance
    # instance_bound_VideoNode: caffe
    @property
    def caffe(self) -> _Plugin_caffe_VideoNode_Bound:
        """Image Super-Resolution using Deep Convolutional Neural Networks"""
    # end instance
    # instance_bound_VideoNode: cas
    @property
    def cas(self) -> _Plugin_cas_VideoNode_Bound:
        """Contrast Adaptive Sharpening"""
    # end instance
    # instance_bound_VideoNode: ccd
    @property
    def ccd(self) -> _Plugin_ccd_VideoNode_Bound:
        """chroma denoiser"""
    # end instance
    # instance_bound_VideoNode: cf
    @property
    def cf(self) -> _Plugin_cf_VideoNode_Bound:
        """VapourSynth ContinuityFixer port"""
    # end instance
    # instance_bound_VideoNode: chkdr
    @property
    def chkdr(self) -> _Plugin_chkdr_VideoNode_Bound:
        """Film grain generator"""
    # end instance
    # instance_bound_VideoNode: comb
    @property
    def comb(self) -> _Plugin_comb_VideoNode_Bound:
        """comb filters v0.0.1"""
    # end instance
    # instance_bound_VideoNode: ctmf
    @property
    def ctmf(self) -> _Plugin_ctmf_VideoNode_Bound:
        """Constant Time Median Filtering"""
    # end instance
    # instance_bound_VideoNode: d2v
    @property
    def d2v(self) -> _Plugin_d2v_VideoNode_Bound:
        """D2V Source"""
    # end instance
    # instance_bound_VideoNode: dct
    @property
    def dct(self) -> _Plugin_dct_VideoNode_Bound:
        """DCT filtering plugin rev10-b311e2e"""
    # end instance
    # instance_bound_VideoNode: dctf
    @property
    def dctf(self) -> _Plugin_dctf_VideoNode_Bound:
        """DCT/IDCT Frequency Suppressor"""
    # end instance
    # instance_bound_VideoNode: deblock
    @property
    def deblock(self) -> _Plugin_deblock_VideoNode_Bound:
        """It does a deblocking of the picture, using the deblocking filter of h264"""
    # end instance
    # instance_bound_VideoNode: descale
    @property
    def descale(self) -> _Plugin_descale_VideoNode_Bound:
        """Undo linear interpolation"""
    # end instance
    # instance_bound_VideoNode: descale_getnative
    @property
    def descale_getnative(self) -> _Plugin_descale_getnative_VideoNode_Bound:
        """Undo linear interpolation"""
    # end instance
    # instance_bound_VideoNode: dfttest
    @property
    def dfttest(self) -> _Plugin_dfttest_VideoNode_Bound:
        """2D/3D frequency domain denoiser"""
    # end instance
    # instance_bound_VideoNode: dfttest2_avx2
    @property
    def dfttest2_avx2(self) -> _Plugin_dfttest2_avx2_VideoNode_Bound:
        """DFTTest2 (AVX2)"""
    # end instance
    # instance_bound_VideoNode: dfttest2_cpu
    @property
    def dfttest2_cpu(self) -> _Plugin_dfttest2_cpu_VideoNode_Bound:
        """DFTTest2 (CPU)"""
    # end instance
    # instance_bound_VideoNode: dfttest2_cuda
    @property
    def dfttest2_cuda(self) -> _Plugin_dfttest2_cuda_VideoNode_Bound:
        """DFTTest2 (CUDA)"""
    # end instance
    # instance_bound_VideoNode: dfttest2_nvrtc
    @property
    def dfttest2_nvrtc(self) -> _Plugin_dfttest2_nvrtc_VideoNode_Bound:
        """DFTTest2 (NVRTC)"""
    # end instance
    # instance_bound_VideoNode: dpid
    @property
    def dpid(self) -> _Plugin_dpid_VideoNode_Bound:
        """Rapid, Detail-Preserving Image Downscaling"""
    # end instance
    # instance_bound_VideoNode: eedi2
    @property
    def eedi2(self) -> _Plugin_eedi2_VideoNode_Bound:
        """EEDI2"""
    # end instance
    # instance_bound_VideoNode: eedi2cuda
    @property
    def eedi2cuda(self) -> _Plugin_eedi2cuda_VideoNode_Bound:
        """EEDI2 filter using CUDA"""
    # end instance
    # instance_bound_VideoNode: eedi3m
    @property
    def eedi3m(self) -> _Plugin_eedi3m_VideoNode_Bound:
        """Enhanced Edge Directed Interpolation 3"""
    # end instance
    # instance_bound_VideoNode: f3kdb
    @property
    def f3kdb(self) -> _Plugin_f3kdb_VideoNode_Bound:
        """flash3kyuu_deband"""
    # end instance
    # instance_bound_VideoNode: fft3dfilter
    @property
    def fft3dfilter(self) -> _Plugin_fft3dfilter_VideoNode_Bound:
        """systems"""
    # end instance
    # instance_bound_VideoNode: fh
    @property
    def fh(self) -> _Plugin_fh_VideoNode_Bound:
        """FieldHint Plugin"""
    # end instance
    # instance_bound_VideoNode: flux
    @property
    def flux(self) -> _Plugin_flux_VideoNode_Bound:
        """FluxSmooth plugin for VapourSynth"""
    # end instance
    # instance_bound_VideoNode: fmtc
    @property
    def fmtc(self) -> _Plugin_fmtc_VideoNode_Bound:
        """Format converter"""
    # end instance
    # instance_bound_VideoNode: focus
    @property
    def focus(self) -> _Plugin_focus_VideoNode_Bound:
        """VapourSynth Pixel Restoration Filters"""
    # end instance
    # instance_bound_VideoNode: focus2
    @property
    def focus2(self) -> _Plugin_focus2_VideoNode_Bound:
        """VapourSynth TemporalSoften Filter v0.1.1"""
    # end instance
    # instance_bound_VideoNode: ftf
    @property
    def ftf(self) -> _Plugin_ftf_VideoNode_Bound:
        """Fix Telecined Fades"""
    # end instance
    # instance_bound_VideoNode: grad
    @property
    def grad(self) -> _Plugin_grad_VideoNode_Bound:
        """Adjustment of contrast, brightness, gamma and a wide range of color manipulations through gradation curves is possible."""
    # end instance
    # instance_bound_VideoNode: grain
    @property
    def grain(self) -> _Plugin_grain_VideoNode_Bound:
        """Random noise film grain generator"""
    # end instance
    # instance_bound_VideoNode: hist
    @property
    def hist(self) -> _Plugin_hist_VideoNode_Bound:
        """VapourSynth Histogram Plugin"""
    # end instance
    # instance_bound_VideoNode: hqdn3d
    @property
    def hqdn3d(self) -> _Plugin_hqdn3d_VideoNode_Bound:
        """HQDn3D port as used in avisynth/mplayer"""
    # end instance
    # instance_bound_VideoNode: iccc
    @property
    def iccc(self) -> _Plugin_iccc_VideoNode_Bound:
        """ICC Conversion"""
    # end instance
    # instance_bound_VideoNode: imwri
    @property
    def imwri(self) -> _Plugin_imwri_VideoNode_Bound:
        """VapourSynth ImageMagick 7 HDRI Writer/Reader"""
    # end instance
    # instance_bound_VideoNode: knlm
    @property
    def knlm(self) -> _Plugin_knlm_VideoNode_Bound:
        """KNLMeansCL for VapourSynth"""
    # end instance
    # instance_bound_VideoNode: libp2p
    @property
    def libp2p(self) -> _Plugin_libp2p_VideoNode_Bound:
        """libp2p rgb formats packer/unpacker"""
    # end instance
    # instance_bound_VideoNode: median
    @property
    def median(self) -> _Plugin_median_VideoNode_Bound:
        """Median of clips"""
    # end instance
    # instance_bound_VideoNode: minsrp
    @property
    def minsrp(self) -> _Plugin_minsrp_VideoNode_Bound:
        """VapourSynth MinSRP Filter"""
    # end instance
    # instance_bound_VideoNode: misc
    @property
    def misc(self) -> _Plugin_misc_VideoNode_Bound:
        """Miscellaneous filters"""
    # end instance
    # instance_bound_VideoNode: morpho
    @property
    def morpho(self) -> _Plugin_morpho_VideoNode_Bound:
        """Simple morphological filters."""
    # end instance
    # instance_bound_VideoNode: mpeg2stinx
    @property
    def mpeg2stinx(self) -> _Plugin_mpeg2stinx_VideoNode_Bound:
        """Mpeg2Stinx"""
    # end instance
    # instance_bound_VideoNode: mv
    @property
    def mv(self) -> _Plugin_mv_VideoNode_Bound:
        """MVTools v23"""
    # end instance
    # instance_bound_VideoNode: mvsf
    @property
    def mvsf(self) -> _Plugin_mvsf_VideoNode_Bound:
        """MVTools Single Precision"""
    # end instance
    # instance_bound_VideoNode: ncnn
    @property
    def ncnn(self) -> _Plugin_ncnn_VideoNode_Bound:
        """NCNN ML Filter Runtime"""
    # end instance
    # instance_bound_VideoNode: neo_f3kdb
    @property
    def neo_f3kdb(self) -> _Plugin_neo_f3kdb_VideoNode_Bound:
        """Neo F3KDB Deband Filter r9"""
    # end instance
    # instance_bound_VideoNode: nnedi3
    @property
    def nnedi3(self) -> _Plugin_nnedi3_VideoNode_Bound:
        """Neural network edge directed interpolation (3rd gen.), v12"""
    # end instance
    # instance_bound_VideoNode: nnedi3cl
    @property
    def nnedi3cl(self) -> _Plugin_nnedi3cl_VideoNode_Bound:
        """An intra-field only deinterlacer"""
    # end instance
    # instance_bound_VideoNode: noise
    @property
    def noise(self) -> _Plugin_noise_VideoNode_Bound:
        """Noise generator"""
    # end instance
    # instance_bound_VideoNode: ort
    @property
    def ort(self) -> _Plugin_ort_VideoNode_Bound:
        """ONNX Runtime ML Filter Runtime"""
    # end instance
    # instance_bound_VideoNode: ov
    @property
    def ov(self) -> _Plugin_ov_VideoNode_Bound:
        """OpenVINO ML Filter Runtime"""
    # end instance
    # instance_bound_VideoNode: placebo
    @property
    def placebo(self) -> _Plugin_placebo_VideoNode_Bound:
        """libplacebo plugin for VapourSynth"""
    # end instance
    # instance_bound_VideoNode: psm
    @property
    def psm(self) -> _Plugin_psm_VideoNode_Bound:
        """PlaneStats with threshold"""
    # end instance
    # instance_bound_VideoNode: rdvs
    @property
    def rdvs(self) -> _Plugin_rdvs_VideoNode_Bound:
        """RemoveDirt VapourSynth Port"""
    # end instance
    # instance_bound_VideoNode: reduceflicker
    @property
    def reduceflicker(self) -> _Plugin_reduceflicker_VideoNode_Bound:
        """ReduceFlicker rev-"""
    # end instance
    # instance_bound_VideoNode: resize
    @property
    def resize(self) -> _Plugin_resize_VideoNode_Bound:
        """VapourSynth Resize"""
    # end instance
    # instance_bound_VideoNode: retinex
    @property
    def retinex(self) -> _Plugin_retinex_VideoNode_Bound:
        """Implementation of Retinex algorithm for VapourSynth."""
    # end instance
    # instance_bound_VideoNode: rf
    @property
    def rf(self) -> _Plugin_rf_VideoNode_Bound:
        """VapourSynth Replace Frames Tool"""
    # end instance
    # instance_bound_VideoNode: sangnom
    @property
    def sangnom(self) -> _Plugin_sangnom_VideoNode_Bound:
        """VapourSynth Single Field Deinterlacer"""
    # end instance
    # instance_bound_VideoNode: scd
    @property
    def scd(self) -> _Plugin_scd_VideoNode_Bound:
        """Scene change detect filter for VapourSynth v0.2.0"""
    # end instance
    # instance_bound_VideoNode: scrawl
    @property
    def scrawl(self) -> _Plugin_scrawl_VideoNode_Bound:
        """Simple text output plugin for VapourSynth"""
    # end instance
    # instance_bound_VideoNode: scxvid
    @property
    def scxvid(self) -> _Plugin_scxvid_VideoNode_Bound:
        """VapourSynth Scxvid Plugin"""
    # end instance
    # instance_bound_VideoNode: std
    @property
    def std(self) -> _Plugin_std_VideoNode_Bound:
        """VapourSynth Core Functions"""
    # end instance
    # instance_bound_VideoNode: surfaceblur
    @property
    def surfaceblur(self) -> _Plugin_surfaceblur_VideoNode_Bound:
        """surface blur"""
    # end instance
    # instance_bound_VideoNode: svp1
    @property
    def svp1(self) -> _Plugin_svp1_VideoNode_Bound:
        """SVPFlow1"""
    # end instance
    # instance_bound_VideoNode: svp2
    @property
    def svp2(self) -> _Plugin_svp2_VideoNode_Bound:
        """SVPFlow2"""
    # end instance
    # instance_bound_VideoNode: tcanny
    @property
    def tcanny(self) -> _Plugin_tcanny_VideoNode_Bound:
        """Build an edge map using canny edge detection"""
    # end instance
    # instance_bound_VideoNode: tdm
    @property
    def tdm(self) -> _Plugin_tdm_VideoNode_Bound:
        """A bi-directionally motion adaptive deinterlacer"""
    # end instance
    # instance_bound_VideoNode: tedgemask
    @property
    def tedgemask(self) -> _Plugin_tedgemask_VideoNode_Bound:
        """Edge detection plugin"""
    # end instance
    # instance_bound_VideoNode: text
    @property
    def text(self) -> _Plugin_text_VideoNode_Bound:
        """VapourSynth Text"""
    # end instance
    # instance_bound_VideoNode: tivtc
    @property
    def tivtc(self) -> _Plugin_tivtc_VideoNode_Bound:
        """Field matching and decimation"""
    # end instance
    # instance_bound_VideoNode: tmap
    @property
    def tmap(self) -> _Plugin_tmap_VideoNode_Bound:
        """Hable Tonemapping"""
    # end instance
    # instance_bound_VideoNode: tonemap
    @property
    def tonemap(self) -> _Plugin_tonemap_VideoNode_Bound:
        """Simple tone mapping for VapourSynth"""
    # end instance
    # instance_bound_VideoNode: trt
    @property
    def trt(self) -> _Plugin_trt_VideoNode_Bound:
        """TensorRT ML Filter Runtime"""
    # end instance
    # instance_bound_VideoNode: ttmpsm
    @property
    def ttmpsm(self) -> _Plugin_ttmpsm_VideoNode_Bound:
        """A basic, motion adaptive, temporal smoothing filter"""
    # end instance
    # instance_bound_VideoNode: vcfreq
    @property
    def vcfreq(self) -> _Plugin_vcfreq_VideoNode_Bound:
        """VapourSynth  Frequency Domain Filters"""
    # end instance
    # instance_bound_VideoNode: vcmod
    @property
    def vcmod(self) -> _Plugin_vcmod_VideoNode_Bound:
        """VapourSynth Pixel Amplitude modification """
    # end instance
    # instance_bound_VideoNode: vcmove
    @property
    def vcmove(self) -> _Plugin_vcmove_VideoNode_Bound:
        """VapourSynth pixel repositioning Plugin"""
    # end instance
    # instance_bound_VideoNode: vfx
    @property
    def vfx(self) -> _Plugin_vfx_VideoNode_Bound:
        """Special Effects """
    # end instance
    # instance_bound_VideoNode: vivtc
    @property
    def vivtc(self) -> _Plugin_vivtc_VideoNode_Bound:
        """VFM"""
    # end instance
    # instance_bound_VideoNode: vmaf
    @property
    def vmaf(self) -> _Plugin_vmaf_VideoNode_Bound:
        """Video Multi-Method Assessment Fusion"""
    # end instance
    # instance_bound_VideoNode: vscope
    @property
    def vscope(self) -> _Plugin_vscope_VideoNode_Bound:
        """Videoscope plugin for VapourSynth"""
    # end instance
    # instance_bound_VideoNode: vsf
    @property
    def vsf(self) -> _Plugin_vsf_VideoNode_Bound:
        """VSFilter"""
    # end instance
    # instance_bound_VideoNode: vsfm
    @property
    def vsfm(self) -> _Plugin_vsfm_VideoNode_Bound:
        """VSFilterMod"""
    # end instance
    # instance_bound_VideoNode: waifu2x
    @property
    def waifu2x(self) -> _Plugin_waifu2x_VideoNode_Bound:
        """Waifu2x-opt image restoration filter for VapourSynth."""
    # end instance
    # instance_bound_VideoNode: warp
    @property
    def warp(self) -> _Plugin_warp_VideoNode_Bound:
        """Sharpen images by warping"""
    # end instance
    # instance_bound_VideoNode: warpsf
    @property
    def warpsf(self) -> _Plugin_warpsf_VideoNode_Bound:
        """Warpsharp floating point version"""
    # end instance
    # instance_bound_VideoNode: wnnm
    @property
    def wnnm(self) -> _Plugin_wnnm_VideoNode_Bound:
        """Weighted Nuclear Norm Minimization Denoiser"""
    # end instance
    # instance_bound_VideoNode: wwxd
    @property
    def wwxd(self) -> _Plugin_wwxd_VideoNode_Bound:
        """Scene change detection approximately like Xvid's"""
    # end instance
    # instance_bound_VideoNode: xyvsf
    @property
    def xyvsf(self) -> _Plugin_xyvsf_VideoNode_Bound:
        """xy-VSFilter"""
    # end instance
    # instance_bound_VideoNode: yadifmod
    @property
    def yadifmod(self) -> _Plugin_yadifmod_VideoNode_Bound:
        """Modification of Fizick's yadif avisynth filter"""
    # end instance
    # instance_bound_VideoNode: znedi3
    @property
    def znedi3(self) -> _Plugin_znedi3_VideoNode_Bound:
        """Neural network edge directed interpolation (3rd gen.)"""
    # end instance


class AudioNode(RawNode):
    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int

    channel_layout: int
    num_channels: int

    sample_rate: int
    num_samples: int

    num_frames: int

    @property
    def channels(self) -> ChannelLayout: ...

    def get_frame(self, n: int) -> AudioFrame: ...

    @overload  # type: ignore[override]
    def get_frame_async(self, n: int, cb: None = None) -> _Future[AudioFrame]: ...

    @overload
    def get_frame_async(self, n: int, cb: Callable[[Union[AudioFrame, None], Union[Exception, None]], None]) -> None: ...

    def frames(
        self, prefetch: Union[int, None] = None, backlog: Union[int, None] = None, close: bool = False
    ) -> Iterator[AudioFrame]: ...

    # instance_bound_AudioNode: std
    @property
    def std(self) -> _Plugin_std_AudioNode_Bound:
        """VapourSynth Core Functions"""
    # end instance


class LogHandle:
    def __init__(self) -> NoReturn: ...


class Function:
    plugin: 'Plugin'
    name: str
    signature: str
    return_signature: str

    def __init__(self) -> NoReturn: ...

    def __call__(self, *args: _VapourSynthMapValue, **kwargs: _VapourSynthMapValue) -> _VapourSynthMapValue: ...

    @property
    def __signature__(self) -> Signature: ...


class Plugin:
    identifier: str
    namespace: str
    name: str

    def __init__(self) -> NoReturn: ...

    def __getattr__(self, name: str) -> Function: ...

    def functions(self) -> Iterator[Function]: ...

    @property
    def version(self) -> PluginVersion: ...


class Core:
    def __init__(self) -> NoReturn: ...

    @property
    def num_threads(self) -> int: ...

    @num_threads.setter
    def num_threads(self) -> None: ...

    @property
    def max_cache_size(self) -> int: ...

    @max_cache_size.setter
    def max_cache_size(self) -> None: ...

    @property
    def flags(self) -> int: ...

    def plugins(self) -> Iterator[Plugin]: ...

    def query_video_format(
        self, color_family: ColorFamily, sample_type: SampleType, bits_per_sample: int, subsampling_w: int = 0,
        subsampling_h: int = 0
    ) -> VideoFormat: ...

    def get_video_format(self, id: Union[VideoFormat, int, PresetFormat]) -> VideoFormat: ...

    def create_video_frame(self, format: VideoFormat, width: int, height: int) -> VideoFrame: ...

    def log_message(self, message_type: MessageType, message: str) -> None: ...

    def add_log_handler(self, handler_func: Callable[[MessageType, str], None]) -> LogHandle: ...

    def remove_log_handler(self, handle: LogHandle) -> None: ...

    def version(self) -> str: ...

    def version_number(self) -> int: ...

    # instance_bound_Core: adg
    @property
    def adg(self) -> _Plugin_adg_Core_Bound:
        """Adaptive grain"""
    # end instance
    # instance_bound_Core: akarin
    @property
    def akarin(self) -> _Plugin_akarin_Core_Bound:
        """Akarin's Experimental Filters"""
    # end instance
    # instance_bound_Core: assrender
    @property
    def assrender(self) -> _Plugin_assrender_Core_Bound:
        """AssRender"""
    # end instance
    # instance_bound_Core: average
    @property
    def average(self) -> _Plugin_average_Core_Bound:
        """vs-average"""
    # end instance
    # instance_bound_Core: avs
    @property
    def avs(self) -> _Plugin_avs_Core_Bound:
        """VapourSynth Avisynth Compatibility"""
    # end instance
    # instance_bound_Core: bas
    @property
    def bas(self) -> _Plugin_bas_Core_Bound:
        """Best Audio Source"""
    # end instance
    # instance_bound_Core: bilateral
    @property
    def bilateral(self) -> _Plugin_bilateral_Core_Bound:
        """Bilateral filter and Gaussian filter for VapourSynth."""
    # end instance
    # instance_bound_Core: bilateralgpu
    @property
    def bilateralgpu(self) -> _Plugin_bilateralgpu_Core_Bound:
        """Bilateral filter using CUDA"""
    # end instance
    # instance_bound_Core: bm3d
    @property
    def bm3d(self) -> _Plugin_bm3d_Core_Bound:
        """Implementation of BM3D denoising filter for VapourSynth."""
    # end instance
    # instance_bound_Core: bm3dcpu
    @property
    def bm3dcpu(self) -> _Plugin_bm3dcpu_Core_Bound:
        """BM3D algorithm implemented in AVX and AVX2 intrinsics"""
    # end instance
    # instance_bound_Core: bm3dcuda
    @property
    def bm3dcuda(self) -> _Plugin_bm3dcuda_Core_Bound:
        """BM3D algorithm implemented in CUDA"""
    # end instance
    # instance_bound_Core: bm3dcuda_rtc
    @property
    def bm3dcuda_rtc(self) -> _Plugin_bm3dcuda_rtc_Core_Bound:
        """BM3D algorithm implemented in CUDA (NVRTC)"""
    # end instance
    # instance_bound_Core: box
    @property
    def box(self) -> _Plugin_box_Core_Bound:
        """AVX2-optimized boxfilter"""
    # end instance
    # instance_bound_Core: bs
    @property
    def bs(self) -> _Plugin_bs_Core_Bound:
        """Best Source"""
    # end instance
    # instance_bound_Core: butteraugli
    @property
    def butteraugli(self) -> _Plugin_butteraugli_Core_Bound:
        """modified version of Google's butteraugli"""
    # end instance
    # instance_bound_Core: caffe
    @property
    def caffe(self) -> _Plugin_caffe_Core_Bound:
        """Image Super-Resolution using Deep Convolutional Neural Networks"""
    # end instance
    # instance_bound_Core: cas
    @property
    def cas(self) -> _Plugin_cas_Core_Bound:
        """Contrast Adaptive Sharpening"""
    # end instance
    # instance_bound_Core: ccd
    @property
    def ccd(self) -> _Plugin_ccd_Core_Bound:
        """chroma denoiser"""
    # end instance
    # instance_bound_Core: cf
    @property
    def cf(self) -> _Plugin_cf_Core_Bound:
        """VapourSynth ContinuityFixer port"""
    # end instance
    # instance_bound_Core: chkdr
    @property
    def chkdr(self) -> _Plugin_chkdr_Core_Bound:
        """Film grain generator"""
    # end instance
    # instance_bound_Core: comb
    @property
    def comb(self) -> _Plugin_comb_Core_Bound:
        """comb filters v0.0.1"""
    # end instance
    # instance_bound_Core: ctmf
    @property
    def ctmf(self) -> _Plugin_ctmf_Core_Bound:
        """Constant Time Median Filtering"""
    # end instance
    # instance_bound_Core: d2v
    @property
    def d2v(self) -> _Plugin_d2v_Core_Bound:
        """D2V Source"""
    # end instance
    # instance_bound_Core: dct
    @property
    def dct(self) -> _Plugin_dct_Core_Bound:
        """DCT filtering plugin rev10-b311e2e"""
    # end instance
    # instance_bound_Core: dctf
    @property
    def dctf(self) -> _Plugin_dctf_Core_Bound:
        """DCT/IDCT Frequency Suppressor"""
    # end instance
    # instance_bound_Core: deblock
    @property
    def deblock(self) -> _Plugin_deblock_Core_Bound:
        """It does a deblocking of the picture, using the deblocking filter of h264"""
    # end instance
    # instance_bound_Core: descale
    @property
    def descale(self) -> _Plugin_descale_Core_Bound:
        """Undo linear interpolation"""
    # end instance
    # instance_bound_Core: descale_getnative
    @property
    def descale_getnative(self) -> _Plugin_descale_getnative_Core_Bound:
        """Undo linear interpolation"""
    # end instance
    # instance_bound_Core: dfttest
    @property
    def dfttest(self) -> _Plugin_dfttest_Core_Bound:
        """2D/3D frequency domain denoiser"""
    # end instance
    # instance_bound_Core: dfttest2_avx2
    @property
    def dfttest2_avx2(self) -> _Plugin_dfttest2_avx2_Core_Bound:
        """DFTTest2 (AVX2)"""
    # end instance
    # instance_bound_Core: dfttest2_cpu
    @property
    def dfttest2_cpu(self) -> _Plugin_dfttest2_cpu_Core_Bound:
        """DFTTest2 (CPU)"""
    # end instance
    # instance_bound_Core: dfttest2_cuda
    @property
    def dfttest2_cuda(self) -> _Plugin_dfttest2_cuda_Core_Bound:
        """DFTTest2 (CUDA)"""
    # end instance
    # instance_bound_Core: dfttest2_nvrtc
    @property
    def dfttest2_nvrtc(self) -> _Plugin_dfttest2_nvrtc_Core_Bound:
        """DFTTest2 (NVRTC)"""
    # end instance
    # instance_bound_Core: dgdecodenv
    @property
    def dgdecodenv(self) -> _Plugin_dgdecodenv_Core_Bound:
        """DGDecodeNV for VapourSynth"""
    # end instance
    # instance_bound_Core: dpid
    @property
    def dpid(self) -> _Plugin_dpid_Core_Bound:
        """Rapid, Detail-Preserving Image Downscaling"""
    # end instance
    # instance_bound_Core: eedi2
    @property
    def eedi2(self) -> _Plugin_eedi2_Core_Bound:
        """EEDI2"""
    # end instance
    # instance_bound_Core: eedi2cuda
    @property
    def eedi2cuda(self) -> _Plugin_eedi2cuda_Core_Bound:
        """EEDI2 filter using CUDA"""
    # end instance
    # instance_bound_Core: eedi3m
    @property
    def eedi3m(self) -> _Plugin_eedi3m_Core_Bound:
        """Enhanced Edge Directed Interpolation 3"""
    # end instance
    # instance_bound_Core: f3kdb
    @property
    def f3kdb(self) -> _Plugin_f3kdb_Core_Bound:
        """flash3kyuu_deband"""
    # end instance
    # instance_bound_Core: ffms2
    @property
    def ffms2(self) -> _Plugin_ffms2_Core_Bound:
        """FFmpegSource 2 for VapourSynth"""
    # end instance
    # instance_bound_Core: fft3dfilter
    @property
    def fft3dfilter(self) -> _Plugin_fft3dfilter_Core_Bound:
        """systems"""
    # end instance
    # instance_bound_Core: fh
    @property
    def fh(self) -> _Plugin_fh_Core_Bound:
        """FieldHint Plugin"""
    # end instance
    # instance_bound_Core: flux
    @property
    def flux(self) -> _Plugin_flux_Core_Bound:
        """FluxSmooth plugin for VapourSynth"""
    # end instance
    # instance_bound_Core: fmtc
    @property
    def fmtc(self) -> _Plugin_fmtc_Core_Bound:
        """Format converter"""
    # end instance
    # instance_bound_Core: focus
    @property
    def focus(self) -> _Plugin_focus_Core_Bound:
        """VapourSynth Pixel Restoration Filters"""
    # end instance
    # instance_bound_Core: focus2
    @property
    def focus2(self) -> _Plugin_focus2_Core_Bound:
        """VapourSynth TemporalSoften Filter v0.1.1"""
    # end instance
    # instance_bound_Core: ftf
    @property
    def ftf(self) -> _Plugin_ftf_Core_Bound:
        """Fix Telecined Fades"""
    # end instance
    # instance_bound_Core: grad
    @property
    def grad(self) -> _Plugin_grad_Core_Bound:
        """Adjustment of contrast, brightness, gamma and a wide range of color manipulations through gradation curves is possible."""
    # end instance
    # instance_bound_Core: grain
    @property
    def grain(self) -> _Plugin_grain_Core_Bound:
        """Random noise film grain generator"""
    # end instance
    # instance_bound_Core: hist
    @property
    def hist(self) -> _Plugin_hist_Core_Bound:
        """VapourSynth Histogram Plugin"""
    # end instance
    # instance_bound_Core: hqdn3d
    @property
    def hqdn3d(self) -> _Plugin_hqdn3d_Core_Bound:
        """HQDn3D port as used in avisynth/mplayer"""
    # end instance
    # instance_bound_Core: iccc
    @property
    def iccc(self) -> _Plugin_iccc_Core_Bound:
        """ICC Conversion"""
    # end instance
    # instance_bound_Core: imwri
    @property
    def imwri(self) -> _Plugin_imwri_Core_Bound:
        """VapourSynth ImageMagick 7 HDRI Writer/Reader"""
    # end instance
    # instance_bound_Core: knlm
    @property
    def knlm(self) -> _Plugin_knlm_Core_Bound:
        """KNLMeansCL for VapourSynth"""
    # end instance
    # instance_bound_Core: libp2p
    @property
    def libp2p(self) -> _Plugin_libp2p_Core_Bound:
        """libp2p rgb formats packer/unpacker"""
    # end instance
    # instance_bound_Core: lsmas
    @property
    def lsmas(self) -> _Plugin_lsmas_Core_Bound:
        """LSMASHSource for VapourSynth"""
    # end instance
    # instance_bound_Core: median
    @property
    def median(self) -> _Plugin_median_Core_Bound:
        """Median of clips"""
    # end instance
    # instance_bound_Core: minsrp
    @property
    def minsrp(self) -> _Plugin_minsrp_Core_Bound:
        """VapourSynth MinSRP Filter"""
    # end instance
    # instance_bound_Core: misc
    @property
    def misc(self) -> _Plugin_misc_Core_Bound:
        """Miscellaneous filters"""
    # end instance
    # instance_bound_Core: morpho
    @property
    def morpho(self) -> _Plugin_morpho_Core_Bound:
        """Simple morphological filters."""
    # end instance
    # instance_bound_Core: mpeg2stinx
    @property
    def mpeg2stinx(self) -> _Plugin_mpeg2stinx_Core_Bound:
        """Mpeg2Stinx"""
    # end instance
    # instance_bound_Core: mpls
    @property
    def mpls(self) -> _Plugin_mpls_Core_Bound:
        """Get m2ts clip id from a playlist and return a dict"""
    # end instance
    # instance_bound_Core: mv
    @property
    def mv(self) -> _Plugin_mv_Core_Bound:
        """MVTools v23"""
    # end instance
    # instance_bound_Core: mvsf
    @property
    def mvsf(self) -> _Plugin_mvsf_Core_Bound:
        """MVTools Single Precision"""
    # end instance
    # instance_bound_Core: ncnn
    @property
    def ncnn(self) -> _Plugin_ncnn_Core_Bound:
        """NCNN ML Filter Runtime"""
    # end instance
    # instance_bound_Core: neo_f3kdb
    @property
    def neo_f3kdb(self) -> _Plugin_neo_f3kdb_Core_Bound:
        """Neo F3KDB Deband Filter r9"""
    # end instance
    # instance_bound_Core: nnedi3
    @property
    def nnedi3(self) -> _Plugin_nnedi3_Core_Bound:
        """Neural network edge directed interpolation (3rd gen.), v12"""
    # end instance
    # instance_bound_Core: nnedi3cl
    @property
    def nnedi3cl(self) -> _Plugin_nnedi3cl_Core_Bound:
        """An intra-field only deinterlacer"""
    # end instance
    # instance_bound_Core: noise
    @property
    def noise(self) -> _Plugin_noise_Core_Bound:
        """Noise generator"""
    # end instance
    # instance_bound_Core: ort
    @property
    def ort(self) -> _Plugin_ort_Core_Bound:
        """ONNX Runtime ML Filter Runtime"""
    # end instance
    # instance_bound_Core: ov
    @property
    def ov(self) -> _Plugin_ov_Core_Bound:
        """OpenVINO ML Filter Runtime"""
    # end instance
    # instance_bound_Core: placebo
    @property
    def placebo(self) -> _Plugin_placebo_Core_Bound:
        """libplacebo plugin for VapourSynth"""
    # end instance
    # instance_bound_Core: psm
    @property
    def psm(self) -> _Plugin_psm_Core_Bound:
        """PlaneStats with threshold"""
    # end instance
    # instance_bound_Core: rdvs
    @property
    def rdvs(self) -> _Plugin_rdvs_Core_Bound:
        """RemoveDirt VapourSynth Port"""
    # end instance
    # instance_bound_Core: reduceflicker
    @property
    def reduceflicker(self) -> _Plugin_reduceflicker_Core_Bound:
        """ReduceFlicker rev-"""
    # end instance
    # instance_bound_Core: resize
    @property
    def resize(self) -> _Plugin_resize_Core_Bound:
        """VapourSynth Resize"""
    # end instance
    # instance_bound_Core: retinex
    @property
    def retinex(self) -> _Plugin_retinex_Core_Bound:
        """Implementation of Retinex algorithm for VapourSynth."""
    # end instance
    # instance_bound_Core: rf
    @property
    def rf(self) -> _Plugin_rf_Core_Bound:
        """VapourSynth Replace Frames Tool"""
    # end instance
    # instance_bound_Core: sangnom
    @property
    def sangnom(self) -> _Plugin_sangnom_Core_Bound:
        """VapourSynth Single Field Deinterlacer"""
    # end instance
    # instance_bound_Core: scd
    @property
    def scd(self) -> _Plugin_scd_Core_Bound:
        """Scene change detect filter for VapourSynth v0.2.0"""
    # end instance
    # instance_bound_Core: scrawl
    @property
    def scrawl(self) -> _Plugin_scrawl_Core_Bound:
        """Simple text output plugin for VapourSynth"""
    # end instance
    # instance_bound_Core: scxvid
    @property
    def scxvid(self) -> _Plugin_scxvid_Core_Bound:
        """VapourSynth Scxvid Plugin"""
    # end instance
    # instance_bound_Core: std
    @property
    def std(self) -> _Plugin_std_Core_Bound:
        """VapourSynth Core Functions"""
    # end instance
    # instance_bound_Core: surfaceblur
    @property
    def surfaceblur(self) -> _Plugin_surfaceblur_Core_Bound:
        """surface blur"""
    # end instance
    # instance_bound_Core: svp1
    @property
    def svp1(self) -> _Plugin_svp1_Core_Bound:
        """SVPFlow1"""
    # end instance
    # instance_bound_Core: svp2
    @property
    def svp2(self) -> _Plugin_svp2_Core_Bound:
        """SVPFlow2"""
    # end instance
    # instance_bound_Core: tcanny
    @property
    def tcanny(self) -> _Plugin_tcanny_Core_Bound:
        """Build an edge map using canny edge detection"""
    # end instance
    # instance_bound_Core: tdm
    @property
    def tdm(self) -> _Plugin_tdm_Core_Bound:
        """A bi-directionally motion adaptive deinterlacer"""
    # end instance
    # instance_bound_Core: tedgemask
    @property
    def tedgemask(self) -> _Plugin_tedgemask_Core_Bound:
        """Edge detection plugin"""
    # end instance
    # instance_bound_Core: text
    @property
    def text(self) -> _Plugin_text_Core_Bound:
        """VapourSynth Text"""
    # end instance
    # instance_bound_Core: tivtc
    @property
    def tivtc(self) -> _Plugin_tivtc_Core_Bound:
        """Field matching and decimation"""
    # end instance
    # instance_bound_Core: tmap
    @property
    def tmap(self) -> _Plugin_tmap_Core_Bound:
        """Hable Tonemapping"""
    # end instance
    # instance_bound_Core: tonemap
    @property
    def tonemap(self) -> _Plugin_tonemap_Core_Bound:
        """Simple tone mapping for VapourSynth"""
    # end instance
    # instance_bound_Core: trt
    @property
    def trt(self) -> _Plugin_trt_Core_Bound:
        """TensorRT ML Filter Runtime"""
    # end instance
    # instance_bound_Core: ttmpsm
    @property
    def ttmpsm(self) -> _Plugin_ttmpsm_Core_Bound:
        """A basic, motion adaptive, temporal smoothing filter"""
    # end instance
    # instance_bound_Core: vcfreq
    @property
    def vcfreq(self) -> _Plugin_vcfreq_Core_Bound:
        """VapourSynth  Frequency Domain Filters"""
    # end instance
    # instance_bound_Core: vcmod
    @property
    def vcmod(self) -> _Plugin_vcmod_Core_Bound:
        """VapourSynth Pixel Amplitude modification """
    # end instance
    # instance_bound_Core: vcmove
    @property
    def vcmove(self) -> _Plugin_vcmove_Core_Bound:
        """VapourSynth pixel repositioning Plugin"""
    # end instance
    # instance_bound_Core: vfx
    @property
    def vfx(self) -> _Plugin_vfx_Core_Bound:
        """Special Effects """
    # end instance
    # instance_bound_Core: vivtc
    @property
    def vivtc(self) -> _Plugin_vivtc_Core_Bound:
        """VFM"""
    # end instance
    # instance_bound_Core: vmaf
    @property
    def vmaf(self) -> _Plugin_vmaf_Core_Bound:
        """Video Multi-Method Assessment Fusion"""
    # end instance
    # instance_bound_Core: vscope
    @property
    def vscope(self) -> _Plugin_vscope_Core_Bound:
        """Videoscope plugin for VapourSynth"""
    # end instance
    # instance_bound_Core: vsf
    @property
    def vsf(self) -> _Plugin_vsf_Core_Bound:
        """VSFilter"""
    # end instance
    # instance_bound_Core: vsfm
    @property
    def vsfm(self) -> _Plugin_vsfm_Core_Bound:
        """VSFilterMod"""
    # end instance
    # instance_bound_Core: waifu2x
    @property
    def waifu2x(self) -> _Plugin_waifu2x_Core_Bound:
        """Waifu2x-opt image restoration filter for VapourSynth."""
    # end instance
    # instance_bound_Core: warp
    @property
    def warp(self) -> _Plugin_warp_Core_Bound:
        """Sharpen images by warping"""
    # end instance
    # instance_bound_Core: warpsf
    @property
    def warpsf(self) -> _Plugin_warpsf_Core_Bound:
        """Warpsharp floating point version"""
    # end instance
    # instance_bound_Core: wnnm
    @property
    def wnnm(self) -> _Plugin_wnnm_Core_Bound:
        """Weighted Nuclear Norm Minimization Denoiser"""
    # end instance
    # instance_bound_Core: wwxd
    @property
    def wwxd(self) -> _Plugin_wwxd_Core_Bound:
        """Scene change detection approximately like Xvid's"""
    # end instance
    # instance_bound_Core: xyvsf
    @property
    def xyvsf(self) -> _Plugin_xyvsf_Core_Bound:
        """xy-VSFilter"""
    # end instance
    # instance_bound_Core: yadifmod
    @property
    def yadifmod(self) -> _Plugin_yadifmod_Core_Bound:
        """Modification of Fizick's yadif avisynth filter"""
    # end instance
    # instance_bound_Core: znedi3
    @property
    def znedi3(self) -> _Plugin_znedi3_Core_Bound:
        """Neural network edge directed interpolation (3rd gen.)"""
    # end instance


class _CoreProxy(Core):
    @property
    def core(self) -> Core: ...


core: _CoreProxy
