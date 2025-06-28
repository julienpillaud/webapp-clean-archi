import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.sql.models import OrmUser
from app.utils.sqlalchemy_instrument import SQLAlchemyInstrument


def test_sqlalchemy_instrument_init_error() -> None:
    with pytest.raises(RuntimeError):
        SQLAlchemyInstrument()


def test_sqlalchemy_instrument_record(session: Session) -> None:
    expected_queries = 1

    with SQLAlchemyInstrument.record() as instrument:
        assert instrument.queries_count == 0

        session.execute(select(OrmUser)).scalars().all()

    assert instrument.total_duration > 0
    assert instrument.queries_count == expected_queries

    with SQLAlchemyInstrument.record() as instrument:
        assert instrument.queries_count == 0


def test_sqlalchemy_instrument_record_with_commit(session: Session) -> None:
    expected_queries = 2

    with SQLAlchemyInstrument.record() as instrument:
        session.execute(select(OrmUser)).scalars().all()
        session.commit()
        session.execute(select(OrmUser)).scalars().all()

        assert instrument.queries_count == expected_queries
