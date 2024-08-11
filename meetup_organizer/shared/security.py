from datetime import datetime, timedelta

from jwt import encode
from zoneinfo import ZoneInfo

from meetup_organizer.shared.settings import Settings

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encoded_jwt = encode(
        payload=to_encode,
        key=Settings().SECRET_KEY,  # type: ignore
        algorithm=Settings().ALGORITHM,  # type: ignore
    )
    return encoded_jwt
