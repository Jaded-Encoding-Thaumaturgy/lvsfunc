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

import ctypes
import enum
import fractions
import inspect
import types
import typing

T = typing.TypeVar("T")
SingleAndSequence = typing.Union[T, typing.Sequence[T]]


###
# ENUMS AND CONSTANTS
class MediaType(enum.IntEnum):
    VIDEO: 'MediaType'
    AUDIO: 'MediaType'


VIDEO: MediaType
AUDIO: MediaType


class ColorFamily(enum.IntEnum):
    GRAY: 'ColorFamily'
    RGB: 'ColorFamily'
    YUV: 'ColorFamily'


GRAY: ColorFamily
RGB: ColorFamily
YUV: ColorFamily


class SampleType(enum.IntEnum):
    INTEGER: 'SampleType'
    FLOAT: 'SampleType'


INTEGER: SampleType
FLOAT: SampleType


class PresetFormat(enum.IntEnum):
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


NONE: PresetFormat

GRAY8: PresetFormat
GRAY9: PresetFormat
GRAY10: PresetFormat
GRAY12: PresetFormat
GRAY14: PresetFormat
GRAY16: PresetFormat
GRAY32: PresetFormat

GRAYH: PresetFormat
GRAYS: PresetFormat

YUV420P8: PresetFormat
YUV422P8: PresetFormat
YUV444P8: PresetFormat
YUV410P8: PresetFormat
YUV411P8: PresetFormat
YUV440P8: PresetFormat

YUV420P9: PresetFormat
YUV422P9: PresetFormat
YUV444P9: PresetFormat

YUV420P10: PresetFormat
YUV422P10: PresetFormat
YUV444P10: PresetFormat

YUV420P12: PresetFormat
YUV422P12: PresetFormat
YUV444P12: PresetFormat

YUV420P14: PresetFormat
YUV422P14: PresetFormat
YUV444P14: PresetFormat

YUV420P16: PresetFormat
YUV422P16: PresetFormat
YUV444P16: PresetFormat

YUV444PH: PresetFormat
YUV444PS: PresetFormat

RGB24: PresetFormat
RGB27: PresetFormat
RGB30: PresetFormat
RGB36: PresetFormat
RGB42: PresetFormat
RGB48: PresetFormat

RGBH: PresetFormat
RGBS: PresetFormat


class AudioChannels(enum.IntEnum):
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


FRONT_LEFT: AudioChannels
FRONT_RIGHT: AudioChannels
FRONT_CENTER: AudioChannels
LOW_FREQUENCY: AudioChannels
BACK_LEFT: AudioChannels
BACK_RIGHT: AudioChannels
FRONT_LEFT_OF_CENTER: AudioChannels
FRONT_RIGHT_OF_CENTER: AudioChannels
BACK_CENTER: AudioChannels
SIDE_LEFT: AudioChannels
SIDE_RIGHT: AudioChannels
TOP_CENTER: AudioChannels
TOP_FRONT_LEFT: AudioChannels
TOP_FRONT_CENTER: AudioChannels
TOP_FRONT_RIGHT: AudioChannels
TOP_BACK_LEFT: AudioChannels
TOP_BACK_CENTER: AudioChannels
TOP_BACK_RIGHT: AudioChannels
STEREO_LEFT: AudioChannels
STEREO_RIGHT: AudioChannels
WIDE_LEFT: AudioChannels
WIDE_RIGHT: AudioChannels
SURROUND_DIRECT_LEFT: AudioChannels
SURROUND_DIRECT_RIGHT: AudioChannels
LOW_FREQUENCY2: AudioChannels


class MessageType(enum.IntEnum):
    MESSAGE_TYPE_DEBUG: 'MessageType'
    MESSAGE_TYPE_INFORMATION: 'MessageType'
    MESSAGE_TYPE_WARNING: 'MessageType'
    MESSAGE_TYPE_CRITICAL: 'MessageType'
    MESSAGE_TYPE_FATAL: 'MessageType'


MESSAGE_TYPE_DEBUG: MessageType
MESSAGE_TYPE_INFORMATION: MessageType
MESSAGE_TYPE_WARNING: MessageType
MESSAGE_TYPE_CRITICAL: MessageType
MESSAGE_TYPE_FATAL: MessageType


class VapourSynthVersion(typing.NamedTuple):
    release_major: int
    release_minor: int


__version__: VapourSynthVersion


class VapourSynthAPIVersion(typing.NamedTuple):
    api_major: int
    api_minor: int


__api_version__: VapourSynthAPIVersion


class ColorRange(enum.IntEnum):
    RANGE_FULL: 'ColorRange'
    RANGE_LIMITED: 'ColorRange'


RANGE_FULL: ColorRange
RANGE_LIMITED: ColorRange


class ChromaLocation(enum.IntEnum):
    CHROMA_LEFT: 'ChromaLocation'
    CHROMA_CENTER: 'ChromaLocation'
    CHROMA_TOP_LEFT: 'ChromaLocation'
    CHROMA_TOP: 'ChromaLocation'
    CHROMA_BOTTOM_LEFT: 'ChromaLocation'
    CHROMA_BOTTOM: 'ChromaLocation'


CHROMA_LEFT: ChromaLocation
CHROMA_CENTER: ChromaLocation
CHROMA_TOP_LEFT: ChromaLocation
CHROMA_TOP: ChromaLocation
CHROMA_BOTTOM_LEFT: ChromaLocation
CHROMA_BOTTOM: ChromaLocation


class FieldBased(enum.IntEnum):
    FIELD_PROGRESSIVE: 'FieldBased'
    FIELD_TOP: 'FieldBased'
    FIELD_BOTTOM: 'FieldBased'


FIELD_PROGRESSIVE: FieldBased
FIELD_TOP: FieldBased
FIELD_BOTTOM: FieldBased


class MatrixCoefficients(enum.IntEnum):
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


MATRIX_RGB: MatrixCoefficients
MATRIX_BT709: MatrixCoefficients
MATRIX_UNSPECIFIED: MatrixCoefficients
MATRIX_FCC: MatrixCoefficients
MATRIX_BT470_BG: MatrixCoefficients
MATRIX_ST170_M: MatrixCoefficients
MATRIX_YCGCO: MatrixCoefficients
MATRIX_BT2020_NCL: MatrixCoefficients
MATRIX_BT2020_CL: MatrixCoefficients
MATRIX_CHROMATICITY_DERIVED_NCL: MatrixCoefficients
MATRIX_CHROMATICITY_DERIVED_CL: MatrixCoefficients
MATRIX_ICTCP: MatrixCoefficients


class TransferCharacteristics(enum.IntEnum):
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


TRANSFER_BT709: TransferCharacteristics
TRANSFER_UNSPECIFIED: TransferCharacteristics
TRANSFER_BT470_M: TransferCharacteristics
TRANSFER_BT470_BG: TransferCharacteristics
TRANSFER_BT601: TransferCharacteristics
TRANSFER_ST240_M: TransferCharacteristics
TRANSFER_LINEAR: TransferCharacteristics
TRANSFER_LOG_100: TransferCharacteristics
TRANSFER_LOG_316: TransferCharacteristics
TRANSFER_IEC_61966_2_4: TransferCharacteristics
TRANSFER_IEC_61966_2_1: TransferCharacteristics
TRANSFER_BT2020_10: TransferCharacteristics
TRANSFER_BT2020_12: TransferCharacteristics
TRANSFER_ST2084: TransferCharacteristics
TRANSFER_ARIB_B67: TransferCharacteristics


class ColorPrimaries(enum.IntEnum):
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


PRIMARIES_BT709: ColorPrimaries
PRIMARIES_UNSPECIFIED: ColorPrimaries
PRIMARIES_BT470_M: ColorPrimaries
PRIMARIES_BT470_BG: ColorPrimaries
PRIMARIES_ST170_M: ColorPrimaries
PRIMARIES_ST240_M: ColorPrimaries
PRIMARIES_FILM: ColorPrimaries
PRIMARIES_BT2020: ColorPrimaries
PRIMARIES_ST428: ColorPrimaries
PRIMARIES_ST431_2: ColorPrimaries
PRIMARIES_ST432_1: ColorPrimaries
PRIMARIES_EBU3213_E: ColorPrimaries


###
# VapourSynth Environment SubSystem
class EnvironmentData:
    """
    Contains the data VapourSynth stores for a specific environment.
    """


class Environment:
    @property
    def alive(self) -> bool: ...
    @property
    def single(self) -> bool: ...
    @property
    def env_id(self) -> int: ...
    @property
    def active(self) -> bool: ...
    @classmethod
    def is_single(cls) -> bool: ...
    def copy(self) -> Environment: ...
    def use(self) -> typing.ContextManager[None]: ...

    def __enter__(self) -> Environment: ...
    def __exit__(self, ty: typing.Optional[typing.Type[BaseException]], tv: typing.Optional[BaseException], tb: typing.Optional[types.TracebackType]) -> None: ...

class EnvironmentPolicyAPI:
    def wrap_environment(self, environment_data: EnvironmentData) -> Environment: ...
    def create_environment(self, flags: int = 0) -> EnvironmentData: ...
    def set_logger(self, env: Environment, logger: typing.Callable[[int, str], None]) -> None: ...
    def destroy_environment(self, env: EnvironmentData) -> None: ...
    def unregister_policy(self) -> None: ...

class EnvironmentPolicy:
    def on_policy_registered(self, special_api: EnvironmentPolicyAPI) -> None: ...
    def on_policy_cleared(self) -> None: ...
    def get_current_environment(self) -> typing.Optional[EnvironmentData]: ...
    def set_environment(self, environment: typing.Optional[EnvironmentData]) -> None: ...
    def is_active(self, environment: EnvironmentData) -> bool: ...


def register_policy(policy: EnvironmentPolicy) -> None: ...
def has_policy() -> bool: ...

# vpy_current_environment is deprecated
def vpy_current_environment() -> Environment: ...
def get_current_environment() -> Environment: ...

def construct_signature(signature: str, return_signature: str, injected: typing.Optional[str] = None) -> inspect.Signature: ...


class VideoOutputTuple(typing.NamedTuple):
    clip: 'VideoNode'
    alpha: typing.Optional['VideoNode']
    alt_output: int


class Error(Exception): ...

def set_message_handler(handler_func: typing.Callable[[int, str], None]) -> None: ...
def clear_output(index: int = 0) -> None: ...
def clear_outputs() -> None: ...
def get_outputs() -> types.MappingProxyType[int, typing.Union[VideoOutputTuple, 'AudioNode']]: ...
def get_output(index: int = 0) -> typing.Union[VideoOutputTuple, 'AudioNode']: ...


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

    def __int__(self) -> int: ...

    def _as_dict(self) -> typing.Dict[str, typing.Any]: ...
    def replace(self, *,
                color_family: typing.Optional[ColorFamily] = None,
                sample_type: typing.Optional[SampleType] = None,
                bits_per_sample: typing.Optional[int] = None,
                subsampling_w: typing.Optional[int] = None,
                subsampling_h: typing.Optional[int] = None
                ) -> 'VideoFormat': ...


_FramePropsValue = typing.Union[
    SingleAndSequence[int],
    SingleAndSequence[float],
    SingleAndSequence[str],
    SingleAndSequence['VideoNode'],
    SingleAndSequence['VideoFrame'],
    SingleAndSequence['AudioNode'],
    SingleAndSequence['AudioFrame'],
    SingleAndSequence[typing.Callable[..., typing.Any]]
]

class FrameProps(typing.MutableMapping[str, _FramePropsValue]):

    def copy(self) -> typing.Dict[str, _FramePropsValue]: ...

    def __getattr__(self, name: str) -> _FramePropsValue: ...
    def __setattr__(self, name: str, value: _FramePropsValue) -> None: ...

    # mypy lo vult.
    # In all seriousness, why do I need to manually define them in a typestub?
    def __delitem__(self, name: str) -> None: ...
    def __setitem__(self, name: str, value: _FramePropsValue) -> None: ...
    def __getitem__(self, name: str) -> _FramePropsValue: ...
    def __iter__(self) -> typing.Iterator[str]: ...
    def __len__(self) -> int: ...


class _RawFrame:
    @property
    def readonly(self) -> bool: ...

    @property
    def props(self) -> FrameProps: ...

    def get_read_ptr(self, plane: int) -> ctypes.c_void_p: ...
    def get_write_ptr(self, plane: int) -> ctypes.c_void_p: ...
    def get_stride(self, plane: int) -> int: ...

    @property
    def closed(self) -> bool: ...

    def close(self) -> None: ...
    def __enter__(self) -> '_RawFrame': ...
    def __exit__(self, ty: typing.Optional[typing.Type[BaseException]], tv: typing.Optional[BaseException], tb: typing.Optional[types.TracebackType]) -> None: ...


class VideoFrame(_RawFrame):
    height: int
    width: int
    format: VideoFormat

    def copy(self) -> 'VideoFrame': ...
    def _writelines(self, write: typing.Callable[[bytes], int]) -> None: ...

    def __getitem__(self, index: int) -> memoryview: ...
    def __len__(self) -> int: ...
    def __enter__(self) -> 'VideoFrame': ...


class _Future(typing.Generic[T]):
    def set_result(self, value: T) -> None: ...
    def set_exception(self, exception: BaseException) -> None: ...
    def result(self) -> T: ...
    def exception(self) -> typing.Optional[typing.NoReturn]: ...


Func = typing.Callable[..., typing.Any]


class Plugin:
    identifier: str
    namespace: str
    name: str

    def functions(self) -> typing.Iterator[Function]: ...

    # get_functions is deprecated
    def get_functions(self) -> typing.Dict[str, str]: ...
    # list_functions is deprecated
    def list_functions(self) -> str: ...


class Function:
    plugin: Plugin
    name: str
    signature: str
    return_signature: str

    @property
    def __signature__(self) -> inspect.Signature: ...
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...


# implementation: DGMVC

