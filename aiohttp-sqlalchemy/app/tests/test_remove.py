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
        "login": "sameemail@example.com",
        "password": "password123"
    }
    user_storage.add_entity(**user)

    assert user_storage.entity_exists(**user)

    user_storage.remove_entity(**user)

    assert user_storage.entity_exists(**user) is False
