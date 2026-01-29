import pytest

from app.api.utils import parse_filters
from app.domain.filters import FilterEntity, FilterOperator


@pytest.mark.parametrize(
    "filters",
    [
        # wrong pattern
        [""],
        ["="],
        ["field"],
        ["field="],
        ["=value"],
        ["field[=value"],
        ["field]=value"],
        ["field[]=value"],
        ["[gt]=value"],
        ["field[a]=value"],
        ["field[eq]=value"],
        # wrong list format
        ["field[in]=value,"],
        ["field[in]=,value"],
        ["field[in]=value1,,value2"],
        # unauthorized list
        ["field[gt]=value1,value2"],
    ],
)
def test_parse_filters_wrong_format(filters: list[str]) -> None:
    with pytest.raises(ValueError):
        parse_filters(filters)


def test_parse_filters_eq() -> None:
    assert parse_filters(["field=value"]) == (
        [FilterEntity(field="field", value="value", operator=FilterOperator.EQ)]
    )


@pytest.mark.parametrize(
    "operator",
    [
        FilterOperator.GT,
        FilterOperator.GTE,
        FilterOperator.LT,
        FilterOperator.LTE,
    ],
)
def test_parse_filters_scalar(operator: FilterOperator) -> None:
    assert parse_filters([f"field[{operator}]=value"]) == (
        [FilterEntity(field="field", value="value", operator=operator)]
    )


@pytest.mark.parametrize(
    "operator",
    [FilterOperator.IN, FilterOperator.NIN],
)
def test_parse_filters_multiple(operator: FilterOperator) -> None:
    assert parse_filters([f"field[{operator}]=value1,value2"]) == (
        [
            FilterEntity(
                field="field",
                value=["value1", "value2"],
                operator=operator,
            )
        ]
    )
