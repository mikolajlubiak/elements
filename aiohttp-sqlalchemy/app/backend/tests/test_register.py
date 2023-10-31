import pytest
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from backend.database.storage import UserStorage
from backend.database.tables import Base
from backend.database.engine import get_db

engine = get_db()

@pytest.fixture
def init_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def user_storage(init_database):
    return UserStorage(engine)


def test_register_user(user_storage):
    user = {
            "login": "email@example.com",
            "password": "password123"
            }
    user_storage.add_entity(**user)

    assert user_storage.entity_exists(**user)

def test_register_existing_user(user_storage):
    existing_user = {
            "login": "email@example.com",
            "password": "password123"
            }
    user_storage.add_entity(**existing_user)

    new_user = {
            "login": "email@example.com",
            "password": "qwe7112"
            }

    with pytest.raises(IntegrityError):
        user_storage.add_entity(**new_user)
