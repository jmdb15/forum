from uuid import UUID
from fastapi import (
    Request,
    Form,
    File,
    UploadFile,
    HTTPException,
    status,
    Query
)
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Annotated

from app.posts.models import PostSection, Post, PostAttachment
from app.posts.schema import PostResponse, CreatePost, PostFilterParams
from app.posts.repository import PostRepository
from app.core.storage import save_uploaded_attachments
from app.core.utils import build_image_url

class PostService:
    def __init__(self, db: Session):
        self.repository = PostRepository(db)

    def list_posts(
        self, 
        request: Request,
        filters: Annotated[PostFilterParams, Query()]
    ) -> list[PostResponse]:
        posts = self.repository.list_posts(filters)
        response = []
        for post in posts:
            item = PostResponse.model_validate(post)
            for attachment in item.attachments or []:
                attachment.file_url = build_image_url(
                    attachment.file_url, 
                    str(request.base_url)
                )
            response.append(item)
        
        return response

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
            self.repository.create(post)

            uploaded_files = []
            for position, file in enumerate(attachments):
                file_data = save_uploaded_attachments(file)
                uploaded_files.append(file_data['file_url'])

                attachment = PostAttachment(
                    media_type=file_data['media_type'],
                    file_url=file_data['file_url'],
                    content_type=file_data['content_type'],
                    position=position,
                    post=post,
                )
                self.repository.create_attachment(attachment)

            self.repository.db.commit()
            self.repository.db.refresh(post)
            return post
        except (ValueError, ValidationError) as exc:
            self.repository.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc
        except SQLAlchemyError as exc:
            self.repository.db.rollback()

            # Delete uploaded files here if necessary.
            raise HTTPException(
                detail="Failed to create post.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            ) from exc

    def update_post_content(
        self, 
        post_id: UUID,
        content: str
    ) -> PostResponse:
        post = self.repository.get_post_by_id(post_id)

        if content is None or content == "":
            raise HTTPException(
                detail="content must have value",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        post.content = content
        return self.repository.update_post_content(post)
