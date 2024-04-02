from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OrderQueueRequest(_message.Message):
    __slots__ = ("is_valid", "orderID")
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    is_valid: bool
    orderID: str
    def __init__(self, is_valid: bool = ..., orderID: _Optional[str] = ...) -> None: ...

class OrderQueueResponse(_message.Message):
    __slots__ = ("is_in_queue", "message")
    IS_IN_QUEUE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    is_in_queue: bool
    message: str
    def __init__(self, is_in_queue: bool = ..., message: _Optional[str] = ...) -> None: ...
