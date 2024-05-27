from pydantic import BaseModel, EmailStr, ValidationError
from datetime import date
from typing import Optional
from passlib.context import CryptContext


class UserModel(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    address: str
    phone_no: str
    role: str
    created_at: Optional[date] = None

    def hash_password(self):
        self.password = CryptContext(
            schemes=["bcrypt"], deprecated="auto").hash(self.password)

    def verify_password(self, plain_password):
        return CryptContext(schemes=["bcrypt"], deprecated="auto").verify(plain_password, self.password)

    @classmethod
    def from_user_collection(cls, user_collection: dict) -> 'UserModel':
        try:
            return cls(**user_collection)
        except ValidationError as e:
            raise ValueError(f"Invalid user collection: {e}")