class _Plugin_DGMVC_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DGMVCSource(self, base: typing.Union[str, bytes, bytearray], dependent: typing.Union[str, bytes, bytearray], view: int, frames: int, mode: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: acrop

class _Plugin_acrop_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AutoCrop(self, clip: "VideoNode", range: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, left: typing.Optional[int] = None, right: typing.Optional[int] = None, color: typing.Union[int, typing.Sequence[int], None] = None, color_second: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def CropProp(self, clip: "VideoNode") -> "VideoNode": ...
    def CropValues(self, clip: "VideoNode", range: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, left: typing.Optional[int] = None, right: typing.Optional[int] = None, color: typing.Union[int, typing.Sequence[int], None] = None, color_second: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_acrop_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AutoCrop(self, range: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, left: typing.Optional[int] = None, right: typing.Optional[int] = None, color: typing.Union[int, typing.Sequence[int], None] = None, color_second: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def CropProp(self) -> "VideoNode": ...
    def CropValues(self, range: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, left: typing.Optional[int] = None, right: typing.Optional[int] = None, color: typing.Union[int, typing.Sequence[int], None] = None, color_second: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: adg

class _Plugin_adg_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mask(self, clip: "VideoNode", luma_scaling: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_adg_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mask(self, luma_scaling: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: akarin

class _Plugin_akarin_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Cambi(self, clip: "VideoNode", window_size: typing.Optional[int] = None, topk: typing.Optional[float] = None, tvi_threshold: typing.Optional[float] = None, scores: typing.Optional[int] = None, scaling: typing.Optional[float] = None) -> "VideoNode": ...
    def Expr(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = None, opt: typing.Optional[int] = None, boundary: typing.Optional[int] = None) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...


class _Plugin_akarin_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Cambi(self, window_size: typing.Optional[int] = None, topk: typing.Optional[float] = None, tvi_threshold: typing.Optional[float] = None, scores: typing.Optional[int] = None, scaling: typing.Optional[float] = None) -> "VideoNode": ...
    def Expr(self, expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = None, opt: typing.Optional[int] = None, boundary: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: anime4kcpp

class _Plugin_anime4kcpp_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Anime4KCPP(self, src: "VideoNode", passes: typing.Optional[int] = None, pushColorCount: typing.Optional[int] = None, strengthColor: typing.Optional[float] = None, strengthGradient: typing.Optional[float] = None, zoomFactor: typing.Optional[int] = None, ACNet: typing.Optional[int] = None, GPUMode: typing.Optional[int] = None, GPGPUModel: typing.Union[str, bytes, bytearray, None] = None, HDN: typing.Optional[int] = None, HDNLevel: typing.Optional[int] = None, platformID: typing.Optional[int] = None, deviceID: typing.Optional[int] = None, OpenCLQueueNum: typing.Optional[int] = None, OpenCLParallelIO: typing.Optional[int] = None, safeMode: typing.Optional[int] = None) -> "VideoNode": ...
    def benchmark(self, platformID: typing.Optional[int] = None, deviceID: typing.Optional[int] = None) -> "VideoNode": ...
    def listGPUs(self, GPGPUModel: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_anime4kcpp_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Anime4KCPP(self, passes: typing.Optional[int] = None, pushColorCount: typing.Optional[int] = None, strengthColor: typing.Optional[float] = None, strengthGradient: typing.Optional[float] = None, zoomFactor: typing.Optional[int] = None, ACNet: typing.Optional[int] = None, GPUMode: typing.Optional[int] = None, GPGPUModel: typing.Union[str, bytes, bytearray, None] = None, HDN: typing.Optional[int] = None, HDNLevel: typing.Optional[int] = None, platformID: typing.Optional[int] = None, deviceID: typing.Optional[int] = None, OpenCLQueueNum: typing.Optional[int] = None, OpenCLParallelIO: typing.Optional[int] = None, safeMode: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: area

class _Plugin_area_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AreaResize(self, clip: "VideoNode", width: int, height: int, gamma: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_area_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AreaResize(self, width: int, height: int, gamma: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: asharp

class _Plugin_asharp_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ASharp(self, clip: "VideoNode", t: typing.Optional[float] = None, d: typing.Optional[float] = None, b: typing.Optional[float] = None, hqbf: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_asharp_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ASharp(self, t: typing.Optional[float] = None, d: typing.Optional[float] = None, b: typing.Optional[float] = None, hqbf: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: assrender

class _Plugin_assrender_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Subtitle(self, clip: "VideoNode", text: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], style: typing.Union[str, bytes, bytearray, None] = None, start: typing.Union[int, typing.Sequence[int], None] = None, end: typing.Union[int, typing.Sequence[int], None] = None, vfr: typing.Union[str, bytes, bytearray, None] = None, hinting: typing.Optional[int] = None, scale: typing.Optional[float] = None, line_spacing: typing.Optional[float] = None, dar: typing.Optional[float] = None, sar: typing.Optional[float] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, left: typing.Optional[int] = None, right: typing.Optional[int] = None, charset: typing.Union[str, bytes, bytearray, None] = None, debuglevel: typing.Optional[int] = None, fontdir: typing.Union[str, bytes, bytearray, None] = None, srt_font: typing.Union[str, bytes, bytearray, None] = None, colorspace: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def TextSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], vfr: typing.Union[str, bytes, bytearray, None] = None, hinting: typing.Optional[int] = None, scale: typing.Optional[float] = None, line_spacing: typing.Optional[float] = None, dar: typing.Optional[float] = None, sar: typing.Optional[float] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, left: typing.Optional[int] = None, right: typing.Optional[int] = None, charset: typing.Union[str, bytes, bytearray, None] = None, debuglevel: typing.Optional[int] = None, fontdir: typing.Union[str, bytes, bytearray, None] = None, srt_font: typing.Union[str, bytes, bytearray, None] = None, colorspace: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_assrender_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Subtitle(self, text: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], style: typing.Union[str, bytes, bytearray, None] = None, start: typing.Union[int, typing.Sequence[int], None] = None, end: typing.Union[int, typing.Sequence[int], None] = None, vfr: typing.Union[str, bytes, bytearray, None] = None, hinting: typing.Optional[int] = None, scale: typing.Optional[float] = None, line_spacing: typing.Optional[float] = None, dar: typing.Optional[float] = None, sar: typing.Optional[float] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, left: typing.Optional[int] = None, right: typing.Optional[int] = None, charset: typing.Union[str, bytes, bytearray, None] = None, debuglevel: typing.Optional[int] = None, fontdir: typing.Union[str, bytes, bytearray, None] = None, srt_font: typing.Union[str, bytes, bytearray, None] = None, colorspace: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def TextSub(self, file: typing.Union[str, bytes, bytearray], vfr: typing.Union[str, bytes, bytearray, None] = None, hinting: typing.Optional[int] = None, scale: typing.Optional[float] = None, line_spacing: typing.Optional[float] = None, dar: typing.Optional[float] = None, sar: typing.Optional[float] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, left: typing.Optional[int] = None, right: typing.Optional[int] = None, charset: typing.Union[str, bytes, bytearray, None] = None, debuglevel: typing.Optional[int] = None, fontdir: typing.Union[str, bytes, bytearray, None] = None, srt_font: typing.Union[str, bytes, bytearray, None] = None, colorspace: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: average

class _Plugin_average_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mean(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None, preset: typing.Optional[int] = None, discard: typing.Optional[int] = None) -> "VideoNode": ...
    def Median(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None) -> "VideoNode": ...


class _Plugin_average_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mean(self, preset: typing.Optional[int] = None, discard: typing.Optional[int] = None) -> "VideoNode": ...
    def Median(self) -> "VideoNode": ...

# end implementation


# implementation: avs

class _Plugin_avs_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LoadPlugin(self, path: typing.Union[str, bytes, bytearray]) -> None: ...

# end implementation


# implementation: avsr

class _Plugin_avsr_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Eval(self, lines: typing.Union[str, bytes, bytearray], bitdepth: typing.Optional[int] = None, alpha: typing.Optional[int] = None) -> "VideoNode": ...
    def Import(self, script: typing.Union[str, bytes, bytearray], bitdepth: typing.Optional[int] = None, alpha: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: avsw

class _Plugin_avsw_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Eval(self, script: typing.Union[str, bytes, bytearray], clips: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None, clip_names: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, avisynth: typing.Union[str, bytes, bytearray, None] = None, slave: typing.Union[str, bytes, bytearray, None] = None, slave_log: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_avsw_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Eval(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None, clip_names: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, avisynth: typing.Union[str, bytes, bytearray, None] = None, slave: typing.Union[str, bytes, bytearray, None] = None, slave_log: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: bas

class _Plugin_bas_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Source(self, source: typing.Union[str, bytes, bytearray], track: typing.Optional[int] = None, adjustdelay: typing.Optional[int] = None, exactsamples: typing.Optional[int] = None, enable_drefs: typing.Optional[int] = None, use_absolute_path: typing.Optional[int] = None, drc_scale: typing.Optional[float] = None) -> "AudioNode": ...

# end implementation


# implementation: bezier

class _Plugin_bezier_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Cubic(self, clip: "VideoNode", accur: typing.Optional[float] = None, input_range: typing.Optional[int] = None, begin: typing.Optional[int] = None, end: typing.Optional[int] = None, x1: typing.Optional[int] = None, y1: typing.Optional[int] = None, x2: typing.Optional[int] = None, y2: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Quadratic(self, clip: "VideoNode", accur: typing.Optional[float] = None, input_range: typing.Optional[int] = None, begin: typing.Optional[int] = None, end: typing.Optional[int] = None, x1: typing.Optional[int] = None, y1: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_bezier_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Cubic(self, accur: typing.Optional[float] = None, input_range: typing.Optional[int] = None, begin: typing.Optional[int] = None, end: typing.Optional[int] = None, x1: typing.Optional[int] = None, y1: typing.Optional[int] = None, x2: typing.Optional[int] = None, y2: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Quadratic(self, accur: typing.Optional[float] = None, input_range: typing.Optional[int] = None, begin: typing.Optional[int] = None, end: typing.Optional[int] = None, x1: typing.Optional[int] = None, y1: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: bifrost

class _Plugin_bifrost_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bifrost(self, clip: "VideoNode", altclip: typing.Optional["VideoNode"] = None, luma_thresh: typing.Optional[float] = None, variation: typing.Optional[int] = None, conservative_mask: typing.Optional[int] = None, interlaced: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None) -> "VideoNode": ...
    def BlockDiff(self, clip: "VideoNode", interlaced: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_bifrost_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bifrost(self, altclip: typing.Optional["VideoNode"] = None, luma_thresh: typing.Optional[float] = None, variation: typing.Optional[int] = None, conservative_mask: typing.Optional[int] = None, interlaced: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None) -> "VideoNode": ...
    def BlockDiff(self, interlaced: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: bilateral

class _Plugin_bilateral_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bilateral(self, input: "VideoNode", ref: typing.Optional["VideoNode"] = None, sigmaS: typing.Union[float, typing.Sequence[float], None] = None, sigmaR: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, algorithm: typing.Union[int, typing.Sequence[int], None] = None, PBFICnum: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Gaussian(self, input: "VideoNode", sigma: typing.Union[float, typing.Sequence[float], None] = None, sigmaV: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...


class _Plugin_bilateral_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bilateral(self, ref: typing.Optional["VideoNode"] = None, sigmaS: typing.Union[float, typing.Sequence[float], None] = None, sigmaR: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, algorithm: typing.Union[int, typing.Sequence[int], None] = None, PBFICnum: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Gaussian(self, sigma: typing.Union[float, typing.Sequence[float], None] = None, sigmaV: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...

# end implementation


# implementation: bilateralgpu

class _Plugin_bilateralgpu_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bilateral(self, clip: "VideoNode", sigma_spatial: typing.Union[float, typing.Sequence[float], None] = None, sigma_color: typing.Union[float, typing.Sequence[float], None] = None, radius: typing.Union[int, typing.Sequence[int], None] = None, device_id: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, use_shared_memory: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_bilateralgpu_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bilateral(self, sigma_spatial: typing.Union[float, typing.Sequence[float], None] = None, sigma_color: typing.Union[float, typing.Sequence[float], None] = None, radius: typing.Union[int, typing.Sequence[int], None] = None, device_id: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, use_shared_memory: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: bm3d

class _Plugin_bm3d_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Basic(self, input: "VideoNode", ref: typing.Optional["VideoNode"] = None, profile: typing.Union[str, bytes, bytearray, None] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_size: typing.Optional[int] = None, block_step: typing.Optional[int] = None, group_size: typing.Optional[int] = None, bm_range: typing.Optional[int] = None, bm_step: typing.Optional[int] = None, th_mse: typing.Optional[float] = None, hard_thr: typing.Optional[float] = None, matrix: typing.Optional[int] = None) -> "VideoNode": ...
    def Final(self, input: "VideoNode", ref: "VideoNode", profile: typing.Union[str, bytes, bytearray, None] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_size: typing.Optional[int] = None, block_step: typing.Optional[int] = None, group_size: typing.Optional[int] = None, bm_range: typing.Optional[int] = None, bm_step: typing.Optional[int] = None, th_mse: typing.Optional[float] = None, matrix: typing.Optional[int] = None) -> "VideoNode": ...
    def OPP2RGB(self, input: "VideoNode", sample: typing.Optional[int] = None) -> "VideoNode": ...
    def RGB2OPP(self, input: "VideoNode", sample: typing.Optional[int] = None) -> "VideoNode": ...
    def VAggregate(self, input: "VideoNode", radius: typing.Optional[int] = None, sample: typing.Optional[int] = None) -> "VideoNode": ...
    def VBasic(self, input: "VideoNode", ref: typing.Optional["VideoNode"] = None, profile: typing.Union[str, bytes, bytearray, None] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, radius: typing.Optional[int] = None, block_size: typing.Optional[int] = None, block_step: typing.Optional[int] = None, group_size: typing.Optional[int] = None, bm_range: typing.Optional[int] = None, bm_step: typing.Optional[int] = None, ps_num: typing.Optional[int] = None, ps_range: typing.Optional[int] = None, ps_step: typing.Optional[int] = None, th_mse: typing.Optional[float] = None, hard_thr: typing.Optional[float] = None, matrix: typing.Optional[int] = None) -> "VideoNode": ...
    def VFinal(self, input: "VideoNode", ref: "VideoNode", profile: typing.Union[str, bytes, bytearray, None] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, radius: typing.Optional[int] = None, block_size: typing.Optional[int] = None, block_step: typing.Optional[int] = None, group_size: typing.Optional[int] = None, bm_range: typing.Optional[int] = None, bm_step: typing.Optional[int] = None, ps_num: typing.Optional[int] = None, ps_range: typing.Optional[int] = None, ps_step: typing.Optional[int] = None, th_mse: typing.Optional[float] = None, matrix: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_bm3d_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Basic(self, ref: typing.Optional["VideoNode"] = None, profile: typing.Union[str, bytes, bytearray, None] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_size: typing.Optional[int] = None, block_step: typing.Optional[int] = None, group_size: typing.Optional[int] = None, bm_range: typing.Optional[int] = None, bm_step: typing.Optional[int] = None, th_mse: typing.Optional[float] = None, hard_thr: typing.Optional[float] = None, matrix: typing.Optional[int] = None) -> "VideoNode": ...
    def Final(self, ref: "VideoNode", profile: typing.Union[str, bytes, bytearray, None] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_size: typing.Optional[int] = None, block_step: typing.Optional[int] = None, group_size: typing.Optional[int] = None, bm_range: typing.Optional[int] = None, bm_step: typing.Optional[int] = None, th_mse: typing.Optional[float] = None, matrix: typing.Optional[int] = None) -> "VideoNode": ...
    def OPP2RGB(self, sample: typing.Optional[int] = None) -> "VideoNode": ...
    def RGB2OPP(self, sample: typing.Optional[int] = None) -> "VideoNode": ...
    def VAggregate(self, radius: typing.Optional[int] = None, sample: typing.Optional[int] = None) -> "VideoNode": ...
    def VBasic(self, ref: typing.Optional["VideoNode"] = None, profile: typing.Union[str, bytes, bytearray, None] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, radius: typing.Optional[int] = None, block_size: typing.Optional[int] = None, block_step: typing.Optional[int] = None, group_size: typing.Optional[int] = None, bm_range: typing.Optional[int] = None, bm_step: typing.Optional[int] = None, ps_num: typing.Optional[int] = None, ps_range: typing.Optional[int] = None, ps_step: typing.Optional[int] = None, th_mse: typing.Optional[float] = None, hard_thr: typing.Optional[float] = None, matrix: typing.Optional[int] = None) -> "VideoNode": ...
    def VFinal(self, ref: "VideoNode", profile: typing.Union[str, bytes, bytearray, None] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, radius: typing.Optional[int] = None, block_size: typing.Optional[int] = None, block_step: typing.Optional[int] = None, group_size: typing.Optional[int] = None, bm_range: typing.Optional[int] = None, bm_step: typing.Optional[int] = None, ps_num: typing.Optional[int] = None, ps_range: typing.Optional[int] = None, ps_step: typing.Optional[int] = None, th_mse: typing.Optional[float] = None, matrix: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: bm3dcpu

class _Plugin_bm3dcpu_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BM3D(self, clip: "VideoNode", ref: typing.Optional["VideoNode"] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_step: typing.Union[int, typing.Sequence[int], None] = None, bm_range: typing.Union[int, typing.Sequence[int], None] = None, radius: typing.Optional[int] = None, ps_num: typing.Optional[int] = None, ps_range: typing.Optional[int] = None, chroma: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_bm3dcpu_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BM3D(self, ref: typing.Optional["VideoNode"] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_step: typing.Union[int, typing.Sequence[int], None] = None, bm_range: typing.Union[int, typing.Sequence[int], None] = None, radius: typing.Optional[int] = None, ps_num: typing.Optional[int] = None, ps_range: typing.Optional[int] = None, chroma: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: bm3dcuda

class _Plugin_bm3dcuda_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BM3D(self, clip: "VideoNode", ref: typing.Optional["VideoNode"] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_step: typing.Union[int, typing.Sequence[int], None] = None, bm_range: typing.Union[int, typing.Sequence[int], None] = None, radius: typing.Optional[int] = None, ps_num: typing.Union[int, typing.Sequence[int], None] = None, ps_range: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, device_id: typing.Optional[int] = None, fast: typing.Optional[int] = None, extractor_exp: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_bm3dcuda_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BM3D(self, ref: typing.Optional["VideoNode"] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_step: typing.Union[int, typing.Sequence[int], None] = None, bm_range: typing.Union[int, typing.Sequence[int], None] = None, radius: typing.Optional[int] = None, ps_num: typing.Union[int, typing.Sequence[int], None] = None, ps_range: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, device_id: typing.Optional[int] = None, fast: typing.Optional[int] = None, extractor_exp: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: bm3dcuda_rtc

class _Plugin_bm3dcuda_rtc_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BM3D(self, clip: "VideoNode", ref: typing.Optional["VideoNode"] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_step: typing.Union[int, typing.Sequence[int], None] = None, bm_range: typing.Union[int, typing.Sequence[int], None] = None, radius: typing.Optional[int] = None, ps_num: typing.Union[int, typing.Sequence[int], None] = None, ps_range: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, device_id: typing.Optional[int] = None, fast: typing.Optional[int] = None, extractor_exp: typing.Optional[int] = None, bm_error_s: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, transform_2d_s: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, transform_1d_s: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...


class _Plugin_bm3dcuda_rtc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BM3D(self, ref: typing.Optional["VideoNode"] = None, sigma: typing.Union[float, typing.Sequence[float], None] = None, block_step: typing.Union[int, typing.Sequence[int], None] = None, bm_range: typing.Union[int, typing.Sequence[int], None] = None, radius: typing.Optional[int] = None, ps_num: typing.Union[int, typing.Sequence[int], None] = None, ps_range: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, device_id: typing.Optional[int] = None, fast: typing.Optional[int] = None, extractor_exp: typing.Optional[int] = None, bm_error_s: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, transform_2d_s: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, transform_1d_s: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...

# end implementation


# implementation: box

class _Plugin_box_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Blur(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, hradius: typing.Optional[int] = None, hpasses: typing.Optional[int] = None, vradius: typing.Optional[int] = None, vpasses: typing.Optional[int] = None) -> "VideoNode": ...
    def BlurV(self, clip: "VideoNode", radius: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...


class _Plugin_box_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Blur(self, planes: typing.Union[int, typing.Sequence[int], None] = None, hradius: typing.Optional[int] = None, hpasses: typing.Optional[int] = None, vradius: typing.Optional[int] = None, vpasses: typing.Optional[int] = None) -> "VideoNode": ...
    def BlurV(self, radius: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: butteraugli

class _Plugin_butteraugli_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def butteraugli(self, clipa: "VideoNode", clipb: "VideoNode", heatmap: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_butteraugli_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def butteraugli(self, clipb: "VideoNode", heatmap: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: bwdif

class _Plugin_bwdif_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bwdif(self, clip: "VideoNode", field: int, edeint: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_bwdif_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bwdif(self, field: int, edeint: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: caffe

class _Plugin_caffe_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, clip: "VideoNode", noise: typing.Optional[int] = None, scale: typing.Optional[int] = None, block_w: typing.Optional[int] = None, block_h: typing.Optional[int] = None, model: typing.Optional[int] = None, cudnn: typing.Optional[int] = None, processor: typing.Optional[int] = None, tta: typing.Optional[int] = None, batch: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_caffe_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, noise: typing.Optional[int] = None, scale: typing.Optional[int] = None, block_w: typing.Optional[int] = None, block_h: typing.Optional[int] = None, model: typing.Optional[int] = None, cudnn: typing.Optional[int] = None, processor: typing.Optional[int] = None, tta: typing.Optional[int] = None, batch: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: cas

class _Plugin_cas_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CAS(self, clip: "VideoNode", sharpness: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_cas_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CAS(self, sharpness: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: ccd

class _Plugin_ccd_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CCD(self, clip: "VideoNode", threshold: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_ccd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CCD(self, threshold: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: cf

class _Plugin_cf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ContinuityFixer(self, clip: "VideoNode", left: typing.Union[int, typing.Sequence[int], None] = None, top: typing.Union[int, typing.Sequence[int], None] = None, right: typing.Union[int, typing.Sequence[int], None] = None, bottom: typing.Union[int, typing.Sequence[int], None] = None, radius: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_cf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ContinuityFixer(self, left: typing.Union[int, typing.Sequence[int], None] = None, top: typing.Union[int, typing.Sequence[int], None] = None, right: typing.Union[int, typing.Sequence[int], None] = None, bottom: typing.Union[int, typing.Sequence[int], None] = None, radius: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: chkdr

class _Plugin_chkdr_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def grain(self, clip: "VideoNode", sigma: typing.Optional[float] = None, res: typing.Optional[int] = None, rad: typing.Optional[float] = None, dev: typing.Optional[float] = None, seed: typing.Optional[int] = None, cf: typing.Optional[int] = None, cp: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_chkdr_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def grain(self, sigma: typing.Optional[float] = None, res: typing.Optional[int] = None, rad: typing.Optional[float] = None, dev: typing.Optional[float] = None, seed: typing.Optional[int] = None, cf: typing.Optional[int] = None, cp: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: cnr2

class _Plugin_cnr2_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Cnr2(self, clip: "VideoNode", mode: typing.Union[str, bytes, bytearray, None] = None, scdthr: typing.Optional[float] = None, ln: typing.Optional[int] = None, lm: typing.Optional[int] = None, un: typing.Optional[int] = None, um: typing.Optional[int] = None, vn: typing.Optional[int] = None, vm: typing.Optional[int] = None, scenechroma: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_cnr2_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Cnr2(self, mode: typing.Union[str, bytes, bytearray, None] = None, scdthr: typing.Optional[float] = None, ln: typing.Optional[int] = None, lm: typing.Optional[int] = None, un: typing.Optional[int] = None, um: typing.Optional[int] = None, vn: typing.Optional[int] = None, vm: typing.Optional[int] = None, scenechroma: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: colorbars

class _Plugin_colorbars_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ColorBars(self, resolution: typing.Optional[int] = None, format: typing.Optional[int] = None, hdr: typing.Optional[int] = None, wcg: typing.Optional[int] = None, compatability: typing.Optional[int] = None, subblack: typing.Optional[int] = None, superwhite: typing.Optional[int] = None, iq: typing.Optional[int] = None, filter: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: comb

class _Plugin_comb_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CMaskedMerge(self, base: "VideoNode", alt: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def CombMask(self, clip: "VideoNode", cthresh: typing.Optional[int] = None, mthresh: typing.Optional[int] = None, mi: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_comb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CMaskedMerge(self, alt: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def CombMask(self, cthresh: typing.Optional[int] = None, mthresh: typing.Optional[int] = None, mi: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: ctmf

class _Plugin_ctmf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CTMF(self, clip: "VideoNode", radius: typing.Optional[int] = None, memsize: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_ctmf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CTMF(self, radius: typing.Optional[int] = None, memsize: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: curve

class _Plugin_curve_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Curve(self, clip: "VideoNode", preset: typing.Optional[int] = None, r: typing.Union[float, typing.Sequence[float], None] = None, g: typing.Union[float, typing.Sequence[float], None] = None, b: typing.Union[float, typing.Sequence[float], None] = None, master: typing.Union[float, typing.Sequence[float], None] = None, acv: typing.Union[str, bytes, bytearray, None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_curve_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Curve(self, preset: typing.Optional[int] = None, r: typing.Union[float, typing.Sequence[float], None] = None, g: typing.Union[float, typing.Sequence[float], None] = None, b: typing.Union[float, typing.Sequence[float], None] = None, master: typing.Union[float, typing.Sequence[float], None] = None, acv: typing.Union[str, bytes, bytearray, None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: d2v

class _Plugin_d2v_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ApplyRFF(self, clip: "VideoNode", d2v: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Source(self, input: typing.Union[str, bytes, bytearray], threads: typing.Optional[int] = None, nocrop: typing.Optional[int] = None, rff: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_d2v_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ApplyRFF(self, d2v: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...

# end implementation


# implementation: damb

class _Plugin_damb_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], delay: typing.Optional[float] = None) -> "VideoNode": ...
    def Write(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], format: typing.Union[str, bytes, bytearray, None] = None, sample_type: typing.Union[str, bytes, bytearray, None] = None, quality: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_damb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, file: typing.Union[str, bytes, bytearray], delay: typing.Optional[float] = None) -> "VideoNode": ...
    def Write(self, file: typing.Union[str, bytes, bytearray], format: typing.Union[str, bytes, bytearray, None] = None, sample_type: typing.Union[str, bytes, bytearray, None] = None, quality: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: dct

class _Plugin_dct_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Filter(self, clip: "VideoNode", factors: typing.Union[float, typing.Sequence[float]]) -> "VideoNode": ...


class _Plugin_dct_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Filter(self, factors: typing.Union[float, typing.Sequence[float]]) -> "VideoNode": ...

# end implementation


# implementation: dctf

class _Plugin_dctf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DCTFilter(self, clip: "VideoNode", factors: typing.Union[float, typing.Sequence[float]], planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_dctf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DCTFilter(self, factors: typing.Union[float, typing.Sequence[float]], planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: deblock

class _Plugin_deblock_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deblock(self, clip: "VideoNode", quant: typing.Optional[int] = None, aoffset: typing.Optional[int] = None, boffset: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_deblock_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deblock(self, quant: typing.Optional[int] = None, aoffset: typing.Optional[int] = None, boffset: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: decross

class _Plugin_decross_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DeCross(self, clip: "VideoNode", thresholdy: typing.Optional[int] = None, noise: typing.Optional[int] = None, margin: typing.Optional[int] = None, debug: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_decross_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DeCross(self, thresholdy: typing.Optional[int] = None, noise: typing.Optional[int] = None, margin: typing.Optional[int] = None, debug: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: dedot

class _Plugin_dedot_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Dedot(self, clip: "VideoNode", luma_2d: typing.Optional[int] = None, luma_t: typing.Optional[int] = None, chroma_t1: typing.Optional[int] = None, chroma_t2: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_dedot_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Dedot(self, luma_2d: typing.Optional[int] = None, luma_t: typing.Optional[int] = None, chroma_t1: typing.Optional[int] = None, chroma_t2: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: delogo

class _Plugin_delogo_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddLogo(self, clip: "VideoNode", logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = None, pos_x: typing.Optional[int] = None, pos_y: typing.Optional[int] = None, depth: typing.Optional[int] = None, yc_y: typing.Optional[int] = None, yc_u: typing.Optional[int] = None, yc_v: typing.Optional[int] = None, start: typing.Optional[int] = None, end: typing.Optional[int] = None, fadein: typing.Optional[int] = None, fadeout: typing.Optional[int] = None, cutoff: typing.Optional[int] = None) -> "VideoNode": ...
    def EraseLogo(self, clip: "VideoNode", logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = None, pos_x: typing.Optional[int] = None, pos_y: typing.Optional[int] = None, depth: typing.Optional[int] = None, yc_y: typing.Optional[int] = None, yc_u: typing.Optional[int] = None, yc_v: typing.Optional[int] = None, start: typing.Optional[int] = None, end: typing.Optional[int] = None, fadein: typing.Optional[int] = None, fadeout: typing.Optional[int] = None, cutoff: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_delogo_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddLogo(self, logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = None, pos_x: typing.Optional[int] = None, pos_y: typing.Optional[int] = None, depth: typing.Optional[int] = None, yc_y: typing.Optional[int] = None, yc_u: typing.Optional[int] = None, yc_v: typing.Optional[int] = None, start: typing.Optional[int] = None, end: typing.Optional[int] = None, fadein: typing.Optional[int] = None, fadeout: typing.Optional[int] = None, cutoff: typing.Optional[int] = None) -> "VideoNode": ...
    def EraseLogo(self, logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = None, pos_x: typing.Optional[int] = None, pos_y: typing.Optional[int] = None, depth: typing.Optional[int] = None, yc_y: typing.Optional[int] = None, yc_u: typing.Optional[int] = None, yc_v: typing.Optional[int] = None, start: typing.Optional[int] = None, end: typing.Optional[int] = None, fadein: typing.Optional[int] = None, fadeout: typing.Optional[int] = None, cutoff: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: delogohd

class _Plugin_delogohd_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddlogoHD(self, clip: "VideoNode", logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = None, left: typing.Optional[int] = None, top: typing.Optional[int] = None, start: typing.Optional[int] = None, end: typing.Optional[int] = None, fadein: typing.Optional[int] = None, fadeout: typing.Optional[int] = None, mono: typing.Optional[int] = None, cutoff: typing.Optional[int] = None) -> "VideoNode": ...
    def DelogoHD(self, clip: "VideoNode", logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = None, left: typing.Optional[int] = None, top: typing.Optional[int] = None, start: typing.Optional[int] = None, end: typing.Optional[int] = None, fadein: typing.Optional[int] = None, fadeout: typing.Optional[int] = None, mono: typing.Optional[int] = None, cutoff: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_delogohd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddlogoHD(self, logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = None, left: typing.Optional[int] = None, top: typing.Optional[int] = None, start: typing.Optional[int] = None, end: typing.Optional[int] = None, fadein: typing.Optional[int] = None, fadeout: typing.Optional[int] = None, mono: typing.Optional[int] = None, cutoff: typing.Optional[int] = None) -> "VideoNode": ...
    def DelogoHD(self, logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = None, left: typing.Optional[int] = None, top: typing.Optional[int] = None, start: typing.Optional[int] = None, end: typing.Optional[int] = None, fadein: typing.Optional[int] = None, fadeout: typing.Optional[int] = None, mono: typing.Optional[int] = None, cutoff: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: depan

class _Plugin_depan_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DePan(self, clip: "VideoNode", data: "VideoNode", offset: typing.Optional[float] = None, pixaspect: typing.Optional[float] = None, matchfields: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def DePanEstimate(self, clip: "VideoNode", range: typing.Optional[int] = None, trust: typing.Optional[float] = None, winx: typing.Optional[int] = None, winy: typing.Optional[int] = None, wleft: typing.Optional[int] = None, wtop: typing.Optional[int] = None, dxmax: typing.Optional[int] = None, dymax: typing.Optional[int] = None, zoommax: typing.Optional[float] = None, stab: typing.Optional[float] = None, pixaspect: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_depan_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DePan(self, data: "VideoNode", offset: typing.Optional[float] = None, pixaspect: typing.Optional[float] = None, matchfields: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def DePanEstimate(self, range: typing.Optional[int] = None, trust: typing.Optional[float] = None, winx: typing.Optional[int] = None, winy: typing.Optional[int] = None, wleft: typing.Optional[int] = None, wtop: typing.Optional[int] = None, dxmax: typing.Optional[int] = None, dymax: typing.Optional[int] = None, zoommax: typing.Optional[float] = None, stab: typing.Optional[float] = None, pixaspect: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: descale

class _Plugin_descale_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Debicubic(self, src: "VideoNode", width: int, height: int, b: typing.Optional[float] = None, c: typing.Optional[float] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Debilinear(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Delanczos(self, src: "VideoNode", width: int, height: int, taps: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Descale(self, src: "VideoNode", width: int, height: int, kernel: typing.Union[str, bytes, bytearray, None] = None, custom_kernel: typing.Optional[typing.Callable[..., typing.Any]] = None, taps: typing.Optional[int] = None, b: typing.Optional[float] = None, c: typing.Optional[float] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline16(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline36(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline64(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_descale_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Debicubic(self, width: int, height: int, b: typing.Optional[float] = None, c: typing.Optional[float] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Debilinear(self, width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Delanczos(self, width: int, height: int, taps: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Descale(self, width: int, height: int, kernel: typing.Union[str, bytes, bytearray, None] = None, custom_kernel: typing.Optional[typing.Callable[..., typing.Any]] = None, taps: typing.Optional[int] = None, b: typing.Optional[float] = None, c: typing.Optional[float] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline16(self, width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline36(self, width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline64(self, width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, force: typing.Optional[int] = None, force_h: typing.Optional[int] = None, force_v: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: descale_getnative

class _Plugin_descale_getnative_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Debicubic(self, src: "VideoNode", width: int, height: int, b: typing.Optional[float] = None, c: typing.Optional[float] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...
    def Debilinear(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...
    def Delanczos(self, src: "VideoNode", width: int, height: int, taps: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline16(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline36(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_descale_getnative_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Debicubic(self, width: int, height: int, b: typing.Optional[float] = None, c: typing.Optional[float] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...
    def Debilinear(self, width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...
    def Delanczos(self, width: int, height: int, taps: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline16(self, width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...
    def Despline36(self, width: int, height: int, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, cache_size: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: dfttest

class _Plugin_dfttest_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DFTTest(self, clip: "VideoNode", ftype: typing.Optional[int] = None, sigma: typing.Optional[float] = None, sigma2: typing.Optional[float] = None, pmin: typing.Optional[float] = None, pmax: typing.Optional[float] = None, sbsize: typing.Optional[int] = None, smode: typing.Optional[int] = None, sosize: typing.Optional[int] = None, tbsize: typing.Optional[int] = None, tmode: typing.Optional[int] = None, tosize: typing.Optional[int] = None, swin: typing.Optional[int] = None, twin: typing.Optional[int] = None, sbeta: typing.Optional[float] = None, tbeta: typing.Optional[float] = None, zmean: typing.Optional[int] = None, f0beta: typing.Optional[float] = None, nlocation: typing.Union[int, typing.Sequence[int], None] = None, alpha: typing.Optional[float] = None, slocation: typing.Union[float, typing.Sequence[float], None] = None, ssx: typing.Union[float, typing.Sequence[float], None] = None, ssy: typing.Union[float, typing.Sequence[float], None] = None, sst: typing.Union[float, typing.Sequence[float], None] = None, ssystem: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_dfttest_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DFTTest(self, ftype: typing.Optional[int] = None, sigma: typing.Optional[float] = None, sigma2: typing.Optional[float] = None, pmin: typing.Optional[float] = None, pmax: typing.Optional[float] = None, sbsize: typing.Optional[int] = None, smode: typing.Optional[int] = None, sosize: typing.Optional[int] = None, tbsize: typing.Optional[int] = None, tmode: typing.Optional[int] = None, tosize: typing.Optional[int] = None, swin: typing.Optional[int] = None, twin: typing.Optional[int] = None, sbeta: typing.Optional[float] = None, tbeta: typing.Optional[float] = None, zmean: typing.Optional[int] = None, f0beta: typing.Optional[float] = None, nlocation: typing.Union[int, typing.Sequence[int], None] = None, alpha: typing.Optional[float] = None, slocation: typing.Union[float, typing.Sequence[float], None] = None, ssx: typing.Union[float, typing.Sequence[float], None] = None, ssy: typing.Union[float, typing.Sequence[float], None] = None, sst: typing.Union[float, typing.Sequence[float], None] = None, ssystem: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: dgdecodenv

class _Plugin_dgdecodenv_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DGSource(self, source: typing.Union[str, bytes, bytearray], i420: typing.Optional[int] = None, deinterlace: typing.Optional[int] = None, use_top_field: typing.Optional[int] = None, use_pf: typing.Optional[int] = None, ct: typing.Optional[int] = None, cb: typing.Optional[int] = None, cl: typing.Optional[int] = None, cr: typing.Optional[int] = None, rw: typing.Optional[int] = None, rh: typing.Optional[int] = None, fieldop: typing.Optional[int] = None, show: typing.Optional[int] = None, show2: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: dghdrtosdr

class _Plugin_dghdrtosdr_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DGHDRtoSDR(self, clip: "VideoNode", white: typing.Optional[int] = None, black: typing.Optional[int] = None, gamma: typing.Optional[float] = None, hue: typing.Optional[float] = None, r: typing.Optional[float] = None, g: typing.Optional[float] = None, b: typing.Optional[float] = None, tm: typing.Optional[float] = None, roll: typing.Optional[float] = None, fulldepth: typing.Optional[int] = None, impl: typing.Union[str, bytes, bytearray, None] = None, mode: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_dghdrtosdr_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DGHDRtoSDR(self, white: typing.Optional[int] = None, black: typing.Optional[int] = None, gamma: typing.Optional[float] = None, hue: typing.Optional[float] = None, r: typing.Optional[float] = None, g: typing.Optional[float] = None, b: typing.Optional[float] = None, tm: typing.Optional[float] = None, roll: typing.Optional[float] = None, fulldepth: typing.Optional[int] = None, impl: typing.Union[str, bytes, bytearray, None] = None, mode: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: dgm

class _Plugin_dgm_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DegrainMedian(self, clip: "VideoNode", limit: typing.Union[int, typing.Sequence[int], None] = None, mode: typing.Union[int, typing.Sequence[int], None] = None, interlaced: typing.Optional[int] = None, norow: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_dgm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DegrainMedian(self, limit: typing.Union[int, typing.Sequence[int], None] = None, mode: typing.Union[int, typing.Sequence[int], None] = None, interlaced: typing.Optional[int] = None, norow: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: dotkill

class _Plugin_dotkill_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DotKillS(self, clip: "VideoNode", iterations: typing.Optional[int] = None, usematch: typing.Optional[int] = None) -> "VideoNode": ...
    def DotKillT(self, clip: "VideoNode", order: typing.Optional[int] = None, offset: typing.Optional[int] = None, dupthresh: typing.Optional[int] = None, tratio: typing.Optional[int] = None, show: typing.Optional[int] = None) -> "VideoNode": ...
    def DotKillZ(self, clip: "VideoNode", order: typing.Optional[int] = None, offset: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_dotkill_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DotKillS(self, iterations: typing.Optional[int] = None, usematch: typing.Optional[int] = None) -> "VideoNode": ...
    def DotKillT(self, order: typing.Optional[int] = None, offset: typing.Optional[int] = None, dupthresh: typing.Optional[int] = None, tratio: typing.Optional[int] = None, show: typing.Optional[int] = None) -> "VideoNode": ...
    def DotKillZ(self, order: typing.Optional[int] = None, offset: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: dpid

class _Plugin_dpid_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Dpid(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, lambda_: typing.Union[float, typing.Sequence[float], None] = None, src_left: typing.Union[float, typing.Sequence[float], None] = None, src_top: typing.Union[float, typing.Sequence[float], None] = None, read_chromaloc: typing.Optional[int] = None) -> "VideoNode": ...
    def DpidRaw(self, clip: "VideoNode", clip2: "VideoNode", lambda_: typing.Union[float, typing.Sequence[float], None] = None, src_left: typing.Union[float, typing.Sequence[float], None] = None, src_top: typing.Union[float, typing.Sequence[float], None] = None, read_chromaloc: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_dpid_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Dpid(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, lambda_: typing.Union[float, typing.Sequence[float], None] = None, src_left: typing.Union[float, typing.Sequence[float], None] = None, src_top: typing.Union[float, typing.Sequence[float], None] = None, read_chromaloc: typing.Optional[int] = None) -> "VideoNode": ...
    def DpidRaw(self, clip2: "VideoNode", lambda_: typing.Union[float, typing.Sequence[float], None] = None, src_left: typing.Union[float, typing.Sequence[float], None] = None, src_top: typing.Union[float, typing.Sequence[float], None] = None, read_chromaloc: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: draw

class _Plugin_draw_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Draw(self, clip: "VideoNode", expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]]) -> "VideoNode": ...


class _Plugin_draw_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Draw(self, expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]]) -> "VideoNode": ...

# end implementation


# implementation: edgefixer

class _Plugin_edgefixer_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Continuity(self, clip: "VideoNode", left: typing.Optional[int] = None, top: typing.Optional[int] = None, right: typing.Optional[int] = None, bottom: typing.Optional[int] = None, radius: typing.Optional[int] = None) -> "VideoNode": ...
    def Reference(self, clip: "VideoNode", ref: "VideoNode", left: typing.Optional[int] = None, top: typing.Optional[int] = None, right: typing.Optional[int] = None, bottom: typing.Optional[int] = None, radius: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_edgefixer_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Continuity(self, left: typing.Optional[int] = None, top: typing.Optional[int] = None, right: typing.Optional[int] = None, bottom: typing.Optional[int] = None, radius: typing.Optional[int] = None) -> "VideoNode": ...
    def Reference(self, ref: "VideoNode", left: typing.Optional[int] = None, top: typing.Optional[int] = None, right: typing.Optional[int] = None, bottom: typing.Optional[int] = None, radius: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: eedi2

class _Plugin_eedi2_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI2(self, clip: "VideoNode", field: int, mthresh: typing.Optional[int] = None, lthresh: typing.Optional[int] = None, vthresh: typing.Optional[int] = None, estr: typing.Optional[int] = None, dstr: typing.Optional[int] = None, maxd: typing.Optional[int] = None, map: typing.Optional[int] = None, nt: typing.Optional[int] = None, pp: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_eedi2_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI2(self, field: int, mthresh: typing.Optional[int] = None, lthresh: typing.Optional[int] = None, vthresh: typing.Optional[int] = None, estr: typing.Optional[int] = None, dstr: typing.Optional[int] = None, maxd: typing.Optional[int] = None, map: typing.Optional[int] = None, nt: typing.Optional[int] = None, pp: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: eedi2cuda

class _Plugin_eedi2cuda_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AA2(self, clip: "VideoNode", mthresh: typing.Optional[int] = None, lthresh: typing.Optional[int] = None, vthresh: typing.Optional[int] = None, estr: typing.Optional[int] = None, dstr: typing.Optional[int] = None, maxd: typing.Optional[int] = None, map: typing.Optional[int] = None, nt: typing.Optional[int] = None, pp: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, device_id: typing.Optional[int] = None) -> "VideoNode": ...
    def BuildConfig(self) -> "VideoNode": ...
    def EEDI2(self, clip: "VideoNode", field: int, mthresh: typing.Optional[int] = None, lthresh: typing.Optional[int] = None, vthresh: typing.Optional[int] = None, estr: typing.Optional[int] = None, dstr: typing.Optional[int] = None, maxd: typing.Optional[int] = None, map: typing.Optional[int] = None, nt: typing.Optional[int] = None, pp: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, device_id: typing.Optional[int] = None) -> "VideoNode": ...
    def Enlarge2(self, clip: "VideoNode", mthresh: typing.Optional[int] = None, lthresh: typing.Optional[int] = None, vthresh: typing.Optional[int] = None, estr: typing.Optional[int] = None, dstr: typing.Optional[int] = None, maxd: typing.Optional[int] = None, map: typing.Optional[int] = None, nt: typing.Optional[int] = None, pp: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, device_id: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_eedi2cuda_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AA2(self, mthresh: typing.Optional[int] = None, lthresh: typing.Optional[int] = None, vthresh: typing.Optional[int] = None, estr: typing.Optional[int] = None, dstr: typing.Optional[int] = None, maxd: typing.Optional[int] = None, map: typing.Optional[int] = None, nt: typing.Optional[int] = None, pp: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, device_id: typing.Optional[int] = None) -> "VideoNode": ...
    def EEDI2(self, field: int, mthresh: typing.Optional[int] = None, lthresh: typing.Optional[int] = None, vthresh: typing.Optional[int] = None, estr: typing.Optional[int] = None, dstr: typing.Optional[int] = None, maxd: typing.Optional[int] = None, map: typing.Optional[int] = None, nt: typing.Optional[int] = None, pp: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, device_id: typing.Optional[int] = None) -> "VideoNode": ...
    def Enlarge2(self, mthresh: typing.Optional[int] = None, lthresh: typing.Optional[int] = None, vthresh: typing.Optional[int] = None, estr: typing.Optional[int] = None, dstr: typing.Optional[int] = None, maxd: typing.Optional[int] = None, map: typing.Optional[int] = None, nt: typing.Optional[int] = None, pp: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, device_id: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: eedi3m

class _Plugin_eedi3m_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI3(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, alpha: typing.Optional[float] = None, beta: typing.Optional[float] = None, gamma: typing.Optional[float] = None, nrad: typing.Optional[int] = None, mdis: typing.Optional[int] = None, hp: typing.Optional[int] = None, ucubic: typing.Optional[int] = None, cost3: typing.Optional[int] = None, vcheck: typing.Optional[int] = None, vthresh0: typing.Optional[float] = None, vthresh1: typing.Optional[float] = None, vthresh2: typing.Optional[float] = None, sclip: typing.Optional["VideoNode"] = None, mclip: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def EEDI3CL(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, alpha: typing.Optional[float] = None, beta: typing.Optional[float] = None, gamma: typing.Optional[float] = None, nrad: typing.Optional[int] = None, mdis: typing.Optional[int] = None, hp: typing.Optional[int] = None, ucubic: typing.Optional[int] = None, cost3: typing.Optional[int] = None, vcheck: typing.Optional[int] = None, vthresh0: typing.Optional[float] = None, vthresh1: typing.Optional[float] = None, vthresh2: typing.Optional[float] = None, sclip: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None, device: typing.Optional[int] = None, list_device: typing.Optional[int] = None, info: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_eedi3m_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI3(self, field: int, dh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, alpha: typing.Optional[float] = None, beta: typing.Optional[float] = None, gamma: typing.Optional[float] = None, nrad: typing.Optional[int] = None, mdis: typing.Optional[int] = None, hp: typing.Optional[int] = None, ucubic: typing.Optional[int] = None, cost3: typing.Optional[int] = None, vcheck: typing.Optional[int] = None, vthresh0: typing.Optional[float] = None, vthresh1: typing.Optional[float] = None, vthresh2: typing.Optional[float] = None, sclip: typing.Optional["VideoNode"] = None, mclip: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def EEDI3CL(self, field: int, dh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, alpha: typing.Optional[float] = None, beta: typing.Optional[float] = None, gamma: typing.Optional[float] = None, nrad: typing.Optional[int] = None, mdis: typing.Optional[int] = None, hp: typing.Optional[int] = None, ucubic: typing.Optional[int] = None, cost3: typing.Optional[int] = None, vcheck: typing.Optional[int] = None, vthresh0: typing.Optional[float] = None, vthresh1: typing.Optional[float] = None, vthresh2: typing.Optional[float] = None, sclip: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None, device: typing.Optional[int] = None, list_device: typing.Optional[int] = None, info: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: f3kdb

class _Plugin_f3kdb_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, clip: "VideoNode", range: typing.Optional[int] = None, y: typing.Optional[int] = None, cb: typing.Optional[int] = None, cr: typing.Optional[int] = None, grainy: typing.Optional[int] = None, grainc: typing.Optional[int] = None, sample_mode: typing.Optional[int] = None, seed: typing.Optional[int] = None, blur_first: typing.Optional[int] = None, dynamic_grain: typing.Optional[int] = None, opt: typing.Optional[int] = None, dither_algo: typing.Optional[int] = None, keep_tv_range: typing.Optional[int] = None, output_depth: typing.Optional[int] = None, random_algo_ref: typing.Optional[int] = None, random_algo_grain: typing.Optional[int] = None, random_param_ref: typing.Optional[float] = None, random_param_grain: typing.Optional[float] = None, preset: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_f3kdb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, range: typing.Optional[int] = None, y: typing.Optional[int] = None, cb: typing.Optional[int] = None, cr: typing.Optional[int] = None, grainy: typing.Optional[int] = None, grainc: typing.Optional[int] = None, sample_mode: typing.Optional[int] = None, seed: typing.Optional[int] = None, blur_first: typing.Optional[int] = None, dynamic_grain: typing.Optional[int] = None, opt: typing.Optional[int] = None, dither_algo: typing.Optional[int] = None, keep_tv_range: typing.Optional[int] = None, output_depth: typing.Optional[int] = None, random_algo_ref: typing.Optional[int] = None, random_algo_grain: typing.Optional[int] = None, random_param_ref: typing.Optional[float] = None, random_param_grain: typing.Optional[float] = None, preset: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: fb

class _Plugin_fb_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FillBorders(self, clip: "VideoNode", left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, mode: typing.Union[str, bytes, bytearray, None] = None, interlaced: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_fb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FillBorders(self, left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, mode: typing.Union[str, bytes, bytearray, None] = None, interlaced: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: ffms2

class _Plugin_ffms2_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def GetLogLevel(self) -> "VideoNode": ...
    def Index(self, source: typing.Union[str, bytes, bytearray], cachefile: typing.Union[str, bytes, bytearray, None] = None, indextracks: typing.Union[int, typing.Sequence[int], None] = None, errorhandling: typing.Optional[int] = None, overwrite: typing.Optional[int] = None) -> "VideoNode": ...
    def SetLogLevel(self, level: int) -> "VideoNode": ...
    def Source(self, source: typing.Union[str, bytes, bytearray], track: typing.Optional[int] = None, cache: typing.Optional[int] = None, cachefile: typing.Union[str, bytes, bytearray, None] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, threads: typing.Optional[int] = None, timecodes: typing.Union[str, bytes, bytearray, None] = None, seekmode: typing.Optional[int] = None, width: typing.Optional[int] = None, height: typing.Optional[int] = None, resizer: typing.Union[str, bytes, bytearray, None] = None, format: typing.Optional[int] = None, alpha: typing.Optional[int] = None) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...

# end implementation


# implementation: fft3dfilter

class _Plugin_fft3dfilter_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFT3DFilter(self, clip: "VideoNode", sigma: typing.Optional[float] = None, beta: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, bw: typing.Optional[int] = None, bh: typing.Optional[int] = None, bt: typing.Optional[int] = None, ow: typing.Optional[int] = None, oh: typing.Optional[int] = None, kratio: typing.Optional[float] = None, sharpen: typing.Optional[float] = None, scutoff: typing.Optional[float] = None, svr: typing.Optional[float] = None, smin: typing.Optional[float] = None, smax: typing.Optional[float] = None, measure: typing.Optional[int] = None, interlaced: typing.Optional[int] = None, wintype: typing.Optional[int] = None, pframe: typing.Optional[int] = None, px: typing.Optional[int] = None, py: typing.Optional[int] = None, pshow: typing.Optional[int] = None, pcutoff: typing.Optional[float] = None, pfactor: typing.Optional[float] = None, sigma2: typing.Optional[float] = None, sigma3: typing.Optional[float] = None, sigma4: typing.Optional[float] = None, degrid: typing.Optional[float] = None, dehalo: typing.Optional[float] = None, hr: typing.Optional[float] = None, ht: typing.Optional[float] = None, ncpu: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_fft3dfilter_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFT3DFilter(self, sigma: typing.Optional[float] = None, beta: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, bw: typing.Optional[int] = None, bh: typing.Optional[int] = None, bt: typing.Optional[int] = None, ow: typing.Optional[int] = None, oh: typing.Optional[int] = None, kratio: typing.Optional[float] = None, sharpen: typing.Optional[float] = None, scutoff: typing.Optional[float] = None, svr: typing.Optional[float] = None, smin: typing.Optional[float] = None, smax: typing.Optional[float] = None, measure: typing.Optional[int] = None, interlaced: typing.Optional[int] = None, wintype: typing.Optional[int] = None, pframe: typing.Optional[int] = None, px: typing.Optional[int] = None, py: typing.Optional[int] = None, pshow: typing.Optional[int] = None, pcutoff: typing.Optional[float] = None, pfactor: typing.Optional[float] = None, sigma2: typing.Optional[float] = None, sigma3: typing.Optional[float] = None, sigma4: typing.Optional[float] = None, degrid: typing.Optional[float] = None, dehalo: typing.Optional[float] = None, hr: typing.Optional[float] = None, ht: typing.Optional[float] = None, ncpu: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: fftspectrum

class _Plugin_fftspectrum_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFTSpectrum(self, clip: "VideoNode", grid: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_fftspectrum_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFTSpectrum(self, grid: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: fh

class _Plugin_fh_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FieldHint(self, clip: "VideoNode", ovr: typing.Union[str, bytes, bytearray, None] = None, tff: typing.Optional[int] = None, matches: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Fieldhint(self, clip: "VideoNode", ovr: typing.Union[str, bytes, bytearray, None] = None, tff: typing.Optional[int] = None, matches: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_fh_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FieldHint(self, ovr: typing.Union[str, bytes, bytearray, None] = None, tff: typing.Optional[int] = None, matches: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Fieldhint(self, ovr: typing.Union[str, bytes, bytearray, None] = None, tff: typing.Optional[int] = None, matches: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: flux

class _Plugin_flux_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothST(self, clip: "VideoNode", temporal_threshold: typing.Optional[int] = None, spatial_threshold: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def SmoothT(self, clip: "VideoNode", temporal_threshold: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_flux_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothST(self, temporal_threshold: typing.Optional[int] = None, spatial_threshold: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def SmoothT(self, temporal_threshold: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: fmtc

class _Plugin_fmtc_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def bitdepth(self, clip: "VideoNode", csp: typing.Optional[int] = None, bits: typing.Optional[int] = None, flt: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, dmode: typing.Optional[int] = None, ampo: typing.Optional[float] = None, ampn: typing.Optional[float] = None, dyn: typing.Optional[int] = None, staticnoise: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None, patsize: typing.Optional[int] = None, tpdfo: typing.Optional[int] = None, tpdfn: typing.Optional[int] = None, corplane: typing.Optional[int] = None) -> "VideoNode": ...
    def histluma(self, clip: "VideoNode", full: typing.Optional[int] = None, amp: typing.Optional[int] = None) -> "VideoNode": ...
    def matrix(self, clip: "VideoNode", mat: typing.Union[str, bytes, bytearray, None] = None, mats: typing.Union[str, bytes, bytearray, None] = None, matd: typing.Union[str, bytes, bytearray, None] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, coef: typing.Union[float, typing.Sequence[float], None] = None, csp: typing.Optional[int] = None, col_fam: typing.Optional[int] = None, bits: typing.Optional[int] = None, singleout: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None, planes: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def matrix2020cl(self, clip: "VideoNode", full: typing.Optional[int] = None, csp: typing.Optional[int] = None, bits: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None) -> "VideoNode": ...
    def nativetostack16(self, clip: "VideoNode") -> "VideoNode": ...
    def primaries(self, clip: "VideoNode", rs: typing.Union[float, typing.Sequence[float], None] = None, gs: typing.Union[float, typing.Sequence[float], None] = None, bs: typing.Union[float, typing.Sequence[float], None] = None, ws: typing.Union[float, typing.Sequence[float], None] = None, rd: typing.Union[float, typing.Sequence[float], None] = None, gd: typing.Union[float, typing.Sequence[float], None] = None, bd: typing.Union[float, typing.Sequence[float], None] = None, wd: typing.Union[float, typing.Sequence[float], None] = None, prims: typing.Union[str, bytes, bytearray, None] = None, primd: typing.Union[str, bytes, bytearray, None] = None, cpuopt: typing.Optional[int] = None) -> "VideoNode": ...
    def resample(self, clip: "VideoNode", w: typing.Optional[int] = None, h: typing.Optional[int] = None, sx: typing.Union[float, typing.Sequence[float], None] = None, sy: typing.Union[float, typing.Sequence[float], None] = None, sw: typing.Union[float, typing.Sequence[float], None] = None, sh: typing.Union[float, typing.Sequence[float], None] = None, scale: typing.Optional[float] = None, scaleh: typing.Optional[float] = None, scalev: typing.Optional[float] = None, kernel: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, kernelh: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, kernelv: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, impulse: typing.Union[float, typing.Sequence[float], None] = None, impulseh: typing.Union[float, typing.Sequence[float], None] = None, impulsev: typing.Union[float, typing.Sequence[float], None] = None, taps: typing.Union[int, typing.Sequence[int], None] = None, tapsh: typing.Union[int, typing.Sequence[int], None] = None, tapsv: typing.Union[int, typing.Sequence[int], None] = None, a1: typing.Union[float, typing.Sequence[float], None] = None, a2: typing.Union[float, typing.Sequence[float], None] = None, a3: typing.Union[float, typing.Sequence[float], None] = None, a1h: typing.Union[float, typing.Sequence[float], None] = None, a2h: typing.Union[float, typing.Sequence[float], None] = None, a3h: typing.Union[float, typing.Sequence[float], None] = None, a1v: typing.Union[float, typing.Sequence[float], None] = None, a2v: typing.Union[float, typing.Sequence[float], None] = None, a3v: typing.Union[float, typing.Sequence[float], None] = None, kovrspl: typing.Union[int, typing.Sequence[int], None] = None, fh: typing.Union[float, typing.Sequence[float], None] = None, fv: typing.Union[float, typing.Sequence[float], None] = None, cnorm: typing.Union[int, typing.Sequence[int], None] = None, total: typing.Union[float, typing.Sequence[float], None] = None, totalh: typing.Union[float, typing.Sequence[float], None] = None, totalv: typing.Union[float, typing.Sequence[float], None] = None, invks: typing.Union[int, typing.Sequence[int], None] = None, invksh: typing.Union[int, typing.Sequence[int], None] = None, invksv: typing.Union[int, typing.Sequence[int], None] = None, invkstaps: typing.Union[int, typing.Sequence[int], None] = None, invkstapsh: typing.Union[int, typing.Sequence[int], None] = None, invkstapsv: typing.Union[int, typing.Sequence[int], None] = None, csp: typing.Optional[int] = None, css: typing.Union[str, bytes, bytearray, None] = None, planes: typing.Union[float, typing.Sequence[float], None] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, center: typing.Union[int, typing.Sequence[int], None] = None, cplace: typing.Union[str, bytes, bytearray, None] = None, cplaces: typing.Union[str, bytes, bytearray, None] = None, cplaced: typing.Union[str, bytes, bytearray, None] = None, interlaced: typing.Optional[int] = None, interlacedd: typing.Optional[int] = None, tff: typing.Optional[int] = None, tffd: typing.Optional[int] = None, flt: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None) -> "VideoNode": ...
    def stack16tonative(self, clip: "VideoNode") -> "VideoNode": ...
    def transfer(self, clip: "VideoNode", transs: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, transd: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, cont: typing.Optional[float] = None, gcor: typing.Optional[float] = None, bits: typing.Optional[int] = None, flt: typing.Optional[int] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, logceis: typing.Optional[int] = None, logceid: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None, blacklvl: typing.Optional[float] = None, sceneref: typing.Optional[int] = None, lb: typing.Optional[float] = None, lw: typing.Optional[float] = None, lws: typing.Optional[float] = None, lwd: typing.Optional[float] = None, ambient: typing.Optional[float] = None, match: typing.Optional[int] = None, gy: typing.Optional[int] = None, debug: typing.Optional[int] = None, sig_c: typing.Optional[float] = None, sig_t: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_fmtc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def bitdepth(self, csp: typing.Optional[int] = None, bits: typing.Optional[int] = None, flt: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, dmode: typing.Optional[int] = None, ampo: typing.Optional[float] = None, ampn: typing.Optional[float] = None, dyn: typing.Optional[int] = None, staticnoise: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None, patsize: typing.Optional[int] = None, tpdfo: typing.Optional[int] = None, tpdfn: typing.Optional[int] = None, corplane: typing.Optional[int] = None) -> "VideoNode": ...
    def histluma(self, full: typing.Optional[int] = None, amp: typing.Optional[int] = None) -> "VideoNode": ...
    def matrix(self, mat: typing.Union[str, bytes, bytearray, None] = None, mats: typing.Union[str, bytes, bytearray, None] = None, matd: typing.Union[str, bytes, bytearray, None] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, coef: typing.Union[float, typing.Sequence[float], None] = None, csp: typing.Optional[int] = None, col_fam: typing.Optional[int] = None, bits: typing.Optional[int] = None, singleout: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None, planes: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def matrix2020cl(self, full: typing.Optional[int] = None, csp: typing.Optional[int] = None, bits: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None) -> "VideoNode": ...
    def nativetostack16(self) -> "VideoNode": ...
    def primaries(self, rs: typing.Union[float, typing.Sequence[float], None] = None, gs: typing.Union[float, typing.Sequence[float], None] = None, bs: typing.Union[float, typing.Sequence[float], None] = None, ws: typing.Union[float, typing.Sequence[float], None] = None, rd: typing.Union[float, typing.Sequence[float], None] = None, gd: typing.Union[float, typing.Sequence[float], None] = None, bd: typing.Union[float, typing.Sequence[float], None] = None, wd: typing.Union[float, typing.Sequence[float], None] = None, prims: typing.Union[str, bytes, bytearray, None] = None, primd: typing.Union[str, bytes, bytearray, None] = None, cpuopt: typing.Optional[int] = None) -> "VideoNode": ...
    def resample(self, w: typing.Optional[int] = None, h: typing.Optional[int] = None, sx: typing.Union[float, typing.Sequence[float], None] = None, sy: typing.Union[float, typing.Sequence[float], None] = None, sw: typing.Union[float, typing.Sequence[float], None] = None, sh: typing.Union[float, typing.Sequence[float], None] = None, scale: typing.Optional[float] = None, scaleh: typing.Optional[float] = None, scalev: typing.Optional[float] = None, kernel: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, kernelh: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, kernelv: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, impulse: typing.Union[float, typing.Sequence[float], None] = None, impulseh: typing.Union[float, typing.Sequence[float], None] = None, impulsev: typing.Union[float, typing.Sequence[float], None] = None, taps: typing.Union[int, typing.Sequence[int], None] = None, tapsh: typing.Union[int, typing.Sequence[int], None] = None, tapsv: typing.Union[int, typing.Sequence[int], None] = None, a1: typing.Union[float, typing.Sequence[float], None] = None, a2: typing.Union[float, typing.Sequence[float], None] = None, a3: typing.Union[float, typing.Sequence[float], None] = None, a1h: typing.Union[float, typing.Sequence[float], None] = None, a2h: typing.Union[float, typing.Sequence[float], None] = None, a3h: typing.Union[float, typing.Sequence[float], None] = None, a1v: typing.Union[float, typing.Sequence[float], None] = None, a2v: typing.Union[float, typing.Sequence[float], None] = None, a3v: typing.Union[float, typing.Sequence[float], None] = None, kovrspl: typing.Union[int, typing.Sequence[int], None] = None, fh: typing.Union[float, typing.Sequence[float], None] = None, fv: typing.Union[float, typing.Sequence[float], None] = None, cnorm: typing.Union[int, typing.Sequence[int], None] = None, total: typing.Union[float, typing.Sequence[float], None] = None, totalh: typing.Union[float, typing.Sequence[float], None] = None, totalv: typing.Union[float, typing.Sequence[float], None] = None, invks: typing.Union[int, typing.Sequence[int], None] = None, invksh: typing.Union[int, typing.Sequence[int], None] = None, invksv: typing.Union[int, typing.Sequence[int], None] = None, invkstaps: typing.Union[int, typing.Sequence[int], None] = None, invkstapsh: typing.Union[int, typing.Sequence[int], None] = None, invkstapsv: typing.Union[int, typing.Sequence[int], None] = None, csp: typing.Optional[int] = None, css: typing.Union[str, bytes, bytearray, None] = None, planes: typing.Union[float, typing.Sequence[float], None] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, center: typing.Union[int, typing.Sequence[int], None] = None, cplace: typing.Union[str, bytes, bytearray, None] = None, cplaces: typing.Union[str, bytes, bytearray, None] = None, cplaced: typing.Union[str, bytes, bytearray, None] = None, interlaced: typing.Optional[int] = None, interlacedd: typing.Optional[int] = None, tff: typing.Optional[int] = None, tffd: typing.Optional[int] = None, flt: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None) -> "VideoNode": ...
    def stack16tonative(self) -> "VideoNode": ...
    def transfer(self, transs: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, transd: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, cont: typing.Optional[float] = None, gcor: typing.Optional[float] = None, bits: typing.Optional[int] = None, flt: typing.Optional[int] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, logceis: typing.Optional[int] = None, logceid: typing.Optional[int] = None, cpuopt: typing.Optional[int] = None, blacklvl: typing.Optional[float] = None, sceneref: typing.Optional[int] = None, lb: typing.Optional[float] = None, lw: typing.Optional[float] = None, lws: typing.Optional[float] = None, lwd: typing.Optional[float] = None, ambient: typing.Optional[float] = None, match: typing.Optional[int] = None, gy: typing.Optional[int] = None, debug: typing.Optional[int] = None, sig_c: typing.Optional[float] = None, sig_t: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: focus

class _Plugin_focus_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SpatialSoften(self, clip: "VideoNode", radius: typing.Optional[int] = None, luma_threshold: typing.Optional[float] = None, chroma_threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def TemporalSoften(self, clip: "VideoNode", radius: typing.Optional[int] = None, luma_threshold: typing.Optional[float] = None, chroma_threshold: typing.Optional[float] = None, scenechange: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_focus_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SpatialSoften(self, radius: typing.Optional[int] = None, luma_threshold: typing.Optional[float] = None, chroma_threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def TemporalSoften(self, radius: typing.Optional[int] = None, luma_threshold: typing.Optional[float] = None, chroma_threshold: typing.Optional[float] = None, scenechange: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: focus2

class _Plugin_focus2_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalSoften2(self, clip: "VideoNode", radius: typing.Optional[int] = None, luma_threshold: typing.Optional[int] = None, chroma_threshold: typing.Optional[int] = None, scenechange: typing.Optional[int] = None, mode: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_focus2_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalSoften2(self, radius: typing.Optional[int] = None, luma_threshold: typing.Optional[int] = None, chroma_threshold: typing.Optional[int] = None, scenechange: typing.Optional[int] = None, mode: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: ftf

class _Plugin_ftf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FixFades(self, clip: "VideoNode", mode: typing.Optional[int] = None, threshold: typing.Optional[float] = None, color: typing.Union[float, typing.Sequence[float], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_ftf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FixFades(self, mode: typing.Optional[int] = None, threshold: typing.Optional[float] = None, color: typing.Union[float, typing.Sequence[float], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: grad

class _Plugin_grad_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Curve(self, clip: "VideoNode", fname: typing.Union[str, bytes, bytearray, None] = None, ftype: typing.Optional[int] = None, pmode: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_grad_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Curve(self, fname: typing.Union[str, bytes, bytearray, None] = None, ftype: typing.Optional[int] = None, pmode: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: grain

class _Plugin_grain_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Add(self, clip: "VideoNode", var: typing.Optional[float] = None, uvar: typing.Optional[float] = None, hcorr: typing.Optional[float] = None, vcorr: typing.Optional[float] = None, seed: typing.Optional[int] = None, constant: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_grain_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Add(self, var: typing.Optional[float] = None, uvar: typing.Optional[float] = None, hcorr: typing.Optional[float] = None, vcorr: typing.Optional[float] = None, seed: typing.Optional[int] = None, constant: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: hist

class _Plugin_hist_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Classic(self, clip: "VideoNode") -> "VideoNode": ...
    def Color(self, clip: "VideoNode") -> "VideoNode": ...
    def Color2(self, clip: "VideoNode") -> "VideoNode": ...
    def Levels(self, clip: "VideoNode", factor: typing.Optional[float] = None) -> "VideoNode": ...
    def Luma(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_hist_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Classic(self) -> "VideoNode": ...
    def Color(self) -> "VideoNode": ...
    def Color2(self) -> "VideoNode": ...
    def Levels(self, factor: typing.Optional[float] = None) -> "VideoNode": ...
    def Luma(self) -> "VideoNode": ...

# end implementation


# implementation: hqdn3d

class _Plugin_hqdn3d_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Hqdn3d(self, clip: "VideoNode", lum_spac: typing.Optional[float] = None, chrom_spac: typing.Optional[float] = None, lum_tmp: typing.Optional[float] = None, chrom_tmp: typing.Optional[float] = None, restart_lap: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_hqdn3d_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Hqdn3d(self, lum_spac: typing.Optional[float] = None, chrom_spac: typing.Optional[float] = None, lum_tmp: typing.Optional[float] = None, chrom_tmp: typing.Optional[float] = None, restart_lap: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: iccc

class _Plugin_iccc_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ICCConvert(self, clip: "VideoNode", simulation_icc: typing.Union[str, bytes, bytearray], display_icc: typing.Union[str, bytes, bytearray, None] = None, soft_proofing: typing.Optional[int] = None, simulation_intent: typing.Union[str, bytes, bytearray, None] = None, display_intent: typing.Union[str, bytes, bytearray, None] = None, gamut_warning: typing.Optional[int] = None, black_point_compensation: typing.Optional[int] = None, clut_size: typing.Optional[int] = None) -> "VideoNode": ...
    def ICCPlayback(self, clip: "VideoNode", display_icc: typing.Union[str, bytes, bytearray, None] = None, playback_csp: typing.Union[str, bytes, bytearray, None] = None, gamma: typing.Optional[float] = None, intent: typing.Union[str, bytes, bytearray, None] = None, clut_size: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_iccc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ICCConvert(self, simulation_icc: typing.Union[str, bytes, bytearray], display_icc: typing.Union[str, bytes, bytearray, None] = None, soft_proofing: typing.Optional[int] = None, simulation_intent: typing.Union[str, bytes, bytearray, None] = None, display_intent: typing.Union[str, bytes, bytearray, None] = None, gamut_warning: typing.Optional[int] = None, black_point_compensation: typing.Optional[int] = None, clut_size: typing.Optional[int] = None) -> "VideoNode": ...
    def ICCPlayback(self, display_icc: typing.Union[str, bytes, bytearray, None] = None, playback_csp: typing.Union[str, bytes, bytearray, None] = None, gamma: typing.Optional[float] = None, intent: typing.Union[str, bytes, bytearray, None] = None, clut_size: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: imwri

class _Plugin_imwri_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, filename: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], firstnum: typing.Optional[int] = None, mismatch: typing.Optional[int] = None, alpha: typing.Optional[int] = None, float_output: typing.Optional[int] = None, embed_icc: typing.Optional[int] = None) -> "VideoNode": ...
    def Write(self, clip: "VideoNode", imgformat: typing.Union[str, bytes, bytearray], filename: typing.Union[str, bytes, bytearray], firstnum: typing.Optional[int] = None, quality: typing.Optional[int] = None, dither: typing.Optional[int] = None, compression_type: typing.Union[str, bytes, bytearray, None] = None, overwrite: typing.Optional[int] = None, alpha: typing.Optional["VideoNode"] = None) -> "VideoNode": ...


class _Plugin_imwri_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Write(self, imgformat: typing.Union[str, bytes, bytearray], filename: typing.Union[str, bytes, bytearray], firstnum: typing.Optional[int] = None, quality: typing.Optional[int] = None, dither: typing.Optional[int] = None, compression_type: typing.Union[str, bytes, bytearray, None] = None, overwrite: typing.Optional[int] = None, alpha: typing.Optional["VideoNode"] = None) -> "VideoNode": ...

# end implementation


# implementation: it

class _Plugin_it_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def IT(self, clip: "VideoNode", fps: typing.Optional[int] = None, threshold: typing.Optional[int] = None, pthreshold: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_it_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def IT(self, fps: typing.Optional[int] = None, threshold: typing.Optional[int] = None, pthreshold: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: jinc

class _Plugin_jinc_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def JincResize(self, clip: "VideoNode", width: int, height: int, tap: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, quant_x: typing.Optional[int] = None, quant_y: typing.Optional[int] = None, blur: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_jinc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def JincResize(self, width: int, height: int, tap: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, quant_x: typing.Optional[int] = None, quant_y: typing.Optional[int] = None, blur: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: knlm

class _Plugin_knlm_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def KNLMeansCL(self, clip: "VideoNode", d: typing.Optional[int] = None, a: typing.Optional[int] = None, s: typing.Optional[int] = None, h: typing.Optional[float] = None, channels: typing.Union[str, bytes, bytearray, None] = None, wmode: typing.Optional[int] = None, wref: typing.Optional[float] = None, rclip: typing.Optional["VideoNode"] = None, device_type: typing.Union[str, bytes, bytearray, None] = None, device_id: typing.Optional[int] = None, ocl_x: typing.Optional[int] = None, ocl_y: typing.Optional[int] = None, ocl_r: typing.Optional[int] = None, info: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_knlm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def KNLMeansCL(self, d: typing.Optional[int] = None, a: typing.Optional[int] = None, s: typing.Optional[int] = None, h: typing.Optional[float] = None, channels: typing.Union[str, bytes, bytearray, None] = None, wmode: typing.Optional[int] = None, wref: typing.Optional[float] = None, rclip: typing.Optional["VideoNode"] = None, device_type: typing.Union[str, bytes, bytearray, None] = None, device_id: typing.Optional[int] = None, ocl_x: typing.Optional[int] = None, ocl_y: typing.Optional[int] = None, ocl_r: typing.Optional[int] = None, info: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: lghost

class _Plugin_lghost_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LGhost(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]], shift: typing.Union[int, typing.Sequence[int]], intensity: typing.Union[int, typing.Sequence[int]], planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_lghost_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LGhost(self, mode: typing.Union[int, typing.Sequence[int]], shift: typing.Union[int, typing.Sequence[int]], intensity: typing.Union[int, typing.Sequence[int]], planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: libp2p

class _Plugin_libp2p_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Pack(self, clip: "VideoNode") -> "VideoNode": ...
    def Unpack(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_libp2p_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Pack(self) -> "VideoNode": ...
    def Unpack(self) -> "VideoNode": ...

# end implementation


# implementation: lsmas

class _Plugin_lsmas_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LWLibavSource(self, source: typing.Union[str, bytes, bytearray], stream_index: typing.Optional[int] = None, cache: typing.Optional[int] = None, cachefile: typing.Union[str, bytes, bytearray, None] = None, threads: typing.Optional[int] = None, seek_mode: typing.Optional[int] = None, seek_threshold: typing.Optional[int] = None, dr: typing.Optional[int] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, variable: typing.Optional[int] = None, format: typing.Union[str, bytes, bytearray, None] = None, decoder: typing.Union[str, bytes, bytearray, None] = None, prefer_hw: typing.Optional[int] = None, repeat: typing.Optional[int] = None, dominance: typing.Optional[int] = None, ff_loglevel: typing.Optional[int] = None, cachedir: typing.Union[str, bytes, bytearray, None] = None, soft_reset: typing.Optional[int] = None) -> "VideoNode": ...
    def LibavSMASHSource(self, source: typing.Union[str, bytes, bytearray], track: typing.Optional[int] = None, threads: typing.Optional[int] = None, seek_mode: typing.Optional[int] = None, seek_threshold: typing.Optional[int] = None, dr: typing.Optional[int] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, variable: typing.Optional[int] = None, format: typing.Union[str, bytes, bytearray, None] = None, decoder: typing.Union[str, bytes, bytearray, None] = None, prefer_hw: typing.Optional[int] = None, ff_loglevel: typing.Optional[int] = None) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...

# end implementation


# implementation: matchhist

class _Plugin_matchhist_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MatchHistogram(self, clip1: "VideoNode", clip2: "VideoNode", clip3: typing.Optional["VideoNode"] = None, raw: typing.Optional[int] = None, show: typing.Optional[int] = None, debug: typing.Optional[int] = None, smoothing_window: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_matchhist_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MatchHistogram(self, clip2: "VideoNode", clip3: typing.Optional["VideoNode"] = None, raw: typing.Optional[int] = None, show: typing.Optional[int] = None, debug: typing.Optional[int] = None, smoothing_window: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: median

class _Plugin_median_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Median(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], sync: typing.Optional[int] = None, samples: typing.Optional[int] = None, debug: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MedianBlend(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], low: typing.Optional[int] = None, high: typing.Optional[int] = None, closest: typing.Optional[int] = None, sync: typing.Optional[int] = None, samples: typing.Optional[int] = None, debug: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def TemporalMedian(self, clip: "VideoNode", radius: typing.Optional[int] = None, debug: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_median_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Median(self, sync: typing.Optional[int] = None, samples: typing.Optional[int] = None, debug: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MedianBlend(self, low: typing.Optional[int] = None, high: typing.Optional[int] = None, closest: typing.Optional[int] = None, sync: typing.Optional[int] = None, samples: typing.Optional[int] = None, debug: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def TemporalMedian(self, radius: typing.Optional[int] = None, debug: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: minideen

class _Plugin_minideen_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MiniDeen(self, clip: "VideoNode", radius: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Union[int, typing.Sequence[int], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_minideen_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MiniDeen(self, radius: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Union[int, typing.Sequence[int], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: minsrp

class _Plugin_minsrp_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Sharp(self, clip: "VideoNode", str: typing.Union[float, typing.Sequence[float], None] = None, mode: typing.Union[int, typing.Sequence[int], None] = None, linear: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_minsrp_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Sharp(self, str: typing.Union[float, typing.Sequence[float], None] = None, mode: typing.Union[int, typing.Sequence[int], None] = None, linear: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: misc

class _Plugin_misc_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AverageFrames(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], weights: typing.Union[float, typing.Sequence[float]], scale: typing.Optional[float] = None, scenechange: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Hysteresis(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def SCDetect(self, clip: "VideoNode", threshold: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_misc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AverageFrames(self, weights: typing.Union[float, typing.Sequence[float]], scale: typing.Optional[float] = None, scenechange: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Hysteresis(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def SCDetect(self, threshold: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: morpho

class _Plugin_morpho_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BottomHat(self, clip: "VideoNode", size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def Close(self, clip: "VideoNode", size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def Dilate(self, clip: "VideoNode", size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def Erode(self, clip: "VideoNode", size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def Open(self, clip: "VideoNode", size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def TopHat(self, clip: "VideoNode", size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_morpho_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BottomHat(self, size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def Close(self, size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def Dilate(self, size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def Erode(self, size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def Open(self, size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...
    def TopHat(self, size: typing.Optional[int] = None, shape: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: motionmask

class _Plugin_motionmask_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MotionMask(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, th1: typing.Union[int, typing.Sequence[int], None] = None, th2: typing.Union[int, typing.Sequence[int], None] = None, tht: typing.Optional[int] = None, sc_value: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_motionmask_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MotionMask(self, planes: typing.Union[int, typing.Sequence[int], None] = None, th1: typing.Union[int, typing.Sequence[int], None] = None, th2: typing.Union[int, typing.Sequence[int], None] = None, tht: typing.Optional[int] = None, sc_value: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: mpeg2stinx

class _Plugin_mpeg2stinx_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LutXYDiff(self, clip1: "VideoNode", clip2: "VideoNode") -> "VideoNode": ...
    def Max(self, clip1: "VideoNode", clip2: "VideoNode") -> "VideoNode": ...
    def Median3(self, clip1: "VideoNode", clip2: "VideoNode", clip3: "VideoNode", process_chroma: typing.Optional[int] = None) -> "VideoNode": ...
    def Min(self, clip1: "VideoNode", clip2: "VideoNode") -> "VideoNode": ...
    def Mpeg2Stinx(self, clip: "VideoNode", mode: typing.Optional[int] = None, sw: typing.Optional[int] = None, sh: typing.Optional[int] = None, contra: typing.Optional[int] = None, blurv: typing.Optional[float] = None, sstr: typing.Optional[float] = None, scl: typing.Optional[float] = None, dither: typing.Optional[int] = None, order: typing.Optional[int] = None, diffscl: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_mpeg2stinx_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LutXYDiff(self, clip2: "VideoNode") -> "VideoNode": ...
    def Max(self, clip2: "VideoNode") -> "VideoNode": ...
    def Median3(self, clip2: "VideoNode", clip3: "VideoNode", process_chroma: typing.Optional[int] = None) -> "VideoNode": ...
    def Min(self, clip2: "VideoNode") -> "VideoNode": ...
    def Mpeg2Stinx(self, mode: typing.Optional[int] = None, sw: typing.Optional[int] = None, sh: typing.Optional[int] = None, contra: typing.Optional[int] = None, blurv: typing.Optional[float] = None, sstr: typing.Optional[float] = None, scl: typing.Optional[float] = None, dither: typing.Optional[int] = None, order: typing.Optional[int] = None, diffscl: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: mpls

class _Plugin_mpls_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, bd_path: typing.Union[str, bytes, bytearray], playlist: int, angle: typing.Optional[int] = None) -> typing.Tuple[typing.Any, ...]: ...

# end implementation


# implementation: msmoosh

class _Plugin_msmoosh_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MSharpen(self, clip: "VideoNode", threshold: typing.Optional[float] = None, strength: typing.Optional[float] = None, mask: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MSmooth(self, clip: "VideoNode", threshold: typing.Optional[float] = None, strength: typing.Optional[int] = None, mask: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_msmoosh_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MSharpen(self, threshold: typing.Optional[float] = None, strength: typing.Optional[float] = None, mask: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MSmooth(self, threshold: typing.Optional[float] = None, strength: typing.Optional[int] = None, mask: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: mv

class _Plugin_mv_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, super: "VideoNode", blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, levels: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, pelsearch: typing.Optional[int] = None, isb: typing.Optional[int] = None, lambda_: typing.Optional[int] = None, chroma: typing.Optional[int] = None, delta: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, lsad: typing.Optional[int] = None, plevel: typing.Optional[int] = None, global_: typing.Optional[int] = None, pnew: typing.Optional[int] = None, pzero: typing.Optional[int] = None, pglobal: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, badsad: typing.Optional[int] = None, badrange: typing.Optional[int] = None, opt: typing.Optional[int] = None, meander: typing.Optional[int] = None, trymany: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, search_coarse: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def BlockFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mode: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Compensate(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = None, thsad: typing.Optional[int] = None, fields: typing.Optional[int] = None, time: typing.Optional[float] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain1(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain2(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain3(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanAnalyse(self, clip: "VideoNode", vectors: "VideoNode", mask: typing.Optional["VideoNode"] = None, zoom: typing.Optional[int] = None, rot: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, error: typing.Optional[float] = None, info: typing.Optional[int] = None, wrong: typing.Optional[float] = None, zerow: typing.Optional[float] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanCompensate(self, clip: "VideoNode", data: "VideoNode", offset: typing.Optional[float] = None, subpixel: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, matchfields: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, info: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanEstimate(self, clip: "VideoNode", trust: typing.Optional[float] = None, winx: typing.Optional[int] = None, winy: typing.Optional[int] = None, wleft: typing.Optional[int] = None, wtop: typing.Optional[int] = None, dxmax: typing.Optional[int] = None, dymax: typing.Optional[int] = None, zoommax: typing.Optional[float] = None, stab: typing.Optional[float] = None, pixaspect: typing.Optional[float] = None, info: typing.Optional[int] = None, show: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanStabilise(self, clip: "VideoNode", data: "VideoNode", cutoff: typing.Optional[float] = None, damping: typing.Optional[float] = None, initzoom: typing.Optional[float] = None, addzoom: typing.Optional[int] = None, prev: typing.Optional[int] = None, next: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, dxmax: typing.Optional[float] = None, dymax: typing.Optional[float] = None, zoommax: typing.Optional[float] = None, rotmax: typing.Optional[float] = None, subpixel: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, fitlast: typing.Optional[int] = None, tzoom: typing.Optional[float] = None, info: typing.Optional[int] = None, method: typing.Optional[int] = None, fields: typing.Optional[int] = None) -> "VideoNode": ...
    def Finest(self, super: "VideoNode", opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Flow(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = None, mode: typing.Optional[int] = None, fields: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowBlur(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = None, prec: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mask: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowInter(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Mask(self, clip: "VideoNode", vectors: "VideoNode", ml: typing.Optional[float] = None, gamma: typing.Optional[float] = None, kind: typing.Optional[int] = None, time: typing.Optional[float] = None, ysc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Recalculate(self, super: "VideoNode", vectors: "VideoNode", thsad: typing.Optional[int] = None, smooth: typing.Optional[int] = None, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, lambda_: typing.Optional[int] = None, chroma: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, pnew: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, opt: typing.Optional[int] = None, meander: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def SCDetection(self, clip: "VideoNode", vectors: "VideoNode", thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None) -> "VideoNode": ...
    def Super(self, clip: "VideoNode", hpad: typing.Optional[int] = None, vpad: typing.Optional[int] = None, pel: typing.Optional[int] = None, levels: typing.Optional[int] = None, chroma: typing.Optional[int] = None, sharp: typing.Optional[int] = None, rfilter: typing.Optional[int] = None, pelclip: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_mv_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, levels: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, pelsearch: typing.Optional[int] = None, isb: typing.Optional[int] = None, lambda_: typing.Optional[int] = None, chroma: typing.Optional[int] = None, delta: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, lsad: typing.Optional[int] = None, plevel: typing.Optional[int] = None, global_: typing.Optional[int] = None, pnew: typing.Optional[int] = None, pzero: typing.Optional[int] = None, pglobal: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, badsad: typing.Optional[int] = None, badrange: typing.Optional[int] = None, opt: typing.Optional[int] = None, meander: typing.Optional[int] = None, trymany: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, search_coarse: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def BlockFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mode: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Compensate(self, super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = None, thsad: typing.Optional[int] = None, fields: typing.Optional[int] = None, time: typing.Optional[float] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain1(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain2(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain3(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanAnalyse(self, vectors: "VideoNode", mask: typing.Optional["VideoNode"] = None, zoom: typing.Optional[int] = None, rot: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, error: typing.Optional[float] = None, info: typing.Optional[int] = None, wrong: typing.Optional[float] = None, zerow: typing.Optional[float] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanCompensate(self, data: "VideoNode", offset: typing.Optional[float] = None, subpixel: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, matchfields: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, info: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanEstimate(self, trust: typing.Optional[float] = None, winx: typing.Optional[int] = None, winy: typing.Optional[int] = None, wleft: typing.Optional[int] = None, wtop: typing.Optional[int] = None, dxmax: typing.Optional[int] = None, dymax: typing.Optional[int] = None, zoommax: typing.Optional[float] = None, stab: typing.Optional[float] = None, pixaspect: typing.Optional[float] = None, info: typing.Optional[int] = None, show: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanStabilise(self, data: "VideoNode", cutoff: typing.Optional[float] = None, damping: typing.Optional[float] = None, initzoom: typing.Optional[float] = None, addzoom: typing.Optional[int] = None, prev: typing.Optional[int] = None, next: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, dxmax: typing.Optional[float] = None, dymax: typing.Optional[float] = None, zoommax: typing.Optional[float] = None, rotmax: typing.Optional[float] = None, subpixel: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, fitlast: typing.Optional[int] = None, tzoom: typing.Optional[float] = None, info: typing.Optional[int] = None, method: typing.Optional[int] = None, fields: typing.Optional[int] = None) -> "VideoNode": ...
    def Finest(self, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Flow(self, super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = None, mode: typing.Optional[int] = None, fields: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowBlur(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = None, prec: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mask: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowInter(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Mask(self, vectors: "VideoNode", ml: typing.Optional[float] = None, gamma: typing.Optional[float] = None, kind: typing.Optional[int] = None, time: typing.Optional[float] = None, ysc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Recalculate(self, vectors: "VideoNode", thsad: typing.Optional[int] = None, smooth: typing.Optional[int] = None, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, lambda_: typing.Optional[int] = None, chroma: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, pnew: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, opt: typing.Optional[int] = None, meander: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def SCDetection(self, vectors: "VideoNode", thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None) -> "VideoNode": ...
    def Super(self, hpad: typing.Optional[int] = None, vpad: typing.Optional[int] = None, pel: typing.Optional[int] = None, levels: typing.Optional[int] = None, chroma: typing.Optional[int] = None, sharp: typing.Optional[int] = None, rfilter: typing.Optional[int] = None, pelclip: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: mvsf

class _Plugin_mvsf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, super: "VideoNode", blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, levels: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, pelsearch: typing.Optional[int] = None, isb: typing.Optional[int] = None, lambda_: typing.Optional[float] = None, chroma: typing.Optional[int] = None, delta: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, lsad: typing.Optional[float] = None, plevel: typing.Optional[int] = None, global_: typing.Optional[int] = None, pnew: typing.Optional[int] = None, pzero: typing.Optional[int] = None, pglobal: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, badsad: typing.Optional[float] = None, badrange: typing.Optional[int] = None, meander: typing.Optional[int] = None, trymany: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, search_coarse: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def Analyze(self, super: "VideoNode", blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, levels: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, pelsearch: typing.Optional[int] = None, isb: typing.Optional[int] = None, lambda_: typing.Optional[float] = None, chroma: typing.Optional[int] = None, delta: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, lsad: typing.Optional[float] = None, plevel: typing.Optional[int] = None, global_: typing.Optional[int] = None, pnew: typing.Optional[int] = None, pzero: typing.Optional[int] = None, pglobal: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, badsad: typing.Optional[float] = None, badrange: typing.Optional[int] = None, meander: typing.Optional[int] = None, trymany: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, search_coarse: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def BlockFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mode: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Compensate(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = None, thsad: typing.Optional[float] = None, fields: typing.Optional[int] = None, time: typing.Optional[float] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain1(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain10(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain11(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain12(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain13(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain14(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain15(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain16(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain17(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain18(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain19(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain2(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain20(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain21(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain22(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain23(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", mvbw23: "VideoNode", mvfw23: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain24(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", mvbw23: "VideoNode", mvfw23: "VideoNode", mvbw24: "VideoNode", mvfw24: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain3(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain4(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain5(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain6(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain7(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain8(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain9(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Finest(self, super: "VideoNode") -> "VideoNode": ...
    def Flow(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = None, mode: typing.Optional[int] = None, fields: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowBlur(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = None, prec: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def FlowFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mask: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def FlowInter(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Mask(self, clip: "VideoNode", vectors: "VideoNode", ml: typing.Optional[float] = None, gamma: typing.Optional[float] = None, kind: typing.Optional[int] = None, time: typing.Optional[float] = None, ysc: typing.Optional[float] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Recalculate(self, super: "VideoNode", vectors: "VideoNode", thsad: typing.Optional[float] = None, smooth: typing.Optional[int] = None, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, lambda_: typing.Optional[float] = None, chroma: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, pnew: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, meander: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def SCDetection(self, clip: "VideoNode", vectors: "VideoNode", thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Super(self, clip: "VideoNode", hpad: typing.Optional[int] = None, vpad: typing.Optional[int] = None, pel: typing.Optional[int] = None, levels: typing.Optional[int] = None, chroma: typing.Optional[int] = None, sharp: typing.Optional[int] = None, rfilter: typing.Optional[int] = None, pelclip: typing.Optional["VideoNode"] = None) -> "VideoNode": ...


class _Plugin_mvsf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, levels: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, pelsearch: typing.Optional[int] = None, isb: typing.Optional[int] = None, lambda_: typing.Optional[float] = None, chroma: typing.Optional[int] = None, delta: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, lsad: typing.Optional[float] = None, plevel: typing.Optional[int] = None, global_: typing.Optional[int] = None, pnew: typing.Optional[int] = None, pzero: typing.Optional[int] = None, pglobal: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, badsad: typing.Optional[float] = None, badrange: typing.Optional[int] = None, meander: typing.Optional[int] = None, trymany: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, search_coarse: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def Analyze(self, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, levels: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, pelsearch: typing.Optional[int] = None, isb: typing.Optional[int] = None, lambda_: typing.Optional[float] = None, chroma: typing.Optional[int] = None, delta: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, lsad: typing.Optional[float] = None, plevel: typing.Optional[int] = None, global_: typing.Optional[int] = None, pnew: typing.Optional[int] = None, pzero: typing.Optional[int] = None, pglobal: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, badsad: typing.Optional[float] = None, badrange: typing.Optional[int] = None, meander: typing.Optional[int] = None, trymany: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, search_coarse: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def BlockFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mode: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Compensate(self, super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = None, thsad: typing.Optional[float] = None, fields: typing.Optional[int] = None, time: typing.Optional[float] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain1(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain10(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain11(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain12(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain13(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain14(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain15(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain16(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain17(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain18(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain19(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain2(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain20(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain21(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain22(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain23(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", mvbw23: "VideoNode", mvfw23: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain24(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", mvbw23: "VideoNode", mvfw23: "VideoNode", mvbw24: "VideoNode", mvfw24: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain3(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain4(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain5(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain6(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain7(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain8(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Degrain9(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = None, plane: typing.Optional[int] = None, limit: typing.Union[float, typing.Sequence[float], None] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Finest(self) -> "VideoNode": ...
    def Flow(self, super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = None, mode: typing.Optional[int] = None, fields: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowBlur(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = None, prec: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def FlowFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mask: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def FlowInter(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Mask(self, vectors: "VideoNode", ml: typing.Optional[float] = None, gamma: typing.Optional[float] = None, kind: typing.Optional[int] = None, time: typing.Optional[float] = None, ysc: typing.Optional[float] = None, thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Recalculate(self, vectors: "VideoNode", thsad: typing.Optional[float] = None, smooth: typing.Optional[int] = None, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, lambda_: typing.Optional[float] = None, chroma: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, pnew: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, meander: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def SCDetection(self, vectors: "VideoNode", thscd1: typing.Optional[float] = None, thscd2: typing.Optional[float] = None) -> "VideoNode": ...
    def Super(self, hpad: typing.Optional[int] = None, vpad: typing.Optional[int] = None, pel: typing.Optional[int] = None, levels: typing.Optional[int] = None, chroma: typing.Optional[int] = None, sharp: typing.Optional[int] = None, rfilter: typing.Optional[int] = None, pelclip: typing.Optional["VideoNode"] = None) -> "VideoNode": ...

# end implementation


# implementation: neo_dfttest

class _Plugin_neo_dfttest_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DFTTest(self, clip: "VideoNode", ftype: typing.Optional[int] = None, sigma: typing.Optional[float] = None, sigma2: typing.Optional[float] = None, pmin: typing.Optional[float] = None, pmax: typing.Optional[float] = None, sbsize: typing.Optional[int] = None, smode: typing.Optional[int] = None, sosize: typing.Optional[int] = None, tbsize: typing.Optional[int] = None, tmode: typing.Optional[int] = None, tosize: typing.Optional[int] = None, swin: typing.Optional[int] = None, twin: typing.Optional[int] = None, sbeta: typing.Optional[float] = None, tbeta: typing.Optional[float] = None, zmean: typing.Optional[int] = None, f0beta: typing.Optional[float] = None, nlocation: typing.Union[int, typing.Sequence[int], None] = None, alpha: typing.Optional[float] = None, slocation: typing.Union[float, typing.Sequence[float], None] = None, ssx: typing.Union[float, typing.Sequence[float], None] = None, ssy: typing.Union[float, typing.Sequence[float], None] = None, sst: typing.Union[float, typing.Sequence[float], None] = None, ssystem: typing.Optional[int] = None, dither: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None, threads: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_neo_dfttest_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DFTTest(self, ftype: typing.Optional[int] = None, sigma: typing.Optional[float] = None, sigma2: typing.Optional[float] = None, pmin: typing.Optional[float] = None, pmax: typing.Optional[float] = None, sbsize: typing.Optional[int] = None, smode: typing.Optional[int] = None, sosize: typing.Optional[int] = None, tbsize: typing.Optional[int] = None, tmode: typing.Optional[int] = None, tosize: typing.Optional[int] = None, swin: typing.Optional[int] = None, twin: typing.Optional[int] = None, sbeta: typing.Optional[float] = None, tbeta: typing.Optional[float] = None, zmean: typing.Optional[int] = None, f0beta: typing.Optional[float] = None, nlocation: typing.Union[int, typing.Sequence[int], None] = None, alpha: typing.Optional[float] = None, slocation: typing.Union[float, typing.Sequence[float], None] = None, ssx: typing.Union[float, typing.Sequence[float], None] = None, ssy: typing.Union[float, typing.Sequence[float], None] = None, sst: typing.Union[float, typing.Sequence[float], None] = None, ssystem: typing.Optional[int] = None, dither: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None, threads: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: neo_f3kdb

class _Plugin_neo_f3kdb_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, clip: "VideoNode", range: typing.Optional[int] = None, y: typing.Optional[int] = None, cb: typing.Optional[int] = None, cr: typing.Optional[int] = None, grainy: typing.Optional[int] = None, grainc: typing.Optional[int] = None, sample_mode: typing.Optional[int] = None, seed: typing.Optional[int] = None, blur_first: typing.Optional[int] = None, dynamic_grain: typing.Optional[int] = None, opt: typing.Optional[int] = None, mt: typing.Optional[int] = None, dither_algo: typing.Optional[int] = None, keep_tv_range: typing.Optional[int] = None, output_depth: typing.Optional[int] = None, random_algo_ref: typing.Optional[int] = None, random_algo_grain: typing.Optional[int] = None, random_param_ref: typing.Optional[float] = None, random_param_grain: typing.Optional[float] = None, preset: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_neo_f3kdb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, range: typing.Optional[int] = None, y: typing.Optional[int] = None, cb: typing.Optional[int] = None, cr: typing.Optional[int] = None, grainy: typing.Optional[int] = None, grainc: typing.Optional[int] = None, sample_mode: typing.Optional[int] = None, seed: typing.Optional[int] = None, blur_first: typing.Optional[int] = None, dynamic_grain: typing.Optional[int] = None, opt: typing.Optional[int] = None, mt: typing.Optional[int] = None, dither_algo: typing.Optional[int] = None, keep_tv_range: typing.Optional[int] = None, output_depth: typing.Optional[int] = None, random_algo_ref: typing.Optional[int] = None, random_algo_grain: typing.Optional[int] = None, random_param_ref: typing.Optional[float] = None, random_param_grain: typing.Optional[float] = None, preset: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: neo_fft3d

class _Plugin_neo_fft3d_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFT3D(self, clip: "VideoNode", sigma: typing.Optional[float] = None, beta: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, bw: typing.Optional[int] = None, bh: typing.Optional[int] = None, bt: typing.Optional[int] = None, ow: typing.Optional[int] = None, oh: typing.Optional[int] = None, kratio: typing.Optional[float] = None, sharpen: typing.Optional[float] = None, scutoff: typing.Optional[float] = None, svr: typing.Optional[float] = None, smin: typing.Optional[float] = None, smax: typing.Optional[float] = None, measure: typing.Optional[int] = None, interlaced: typing.Optional[int] = None, wintype: typing.Optional[int] = None, pframe: typing.Optional[int] = None, px: typing.Optional[int] = None, py: typing.Optional[int] = None, pshow: typing.Optional[int] = None, pcutoff: typing.Optional[float] = None, pfactor: typing.Optional[float] = None, sigma2: typing.Optional[float] = None, sigma3: typing.Optional[float] = None, sigma4: typing.Optional[float] = None, degrid: typing.Optional[float] = None, dehalo: typing.Optional[float] = None, hr: typing.Optional[float] = None, ht: typing.Optional[float] = None, l: typing.Optional[int] = None, t: typing.Optional[int] = None, r: typing.Optional[int] = None, b: typing.Optional[int] = None, opt: typing.Optional[int] = None, ncpu: typing.Optional[int] = None, mt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_neo_fft3d_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFT3D(self, sigma: typing.Optional[float] = None, beta: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, bw: typing.Optional[int] = None, bh: typing.Optional[int] = None, bt: typing.Optional[int] = None, ow: typing.Optional[int] = None, oh: typing.Optional[int] = None, kratio: typing.Optional[float] = None, sharpen: typing.Optional[float] = None, scutoff: typing.Optional[float] = None, svr: typing.Optional[float] = None, smin: typing.Optional[float] = None, smax: typing.Optional[float] = None, measure: typing.Optional[int] = None, interlaced: typing.Optional[int] = None, wintype: typing.Optional[int] = None, pframe: typing.Optional[int] = None, px: typing.Optional[int] = None, py: typing.Optional[int] = None, pshow: typing.Optional[int] = None, pcutoff: typing.Optional[float] = None, pfactor: typing.Optional[float] = None, sigma2: typing.Optional[float] = None, sigma3: typing.Optional[float] = None, sigma4: typing.Optional[float] = None, degrid: typing.Optional[float] = None, dehalo: typing.Optional[float] = None, hr: typing.Optional[float] = None, ht: typing.Optional[float] = None, l: typing.Optional[int] = None, t: typing.Optional[int] = None, r: typing.Optional[int] = None, b: typing.Optional[int] = None, opt: typing.Optional[int] = None, ncpu: typing.Optional[int] = None, mt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: neo_minideen

class _Plugin_neo_minideen_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MiniDeen(self, clip: "VideoNode", radius: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Union[int, typing.Sequence[int], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_neo_minideen_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MiniDeen(self, radius: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Union[int, typing.Sequence[int], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: neo_tmedian

class _Plugin_neo_tmedian_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalMedian(self, clip: "VideoNode", radius: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_neo_tmedian_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalMedian(self, radius: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: neo_vd

class _Plugin_neo_vd_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VagueDenoiser(self, clip: "VideoNode", threshold: typing.Optional[float] = None, method: typing.Optional[int] = None, nsteps: typing.Optional[int] = None, percent: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_neo_vd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VagueDenoiser(self, threshold: typing.Optional[float] = None, method: typing.Optional[int] = None, nsteps: typing.Optional[int] = None, percent: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: nnedi3

class _Plugin_nnedi3_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, nsize: typing.Optional[int] = None, nns: typing.Optional[int] = None, qual: typing.Optional[int] = None, etype: typing.Optional[int] = None, pscrn: typing.Optional[int] = None, opt: typing.Optional[int] = None, int16_prescreener: typing.Optional[int] = None, int16_predictor: typing.Optional[int] = None, exp: typing.Optional[int] = None, show_mask: typing.Optional[int] = None, combed_only: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_nnedi3_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, field: int, dh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, nsize: typing.Optional[int] = None, nns: typing.Optional[int] = None, qual: typing.Optional[int] = None, etype: typing.Optional[int] = None, pscrn: typing.Optional[int] = None, opt: typing.Optional[int] = None, int16_prescreener: typing.Optional[int] = None, int16_predictor: typing.Optional[int] = None, exp: typing.Optional[int] = None, show_mask: typing.Optional[int] = None, combed_only: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: nnedi3cl

class _Plugin_nnedi3cl_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def NNEDI3CL(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = None, dw: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, nsize: typing.Optional[int] = None, nns: typing.Optional[int] = None, qual: typing.Optional[int] = None, etype: typing.Optional[int] = None, pscrn: typing.Optional[int] = None, device: typing.Optional[int] = None, list_device: typing.Optional[int] = None, info: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_nnedi3cl_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def NNEDI3CL(self, field: int, dh: typing.Optional[int] = None, dw: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, nsize: typing.Optional[int] = None, nns: typing.Optional[int] = None, qual: typing.Optional[int] = None, etype: typing.Optional[int] = None, pscrn: typing.Optional[int] = None, device: typing.Optional[int] = None, list_device: typing.Optional[int] = None, info: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: noisegen

class _Plugin_noisegen_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Generate(self, clip: "VideoNode", str: typing.Optional[float] = None, limit: typing.Optional[float] = None, type: typing.Optional[int] = None, mean: typing.Optional[float] = None, var: typing.Optional[float] = None, dyn: typing.Optional[int] = None, full: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_noisegen_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Generate(self, str: typing.Optional[float] = None, limit: typing.Optional[float] = None, type: typing.Optional[int] = None, mean: typing.Optional[float] = None, var: typing.Optional[float] = None, dyn: typing.Optional[int] = None, full: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: ocr

class _Plugin_ocr_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Recognize(self, clip: "VideoNode", datapath: typing.Union[str, bytes, bytearray, None] = None, language: typing.Union[str, bytes, bytearray, None] = None, options: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...


class _Plugin_ocr_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Recognize(self, datapath: typing.Union[str, bytes, bytearray, None] = None, language: typing.Union[str, bytes, bytearray, None] = None, options: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...

# end implementation


# implementation: ort

class _Plugin_ort_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Model(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], network_path: typing.Union[str, bytes, bytearray], overlap: typing.Union[int, typing.Sequence[int], None] = None, tilesize: typing.Union[int, typing.Sequence[int], None] = None, provider: typing.Union[str, bytes, bytearray, None] = None, device_id: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, verbosity: typing.Optional[int] = None, cudnn_benchmark: typing.Optional[int] = None, builtin: typing.Optional[int] = None, builtindir: typing.Union[str, bytes, bytearray, None] = None, fp16: typing.Optional[int] = None) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...


class _Plugin_ort_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Model(self, network_path: typing.Union[str, bytes, bytearray], overlap: typing.Union[int, typing.Sequence[int], None] = None, tilesize: typing.Union[int, typing.Sequence[int], None] = None, provider: typing.Union[str, bytes, bytearray, None] = None, device_id: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, verbosity: typing.Optional[int] = None, cudnn_benchmark: typing.Optional[int] = None, builtin: typing.Optional[int] = None, builtindir: typing.Union[str, bytes, bytearray, None] = None, fp16: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: ov

class _Plugin_ov_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Model(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], network_path: typing.Union[str, bytes, bytearray], overlap: typing.Union[int, typing.Sequence[int], None] = None, tilesize: typing.Union[int, typing.Sequence[int], None] = None, device: typing.Union[str, bytes, bytearray, None] = None, builtin: typing.Optional[int] = None, builtindir: typing.Union[str, bytes, bytearray, None] = None, fp16: typing.Optional[int] = None, dot_path: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...


class _Plugin_ov_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Model(self, network_path: typing.Union[str, bytes, bytearray], overlap: typing.Union[int, typing.Sequence[int], None] = None, tilesize: typing.Union[int, typing.Sequence[int], None] = None, device: typing.Union[str, bytes, bytearray, None] = None, builtin: typing.Optional[int] = None, builtindir: typing.Union[str, bytes, bytearray, None] = None, fp16: typing.Optional[int] = None, dot_path: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: placebo

class _Plugin_placebo_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, clip: "VideoNode", planes: typing.Optional[int] = None, iterations: typing.Optional[int] = None, threshold: typing.Optional[float] = None, radius: typing.Optional[float] = None, grain: typing.Optional[float] = None, dither: typing.Optional[int] = None, dither_algo: typing.Optional[int] = None, log_level: typing.Optional[int] = None) -> "VideoNode": ...
    def Resample(self, clip: "VideoNode", width: int, height: int, filter: typing.Union[str, bytes, bytearray, None] = None, clamp: typing.Optional[float] = None, blur: typing.Optional[float] = None, taper: typing.Optional[float] = None, radius: typing.Optional[float] = None, param1: typing.Optional[float] = None, param2: typing.Optional[float] = None, sx: typing.Optional[float] = None, sy: typing.Optional[float] = None, antiring: typing.Optional[float] = None, lut_entries: typing.Optional[int] = None, cutoff: typing.Optional[float] = None, sigmoidize: typing.Optional[int] = None, sigmoid_center: typing.Optional[float] = None, sigmoid_slope: typing.Optional[float] = None, linearize: typing.Optional[int] = None, trc: typing.Optional[int] = None, log_level: typing.Optional[int] = None) -> "VideoNode": ...
    def Shader(self, clip: "VideoNode", shader: typing.Union[str, bytes, bytearray, None] = None, width: typing.Optional[int] = None, height: typing.Optional[int] = None, chroma_loc: typing.Optional[int] = None, matrix: typing.Optional[int] = None, trc: typing.Optional[int] = None, linearize: typing.Optional[int] = None, sigmoidize: typing.Optional[int] = None, sigmoid_center: typing.Optional[float] = None, sigmoid_slope: typing.Optional[float] = None, lut_entries: typing.Optional[int] = None, antiring: typing.Optional[float] = None, filter: typing.Union[str, bytes, bytearray, None] = None, clamp: typing.Optional[float] = None, blur: typing.Optional[float] = None, taper: typing.Optional[float] = None, radius: typing.Optional[float] = None, param1: typing.Optional[float] = None, param2: typing.Optional[float] = None, shader_s: typing.Union[str, bytes, bytearray, None] = None, log_level: typing.Optional[int] = None) -> "VideoNode": ...
    def Tonemap(self, clip: "VideoNode", src_csp: typing.Optional[int] = None, dst_csp: typing.Optional[int] = None, src_max: typing.Optional[float] = None, src_min: typing.Optional[float] = None, dst_max: typing.Optional[float] = None, dst_min: typing.Optional[float] = None, dynamic_peak_detection: typing.Optional[int] = None, smoothing_period: typing.Optional[float] = None, scene_threshold_low: typing.Optional[float] = None, scene_threshold_high: typing.Optional[float] = None, intent: typing.Optional[int] = None, gamut_mode: typing.Optional[int] = None, tone_mapping_function: typing.Optional[int] = None, tone_mapping_mode: typing.Optional[int] = None, tone_mapping_param: typing.Optional[float] = None, tone_mapping_crosstalk: typing.Optional[float] = None, log_level: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_placebo_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, planes: typing.Optional[int] = None, iterations: typing.Optional[int] = None, threshold: typing.Optional[float] = None, radius: typing.Optional[float] = None, grain: typing.Optional[float] = None, dither: typing.Optional[int] = None, dither_algo: typing.Optional[int] = None, log_level: typing.Optional[int] = None) -> "VideoNode": ...
    def Resample(self, width: int, height: int, filter: typing.Union[str, bytes, bytearray, None] = None, clamp: typing.Optional[float] = None, blur: typing.Optional[float] = None, taper: typing.Optional[float] = None, radius: typing.Optional[float] = None, param1: typing.Optional[float] = None, param2: typing.Optional[float] = None, sx: typing.Optional[float] = None, sy: typing.Optional[float] = None, antiring: typing.Optional[float] = None, lut_entries: typing.Optional[int] = None, cutoff: typing.Optional[float] = None, sigmoidize: typing.Optional[int] = None, sigmoid_center: typing.Optional[float] = None, sigmoid_slope: typing.Optional[float] = None, linearize: typing.Optional[int] = None, trc: typing.Optional[int] = None, log_level: typing.Optional[int] = None) -> "VideoNode": ...
    def Shader(self, shader: typing.Union[str, bytes, bytearray, None] = None, width: typing.Optional[int] = None, height: typing.Optional[int] = None, chroma_loc: typing.Optional[int] = None, matrix: typing.Optional[int] = None, trc: typing.Optional[int] = None, linearize: typing.Optional[int] = None, sigmoidize: typing.Optional[int] = None, sigmoid_center: typing.Optional[float] = None, sigmoid_slope: typing.Optional[float] = None, lut_entries: typing.Optional[int] = None, antiring: typing.Optional[float] = None, filter: typing.Union[str, bytes, bytearray, None] = None, clamp: typing.Optional[float] = None, blur: typing.Optional[float] = None, taper: typing.Optional[float] = None, radius: typing.Optional[float] = None, param1: typing.Optional[float] = None, param2: typing.Optional[float] = None, shader_s: typing.Union[str, bytes, bytearray, None] = None, log_level: typing.Optional[int] = None) -> "VideoNode": ...
    def Tonemap(self, src_csp: typing.Optional[int] = None, dst_csp: typing.Optional[int] = None, src_max: typing.Optional[float] = None, src_min: typing.Optional[float] = None, dst_max: typing.Optional[float] = None, dst_min: typing.Optional[float] = None, dynamic_peak_detection: typing.Optional[int] = None, smoothing_period: typing.Optional[float] = None, scene_threshold_low: typing.Optional[float] = None, scene_threshold_high: typing.Optional[float] = None, intent: typing.Optional[int] = None, gamut_mode: typing.Optional[int] = None, tone_mapping_function: typing.Optional[int] = None, tone_mapping_mode: typing.Optional[int] = None, tone_mapping_param: typing.Optional[float] = None, tone_mapping_crosstalk: typing.Optional[float] = None, log_level: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: pp7

class _Plugin_pp7_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DeblockPP7(self, clip: "VideoNode", qp: typing.Optional[float] = None, mode: typing.Optional[int] = None, opt: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_pp7_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DeblockPP7(self, qp: typing.Optional[float] = None, mode: typing.Optional[int] = None, opt: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: qr

class _Plugin_qr_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Code(self, message: typing.Union[str, bytes, bytearray], version: typing.Optional[int] = None, error_correction: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: raws

class _Plugin_raws_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Source(self, source: typing.Union[str, bytes, bytearray], width: typing.Optional[int] = None, height: typing.Optional[int] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, sarnum: typing.Optional[int] = None, sarden: typing.Optional[int] = None, src_fmt: typing.Union[str, bytes, bytearray, None] = None, off_header: typing.Optional[int] = None, off_frame: typing.Optional[int] = None, rowbytes_align: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: rdfl

class _Plugin_rdfl_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ReduceFlicker(self, clip: "VideoNode", strength: typing.Optional[int] = None, aggressive: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_rdfl_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ReduceFlicker(self, strength: typing.Optional[int] = None, aggressive: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: rdvs

class _Plugin_rdvs_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DupBlocks(self, input: "VideoNode", gmthreshold: typing.Optional[int] = None, mthreshold: typing.Optional[int] = None, noise: typing.Optional[int] = None, noisy: typing.Optional[int] = None, dist: typing.Optional[int] = None, tolerance: typing.Optional[int] = None, dmode: typing.Optional[int] = None, pthreshold: typing.Optional[int] = None, cthreshold: typing.Optional[int] = None, grey: typing.Optional[int] = None) -> "VideoNode": ...
    def RestoreMotionBlocks(self, input: "VideoNode", restore: "VideoNode", neighbour: typing.Optional["VideoNode"] = None, neighbour2: typing.Optional["VideoNode"] = None, alternative: typing.Optional["VideoNode"] = None, gmthreshold: typing.Optional[int] = None, mthreshold: typing.Optional[int] = None, noise: typing.Optional[int] = None, noisy: typing.Optional[int] = None, dist: typing.Optional[int] = None, tolerance: typing.Optional[int] = None, dmode: typing.Optional[int] = None, pthreshold: typing.Optional[int] = None, cthreshold: typing.Optional[int] = None, grey: typing.Optional[int] = None) -> "VideoNode": ...
    def SCSelect(self, input: "VideoNode", sceneBegin: "VideoNode", sceneEnd: "VideoNode", globalMotion: "VideoNode", dfactor: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_rdvs_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DupBlocks(self, gmthreshold: typing.Optional[int] = None, mthreshold: typing.Optional[int] = None, noise: typing.Optional[int] = None, noisy: typing.Optional[int] = None, dist: typing.Optional[int] = None, tolerance: typing.Optional[int] = None, dmode: typing.Optional[int] = None, pthreshold: typing.Optional[int] = None, cthreshold: typing.Optional[int] = None, grey: typing.Optional[int] = None) -> "VideoNode": ...
    def RestoreMotionBlocks(self, restore: "VideoNode", neighbour: typing.Optional["VideoNode"] = None, neighbour2: typing.Optional["VideoNode"] = None, alternative: typing.Optional["VideoNode"] = None, gmthreshold: typing.Optional[int] = None, mthreshold: typing.Optional[int] = None, noise: typing.Optional[int] = None, noisy: typing.Optional[int] = None, dist: typing.Optional[int] = None, tolerance: typing.Optional[int] = None, dmode: typing.Optional[int] = None, pthreshold: typing.Optional[int] = None, cthreshold: typing.Optional[int] = None, grey: typing.Optional[int] = None) -> "VideoNode": ...
    def SCSelect(self, sceneBegin: "VideoNode", sceneEnd: "VideoNode", globalMotion: "VideoNode", dfactor: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: reduceflicker

class _Plugin_reduceflicker_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ReduceFlicker(self, clip: "VideoNode", strength: typing.Optional[int] = None, aggressive: typing.Optional[int] = None, grey: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_reduceflicker_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ReduceFlicker(self, strength: typing.Optional[int] = None, aggressive: typing.Optional[int] = None, grey: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: remap

class _Plugin_remap_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RemapFrames(self, baseclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None, sourceclip: typing.Optional["VideoNode"] = None, mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def RemapFramesSimple(self, clip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Remf(self, baseclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None, sourceclip: typing.Optional["VideoNode"] = None, mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def Remfs(self, clip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def ReplaceFramesSimple(self, baseclip: "VideoNode", sourceclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None, mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def Rfs(self, baseclip: "VideoNode", sourceclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None, mismatch: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_remap_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RemapFrames(self, filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None, sourceclip: typing.Optional["VideoNode"] = None, mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def RemapFramesSimple(self, filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Remf(self, filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None, sourceclip: typing.Optional["VideoNode"] = None, mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def Remfs(self, filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def ReplaceFramesSimple(self, sourceclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None, mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def Rfs(self, sourceclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = None, mappings: typing.Union[str, bytes, bytearray, None] = None, mismatch: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: resize

class _Plugin_resize_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bicubic(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Bilinear(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Bob(self, clip: "VideoNode", filter: typing.Union[str, bytes, bytearray, None] = None, tff: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Lanczos(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Point(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline16(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline36(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline64(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_resize_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bicubic(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Bilinear(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Bob(self, filter: typing.Union[str, bytes, bytearray, None] = None, tff: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Lanczos(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Point(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline16(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline36(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline64(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: retinex

class _Plugin_retinex_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MSRCP(self, input: "VideoNode", sigma: typing.Union[float, typing.Sequence[float], None] = None, lower_thr: typing.Optional[float] = None, upper_thr: typing.Optional[float] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, chroma_protect: typing.Optional[float] = None) -> "VideoNode": ...
    def MSRCR(self, input: "VideoNode", sigma: typing.Union[float, typing.Sequence[float], None] = None, lower_thr: typing.Optional[float] = None, upper_thr: typing.Optional[float] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, restore: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_retinex_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MSRCP(self, sigma: typing.Union[float, typing.Sequence[float], None] = None, lower_thr: typing.Optional[float] = None, upper_thr: typing.Optional[float] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, chroma_protect: typing.Optional[float] = None) -> "VideoNode": ...
    def MSRCR(self, sigma: typing.Union[float, typing.Sequence[float], None] = None, lower_thr: typing.Optional[float] = None, upper_thr: typing.Optional[float] = None, fulls: typing.Optional[int] = None, fulld: typing.Optional[int] = None, restore: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: rf

class _Plugin_rf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Replace(self, clip: "VideoNode", clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], intervals: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]]) -> "VideoNode": ...


class _Plugin_rf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Replace(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], intervals: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]]) -> "VideoNode": ...

# end implementation


# implementation: rgsf

class _Plugin_rgsf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BackwardClense(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Clense(self, clip: "VideoNode", previous: typing.Optional["VideoNode"] = None, next: typing.Optional["VideoNode"] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ForwardClense(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def RemoveGrain(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Repair(self, clip: "VideoNode", repairclip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def VerticalCleaner(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...


class _Plugin_rgsf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BackwardClense(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Clense(self, previous: typing.Optional["VideoNode"] = None, next: typing.Optional["VideoNode"] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ForwardClense(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def RemoveGrain(self, mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Repair(self, repairclip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def VerticalCleaner(self, mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...

# end implementation


# implementation: rgvs

class _Plugin_rgvs_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BackwardClense(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Clense(self, clip: "VideoNode", previous: typing.Optional["VideoNode"] = None, next: typing.Optional["VideoNode"] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ForwardClense(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def RemoveGrain(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Repair(self, clip: "VideoNode", repairclip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def VerticalCleaner(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...


class _Plugin_rgvs_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BackwardClense(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Clense(self, previous: typing.Optional["VideoNode"] = None, next: typing.Optional["VideoNode"] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ForwardClense(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def RemoveGrain(self, mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Repair(self, repairclip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def VerticalCleaner(self, mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...

# end implementation


# implementation: rife

class _Plugin_rife_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RIFE(self, clip: "VideoNode", model: typing.Optional[int] = None, multiplier: typing.Optional[int] = None, gpu_id: typing.Optional[int] = None, gpu_thread: typing.Optional[int] = None, tta: typing.Optional[int] = None, uhd: typing.Optional[int] = None, sc: typing.Optional[int] = None, list_gpu: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_rife_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RIFE(self, model: typing.Optional[int] = None, multiplier: typing.Optional[int] = None, gpu_id: typing.Optional[int] = None, gpu_thread: typing.Optional[int] = None, tta: typing.Optional[int] = None, uhd: typing.Optional[int] = None, sc: typing.Optional[int] = None, list_gpu: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: rsnv

class _Plugin_rsnv_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RealSR(self, clip: "VideoNode", scale: typing.Optional[int] = None, tilesize_x: typing.Optional[int] = None, tilesize_y: typing.Optional[int] = None, model: typing.Optional[int] = None, gpu_id: typing.Optional[int] = None, gpu_thread: typing.Optional[int] = None, tta: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_rsnv_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RealSR(self, scale: typing.Optional[int] = None, tilesize_x: typing.Optional[int] = None, tilesize_y: typing.Optional[int] = None, model: typing.Optional[int] = None, gpu_id: typing.Optional[int] = None, gpu_thread: typing.Optional[int] = None, tta: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: sangnom

class _Plugin_sangnom_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SangNom(self, clip: "VideoNode", order: typing.Optional[int] = None, dh: typing.Optional[int] = None, aa: typing.Union[int, typing.Sequence[int], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_sangnom_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SangNom(self, order: typing.Optional[int] = None, dh: typing.Optional[int] = None, aa: typing.Union[int, typing.Sequence[int], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: scd

class _Plugin_scd_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ApplyLog(self, clip: "VideoNode", log: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Detect(self, clip: "VideoNode", thresh: typing.Optional[int] = None, interval_h: typing.Optional[int] = None, interval_v: typing.Optional[int] = None, log: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_scd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ApplyLog(self, log: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Detect(self, thresh: typing.Optional[int] = None, interval_h: typing.Optional[int] = None, interval_v: typing.Optional[int] = None, log: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: scrawl

class _Plugin_scrawl_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ClipInfo(self, clip: "VideoNode", alignment: typing.Optional[int] = None) -> "VideoNode": ...
    def CoreInfo(self, clip: "VideoNode", alignment: typing.Optional[int] = None) -> "VideoNode": ...
    def FrameNum(self, clip: "VideoNode", alignment: typing.Optional[int] = None) -> "VideoNode": ...
    def FrameProps(self, clip: "VideoNode", alignment: typing.Optional[int] = None) -> "VideoNode": ...
    def Text(self, clip: "VideoNode", text: typing.Union[str, bytes, bytearray], alignment: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_scrawl_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ClipInfo(self, alignment: typing.Optional[int] = None) -> "VideoNode": ...
    def CoreInfo(self, alignment: typing.Optional[int] = None) -> "VideoNode": ...
    def FrameNum(self, alignment: typing.Optional[int] = None) -> "VideoNode": ...
    def FrameProps(self, alignment: typing.Optional[int] = None) -> "VideoNode": ...
    def Text(self, text: typing.Union[str, bytes, bytearray], alignment: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: scxvid

class _Plugin_scxvid_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Scxvid(self, clip: "VideoNode", log: typing.Union[str, bytes, bytearray, None] = None, use_slices: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_scxvid_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Scxvid(self, log: typing.Union[str, bytes, bytearray, None] = None, use_slices: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: smoothuv

class _Plugin_smoothuv_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothUV(self, clip: "VideoNode", radius: typing.Optional[int] = None, threshold: typing.Optional[int] = None, interlaced: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_smoothuv_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothUV(self, radius: typing.Optional[int] = None, threshold: typing.Optional[int] = None, interlaced: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: srmdnv

class _Plugin_srmdnv_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SRMD(self, clip: "VideoNode", scale: typing.Optional[int] = None, noise: typing.Optional[int] = None, tilesize_x: typing.Optional[int] = None, tilesize_y: typing.Optional[int] = None, gpu_id: typing.Optional[int] = None, gpu_thread: typing.Optional[int] = None, tta: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_srmdnv_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SRMD(self, scale: typing.Optional[int] = None, noise: typing.Optional[int] = None, tilesize_x: typing.Optional[int] = None, tilesize_y: typing.Optional[int] = None, gpu_id: typing.Optional[int] = None, gpu_thread: typing.Optional[int] = None, tta: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: ssiq

class _Plugin_ssiq_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SSIQ(self, clip: "VideoNode", diameter: typing.Optional[int] = None, strength: typing.Optional[int] = None, interlaced: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_ssiq_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SSIQ(self, diameter: typing.Optional[int] = None, strength: typing.Optional[int] = None, interlaced: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: std

class _Plugin_std_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddBorders(self, clip: "VideoNode", left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, color: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def AssumeFPS(self, clip: "VideoNode", src: typing.Optional["VideoNode"] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None) -> "VideoNode": ...
    def AssumeSampleRate(self, clip: "AudioNode", src: typing.Optional["AudioNode"] = None, samplerate: typing.Optional[int] = None) -> "AudioNode": ...
    def AudioGain(self, clip: "AudioNode", gain: typing.Union[float, typing.Sequence[float], None] = None) -> "AudioNode": ...
    def AudioLoop(self, clip: "AudioNode", times: typing.Optional[int] = None) -> "AudioNode": ...
    def AudioMix(self, clips: typing.Union["AudioNode", typing.Sequence["AudioNode"]], matrix: typing.Union[float, typing.Sequence[float]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "AudioNode": ...
    def AudioReverse(self, clip: "AudioNode") -> "AudioNode": ...
    def AudioSplice(self, clips: typing.Union["AudioNode", typing.Sequence["AudioNode"]]) -> "AudioNode": ...
    def AudioTrim(self, clip: "AudioNode", first: typing.Optional[int] = None, last: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "AudioNode": ...
    def AverageFrames(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], weights: typing.Union[float, typing.Sequence[float]], scale: typing.Optional[float] = None, scenechange: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Binarize(self, clip: "VideoNode", threshold: typing.Union[float, typing.Sequence[float], None] = None, v0: typing.Union[float, typing.Sequence[float], None] = None, v1: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BinarizeMask(self, clip: "VideoNode", threshold: typing.Union[float, typing.Sequence[float], None] = None, v0: typing.Union[float, typing.Sequence[float], None] = None, v1: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BlankAudio(self, clip: typing.Optional["AudioNode"] = None, channels: typing.Optional[int] = None, bits: typing.Optional[int] = None, sampletype: typing.Optional[int] = None, samplerate: typing.Optional[int] = None, length: typing.Optional[int] = None, keep: typing.Optional[int] = None) -> "AudioNode": ...
    def BlankClip(self, clip: typing.Optional["VideoNode"] = None, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, length: typing.Optional[int] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, color: typing.Union[float, typing.Sequence[float], None] = None, keep: typing.Optional[int] = None) -> "VideoNode": ...
    def BoxBlur(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, hradius: typing.Optional[int] = None, hpasses: typing.Optional[int] = None, vradius: typing.Optional[int] = None, vpasses: typing.Optional[int] = None) -> "VideoNode": ...
    def Cache(self, clip: "VideoNode", size: typing.Optional[int] = None, fixed: typing.Optional[int] = None, make_linear: typing.Optional[int] = None) -> "VideoNode": ...
    def ClipToProp(self, clip: "VideoNode", mclip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Convolution(self, clip: "VideoNode", matrix: typing.Union[float, typing.Sequence[float]], bias: typing.Optional[float] = None, divisor: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, saturate: typing.Optional[int] = None, mode: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def CopyFrameProps(self, clip: "VideoNode", prop_src: "VideoNode") -> "VideoNode": ...
    def Crop(self, clip: "VideoNode", left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None) -> "VideoNode": ...
    def CropAbs(self, clip: "VideoNode", width: int, height: int, left: typing.Optional[int] = None, top: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def CropRel(self, clip: "VideoNode", left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None) -> "VideoNode": ...
    def Deflate(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def DeleteFrames(self, clip: "VideoNode", frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def DoubleWeave(self, clip: "VideoNode", tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DuplicateFrames(self, clip: "VideoNode", frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Expr(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = None) -> "VideoNode": ...
    def FlipHorizontal(self, clip: "VideoNode") -> "VideoNode": ...
    def FlipVertical(self, clip: "VideoNode") -> "VideoNode": ...
    def FrameEval(self, clip: "VideoNode", eval: typing.Callable[..., typing.Any], prop_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None, clip_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None) -> "VideoNode": ...
    def FreezeFrames(self, clip: "VideoNode", first: typing.Union[int, typing.Sequence[int]], last: typing.Union[int, typing.Sequence[int]], replacement: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Inflate(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def Interleave(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], extend: typing.Optional[int] = None, mismatch: typing.Optional[int] = None, modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def Invert(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def InvertMask(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Levels(self, clip: "VideoNode", min_in: typing.Union[float, typing.Sequence[float], None] = None, max_in: typing.Union[float, typing.Sequence[float], None] = None, gamma: typing.Union[float, typing.Sequence[float], None] = None, min_out: typing.Union[float, typing.Sequence[float], None] = None, max_out: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Limiter(self, clip: "VideoNode", min: typing.Union[float, typing.Sequence[float], None] = None, max: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def LoadAllPlugins(self, path: typing.Union[str, bytes, bytearray]) -> None: ...
    def LoadPlugin(self, path: typing.Union[str, bytes, bytearray], altsearchpath: typing.Optional[int] = None, forcens: typing.Union[str, bytes, bytearray, None] = None, forceid: typing.Union[str, bytes, bytearray, None] = None) -> None: ...
    def Loop(self, clip: "VideoNode", times: typing.Optional[int] = None) -> "VideoNode": ...
    def Lut(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, lut: typing.Union[int, typing.Sequence[int], None] = None, lutf: typing.Union[float, typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Optional[int] = None, floatout: typing.Optional[int] = None) -> "VideoNode": ...
    def Lut2(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, lut: typing.Union[int, typing.Sequence[int], None] = None, lutf: typing.Union[float, typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Optional[int] = None, floatout: typing.Optional[int] = None) -> "VideoNode": ...
    def MakeDiff(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MaskedMerge(self, clipa: "VideoNode", clipb: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, first_plane: typing.Optional[int] = None, premultiplied: typing.Optional[int] = None) -> "VideoNode": ...
    def Maximum(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None, coordinates: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Median(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Merge(self, clipa: "VideoNode", clipb: "VideoNode", weight: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def MergeDiff(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Minimum(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None, coordinates: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ModifyFrame(self, clip: "VideoNode", clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], selector: typing.Callable[..., typing.Any]) -> "VideoNode": ...
    def PEMVerifier(self, clip: "VideoNode", upper: typing.Union[float, typing.Sequence[float], None] = None, lower: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def PlaneStats(self, clipa: "VideoNode", clipb: typing.Optional["VideoNode"] = None, plane: typing.Optional[int] = None, prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def PreMultiply(self, clip: "VideoNode", alpha: "VideoNode") -> "VideoNode": ...
    def Prewitt(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...
    def PropToClip(self, clip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def RemoveFrameProps(self, clip: "VideoNode", props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def Reverse(self, clip: "VideoNode") -> "VideoNode": ...
    def SelectEvery(self, clip: "VideoNode", cycle: int, offsets: typing.Union[int, typing.Sequence[int]], modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def SeparateFields(self, clip: "VideoNode", tff: typing.Optional[int] = None, modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def SetAudioCache(self, clip: "AudioNode", mode: typing.Optional[int] = None, fixedsize: typing.Optional[int] = None, maxsize: typing.Optional[int] = None, maxhistory: typing.Optional[int] = None) -> None: ...
    def SetFieldBased(self, clip: "VideoNode", value: int) -> "VideoNode": ...
    def SetFrameProp(self, clip: "VideoNode", prop: typing.Union[str, bytes, bytearray], intval: typing.Union[int, typing.Sequence[int], None] = None, floatval: typing.Union[float, typing.Sequence[float], None] = None, data: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def SetFrameProps(self, clip: "VideoNode", **kwargs: typing.Any) -> "VideoNode": ...
    def SetMaxCPU(self, cpu: typing.Union[str, bytes, bytearray]) -> typing.Union[str, bytes, bytearray]: ...
    def SetVideoCache(self, clip: "VideoNode", mode: typing.Optional[int] = None, fixedsize: typing.Optional[int] = None, maxsize: typing.Optional[int] = None, maxhistory: typing.Optional[int] = None) -> None: ...
    def ShuffleChannels(self, clips: typing.Union["AudioNode", typing.Sequence["AudioNode"]], channels_in: typing.Union[int, typing.Sequence[int]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "AudioNode": ...
    def ShufflePlanes(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], planes: typing.Union[int, typing.Sequence[int]], colorfamily: int) -> "VideoNode": ...
    def Sobel(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...
    def Splice(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def SplitChannels(self, clip: "AudioNode") -> typing.Union["AudioNode", typing.Sequence["AudioNode"]]: ...
    def SplitPlanes(self, clip: "VideoNode") -> typing.Union["VideoNode", typing.Sequence["VideoNode"]]: ...
    def StackHorizontal(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]]) -> "VideoNode": ...
    def StackVertical(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]]) -> "VideoNode": ...
    def TestAudio(self, channels: typing.Optional[int] = None, bits: typing.Optional[int] = None, isfloat: typing.Optional[int] = None, samplerate: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "AudioNode": ...
    def Transpose(self, clip: "VideoNode") -> "VideoNode": ...
    def Trim(self, clip: "VideoNode", first: typing.Optional[int] = None, last: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "VideoNode": ...
    def Turn180(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_std_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddBorders(self, left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, color: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def AssumeFPS(self, src: typing.Optional["VideoNode"] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None) -> "VideoNode": ...
    def AverageFrames(self, weights: typing.Union[float, typing.Sequence[float]], scale: typing.Optional[float] = None, scenechange: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Binarize(self, threshold: typing.Union[float, typing.Sequence[float], None] = None, v0: typing.Union[float, typing.Sequence[float], None] = None, v1: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BinarizeMask(self, threshold: typing.Union[float, typing.Sequence[float], None] = None, v0: typing.Union[float, typing.Sequence[float], None] = None, v1: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BlankClip(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, length: typing.Optional[int] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, color: typing.Union[float, typing.Sequence[float], None] = None, keep: typing.Optional[int] = None) -> "VideoNode": ...
    def BoxBlur(self, planes: typing.Union[int, typing.Sequence[int], None] = None, hradius: typing.Optional[int] = None, hpasses: typing.Optional[int] = None, vradius: typing.Optional[int] = None, vpasses: typing.Optional[int] = None) -> "VideoNode": ...
    def Cache(self, size: typing.Optional[int] = None, fixed: typing.Optional[int] = None, make_linear: typing.Optional[int] = None) -> "VideoNode": ...
    def ClipToProp(self, mclip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Convolution(self, matrix: typing.Union[float, typing.Sequence[float]], bias: typing.Optional[float] = None, divisor: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, saturate: typing.Optional[int] = None, mode: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def CopyFrameProps(self, prop_src: "VideoNode") -> "VideoNode": ...
    def Crop(self, left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None) -> "VideoNode": ...
    def CropAbs(self, width: int, height: int, left: typing.Optional[int] = None, top: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def CropRel(self, left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None) -> "VideoNode": ...
    def Deflate(self, planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def DeleteFrames(self, frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def DoubleWeave(self, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DuplicateFrames(self, frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Expr(self, expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = None) -> "VideoNode": ...
    def FlipHorizontal(self) -> "VideoNode": ...
    def FlipVertical(self) -> "VideoNode": ...
    def FrameEval(self, eval: typing.Callable[..., typing.Any], prop_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None, clip_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None) -> "VideoNode": ...
    def FreezeFrames(self, first: typing.Union[int, typing.Sequence[int]], last: typing.Union[int, typing.Sequence[int]], replacement: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Inflate(self, planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def Interleave(self, extend: typing.Optional[int] = None, mismatch: typing.Optional[int] = None, modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def Invert(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def InvertMask(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Levels(self, min_in: typing.Union[float, typing.Sequence[float], None] = None, max_in: typing.Union[float, typing.Sequence[float], None] = None, gamma: typing.Union[float, typing.Sequence[float], None] = None, min_out: typing.Union[float, typing.Sequence[float], None] = None, max_out: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Limiter(self, min: typing.Union[float, typing.Sequence[float], None] = None, max: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Loop(self, times: typing.Optional[int] = None) -> "VideoNode": ...
    def Lut(self, planes: typing.Union[int, typing.Sequence[int], None] = None, lut: typing.Union[int, typing.Sequence[int], None] = None, lutf: typing.Union[float, typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Optional[int] = None, floatout: typing.Optional[int] = None) -> "VideoNode": ...
    def Lut2(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, lut: typing.Union[int, typing.Sequence[int], None] = None, lutf: typing.Union[float, typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Optional[int] = None, floatout: typing.Optional[int] = None) -> "VideoNode": ...
    def MakeDiff(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MaskedMerge(self, clipb: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, first_plane: typing.Optional[int] = None, premultiplied: typing.Optional[int] = None) -> "VideoNode": ...
    def Maximum(self, planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None, coordinates: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Median(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Merge(self, clipb: "VideoNode", weight: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def MergeDiff(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Minimum(self, planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None, coordinates: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ModifyFrame(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], selector: typing.Callable[..., typing.Any]) -> "VideoNode": ...
    def PEMVerifier(self, upper: typing.Union[float, typing.Sequence[float], None] = None, lower: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def PlaneStats(self, clipb: typing.Optional["VideoNode"] = None, plane: typing.Optional[int] = None, prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def PreMultiply(self, alpha: "VideoNode") -> "VideoNode": ...
    def Prewitt(self, planes: typing.Union[int, typing.Sequence[int], None] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...
    def PropToClip(self, prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def RemoveFrameProps(self, props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def Reverse(self) -> "VideoNode": ...
    def SelectEvery(self, cycle: int, offsets: typing.Union[int, typing.Sequence[int]], modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def SeparateFields(self, tff: typing.Optional[int] = None, modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def SetFieldBased(self, value: int) -> "VideoNode": ...
    def SetFrameProp(self, prop: typing.Union[str, bytes, bytearray], intval: typing.Union[int, typing.Sequence[int], None] = None, floatval: typing.Union[float, typing.Sequence[float], None] = None, data: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def SetFrameProps(self, **kwargs: typing.Any) -> "VideoNode": ...
    def SetVideoCache(self, mode: typing.Optional[int] = None, fixedsize: typing.Optional[int] = None, maxsize: typing.Optional[int] = None, maxhistory: typing.Optional[int] = None) -> None: ...
    def ShufflePlanes(self, planes: typing.Union[int, typing.Sequence[int]], colorfamily: int) -> "VideoNode": ...
    def Sobel(self, planes: typing.Union[int, typing.Sequence[int], None] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...
    def Splice(self, mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def SplitPlanes(self) -> typing.Union["VideoNode", typing.Sequence["VideoNode"]]: ...
    def StackHorizontal(self) -> "VideoNode": ...
    def StackVertical(self) -> "VideoNode": ...
    def Transpose(self) -> "VideoNode": ...
    def Trim(self, first: typing.Optional[int] = None, last: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "VideoNode": ...
    def Turn180(self) -> "VideoNode": ...


class _Plugin_std_AudioNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AssumeSampleRate(self, src: typing.Optional["AudioNode"] = None, samplerate: typing.Optional[int] = None) -> "AudioNode": ...
    def AudioGain(self, gain: typing.Union[float, typing.Sequence[float], None] = None) -> "AudioNode": ...
    def AudioLoop(self, times: typing.Optional[int] = None) -> "AudioNode": ...
    def AudioMix(self, matrix: typing.Union[float, typing.Sequence[float]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "AudioNode": ...
    def AudioReverse(self) -> "AudioNode": ...
    def AudioSplice(self) -> "AudioNode": ...
    def AudioTrim(self, first: typing.Optional[int] = None, last: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "AudioNode": ...
    def BlankAudio(self, channels: typing.Optional[int] = None, bits: typing.Optional[int] = None, sampletype: typing.Optional[int] = None, samplerate: typing.Optional[int] = None, length: typing.Optional[int] = None, keep: typing.Optional[int] = None) -> "AudioNode": ...
    def SetAudioCache(self, mode: typing.Optional[int] = None, fixedsize: typing.Optional[int] = None, maxsize: typing.Optional[int] = None, maxhistory: typing.Optional[int] = None) -> None: ...
    def ShuffleChannels(self, channels_in: typing.Union[int, typing.Sequence[int]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "AudioNode": ...
    def SplitChannels(self) -> typing.Union["AudioNode", typing.Sequence["AudioNode"]]: ...

# end implementation


# implementation: sub

class _Plugin_sub_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ImageFile(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], id: typing.Optional[int] = None, palette: typing.Union[int, typing.Sequence[int], None] = None, gray: typing.Optional[int] = None, info: typing.Optional[int] = None, flatten: typing.Optional[int] = None, blend: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None) -> "VideoNode": ...
    def Subtitle(self, clip: "VideoNode", text: typing.Union[str, bytes, bytearray], start: typing.Optional[int] = None, end: typing.Optional[int] = None, debuglevel: typing.Optional[int] = None, fontdir: typing.Union[str, bytes, bytearray, None] = None, linespacing: typing.Optional[float] = None, margins: typing.Union[int, typing.Sequence[int], None] = None, sar: typing.Optional[float] = None, style: typing.Union[str, bytes, bytearray, None] = None, blend: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None) -> "VideoNode": ...
    def TextFile(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], charset: typing.Union[str, bytes, bytearray, None] = None, scale: typing.Optional[float] = None, debuglevel: typing.Optional[int] = None, fontdir: typing.Union[str, bytes, bytearray, None] = None, linespacing: typing.Optional[float] = None, margins: typing.Union[int, typing.Sequence[int], None] = None, sar: typing.Optional[float] = None, style: typing.Union[str, bytes, bytearray, None] = None, blend: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_sub_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ImageFile(self, file: typing.Union[str, bytes, bytearray], id: typing.Optional[int] = None, palette: typing.Union[int, typing.Sequence[int], None] = None, gray: typing.Optional[int] = None, info: typing.Optional[int] = None, flatten: typing.Optional[int] = None, blend: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None) -> "VideoNode": ...
    def Subtitle(self, text: typing.Union[str, bytes, bytearray], start: typing.Optional[int] = None, end: typing.Optional[int] = None, debuglevel: typing.Optional[int] = None, fontdir: typing.Union[str, bytes, bytearray, None] = None, linespacing: typing.Optional[float] = None, margins: typing.Union[int, typing.Sequence[int], None] = None, sar: typing.Optional[float] = None, style: typing.Union[str, bytes, bytearray, None] = None, blend: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None) -> "VideoNode": ...
    def TextFile(self, file: typing.Union[str, bytes, bytearray], charset: typing.Union[str, bytes, bytearray, None] = None, scale: typing.Optional[float] = None, debuglevel: typing.Optional[int] = None, fontdir: typing.Union[str, bytes, bytearray, None] = None, linespacing: typing.Optional[float] = None, margins: typing.Union[int, typing.Sequence[int], None] = None, sar: typing.Optional[float] = None, style: typing.Union[str, bytes, bytearray, None] = None, blend: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: surfaceblur

class _Plugin_surfaceblur_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def surfaceblur(self, input: "VideoNode", threshold: typing.Optional[float] = None, radius: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_surfaceblur_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def surfaceblur(self, threshold: typing.Optional[float] = None, radius: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: svp1

class _Plugin_svp1_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, clip: "VideoNode", sdata: int, src: "VideoNode", opt: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Super(self, clip: "VideoNode", opt: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...


class _Plugin_svp1_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, sdata: int, src: "VideoNode", opt: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Super(self, opt: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...

# end implementation


# implementation: svp2

class _Plugin_svp2_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothFps(self, clip: "VideoNode", super: "VideoNode", sdata: int, vectors: "VideoNode", vdata: int, opt: typing.Union[str, bytes, bytearray], src: typing.Optional["VideoNode"] = None, fps: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_svp2_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothFps(self, super: "VideoNode", sdata: int, vectors: "VideoNode", vdata: int, opt: typing.Union[str, bytes, bytearray], src: typing.Optional["VideoNode"] = None, fps: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: tbilateral

class _Plugin_tbilateral_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TBilateral(self, clip: "VideoNode", ppclip: typing.Optional["VideoNode"] = None, diameter: typing.Union[int, typing.Sequence[int], None] = None, sdev: typing.Union[float, typing.Sequence[float], None] = None, idev: typing.Union[float, typing.Sequence[float], None] = None, cs: typing.Union[float, typing.Sequence[float], None] = None, d2: typing.Optional[int] = None, kerns: typing.Optional[int] = None, kerni: typing.Optional[int] = None, restype: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_tbilateral_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TBilateral(self, ppclip: typing.Optional["VideoNode"] = None, diameter: typing.Union[int, typing.Sequence[int], None] = None, sdev: typing.Union[float, typing.Sequence[float], None] = None, idev: typing.Union[float, typing.Sequence[float], None] = None, cs: typing.Union[float, typing.Sequence[float], None] = None, d2: typing.Optional[int] = None, kerns: typing.Optional[int] = None, kerni: typing.Optional[int] = None, restype: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: tcanny

class _Plugin_tcanny_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TCanny(self, clip: "VideoNode", sigma: typing.Union[float, typing.Sequence[float], None] = None, sigma_v: typing.Union[float, typing.Sequence[float], None] = None, t_h: typing.Optional[float] = None, t_l: typing.Optional[float] = None, mode: typing.Optional[int] = None, op: typing.Optional[int] = None, scale: typing.Optional[float] = None, opt: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_tcanny_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TCanny(self, sigma: typing.Union[float, typing.Sequence[float], None] = None, sigma_v: typing.Union[float, typing.Sequence[float], None] = None, t_h: typing.Optional[float] = None, t_l: typing.Optional[float] = None, mode: typing.Optional[int] = None, op: typing.Optional[int] = None, scale: typing.Optional[float] = None, opt: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: tcax

class _Plugin_tcax_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TcasSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], fps: typing.Optional[float] = None, max_frame: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_tcax_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TcasSub(self, file: typing.Union[str, bytes, bytearray], fps: typing.Optional[float] = None, max_frame: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: tcm

class _Plugin_tcm_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TColorMask(self, clip: "VideoNode", colors: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], tolerance: typing.Optional[int] = None, bt601: typing.Optional[int] = None, gray: typing.Optional[int] = None, lutthr: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_tcm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TColorMask(self, colors: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], tolerance: typing.Optional[int] = None, bt601: typing.Optional[int] = None, gray: typing.Optional[int] = None, lutthr: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: tcomb

class _Plugin_tcomb_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TComb(self, clip: "VideoNode", mode: typing.Optional[int] = None, fthreshl: typing.Optional[int] = None, fthreshc: typing.Optional[int] = None, othreshl: typing.Optional[int] = None, othreshc: typing.Optional[int] = None, map: typing.Optional[int] = None, scthresh: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_tcomb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TComb(self, mode: typing.Optional[int] = None, fthreshl: typing.Optional[int] = None, fthreshc: typing.Optional[int] = None, othreshl: typing.Optional[int] = None, othreshc: typing.Optional[int] = None, map: typing.Optional[int] = None, scthresh: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: tdm

class _Plugin_tdm_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def IsCombed(self, clip: "VideoNode", cthresh: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, chroma: typing.Optional[int] = None, mi: typing.Optional[int] = None, metric: typing.Optional[int] = None) -> "VideoNode": ...
    def TDeintMod(self, clip: "VideoNode", order: int, field: typing.Optional[int] = None, mode: typing.Optional[int] = None, length: typing.Optional[int] = None, mtype: typing.Optional[int] = None, ttype: typing.Optional[int] = None, mtql: typing.Optional[int] = None, mthl: typing.Optional[int] = None, mtqc: typing.Optional[int] = None, mthc: typing.Optional[int] = None, nt: typing.Optional[int] = None, minthresh: typing.Optional[int] = None, maxthresh: typing.Optional[int] = None, cstr: typing.Optional[int] = None, athresh: typing.Optional[int] = None, metric: typing.Optional[int] = None, expand: typing.Optional[int] = None, link: typing.Optional[int] = None, show: typing.Optional[int] = None, edeint: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_tdm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def IsCombed(self, cthresh: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, chroma: typing.Optional[int] = None, mi: typing.Optional[int] = None, metric: typing.Optional[int] = None) -> "VideoNode": ...
    def TDeintMod(self, order: int, field: typing.Optional[int] = None, mode: typing.Optional[int] = None, length: typing.Optional[int] = None, mtype: typing.Optional[int] = None, ttype: typing.Optional[int] = None, mtql: typing.Optional[int] = None, mthl: typing.Optional[int] = None, mtqc: typing.Optional[int] = None, mthc: typing.Optional[int] = None, nt: typing.Optional[int] = None, minthresh: typing.Optional[int] = None, maxthresh: typing.Optional[int] = None, cstr: typing.Optional[int] = None, athresh: typing.Optional[int] = None, metric: typing.Optional[int] = None, expand: typing.Optional[int] = None, link: typing.Optional[int] = None, show: typing.Optional[int] = None, edeint: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: tedgemask

class _Plugin_tedgemask_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TEdgeMask(self, clip: "VideoNode", threshold: typing.Union[float, typing.Sequence[float], None] = None, type: typing.Optional[int] = None, link: typing.Optional[int] = None, scale: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_tedgemask_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TEdgeMask(self, threshold: typing.Union[float, typing.Sequence[float], None] = None, type: typing.Optional[int] = None, link: typing.Optional[int] = None, scale: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: text

class _Plugin_text_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ClipInfo(self, clip: "VideoNode", alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...
    def CoreInfo(self, clip: typing.Optional["VideoNode"] = None, alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...
    def FrameNum(self, clip: "VideoNode", alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...
    def FrameProps(self, clip: "VideoNode", props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...
    def Text(self, clip: "VideoNode", text: typing.Union[str, bytes, bytearray], alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_text_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ClipInfo(self, alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...
    def CoreInfo(self, alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...
    def FrameNum(self, alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...
    def FrameProps(self, props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...
    def Text(self, text: typing.Union[str, bytes, bytearray], alignment: typing.Optional[int] = None, scale: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: timecube

class _Plugin_timecube_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Cube(self, clip: "VideoNode", cube: typing.Union[str, bytes, bytearray], format: typing.Optional[int] = None, range: typing.Optional[int] = None, cpu: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_timecube_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Cube(self, cube: typing.Union[str, bytes, bytearray], format: typing.Optional[int] = None, range: typing.Optional[int] = None, cpu: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: tivtc

class _Plugin_tivtc_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TDecimate(self, clip: "VideoNode", mode: typing.Optional[int] = None, cycleR: typing.Optional[int] = None, cycle: typing.Optional[int] = None, rate: typing.Optional[float] = None, dupThresh: typing.Optional[float] = None, vidThresh: typing.Optional[float] = None, sceneThresh: typing.Optional[float] = None, hybrid: typing.Optional[int] = None, vidDetect: typing.Optional[int] = None, conCycle: typing.Optional[int] = None, conCycleTP: typing.Optional[int] = None, ovr: typing.Union[str, bytes, bytearray, None] = None, output: typing.Union[str, bytes, bytearray, None] = None, input: typing.Union[str, bytes, bytearray, None] = None, tfmIn: typing.Union[str, bytes, bytearray, None] = None, mkvOut: typing.Union[str, bytes, bytearray, None] = None, nt: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, debug: typing.Optional[int] = None, display: typing.Optional[int] = None, vfrDec: typing.Optional[int] = None, batch: typing.Optional[int] = None, tcfv1: typing.Optional[int] = None, se: typing.Optional[int] = None, chroma: typing.Optional[int] = None, exPP: typing.Optional[int] = None, maxndl: typing.Optional[int] = None, m2PA: typing.Optional[int] = None, denoise: typing.Optional[int] = None, noblend: typing.Optional[int] = None, ssd: typing.Optional[int] = None, hint: typing.Optional[int] = None, clip2: typing.Optional["VideoNode"] = None, sdlim: typing.Optional[int] = None, opt: typing.Optional[int] = None, orgOut: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def TFM(self, clip: "VideoNode", order: typing.Optional[int] = None, field: typing.Optional[int] = None, mode: typing.Optional[int] = None, PP: typing.Optional[int] = None, ovr: typing.Union[str, bytes, bytearray, None] = None, input: typing.Union[str, bytes, bytearray, None] = None, output: typing.Union[str, bytes, bytearray, None] = None, outputC: typing.Union[str, bytes, bytearray, None] = None, debug: typing.Optional[int] = None, display: typing.Optional[int] = None, slow: typing.Optional[int] = None, mChroma: typing.Optional[int] = None, cNum: typing.Optional[int] = None, cthresh: typing.Optional[int] = None, MI: typing.Optional[int] = None, chroma: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, y0: typing.Optional[int] = None, y1: typing.Optional[int] = None, mthresh: typing.Optional[int] = None, clip2: typing.Optional["VideoNode"] = None, d2v: typing.Union[str, bytes, bytearray, None] = None, ovrDefault: typing.Optional[int] = None, flags: typing.Optional[int] = None, scthresh: typing.Optional[float] = None, micout: typing.Optional[int] = None, micmatching: typing.Optional[int] = None, trimIn: typing.Union[str, bytes, bytearray, None] = None, hint: typing.Optional[int] = None, metric: typing.Optional[int] = None, batch: typing.Optional[int] = None, ubsco: typing.Optional[int] = None, mmsco: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_tivtc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TDecimate(self, mode: typing.Optional[int] = None, cycleR: typing.Optional[int] = None, cycle: typing.Optional[int] = None, rate: typing.Optional[float] = None, dupThresh: typing.Optional[float] = None, vidThresh: typing.Optional[float] = None, sceneThresh: typing.Optional[float] = None, hybrid: typing.Optional[int] = None, vidDetect: typing.Optional[int] = None, conCycle: typing.Optional[int] = None, conCycleTP: typing.Optional[int] = None, ovr: typing.Union[str, bytes, bytearray, None] = None, output: typing.Union[str, bytes, bytearray, None] = None, input: typing.Union[str, bytes, bytearray, None] = None, tfmIn: typing.Union[str, bytes, bytearray, None] = None, mkvOut: typing.Union[str, bytes, bytearray, None] = None, nt: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, debug: typing.Optional[int] = None, display: typing.Optional[int] = None, vfrDec: typing.Optional[int] = None, batch: typing.Optional[int] = None, tcfv1: typing.Optional[int] = None, se: typing.Optional[int] = None, chroma: typing.Optional[int] = None, exPP: typing.Optional[int] = None, maxndl: typing.Optional[int] = None, m2PA: typing.Optional[int] = None, denoise: typing.Optional[int] = None, noblend: typing.Optional[int] = None, ssd: typing.Optional[int] = None, hint: typing.Optional[int] = None, clip2: typing.Optional["VideoNode"] = None, sdlim: typing.Optional[int] = None, opt: typing.Optional[int] = None, orgOut: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def TFM(self, order: typing.Optional[int] = None, field: typing.Optional[int] = None, mode: typing.Optional[int] = None, PP: typing.Optional[int] = None, ovr: typing.Union[str, bytes, bytearray, None] = None, input: typing.Union[str, bytes, bytearray, None] = None, output: typing.Union[str, bytes, bytearray, None] = None, outputC: typing.Union[str, bytes, bytearray, None] = None, debug: typing.Optional[int] = None, display: typing.Optional[int] = None, slow: typing.Optional[int] = None, mChroma: typing.Optional[int] = None, cNum: typing.Optional[int] = None, cthresh: typing.Optional[int] = None, MI: typing.Optional[int] = None, chroma: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, y0: typing.Optional[int] = None, y1: typing.Optional[int] = None, mthresh: typing.Optional[int] = None, clip2: typing.Optional["VideoNode"] = None, d2v: typing.Union[str, bytes, bytearray, None] = None, ovrDefault: typing.Optional[int] = None, flags: typing.Optional[int] = None, scthresh: typing.Optional[float] = None, micout: typing.Optional[int] = None, micmatching: typing.Optional[int] = None, trimIn: typing.Union[str, bytes, bytearray, None] = None, hint: typing.Optional[int] = None, metric: typing.Optional[int] = None, batch: typing.Optional[int] = None, ubsco: typing.Optional[int] = None, mmsco: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: tla

class _Plugin_tla_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TempLinearApproximate(self, clip: "VideoNode", radius: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, gamma: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_tla_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TempLinearApproximate(self, radius: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, gamma: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: tmap

class _Plugin_tmap_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def tm(self, clip: "VideoNode", source_peak: float, desat: typing.Optional[float] = None, lin: typing.Optional[int] = None, show_satmask: typing.Optional[int] = None, show_clipped: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_tmap_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def tm(self, source_peak: float, desat: typing.Optional[float] = None, lin: typing.Optional[int] = None, show_satmask: typing.Optional[int] = None, show_clipped: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: tmc

class _Plugin_tmc_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TMaskCleaner(self, clip: "VideoNode", length: typing.Optional[int] = None, thresh: typing.Optional[int] = None, fade: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_tmc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TMaskCleaner(self, length: typing.Optional[int] = None, thresh: typing.Optional[int] = None, fade: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: tmedian

class _Plugin_tmedian_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalMedian(self, clip: "VideoNode", radius: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_tmedian_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalMedian(self, radius: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: tnlm

class _Plugin_tnlm_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TNLMeans(self, clip: "VideoNode", ax: typing.Optional[int] = None, ay: typing.Optional[int] = None, az: typing.Optional[int] = None, sx: typing.Optional[int] = None, sy: typing.Optional[int] = None, bx: typing.Optional[int] = None, by: typing.Optional[int] = None, a: typing.Optional[float] = None, h: typing.Optional[float] = None, ssd: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_tnlm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TNLMeans(self, ax: typing.Optional[int] = None, ay: typing.Optional[int] = None, az: typing.Optional[int] = None, sx: typing.Optional[int] = None, sy: typing.Optional[int] = None, bx: typing.Optional[int] = None, by: typing.Optional[int] = None, a: typing.Optional[float] = None, h: typing.Optional[float] = None, ssd: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: tonemap

class _Plugin_tonemap_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Hable(self, clip: "VideoNode", exposure: typing.Optional[float] = None, a: typing.Optional[float] = None, b: typing.Optional[float] = None, c: typing.Optional[float] = None, d: typing.Optional[float] = None, e: typing.Optional[float] = None, f: typing.Optional[float] = None, w: typing.Optional[float] = None) -> "VideoNode": ...
    def Mobius(self, clip: "VideoNode", exposure: typing.Optional[float] = None, transition: typing.Optional[float] = None, peak: typing.Optional[float] = None) -> "VideoNode": ...
    def Reinhard(self, clip: "VideoNode", exposure: typing.Optional[float] = None, contrast: typing.Optional[float] = None, peak: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_tonemap_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Hable(self, exposure: typing.Optional[float] = None, a: typing.Optional[float] = None, b: typing.Optional[float] = None, c: typing.Optional[float] = None, d: typing.Optional[float] = None, e: typing.Optional[float] = None, f: typing.Optional[float] = None, w: typing.Optional[float] = None) -> "VideoNode": ...
    def Mobius(self, exposure: typing.Optional[float] = None, transition: typing.Optional[float] = None, peak: typing.Optional[float] = None) -> "VideoNode": ...
    def Reinhard(self, exposure: typing.Optional[float] = None, contrast: typing.Optional[float] = None, peak: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: trans

class _Plugin_trans_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Accord(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None, twin: typing.Optional[int] = None, open: typing.Optional[int] = None) -> "VideoNode": ...
    def Bubbles(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, static: typing.Optional[int] = None) -> "VideoNode": ...
    def Central(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, nturns: typing.Optional[int] = None, emerge: typing.Optional[int] = None, resize: typing.Optional[int] = None) -> "VideoNode": ...
    def Crumple(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, crumple: typing.Optional[int] = None, emerge: typing.Optional[int] = None) -> "VideoNode": ...
    def Disco(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, emerge: typing.Optional[int] = None, rad: typing.Optional[int] = None, nturns: typing.Optional[int] = None) -> "VideoNode": ...
    def Door(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, open: typing.Optional[int] = None, vert: typing.Optional[int] = None) -> "VideoNode": ...
    def FlipPage(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, left: typing.Optional[int] = None) -> "VideoNode": ...
    def Funnel(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def Paint(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, style: typing.Optional[int] = None) -> "VideoNode": ...
    def Push(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def Ripple(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, origin: typing.Optional[int] = None, amp: typing.Optional[int] = None, wlength: typing.Optional[int] = None, merge: typing.Optional[int] = None) -> "VideoNode": ...
    def Roll(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None, rollin: typing.Optional[int] = None) -> "VideoNode": ...
    def Scratch(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, style: typing.Optional[int] = None) -> "VideoNode": ...
    def Shuffle(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def Slide(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None, slidein: typing.Optional[int] = None) -> "VideoNode": ...
    def Sprite(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def Swing(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None, open: typing.Optional[int] = None, ndoors: typing.Optional[int] = None, corner: typing.Optional[int] = None) -> "VideoNode": ...
    def Swirl(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, qr: typing.Optional[int] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def VenitianBlinds(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, style: typing.Optional[int] = None, slatwidth: typing.Optional[int] = None, open: typing.Optional[int] = None) -> "VideoNode": ...
    def Weave(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, style: typing.Optional[int] = None, slatwidth: typing.Optional[int] = None) -> "VideoNode": ...
    def Wipe(self, clip: "VideoNode", clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_trans_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Accord(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None, twin: typing.Optional[int] = None, open: typing.Optional[int] = None) -> "VideoNode": ...
    def Bubbles(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, static: typing.Optional[int] = None) -> "VideoNode": ...
    def Central(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, nturns: typing.Optional[int] = None, emerge: typing.Optional[int] = None, resize: typing.Optional[int] = None) -> "VideoNode": ...
    def Crumple(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, crumple: typing.Optional[int] = None, emerge: typing.Optional[int] = None) -> "VideoNode": ...
    def Disco(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, emerge: typing.Optional[int] = None, rad: typing.Optional[int] = None, nturns: typing.Optional[int] = None) -> "VideoNode": ...
    def Door(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, open: typing.Optional[int] = None, vert: typing.Optional[int] = None) -> "VideoNode": ...
    def FlipPage(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, left: typing.Optional[int] = None) -> "VideoNode": ...
    def Funnel(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def Paint(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, style: typing.Optional[int] = None) -> "VideoNode": ...
    def Push(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def Ripple(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, origin: typing.Optional[int] = None, amp: typing.Optional[int] = None, wlength: typing.Optional[int] = None, merge: typing.Optional[int] = None) -> "VideoNode": ...
    def Roll(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None, rollin: typing.Optional[int] = None) -> "VideoNode": ...
    def Scratch(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, style: typing.Optional[int] = None) -> "VideoNode": ...
    def Shuffle(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def Slide(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None, slidein: typing.Optional[int] = None) -> "VideoNode": ...
    def Sprite(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def Swing(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None, open: typing.Optional[int] = None, ndoors: typing.Optional[int] = None, corner: typing.Optional[int] = None) -> "VideoNode": ...
    def Swirl(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, qr: typing.Optional[int] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...
    def VenitianBlinds(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, style: typing.Optional[int] = None, slatwidth: typing.Optional[int] = None, open: typing.Optional[int] = None) -> "VideoNode": ...
    def Weave(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, style: typing.Optional[int] = None, slatwidth: typing.Optional[int] = None) -> "VideoNode": ...
    def Wipe(self, clipb: "VideoNode", overlap: typing.Optional[float] = None, dir: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: trt

class _Plugin_trt_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DeviceProperties(self, device_id: typing.Optional[int] = None) -> "VideoNode": ...
    def Model(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], engine_path: typing.Union[str, bytes, bytearray], overlap: typing.Union[int, typing.Sequence[int], None] = None, tilesize: typing.Union[int, typing.Sequence[int], None] = None, device_id: typing.Optional[int] = None, use_cuda_graph: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, verbosity: typing.Optional[int] = None) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...


class _Plugin_trt_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Model(self, engine_path: typing.Union[str, bytes, bytearray], overlap: typing.Union[int, typing.Sequence[int], None] = None, tilesize: typing.Union[int, typing.Sequence[int], None] = None, device_id: typing.Optional[int] = None, use_cuda_graph: typing.Optional[int] = None, num_streams: typing.Optional[int] = None, verbosity: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: ttmpsm

class _Plugin_ttmpsm_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TTempSmooth(self, clip: "VideoNode", maxr: typing.Optional[int] = None, thresh: typing.Union[int, typing.Sequence[int], None] = None, mdiff: typing.Union[int, typing.Sequence[int], None] = None, strength: typing.Optional[int] = None, scthresh: typing.Optional[float] = None, fp: typing.Optional[int] = None, pfclip: typing.Optional["VideoNode"] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_ttmpsm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TTempSmooth(self, maxr: typing.Optional[int] = None, thresh: typing.Union[int, typing.Sequence[int], None] = None, mdiff: typing.Union[int, typing.Sequence[int], None] = None, strength: typing.Optional[int] = None, scthresh: typing.Optional[float] = None, fp: typing.Optional[int] = None, pfclip: typing.Optional["VideoNode"] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: vcfreq

class _Plugin_vcfreq_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Blur(self, clip: "VideoNode", line: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def F1Quiver(self, clip: "VideoNode", filter: typing.Union[int, typing.Sequence[int]], morph: typing.Optional[int] = None, custom: typing.Optional[int] = None, test: typing.Optional[int] = None, strow: typing.Optional[int] = None, nrows: typing.Optional[int] = None, gamma: typing.Optional[float] = None) -> "VideoNode": ...
    def F2Quiver(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Sharp(self, clip: "VideoNode", line: typing.Optional[int] = None, wn: typing.Optional[float] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None, fr: typing.Optional[int] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_vcfreq_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Blur(self, line: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def F1Quiver(self, filter: typing.Union[int, typing.Sequence[int]], morph: typing.Optional[int] = None, custom: typing.Optional[int] = None, test: typing.Optional[int] = None, strow: typing.Optional[int] = None, nrows: typing.Optional[int] = None, gamma: typing.Optional[float] = None) -> "VideoNode": ...
    def F2Quiver(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Sharp(self, line: typing.Optional[int] = None, wn: typing.Optional[float] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None, fr: typing.Optional[int] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: vcm

class _Plugin_vcm_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Amp(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Bokeh(self, clip: "VideoNode", clipb: "VideoNode", grid: typing.Optional[int] = None, thresh: typing.Optional[float] = None, rgb: typing.Union[int, typing.Sequence[int], None] = None, yuv: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Circles(self, clip: "VideoNode", xo: typing.Optional[int] = None, yo: typing.Optional[int] = None, frad: typing.Optional[int] = None, cint: typing.Optional[int] = None, dots: typing.Optional[int] = None, rgb: typing.Union[int, typing.Sequence[int], None] = None, dim: typing.Optional[float] = None) -> "VideoNode": ...
    def ColorBox(self, format: typing.Optional[int] = None, luma: typing.Optional[int] = None, nbw: typing.Optional[int] = None, nbh: typing.Optional[int] = None) -> "VideoNode": ...
    def DeBarrel(self, clip: "VideoNode", abc: typing.Union[float, typing.Sequence[float]], method: typing.Optional[int] = None, pin: typing.Optional[int] = None, q: typing.Optional[int] = None, test: typing.Optional[int] = None, dots: typing.Union[str, bytes, bytearray, None] = None, dim: typing.Optional[float] = None) -> "VideoNode": ...
    def DeJitter(self, clip: "VideoNode", jmax: typing.Optional[int] = None, wsyn: typing.Optional[int] = None, thresh: typing.Optional[float] = None) -> "VideoNode": ...
    def F1QClean(self, clip: "VideoNode", span: typing.Optional[int] = None, fromf: typing.Optional[int] = None, upto: typing.Optional[int] = None) -> "VideoNode": ...
    def F1QLimit(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def F1Quiver(self, clip: "VideoNode", filter: typing.Union[int, typing.Sequence[int]], morph: typing.Optional[int] = None, custom: typing.Optional[int] = None, test: typing.Optional[int] = None, strow: typing.Optional[int] = None, nrows: typing.Optional[int] = None, gamma: typing.Optional[float] = None) -> "VideoNode": ...
    def F2QBlur(self, clip: "VideoNode", line: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def F2QBokeh(self, clip: "VideoNode", clipb: "VideoNode", grid: typing.Optional[int] = None, thresh: typing.Optional[float] = None, rgb: typing.Union[int, typing.Sequence[int], None] = None, yuv: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def F2QCorr(self, clip: "VideoNode", bclip: "VideoNode", cx: typing.Optional[int] = None, cy: typing.Optional[int] = None, txt: typing.Optional[int] = None, filename: typing.Union[str, bytes, bytearray, None] = None, sf: typing.Optional[int] = None, ef: typing.Optional[int] = None, every: typing.Optional[int] = None) -> "VideoNode": ...
    def F2QLimit(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def F2QSharp(self, clip: "VideoNode", line: typing.Optional[int] = None, wn: typing.Optional[float] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None, frad: typing.Optional[int] = None, ham: typing.Optional[int] = None, scale: typing.Optional[float] = None, rgb: typing.Union[int, typing.Sequence[int], None] = None, yuv: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def F2Quiver(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Fan(self, clip: "VideoNode", span: typing.Optional[int] = None, edge: typing.Optional[int] = None, plus: typing.Optional[int] = None, minus: typing.Optional[int] = None, uv: typing.Optional[int] = None) -> "VideoNode": ...
    def Fisheye(self, clip: "VideoNode", method: typing.Optional[int] = None, xo: typing.Optional[int] = None, yo: typing.Optional[int] = None, frad: typing.Optional[int] = None, sqr: typing.Optional[int] = None, rix: typing.Optional[float] = None, fov: typing.Optional[float] = None, test: typing.Optional[int] = None, dim: typing.Optional[float] = None, q: typing.Optional[int] = None, dots: typing.Optional[int] = None) -> "VideoNode": ...
    def GBlur(self, clip: "VideoNode", ksize: typing.Optional[int] = None, sd: typing.Optional[float] = None) -> "VideoNode": ...
    def Grid(self, clip: "VideoNode", lineint: typing.Optional[int] = None, bold: typing.Optional[int] = None, vbold: typing.Optional[int] = None, color: typing.Union[int, typing.Sequence[int], None] = None, bcolor: typing.Union[int, typing.Sequence[int], None] = None, vbcolor: typing.Union[int, typing.Sequence[int], None] = None, style: typing.Optional[int] = None) -> "VideoNode": ...
    def Hist(self, clip: "VideoNode", clipm: typing.Optional["VideoNode"] = None, type: typing.Optional[int] = None, table: typing.Union[int, typing.Sequence[int], None] = None, mf: typing.Optional[int] = None, window: typing.Optional[int] = None, limit: typing.Optional[int] = None) -> "VideoNode": ...
    def Jitter(self, clip: "VideoNode", type: typing.Optional[int] = None, jmax: typing.Optional[int] = None, dense: typing.Union[str, bytes, bytearray, None] = None, wl: typing.Optional[int] = None, stat: typing.Optional[int] = None, speed: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def MBlur(self, clip: "VideoNode", type: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def Mean(self, clip: "VideoNode", grid: typing.Optional[int] = None, tol: typing.Optional[float] = None) -> "VideoNode": ...
    def Median(self, clip: "VideoNode", maxgrid: typing.Optional[int] = None, plane: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Neural(self, clip: "VideoNode", txt: typing.Union[str, bytes, bytearray, None] = None, fname: typing.Union[str, bytes, bytearray, None] = None, tclip: typing.Optional["VideoNode"] = None, xpts: typing.Optional[int] = None, ypts: typing.Optional[int] = None, tlx: typing.Optional[int] = None, tty: typing.Optional[int] = None, trx: typing.Optional[int] = None, tby: typing.Optional[int] = None, iter: typing.Optional[int] = None, bestof: typing.Optional[int] = None, wset: typing.Optional[int] = None, rgb: typing.Optional[int] = None) -> "VideoNode": ...
    def Pattern(self, clip: "VideoNode", type: typing.Optional[int] = None, orient: typing.Optional[int] = None, spk: typing.Optional[int] = None, spike: typing.Optional[float] = None, wl: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None, rad: typing.Optional[int] = None, stat: typing.Optional[int] = None, overlay: typing.Optional[float] = None, bgr: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Reform(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Rotate(self, clip: "VideoNode", bkg: "VideoNode", angle: float, dinc: typing.Optional[float] = None, lx: typing.Optional[int] = None, wd: typing.Optional[int] = None, ty: typing.Optional[int] = None, ht: typing.Optional[int] = None, axx: typing.Optional[int] = None, axy: typing.Optional[int] = None, intq: typing.Optional[int] = None) -> "VideoNode": ...
    def SaltPepper(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, tol: typing.Optional[int] = None, avg: typing.Optional[int] = None) -> "VideoNode": ...
    def StepFilter(self, clip: "VideoNode", add: typing.Optional[int] = None, boost: typing.Optional[float] = None, segmenthor: typing.Optional[int] = None, segmentvert: typing.Optional[int] = None, limit: typing.Optional[int] = None) -> "VideoNode": ...
    def Variance(self, clip: "VideoNode", lx: int, wd: int, ty: int, ht: int, fn: typing.Optional[int] = None, uv: typing.Optional[int] = None, xgrid: typing.Optional[int] = None, ygrid: typing.Optional[int] = None) -> "VideoNode": ...
    def Veed(self, clip: "VideoNode", str: typing.Optional[int] = None, rad: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, plimit: typing.Union[int, typing.Sequence[int], None] = None, mlimit: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_vcm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Amp(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Bokeh(self, clipb: "VideoNode", grid: typing.Optional[int] = None, thresh: typing.Optional[float] = None, rgb: typing.Union[int, typing.Sequence[int], None] = None, yuv: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Circles(self, xo: typing.Optional[int] = None, yo: typing.Optional[int] = None, frad: typing.Optional[int] = None, cint: typing.Optional[int] = None, dots: typing.Optional[int] = None, rgb: typing.Union[int, typing.Sequence[int], None] = None, dim: typing.Optional[float] = None) -> "VideoNode": ...
    def DeBarrel(self, abc: typing.Union[float, typing.Sequence[float]], method: typing.Optional[int] = None, pin: typing.Optional[int] = None, q: typing.Optional[int] = None, test: typing.Optional[int] = None, dots: typing.Union[str, bytes, bytearray, None] = None, dim: typing.Optional[float] = None) -> "VideoNode": ...
    def DeJitter(self, jmax: typing.Optional[int] = None, wsyn: typing.Optional[int] = None, thresh: typing.Optional[float] = None) -> "VideoNode": ...
    def F1QClean(self, span: typing.Optional[int] = None, fromf: typing.Optional[int] = None, upto: typing.Optional[int] = None) -> "VideoNode": ...
    def F1QLimit(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def F1Quiver(self, filter: typing.Union[int, typing.Sequence[int]], morph: typing.Optional[int] = None, custom: typing.Optional[int] = None, test: typing.Optional[int] = None, strow: typing.Optional[int] = None, nrows: typing.Optional[int] = None, gamma: typing.Optional[float] = None) -> "VideoNode": ...
    def F2QBlur(self, line: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def F2QBokeh(self, clipb: "VideoNode", grid: typing.Optional[int] = None, thresh: typing.Optional[float] = None, rgb: typing.Union[int, typing.Sequence[int], None] = None, yuv: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def F2QCorr(self, bclip: "VideoNode", cx: typing.Optional[int] = None, cy: typing.Optional[int] = None, txt: typing.Optional[int] = None, filename: typing.Union[str, bytes, bytearray, None] = None, sf: typing.Optional[int] = None, ef: typing.Optional[int] = None, every: typing.Optional[int] = None) -> "VideoNode": ...
    def F2QLimit(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def F2QSharp(self, line: typing.Optional[int] = None, wn: typing.Optional[float] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None, frad: typing.Optional[int] = None, ham: typing.Optional[int] = None, scale: typing.Optional[float] = None, rgb: typing.Union[int, typing.Sequence[int], None] = None, yuv: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def F2Quiver(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Fan(self, span: typing.Optional[int] = None, edge: typing.Optional[int] = None, plus: typing.Optional[int] = None, minus: typing.Optional[int] = None, uv: typing.Optional[int] = None) -> "VideoNode": ...
    def Fisheye(self, method: typing.Optional[int] = None, xo: typing.Optional[int] = None, yo: typing.Optional[int] = None, frad: typing.Optional[int] = None, sqr: typing.Optional[int] = None, rix: typing.Optional[float] = None, fov: typing.Optional[float] = None, test: typing.Optional[int] = None, dim: typing.Optional[float] = None, q: typing.Optional[int] = None, dots: typing.Optional[int] = None) -> "VideoNode": ...
    def GBlur(self, ksize: typing.Optional[int] = None, sd: typing.Optional[float] = None) -> "VideoNode": ...
    def Grid(self, lineint: typing.Optional[int] = None, bold: typing.Optional[int] = None, vbold: typing.Optional[int] = None, color: typing.Union[int, typing.Sequence[int], None] = None, bcolor: typing.Union[int, typing.Sequence[int], None] = None, vbcolor: typing.Union[int, typing.Sequence[int], None] = None, style: typing.Optional[int] = None) -> "VideoNode": ...
    def Hist(self, clipm: typing.Optional["VideoNode"] = None, type: typing.Optional[int] = None, table: typing.Union[int, typing.Sequence[int], None] = None, mf: typing.Optional[int] = None, window: typing.Optional[int] = None, limit: typing.Optional[int] = None) -> "VideoNode": ...
    def Jitter(self, type: typing.Optional[int] = None, jmax: typing.Optional[int] = None, dense: typing.Union[str, bytes, bytearray, None] = None, wl: typing.Optional[int] = None, stat: typing.Optional[int] = None, speed: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def MBlur(self, type: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def Mean(self, grid: typing.Optional[int] = None, tol: typing.Optional[float] = None) -> "VideoNode": ...
    def Median(self, maxgrid: typing.Optional[int] = None, plane: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Neural(self, txt: typing.Union[str, bytes, bytearray, None] = None, fname: typing.Union[str, bytes, bytearray, None] = None, tclip: typing.Optional["VideoNode"] = None, xpts: typing.Optional[int] = None, ypts: typing.Optional[int] = None, tlx: typing.Optional[int] = None, tty: typing.Optional[int] = None, trx: typing.Optional[int] = None, tby: typing.Optional[int] = None, iter: typing.Optional[int] = None, bestof: typing.Optional[int] = None, wset: typing.Optional[int] = None, rgb: typing.Optional[int] = None) -> "VideoNode": ...
    def Pattern(self, type: typing.Optional[int] = None, orient: typing.Optional[int] = None, spk: typing.Optional[int] = None, spike: typing.Optional[float] = None, wl: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None, rad: typing.Optional[int] = None, stat: typing.Optional[int] = None, overlay: typing.Optional[float] = None, bgr: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Reform(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Rotate(self, bkg: "VideoNode", angle: float, dinc: typing.Optional[float] = None, lx: typing.Optional[int] = None, wd: typing.Optional[int] = None, ty: typing.Optional[int] = None, ht: typing.Optional[int] = None, axx: typing.Optional[int] = None, axy: typing.Optional[int] = None, intq: typing.Optional[int] = None) -> "VideoNode": ...
    def SaltPepper(self, planes: typing.Union[int, typing.Sequence[int], None] = None, tol: typing.Optional[int] = None, avg: typing.Optional[int] = None) -> "VideoNode": ...
    def StepFilter(self, add: typing.Optional[int] = None, boost: typing.Optional[float] = None, segmenthor: typing.Optional[int] = None, segmentvert: typing.Optional[int] = None, limit: typing.Optional[int] = None) -> "VideoNode": ...
    def Variance(self, lx: int, wd: int, ty: int, ht: int, fn: typing.Optional[int] = None, uv: typing.Optional[int] = None, xgrid: typing.Optional[int] = None, ygrid: typing.Optional[int] = None) -> "VideoNode": ...
    def Veed(self, str: typing.Optional[int] = None, rad: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, plimit: typing.Union[int, typing.Sequence[int], None] = None, mlimit: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: vcmod

class _Plugin_vcmod_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Amplitude(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Fan(self, clip: "VideoNode", span: typing.Optional[int] = None, edge: typing.Optional[int] = None, plus: typing.Optional[int] = None, minus: typing.Optional[int] = None, uv: typing.Optional[int] = None) -> "VideoNode": ...
    def GBlur(self, clip: "VideoNode", ksize: typing.Optional[int] = None, sd: typing.Optional[float] = None) -> "VideoNode": ...
    def Histogram(self, clip: "VideoNode", clipm: typing.Optional["VideoNode"] = None, type: typing.Optional[int] = None, table: typing.Union[int, typing.Sequence[int], None] = None, mf: typing.Optional[int] = None, window: typing.Optional[int] = None, limit: typing.Optional[int] = None) -> "VideoNode": ...
    def MBlur(self, clip: "VideoNode", type: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def Median(self, clip: "VideoNode", maxgrid: typing.Optional[int] = None, plane: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Neural(self, clip: "VideoNode", txt: typing.Union[str, bytes, bytearray, None] = None, fname: typing.Union[str, bytes, bytearray, None] = None, tclip: typing.Optional["VideoNode"] = None, xpts: typing.Optional[int] = None, ypts: typing.Optional[int] = None, tlx: typing.Optional[int] = None, tty: typing.Optional[int] = None, trx: typing.Optional[int] = None, tby: typing.Optional[int] = None, iter: typing.Optional[int] = None, bestof: typing.Optional[int] = None, wset: typing.Optional[int] = None, rgb: typing.Optional[int] = None) -> "VideoNode": ...
    def SaltPepper(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, tol: typing.Optional[int] = None, avg: typing.Optional[int] = None) -> "VideoNode": ...
    def Variance(self, clip: "VideoNode", lx: int, wd: int, ty: int, ht: int, fn: typing.Optional[int] = None, uv: typing.Optional[int] = None, xgrid: typing.Optional[int] = None, ygrid: typing.Optional[int] = None) -> "VideoNode": ...
    def Veed(self, clip: "VideoNode", str: typing.Optional[int] = None, rad: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, plimit: typing.Union[int, typing.Sequence[int], None] = None, mlimit: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_vcmod_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Amplitude(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Fan(self, span: typing.Optional[int] = None, edge: typing.Optional[int] = None, plus: typing.Optional[int] = None, minus: typing.Optional[int] = None, uv: typing.Optional[int] = None) -> "VideoNode": ...
    def GBlur(self, ksize: typing.Optional[int] = None, sd: typing.Optional[float] = None) -> "VideoNode": ...
    def Histogram(self, clipm: typing.Optional["VideoNode"] = None, type: typing.Optional[int] = None, table: typing.Union[int, typing.Sequence[int], None] = None, mf: typing.Optional[int] = None, window: typing.Optional[int] = None, limit: typing.Optional[int] = None) -> "VideoNode": ...
    def MBlur(self, type: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def Median(self, maxgrid: typing.Optional[int] = None, plane: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Neural(self, txt: typing.Union[str, bytes, bytearray, None] = None, fname: typing.Union[str, bytes, bytearray, None] = None, tclip: typing.Optional["VideoNode"] = None, xpts: typing.Optional[int] = None, ypts: typing.Optional[int] = None, tlx: typing.Optional[int] = None, tty: typing.Optional[int] = None, trx: typing.Optional[int] = None, tby: typing.Optional[int] = None, iter: typing.Optional[int] = None, bestof: typing.Optional[int] = None, wset: typing.Optional[int] = None, rgb: typing.Optional[int] = None) -> "VideoNode": ...
    def SaltPepper(self, planes: typing.Union[int, typing.Sequence[int], None] = None, tol: typing.Optional[int] = None, avg: typing.Optional[int] = None) -> "VideoNode": ...
    def Variance(self, lx: int, wd: int, ty: int, ht: int, fn: typing.Optional[int] = None, uv: typing.Optional[int] = None, xgrid: typing.Optional[int] = None, ygrid: typing.Optional[int] = None) -> "VideoNode": ...
    def Veed(self, str: typing.Optional[int] = None, rad: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, plimit: typing.Union[int, typing.Sequence[int], None] = None, mlimit: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: vcmove

class _Plugin_vcmove_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DeBarrel(self, clip: "VideoNode", a: float, b: float, c: float, vhr: typing.Optional[float] = None, pin: typing.Optional[int] = None, yind: typing.Optional[int] = None, ypin: typing.Optional[int] = None, ya: typing.Optional[float] = None, yb: typing.Optional[float] = None, yc: typing.Optional[float] = None, test: typing.Optional[int] = None) -> "VideoNode": ...
    def Quad2Rect(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Rect2Quad(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Rotate(self, clip: "VideoNode", bkg: "VideoNode", angle: float, dinc: typing.Optional[float] = None, lx: typing.Optional[int] = None, wd: typing.Optional[int] = None, ty: typing.Optional[int] = None, ht: typing.Optional[int] = None, axx: typing.Optional[int] = None, axy: typing.Optional[int] = None, intq: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_vcmove_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DeBarrel(self, a: float, b: float, c: float, vhr: typing.Optional[float] = None, pin: typing.Optional[int] = None, yind: typing.Optional[int] = None, ypin: typing.Optional[int] = None, ya: typing.Optional[float] = None, yb: typing.Optional[float] = None, yc: typing.Optional[float] = None, test: typing.Optional[int] = None) -> "VideoNode": ...
    def Quad2Rect(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Rect2Quad(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Rotate(self, bkg: "VideoNode", angle: float, dinc: typing.Optional[float] = None, lx: typing.Optional[int] = None, wd: typing.Optional[int] = None, ty: typing.Optional[int] = None, ht: typing.Optional[int] = None, axx: typing.Optional[int] = None, axy: typing.Optional[int] = None, intq: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: vd

class _Plugin_vd_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VagueDenoiser(self, clip: "VideoNode", threshold: typing.Optional[float] = None, method: typing.Optional[int] = None, nsteps: typing.Optional[int] = None, percent: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_vd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VagueDenoiser(self, threshold: typing.Optional[float] = None, method: typing.Optional[int] = None, nsteps: typing.Optional[int] = None, percent: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: vfrtocfr

class _Plugin_vfrtocfr_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VFRToCFR(self, clip: "VideoNode", timecodes: typing.Union[str, bytes, bytearray], fpsnum: int, fpsden: int, drop: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_vfrtocfr_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VFRToCFR(self, timecodes: typing.Union[str, bytes, bytearray], fpsnum: int, fpsden: int, drop: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: vivtc

class _Plugin_vivtc_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VDecimate(self, clip: "VideoNode", cycle: typing.Optional[int] = None, chroma: typing.Optional[int] = None, dupthresh: typing.Optional[float] = None, scthresh: typing.Optional[float] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, clip2: typing.Optional["VideoNode"] = None, ovr: typing.Union[str, bytes, bytearray, None] = None, dryrun: typing.Optional[int] = None) -> "VideoNode": ...
    def VFM(self, clip: "VideoNode", order: int, field: typing.Optional[int] = None, mode: typing.Optional[int] = None, mchroma: typing.Optional[int] = None, cthresh: typing.Optional[int] = None, mi: typing.Optional[int] = None, chroma: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, y0: typing.Optional[int] = None, y1: typing.Optional[int] = None, scthresh: typing.Optional[float] = None, micmatch: typing.Optional[int] = None, micout: typing.Optional[int] = None, clip2: typing.Optional["VideoNode"] = None) -> "VideoNode": ...


class _Plugin_vivtc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VDecimate(self, cycle: typing.Optional[int] = None, chroma: typing.Optional[int] = None, dupthresh: typing.Optional[float] = None, scthresh: typing.Optional[float] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, clip2: typing.Optional["VideoNode"] = None, ovr: typing.Union[str, bytes, bytearray, None] = None, dryrun: typing.Optional[int] = None) -> "VideoNode": ...
    def VFM(self, order: int, field: typing.Optional[int] = None, mode: typing.Optional[int] = None, mchroma: typing.Optional[int] = None, cthresh: typing.Optional[int] = None, mi: typing.Optional[int] = None, chroma: typing.Optional[int] = None, blockx: typing.Optional[int] = None, blocky: typing.Optional[int] = None, y0: typing.Optional[int] = None, y1: typing.Optional[int] = None, scthresh: typing.Optional[float] = None, micmatch: typing.Optional[int] = None, micout: typing.Optional[int] = None, clip2: typing.Optional["VideoNode"] = None) -> "VideoNode": ...

# end implementation


# implementation: vmaf

class _Plugin_vmaf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CAMBI(self, clip: "VideoNode", log_path: typing.Union[str, bytes, bytearray], log_format: typing.Optional[int] = None, window_size: typing.Optional[int] = None, topk: typing.Optional[float] = None, tvi_threshold: typing.Optional[float] = None, enc_width: typing.Optional[int] = None, enc_height: typing.Optional[int] = None) -> "VideoNode": ...
    def VMAF(self, reference: "VideoNode", distorted: "VideoNode", log_path: typing.Union[str, bytes, bytearray], log_format: typing.Optional[int] = None, model: typing.Union[int, typing.Sequence[int], None] = None, feature: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_vmaf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CAMBI(self, log_path: typing.Union[str, bytes, bytearray], log_format: typing.Optional[int] = None, window_size: typing.Optional[int] = None, topk: typing.Optional[float] = None, tvi_threshold: typing.Optional[float] = None, enc_width: typing.Optional[int] = None, enc_height: typing.Optional[int] = None) -> "VideoNode": ...
    def VMAF(self, distorted: "VideoNode", log_path: typing.Union[str, bytes, bytearray], log_format: typing.Optional[int] = None, model: typing.Union[int, typing.Sequence[int], None] = None, feature: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: vscope

class _Plugin_vscope_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Scope(self, clip: "VideoNode", mode: typing.Union[str, bytes, bytearray, None] = None, tickmarks: typing.Optional[int] = None, side: typing.Union[str, bytes, bytearray, None] = None, bottom: typing.Union[str, bytes, bytearray, None] = None, corner: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_vscope_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Scope(self, mode: typing.Union[str, bytes, bytearray, None] = None, tickmarks: typing.Optional[int] = None, side: typing.Union[str, bytes, bytearray, None] = None, bottom: typing.Union[str, bytes, bytearray, None] = None, corner: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: vsf

class _Plugin_vsf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = None, fps: typing.Optional[float] = None, vfr: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def VobSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...


class _Plugin_vsf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSub(self, file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = None, fps: typing.Optional[float] = None, vfr: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def VobSub(self, file: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...

# end implementation


# implementation: vsfm

class _Plugin_vsfm_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSubMod(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = None, fps: typing.Optional[float] = None, vfr: typing.Union[str, bytes, bytearray, None] = None, accurate: typing.Optional[int] = None) -> "VideoNode": ...
    def VobSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], accurate: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_vsfm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSubMod(self, file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = None, fps: typing.Optional[float] = None, vfr: typing.Union[str, bytes, bytearray, None] = None, accurate: typing.Optional[int] = None) -> "VideoNode": ...
    def VobSub(self, file: typing.Union[str, bytes, bytearray], accurate: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: w2xc

class _Plugin_w2xc_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, clip: "VideoNode", noise: typing.Optional[int] = None, scale: typing.Optional[int] = None, block: typing.Optional[int] = None, photo: typing.Optional[int] = None, gpu: typing.Optional[int] = None, processor: typing.Optional[int] = None, list_proc: typing.Optional[int] = None, log: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_w2xc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, noise: typing.Optional[int] = None, scale: typing.Optional[int] = None, block: typing.Optional[int] = None, photo: typing.Optional[int] = None, gpu: typing.Optional[int] = None, processor: typing.Optional[int] = None, list_proc: typing.Optional[int] = None, log: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: w2xnvk

class _Plugin_w2xnvk_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, clip: "VideoNode", noise: typing.Optional[int] = None, scale: typing.Optional[int] = None, model: typing.Optional[int] = None, tile_size: typing.Optional[int] = None, gpu_id: typing.Optional[int] = None, gpu_thread: typing.Optional[int] = None, precision: typing.Optional[int] = None, tile_size_w: typing.Optional[int] = None, tile_size_h: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_w2xnvk_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, noise: typing.Optional[int] = None, scale: typing.Optional[int] = None, model: typing.Optional[int] = None, tile_size: typing.Optional[int] = None, gpu_id: typing.Optional[int] = None, gpu_thread: typing.Optional[int] = None, precision: typing.Optional[int] = None, tile_size_w: typing.Optional[int] = None, tile_size_h: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: w3fdif

class _Plugin_w3fdif_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def W3FDIF(self, clip: "VideoNode", order: int, mode: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_w3fdif_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def W3FDIF(self, order: int, mode: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: waifu2x

class _Plugin_waifu2x_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Denoise(self, input: "VideoNode", mode: typing.Optional[int] = None, matrix: typing.Optional[int] = None, full: typing.Optional[int] = None, block_width: typing.Optional[int] = None, block_height: typing.Optional[int] = None, threads: typing.Optional[int] = None) -> "VideoNode": ...
    def Resize(self, input: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, shift_w: typing.Optional[float] = None, shift_h: typing.Optional[float] = None, subwidth: typing.Optional[float] = None, subheight: typing.Optional[float] = None, filter: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, subsample_w: typing.Optional[int] = None, subsample_h: typing.Optional[int] = None, chroma_loc_in: typing.Union[str, bytes, bytearray, None] = None, chroma_loc_out: typing.Union[str, bytes, bytearray, None] = None, matrix: typing.Optional[int] = None, full: typing.Optional[int] = None, block_width: typing.Optional[int] = None, block_height: typing.Optional[int] = None, threads: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_waifu2x_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Denoise(self, mode: typing.Optional[int] = None, matrix: typing.Optional[int] = None, full: typing.Optional[int] = None, block_width: typing.Optional[int] = None, block_height: typing.Optional[int] = None, threads: typing.Optional[int] = None) -> "VideoNode": ...
    def Resize(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, shift_w: typing.Optional[float] = None, shift_h: typing.Optional[float] = None, subwidth: typing.Optional[float] = None, subheight: typing.Optional[float] = None, filter: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, subsample_w: typing.Optional[int] = None, subsample_h: typing.Optional[int] = None, chroma_loc_in: typing.Union[str, bytes, bytearray, None] = None, chroma_loc_out: typing.Union[str, bytes, bytearray, None] = None, matrix: typing.Optional[int] = None, full: typing.Optional[int] = None, block_width: typing.Optional[int] = None, block_height: typing.Optional[int] = None, threads: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: warp

class _Plugin_warp_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ABlur(self, clip: "VideoNode", blur: typing.Optional[int] = None, type: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def ASobel(self, clip: "VideoNode", thresh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def AWarp(self, clip: "VideoNode", mask: "VideoNode", depth: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None, cplace: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def AWarpSharp2(self, clip: "VideoNode", thresh: typing.Optional[int] = None, blur: typing.Optional[int] = None, type: typing.Optional[int] = None, depth: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None, cplace: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_warp_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ABlur(self, blur: typing.Optional[int] = None, type: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def ASobel(self, thresh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def AWarp(self, mask: "VideoNode", depth: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None, cplace: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def AWarpSharp2(self, thresh: typing.Optional[int] = None, blur: typing.Optional[int] = None, type: typing.Optional[int] = None, depth: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, opt: typing.Optional[int] = None, cplace: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


# implementation: warpsf

class _Plugin_warpsf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ABlur(self, clip: "VideoNode", blur: typing.Optional[int] = None, type: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ASobel(self, clip: "VideoNode", thresh: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def AWarp(self, clip: "VideoNode", mask: "VideoNode", depth: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_warpsf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ABlur(self, blur: typing.Optional[int] = None, type: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ASobel(self, thresh: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def AWarp(self, mask: "VideoNode", depth: typing.Union[int, typing.Sequence[int], None] = None, chroma: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...

# end implementation


# implementation: wwxd

class _Plugin_wwxd_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def WWXD(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_wwxd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def WWXD(self) -> "VideoNode": ...

# end implementation


# implementation: xyvsf

class _Plugin_xyvsf_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = None, fps: typing.Optional[float] = None, vfr: typing.Union[str, bytes, bytearray, None] = None, swapuv: typing.Optional[int] = None) -> "VideoNode": ...
    def VobSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], swapuv: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_xyvsf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSub(self, file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = None, fps: typing.Optional[float] = None, vfr: typing.Union[str, bytes, bytearray, None] = None, swapuv: typing.Optional[int] = None) -> "VideoNode": ...
    def VobSub(self, file: typing.Union[str, bytes, bytearray], swapuv: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: yadifmod

class _Plugin_yadifmod_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Yadifmod(self, clip: "VideoNode", edeint: "VideoNode", order: int, field: typing.Optional[int] = None, mode: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_yadifmod_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Yadifmod(self, edeint: "VideoNode", order: int, field: typing.Optional[int] = None, mode: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: znedi3

class _Plugin_znedi3_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, nsize: typing.Optional[int] = None, nns: typing.Optional[int] = None, qual: typing.Optional[int] = None, etype: typing.Optional[int] = None, pscrn: typing.Optional[int] = None, opt: typing.Optional[int] = None, int16_prescreener: typing.Optional[int] = None, int16_predictor: typing.Optional[int] = None, exp: typing.Optional[int] = None, show_mask: typing.Optional[int] = None, x_nnedi3_weights_bin: typing.Union[str, bytes, bytearray, None] = None, x_cpu: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_znedi3_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, field: int, dh: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, nsize: typing.Optional[int] = None, nns: typing.Optional[int] = None, qual: typing.Optional[int] = None, etype: typing.Optional[int] = None, pscrn: typing.Optional[int] = None, opt: typing.Optional[int] = None, int16_prescreener: typing.Optional[int] = None, int16_predictor: typing.Optional[int] = None, exp: typing.Optional[int] = None, show_mask: typing.Optional[int] = None, x_nnedi3_weights_bin: typing.Union[str, bytes, bytearray, None] = None, x_cpu: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...

# end implementation


class VideoNode:
# instance_bound_VideoNode: acrop
    @property
    def acrop(self) -> _Plugin_acrop_VideoNode_Bound:
        """
        VapourSynth Auto Crop
        """
# end instance
# instance_bound_VideoNode: adg
    @property
    def adg(self) -> _Plugin_adg_VideoNode_Bound:
        """
        Adaptive grain
        """
# end instance
# instance_bound_VideoNode: akarin
    @property
    def akarin(self) -> _Plugin_akarin_VideoNode_Bound:
        """
        Akarin's Experimental Filters
        """
# end instance
# instance_bound_VideoNode: anime4kcpp
    @property
    def anime4kcpp(self) -> _Plugin_anime4kcpp_VideoNode_Bound:
        """
        Anime4KCPP for VapourSynth
        """
# end instance
# instance_bound_VideoNode: area
    @property
    def area(self) -> _Plugin_area_VideoNode_Bound:
        """
        area average downscaler plugin
        """
# end instance
# instance_bound_VideoNode: asharp
    @property
    def asharp(self) -> _Plugin_asharp_VideoNode_Bound:
        """
        adaptive sharpening filter
        """
# end instance
# instance_bound_VideoNode: assrender
    @property
    def assrender(self) -> _Plugin_assrender_VideoNode_Bound:
        """
        AssRender
        """
# end instance
# instance_bound_VideoNode: average
    @property
    def average(self) -> _Plugin_average_VideoNode_Bound:
        """
        vs-average
        """
# end instance
# instance_bound_VideoNode: avsw
    @property
    def avsw(self) -> _Plugin_avsw_VideoNode_Bound:
        """
        avsproxy
        """
# end instance
# instance_bound_VideoNode: bezier
    @property
    def bezier(self) -> _Plugin_bezier_VideoNode_Bound:
        """
        vapoursynth bezier curve test
        """
# end instance
# instance_bound_VideoNode: bifrost
    @property
    def bifrost(self) -> _Plugin_bifrost_VideoNode_Bound:
        """
        Bifrost plugin for VapourSynth
        """
# end instance
# instance_bound_VideoNode: bilateral
    @property
    def bilateral(self) -> _Plugin_bilateral_VideoNode_Bound:
        """
        Bilateral filter and Gaussian filter for VapourSynth.
        """
# end instance
# instance_bound_VideoNode: bilateralgpu
    @property
    def bilateralgpu(self) -> _Plugin_bilateralgpu_VideoNode_Bound:
        """
        Bilateral filter using CUDA
        """
# end instance
# instance_bound_VideoNode: bm3d
    @property
    def bm3d(self) -> _Plugin_bm3d_VideoNode_Bound:
        """
        Implementation of BM3D denoising filter for VapourSynth.
        """
# end instance
# instance_bound_VideoNode: bm3dcpu
    @property
    def bm3dcpu(self) -> _Plugin_bm3dcpu_VideoNode_Bound:
        """
        BM3D algorithm implemented in AVX and AVX2 intrinsics
        """
# end instance
# instance_bound_VideoNode: bm3dcuda
    @property
    def bm3dcuda(self) -> _Plugin_bm3dcuda_VideoNode_Bound:
        """
        BM3D algorithm implemented in CUDA
        """
# end instance
# instance_bound_VideoNode: bm3dcuda_rtc
    @property
    def bm3dcuda_rtc(self) -> _Plugin_bm3dcuda_rtc_VideoNode_Bound:
        """
        BM3D algorithm implemented in CUDA (NVRTC)
        """
# end instance
# instance_bound_VideoNode: box
    @property
    def box(self) -> _Plugin_box_VideoNode_Bound:
        """
        AVX2-optimized boxfilter
        """
# end instance
# instance_bound_VideoNode: butteraugli
    @property
    def butteraugli(self) -> _Plugin_butteraugli_VideoNode_Bound:
        """
        modified version of Google's butteraugli
        """
# end instance
# instance_bound_VideoNode: bwdif
    @property
    def bwdif(self) -> _Plugin_bwdif_VideoNode_Bound:
        """
        BobWeaver Deinterlacing Filter
        """
# end instance
# instance_bound_VideoNode: caffe
    @property
    def caffe(self) -> _Plugin_caffe_VideoNode_Bound:
        """
        Image Super-Resolution using Deep Convolutional Neural Networks
        """
# end instance
# instance_bound_VideoNode: cas
    @property
    def cas(self) -> _Plugin_cas_VideoNode_Bound:
        """
        Contrast Adaptive Sharpening
        """
# end instance
# instance_bound_VideoNode: ccd
    @property
    def ccd(self) -> _Plugin_ccd_VideoNode_Bound:
        """
        chroma denoiser
        """
# end instance
# instance_bound_VideoNode: cf
    @property
    def cf(self) -> _Plugin_cf_VideoNode_Bound:
        """
        VapourSynth ContinuityFixer port
        """
# end instance
# instance_bound_VideoNode: chkdr
    @property
    def chkdr(self) -> _Plugin_chkdr_VideoNode_Bound:
        """
        Film grain generator
        """
# end instance
# instance_bound_VideoNode: cnr2
    @property
    def cnr2(self) -> _Plugin_cnr2_VideoNode_Bound:
        """
        Chroma noise reducer
        """
# end instance
# instance_bound_VideoNode: comb
    @property
    def comb(self) -> _Plugin_comb_VideoNode_Bound:
        """
        comb filters v0.0.1
        """
# end instance
# instance_bound_VideoNode: ctmf
    @property
    def ctmf(self) -> _Plugin_ctmf_VideoNode_Bound:
        """
        Constant Time Median Filtering
        """
# end instance
# instance_bound_VideoNode: curve
    @property
    def curve(self) -> _Plugin_curve_VideoNode_Bound:
        """
        Apply color adjustments using curves
        """
# end instance
# instance_bound_VideoNode: d2v
    @property
    def d2v(self) -> _Plugin_d2v_VideoNode_Bound:
        """
        D2V Source
        """
# end instance
# instance_bound_VideoNode: damb
    @property
    def damb(self) -> _Plugin_damb_VideoNode_Bound:
        """
        Audio file reader and writer
        """
# end instance
# instance_bound_VideoNode: dct
    @property
    def dct(self) -> _Plugin_dct_VideoNode_Bound:
        """
        DCT filtering plugin rev10-b311e2e
        """
# end instance
# instance_bound_VideoNode: dctf
    @property
    def dctf(self) -> _Plugin_dctf_VideoNode_Bound:
        """
        DCT/IDCT Frequency Suppressor
        """
# end instance
# instance_bound_VideoNode: deblock
    @property
    def deblock(self) -> _Plugin_deblock_VideoNode_Bound:
        """
        It does a deblocking of the picture, using the deblocking filter of h264
        """
# end instance
# instance_bound_VideoNode: decross
    @property
    def decross(self) -> _Plugin_decross_VideoNode_Bound:
        """
        Spatio-temporal derainbow filter
        """
# end instance
# instance_bound_VideoNode: dedot
    @property
    def dedot(self) -> _Plugin_dedot_VideoNode_Bound:
        """
        Temporal dotcrawl and rainbow remover
        """
# end instance
# instance_bound_VideoNode: delogo
    @property
    def delogo(self) -> _Plugin_delogo_VideoNode_Bound:
        """
        VapourSynth Delogo Filter v005a.0.4
        """
# end instance
# instance_bound_VideoNode: delogohd
    @property
    def delogohd(self) -> _Plugin_delogohd_VideoNode_Bound:
        """
        VapourSynth DelogoHD Filter r12
        """
# end instance
# instance_bound_VideoNode: depan
    @property
    def depan(self) -> _Plugin_depan_VideoNode_Bound:
        """
        Tools for estimation and compensation of global motion (pan)
        """
# end instance
# instance_bound_VideoNode: descale
    @property
    def descale(self) -> _Plugin_descale_VideoNode_Bound:
        """
        Undo linear interpolation
        """
# end instance
# instance_bound_VideoNode: descale_getnative
    @property
    def descale_getnative(self) -> _Plugin_descale_getnative_VideoNode_Bound:
        """
        Undo linear interpolation
        """
# end instance
# instance_bound_VideoNode: dfttest
    @property
    def dfttest(self) -> _Plugin_dfttest_VideoNode_Bound:
        """
        2D/3D frequency domain denoiser
        """
# end instance
# instance_bound_VideoNode: dghdrtosdr
    @property
    def dghdrtosdr(self) -> _Plugin_dghdrtosdr_VideoNode_Bound:
        """
        Convert HDR to SDR
        """
# end instance
# instance_bound_VideoNode: dgm
    @property
    def dgm(self) -> _Plugin_dgm_VideoNode_Bound:
        """
        Spatio-temporal limited median denoiser
        """
# end instance
# instance_bound_VideoNode: dotkill
    @property
    def dotkill(self) -> _Plugin_dotkill_VideoNode_Bound:
        """
        VapourSynth DotKill
        """
# end instance
# instance_bound_VideoNode: dpid
    @property
    def dpid(self) -> _Plugin_dpid_VideoNode_Bound:
        """
        Rapid, Detail-Preserving Image Downscaling
        """
# end instance
# instance_bound_VideoNode: draw
    @property
    def draw(self) -> _Plugin_draw_VideoNode_Bound:
        """
        a simple alternative to Masktools2's mt_lutspa
        """
# end instance
# instance_bound_VideoNode: edgefixer
    @property
    def edgefixer(self) -> _Plugin_edgefixer_VideoNode_Bound:
        """
        ultraman
        """
# end instance
# instance_bound_VideoNode: eedi2
    @property
    def eedi2(self) -> _Plugin_eedi2_VideoNode_Bound:
        """
        EEDI2
        """
# end instance
# instance_bound_VideoNode: eedi2cuda
    @property
    def eedi2cuda(self) -> _Plugin_eedi2cuda_VideoNode_Bound:
        """
        EEDI2 filter using CUDA
        """
# end instance
# instance_bound_VideoNode: eedi3m
    @property
    def eedi3m(self) -> _Plugin_eedi3m_VideoNode_Bound:
        """
        Enhanced Edge Directed Interpolation 3
        """
# end instance
# instance_bound_VideoNode: f3kdb
    @property
    def f3kdb(self) -> _Plugin_f3kdb_VideoNode_Bound:
        """
        flash3kyuu_deband
        """
# end instance
# instance_bound_VideoNode: fb
    @property
    def fb(self) -> _Plugin_fb_VideoNode_Bound:
        """
        FillBorders plugin for VapourSynth
        """
# end instance
# instance_bound_VideoNode: fft3dfilter
    @property
    def fft3dfilter(self) -> _Plugin_fft3dfilter_VideoNode_Bound:
        """
        systems
        """
# end instance
# instance_bound_VideoNode: fftspectrum
    @property
    def fftspectrum(self) -> _Plugin_fftspectrum_VideoNode_Bound:
        """
        FFT Spectrum plugin
        """
# end instance
# instance_bound_VideoNode: fh
    @property
    def fh(self) -> _Plugin_fh_VideoNode_Bound:
        """
        FieldHint Plugin
        """
# end instance
# instance_bound_VideoNode: flux
    @property
    def flux(self) -> _Plugin_flux_VideoNode_Bound:
        """
        FluxSmooth plugin for VapourSynth
        """
# end instance
# instance_bound_VideoNode: fmtc
    @property
    def fmtc(self) -> _Plugin_fmtc_VideoNode_Bound:
        """
        Format converter
        """
# end instance
# instance_bound_VideoNode: focus
    @property
    def focus(self) -> _Plugin_focus_VideoNode_Bound:
        """
        VapourSynth Pixel Restoration Filters
        """
# end instance
# instance_bound_VideoNode: focus2
    @property
    def focus2(self) -> _Plugin_focus2_VideoNode_Bound:
        """
        VapourSynth TemporalSoften Filter v1
        """
# end instance
# instance_bound_VideoNode: ftf
    @property
    def ftf(self) -> _Plugin_ftf_VideoNode_Bound:
        """
        Fix Telecined Fades
        """
# end instance
# instance_bound_VideoNode: grad
    @property
    def grad(self) -> _Plugin_grad_VideoNode_Bound:
        """
        Adjustment of contrast, brightness, gamma and a wide range of color manipulations through gradation curves is possible.
        """
# end instance
# instance_bound_VideoNode: grain
    @property
    def grain(self) -> _Plugin_grain_VideoNode_Bound:
        """
        Random noise film grain generator
        """
# end instance
# instance_bound_VideoNode: hist
    @property
    def hist(self) -> _Plugin_hist_VideoNode_Bound:
        """
        VapourSynth Histogram Plugin
        """
# end instance
# instance_bound_VideoNode: hqdn3d
    @property
    def hqdn3d(self) -> _Plugin_hqdn3d_VideoNode_Bound:
        """
        HQDn3D port as used in avisynth/mplayer
        """
# end instance
# instance_bound_VideoNode: iccc
    @property
    def iccc(self) -> _Plugin_iccc_VideoNode_Bound:
        """
        ICC Conversion
        """
# end instance
# instance_bound_VideoNode: imwri
    @property
    def imwri(self) -> _Plugin_imwri_VideoNode_Bound:
        """
        VapourSynth ImageMagick 7 HDRI Writer/Reader
        """
# end instance
# instance_bound_VideoNode: it
    @property
    def it(self) -> _Plugin_it_VideoNode_Bound:
        """
        VapourSynth IVTC Filter v0103.1.1
        """
# end instance
# instance_bound_VideoNode: jinc
    @property
    def jinc(self) -> _Plugin_jinc_VideoNode_Bound:
        """
        VapourSynth EWA resampling
        """
# end instance
# instance_bound_VideoNode: knlm
    @property
    def knlm(self) -> _Plugin_knlm_VideoNode_Bound:
        """
        KNLMeansCL for VapourSynth
        """
# end instance
# instance_bound_VideoNode: lghost
    @property
    def lghost(self) -> _Plugin_lghost_VideoNode_Bound:
        """
        Ghost Reduction
        """
# end instance
# instance_bound_VideoNode: libp2p
    @property
    def libp2p(self) -> _Plugin_libp2p_VideoNode_Bound:
        """
        libp2p rgb formats packer/unpacker
        """
# end instance
# instance_bound_VideoNode: matchhist
    @property
    def matchhist(self) -> _Plugin_matchhist_VideoNode_Bound:
        """
        MatchHistogram
        """
# end instance
# instance_bound_VideoNode: median
    @property
    def median(self) -> _Plugin_median_VideoNode_Bound:
        """
        Median of clips
        """
# end instance
# instance_bound_VideoNode: minideen
    @property
    def minideen(self) -> _Plugin_minideen_VideoNode_Bound:
        """
        Spatial convolution with thresholds
        """
# end instance
# instance_bound_VideoNode: minsrp
    @property
    def minsrp(self) -> _Plugin_minsrp_VideoNode_Bound:
        """
        VapourSynth MinSRP Filter
        """
# end instance
# instance_bound_VideoNode: misc
    @property
    def misc(self) -> _Plugin_misc_VideoNode_Bound:
        """
        Miscellaneous filters
        """
# end instance
# instance_bound_VideoNode: morpho
    @property
    def morpho(self) -> _Plugin_morpho_VideoNode_Bound:
        """
        Simple morphological filters.
        """
# end instance
# instance_bound_VideoNode: motionmask
    @property
    def motionmask(self) -> _Plugin_motionmask_VideoNode_Bound:
        """
        MotionMask creates a mask of moving pixels
        """
# end instance
# instance_bound_VideoNode: mpeg2stinx
    @property
    def mpeg2stinx(self) -> _Plugin_mpeg2stinx_VideoNode_Bound:
        """
        Mpeg2Stinx
        """
# end instance
# instance_bound_VideoNode: msmoosh
    @property
    def msmoosh(self) -> _Plugin_msmoosh_VideoNode_Bound:
        """
        MSmooth and MSharpen
        """
# end instance
# instance_bound_VideoNode: mv
    @property
    def mv(self) -> _Plugin_mv_VideoNode_Bound:
        """
        MVTools v23
        """
# end instance
# instance_bound_VideoNode: mvsf
    @property
    def mvsf(self) -> _Plugin_mvsf_VideoNode_Bound:
        """
        MVTools Single Precision
        """
# end instance
# instance_bound_VideoNode: neo_dfttest
    @property
    def neo_dfttest(self) -> _Plugin_neo_dfttest_VideoNode_Bound:
        """
        Neo DFTTest Deband Filter r7 - 2D/3D frequency domain denoiser
        """
# end instance
# instance_bound_VideoNode: neo_f3kdb
    @property
    def neo_f3kdb(self) -> _Plugin_neo_f3kdb_VideoNode_Bound:
        """
        Neo F3KDB Deband Filter r7
        """
# end instance
# instance_bound_VideoNode: neo_fft3d
    @property
    def neo_fft3d(self) -> _Plugin_neo_fft3d_VideoNode_Bound:
        """
        Neo FFT3D Filter r11
        """
# end instance
# instance_bound_VideoNode: neo_minideen
    @property
    def neo_minideen(self) -> _Plugin_neo_minideen_VideoNode_Bound:
        """
        Neo Minideen Filter r11
        """
# end instance
# instance_bound_VideoNode: neo_tmedian
    @property
    def neo_tmedian(self) -> _Plugin_neo_tmedian_VideoNode_Bound:
        """
        Neo Temporal Median Filter r2
        """
# end instance
# instance_bound_VideoNode: neo_vd
    @property
    def neo_vd(self) -> _Plugin_neo_vd_VideoNode_Bound:
        """
        Neo Vague Denoiser Filter r2
        """
# end instance
# instance_bound_VideoNode: nnedi3
    @property
    def nnedi3(self) -> _Plugin_nnedi3_VideoNode_Bound:
        """
        Neural network edge directed interpolation (3rd gen.), v12
        """
# end instance
# instance_bound_VideoNode: nnedi3cl
    @property
    def nnedi3cl(self) -> _Plugin_nnedi3cl_VideoNode_Bound:
        """
        An intra-field only deinterlacer
        """
# end instance
# instance_bound_VideoNode: noisegen
    @property
    def noisegen(self) -> _Plugin_noisegen_VideoNode_Bound:
        """
        VapourSynth Noise Generator
        """
# end instance
# instance_bound_VideoNode: ocr
    @property
    def ocr(self) -> _Plugin_ocr_VideoNode_Bound:
        """
        Tesseract OCR Filter
        """
# end instance
# instance_bound_VideoNode: ort
    @property
    def ort(self) -> _Plugin_ort_VideoNode_Bound:
        """
        ONNX Runtime ML Filter Runtime
        """
# end instance
# instance_bound_VideoNode: ov
    @property
    def ov(self) -> _Plugin_ov_VideoNode_Bound:
        """
        OpenVINO ML Filter Runtime
        """
# end instance
# instance_bound_VideoNode: placebo
    @property
    def placebo(self) -> _Plugin_placebo_VideoNode_Bound:
        """
        libplacebo plugin for VapourSynth
        """
# end instance
# instance_bound_VideoNode: pp7
    @property
    def pp7(self) -> _Plugin_pp7_VideoNode_Bound:
        """
        Postprocess 7 from MPlayer
        """
# end instance
# instance_bound_VideoNode: rdfl
    @property
    def rdfl(self) -> _Plugin_rdfl_VideoNode_Bound:
        """
        ReduceFlicker for VapourSynth ver. 0.0.0
        """
# end instance
# instance_bound_VideoNode: rdvs
    @property
    def rdvs(self) -> _Plugin_rdvs_VideoNode_Bound:
        """
        RemoveDirt VapourSynth Port
        """
# end instance
# instance_bound_VideoNode: reduceflicker
    @property
    def reduceflicker(self) -> _Plugin_reduceflicker_VideoNode_Bound:
        """
        ReduceFlicker rev-
        """
# end instance
# instance_bound_VideoNode: remap
    @property
    def remap(self) -> _Plugin_remap_VideoNode_Bound:
        """
        Remaps frame indices based on a file/string
        """
# end instance
# instance_bound_VideoNode: resize
    @property
    def resize(self) -> _Plugin_resize_VideoNode_Bound:
        """
        VapourSynth Resize
        """
# end instance
# instance_bound_VideoNode: retinex
    @property
    def retinex(self) -> _Plugin_retinex_VideoNode_Bound:
        """
        Implementation of Retinex algorithm for VapourSynth.
        """
# end instance
# instance_bound_VideoNode: rf
    @property
    def rf(self) -> _Plugin_rf_VideoNode_Bound:
        """
        VapourSynth Replace Frames Tool
        """
# end instance
# instance_bound_VideoNode: rgsf
    @property
    def rgsf(self) -> _Plugin_rgsf_VideoNode_Bound:
        """
        RemoveGrain Single Precision
        """
# end instance
# instance_bound_VideoNode: rgvs
    @property
    def rgvs(self) -> _Plugin_rgvs_VideoNode_Bound:
        """
        RemoveGrain VapourSynth Port
        """
# end instance
# instance_bound_VideoNode: rife
    @property
    def rife(self) -> _Plugin_rife_VideoNode_Bound:
        """
        Real-Time Intermediate Flow Estimation for Video Frame Interpolation
        """
# end instance
# instance_bound_VideoNode: rsnv
    @property
    def rsnv(self) -> _Plugin_rsnv_VideoNode_Bound:
        """
        RealSR ncnn Vulkan plugin
        """
# end instance
# instance_bound_VideoNode: sangnom
    @property
    def sangnom(self) -> _Plugin_sangnom_VideoNode_Bound:
        """
        VapourSynth Single Field Deinterlacer
        """
# end instance
# instance_bound_VideoNode: scd
    @property
    def scd(self) -> _Plugin_scd_VideoNode_Bound:
        """
        Scene change detect filter for VapourSynth v0.2.0
        """
# end instance
# instance_bound_VideoNode: scrawl
    @property
    def scrawl(self) -> _Plugin_scrawl_VideoNode_Bound:
        """
        Simple text output plugin for VapourSynth
        """
# end instance
# instance_bound_VideoNode: scxvid
    @property
    def scxvid(self) -> _Plugin_scxvid_VideoNode_Bound:
        """
        VapourSynth Scxvid Plugin
        """
# end instance
# instance_bound_VideoNode: smoothuv
    @property
    def smoothuv(self) -> _Plugin_smoothuv_VideoNode_Bound:
        """
        SmoothUV is a spatial derainbow filter
        """
# end instance
# instance_bound_VideoNode: srmdnv
    @property
    def srmdnv(self) -> _Plugin_srmdnv_VideoNode_Bound:
        """
        SRMD ncnn Vulkan plugin
        """
# end instance
# instance_bound_VideoNode: ssiq
    @property
    def ssiq(self) -> _Plugin_ssiq_VideoNode_Bound:
        """
        SSIQ plugin for VapourSynth
        """
# end instance
# instance_bound_VideoNode: std
    @property
    def std(self) -> _Plugin_std_VideoNode_Bound:
        """
        VapourSynth Core Functions
        """
# end instance
# instance_bound_VideoNode: sub
    @property
    def sub(self) -> _Plugin_sub_VideoNode_Bound:
        """
        A subtitling filter based on libass and FFmpeg.
        """
# end instance
# instance_bound_VideoNode: surfaceblur
    @property
    def surfaceblur(self) -> _Plugin_surfaceblur_VideoNode_Bound:
        """
        surface blur
        """
# end instance
# instance_bound_VideoNode: svp1
    @property
    def svp1(self) -> _Plugin_svp1_VideoNode_Bound:
        """
        SVPFlow1
        """
# end instance
# instance_bound_VideoNode: svp2
    @property
    def svp2(self) -> _Plugin_svp2_VideoNode_Bound:
        """
        SVPFlow2
        """
# end instance
# instance_bound_VideoNode: tbilateral
    @property
    def tbilateral(self) -> _Plugin_tbilateral_VideoNode_Bound:
        """
        Bilateral spatial denoising filter
        """
# end instance
# instance_bound_VideoNode: tcanny
    @property
    def tcanny(self) -> _Plugin_tcanny_VideoNode_Bound:
        """
        Build an edge map using canny edge detection
        """
# end instance
# instance_bound_VideoNode: tcax
    @property
    def tcax(self) -> _Plugin_tcax_VideoNode_Bound:
        """
        VapourSynth TCAS Filter
        """
# end instance
# instance_bound_VideoNode: tcm
    @property
    def tcm(self) -> _Plugin_tcm_VideoNode_Bound:
        """
        TColorMask plugin for VapourSynth.
        """
# end instance
# instance_bound_VideoNode: tcomb
    @property
    def tcomb(self) -> _Plugin_tcomb_VideoNode_Bound:
        """
        Dotcrawl and rainbow remover
        """
# end instance
# instance_bound_VideoNode: tdm
    @property
    def tdm(self) -> _Plugin_tdm_VideoNode_Bound:
        """
        A bi-directionally motion adaptive deinterlacer
        """
# end instance
# instance_bound_VideoNode: tedgemask
    @property
    def tedgemask(self) -> _Plugin_tedgemask_VideoNode_Bound:
        """
        Edge detection plugin
        """
# end instance
# instance_bound_VideoNode: text
    @property
    def text(self) -> _Plugin_text_VideoNode_Bound:
        """
        VapourSynth Text
        """
# end instance
# instance_bound_VideoNode: timecube
    @property
    def timecube(self) -> _Plugin_timecube_VideoNode_Bound:
        """
        TimeCube 4D
        """
# end instance
# instance_bound_VideoNode: tivtc
    @property
    def tivtc(self) -> _Plugin_tivtc_VideoNode_Bound:
        """
        Field matching and decimation
        """
# end instance
# instance_bound_VideoNode: tla
    @property
    def tla(self) -> _Plugin_tla_VideoNode_Bound:
        """
        VapourSynth Temporal Linear Approximation plugin
        """
# end instance
# instance_bound_VideoNode: tmap
    @property
    def tmap(self) -> _Plugin_tmap_VideoNode_Bound:
        """
        Hable Tonemapping
        """
# end instance
# instance_bound_VideoNode: tmc
    @property
    def tmc(self) -> _Plugin_tmc_VideoNode_Bound:
        """
        A really simple mask cleaning plugin for VapourSynth based on mt_hysteresis.
        """
# end instance
# instance_bound_VideoNode: tmedian
    @property
    def tmedian(self) -> _Plugin_tmedian_VideoNode_Bound:
        """
        Calculates temporal median
        """
# end instance
# instance_bound_VideoNode: tnlm
    @property
    def tnlm(self) -> _Plugin_tnlm_VideoNode_Bound:
        """
        TNLMeans rev39-22a40af
        """
# end instance
# instance_bound_VideoNode: tonemap
    @property
    def tonemap(self) -> _Plugin_tonemap_VideoNode_Bound:
        """
        Simple tone mapping for VapourSynth
        """
# end instance
# instance_bound_VideoNode: trans
    @property
    def trans(self) -> _Plugin_trans_VideoNode_Bound:
        """
        VapourSynth transition plugin
        """
# end instance
# instance_bound_VideoNode: trt
    @property
    def trt(self) -> _Plugin_trt_VideoNode_Bound:
        """
        TensorRT ML Filter Runtime
        """
# end instance
# instance_bound_VideoNode: ttmpsm
    @property
    def ttmpsm(self) -> _Plugin_ttmpsm_VideoNode_Bound:
        """
        A basic, motion adaptive, temporal smoothing filter
        """
# end instance
# instance_bound_VideoNode: vcfreq
    @property
    def vcfreq(self) -> _Plugin_vcfreq_VideoNode_Bound:
        """
        VapourSynth  Frequency Domain Filters
        """
# end instance
# instance_bound_VideoNode: vcm
    @property
    def vcm(self) -> _Plugin_vcm_VideoNode_Bound:
        """
        VapourSynth Plugin by vcmohan 
        """
# end instance
# instance_bound_VideoNode: vcmod
    @property
    def vcmod(self) -> _Plugin_vcmod_VideoNode_Bound:
        """
        VapourSynth Pixel Amplitude modification 
        """
# end instance
# instance_bound_VideoNode: vcmove
    @property
    def vcmove(self) -> _Plugin_vcmove_VideoNode_Bound:
        """
        VapourSynth pixel repositioning Plugin
        """
# end instance
# instance_bound_VideoNode: vd
    @property
    def vd(self) -> _Plugin_vd_VideoNode_Bound:
        """
        A wavelet based denoiser
        """
# end instance
# instance_bound_VideoNode: vfrtocfr
    @property
    def vfrtocfr(self) -> _Plugin_vfrtocfr_VideoNode_Bound:
        """
        VFR to CFR Video Converter
        """
# end instance
# instance_bound_VideoNode: vivtc
    @property
    def vivtc(self) -> _Plugin_vivtc_VideoNode_Bound:
        """
        VFM
        """
# end instance
# instance_bound_VideoNode: vmaf
    @property
    def vmaf(self) -> _Plugin_vmaf_VideoNode_Bound:
        """
        Video Multi-Method Assessment Fusion
        """
# end instance
# instance_bound_VideoNode: vscope
    @property
    def vscope(self) -> _Plugin_vscope_VideoNode_Bound:
        """
        Videoscope plugin for VapourSynth
        """
# end instance
# instance_bound_VideoNode: vsf
    @property
    def vsf(self) -> _Plugin_vsf_VideoNode_Bound:
        """
        VSFilter
        """
# end instance
# instance_bound_VideoNode: vsfm
    @property
    def vsfm(self) -> _Plugin_vsfm_VideoNode_Bound:
        """
        VSFilterMod
        """
# end instance
# instance_bound_VideoNode: w2xc
    @property
    def w2xc(self) -> _Plugin_w2xc_VideoNode_Bound:
        """
        Image Super-Resolution using Deep Convolutional Neural Networks
        """
# end instance
# instance_bound_VideoNode: w2xnvk
    @property
    def w2xnvk(self) -> _Plugin_w2xnvk_VideoNode_Bound:
        """
        VapourSynth Waifu2x NCNN Vulkan Plugin
        """
# end instance
# instance_bound_VideoNode: w3fdif
    @property
    def w3fdif(self) -> _Plugin_w3fdif_VideoNode_Bound:
        """
        Weston 3 Field Deinterlacing Filter
        """
# end instance
# instance_bound_VideoNode: waifu2x
    @property
    def waifu2x(self) -> _Plugin_waifu2x_VideoNode_Bound:
        """
        Waifu2x-opt image restoration filter for VapourSynth.
        """
# end instance
# instance_bound_VideoNode: warp
    @property
    def warp(self) -> _Plugin_warp_VideoNode_Bound:
        """
        Sharpen images by warping
        """
# end instance
# instance_bound_VideoNode: warpsf
    @property
    def warpsf(self) -> _Plugin_warpsf_VideoNode_Bound:
        """
        Warpsharp floating point version
        """
# end instance
# instance_bound_VideoNode: wwxd
    @property
    def wwxd(self) -> _Plugin_wwxd_VideoNode_Bound:
        """
        Scene change detection approximately like Xvid's
        """
# end instance
# instance_bound_VideoNode: xyvsf
    @property
    def xyvsf(self) -> _Plugin_xyvsf_VideoNode_Bound:
        """
        xy-VSFilter
        """
# end instance
# instance_bound_VideoNode: yadifmod
    @property
    def yadifmod(self) -> _Plugin_yadifmod_VideoNode_Bound:
        """
        Modification of Fizick's yadif avisynth filter
        """
# end instance
# instance_bound_VideoNode: znedi3
    @property
    def znedi3(self) -> _Plugin_znedi3_VideoNode_Bound:
        """
        Neural network edge directed interpolation (3rd gen.)
        """
# end instance

    format: typing.Optional[VideoFormat]

    fps: fractions.Fraction
    fps_den: int
    fps_num: int

    height: int
    width: int

    num_frames: int

    # RawNode methods
    @typing.overload
    def get_frame_async_raw(self, n: int, cb: typing.Callable[['VideoNode', int, VideoFrame], None]) -> None: ...
    @typing.overload
    def get_frame_async_raw(self, n: int, cb: _Future[VideoFrame], future_wrapper: typing.Optional[typing.Callable[..., None]] = None) -> _Future[VideoFrame]: ...
    def get_frame_async(self, n: int) -> _Future[VideoFrame]: ...
    def frames(self, prefetch: typing.Optional[int] = None, backlog: typing.Optional[int] = None, close: bool = False) -> typing.Iterator[VideoFrame]: ...

    def get_frame(self, n: int) -> VideoFrame: ...
    def set_output(self, index: int = 0, alpha: typing.Optional['VideoNode'] = None, alt_output: int = 0) -> None: ...
    def output(self, fileobj: typing.BinaryIO, y4m: bool = False, progress_update: typing.Optional[typing.Callable[[int, int], None]] = None, prefetch: int = 0, backlog: int = -1) -> None: ...

    def __add__(self, other: 'VideoNode') -> 'VideoNode': ...
    def __radd__(self, other: 'VideoNode') -> 'VideoNode': ...
    def __mul__(self, other: int) -> 'VideoNode': ...
    def __rmul__(self, other: int) -> 'VideoNode': ...
    def __getitem__(self, other: typing.Union[int, slice]) -> 'VideoNode': ...
    def __len__(self) -> int: ...


class AudioFrame(_RawFrame):
    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    channel_layout: int
    num_channels: int

    def copy(self) -> 'AudioFrame': ...

    def __enter__(self) -> 'AudioFrame': ...

    def __getitem__(self, index: int) -> memoryview: ...
    def __len__(self) -> int: ...


class AudioNode:
# instance_bound_AudioNode: std
    @property
    def std(self) -> _Plugin_std_AudioNode_Bound:
        """
        VapourSynth Core Functions
        """
# end instance

    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    channel_layout: int
    num_channels: int
    sample_rate: int
    num_samples: int

    num_frames: int

    # RawNode methods
    @typing.overload
    def get_frame_async_raw(self, n: int, cb: typing.Callable[['AudioNode', int, AudioFrame], None]) -> None: ...
    @typing.overload
    def get_frame_async_raw(self, n: int, cb: _Future[AudioFrame], future_wrapper: typing.Optional[typing.Callable[..., None]] = None) -> _Future[AudioFrame]: ...
    def get_frame_async(self, n: int) -> _Future[AudioFrame]: ...
    def frames(self, prefetch: typing.Optional[int] = None, backlog: typing.Optional[int] = None, close: bool = False) -> typing.Iterator[AudioFrame]: ...

    def get_frame(self, n: int) -> AudioFrame: ...
    def set_output(self, index: int = 0) -> None: ...

    def __add__(self, other: 'AudioNode') -> 'AudioNode': ...
    def __radd__(self, other: 'AudioNode') -> 'AudioNode': ...
    def __mul__(self, other: int) -> 'AudioNode': ...
    def __rmul__(self, other: int) -> 'AudioNode': ...
    def __getitem__(self, other: typing.Union[int, slice]) -> 'AudioNode': ...
    def __len__(self) -> int: ...


class _PluginMeta(typing.TypedDict):
    namespace: str
    identifier: str
    name: str
    functions: typing.Dict[str, str]


class LogHandle:
    handler_func: typing.Callable[[MessageType, str], None]


class Core:
# instance_bound_Core: DGMVC
    @property
    def DGMVC(self) -> _Plugin_DGMVC_Core_Bound:
        """
        DGMVCSource for VapourSynth
        """
# end instance
# instance_bound_Core: acrop
    @property
    def acrop(self) -> _Plugin_acrop_Core_Bound:
        """
        VapourSynth Auto Crop
        """
# end instance
# instance_bound_Core: adg
    @property
    def adg(self) -> _Plugin_adg_Core_Bound:
        """
        Adaptive grain
        """
# end instance
# instance_bound_Core: akarin
    @property
    def akarin(self) -> _Plugin_akarin_Core_Bound:
        """
        Akarin's Experimental Filters
        """
# end instance
# instance_bound_Core: anime4kcpp
    @property
    def anime4kcpp(self) -> _Plugin_anime4kcpp_Core_Bound:
        """
        Anime4KCPP for VapourSynth
        """
# end instance
# instance_bound_Core: area
    @property
    def area(self) -> _Plugin_area_Core_Bound:
        """
        area average downscaler plugin
        """
# end instance
# instance_bound_Core: asharp
    @property
    def asharp(self) -> _Plugin_asharp_Core_Bound:
        """
        adaptive sharpening filter
        """
# end instance
# instance_bound_Core: assrender
    @property
    def assrender(self) -> _Plugin_assrender_Core_Bound:
        """
        AssRender
        """
# end instance
# instance_bound_Core: average
    @property
    def average(self) -> _Plugin_average_Core_Bound:
        """
        vs-average
        """
# end instance
# instance_bound_Core: avs
    @property
    def avs(self) -> _Plugin_avs_Core_Bound:
        """
        VapourSynth Avisynth Compatibility
        """
# end instance
# instance_bound_Core: avsr
    @property
    def avsr(self) -> _Plugin_avsr_Core_Bound:
        """
        AviSynth Script Reader for VapourSynth v1.0.0
        """
# end instance
# instance_bound_Core: avsw
    @property
    def avsw(self) -> _Plugin_avsw_Core_Bound:
        """
        avsproxy
        """
# end instance
# instance_bound_Core: bas
    @property
    def bas(self) -> _Plugin_bas_Core_Bound:
        """
        Best Audio Source
        """
# end instance
# instance_bound_Core: bezier
    @property
    def bezier(self) -> _Plugin_bezier_Core_Bound:
        """
        vapoursynth bezier curve test
        """
# end instance
# instance_bound_Core: bifrost
    @property
    def bifrost(self) -> _Plugin_bifrost_Core_Bound:
        """
        Bifrost plugin for VapourSynth
        """
# end instance
# instance_bound_Core: bilateral
    @property
    def bilateral(self) -> _Plugin_bilateral_Core_Bound:
        """
        Bilateral filter and Gaussian filter for VapourSynth.
        """
# end instance
# instance_bound_Core: bilateralgpu
    @property
    def bilateralgpu(self) -> _Plugin_bilateralgpu_Core_Bound:
        """
        Bilateral filter using CUDA
        """
# end instance
# instance_bound_Core: bm3d
    @property
    def bm3d(self) -> _Plugin_bm3d_Core_Bound:
        """
        Implementation of BM3D denoising filter for VapourSynth.
        """
# end instance
# instance_bound_Core: bm3dcpu
    @property
    def bm3dcpu(self) -> _Plugin_bm3dcpu_Core_Bound:
        """
        BM3D algorithm implemented in AVX and AVX2 intrinsics
        """
# end instance
# instance_bound_Core: bm3dcuda
    @property
    def bm3dcuda(self) -> _Plugin_bm3dcuda_Core_Bound:
        """
        BM3D algorithm implemented in CUDA
        """
# end instance
# instance_bound_Core: bm3dcuda_rtc
    @property
    def bm3dcuda_rtc(self) -> _Plugin_bm3dcuda_rtc_Core_Bound:
        """
        BM3D algorithm implemented in CUDA (NVRTC)
        """
# end instance
# instance_bound_Core: box
    @property
    def box(self) -> _Plugin_box_Core_Bound:
        """
        AVX2-optimized boxfilter
        """
# end instance
# instance_bound_Core: butteraugli
    @property
    def butteraugli(self) -> _Plugin_butteraugli_Core_Bound:
        """
        modified version of Google's butteraugli
        """
# end instance
# instance_bound_Core: bwdif
    @property
    def bwdif(self) -> _Plugin_bwdif_Core_Bound:
        """
        BobWeaver Deinterlacing Filter
        """
# end instance
# instance_bound_Core: caffe
    @property
    def caffe(self) -> _Plugin_caffe_Core_Bound:
        """
        Image Super-Resolution using Deep Convolutional Neural Networks
        """
# end instance
# instance_bound_Core: cas
    @property
    def cas(self) -> _Plugin_cas_Core_Bound:
        """
        Contrast Adaptive Sharpening
        """
# end instance
# instance_bound_Core: ccd
    @property
    def ccd(self) -> _Plugin_ccd_Core_Bound:
        """
        chroma denoiser
        """
# end instance
# instance_bound_Core: cf
    @property
    def cf(self) -> _Plugin_cf_Core_Bound:
        """
        VapourSynth ContinuityFixer port
        """
# end instance
# instance_bound_Core: chkdr
    @property
    def chkdr(self) -> _Plugin_chkdr_Core_Bound:
        """
        Film grain generator
        """
# end instance
# instance_bound_Core: cnr2
    @property
    def cnr2(self) -> _Plugin_cnr2_Core_Bound:
        """
        Chroma noise reducer
        """
# end instance
# instance_bound_Core: colorbars
    @property
    def colorbars(self) -> _Plugin_colorbars_Core_Bound:
        """
        SMPTE RP 219-2:2016 and ITU-BT.2111 color bar generator for VapourSynth
        """
# end instance
# instance_bound_Core: comb
    @property
    def comb(self) -> _Plugin_comb_Core_Bound:
        """
        comb filters v0.0.1
        """
# end instance
# instance_bound_Core: ctmf
    @property
    def ctmf(self) -> _Plugin_ctmf_Core_Bound:
        """
        Constant Time Median Filtering
        """
# end instance
# instance_bound_Core: curve
    @property
    def curve(self) -> _Plugin_curve_Core_Bound:
        """
        Apply color adjustments using curves
        """
# end instance
# instance_bound_Core: d2v
    @property
    def d2v(self) -> _Plugin_d2v_Core_Bound:
        """
        D2V Source
        """
# end instance
# instance_bound_Core: damb
    @property
    def damb(self) -> _Plugin_damb_Core_Bound:
        """
        Audio file reader and writer
        """
# end instance
# instance_bound_Core: dct
    @property
    def dct(self) -> _Plugin_dct_Core_Bound:
        """
        DCT filtering plugin rev10-b311e2e
        """
# end instance
# instance_bound_Core: dctf
    @property
    def dctf(self) -> _Plugin_dctf_Core_Bound:
        """
        DCT/IDCT Frequency Suppressor
        """
# end instance
# instance_bound_Core: deblock
    @property
    def deblock(self) -> _Plugin_deblock_Core_Bound:
        """
        It does a deblocking of the picture, using the deblocking filter of h264
        """
# end instance
# instance_bound_Core: decross
    @property
    def decross(self) -> _Plugin_decross_Core_Bound:
        """
        Spatio-temporal derainbow filter
        """
# end instance
# instance_bound_Core: dedot
    @property
    def dedot(self) -> _Plugin_dedot_Core_Bound:
        """
        Temporal dotcrawl and rainbow remover
        """
# end instance
# instance_bound_Core: delogo
    @property
    def delogo(self) -> _Plugin_delogo_Core_Bound:
        """
        VapourSynth Delogo Filter v005a.0.4
        """
# end instance
# instance_bound_Core: delogohd
    @property
    def delogohd(self) -> _Plugin_delogohd_Core_Bound:
        """
        VapourSynth DelogoHD Filter r12
        """
# end instance
# instance_bound_Core: depan
    @property
    def depan(self) -> _Plugin_depan_Core_Bound:
        """
        Tools for estimation and compensation of global motion (pan)
        """
# end instance
# instance_bound_Core: descale
    @property
    def descale(self) -> _Plugin_descale_Core_Bound:
        """
        Undo linear interpolation
        """
# end instance
# instance_bound_Core: descale_getnative
    @property
    def descale_getnative(self) -> _Plugin_descale_getnative_Core_Bound:
        """
        Undo linear interpolation
        """
# end instance
# instance_bound_Core: dfttest
    @property
    def dfttest(self) -> _Plugin_dfttest_Core_Bound:
        """
        2D/3D frequency domain denoiser
        """
# end instance
# instance_bound_Core: dgdecodenv
    @property
    def dgdecodenv(self) -> _Plugin_dgdecodenv_Core_Bound:
        """
        DGDecodeNV for VapourSynth
        """
# end instance
# instance_bound_Core: dghdrtosdr
    @property
    def dghdrtosdr(self) -> _Plugin_dghdrtosdr_Core_Bound:
        """
        Convert HDR to SDR
        """
# end instance
# instance_bound_Core: dgm
    @property
    def dgm(self) -> _Plugin_dgm_Core_Bound:
        """
        Spatio-temporal limited median denoiser
        """
# end instance
# instance_bound_Core: dotkill
    @property
    def dotkill(self) -> _Plugin_dotkill_Core_Bound:
        """
        VapourSynth DotKill
        """
# end instance
# instance_bound_Core: dpid
    @property
    def dpid(self) -> _Plugin_dpid_Core_Bound:
        """
        Rapid, Detail-Preserving Image Downscaling
        """
# end instance
# instance_bound_Core: draw
    @property
    def draw(self) -> _Plugin_draw_Core_Bound:
        """
        a simple alternative to Masktools2's mt_lutspa
        """
# end instance
# instance_bound_Core: edgefixer
    @property
    def edgefixer(self) -> _Plugin_edgefixer_Core_Bound:
        """
        ultraman
        """
# end instance
# instance_bound_Core: eedi2
    @property
    def eedi2(self) -> _Plugin_eedi2_Core_Bound:
        """
        EEDI2
        """
# end instance
# instance_bound_Core: eedi2cuda
    @property
    def eedi2cuda(self) -> _Plugin_eedi2cuda_Core_Bound:
        """
        EEDI2 filter using CUDA
        """
# end instance
# instance_bound_Core: eedi3m
    @property
    def eedi3m(self) -> _Plugin_eedi3m_Core_Bound:
        """
        Enhanced Edge Directed Interpolation 3
        """
# end instance
# instance_bound_Core: f3kdb
    @property
    def f3kdb(self) -> _Plugin_f3kdb_Core_Bound:
        """
        flash3kyuu_deband
        """
# end instance
# instance_bound_Core: fb
    @property
    def fb(self) -> _Plugin_fb_Core_Bound:
        """
        FillBorders plugin for VapourSynth
        """
# end instance
# instance_bound_Core: ffms2
    @property
    def ffms2(self) -> _Plugin_ffms2_Core_Bound:
        """
        FFmpegSource 2 for VapourSynth
        """
# end instance
# instance_bound_Core: fft3dfilter
    @property
    def fft3dfilter(self) -> _Plugin_fft3dfilter_Core_Bound:
        """
        systems
        """
# end instance
# instance_bound_Core: fftspectrum
    @property
    def fftspectrum(self) -> _Plugin_fftspectrum_Core_Bound:
        """
        FFT Spectrum plugin
        """
# end instance
# instance_bound_Core: fh
    @property
    def fh(self) -> _Plugin_fh_Core_Bound:
        """
        FieldHint Plugin
        """
# end instance
# instance_bound_Core: flux
    @property
    def flux(self) -> _Plugin_flux_Core_Bound:
        """
        FluxSmooth plugin for VapourSynth
        """
# end instance
# instance_bound_Core: fmtc
    @property
    def fmtc(self) -> _Plugin_fmtc_Core_Bound:
        """
        Format converter
        """
# end instance
# instance_bound_Core: focus
    @property
    def focus(self) -> _Plugin_focus_Core_Bound:
        """
        VapourSynth Pixel Restoration Filters
        """
# end instance
# instance_bound_Core: focus2
    @property
    def focus2(self) -> _Plugin_focus2_Core_Bound:
        """
        VapourSynth TemporalSoften Filter v1
        """
# end instance
# instance_bound_Core: ftf
    @property
    def ftf(self) -> _Plugin_ftf_Core_Bound:
        """
        Fix Telecined Fades
        """
# end instance
# instance_bound_Core: grad
    @property
    def grad(self) -> _Plugin_grad_Core_Bound:
        """
        Adjustment of contrast, brightness, gamma and a wide range of color manipulations through gradation curves is possible.
        """
# end instance
# instance_bound_Core: grain
    @property
    def grain(self) -> _Plugin_grain_Core_Bound:
        """
        Random noise film grain generator
        """
# end instance
# instance_bound_Core: hist
    @property
    def hist(self) -> _Plugin_hist_Core_Bound:
        """
        VapourSynth Histogram Plugin
        """
# end instance
# instance_bound_Core: hqdn3d
    @property
    def hqdn3d(self) -> _Plugin_hqdn3d_Core_Bound:
        """
        HQDn3D port as used in avisynth/mplayer
        """
# end instance
# instance_bound_Core: iccc
    @property
    def iccc(self) -> _Plugin_iccc_Core_Bound:
        """
        ICC Conversion
        """
# end instance
# instance_bound_Core: imwri
    @property
    def imwri(self) -> _Plugin_imwri_Core_Bound:
        """
        VapourSynth ImageMagick 7 HDRI Writer/Reader
        """
# end instance
# instance_bound_Core: it
    @property
    def it(self) -> _Plugin_it_Core_Bound:
        """
        VapourSynth IVTC Filter v0103.1.1
        """
# end instance
# instance_bound_Core: jinc
    @property
    def jinc(self) -> _Plugin_jinc_Core_Bound:
        """
        VapourSynth EWA resampling
        """
# end instance
# instance_bound_Core: knlm
    @property
    def knlm(self) -> _Plugin_knlm_Core_Bound:
        """
        KNLMeansCL for VapourSynth
        """
# end instance
# instance_bound_Core: lghost
    @property
    def lghost(self) -> _Plugin_lghost_Core_Bound:
        """
        Ghost Reduction
        """
# end instance
# instance_bound_Core: libp2p
    @property
    def libp2p(self) -> _Plugin_libp2p_Core_Bound:
        """
        libp2p rgb formats packer/unpacker
        """
# end instance
# instance_bound_Core: lsmas
    @property
    def lsmas(self) -> _Plugin_lsmas_Core_Bound:
        """
        LSMASHSource for VapourSynth
        """
# end instance
# instance_bound_Core: matchhist
    @property
    def matchhist(self) -> _Plugin_matchhist_Core_Bound:
        """
        MatchHistogram
        """
# end instance
# instance_bound_Core: median
    @property
    def median(self) -> _Plugin_median_Core_Bound:
        """
        Median of clips
        """
# end instance
# instance_bound_Core: minideen
    @property
    def minideen(self) -> _Plugin_minideen_Core_Bound:
        """
        Spatial convolution with thresholds
        """
# end instance
# instance_bound_Core: minsrp
    @property
    def minsrp(self) -> _Plugin_minsrp_Core_Bound:
        """
        VapourSynth MinSRP Filter
        """
# end instance
# instance_bound_Core: misc
    @property
    def misc(self) -> _Plugin_misc_Core_Bound:
        """
        Miscellaneous filters
        """
# end instance
# instance_bound_Core: morpho
    @property
    def morpho(self) -> _Plugin_morpho_Core_Bound:
        """
        Simple morphological filters.
        """
# end instance
# instance_bound_Core: motionmask
    @property
    def motionmask(self) -> _Plugin_motionmask_Core_Bound:
        """
        MotionMask creates a mask of moving pixels
        """
# end instance
# instance_bound_Core: mpeg2stinx
    @property
    def mpeg2stinx(self) -> _Plugin_mpeg2stinx_Core_Bound:
        """
        Mpeg2Stinx
        """
# end instance
# instance_bound_Core: mpls
    @property
    def mpls(self) -> _Plugin_mpls_Core_Bound:
        """
        Get m2ts clip id from a playlist and return a dict
        """
# end instance
# instance_bound_Core: msmoosh
    @property
    def msmoosh(self) -> _Plugin_msmoosh_Core_Bound:
        """
        MSmooth and MSharpen
        """
# end instance
# instance_bound_Core: mv
    @property
    def mv(self) -> _Plugin_mv_Core_Bound:
        """
        MVTools v23
        """
# end instance
# instance_bound_Core: mvsf
    @property
    def mvsf(self) -> _Plugin_mvsf_Core_Bound:
        """
        MVTools Single Precision
        """
# end instance
# instance_bound_Core: neo_dfttest
    @property
    def neo_dfttest(self) -> _Plugin_neo_dfttest_Core_Bound:
        """
        Neo DFTTest Deband Filter r7 - 2D/3D frequency domain denoiser
        """
# end instance
# instance_bound_Core: neo_f3kdb
    @property
    def neo_f3kdb(self) -> _Plugin_neo_f3kdb_Core_Bound:
        """
        Neo F3KDB Deband Filter r7
        """
# end instance
# instance_bound_Core: neo_fft3d
    @property
    def neo_fft3d(self) -> _Plugin_neo_fft3d_Core_Bound:
        """
        Neo FFT3D Filter r11
        """
# end instance
# instance_bound_Core: neo_minideen
    @property
    def neo_minideen(self) -> _Plugin_neo_minideen_Core_Bound:
        """
        Neo Minideen Filter r11
        """
# end instance
# instance_bound_Core: neo_tmedian
    @property
    def neo_tmedian(self) -> _Plugin_neo_tmedian_Core_Bound:
        """
        Neo Temporal Median Filter r2
        """
# end instance
# instance_bound_Core: neo_vd
    @property
    def neo_vd(self) -> _Plugin_neo_vd_Core_Bound:
        """
        Neo Vague Denoiser Filter r2
        """
# end instance
# instance_bound_Core: nnedi3
    @property
    def nnedi3(self) -> _Plugin_nnedi3_Core_Bound:
        """
        Neural network edge directed interpolation (3rd gen.), v12
        """
# end instance
# instance_bound_Core: nnedi3cl
    @property
    def nnedi3cl(self) -> _Plugin_nnedi3cl_Core_Bound:
        """
        An intra-field only deinterlacer
        """
# end instance
# instance_bound_Core: noisegen
    @property
    def noisegen(self) -> _Plugin_noisegen_Core_Bound:
        """
        VapourSynth Noise Generator
        """
# end instance
# instance_bound_Core: ocr
    @property
    def ocr(self) -> _Plugin_ocr_Core_Bound:
        """
        Tesseract OCR Filter
        """
# end instance
# instance_bound_Core: ort
    @property
    def ort(self) -> _Plugin_ort_Core_Bound:
        """
        ONNX Runtime ML Filter Runtime
        """
# end instance
# instance_bound_Core: ov
    @property
    def ov(self) -> _Plugin_ov_Core_Bound:
        """
        OpenVINO ML Filter Runtime
        """
# end instance
# instance_bound_Core: placebo
    @property
    def placebo(self) -> _Plugin_placebo_Core_Bound:
        """
        libplacebo plugin for VapourSynth
        """
# end instance
# instance_bound_Core: pp7
    @property
    def pp7(self) -> _Plugin_pp7_Core_Bound:
        """
        Postprocess 7 from MPlayer
        """
# end instance
# instance_bound_Core: qr
    @property
    def qr(self) -> _Plugin_qr_Core_Bound:
        """
        QR code filter
        """
# end instance
# instance_bound_Core: raws
    @property
    def raws(self) -> _Plugin_raws_Core_Bound:
        """
        Raw-format file Reader for VapourSynth 0.3.5
        """
# end instance
# instance_bound_Core: rdfl
    @property
    def rdfl(self) -> _Plugin_rdfl_Core_Bound:
        """
        ReduceFlicker for VapourSynth ver. 0.0.0
        """
# end instance
# instance_bound_Core: rdvs
    @property
    def rdvs(self) -> _Plugin_rdvs_Core_Bound:
        """
        RemoveDirt VapourSynth Port
        """
# end instance
# instance_bound_Core: reduceflicker
    @property
    def reduceflicker(self) -> _Plugin_reduceflicker_Core_Bound:
        """
        ReduceFlicker rev-
        """
# end instance
# instance_bound_Core: remap
    @property
    def remap(self) -> _Plugin_remap_Core_Bound:
        """
        Remaps frame indices based on a file/string
        """
# end instance
# instance_bound_Core: resize
    @property
    def resize(self) -> _Plugin_resize_Core_Bound:
        """
        VapourSynth Resize
        """
# end instance
# instance_bound_Core: retinex
    @property
    def retinex(self) -> _Plugin_retinex_Core_Bound:
        """
        Implementation of Retinex algorithm for VapourSynth.
        """
# end instance
# instance_bound_Core: rf
    @property
    def rf(self) -> _Plugin_rf_Core_Bound:
        """
        VapourSynth Replace Frames Tool
        """
# end instance
# instance_bound_Core: rgsf
    @property
    def rgsf(self) -> _Plugin_rgsf_Core_Bound:
        """
        RemoveGrain Single Precision
        """
# end instance
# instance_bound_Core: rgvs
    @property
    def rgvs(self) -> _Plugin_rgvs_Core_Bound:
        """
        RemoveGrain VapourSynth Port
        """
# end instance
# instance_bound_Core: rife
    @property
    def rife(self) -> _Plugin_rife_Core_Bound:
        """
        Real-Time Intermediate Flow Estimation for Video Frame Interpolation
        """
# end instance
# instance_bound_Core: rsnv
    @property
    def rsnv(self) -> _Plugin_rsnv_Core_Bound:
        """
        RealSR ncnn Vulkan plugin
        """
# end instance
# instance_bound_Core: sangnom
    @property
    def sangnom(self) -> _Plugin_sangnom_Core_Bound:
        """
        VapourSynth Single Field Deinterlacer
        """
# end instance
# instance_bound_Core: scd
    @property
    def scd(self) -> _Plugin_scd_Core_Bound:
        """
        Scene change detect filter for VapourSynth v0.2.0
        """
# end instance
# instance_bound_Core: scrawl
    @property
    def scrawl(self) -> _Plugin_scrawl_Core_Bound:
        """
        Simple text output plugin for VapourSynth
        """
# end instance
# instance_bound_Core: scxvid
    @property
    def scxvid(self) -> _Plugin_scxvid_Core_Bound:
        """
        VapourSynth Scxvid Plugin
        """
# end instance
# instance_bound_Core: smoothuv
    @property
    def smoothuv(self) -> _Plugin_smoothuv_Core_Bound:
        """
        SmoothUV is a spatial derainbow filter
        """
# end instance
# instance_bound_Core: srmdnv
    @property
    def srmdnv(self) -> _Plugin_srmdnv_Core_Bound:
        """
        SRMD ncnn Vulkan plugin
        """
# end instance
# instance_bound_Core: ssiq
    @property
    def ssiq(self) -> _Plugin_ssiq_Core_Bound:
        """
        SSIQ plugin for VapourSynth
        """
# end instance
# instance_bound_Core: std
    @property
    def std(self) -> _Plugin_std_Core_Bound:
        """
        VapourSynth Core Functions
        """
# end instance
# instance_bound_Core: sub
    @property
    def sub(self) -> _Plugin_sub_Core_Bound:
        """
        A subtitling filter based on libass and FFmpeg.
        """
# end instance
# instance_bound_Core: surfaceblur
    @property
    def surfaceblur(self) -> _Plugin_surfaceblur_Core_Bound:
        """
        surface blur
        """
# end instance
# instance_bound_Core: svp1
    @property
    def svp1(self) -> _Plugin_svp1_Core_Bound:
        """
        SVPFlow1
        """
# end instance
# instance_bound_Core: svp2
    @property
    def svp2(self) -> _Plugin_svp2_Core_Bound:
        """
        SVPFlow2
        """
# end instance
# instance_bound_Core: tbilateral
    @property
    def tbilateral(self) -> _Plugin_tbilateral_Core_Bound:
        """
        Bilateral spatial denoising filter
        """
# end instance
# instance_bound_Core: tcanny
    @property
    def tcanny(self) -> _Plugin_tcanny_Core_Bound:
        """
        Build an edge map using canny edge detection
        """
# end instance
# instance_bound_Core: tcax
    @property
    def tcax(self) -> _Plugin_tcax_Core_Bound:
        """
        VapourSynth TCAS Filter
        """
# end instance
# instance_bound_Core: tcm
    @property
    def tcm(self) -> _Plugin_tcm_Core_Bound:
        """
        TColorMask plugin for VapourSynth.
        """
# end instance
# instance_bound_Core: tcomb
    @property
    def tcomb(self) -> _Plugin_tcomb_Core_Bound:
        """
        Dotcrawl and rainbow remover
        """
# end instance
# instance_bound_Core: tdm
    @property
    def tdm(self) -> _Plugin_tdm_Core_Bound:
        """
        A bi-directionally motion adaptive deinterlacer
        """
# end instance
# instance_bound_Core: tedgemask
    @property
    def tedgemask(self) -> _Plugin_tedgemask_Core_Bound:
        """
        Edge detection plugin
        """
# end instance
# instance_bound_Core: text
    @property
    def text(self) -> _Plugin_text_Core_Bound:
        """
        VapourSynth Text
        """
# end instance
# instance_bound_Core: timecube
    @property
    def timecube(self) -> _Plugin_timecube_Core_Bound:
        """
        TimeCube 4D
        """
# end instance
# instance_bound_Core: tivtc
    @property
    def tivtc(self) -> _Plugin_tivtc_Core_Bound:
        """
        Field matching and decimation
        """
# end instance
# instance_bound_Core: tla
    @property
    def tla(self) -> _Plugin_tla_Core_Bound:
        """
        VapourSynth Temporal Linear Approximation plugin
        """
# end instance
# instance_bound_Core: tmap
    @property
    def tmap(self) -> _Plugin_tmap_Core_Bound:
        """
        Hable Tonemapping
        """
# end instance
# instance_bound_Core: tmc
    @property
    def tmc(self) -> _Plugin_tmc_Core_Bound:
        """
        A really simple mask cleaning plugin for VapourSynth based on mt_hysteresis.
        """
# end instance
# instance_bound_Core: tmedian
    @property
    def tmedian(self) -> _Plugin_tmedian_Core_Bound:
        """
        Calculates temporal median
        """
# end instance
# instance_bound_Core: tnlm
    @property
    def tnlm(self) -> _Plugin_tnlm_Core_Bound:
        """
        TNLMeans rev39-22a40af
        """
# end instance
# instance_bound_Core: tonemap
    @property
    def tonemap(self) -> _Plugin_tonemap_Core_Bound:
        """
        Simple tone mapping for VapourSynth
        """
# end instance
# instance_bound_Core: trans
    @property
    def trans(self) -> _Plugin_trans_Core_Bound:
        """
        VapourSynth transition plugin
        """
# end instance
# instance_bound_Core: trt
    @property
    def trt(self) -> _Plugin_trt_Core_Bound:
        """
        TensorRT ML Filter Runtime
        """
# end instance
# instance_bound_Core: ttmpsm
    @property
    def ttmpsm(self) -> _Plugin_ttmpsm_Core_Bound:
        """
        A basic, motion adaptive, temporal smoothing filter
        """
# end instance
# instance_bound_Core: vcfreq
    @property
    def vcfreq(self) -> _Plugin_vcfreq_Core_Bound:
        """
        VapourSynth  Frequency Domain Filters
        """
# end instance
# instance_bound_Core: vcm
    @property
    def vcm(self) -> _Plugin_vcm_Core_Bound:
        """
        VapourSynth Plugin by vcmohan 
        """
# end instance
# instance_bound_Core: vcmod
    @property
    def vcmod(self) -> _Plugin_vcmod_Core_Bound:
        """
        VapourSynth Pixel Amplitude modification 
        """
# end instance
# instance_bound_Core: vcmove
    @property
    def vcmove(self) -> _Plugin_vcmove_Core_Bound:
        """
        VapourSynth pixel repositioning Plugin
        """
# end instance
# instance_bound_Core: vd
    @property
    def vd(self) -> _Plugin_vd_Core_Bound:
        """
        A wavelet based denoiser
        """
# end instance
# instance_bound_Core: vfrtocfr
    @property
    def vfrtocfr(self) -> _Plugin_vfrtocfr_Core_Bound:
        """
        VFR to CFR Video Converter
        """
# end instance
# instance_bound_Core: vivtc
    @property
    def vivtc(self) -> _Plugin_vivtc_Core_Bound:
        """
        VFM
        """
# end instance
# instance_bound_Core: vmaf
    @property
    def vmaf(self) -> _Plugin_vmaf_Core_Bound:
        """
        Video Multi-Method Assessment Fusion
        """
# end instance
# instance_bound_Core: vscope
    @property
    def vscope(self) -> _Plugin_vscope_Core_Bound:
        """
        Videoscope plugin for VapourSynth
        """
# end instance
# instance_bound_Core: vsf
    @property
    def vsf(self) -> _Plugin_vsf_Core_Bound:
        """
        VSFilter
        """
# end instance
# instance_bound_Core: vsfm
    @property
    def vsfm(self) -> _Plugin_vsfm_Core_Bound:
        """
        VSFilterMod
        """
# end instance
# instance_bound_Core: w2xc
    @property
    def w2xc(self) -> _Plugin_w2xc_Core_Bound:
        """
        Image Super-Resolution using Deep Convolutional Neural Networks
        """
# end instance
# instance_bound_Core: w2xnvk
    @property
    def w2xnvk(self) -> _Plugin_w2xnvk_Core_Bound:
        """
        VapourSynth Waifu2x NCNN Vulkan Plugin
        """
# end instance
# instance_bound_Core: w3fdif
    @property
    def w3fdif(self) -> _Plugin_w3fdif_Core_Bound:
        """
        Weston 3 Field Deinterlacing Filter
        """
# end instance
# instance_bound_Core: waifu2x
    @property
    def waifu2x(self) -> _Plugin_waifu2x_Core_Bound:
        """
        Waifu2x-opt image restoration filter for VapourSynth.
        """
# end instance
# instance_bound_Core: warp
    @property
    def warp(self) -> _Plugin_warp_Core_Bound:
        """
        Sharpen images by warping
        """
# end instance
# instance_bound_Core: warpsf
    @property
    def warpsf(self) -> _Plugin_warpsf_Core_Bound:
        """
        Warpsharp floating point version
        """
# end instance
# instance_bound_Core: wwxd
    @property
    def wwxd(self) -> _Plugin_wwxd_Core_Bound:
        """
        Scene change detection approximately like Xvid's
        """
# end instance
# instance_bound_Core: xyvsf
    @property
    def xyvsf(self) -> _Plugin_xyvsf_Core_Bound:
        """
        xy-VSFilter
        """
# end instance
# instance_bound_Core: yadifmod
    @property
    def yadifmod(self) -> _Plugin_yadifmod_Core_Bound:
        """
        Modification of Fizick's yadif avisynth filter
        """
# end instance
# instance_bound_Core: znedi3
    @property
    def znedi3(self) -> _Plugin_znedi3_Core_Bound:
        """
        Neural network edge directed interpolation (3rd gen.)
        """
# end instance

    @property
    def num_threads(self) -> int: ...
    @num_threads.setter
    def num_threads(self) -> None: ...
    @property
    def max_cache_size(self) -> int: ...
    @max_cache_size.setter
    def max_cache_size(self) -> None: ...

    def plugins(self) -> typing.Iterator[Plugin]: ...
    # get_plugins is deprecated
    def get_plugins(self) -> typing.Dict[str, _PluginMeta]: ...
    # list_functions is deprecated
    def list_functions(self) -> str: ...

    def query_video_format(self, color_family: ColorFamily, sample_type: SampleType, bits_per_sample: int, subsampling_w: int = 0, subsampling_h: int = 0) -> VideoFormat: ...
    # register_format is deprecated
    def register_format(self, color_family: ColorFamily, sample_type: SampleType, bits_per_sample: int, subsampling_w: int, subsampling_h: int) -> VideoFormat: ...
    def get_video_format(self, id: typing.Union[VideoFormat, int, PresetFormat]) -> VideoFormat: ...
    # get_format is deprecated
    def get_format(self, id: typing.Union[VideoFormat, int, PresetFormat]) -> VideoFormat: ...
    def log_message(self, message_type: MessageType, message: str) -> None: ...
    def add_log_handler(self, handler_func: typing.Optional[typing.Callable[[MessageType, str], None]]) -> LogHandle: ...
    def remove_log_handler(self, handle: LogHandle) -> None: ...

    def version(self) -> str: ...
    def version_number(self) -> int: ...


class _CoreProxy(Core):
    @property
    def core(self) -> Core: ...


core: _CoreProxy
