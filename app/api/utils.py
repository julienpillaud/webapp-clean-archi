import re

from pydantic import BaseModel, NonNegativeInt

from app.domain.filters import FilterEntity, FilterOperator


class PaginatedResponseDTO[T: BaseModel](BaseModel):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]


SEPARATOR = "="
OPERATORS = "|".join(value for value in FilterOperator if value != FilterOperator.EQ)
FILTER_PATTERN = re.compile(
    r"^([a-zA-Z0-9_]+)"  # Start with the field
    r"(?:\["  # Optional operator surrounded by brackets
    rf"({OPERATORS})"
    r"])?"
    rf"{SEPARATOR}"
    r"([a-zA-Z0-9_,.:-]+)$"  # End with the value
)


def parse_filters(filters: list[str], /) -> list[FilterEntity]:
    filter_entities = []
    for filter_ in filters:
        match = FILTER_PATTERN.match(filter_)
        if not match:
            raise ValueError("Invalid filter format.")

        field, operator_str, value_part = match.groups()
        operator = FilterOperator(operator_str) if operator_str else FilterOperator.EQ

        if operator in (FilterOperator.IN, FilterOperator.NIN):
            value = value_part.split(",")
            if "" in value:
                raise ValueError("Invalid filter format.")
        else:
            if "," in value_part:
                raise ValueError("Invalid filter format.")
            value = value_part

        filter_entities.append(
            FilterEntity(
                field=field,
                value=value,
                operator=operator,
            )
        )

    return filter_entities
