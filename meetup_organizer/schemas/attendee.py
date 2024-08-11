from pydantic import BaseModel, EmailStr


class CreationalAttendeeSchema(BaseModel):
    email: EmailStr
    name: str


class Attendee(BaseModel):
    email: EmailStr
    name: str
    is_blocked: bool = False

    @classmethod
    def create(cls, data: CreationalAttendeeSchema):
        return cls(**data.model_dump())
