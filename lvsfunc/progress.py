from __future__ import annotations

from rich.progress import BarColumn, Progress, ProgressColumn, Task, TextColumn, TimeRemainingColumn
from rich.text import Text

__all__ = [
    'BarColumn',
    'FPSColumn',
    'Progress',
    'TextColumn',
    'TimeRemainingColumn'
]


class FPSColumn(ProgressColumn):
    def render(self, task: Task) -> Text:
        return Text(f"{task.speed or 0:.02f} fps")
