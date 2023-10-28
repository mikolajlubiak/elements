from typing import Optional, List, TypeVar
from contextlib import contextmanager

from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from backend.database.tables import User


class BaseStorage:
    T = TypeVar('T')

    def __init__(self, database, model: T):
        self._db = database
        self._model = model

    @contextmanager
    def get_session(self):
        with Session(self._db) as session:
            yield session

    def fetch_all(self) -> List[T]:
        with self.get_session() as session_db:
            return session_db.scalars(select(self._model)).all()

    def entity_exists(self, **kwargs) -> bool:
        with self.get_session() as session_db:
            exists_query = exists().where(
                    *[
                        getattr(self._model, attr) == value
                        for attr, value in kwargs.items()
                        ]
                    )
            return session_db.query(exists_query).scalar()

    def add_entity(self, **kwargs) -> None:
        entity = self._model(**kwargs)
        with self.get_session() as session_db:
            session_db.add(entity)
            session_db.commit()

    def update_entity(self, select_attrs: dict, update_attrs: dict) -> None:
        upd_stmt = select(self._model).where(
            *[
                getattr(self._model, attr) == value
                for attr, value in select_attrs.items()
            ]
        )
        with self.get_session() as session_db:
            try:
                entity = session_db.scalars(upd_stmt).one()
                for attr, value in update_attrs.items():
                    setattr(entity, attr, value)
                session_db.commit()
            except NoResultFound:
                raise NoResultFound("Entity not found")

    def remove_entity(self, **kwargs) -> None:
        del_stmt = select(self._model).where(
            *[
                getattr(self._model, attr) == value
                for attr, value in kwargs.items()
            ]
        )
        with self.get_session() as session_db:
            try:
                entity = session_db.scalars(del_stmt).one()
                session_db.delete(entity)
                session_db.commit()
            except NoResultFound:
                raise NoResultFound("Entity not found")

    def get_entity_by_attributes(self, **kwargs) -> Optional[T]:
        stmt = select(self._model).where(
                *[
                    getattr(self._model, attr) == value
                    for attr, value in kwargs.items()
                    ]
                )
        with self.get_session() as session_db:
            try:
                return session_db.scalars(stmt).one()
            except:
                return None


class UserStorage(BaseStorage):
    def __init__(self, database):
        super().__init__(database, User)
