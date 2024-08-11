from jwt import decode

from meetup_organizer.shared.security import create_access_token
from meetup_organizer.shared.settings import Settings


def test_generate_jwt():
    token = create_access_token({'sub': 'test'})
    decoded_token = decode(token, Settings().SECRET_KEY, Settings().ALGORITHM)  # type: ignore
    assert decoded_token['sub'] == 'test'
    assert decoded_token['exp']
