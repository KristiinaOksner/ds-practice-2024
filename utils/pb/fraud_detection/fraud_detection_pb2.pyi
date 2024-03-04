from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CheckRequest(_message.Message):
    __slots__ = ("user_id", "order_amounts")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_AMOUNTS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    order_amounts: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, user_id: _Optional[str] = ..., order_amounts: _Optional[_Iterable[float]] = ...) -> None: ...

class FraudCheckResponse(_message.Message):
    __slots__ = ("is_fraudulent", "reason")
    IS_FRAUDULENT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    is_fraudulent: bool
    reason: str
    def __init__(self, is_fraudulent: bool = ..., reason: _Optional[str] = ...) -> None: ...
