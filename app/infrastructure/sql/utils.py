import datetime
import uuid
from typing import Any

from sqlalchemy import (
    Boolean,
    ColumnExpressionArgument,
    Date,
    DateTime,
    Float,
    Integer,
    Select,
    String,
    Uuid,
    func,
    or_,
    select,
)
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.interfaces import ORMOption

from app.domain.entities import Pagination
from app.domain.filters import FilterEntity, FilterOperator
from app.infrastructure.sql.entities import OrmEntity, QuerySet
from app.infrastructure.sql.exceptions import InvalidFilterError


class SQLQueryBuilder[T: OrmEntity]:
    def __init__(
        self,
        model: type[T],
        select_options: tuple[ORMOption, ...],
        filterable_fields: dict[str, InstrumentedAttribute[Any]],
        searchable_fields: tuple[InstrumentedAttribute[Any], ...],
    ) -> None:
        self.model = model
        self.select_options = select_options
        self.filterable_fields = filterable_fields
        self.searchable_fields = searchable_fields

    def build(
        self,
        *,
        search: str | None = None,
        filters: list[FilterEntity] | None = None,
        pagination: Pagination,
    ) -> QuerySet[T]:
        stmt = select(self.model)
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_search(stmt, search)

        count_stmt = select(func.count()).select_from(stmt.subquery())

        if self.select_options:
            stmt = stmt.options(*self.select_options)

        stmt = self._apply_pagination(stmt, pagination)

        return QuerySet(count=count_stmt, data=stmt)

    def _apply_filters(
        self,
        stmt: Select[tuple[T]],
        /,
        filters: list[FilterEntity] | None,
    ) -> Select[tuple[T]]:
        if not filters:
            return stmt

        for filter_entity in filters:
            column = self.filterable_fields.get(filter_entity.field)
            if not column:
                raise InvalidFilterError("Unauthorized field.")

            value = convert_filter_value(
                column=column,
                filter_value=filter_entity.value,
                operator=filter_entity.operator,
            )
            clause = apply_operator(
                column=column,
                operator=filter_entity.operator,
                value=value,
            )
            stmt = stmt.where(clause)

        return stmt

    def _apply_search(
        self,
        stmt: Select[tuple[T]],
        /,
        search: str | None,
    ) -> Select[tuple[T]]:
        if not search:
            return stmt

        conditions = [field.ilike(f"%{search}%") for field in self.searchable_fields]
        return stmt.where(or_(*conditions))

    @staticmethod
    def _apply_pagination(
        stmt: Select[tuple[T]],
        /,
        pagination: Pagination,
    ) -> Select[tuple[T]]:
        return stmt.offset(pagination.skip).limit(pagination.limit)


CONVERTERS = {
    Boolean: lambda value: value == "true",
    Date: datetime.date.fromisoformat,
    DateTime: datetime.datetime.fromisoformat,
    Float: float,
    Integer: int,
    String: str,
    Uuid: uuid.UUID,
}


def get_converter(column: InstrumentedAttribute[Any]) -> Any:
    for column_type, converter in CONVERTERS.items():
        if isinstance(column.type, column_type):
            return converter

    raise InvalidFilterError("Unsupported type.")


def convert_filter_value(
    column: InstrumentedAttribute[Any],
    filter_value: str | list[str],
    operator: FilterOperator,
) -> Any:
    if isinstance(filter_value, list):
        return [
            cast_filter_value(
                column=column,
                operator=operator,
                filter_value=value,
            )
            for value in filter_value
        ]
    return cast_filter_value(
        column=column,
        operator=operator,
        filter_value=filter_value,
    )


def cast_filter_value(
    column: InstrumentedAttribute[Any],
    operator: FilterOperator,
    filter_value: str,
) -> Any:
    if isinstance(column.type, (Uuid, String)) and operator not in (
        FilterOperator.EQ,
        FilterOperator.IN,
        FilterOperator.NIN,
    ):
        raise InvalidFilterError("Unsupported operator.")

    if isinstance(column.type, Boolean):
        if operator != FilterOperator.EQ:
            raise InvalidFilterError("Unsupported operator.")
        if filter_value not in ("true", "false"):
            raise InvalidFilterError("Invalid value format.")

    converter = get_converter(column)
    try:
        return converter(filter_value)
    except ValueError as error:
        raise InvalidFilterError("Invalid value format.") from error


def apply_operator(
    column: InstrumentedAttribute[Any],
    operator: FilterOperator,
    value: Any,
) -> ColumnExpressionArgument[bool]:
    match operator:
        case FilterOperator.EQ:
            return column == value
        case FilterOperator.GT:
            return column > value
        case FilterOperator.LT:
            return column < value
        case FilterOperator.GTE:
            return column >= value
        case FilterOperator.LTE:
            return column <= value
        case FilterOperator.IN:
            return column.in_(value)
        case FilterOperator.NIN:
            return column.notin_(value)
