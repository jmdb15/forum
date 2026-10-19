from uuid import UUID
from fastapi import (
    Form,
    File,
    UploadFile,
    HTTPException,
    status
)
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import Annotated

from app.posts.schema import PostResponse, CreatePost
from app.posts.models import PostSection, Post, PostAttachment
from app.core.storage import save_uploaded_attachments

class PostService:
    def __init__(self, db: Session):
        self.db = db

    def list_posts(self) -> list[PostResponse]:
        return []

    def create_post(
        self,
        author_id: UUID | None = None,
        content: str | None = None,
        section: PostSection | None = None,
        attachments: list[UploadFile] | None = None,
    ) -> PostResponse:
        try:
            payload = CreatePost(
                author_id=author_id,
                content=content,
                section=section,
            )
            post = Post(
                author_id=payload.author_id,
                content=payload.content,
                section=payload.section,
            )
            for position, file in enumerate(attachments):
                file_data = save_uploaded_attachments(file)
                attachment = PostAttachment(
                    post_id=post.id,
                    media_type=file_data.get("media_type"),
                    file_url=file_data.get("file_url"),
                    content_type=file_data.get("content_type"),
                    position=position,
                    post=post
                )

            return None
        except (ValueError, ValidationError) as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST
            )
