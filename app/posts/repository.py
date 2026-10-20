from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.posts.models import Post, PostAttachment
from app.posts.schema import PostFilterParams


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_posts(
        self, 
        filters: PostFilterParams,
    ) -> list:
        stmt = select(Post).options(
            joinedload(Post.attachments)
        )

        if filters.author_id is not None:
            stmt = stmt.where(Post.author_id == filters.author_id)

        if filters.search is not None:
            stmt = stmt.where(Post.content.ilike(f"%{filters.search}%"))

        if filters.created_after is not None:
            stmt = stmt.where(
                Post.created_at >= filters.created_after
            )

        if filters.created_before is not None:
            stmt = stmt.where(
                Post.created_at <= filters.created_before
            )

        sort_column = getattr(Post, filters.sort_by)

        if filters.sort_by == "desc":
            stmt = stmt.order_by(sort_column.desc())
        elif filters.sort_by == "asc":
            stmt = stmt.order_by(sort_column.asc())

        stmt = stmt.offset(filters.offset).limit(filters.limit)

        result = self.db.execute(stmt)
        return list(result.scalars().unique().all())
        # return list(self.db.scalars(stmt).unique().all())

    def create(self, post: Post):
        self.db.add(post)
        self.db.flush()
        return post

    def create_attachment(self, attachment: PostAttachment):
        self.db.add(attachment)
        self.db.flush()
        return attachment

    def get_post_by_id(self, post_id: UUID):
        return self.db.scalar(
            select(Post).where(Post.id == post_id)
        )

    def update_post_content(self, post: Post):
        try:
            self.db.commit()
            self.db.refresh(post)
            return post
        except:
            self.db.rollback()
            raise
