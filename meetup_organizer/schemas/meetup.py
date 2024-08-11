from datetime import datetime

from pydantic import BaseModel

from meetup_organizer.schemas.attendee import Attendee


class CreationalMeetupSchema(BaseModel):
    title: str
    location: str
    date: datetime


class Meetup(BaseModel):
    title: str
    location: str
    date: datetime
    description: str | None = None
    attendees: list[Attendee] = []

    @classmethod
    def create(cls, data: CreationalMeetupSchema):
        return cls(**data.model_dump())

    def register(self, attendee: Attendee):
        attendees = self.attendees.copy()

        if attendee in attendees:
            raise ValueError('Attendee already register')

        self.attendees.append(attendee)

    def set_description(self, content: str):
        self.description = content
