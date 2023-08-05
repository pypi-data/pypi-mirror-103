"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from google.protobuf.descriptor import (
    Descriptor as google___protobuf___descriptor___Descriptor,
    EnumDescriptor as google___protobuf___descriptor___EnumDescriptor,
    FileDescriptor as google___protobuf___descriptor___FileDescriptor,
)

from google.protobuf.internal.containers import (
    RepeatedCompositeFieldContainer as google___protobuf___internal___containers___RepeatedCompositeFieldContainer,
    RepeatedScalarFieldContainer as google___protobuf___internal___containers___RepeatedScalarFieldContainer,
)

from google.protobuf.internal.enum_type_wrapper import (
    _EnumTypeWrapper as google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper,
)

from google.protobuf.message import (
    Message as google___protobuf___message___Message,
)

from typing import (
    Iterable as typing___Iterable,
    NewType as typing___NewType,
    Optional as typing___Optional,
    Text as typing___Text,
    cast as typing___cast,
)

from typing_extensions import (
    Literal as typing_extensions___Literal,
)


builtin___bool = bool
builtin___bytes = bytes
builtin___float = float
builtin___int = int


DESCRIPTOR: google___protobuf___descriptor___FileDescriptor = ...

class HistoryRequest(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    RequestTypeValue = typing___NewType('RequestTypeValue', builtin___int)
    type___RequestTypeValue = RequestTypeValue
    RequestType: _RequestType
    class _RequestType(google___protobuf___internal___enum_type_wrapper____EnumTypeWrapper[HistoryRequest.RequestTypeValue]):
        DESCRIPTOR: google___protobuf___descriptor___EnumDescriptor = ...
        AGGREGATE_TIMELINE = typing___cast(HistoryRequest.RequestTypeValue, 0)
        AGGREGATE = typing___cast(HistoryRequest.RequestTypeValue, 1)
        LAST_VALUE = typing___cast(HistoryRequest.RequestTypeValue, 2)
        FLEX_TIMELINE = typing___cast(HistoryRequest.RequestTypeValue, 3)
    AGGREGATE_TIMELINE = typing___cast(HistoryRequest.RequestTypeValue, 0)
    AGGREGATE = typing___cast(HistoryRequest.RequestTypeValue, 1)
    LAST_VALUE = typing___cast(HistoryRequest.RequestTypeValue, 2)
    FLEX_TIMELINE = typing___cast(HistoryRequest.RequestTypeValue, 3)

    start_time: builtin___int = ...
    end_time: builtin___int = ...
    interval_max: builtin___int = ...
    type: type___HistoryRequest.RequestTypeValue = ...

    def __init__(self,
        *,
        start_time : typing___Optional[builtin___int] = None,
        end_time : typing___Optional[builtin___int] = None,
        interval_max : typing___Optional[builtin___int] = None,
        type : typing___Optional[type___HistoryRequest.RequestTypeValue] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"end_time",b"end_time",u"interval_max",b"interval_max",u"start_time",b"start_time",u"type",b"type"]) -> None: ...
type___HistoryRequest = HistoryRequest

class HistoryResponse(google___protobuf___message___Message):
    DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
    class Aggregate(google___protobuf___message___Message):
        DESCRIPTOR: google___protobuf___descriptor___Descriptor = ...
        minimum: builtin___float = ...
        maximum: builtin___float = ...
        sum: builtin___float = ...
        count: builtin___int = ...
        integral: builtin___float = ...
        active_time: builtin___int = ...

        def __init__(self,
            *,
            minimum : typing___Optional[builtin___float] = None,
            maximum : typing___Optional[builtin___float] = None,
            sum : typing___Optional[builtin___float] = None,
            count : typing___Optional[builtin___int] = None,
            integral : typing___Optional[builtin___float] = None,
            active_time : typing___Optional[builtin___int] = None,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions___Literal[u"active_time",b"active_time",u"count",b"count",u"integral",b"integral",u"maximum",b"maximum",u"minimum",b"minimum",u"sum",b"sum"]) -> None: ...
    type___Aggregate = Aggregate

    metric: typing___Text = ...
    time_delta: google___protobuf___internal___containers___RepeatedScalarFieldContainer[builtin___int] = ...
    value_min: google___protobuf___internal___containers___RepeatedScalarFieldContainer[builtin___float] = ...
    value_max: google___protobuf___internal___containers___RepeatedScalarFieldContainer[builtin___float] = ...
    value_avg: google___protobuf___internal___containers___RepeatedScalarFieldContainer[builtin___float] = ...
    value: google___protobuf___internal___containers___RepeatedScalarFieldContainer[builtin___float] = ...
    error: typing___Text = ...

    @property
    def aggregate(self) -> google___protobuf___internal___containers___RepeatedCompositeFieldContainer[type___HistoryResponse.Aggregate]: ...

    def __init__(self,
        *,
        metric : typing___Optional[typing___Text] = None,
        time_delta : typing___Optional[typing___Iterable[builtin___int]] = None,
        value_min : typing___Optional[typing___Iterable[builtin___float]] = None,
        value_max : typing___Optional[typing___Iterable[builtin___float]] = None,
        value_avg : typing___Optional[typing___Iterable[builtin___float]] = None,
        aggregate : typing___Optional[typing___Iterable[type___HistoryResponse.Aggregate]] = None,
        value : typing___Optional[typing___Iterable[builtin___float]] = None,
        error : typing___Optional[typing___Text] = None,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions___Literal[u"aggregate",b"aggregate",u"error",b"error",u"metric",b"metric",u"time_delta",b"time_delta",u"value",b"value",u"value_avg",b"value_avg",u"value_max",b"value_max",u"value_min",b"value_min"]) -> None: ...
type___HistoryResponse = HistoryResponse
