from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.database import get_db
from app.users.models import User
from app.users.schema import UserCreate
from app.users.repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def list_users(self):
        return self.repository.list_users()

    def create_user(self, user: UserCreate):
        if self.repository.exist_by_email(user):
            raise HTTPException(
                detail="User already exists",
                status_code=status.HTTP_409_CONFLICT
            )
        
        if self.repository.exist_by_name(user):
            raise HTTPException(
                detail="User already exists",
                status_code=status.HTTP_409_CONFLICT,
            )

        hashed_password = hash_password(user.password)

        new_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,
            age=user.age,
            birthday=user.birthday,
        )
        
        return self.repository.create_user(new_user)
