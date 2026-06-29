from __future__ import annotations

from collections.abc import Callable
from functools import partial, wraps
from typing import Any, overload

from jetpytools import FuncExcept
from vstools import (
    ChromaLocationLike,
    FieldBasedLike,
    HoldsVideoFormat,
    MatrixLike,
    PrimariesLike,
    RangeLike,
    TransferLike,
    VideoFormatLike,
    finalize_clip,
    initialize_clip,
    vs,
)

__all__ = [
    "finalize_clips",
    "initialize_inputs",
]


def _map_vnode(obj: Any, clip_fn: Callable[..., vs.VideoNode], clip_args: dict[str, Any]) -> Any:
    if isinstance(obj, vs.VideoNode):
        return clip_fn(obj, **clip_args)

    return obj


def _map_vnodes_in_result(result: Any, clip_fn: Callable[..., vs.VideoNode], clip_args: dict[str, Any]) -> Any:
    if isinstance(result, vs.VideoNode):
        return clip_fn(result, **clip_args)

    if isinstance(result, tuple):
        return tuple(_map_vnode(item, clip_fn, clip_args) for item in result)

    if isinstance(result, list):
        return [_map_vnode(item, clip_fn, clip_args) for item in result]

    return result


@overload
def initialize_inputs[**P](
    function: Callable[P, vs.VideoNode],
    /,
    *,
    bits: int | None = 32,
    matrix: MatrixLike | None = None,
    transfer: TransferLike | None = None,
    primaries: PrimariesLike | None = None,
    chroma_location: ChromaLocationLike | None = None,
    color_range: RangeLike | None = None,
    field_based: FieldBasedLike | None = None,
    strict: bool = False,
    func: FuncExcept | None = None,
    **kwargs: Any,
) -> Callable[P, vs.VideoNode]: ...


@overload
def initialize_inputs[**P](
    *,
    bits: int | None = 32,
    matrix: MatrixLike | None = None,
    transfer: TransferLike | None = None,
    primaries: PrimariesLike | None = None,
    chroma_location: ChromaLocationLike | None = None,
    color_range: RangeLike | None = None,
    field_based: FieldBasedLike | None = None,
    func: FuncExcept | None = None,
    **kwargs: Any,
) -> Callable[[Callable[P, vs.VideoNode]], Callable[P, vs.VideoNode]]: ...


def initialize_inputs[**P](
    function: Callable[P, vs.VideoNode] | None = None,
    /,
    *,
    bits: int | None = 32,
    matrix: MatrixLike | None = None,
    transfer: TransferLike | None = None,
    primaries: PrimariesLike | None = None,
    chroma_location: ChromaLocationLike | None = None,
    color_range: RangeLike | None = None,
    field_based: FieldBasedLike | None = None,
    strict: bool = False,
    func: FuncExcept | None = None,
    **kwargs: Any,
) -> Callable[P, vs.VideoNode] | Callable[[Callable[P, vs.VideoNode]], Callable[P, vs.VideoNode]]:
    """
    Decorator implementation of initialize_input.

    Unlike `initialize_input`, this decorator initializes *every* clip passed as an argument.
    """

    init_args = dict[str, Any](
        bits=bits,
        matrix=matrix,
        transfer=transfer,
        primaries=primaries,
        chroma_location=chroma_location,
        color_range=color_range,
        field_based=field_based,
        strict=strict,
        func=func,
        **kwargs,
    )

    if function is None:
        return partial(initialize_inputs, **init_args)

    @wraps(function)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> vs.VideoNode:
        args_l = [_map_vnode(obj, initialize_clip, init_args) for obj in args]
        kwargs2 = {name: _map_vnode(obj, initialize_clip, init_args) for name, obj in kwargs.items()}

        return function(*args_l, **kwargs2)

    return _wrapper


@overload
def finalize_clips[**P, R](
    function: Callable[P, R],
    /,
    *,
    bits: VideoFormatLike | HoldsVideoFormat | int | None = 10,
    clamp_tv_range: bool = False,
    func: FuncExcept | None = None,
    **kwargs: Any,
) -> Callable[P, R]: ...


@overload
def finalize_clips[**P, R](
    *,
    bits: VideoFormatLike | HoldsVideoFormat | int | None = 10,
    clamp_tv_range: bool = False,
    func: FuncExcept | None = None,
    **kwargs: Any,
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def finalize_clips[**P, R](
    function: Callable[P, R] | None = None,
    /,
    *,
    bits: VideoFormatLike | HoldsVideoFormat | int | None = 10,
    clamp_tv_range: bool = False,
    func: FuncExcept | None = None,
    **kwargs: Any,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator implementation of finalize_output.

    Unlike `finalize_output`, this decorator finalizes *every* clip in the wrapped function's return value.
    """

    final_args = dict[str, Any](bits=bits, clamp_tv_range=clamp_tv_range, func=func, **kwargs)

    if function is None:
        return partial(finalize_clips, **final_args)

    @wraps(function)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return _map_vnodes_in_result(function(*args, **kwargs), finalize_clip, final_args)

    return _wrapper
