from typing import Protocol
from typing import Dict
from typing import runtime_checkable

@runtime_checkable
class OutputRecord(Protocol):
    _api: str
    def dict(self) -> Dict: ...
    def schema(self) -> Dict: ...

@runtime_checkable
class OutputModel(Protocol):
    _api: str
    __private_attributes__: Dict
    def schema(self) -> Dict: ...