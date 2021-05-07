from typing import Any, Collection, Iterator, TypeVar

__all__ = ["BarColumn", "Progress", "TextColumn", "TimeRemainingColumn", "FPSColumn"]

T = TypeVar("T")

try:
    from rich.progress import BarColumn, Progress, ProgressColumn, TextColumn, Task, TimeRemainingColumn
    from rich.text import Text

    class FPSColumn(ProgressColumn):
        def render(self, task: Task) -> Text:
            return Text(f"{task.speed or 0:.02f} fps")

except (ImportError, ModuleNotFoundError):
    class Progress:  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def track(self, x: Collection[T], description: str = "", total: int = 0) -> Iterator[T]:
            i = 0
            for y in x:
                i += 1
                print(f"{description} {i}/{total} frames", end="\r")
                yield y

        def __enter__(self) -> None:
            pass

        def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
            pass

    class BarColumn:  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

    class TextColumn:  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

    class TimeRemainingColumn:  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

    class FPSColumn:  # type: ignore
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass
