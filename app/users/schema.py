from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator, model_validator

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
    full_name: str
    email: str
    age: int | None
    birthday: date | None
    is_active: bool


class UserCreate(BaseModel):
    first_name: str = Field(min_length=3, max_length=100)
    last_name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    confirm_password: str = Field(min_length=8, max_length=100)
    age: Optional[int] = Field(default=None, gt=12)
    birthday: Optional[date] = None

    @field_validator("password", "confirm_password")
    @classmethod
    def validate_passwords(cls, value):
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain an uppercase letter")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain a number")

        if not any(not char.isalnum() for char in value):
            raise ValueError("Password must contain a special character")

        return value

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        
        return self
