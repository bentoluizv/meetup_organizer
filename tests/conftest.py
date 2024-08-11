import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from meetup_organizer.app import app
from meetup_organizer.database.models import Base, UserDb
from meetup_organizer.schemas.user import CreationalUserSchema, User
from meetup_organizer.shared.security import create_access_token


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer() as postgres:
        _engine = create_engine(postgres.get_connection_url())
        with _engine.begin():
            yield _engine


@pytest.fixture()
def session(engine):
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)


@pytest.fixture()
def user_db(session):
    new_user = User.create(
        CreationalUserSchema(
            username='test', password1='testtest', password2='testtest'
        )
    )
    user_db = UserDb(**new_user.model_dump())
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    user_db.clean_password = 'testtest'  # type: ignore
    return user_db


@pytest.fixture()
def token(user_db):
    token = create_access_token({'sub': user_db.username})
    return token
