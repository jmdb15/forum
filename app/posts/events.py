from sqlalchemy import event
from sqlalchemy.orm import Session

from app.posts.models import Post

@event.listens_for(Session, "before_flush")
def validate_posts(session, flush_content, instances):
    objects = session.new.union(session.dirty)

    for obj in objects:
        if isinstance(obj, Post):
            obj.validate()
