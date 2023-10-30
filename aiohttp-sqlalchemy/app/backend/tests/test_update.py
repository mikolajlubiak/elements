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


def test_update_user(user_storage):
    user = {
            "login": "email@example.com",
            "password": "password123"
            }
    user_storage.add_entity(**user)

    assert user_storage.entity_exists(**user)

    change_password = {
            "password": "password1234"
            }

    user_storage.update_entity(change_password)

    entity = user_storage.get_entity_by_attributes(login="email@example.com")

    assert entity.password == "password1234"

def test_update_non_existent_user(user_storage):
    with pytest.raises(NoResultFound):
        user_storage.update_entity({"login": "non_existent@example.com"})
        assert user_storage.entity_exists(login="non_existent@example.com") is False

