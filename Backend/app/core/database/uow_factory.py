from contextlib import contextmanager
from typing import Callable, Iterator

from sqlalchemy.orm import Session

from app.core.database.connection import SessionLocal
from app.core.database.sql_unit_of_work import SqlAlchemyUnitOfWork
from app.core.database.unit_of_work import UnitOfWork


def crear_unit_of_work(session: Session) -> UnitOfWork:
    return SqlAlchemyUnitOfWork(session)


@contextmanager
def abrir_unit_of_work(
    session_factory: Callable[[], Session] = SessionLocal,
) -> Iterator[UnitOfWork]:
    session = session_factory()

    try:
        uow = crear_unit_of_work(session)
        with uow:
            yield uow
    finally:
        session.close()
