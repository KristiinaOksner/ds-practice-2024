from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FraudDetectionRequest(_message.Message):
    __slots__ = ("country", "city")
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    country: str
    city: str
    def __init__(self, country: _Optional[str] = ..., city: _Optional[str] = ...) -> None: ...

class FraudDetectionResponse(_message.Message):
    __slots__ = ("is_fraudulent", "reason")
    IS_FRAUDULENT_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    is_fraudulent: bool
    reason: str
    def __init__(self, is_fraudulent: bool = ..., reason: _Optional[str] = ...) -> None: ...
