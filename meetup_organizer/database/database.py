from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from meetup_organizer.shared.settings import Settings

engine = create_engine(Settings().DATABASE_URL)  # type: ignore


def get_database_session():
    with Session(engine) as session:
        yield session
