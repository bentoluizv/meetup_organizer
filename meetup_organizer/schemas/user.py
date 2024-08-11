from typing import Any

from pydantic import (
    BaseModel,
    field_validator,
    model_serializer,
    model_validator,
)

from meetup_organizer.shared.security import get_password_hash


class CreationalUserSchema(BaseModel):
    username: str
    password1: str
    password2: str

    @model_validator(mode='before')
    @classmethod
    def check_passwords_are_equals(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data['password1'] != data['password2']:
                raise ValueError('passwords do not match')
        return data

    @field_validator('password1')
    @classmethod
    def hash_password(cls, value: str) -> str:
        password_hash = get_password_hash(value)
        return password_hash

    @model_serializer
    def to_dict(self):
        return {'username': self.username, 'password': self.password1}


class User(BaseModel):
    username: str
    password: str

    @classmethod
    def create(cls, data: CreationalUserSchema):
        return cls(**data.model_dump())
