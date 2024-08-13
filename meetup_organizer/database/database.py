from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session

from meetup_organizer.shared.settings import Settings

connection_string = URL.create(
    'postgresql',
    username=Settings().DATABASE_USERNAME,  # type: ignore
    password=Settings().DATABASE_PASSWORD,  # type: ignore
    host=Settings().DATABASE_HOST,  # type: ignore
    database=Settings().DATABASE_NAME,  # type: ignore
)

engine = create_engine(connection_string)


def get_database_session():
    with Session(engine) as session:
        yield session
