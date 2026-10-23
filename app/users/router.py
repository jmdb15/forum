import uuid

from fastapi import APIRouter, status, Depends, UploadFile, Request, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.users.schema import UserResponse, UserCreate, UserUpdate
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
    request: Request,
    service: UserService = Depends(get_user_service)
):
    return service.list_users(request)

@user_router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    service: UserService = Depends(get_user_service)
):
    return service.create_user(user, background_tasks)

@user_router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_user(
    user_id: str,
    service: UserService = Depends(get_user_service),
):
    return service.get_user_by_id(user_id)

@user_router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_user(
    user_id: str,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    return service.update_user(user_id, payload)

@user_router.post(
    "/{user_id}/profile-image",
    response_model=UserResponse,
)
def upload_profile_image(
    user_id: uuid.UUID,
    file: UploadFile,
    service: UserService = Depends(get_user_service),
):
    return service.upload_profile_image(user_id, file)
