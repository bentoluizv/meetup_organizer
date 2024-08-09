from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase, MappedAsDataclass):
    pass


meetup_with_attendees = Table(
    'meetup_with_attendees',
    Base.metadata,
    Column('meetup_id', ForeignKey('meetups.id')),
    Column('attendee_email', ForeignKey('attendees.email')),
)


class MeetupDb(Base):
    __tablename__ = 'meetups'
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
    )
    title: Mapped[str]
    description: Mapped[Optional[str]]
    location: Mapped[str]
    date: Mapped[datetime]
    attendees: Mapped[list['AttendeeDb']] = relationship(
        secondary=meetup_with_attendees
    )


class AttendeeDb(Base):
    __tablename__ = 'attendees'
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    is_blocked: Mapped[bool] = mapped_column(default=False)


class UserDb(Base):
    __tablename__ = 'users'
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
