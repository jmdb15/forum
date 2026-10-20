import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator, Field
from typing import Optional, Literal

from app.posts.models import PostSection, PostStatus


class PostFilterParams(BaseModel):
    # Pagination
    limit: int
    offset: int

    # Filtering
    author_id: uuid.UUID | None = None
    search: str | None = Field(default=None, min_length=1, max_length=200)
    created_before: datetime | None = None
    created_after: datetime | None = None

    # Sorting
    sort_by: Literal["created_at", "updated_at"] = "created_at"
    sort_order: Literal["asc", "desc"] = "desc"


class PostAttachmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    media_type: str
    file_url: str
    content_type: str
    position: int


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    author_id: uuid.UUID
    content: str | None
    status: PostStatus
    section: PostSection
    created_at: datetime
    updated_at: datetime
    # formatted_created_at: str

    attachments: list[PostAttachmentResponse] | None


class CreatePost(BaseModel):
    author_id: uuid.UUID
    content: Optional[str]
    section: PostSection

    @model_validator(mode="after")
    def validate_content_and_image_not_null(self):
        if (self.content is None or self.content == "") and \
            (self.image is None or self.image == ""):
            raise ValueError("Either content or image must be provided")

        return self
