from typing import Any

assoc: Any
assoc_in: Any
copy: Any
dissoc: Any
get_in: Any
itemfilter: Any
itemmap: Any
keyfilter: Any
keymap: Any
merge: Any
merge_with: Any
update_in: Any
valfilter: Any
valmap: Any

class _iter_mapping:
    @classmethod
    def __init__(self, *args, **kwargs) -> None: ...
    def __iter__(self) -> Any: ...
    def __next__(self) -> Any: ...
    def __reduce__(self) -> Any: ...
    def __setstate__(self, state) -> Any: ...
