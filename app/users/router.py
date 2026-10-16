from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.users.schema import UserResponse, UserCreate
from app.users.service import UserService

user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


@user_router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
def list_users(
    service: UserService = Depends(get_user_service)
):
    return service.list_users()

@user_router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return service.create_user(user)
