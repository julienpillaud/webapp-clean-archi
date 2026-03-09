import datetime
import uuid

from cleanstack.entities import DomainEntity


class Dummy(DomainEntity):
    uuid_field: uuid.UUID
    string_field: str
    int_field: int
    float_field: float
    bool_field: bool
    datetime_field: datetime.datetime
