import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from meetup_organizer.database.models import Base


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(
        'postgresql://postgres:postgres@127.0.0.1:54322/postgres'
    )
    return engine


@pytest.fixture()
def session(engine):
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
