from typing import Any

class Backend:
    @staticmethod
    def autoselect(**kwargs: Any) -> Backend: ...

class ORT_CPU(Backend): ...
