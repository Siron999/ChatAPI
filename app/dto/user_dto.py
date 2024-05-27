from datetime import date

from pydantic import BaseModel, ValidationError
from ..model.user_model import UserModel
from typing import Optional


class UserDTO(BaseModel):
    _id: Optional[str]
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    address: Optional[str]
    phone_no: Optional[str]
    role: Optional[str]
    created_at: Optional[date]

    @classmethod
    def from_user_collection(cls, user_collection: dict) -> 'UserDTO':
        try:
            return cls(**user_collection)
        except ValidationError as e:
            raise ValueError(f"Invalid user collection: {e}")


class LoginDTO(BaseModel):
    username: Optional[str]
    password: Optional[str]
