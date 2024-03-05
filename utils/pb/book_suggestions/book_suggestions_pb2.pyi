from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BookSuggestionsRequest(_message.Message):
    __slots__ = ("num_suggestions",)
    NUM_SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    num_suggestions: int
    def __init__(self, num_suggestions: _Optional[int] = ...) -> None: ...

class Book(_message.Message):
    __slots__ = ("title", "author")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_FIELD_NUMBER: _ClassVar[int]
    title: str
    author: str
    def __init__(self, title: _Optional[str] = ..., author: _Optional[str] = ...) -> None: ...

class BookSuggestionsResponse(_message.Message):
    __slots__ = ("suggestions",)
    SUGGESTIONS_FIELD_NUMBER: _ClassVar[int]
    suggestions: _containers.RepeatedCompositeFieldContainer[Book]
    def __init__(self, suggestions: _Optional[_Iterable[_Union[Book, _Mapping]]] = ...) -> None: ...
