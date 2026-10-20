import pytest
import uuid

from pydantic import ValidationError

from app.posts.models import PostSection
from app.posts.schema import CreatePost


def test_create_post_with_valid_data():
    post = CreatePost(
        author_id=uuid.uuid4(),
        content="lorem ipsum",
        image=None,
        section=PostSection.OPEN_THOUGHTS
    )

    assert post.content == "lorem ipsum"
    assert post.section == PostSection.OPEN_THOUGHTS
    
def test_create_post_with_invalid_data():
    with pytest.raises(ValueError):
        post = CreatePost(
            author_id=uuid.uuid4(),
            content=None,
            image=None,
            section=PostSection.OPEN_THOUGHTS
        )
