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
import fractions
import types
import typing

T = typing.TypeVar("T")
_NOT_GIVEN = []
SingleAndSequence = typing.Union[T, typing.Sequence[T]]


###
# ENUMS AND CONSTANTS
class ColorFamily(int):
    name: str
    value: int

    RGB: typing.ClassVar['ColorFamily']
    YUV: typing.ClassVar['ColorFamily']
    YCOCG: typing.ClassVar['ColorFamily']
    GRAY: typing.ClassVar['ColorFamily']
    COMPAT: typing.ClassVar['ColorFamily']

RGB: ColorFamily
YUV: ColorFamily
YCOCG: ColorFamily
GRAY: ColorFamily
COMPAT: ColorFamily


class SampleType(int):
    name: str
    value: int

    INTEGER: typing.ClassVar['SampleType']
    FLOAT: typing.ClassVar['SampleType']


INTEGER: SampleType
FLOAT: SampleType


class PresetFormat(int):
    name: str
    value: int

    NONE = typing.ClassVar['PresetFormat']

    GRAY8 = typing.ClassVar['PresetFormat']
    GRAY16 = typing.ClassVar['PresetFormat']

    GRAYH = typing.ClassVar['PresetFormat']
    GRAYS = typing.ClassVar['PresetFormat']

    YUV420P8 = typing.ClassVar['PresetFormat']
    YUV422P8 = typing.ClassVar['PresetFormat']
    YUV444P8 = typing.ClassVar['PresetFormat']
    YUV410P8 = typing.ClassVar['PresetFormat']
    YUV411P8 = typing.ClassVar['PresetFormat']
    YUV440P8 = typing.ClassVar['PresetFormat']

    YUV420P9 = typing.ClassVar['PresetFormat']
    YUV422P9 = typing.ClassVar['PresetFormat']
    YUV444P9 = typing.ClassVar['PresetFormat']

    YUV420P10 = typing.ClassVar['PresetFormat']
    YUV422P10 = typing.ClassVar['PresetFormat']
    YUV444P10 = typing.ClassVar['PresetFormat']

    YUV420P12 = typing.ClassVar['PresetFormat']
    YUV422P12 = typing.ClassVar['PresetFormat']
    YUV444P12 = typing.ClassVar['PresetFormat']

    YUV420P14 = typing.ClassVar['PresetFormat']
    YUV422P14 = typing.ClassVar['PresetFormat']
    YUV444P14 = typing.ClassVar['PresetFormat']

    YUV420P16 = typing.ClassVar['PresetFormat']
    YUV422P16 = typing.ClassVar['PresetFormat']
    YUV444P16 = typing.ClassVar['PresetFormat']

    YUV444PH = typing.ClassVar['PresetFormat']
    YUV444PS = typing.ClassVar['PresetFormat']

    RGB24 = typing.ClassVar['PresetFormat']
    RGB27 = typing.ClassVar['PresetFormat']
    RGB30 = typing.ClassVar['PresetFormat']
    RGB48 = typing.ClassVar['PresetFormat']

    RGBH = typing.ClassVar['PresetFormat']
    RGBS = typing.ClassVar['PresetFormat']

    COMPATBGR32 = typing.ClassVar['PresetFormat']


NONE = PresetFormat

GRAY8 = PresetFormat
GRAY16 = PresetFormat

GRAYH = PresetFormat
GRAYS = PresetFormat

YUV420P8 = PresetFormat
YUV422P8 = PresetFormat
YUV444P8 = PresetFormat
YUV410P8 = PresetFormat
YUV411P8 = PresetFormat
YUV440P8 = PresetFormat

YUV420P9 = PresetFormat
YUV422P9 = PresetFormat
YUV444P9 = PresetFormat

YUV420P10 = PresetFormat
YUV422P10 = PresetFormat
YUV444P10 = PresetFormat

YUV420P12 = PresetFormat
YUV422P12 = PresetFormat
YUV444P12 = PresetFormat

YUV420P14 = PresetFormat
YUV422P14 = PresetFormat
YUV444P14 = PresetFormat

YUV420P16 = PresetFormat
YUV422P16 = PresetFormat
YUV444P16 = PresetFormat

YUV444PH = PresetFormat
YUV444PS = PresetFormat

RGB24 = PresetFormat
RGB27 = PresetFormat
RGB30 = PresetFormat
RGB48 = PresetFormat

RGBH = PresetFormat
RGBS = PresetFormat

COMPATBGR32 = PresetFormat


###
# VapourSynth Environment SubSystem

class EnvironmentData:
    """
    Contains the data VapourSynth stores for a specific environment.
    """


class Environment:
    alive: bool
    single: bool
    env_id: int
    active: bool

    def copy(self) -> Environment: ...
    def use(self) -> typing.ContextManager[None]: ...

    def __enter__(self) -> Environment: ...
    def __exit__(self, ty: typing.Type[BaseException], tv: BaseException, tb: types.TracebackType) -> None: ...

class EnvironmentPolicyAPI:
    def wrap_environment(self, environment_data: EnvironmentData) -> Environment: ...
    def create_environment(self) -> EnvironmentData: ...
    def unregister_policy(self) -> None: ...

class EnvironmentPolicy:
    def on_policy_registered(self, special_api: EnvironmentPolicyAPI) -> None: ...
    def on_policy_cleared(self) -> None: ...
    def get_current_environment(self) -> typing.Optional[EnvironmentData]: ...
    def set_environment(self, environment: typing.Optional[EnvironmentData]) -> None: ...
    def is_active(self, environment: EnvironmentData) -> bool: ...


_using_vsscript: bool


def register_policy(policy: EnvironmentPolicy) -> None: ...
def has_policy() -> None: ...

def vpy_current_environment() -> Environment: ...
def get_current_environment() -> Environment: ...


class AlphaOutputTuple(typing.NamedTuple):
    clip: 'VideoNode'
    alpha: 'VideoNode'

Func = typing.Callable[..., typing.Any]

class Error(Exception): ...

def set_message_handler(handler_func: typing.Callable[[int, str], None]) -> None: ...
def clear_output(index: int = 0) -> None: ...
def clear_outputs() -> None: ...
def get_outputs() -> typing.Mapping[int, typing.Union['VideoNode', AlphaOutputTuple]]: ...
def get_output(index: int = 0) -> typing.Union['VideoNode', AlphaOutputTuple]: ...


class Format:
    id: int
    color_family: ColorFamily
    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    subsampling_h: int
    subsampling_w: int
    num_planes: int

    def _as_dict(self) -> typing.Dict[str, typing.Any]: ...
    def replace(self, *,
                color_family: typing.Optional[ColorFamily] = None,
                sample_type: typing.Optional[SampleType] = None,
                bits_per_pixel: typing.Optional[int] = None,
                subsampling_w: typing.Optional[int] = None,
                subsampling_h: typing.Optional[int] = None
                ) -> 'Format': ...


_VideoPropsValue = typing.Union[
    SingleAndSequence[int],
    SingleAndSequence[float],
    SingleAndSequence[str],
    SingleAndSequence['VideoNode'],
    SingleAndSequence['VideoFrame'],
    SingleAndSequence[typing.Callable[..., typing.Any]]
]

class VideoProps(typing.MutableMapping[str, _VideoPropsValue]):
    def __getattr__(self, name: str) -> _VideoPropsValue: ...
    def __setattr__(self, name: str, value: _VideoPropsValue) -> None: ...

    def __delitem__(self, name: str) -> None: ...
    def __setitem__(self, name: str, value: _VideoPropsValue) -> None: ...
    def __getitem__(self, name: str) -> _VideoPropsValue: ...
    def __iter__(self) -> typing.Iterator[str]: ...
    def __len__(self) -> int: ...

    def keys(self) -> typing.Iterator[str]: ...
    def values(self) -> typing.Iterator[_VideoPropsValue]: ...
    def items(self) -> typing.Iterator[typing.Tuple[str, _VideoPropsValue]]: ...

    def get(self, key: str, default: typing.Optional[T] = _NOT_GIVEN) -> typing.Union[T, None, _VideoPropsValue]: ...
    def pop(self, key: str, default: typing.Union[T, typing.Literal[_NOT_GIVEN]] = _NOT_GIVEN) -> typing.Union[T, _VideoPropsValue]: ...
    def popitem(self) -> typing.Tuple[str, _VideoPropsValue]: ...
    def setdefault(self, key: str, default: _VideoPropsValue) -> _VideoPropsValue: ...

    def update(self, *args: typing.Any, **kwargs: typing.Any) -> None: ...
    def clear(self) -> None: ...

    def copy(self) -> typing.Dict[str, _VideoPropsValue]: ...


