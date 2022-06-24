from __future__ import annotations

from typing import Any, Collection, Iterator, List, TypeVar

# flake8: noqa

__all__: List[str] = [
    'BarColumn',
    'FPSColumn',
    'Progress',
    'TextColumn',
    'TimeRemainingColumn'
]

T = TypeVar("T")

try:
    from rich.progress import BarColumn, Progress, ProgressColumn, Task, TextColumn, TimeRemainingColumn
    from rich.text import Text

    class FPSColumn(ProgressColumn):
        def render(self, task: Task) -> Text:
            return Text(f"{task.speed or 0:.02f} fps")

except (ImportError, ModuleNotFoundError):
    class Progress:  # type: ignore
        description: str
        i: int
        total: int

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.i = 0
            pass

        def _print(self) -> None:
            print(f"{self.description} {self.i:d}/{self.total:d} frames", end="\r")

        def track(self, x: Collection[T], description: str = "", total: int = 0) -> Iterator[T]:
            self.total = total
            self.description = description
            for y in x:
                self.i += 1
                self._print()
                yield y

        def update(self, *args: Any, advance: int = 0, **kwargs: Any) -> None:
            self.i += advance
            self._print()

        def add_task(self, description: str, *args: Any, total: int = 0, **kwargs: Any) -> None:
            self.description = description
            self.total = total

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
