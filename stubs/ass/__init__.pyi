from collections.abc import Iterable, Iterator, MutableMapping, MutableSequence
from datetime import timedelta
from typing import Any, TextIO, TypeVar, overload

__all__ = [
    "Color",
    "Command",
    "Comment",
    "Dialogue",
    "Document",
    "EventsSection",
    "FieldSection",
    "LineSection",
    "Movie",
    "Picture",
    "ScriptInfoSection",
    "Sound",
    "Style",
    "StylesSection",
    "Unknown",
    "parse",
    "parse_file",
    "parse_string",
]

_T = TypeVar("_T")

class Color:
    WHITE: Color
    RED: Color
    BLACK: Color

    r: int
    g: int
    b: int
    a: int

    def __init__(self, r: int, g: int, b: int, a: int = 0) -> None: ...
    def to_int(self) -> int: ...
    def to_ass(self) -> str: ...
    @classmethod
    def from_ass(cls, v: str) -> Color: ...

class _Line:
    TYPE: str | None
    fields: dict[str, Any]
    DEFAULT_FIELD_ORDER: list[str]

    def __init__(self, *args: Any, type_name: str | None = None, **kwargs: Any) -> None: ...
    def dump(self, field_order: list[str] | None = None) -> str: ...
    def dump_with_type(self, field_order: list[str] | None = None) -> str: ...
    @classmethod
    def parse(cls, type_name: str, line: str, field_order: list[str] | None = None) -> _Line: ...

class Unknown(_Line):
    value: str

class Style(_Line):
    name: str
    fontname: str
    fontsize: float
    primary_color: Color
    secondary_color: Color
    outline_color: Color
    back_color: Color
    bold: bool
    italic: bool
    underline: bool
    strike_out: bool
    scale_x: float
    scale_y: float
    spacing: float
    angle: float
    border_style: int
    outline: float
    shadow: float
    alignment: int
    margin_l: int
    margin_r: int
    margin_v: int
    encoding: int

class _Event(_Line):
    layer: int
    start: timedelta
    end: timedelta
    style: str
    name: str
    margin_l: int
    margin_r: int
    margin_v: int
    effect: str
    text: str

class Dialogue(_Event): ...
class Comment(_Event): ...
class Picture(_Event): ...
class Sound(_Event): ...
class Movie(_Event): ...
class Command(_Event): ...

class LineSection(MutableSequence[_T]):
    FORMAT_TYPE: str
    name: str
    field_order: list[str] | None
    line_parsers: dict[str, type[_Line]] | None

    def __init__(self, name: str, lines: list[_T] | None = None) -> None: ...
    def dump(self) -> Iterator[str]: ...
    def add_line(self, type_name: str, raw_line: str) -> None: ...
    def set_data(self, lines: MutableSequence[_T]) -> None: ...
    @overload
    def __getitem__(self, index: int) -> _T: ...
    @overload
    def __getitem__(self, index: slice) -> MutableSequence[_T]: ...
    @overload
    def __setitem__(self, index: int, val: _T) -> None: ...
    @overload
    def __setitem__(self, index: slice, val: Iterable[_T]) -> None: ...
    @overload
    def __delitem__(self, index: int) -> None: ...
    @overload
    def __delitem__(self, index: slice) -> None: ...
    def __len__(self) -> int: ...
    def insert(self, index: int, val: _T) -> None: ...

class FieldSection(MutableMapping[str, Any]):
    FIELDS: dict[str, Any]
    name: str

    def __init__(self, name: str, fields: MutableMapping[str, Any] | None = None) -> None: ...
    def add_line(self, field_name: str, field: str) -> None: ...
    def dump(self) -> Iterator[str]: ...
    def set_data(self, fields: MutableMapping[str, Any]) -> None: ...
    def __contains__(self, key: object) -> bool: ...
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def clear(self) -> None: ...
    def copy(self) -> FieldSection: ...

class EventsSection(LineSection[_Event]): ...
class StylesSection(LineSection[Style]): ...

class ScriptInfoSection(FieldSection):
    VERSION_ASS: str
    VERSION_SSA: str

class Document:
    SCRIPT_INFO_HEADER: str
    STYLE_SSA_HEADER: str
    STYLE_ASS_HEADER: str
    EVENTS_HEADER: str
    AEGISUB_PROJECT_HEADER: str
    PREFERRED_ENCODING: Any
    SECTIONS: Any
    DEFAULT_SECTION_HEADERS: list[str]

    sections: Any
    script_type: str
    play_res_x: int
    play_res_y: int
    wrap_style: int
    scaled_border_and_shadow: str
    info: ScriptInfoSection
    fields: ScriptInfoSection
    styles: StylesSection
    events: EventsSection

    def __init__(self) -> None: ...
    @classmethod
    def parse_file(cls, f: TextIO | Iterable[str]) -> Document: ...
    @classmethod
    def parse_string(cls, string: str) -> Document: ...
    @classmethod
    def is_preferred_encoding(cls, encoding: str) -> bool: ...
    def dump_file(self, f: TextIO) -> None: ...

def parse_file(f: TextIO | Iterable[str]) -> Document: ...
def parse_string(string: str) -> Document: ...
def parse(f: TextIO | Iterable[str]) -> Document: ...