class VideoPlane:
    width: int
    height: int


class VideoFrame:
    props: VideoProps
    height: int
    width: int
    format: Format
    readonly: bool

    def copy(self) -> 'VideoFrame': ...

    def get_read_ptr(self, plane: int) -> ctypes.c_void_p: ...
    def get_read_array(self, plane: int) -> memoryview: ...
    def get_write_ptr(self, plane: int) -> ctypes.c_void_p: ...
    def get_write_array(self, plane: int) -> memoryview: ...

    def get_stride(self, plane: int) -> int: ...
    def planes(self) -> typing.Iterator['VideoPlane']: ...


class _Future(typing.Generic[T]):
    def set_result(self, value: T) -> None: ...
    def set_exception(self, exception: BaseException) -> None: ...
    def result(self) -> T: ...
    def exception(self) -> typing.Optional[typing.NoReturn]: ...


class Plugin:
    def get_functions(self) -> typing.Dict[str, str]: ...
    def list_functions(self) -> str: ...


# implementation: adg
class _Plugin_adg_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mask(self, clip: "VideoNode", luma_scaling: typing.Union[float, None] = None) -> "VideoNode": ...


class _Plugin_adg_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mask(self, luma_scaling: typing.Union[float, None] = None) -> "VideoNode": ...
# end implementation


