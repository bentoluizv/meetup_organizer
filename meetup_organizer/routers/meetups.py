from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from meetup_organizer.database.database import get_database_session
from meetup_organizer.database.models import MeetupDb
from meetup_organizer.schemas.attendee import Attendee
from meetup_organizer.schemas.meetup import Meetup
from meetup_organizer.shared.security import get_current_user

router = APIRouter(
    prefix='/meetups',
    tags=['meetups'],
    dependencies=[Depends(get_current_user)],
)

Database = Annotated[Session, Depends(get_database_session)]


@router.get('/', response_model=list[Meetup])
def meetups(
    database: Database,
):
    meetups_db = database.scalars(select(MeetupDb)).all()

    meetups = [
        Meetup(
            title=meetup_db.title,
            location=meetup_db.location,
            date=meetup_db.date,
            attendees=[
                Attendee(email=attendee.email, name=attendee.name)
                for attendee in meetup_db.attendees
            ],
            description=meetup_db.description,
        )
        for meetup_db in meetups_db
    ]

    return meetups
