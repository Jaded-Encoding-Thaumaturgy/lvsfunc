from typing import Any

class Backend:
    ORT_CPU: type[Backend]

    @staticmethod
    def autoselect(**kwargs: Any) -> Backend: ...

class ORT_CPU(Backend): ...
