import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.users.models import User
from app.users.schema import UserCreate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_users(self) -> list[User]:
        statement = select(User).where(User.is_active == True)

        return list(self.db.scalars(statement).all())

    def exist_by_name(
        self, 
        user: UserCreate
    ) -> bool:
        return self.db.scalar(
            select(User).where(
                User.first_name == user.first_name,
                User.last_name == user.last_name,
            )
        ) is not None
        
    def exist_by_email(
        self, 
        user: UserCreate
    ) -> bool:
        return self.db.scalar(
            select(User).where(
                User.email == user.email,
            )
        ) is not None

    def create_user(
        self, 
        user: User
    ) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_user_by_id(
        self,
        user_id: uuid.UUID
    ) -> User:
        return self.db.scalar(
            select(User).where(User.id == user_id)
        )

    def update_user(self, user: User) -> User:
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except:
            self.db.rollback()
            raise
