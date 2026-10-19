import uuid

from fastapi import HTTPException, status, UploadFile, Request
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.core.storage import save_profile_image
from app.core.utils import build_image_url
from app.db.database import get_db
from app.users.models import User
from app.users.schema import UserCreate, UserUpdate, UserResponse
from app.users.repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def list_users(self, request: Request):
        users = self.repository.list_users()

        response = []
        for user in users:
            item = UserResponse.model_validate(user)
            item.profile_url = build_image_url(
                item.profile_url,
                str(request.base_url),
            )
            response.append(item)

        return response

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

    def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                detail="User ID does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        return user

    def update_user(
        self, 
        user_id: uuid.UUID, 
        payload: UserUpdate
    ):
        user = self.repository.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(
                detail="User ID does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        update_data = payload.model_dump(exclude_unset=True)

        for field in ("first_name", "last_name", "email"):
            if field in update_data and (
                update_data[field] is None or update_data[field] == ""
            ):
                raise HTTPException(
                    detail=f"{field} cannot be null or empty",
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                )

        if 'email' in update_data:
            existing_user = self.repository.exist_by_email(update_data['email'])

            if existing_user and existing_user.id != user.id:
                raise HTTPException(
                    detail=f"Email already exists",
                    status_code=status.HTTP_409_CONFLICT,
                )                

        for field, value in update_data.items():
            setattr(user, field, value)

        return self.repository.update_user(user)

    def upload_profile_image(
        self,
        user_id: uuid.UUID,
        file: UploadFile
    ):
        user = self.repository.get_user_by_id(user_id)

        if user is None:
            raise HTTPException(
                detail="User ID does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )

        image_url = save_profile_image(file)

        user.profile_url = image_url

        return self.repository.update_user(user)
