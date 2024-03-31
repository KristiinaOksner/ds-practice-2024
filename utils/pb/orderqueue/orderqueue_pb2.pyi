from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("name", "contact")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTACT_FIELD_NUMBER: _ClassVar[int]
    name: str
    contact: str
    def __init__(self, name: _Optional[str] = ..., contact: _Optional[str] = ...) -> None: ...

class CreditCard(_message.Message):
    __slots__ = ("number", "expirationDate", "cvv")
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    EXPIRATIONDATE_FIELD_NUMBER: _ClassVar[int]
    CVV_FIELD_NUMBER: _ClassVar[int]
    number: str
    expirationDate: str
    cvv: str
    def __init__(self, number: _Optional[str] = ..., expirationDate: _Optional[str] = ..., cvv: _Optional[str] = ...) -> None: ...

class Book(_message.Message):
    __slots__ = ("name", "quantity")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: int
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[int] = ...) -> None: ...

class BillingAddress(_message.Message):
    __slots__ = ("street", "city", "state", "zip", "country")
    STREET_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ZIP_FIELD_NUMBER: _ClassVar[int]
    COUNTRY_FIELD_NUMBER: _ClassVar[int]
    street: str
    city: str
    state: str
    zip: str
    country: str
    def __init__(self, street: _Optional[str] = ..., city: _Optional[str] = ..., state: _Optional[str] = ..., zip: _Optional[str] = ..., country: _Optional[str] = ...) -> None: ...

class Device(_message.Message):
    __slots__ = ("type", "model", "os")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    OS_FIELD_NUMBER: _ClassVar[int]
    type: str
    model: str
    os: str
    def __init__(self, type: _Optional[str] = ..., model: _Optional[str] = ..., os: _Optional[str] = ...) -> None: ...

class Order(_message.Message):
    __slots__ = ("user", "creditCard", "billingAddress", "books", "userComment", "shippingMethod", "giftMessage", "giftWrapping", "device")
    USER_FIELD_NUMBER: _ClassVar[int]
    CREDITCARD_FIELD_NUMBER: _ClassVar[int]
    BILLINGADDRESS_FIELD_NUMBER: _ClassVar[int]
    BOOKS_FIELD_NUMBER: _ClassVar[int]
    USERCOMMENT_FIELD_NUMBER: _ClassVar[int]
    SHIPPINGMETHOD_FIELD_NUMBER: _ClassVar[int]
    GIFTMESSAGE_FIELD_NUMBER: _ClassVar[int]
    GIFTWRAPPING_FIELD_NUMBER: _ClassVar[int]
    DEVICE_FIELD_NUMBER: _ClassVar[int]
    user: User
    creditCard: CreditCard
    billingAddress: BillingAddress
    books: _containers.RepeatedCompositeFieldContainer[Book]
    userComment: str
    shippingMethod: str
    giftMessage: str
    giftWrapping: str
    device: Device
    def __init__(self, user: _Optional[_Union[User, _Mapping]] = ..., creditCard: _Optional[_Union[CreditCard, _Mapping]] = ..., billingAddress: _Optional[_Union[BillingAddress, _Mapping]] = ..., books: _Optional[_Iterable[_Union[Book, _Mapping]]] = ..., userComment: _Optional[str] = ..., shippingMethod: _Optional[str] = ..., giftMessage: _Optional[str] = ..., giftWrapping: _Optional[str] = ..., device: _Optional[_Union[Device, _Mapping]] = ...) -> None: ...

class EnqueueOrderRequest(_message.Message):
    __slots__ = ("order",)
    ORDER_FIELD_NUMBER: _ClassVar[int]
    order: Order
    def __init__(self, order: _Optional[_Union[Order, _Mapping]] = ...) -> None: ...

class EnqueueOrderResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class DequeueOrderRequest(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class DequeueOrderResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
