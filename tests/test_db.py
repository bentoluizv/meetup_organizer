from datetime import datetime

from sqlalchemy import select

from meetup_organizer.database.models import MeetupDb, UserDb


def test_create_meetup(session):
    new_meetup = MeetupDb(
        title='78 Meetup Python Floripa',
        description='Descrição do Evento',
        location='Senai Florianópolis',
        date=datetime(2024, 8, 31, 14),
        attendees=[],
    )
    session.add(new_meetup)
    session.commit()

    meetup = session.scalar(
        select(MeetupDb).where(MeetupDb.title == '78 Meetup Python Floripa')
    )

    assert meetup.location == 'Senai Florianópolis'


def test_get_user(session, user_db):
    exists = session.scalar(select(UserDb).where(UserDb.uuid == user_db.uuid))
    assert exists.username == 'test'
