from uuid import UUID
from fastapi import (
    APIRouter, 
    status, 
    Request, 
    Depends,
    Form,
    File,
    UploadFile as FastAPIUploadFile,
    Query,
)
from pydantic import WithJsonSchema
from sqlalchemy.orm import Session
from typing import Annotated

from app.posts.schema import PostResponse, PostFilterParams
from app.posts.models import PostSection
from app.posts.service import PostService
from app.db.database import get_db

# Use for current Swagger UI compatibility issue in v0.129.1
UploadFile = Annotated[
    FastAPIUploadFile,
    WithJsonSchema({"type": "string", "format": "binary"}),
]

post_router = APIRouter(
    prefix="/posts",
    tags=["Posts",],
)

def get_post_service(db: Session = Depends(get_db)):
    return PostService(db)

@post_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[PostResponse]
)
def list_posts(
    request: Request,
    filters: Annotated[PostFilterParams, Query()],
    service: PostService = Depends(get_post_service),
) -> list[PostResponse]:
    return service.list_posts(request, filters)


@post_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    author_id: Annotated[UUID | None, Form()] = None,
    content: Annotated[str | None, Form()] = None,
    section: Annotated[PostSection | None, Form()] = None,
    attachments: Annotated[list[UploadFile] | None, File()] = None,
    service: PostService = Depends(get_post_service),
):
    return service.create_post(
        author_id,
        content,
        section,
        attachments,
    )


@post_router.patch(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_206_PARTIAL_CONTENT,
)
async def create_post(
    post_id: UUID,
    content: Annotated[str, Form()],
    service: PostService = Depends(get_post_service),
):
    return service.update_post_content(post_id, content)
