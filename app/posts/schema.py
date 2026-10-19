import uuid

from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional

from app.posts.models import PostSection, PostStatus


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    author_id: uuid.UUID
    content: str
    image: str
    status: PostStatus
    section: PostSection
    created_at: datetime
    updated_at: datetime
    formatted_created_at: str


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
