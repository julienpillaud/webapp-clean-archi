import datetime
import uuid

from app.domain.entities import DomainEntity


class Dummy(DomainEntity):
    uuid_field: uuid.UUID
    string_field: str
    int_field: int
    float_field: float
    bool_field: bool
    date_field: datetime.date
    datetime_field: datetime.datetime
