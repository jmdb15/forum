import enum
import uuid

from datetime import datetime, timezone
from sqlalchemy import (
    String, 
    Uuid, 
    ForeignKey, 
    Enum, 
    Text,
    CheckConstraint,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

class PostSection(str, enum.Enum):
    READING_ROOM = "reading_room"
    OPEN_THOUGHTS = "open_thoughts"

class PostStatus(str, enum.Enum):
    PUBLISHED = "published"
    HIDDEN = "hidden"
    DELETED = "deleted"

class Post(Base):
    __tablename__ = 'posts'

    # __table_args__ = (
    #     CheckConstraint(
    #         "content IS NOT NULL OR image IS NOT NULL",
    #         name="check_post_content_or_image"
    #     ),
    # )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    section: Mapped[PostSection] = mapped_column(
        Enum(
            PostSection, 
            name="post_section",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        ),
        default=PostSection.OPEN_THOUGHTS,
        nullable=False,
        index=True,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=True,        
    )

    status: Mapped[PostStatus] = mapped_column(
        Enum(
            PostStatus, 
            name="post_status",
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls
            ]
        ),
        default=PostStatus.PUBLISHED,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    
    author: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )

    attachments: Mapped[list["PostAttachment"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="PostAttachment.position"
    )

    @property
    def formatted_created_at(self) -> str:
        return str(self.created_at.strftime("%B %-d, %Y").replace(
                    " 0", " "
                ))


class PostAttachment(Base):
    __tablename__ = 'post_attachments'

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    post_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    media_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    file_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    position: Mapped[int] = mapped_column(
        default=0,
        nullable=False,
    )

    post: Mapped["Post"] = relationship(
        back_populates="attachments"
    )
