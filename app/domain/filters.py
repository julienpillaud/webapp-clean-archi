from enum import StrEnum

from pydantic import BaseModel


class FilterOperator(StrEnum):
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    GTE = "gte"
    LTE = "lte"
    IN = "in"
    NIN = "nin"


class FilterEntity(BaseModel):
    field: str
    value: str | list[str]
    operator: FilterOperator = FilterOperator.EQ