# implementation: comb
class _Plugin_comb_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CMaskedMerge(self, base: "VideoNode", alt: "VideoNode", mask: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def CombMask(self, clip: "VideoNode", cthresh: typing.Union[int, None] = None, mthresh: typing.Union[int, None] = None, mi: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_comb_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CMaskedMerge(self, alt: "VideoNode", mask: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def CombMask(self, cthresh: typing.Union[int, None] = None, mthresh: typing.Union[int, None] = None, mi: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
# end implementation


# implementation: d2v
class _Plugin_d2v_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ApplyRFF(self, clip: "VideoNode", d2v: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Source(self, input: typing.Union[str, bytes, bytearray], threads: typing.Union[int, None] = None, nocrop: typing.Union[int, None] = None, rff: typing.Union[int, None] = None) -> "VideoNode": ...


class _Plugin_d2v_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ApplyRFF(self, d2v: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Source(self, threads: typing.Union[int, None] = None, nocrop: typing.Union[int, None] = None, rff: typing.Union[int, None] = None) -> "VideoNode": ...
# end implementation


# implementation: descale
class _Plugin_descale_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Debicubic(self, src: "VideoNode", width: int, height: int, b: typing.Union[float, None] = None, c: typing.Union[float, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Debilinear(self, src: "VideoNode", width: int, height: int, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Delanczos(self, src: "VideoNode", width: int, height: int, taps: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Despline16(self, src: "VideoNode", width: int, height: int, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Despline36(self, src: "VideoNode", width: int, height: int, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Despline64(self, src: "VideoNode", width: int, height: int, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...


class _Plugin_descale_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Debicubic(self, width: int, height: int, b: typing.Union[float, None] = None, c: typing.Union[float, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Debilinear(self, width: int, height: int, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Delanczos(self, width: int, height: int, taps: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Despline16(self, width: int, height: int, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Despline36(self, width: int, height: int, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
    def Despline64(self, width: int, height: int, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None) -> "VideoNode": ...
# end implementation


# implementation: edgefixer
class _Plugin_edgefixer_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ContinuityFixer(self, clip: "VideoNode", left: typing.Sequence[int], top: typing.Sequence[int], right: typing.Sequence[int], bottom: typing.Sequence[int], radius: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...


class _Plugin_edgefixer_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ContinuityFixer(self, left: typing.Sequence[int], top: typing.Sequence[int], right: typing.Sequence[int], bottom: typing.Sequence[int], radius: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
# end implementation


# implementation: eedi3m
class _Plugin_eedi3m_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI3(self, clip: "VideoNode", field: int, dh: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, alpha: typing.Union[float, None] = None, beta: typing.Union[float, None] = None, gamma: typing.Union[float, None] = None, nrad: typing.Union[int, None] = None, mdis: typing.Union[int, None] = None, hp: typing.Union[int, None] = None, ucubic: typing.Union[int, None] = None, cost3: typing.Union[int, None] = None, vcheck: typing.Union[int, None] = None, vthresh0: typing.Union[float, None] = None, vthresh1: typing.Union[float, None] = None, vthresh2: typing.Union[float, None] = None, sclip: typing.Union["VideoNode", None] = None, mclip: typing.Union["VideoNode", None] = None, opt: typing.Union[int, None] = None) -> "VideoNode": ...
    def EEDI3CL(self, clip: "VideoNode", field: int, dh: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, alpha: typing.Union[float, None] = None, beta: typing.Union[float, None] = None, gamma: typing.Union[float, None] = None, nrad: typing.Union[int, None] = None, mdis: typing.Union[int, None] = None, hp: typing.Union[int, None] = None, ucubic: typing.Union[int, None] = None, cost3: typing.Union[int, None] = None, vcheck: typing.Union[int, None] = None, vthresh0: typing.Union[float, None] = None, vthresh1: typing.Union[float, None] = None, vthresh2: typing.Union[float, None] = None, sclip: typing.Union["VideoNode", None] = None, opt: typing.Union[int, None] = None, device: typing.Union[int, None] = None, list_device: typing.Union[int, None] = None, info: typing.Union[int, None] = None) -> "VideoNode": ...


class _Plugin_eedi3m_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI3(self, field: int, dh: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, alpha: typing.Union[float, None] = None, beta: typing.Union[float, None] = None, gamma: typing.Union[float, None] = None, nrad: typing.Union[int, None] = None, mdis: typing.Union[int, None] = None, hp: typing.Union[int, None] = None, ucubic: typing.Union[int, None] = None, cost3: typing.Union[int, None] = None, vcheck: typing.Union[int, None] = None, vthresh0: typing.Union[float, None] = None, vthresh1: typing.Union[float, None] = None, vthresh2: typing.Union[float, None] = None, sclip: typing.Union["VideoNode", None] = None, mclip: typing.Union["VideoNode", None] = None, opt: typing.Union[int, None] = None) -> "VideoNode": ...
    def EEDI3CL(self, field: int, dh: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, alpha: typing.Union[float, None] = None, beta: typing.Union[float, None] = None, gamma: typing.Union[float, None] = None, nrad: typing.Union[int, None] = None, mdis: typing.Union[int, None] = None, hp: typing.Union[int, None] = None, ucubic: typing.Union[int, None] = None, cost3: typing.Union[int, None] = None, vcheck: typing.Union[int, None] = None, vthresh0: typing.Union[float, None] = None, vthresh1: typing.Union[float, None] = None, vthresh2: typing.Union[float, None] = None, sclip: typing.Union["VideoNode", None] = None, opt: typing.Union[int, None] = None, device: typing.Union[int, None] = None, list_device: typing.Union[int, None] = None, info: typing.Union[int, None] = None) -> "VideoNode": ...
# end implementation


# implementation: ffms2
class _Plugin_ffms2_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def GetLogLevel(self) -> "VideoNode": ...
    def Index(self, source: typing.Union[str, bytes, bytearray], cachefile: typing.Union[str, bytes, bytearray, None] = None, indextracks: typing.Union[typing.Sequence[int], None] = None, dumptracks: typing.Union[typing.Sequence[int], None] = None, audiofile: typing.Union[str, bytes, bytearray, None] = None, errorhandling: typing.Union[int, None] = None, overwrite: typing.Union[int, None] = None, demuxer: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def SetLogLevel(self, level: int) -> "VideoNode": ...
    def Source(self, source: typing.Union[str, bytes, bytearray], track: typing.Union[int, None] = None, cache: typing.Union[int, None] = None, cachefile: typing.Union[str, bytes, bytearray, None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None, threads: typing.Union[int, None] = None, timecodes: typing.Union[str, bytes, bytearray, None] = None, seekmode: typing.Union[int, None] = None, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, resizer: typing.Union[str, bytes, bytearray, None] = None, format: typing.Union[int, None] = None, alpha: typing.Union[int, None] = None) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...


class _Plugin_ffms2_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def GetLogLevel(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def Index(self, cachefile: typing.Union[str, bytes, bytearray, None] = None, indextracks: typing.Union[typing.Sequence[int], None] = None, dumptracks: typing.Union[typing.Sequence[int], None] = None, audiofile: typing.Union[str, bytes, bytearray, None] = None, errorhandling: typing.Union[int, None] = None, overwrite: typing.Union[int, None] = None, demuxer: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def SetLogLevel(self) -> "VideoNode": ...
    def Source(self, track: typing.Union[int, None] = None, cache: typing.Union[int, None] = None, cachefile: typing.Union[str, bytes, bytearray, None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None, threads: typing.Union[int, None] = None, timecodes: typing.Union[str, bytes, bytearray, None] = None, seekmode: typing.Union[int, None] = None, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, resizer: typing.Union[str, bytes, bytearray, None] = None, format: typing.Union[int, None] = None, alpha: typing.Union[int, None] = None) -> "VideoNode": ...
    def Version(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
# end implementation


# implementation: fmtc
class _Plugin_fmtc_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def bitdepth(self, clip: "VideoNode", csp: typing.Union[int, None] = None, bits: typing.Union[int, None] = None, flt: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, fulls: typing.Union[int, None] = None, fulld: typing.Union[int, None] = None, dmode: typing.Union[int, None] = None, ampo: typing.Union[float, None] = None, ampn: typing.Union[float, None] = None, dyn: typing.Union[int, None] = None, staticnoise: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None, patsize: typing.Union[int, None] = None) -> "VideoNode": ...
    def histluma(self, clip: "VideoNode", full: typing.Union[int, None] = None, amp: typing.Union[int, None] = None) -> "VideoNode": ...
    def matrix(self, clip: "VideoNode", mat: typing.Union[str, bytes, bytearray, None] = None, mats: typing.Union[str, bytes, bytearray, None] = None, matd: typing.Union[str, bytes, bytearray, None] = None, fulls: typing.Union[int, None] = None, fulld: typing.Union[int, None] = None, coef: typing.Union[typing.Sequence[float], None] = None, csp: typing.Union[int, None] = None, col_fam: typing.Union[int, None] = None, bits: typing.Union[int, None] = None, singleout: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None) -> "VideoNode": ...
    def matrix2020cl(self, clip: "VideoNode", full: typing.Union[int, None] = None, csp: typing.Union[int, None] = None, bits: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None) -> "VideoNode": ...
    def nativetostack16(self, clip: "VideoNode") -> "VideoNode": ...
    def primaries(self, clip: "VideoNode", rs: typing.Union[typing.Sequence[float], None] = None, gs: typing.Union[typing.Sequence[float], None] = None, bs: typing.Union[typing.Sequence[float], None] = None, ws: typing.Union[typing.Sequence[float], None] = None, rd: typing.Union[typing.Sequence[float], None] = None, gd: typing.Union[typing.Sequence[float], None] = None, bd: typing.Union[typing.Sequence[float], None] = None, wd: typing.Union[typing.Sequence[float], None] = None, prims: typing.Union[str, bytes, bytearray, None] = None, primd: typing.Union[str, bytes, bytearray, None] = None, cpuopt: typing.Union[int, None] = None) -> "VideoNode": ...
    def resample(self, clip: "VideoNode", w: typing.Union[int, None] = None, h: typing.Union[int, None] = None, sx: typing.Union[typing.Sequence[float], None] = None, sy: typing.Union[typing.Sequence[float], None] = None, sw: typing.Union[typing.Sequence[float], None] = None, sh: typing.Union[typing.Sequence[float], None] = None, scale: typing.Union[float, None] = None, scaleh: typing.Union[float, None] = None, scalev: typing.Union[float, None] = None, kernel: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, kernelh: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, kernelv: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, impulse: typing.Union[typing.Sequence[float], None] = None, impulseh: typing.Union[typing.Sequence[float], None] = None, impulsev: typing.Union[typing.Sequence[float], None] = None, taps: typing.Union[typing.Sequence[int], None] = None, tapsh: typing.Union[typing.Sequence[int], None] = None, tapsv: typing.Union[typing.Sequence[int], None] = None, a1: typing.Union[typing.Sequence[float], None] = None, a2: typing.Union[typing.Sequence[float], None] = None, a3: typing.Union[typing.Sequence[float], None] = None, kovrspl: typing.Union[typing.Sequence[int], None] = None, fh: typing.Union[typing.Sequence[float], None] = None, fv: typing.Union[typing.Sequence[float], None] = None, cnorm: typing.Union[typing.Sequence[int], None] = None, totalh: typing.Union[typing.Sequence[float], None] = None, totalv: typing.Union[typing.Sequence[float], None] = None, invks: typing.Union[typing.Sequence[int], None] = None, invksh: typing.Union[typing.Sequence[int], None] = None, invksv: typing.Union[typing.Sequence[int], None] = None, invkstaps: typing.Union[typing.Sequence[int], None] = None, invkstapsh: typing.Union[typing.Sequence[int], None] = None, invkstapsv: typing.Union[typing.Sequence[int], None] = None, csp: typing.Union[int, None] = None, css: typing.Union[str, bytes, bytearray, None] = None, planes: typing.Union[typing.Sequence[float], None] = None, fulls: typing.Union[int, None] = None, fulld: typing.Union[int, None] = None, center: typing.Union[typing.Sequence[int], None] = None, cplace: typing.Union[str, bytes, bytearray, None] = None, cplaces: typing.Union[str, bytes, bytearray, None] = None, cplaced: typing.Union[str, bytes, bytearray, None] = None, interlaced: typing.Union[int, None] = None, interlacedd: typing.Union[int, None] = None, tff: typing.Union[int, None] = None, tffd: typing.Union[int, None] = None, flt: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None) -> "VideoNode": ...
    def stack16tonative(self, clip: "VideoNode") -> "VideoNode": ...
    def transfer(self, clip: "VideoNode", transs: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, transd: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, cont: typing.Union[float, None] = None, gcor: typing.Union[float, None] = None, bits: typing.Union[int, None] = None, flt: typing.Union[int, None] = None, fulls: typing.Union[int, None] = None, fulld: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None, blacklvl: typing.Union[float, None] = None) -> "VideoNode": ...


class _Plugin_fmtc_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def bitdepth(self, csp: typing.Union[int, None] = None, bits: typing.Union[int, None] = None, flt: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, fulls: typing.Union[int, None] = None, fulld: typing.Union[int, None] = None, dmode: typing.Union[int, None] = None, ampo: typing.Union[float, None] = None, ampn: typing.Union[float, None] = None, dyn: typing.Union[int, None] = None, staticnoise: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None, patsize: typing.Union[int, None] = None) -> "VideoNode": ...
    def histluma(self, full: typing.Union[int, None] = None, amp: typing.Union[int, None] = None) -> "VideoNode": ...
    def matrix(self, mat: typing.Union[str, bytes, bytearray, None] = None, mats: typing.Union[str, bytes, bytearray, None] = None, matd: typing.Union[str, bytes, bytearray, None] = None, fulls: typing.Union[int, None] = None, fulld: typing.Union[int, None] = None, coef: typing.Union[typing.Sequence[float], None] = None, csp: typing.Union[int, None] = None, col_fam: typing.Union[int, None] = None, bits: typing.Union[int, None] = None, singleout: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None) -> "VideoNode": ...
    def matrix2020cl(self, full: typing.Union[int, None] = None, csp: typing.Union[int, None] = None, bits: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None) -> "VideoNode": ...
    def nativetostack16(self) -> "VideoNode": ...
    def primaries(self, rs: typing.Union[typing.Sequence[float], None] = None, gs: typing.Union[typing.Sequence[float], None] = None, bs: typing.Union[typing.Sequence[float], None] = None, ws: typing.Union[typing.Sequence[float], None] = None, rd: typing.Union[typing.Sequence[float], None] = None, gd: typing.Union[typing.Sequence[float], None] = None, bd: typing.Union[typing.Sequence[float], None] = None, wd: typing.Union[typing.Sequence[float], None] = None, prims: typing.Union[str, bytes, bytearray, None] = None, primd: typing.Union[str, bytes, bytearray, None] = None, cpuopt: typing.Union[int, None] = None) -> "VideoNode": ...
    def resample(self, w: typing.Union[int, None] = None, h: typing.Union[int, None] = None, sx: typing.Union[typing.Sequence[float], None] = None, sy: typing.Union[typing.Sequence[float], None] = None, sw: typing.Union[typing.Sequence[float], None] = None, sh: typing.Union[typing.Sequence[float], None] = None, scale: typing.Union[float, None] = None, scaleh: typing.Union[float, None] = None, scalev: typing.Union[float, None] = None, kernel: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, kernelh: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, kernelv: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, impulse: typing.Union[typing.Sequence[float], None] = None, impulseh: typing.Union[typing.Sequence[float], None] = None, impulsev: typing.Union[typing.Sequence[float], None] = None, taps: typing.Union[typing.Sequence[int], None] = None, tapsh: typing.Union[typing.Sequence[int], None] = None, tapsv: typing.Union[typing.Sequence[int], None] = None, a1: typing.Union[typing.Sequence[float], None] = None, a2: typing.Union[typing.Sequence[float], None] = None, a3: typing.Union[typing.Sequence[float], None] = None, kovrspl: typing.Union[typing.Sequence[int], None] = None, fh: typing.Union[typing.Sequence[float], None] = None, fv: typing.Union[typing.Sequence[float], None] = None, cnorm: typing.Union[typing.Sequence[int], None] = None, totalh: typing.Union[typing.Sequence[float], None] = None, totalv: typing.Union[typing.Sequence[float], None] = None, invks: typing.Union[typing.Sequence[int], None] = None, invksh: typing.Union[typing.Sequence[int], None] = None, invksv: typing.Union[typing.Sequence[int], None] = None, invkstaps: typing.Union[typing.Sequence[int], None] = None, invkstapsh: typing.Union[typing.Sequence[int], None] = None, invkstapsv: typing.Union[typing.Sequence[int], None] = None, csp: typing.Union[int, None] = None, css: typing.Union[str, bytes, bytearray, None] = None, planes: typing.Union[typing.Sequence[float], None] = None, fulls: typing.Union[int, None] = None, fulld: typing.Union[int, None] = None, center: typing.Union[typing.Sequence[int], None] = None, cplace: typing.Union[str, bytes, bytearray, None] = None, cplaces: typing.Union[str, bytes, bytearray, None] = None, cplaced: typing.Union[str, bytes, bytearray, None] = None, interlaced: typing.Union[int, None] = None, interlacedd: typing.Union[int, None] = None, tff: typing.Union[int, None] = None, tffd: typing.Union[int, None] = None, flt: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None) -> "VideoNode": ...
    def stack16tonative(self) -> "VideoNode": ...
    def transfer(self, transs: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, transd: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, cont: typing.Union[float, None] = None, gcor: typing.Union[float, None] = None, bits: typing.Union[int, None] = None, flt: typing.Union[int, None] = None, fulls: typing.Union[int, None] = None, fulld: typing.Union[int, None] = None, cpuopt: typing.Union[int, None] = None, blacklvl: typing.Union[float, None] = None) -> "VideoNode": ...
# end implementation


# implementation: imwri
class _Plugin_imwri_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, filename: typing.Sequence[typing.Union[str, bytes, bytearray]], firstnum: typing.Union[int, None] = None, mismatch: typing.Union[int, None] = None, alpha: typing.Union[int, None] = None, float_output: typing.Union[int, None] = None) -> "VideoNode": ...
    def Write(self, clip: "VideoNode", imgformat: typing.Union[str, bytes, bytearray], filename: typing.Union[str, bytes, bytearray], firstnum: typing.Union[int, None] = None, quality: typing.Union[int, None] = None, dither: typing.Union[int, None] = None, compression_type: typing.Union[str, bytes, bytearray, None] = None, overwrite: typing.Union[int, None] = None, alpha: typing.Union["VideoNode", None] = None) -> "VideoNode": ...


class _Plugin_imwri_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, firstnum: typing.Union[int, None] = None, mismatch: typing.Union[int, None] = None, alpha: typing.Union[int, None] = None, float_output: typing.Union[int, None] = None) -> "VideoNode": ...
    def Write(self, imgformat: typing.Union[str, bytes, bytearray], filename: typing.Union[str, bytes, bytearray], firstnum: typing.Union[int, None] = None, quality: typing.Union[int, None] = None, dither: typing.Union[int, None] = None, compression_type: typing.Union[str, bytes, bytearray, None] = None, overwrite: typing.Union[int, None] = None, alpha: typing.Union["VideoNode", None] = None) -> "VideoNode": ...
# end implementation


# implementation: knlm
class _Plugin_knlm_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def KNLMeansCL(self, clip: "VideoNode", d: typing.Union[int, None] = None, a: typing.Union[int, None] = None, s: typing.Union[int, None] = None, h: typing.Union[float, None] = None, channels: typing.Union[str, bytes, bytearray, None] = None, wmode: typing.Union[int, None] = None, wref: typing.Union[float, None] = None, rclip: typing.Union["VideoNode", None] = None, device_type: typing.Union[str, bytes, bytearray, None] = None, device_id: typing.Union[int, None] = None, ocl_x: typing.Union[int, None] = None, ocl_y: typing.Union[int, None] = None, ocl_r: typing.Union[int, None] = None, info: typing.Union[int, None] = None) -> "VideoNode": ...


class _Plugin_knlm_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def KNLMeansCL(self, d: typing.Union[int, None] = None, a: typing.Union[int, None] = None, s: typing.Union[int, None] = None, h: typing.Union[float, None] = None, channels: typing.Union[str, bytes, bytearray, None] = None, wmode: typing.Union[int, None] = None, wref: typing.Union[float, None] = None, rclip: typing.Union["VideoNode", None] = None, device_type: typing.Union[str, bytes, bytearray, None] = None, device_id: typing.Union[int, None] = None, ocl_x: typing.Union[int, None] = None, ocl_y: typing.Union[int, None] = None, ocl_r: typing.Union[int, None] = None, info: typing.Union[int, None] = None) -> "VideoNode": ...
# end implementation


# implementation: lsmas
class _Plugin_lsmas_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LWLibavSource(self, source: typing.Union[str, bytes, bytearray], stream_index: typing.Union[int, None] = None, cache: typing.Union[int, None] = None, threads: typing.Union[int, None] = None, seek_mode: typing.Union[int, None] = None, seek_threshold: typing.Union[int, None] = None, dr: typing.Union[int, None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None, variable: typing.Union[int, None] = None, format: typing.Union[str, bytes, bytearray, None] = None, decoder: typing.Union[str, bytes, bytearray, None] = None, repeat: typing.Union[int, None] = None, dominance: typing.Union[int, None] = None) -> "VideoNode": ...
    def LibavSMASHSource(self, source: typing.Union[str, bytes, bytearray], track: typing.Union[int, None] = None, threads: typing.Union[int, None] = None, seek_mode: typing.Union[int, None] = None, seek_threshold: typing.Union[int, None] = None, dr: typing.Union[int, None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None, variable: typing.Union[int, None] = None, format: typing.Union[str, bytes, bytearray, None] = None, decoder: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_lsmas_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LWLibavSource(self, stream_index: typing.Union[int, None] = None, cache: typing.Union[int, None] = None, threads: typing.Union[int, None] = None, seek_mode: typing.Union[int, None] = None, seek_threshold: typing.Union[int, None] = None, dr: typing.Union[int, None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None, variable: typing.Union[int, None] = None, format: typing.Union[str, bytes, bytearray, None] = None, decoder: typing.Union[str, bytes, bytearray, None] = None, repeat: typing.Union[int, None] = None, dominance: typing.Union[int, None] = None) -> "VideoNode": ...
    def LibavSMASHSource(self, track: typing.Union[int, None] = None, threads: typing.Union[int, None] = None, seek_mode: typing.Union[int, None] = None, seek_threshold: typing.Union[int, None] = None, dr: typing.Union[int, None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None, variable: typing.Union[int, None] = None, format: typing.Union[str, bytes, bytearray, None] = None, decoder: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
# end implementation


# implementation: mpls
class _Plugin_mpls_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, bd_path: typing.Union[str, bytes, bytearray], playlist: int, angle: typing.Union[int, None] = None) -> "VideoNode": ...


class _Plugin_mpls_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, playlist: int, angle: typing.Union[int, None] = None) -> "VideoNode": ...
# end implementation


# implementation: nnedi3
class _Plugin_nnedi3_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, clip: "VideoNode", field: int, dh: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, nsize: typing.Union[int, None] = None, nns: typing.Union[int, None] = None, qual: typing.Union[int, None] = None, etype: typing.Union[int, None] = None, pscrn: typing.Union[int, None] = None, opt: typing.Union[int, None] = None, int16_prescreener: typing.Union[int, None] = None, int16_predictor: typing.Union[int, None] = None, exp: typing.Union[int, None] = None, show_mask: typing.Union[int, None] = None, combed_only: typing.Union[int, None] = None) -> "VideoNode": ...


class _Plugin_nnedi3_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, field: int, dh: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, nsize: typing.Union[int, None] = None, nns: typing.Union[int, None] = None, qual: typing.Union[int, None] = None, etype: typing.Union[int, None] = None, pscrn: typing.Union[int, None] = None, opt: typing.Union[int, None] = None, int16_prescreener: typing.Union[int, None] = None, int16_predictor: typing.Union[int, None] = None, exp: typing.Union[int, None] = None, show_mask: typing.Union[int, None] = None, combed_only: typing.Union[int, None] = None) -> "VideoNode": ...
# end implementation


# implementation: resize
class _Plugin_resize_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bicubic(self, clip: "VideoNode", width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Bilinear(self, clip: "VideoNode", width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Lanczos(self, clip: "VideoNode", width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Point(self, clip: "VideoNode", width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Spline16(self, clip: "VideoNode", width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Spline36(self, clip: "VideoNode", width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Spline64(self, clip: "VideoNode", width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...


class _Plugin_resize_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bicubic(self, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Bilinear(self, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Lanczos(self, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Point(self, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Spline16(self, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Spline36(self, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
    def Spline64(self, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, matrix: typing.Union[int, None] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Union[int, None] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Union[int, None] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Union[int, None] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Union[int, None] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Union[int, None] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Union[int, None] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Union[int, None] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Union[int, None] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Union[int, None] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Union[float, None] = None, filter_param_b: typing.Union[float, None] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Union[float, None] = None, filter_param_b_uv: typing.Union[float, None] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Union[int, None] = None, src_left: typing.Union[float, None] = None, src_top: typing.Union[float, None] = None, src_width: typing.Union[float, None] = None, src_height: typing.Union[float, None] = None, nominal_luminance: typing.Union[float, None] = None) -> "VideoNode": ...
# end implementation


# implementation: std
class _Plugin_std_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddBorders(self, clip: "VideoNode", left: typing.Union[int, None] = None, right: typing.Union[int, None] = None, top: typing.Union[int, None] = None, bottom: typing.Union[int, None] = None, color: typing.Union[typing.Sequence[float], None] = None) -> "VideoNode": ...
    def AssumeFPS(self, clip: "VideoNode", src: typing.Union["VideoNode", None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None) -> "VideoNode": ...
    def Binarize(self, clip: "VideoNode", threshold: typing.Union[typing.Sequence[float], None] = None, v0: typing.Union[typing.Sequence[float], None] = None, v1: typing.Union[typing.Sequence[float], None] = None, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BlankClip(self, clip: typing.Union["VideoNode", None] = None, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, length: typing.Union[int, None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None, color: typing.Union[typing.Sequence[float], None] = None, keep: typing.Union[int, None] = None) -> "VideoNode": ...
    def BoxBlur(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, hradius: typing.Union[int, None] = None, hpasses: typing.Union[int, None] = None, vradius: typing.Union[int, None] = None, vpasses: typing.Union[int, None] = None) -> "VideoNode": ...
    def Cache(self, clip: "VideoNode", size: typing.Union[int, None] = None, fixed: typing.Union[int, None] = None, make_linear: typing.Union[int, None] = None) -> "VideoNode": ...
    def ClipToProp(self, clip: "VideoNode", mclip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Convolution(self, clip: "VideoNode", matrix: typing.Sequence[float], bias: typing.Union[float, None] = None, divisor: typing.Union[float, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, saturate: typing.Union[int, None] = None, mode: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Crop(self, clip: "VideoNode", left: typing.Union[int, None] = None, right: typing.Union[int, None] = None, top: typing.Union[int, None] = None, bottom: typing.Union[int, None] = None) -> "VideoNode": ...
    def CropAbs(self, clip: "VideoNode", width: int, height: int, left: typing.Union[int, None] = None, top: typing.Union[int, None] = None, x: typing.Union[int, None] = None, y: typing.Union[int, None] = None) -> "VideoNode": ...
    def CropRel(self, clip: "VideoNode", left: typing.Union[int, None] = None, right: typing.Union[int, None] = None, top: typing.Union[int, None] = None, bottom: typing.Union[int, None] = None) -> "VideoNode": ...
    def Deflate(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, threshold: typing.Union[float, None] = None) -> "VideoNode": ...
    def DeleteFrames(self, clip: "VideoNode", frames: typing.Sequence[int]) -> "VideoNode": ...
    def DoubleWeave(self, clip: "VideoNode", tff: typing.Union[int, None] = None) -> "VideoNode": ...
    def DuplicateFrames(self, clip: "VideoNode", frames: typing.Sequence[int]) -> "VideoNode": ...
    def Expr(self, clips: typing.Sequence["VideoNode"], expr: typing.Sequence[typing.Union[str, bytes, bytearray]], format: typing.Union[int, None] = None) -> "VideoNode": ...
    def FlipHorizontal(self, clip: "VideoNode") -> "VideoNode": ...
    def FlipVertical(self, clip: "VideoNode") -> "VideoNode": ...
    def FrameEval(self, clip: "VideoNode", eval: typing.Callable[..., typing.Any], prop_src: typing.Union[typing.Sequence["VideoNode"], None] = None) -> "VideoNode": ...
    def FreezeFrames(self, clip: "VideoNode", first: typing.Sequence[int], last: typing.Sequence[int], replacement: typing.Sequence[int]) -> "VideoNode": ...
    def Inflate(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, threshold: typing.Union[float, None] = None) -> "VideoNode": ...
    def Interleave(self, clips: typing.Sequence["VideoNode"], extend: typing.Union[int, None] = None, mismatch: typing.Union[int, None] = None, modify_duration: typing.Union[int, None] = None) -> "VideoNode": ...
    def Invert(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Levels(self, clip: "VideoNode", min_in: typing.Union[typing.Sequence[float], None] = None, max_in: typing.Union[typing.Sequence[float], None] = None, gamma: typing.Union[typing.Sequence[float], None] = None, min_out: typing.Union[typing.Sequence[float], None] = None, max_out: typing.Union[typing.Sequence[float], None] = None, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Limiter(self, clip: "VideoNode", min: typing.Union[typing.Sequence[float], None] = None, max: typing.Union[typing.Sequence[float], None] = None, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def LoadPlugin(self, path: typing.Union[str, bytes, bytearray], altsearchpath: typing.Union[int, None] = None, forcens: typing.Union[str, bytes, bytearray, None] = None, forceid: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Loop(self, clip: "VideoNode", times: typing.Union[int, None] = None) -> "VideoNode": ...
    def Lut(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, lut: typing.Union[typing.Sequence[int], None] = None, lutf: typing.Union[typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Union[int, None] = None, floatout: typing.Union[int, None] = None) -> "VideoNode": ...
    def Lut2(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, lut: typing.Union[typing.Sequence[int], None] = None, lutf: typing.Union[typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Union[int, None] = None, floatout: typing.Union[int, None] = None) -> "VideoNode": ...
    def MakeDiff(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MaskedMerge(self, clipa: "VideoNode", clipb: "VideoNode", mask: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, first_plane: typing.Union[int, None] = None, premultiplied: typing.Union[int, None] = None) -> "VideoNode": ...
    def Maximum(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, threshold: typing.Union[float, None] = None, coordinates: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Median(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Merge(self, clipa: "VideoNode", clipb: "VideoNode", weight: typing.Union[typing.Sequence[float], None] = None) -> "VideoNode": ...
    def MergeDiff(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Minimum(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, threshold: typing.Union[float, None] = None, coordinates: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ModifyFrame(self, clip: "VideoNode", clips: typing.Sequence["VideoNode"], selector: typing.Callable[..., typing.Any]) -> "VideoNode": ...
    def PEMVerifier(self, clip: "VideoNode", upper: typing.Union[typing.Sequence[float], None] = None, lower: typing.Union[typing.Sequence[float], None] = None) -> "VideoNode": ...
    def PlaneStats(self, clipa: "VideoNode", clipb: typing.Union["VideoNode", None] = None, plane: typing.Union[int, None] = None, prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def PreMultiply(self, clip: "VideoNode", alpha: "VideoNode") -> "VideoNode": ...
    def Prewitt(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, scale: typing.Union[float, None] = None) -> "VideoNode": ...
    def PropToClip(self, clip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Reverse(self, clip: "VideoNode") -> "VideoNode": ...
    def SelectEvery(self, clip: "VideoNode", cycle: int, offsets: typing.Sequence[int], modify_duration: typing.Union[int, None] = None) -> "VideoNode": ...
    def SeparateFields(self, clip: "VideoNode", tff: typing.Union[int, None] = None, modify_duration: typing.Union[int, None] = None) -> "VideoNode": ...
    def SetFieldBased(self, clip: "VideoNode", value: int) -> "VideoNode": ...
    def SetFrameProp(self, clip: "VideoNode", prop: typing.Union[str, bytes, bytearray], delete: typing.Union[int, None] = None, intval: typing.Union[typing.Sequence[int], None] = None, floatval: typing.Union[typing.Sequence[float], None] = None, data: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def SetMaxCPU(self, cpu: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def ShufflePlanes(self, clips: typing.Sequence["VideoNode"], planes: typing.Sequence[int], colorfamily: int) -> "VideoNode": ...
    def Sobel(self, clip: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, scale: typing.Union[float, None] = None) -> "VideoNode": ...
    def Splice(self, clips: typing.Sequence["VideoNode"], mismatch: typing.Union[int, None] = None) -> "VideoNode": ...
    def StackHorizontal(self, clips: typing.Sequence["VideoNode"]) -> "VideoNode": ...
    def StackVertical(self, clips: typing.Sequence["VideoNode"]) -> "VideoNode": ...
    def Transpose(self, clip: "VideoNode") -> "VideoNode": ...
    def Trim(self, clip: "VideoNode", first: typing.Union[int, None] = None, last: typing.Union[int, None] = None, length: typing.Union[int, None] = None) -> "VideoNode": ...
    def Turn180(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_std_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddBorders(self, left: typing.Union[int, None] = None, right: typing.Union[int, None] = None, top: typing.Union[int, None] = None, bottom: typing.Union[int, None] = None, color: typing.Union[typing.Sequence[float], None] = None) -> "VideoNode": ...
    def AssumeFPS(self, src: typing.Union["VideoNode", None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None) -> "VideoNode": ...
    def Binarize(self, threshold: typing.Union[typing.Sequence[float], None] = None, v0: typing.Union[typing.Sequence[float], None] = None, v1: typing.Union[typing.Sequence[float], None] = None, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BlankClip(self, width: typing.Union[int, None] = None, height: typing.Union[int, None] = None, format: typing.Union[int, None] = None, length: typing.Union[int, None] = None, fpsnum: typing.Union[int, None] = None, fpsden: typing.Union[int, None] = None, color: typing.Union[typing.Sequence[float], None] = None, keep: typing.Union[int, None] = None) -> "VideoNode": ...
    def BoxBlur(self, planes: typing.Union[typing.Sequence[int], None] = None, hradius: typing.Union[int, None] = None, hpasses: typing.Union[int, None] = None, vradius: typing.Union[int, None] = None, vpasses: typing.Union[int, None] = None) -> "VideoNode": ...
    def Cache(self, size: typing.Union[int, None] = None, fixed: typing.Union[int, None] = None, make_linear: typing.Union[int, None] = None) -> "VideoNode": ...
    def ClipToProp(self, mclip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Convolution(self, matrix: typing.Sequence[float], bias: typing.Union[float, None] = None, divisor: typing.Union[float, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, saturate: typing.Union[int, None] = None, mode: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Crop(self, left: typing.Union[int, None] = None, right: typing.Union[int, None] = None, top: typing.Union[int, None] = None, bottom: typing.Union[int, None] = None) -> "VideoNode": ...
    def CropAbs(self, width: int, height: int, left: typing.Union[int, None] = None, top: typing.Union[int, None] = None, x: typing.Union[int, None] = None, y: typing.Union[int, None] = None) -> "VideoNode": ...
    def CropRel(self, left: typing.Union[int, None] = None, right: typing.Union[int, None] = None, top: typing.Union[int, None] = None, bottom: typing.Union[int, None] = None) -> "VideoNode": ...
    def Deflate(self, planes: typing.Union[typing.Sequence[int], None] = None, threshold: typing.Union[float, None] = None) -> "VideoNode": ...
    def DeleteFrames(self, frames: typing.Sequence[int]) -> "VideoNode": ...
    def DoubleWeave(self, tff: typing.Union[int, None] = None) -> "VideoNode": ...
    def DuplicateFrames(self, frames: typing.Sequence[int]) -> "VideoNode": ...
    def Expr(self, expr: typing.Sequence[typing.Union[str, bytes, bytearray]], format: typing.Union[int, None] = None) -> "VideoNode": ...
    def FlipHorizontal(self) -> "VideoNode": ...
    def FlipVertical(self) -> "VideoNode": ...
    def FrameEval(self, eval: typing.Callable[..., typing.Any], prop_src: typing.Union[typing.Sequence["VideoNode"], None] = None) -> "VideoNode": ...
    def FreezeFrames(self, first: typing.Sequence[int], last: typing.Sequence[int], replacement: typing.Sequence[int]) -> "VideoNode": ...
    def Inflate(self, planes: typing.Union[typing.Sequence[int], None] = None, threshold: typing.Union[float, None] = None) -> "VideoNode": ...
    def Interleave(self, extend: typing.Union[int, None] = None, mismatch: typing.Union[int, None] = None, modify_duration: typing.Union[int, None] = None) -> "VideoNode": ...
    def Invert(self, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Levels(self, min_in: typing.Union[typing.Sequence[float], None] = None, max_in: typing.Union[typing.Sequence[float], None] = None, gamma: typing.Union[typing.Sequence[float], None] = None, min_out: typing.Union[typing.Sequence[float], None] = None, max_out: typing.Union[typing.Sequence[float], None] = None, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Limiter(self, min: typing.Union[typing.Sequence[float], None] = None, max: typing.Union[typing.Sequence[float], None] = None, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def LoadPlugin(self, altsearchpath: typing.Union[int, None] = None, forcens: typing.Union[str, bytes, bytearray, None] = None, forceid: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Loop(self, times: typing.Union[int, None] = None) -> "VideoNode": ...
    def Lut(self, planes: typing.Union[typing.Sequence[int], None] = None, lut: typing.Union[typing.Sequence[int], None] = None, lutf: typing.Union[typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Union[int, None] = None, floatout: typing.Union[int, None] = None) -> "VideoNode": ...
    def Lut2(self, clipb: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, lut: typing.Union[typing.Sequence[int], None] = None, lutf: typing.Union[typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Union[int, None] = None, floatout: typing.Union[int, None] = None) -> "VideoNode": ...
    def MakeDiff(self, clipb: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MaskedMerge(self, clipb: "VideoNode", mask: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None, first_plane: typing.Union[int, None] = None, premultiplied: typing.Union[int, None] = None) -> "VideoNode": ...
    def Maximum(self, planes: typing.Union[typing.Sequence[int], None] = None, threshold: typing.Union[float, None] = None, coordinates: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Median(self, planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Merge(self, clipb: "VideoNode", weight: typing.Union[typing.Sequence[float], None] = None) -> "VideoNode": ...
    def MergeDiff(self, clipb: "VideoNode", planes: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Minimum(self, planes: typing.Union[typing.Sequence[int], None] = None, threshold: typing.Union[float, None] = None, coordinates: typing.Union[typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ModifyFrame(self, clips: typing.Sequence["VideoNode"], selector: typing.Callable[..., typing.Any]) -> "VideoNode": ...
    def PEMVerifier(self, upper: typing.Union[typing.Sequence[float], None] = None, lower: typing.Union[typing.Sequence[float], None] = None) -> "VideoNode": ...
    def PlaneStats(self, clipb: typing.Union["VideoNode", None] = None, plane: typing.Union[int, None] = None, prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def PreMultiply(self, alpha: "VideoNode") -> "VideoNode": ...
    def Prewitt(self, planes: typing.Union[typing.Sequence[int], None] = None, scale: typing.Union[float, None] = None) -> "VideoNode": ...
    def PropToClip(self, prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Reverse(self) -> "VideoNode": ...
    def SelectEvery(self, cycle: int, offsets: typing.Sequence[int], modify_duration: typing.Union[int, None] = None) -> "VideoNode": ...
    def SeparateFields(self, tff: typing.Union[int, None] = None, modify_duration: typing.Union[int, None] = None) -> "VideoNode": ...
    def SetFieldBased(self, value: int) -> "VideoNode": ...
    def SetFrameProp(self, prop: typing.Union[str, bytes, bytearray], delete: typing.Union[int, None] = None, intval: typing.Union[typing.Sequence[int], None] = None, floatval: typing.Union[typing.Sequence[float], None] = None, data: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def SetMaxCPU(self) -> "VideoNode": ...
    def ShufflePlanes(self, planes: typing.Sequence[int], colorfamily: int) -> "VideoNode": ...
    def Sobel(self, planes: typing.Union[typing.Sequence[int], None] = None, scale: typing.Union[float, None] = None) -> "VideoNode": ...
    def Splice(self, mismatch: typing.Union[int, None] = None) -> "VideoNode": ...
    def StackHorizontal(self) -> "VideoNode": ...
    def StackVertical(self) -> "VideoNode": ...
    def Transpose(self) -> "VideoNode": ...
    def Trim(self, first: typing.Union[int, None] = None, last: typing.Union[int, None] = None, length: typing.Union[int, None] = None) -> "VideoNode": ...
    def Turn180(self) -> "VideoNode": ...
# end implementation


# implementation: text
class _Plugin_text_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ClipInfo(self, clip: "VideoNode", alignment: typing.Union[int, None] = None) -> "VideoNode": ...
    def CoreInfo(self, clip: typing.Union["VideoNode", None] = None, alignment: typing.Union[int, None] = None) -> "VideoNode": ...
    def FrameNum(self, clip: "VideoNode", alignment: typing.Union[int, None] = None) -> "VideoNode": ...
    def FrameProps(self, clip: "VideoNode", props: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, alignment: typing.Union[int, None] = None) -> "VideoNode": ...
    def Text(self, clip: "VideoNode", text: typing.Union[str, bytes, bytearray], alignment: typing.Union[int, None] = None) -> "VideoNode": ...


class _Plugin_text_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ClipInfo(self, alignment: typing.Union[int, None] = None) -> "VideoNode": ...
    def CoreInfo(self, alignment: typing.Union[int, None] = None) -> "VideoNode": ...
    def FrameNum(self, alignment: typing.Union[int, None] = None) -> "VideoNode": ...
    def FrameProps(self, props: typing.Union[typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None, alignment: typing.Union[int, None] = None) -> "VideoNode": ...
    def Text(self, text: typing.Union[str, bytes, bytearray], alignment: typing.Union[int, None] = None) -> "VideoNode": ...
# end implementation


# implementation: vinverse
class _Plugin_vinverse_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Vinverse(self, clip: "VideoNode", sstr: typing.Union[float, None] = None, amnt: typing.Union[int, None] = None, scl: typing.Union[float, None] = None) -> "VideoNode": ...


class _Plugin_vinverse_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Vinverse(self, sstr: typing.Union[float, None] = None, amnt: typing.Union[int, None] = None, scl: typing.Union[float, None] = None) -> "VideoNode": ...
# end implementation


# implementation: vivtc
class _Plugin_vivtc_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VDecimate(self, clip: "VideoNode", cycle: typing.Union[int, None] = None, chroma: typing.Union[int, None] = None, dupthresh: typing.Union[float, None] = None, scthresh: typing.Union[float, None] = None, blockx: typing.Union[int, None] = None, blocky: typing.Union[int, None] = None, clip2: typing.Union["VideoNode", None] = None, ovr: typing.Union[str, bytes, bytearray, None] = None, dryrun: typing.Union[int, None] = None) -> "VideoNode": ...
    def VFM(self, clip: "VideoNode", order: int, field: typing.Union[int, None] = None, mode: typing.Union[int, None] = None, mchroma: typing.Union[int, None] = None, cthresh: typing.Union[int, None] = None, mi: typing.Union[int, None] = None, chroma: typing.Union[int, None] = None, blockx: typing.Union[int, None] = None, blocky: typing.Union[int, None] = None, y0: typing.Union[int, None] = None, y1: typing.Union[int, None] = None, scthresh: typing.Union[float, None] = None, micmatch: typing.Union[int, None] = None, micout: typing.Union[int, None] = None, clip2: typing.Union["VideoNode", None] = None) -> "VideoNode": ...


class _Plugin_vivtc_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VDecimate(self, cycle: typing.Union[int, None] = None, chroma: typing.Union[int, None] = None, dupthresh: typing.Union[float, None] = None, scthresh: typing.Union[float, None] = None, blockx: typing.Union[int, None] = None, blocky: typing.Union[int, None] = None, clip2: typing.Union["VideoNode", None] = None, ovr: typing.Union[str, bytes, bytearray, None] = None, dryrun: typing.Union[int, None] = None) -> "VideoNode": ...
    def VFM(self, order: int, field: typing.Union[int, None] = None, mode: typing.Union[int, None] = None, mchroma: typing.Union[int, None] = None, cthresh: typing.Union[int, None] = None, mi: typing.Union[int, None] = None, chroma: typing.Union[int, None] = None, blockx: typing.Union[int, None] = None, blocky: typing.Union[int, None] = None, y0: typing.Union[int, None] = None, y1: typing.Union[int, None] = None, scthresh: typing.Union[float, None] = None, micmatch: typing.Union[int, None] = None, micout: typing.Union[int, None] = None, clip2: typing.Union["VideoNode", None] = None) -> "VideoNode": ...
# end implementation


# implementation: znedi3
class _Plugin_znedi3_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, clip: "VideoNode", field: int, dh: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, nsize: typing.Union[int, None] = None, nns: typing.Union[int, None] = None, qual: typing.Union[int, None] = None, etype: typing.Union[int, None] = None, pscrn: typing.Union[int, None] = None, opt: typing.Union[int, None] = None, int16_prescreener: typing.Union[int, None] = None, int16_predictor: typing.Union[int, None] = None, exp: typing.Union[int, None] = None, show_mask: typing.Union[int, None] = None, x_nnedi3_weights_bin: typing.Union[str, bytes, bytearray, None] = None, x_cpu: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...


class _Plugin_znedi3_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, field: int, dh: typing.Union[int, None] = None, planes: typing.Union[typing.Sequence[int], None] = None, nsize: typing.Union[int, None] = None, nns: typing.Union[int, None] = None, qual: typing.Union[int, None] = None, etype: typing.Union[int, None] = None, pscrn: typing.Union[int, None] = None, opt: typing.Union[int, None] = None, int16_prescreener: typing.Union[int, None] = None, int16_predictor: typing.Union[int, None] = None, exp: typing.Union[int, None] = None, show_mask: typing.Union[int, None] = None, x_nnedi3_weights_bin: typing.Union[str, bytes, bytearray, None] = None, x_cpu: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
# end implementation


class VideoNode:
# instance_bound: adg
    @property
    def adg(self) -> _Plugin_adg_Bound:
        """
        Adaptive grain
        """
# end instance
# instance_bound: comb
    @property
    def comb(self) -> _Plugin_comb_Bound:
        """
        comb filters v0.0.1
        """
# end instance
# instance_bound: d2v
    @property
    def d2v(self) -> _Plugin_d2v_Bound:
        """
        D2V Source
        """
# end instance
# instance_bound: descale
    @property
    def descale(self) -> _Plugin_descale_Bound:
        """
        Undo linear interpolation
        """
# end instance
# instance_bound: edgefixer
    @property
    def edgefixer(self) -> _Plugin_edgefixer_Bound:
        """
        VapourSynth edgefixer port
        """
# end instance
# instance_bound: eedi3m
    @property
    def eedi3m(self) -> _Plugin_eedi3m_Bound:
        """
        Enhanced Edge Directed Interpolation 3
        """
# end instance
# instance_bound: ffms2
    @property
    def ffms2(self) -> _Plugin_ffms2_Bound:
        """
        FFmpegSource 2 for VapourSynth
        """
# end instance
# instance_bound: fmtc
    @property
    def fmtc(self) -> _Plugin_fmtc_Bound:
        """
        Format converter, r22
        """
# end instance
# instance_bound: imwri
    @property
    def imwri(self) -> _Plugin_imwri_Bound:
        """
        VapourSynth ImageMagick 7 HDRI Writer/Reader
        """
# end instance
# instance_bound: knlm
    @property
    def knlm(self) -> _Plugin_knlm_Bound:
        """
        KNLMeansCL for VapourSynth
        """
# end instance
# instance_bound: lsmas
    @property
    def lsmas(self) -> _Plugin_lsmas_Bound:
        """
        LSMASHSource for VapourSynth
        """
# end instance
# instance_bound: mpls
    @property
    def mpls(self) -> _Plugin_mpls_Bound:
        """
        Get m2ts clip id from a playlist and return a dict
        """
# end instance
# instance_bound: nnedi3
    @property
    def nnedi3(self) -> _Plugin_nnedi3_Bound:
        """
        Neural network edge directed interpolation (3rd gen.), v12
        """
# end instance
# instance_bound: resize
    @property
    def resize(self) -> _Plugin_resize_Bound:
        """
        VapourSynth Resize
        """
# end instance
# instance_bound: std
    @property
    def std(self) -> _Plugin_std_Bound:
        """
        VapourSynth Core Functions
        """
# end instance
# instance_bound: text
    @property
    def text(self) -> _Plugin_text_Bound:
        """
        VapourSynth Text
        """
# end instance
# instance_bound: vinverse
    @property
    def vinverse(self) -> _Plugin_vinverse_Bound:
        """
        A simple filter to remove residual combing.
        """
# end instance
# instance_bound: vivtc
    @property
    def vivtc(self) -> _Plugin_vivtc_Bound:
        """
        VFM
        """
# end instance
# instance_bound: znedi3
    @property
    def znedi3(self) -> _Plugin_znedi3_Bound:
        """
        Neural network edge directed interpolation (3rd gen.)
        """
# end instance

    format: typing.Optional[Format]
    fps: fractions.Fraction
    fps_den: int
    fps_num: int
    height: int
    width: int

    num_frames: int

    def get_frame(self, n: int) -> VideoFrame: ...
    def get_frame_async_raw(self, n: int, cb: _Future[VideoFrame], future_wrapper: typing.Optional[typing.Callable[..., None]]=None) -> _Future[VideoFrame]: ...
    def get_frame_async(self, n: int) -> _Future[VideoFrame]: ...

    def set_output(self, index: int = 0, alpha: typing.Optional['VideoNode']=None) -> None: ...
    def output(self, fileobj: typing.BinaryIO, y4m: bool = False, progress_update: typing.Optional[typing.Callable[[int], int]]=None, prefetch: int = 0) -> None: ...

    def frames(self) -> typing.Generator[VideoFrame, None, None]: ...

    def __add__(self, other: 'VideoNode') -> 'VideoNode': ...
    def __mul__(self, other: int) -> 'VideoNode': ...
    def __getitem__(self, other: typing.Union[int, slice]) -> 'VideoNode': ...
    def __len__(self) -> int: ...


class Core:
# instance_unbound: adg
    @property
    def adg(self) -> _Plugin_adg_Unbound:
        """
        Adaptive grain
        """
# end instance
# instance_unbound: comb
    @property
    def comb(self) -> _Plugin_comb_Unbound:
        """
        comb filters v0.0.1
        """
# end instance
# instance_unbound: d2v
    @property
    def d2v(self) -> _Plugin_d2v_Unbound:
        """
        D2V Source
        """
# end instance
# instance_unbound: descale
    @property
    def descale(self) -> _Plugin_descale_Unbound:
        """
        Undo linear interpolation
        """
# end instance
# instance_unbound: edgefixer
    @property
    def edgefixer(self) -> _Plugin_edgefixer_Unbound:
        """
        VapourSynth edgefixer port
        """
# end instance
# instance_unbound: eedi3m
    @property
    def eedi3m(self) -> _Plugin_eedi3m_Unbound:
        """
        Enhanced Edge Directed Interpolation 3
        """
# end instance
# instance_unbound: ffms2
    @property
    def ffms2(self) -> _Plugin_ffms2_Unbound:
        """
        FFmpegSource 2 for VapourSynth
        """
# end instance
# instance_unbound: fmtc
    @property
    def fmtc(self) -> _Plugin_fmtc_Unbound:
        """
        Format converter, r22
        """
# end instance
# instance_unbound: imwri
    @property
    def imwri(self) -> _Plugin_imwri_Unbound:
        """
        VapourSynth ImageMagick 7 HDRI Writer/Reader
        """
# end instance
# instance_unbound: knlm
    @property
    def knlm(self) -> _Plugin_knlm_Unbound:
        """
        KNLMeansCL for VapourSynth
        """
# end instance
# instance_unbound: lsmas
    @property
    def lsmas(self) -> _Plugin_lsmas_Unbound:
        """
        LSMASHSource for VapourSynth
        """
# end instance
# instance_unbound: mpls
    @property
    def mpls(self) -> _Plugin_mpls_Unbound:
        """
        Get m2ts clip id from a playlist and return a dict
        """
# end instance
# instance_unbound: nnedi3
    @property
    def nnedi3(self) -> _Plugin_nnedi3_Unbound:
        """
        Neural network edge directed interpolation (3rd gen.), v12
        """
# end instance
# instance_unbound: resize
    @property
    def resize(self) -> _Plugin_resize_Unbound:
        """
        VapourSynth Resize
        """
# end instance
# instance_unbound: std
    @property
    def std(self) -> _Plugin_std_Unbound:
        """
        VapourSynth Core Functions
        """
# end instance
# instance_unbound: text
    @property
    def text(self) -> _Plugin_text_Unbound:
        """
        VapourSynth Text
        """
# end instance
# instance_unbound: vinverse
    @property
    def vinverse(self) -> _Plugin_vinverse_Unbound:
        """
        A simple filter to remove residual combing.
        """
# end instance
# instance_unbound: vivtc
    @property
    def vivtc(self) -> _Plugin_vivtc_Unbound:
        """
        VFM
        """
# end instance
# instance_unbound: znedi3
    @property
    def znedi3(self) -> _Plugin_znedi3_Unbound:
        """
        Neural network edge directed interpolation (3rd gen.)
        """
# end instance

    num_threads: int
    max_cache_size: int
    add_cache: bool

    def set_max_cache_size(self, mb: int) -> int: ...
    def get_plugins(self) -> dict: ...
    def list_functions(self) -> str: ...

    def register_format(self, color_family: ColorFamily, sample_type: SampleType, bits_per_sample: int, subsampling_w: int, subsampling_h: int) -> Format: ...
    def get_format(self, id: int) -> Format: ...

    def version(self) -> str: ...
    def version_number(self) -> int: ...


def get_core(threads: typing.Optional[int]=None, add_cache: typing.Optional[bool]=None) -> Core: ...


class _CoreProxy(Core):
    core: Core
core: _CoreProxy
