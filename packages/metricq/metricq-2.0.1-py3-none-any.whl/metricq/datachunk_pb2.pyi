"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    Optional as typing___Optional,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class DataChunk(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    time_delta: google___protobuf___internal___containers___RepeatedScalarFieldContainer[builtin___int] = ...
    value: google___protobuf___internal___containers___RepeatedScalarFieldContainer[builtin___float] = ...

    def __init__(self,
        *,
        time_delta : typing___Optional[typing___Iterable[builtin___int]] = None,
        value : typing___Optional[typing___Iterable[builtin___float]] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"time_delta",b"time_delta",u"value",b"value"]) -> None: ...
type___DataChunk = DataChunk
