import uuid
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from app.users.schema import UserUpdate
from app.users.service import UserService


@pytest.fixture
def service():
    instance = UserService(db=Mock())
    instance.repository = Mock()
    return instance


def test_update_first_name_only(service):
    user_id = uuid.uuid4()

    user = Mock(
        id=user_id,
        first_name="John",
        last_name="Smith",
        email="john@example.com",
    )

    service.repository.get_by_id.return_value = user
    service.repository.update_user.side_effect = lambda obj: obj

    result = service.update_user(
        user_id,
        UserUpdate(first_name="James"),
    )

    assert result.first_name == "James"
    assert result.last_name == "Smith"
    assert result.email == "john@example.com"


def test_update_user_not_found(service):
    service.repository.get_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        service.update_user(
            uuid.uuid4(),
            UserUpdate(first_name="James"),
        )

    assert exc.value.status_code == 404


def test_update_duplicate_email(service):
    user_id = uuid.uuid4()

    service.repository.get_by_id.return_value = Mock(
        id=user_id,
        email="john@example.com",
    )

    service.repository.get_by_email.return_value = Mock(
        id=uuid.uuid4(),
        email="taken@example.com",
    )

    with pytest.raises(HTTPException) as exc:
        service.update_user(
            user_id,
            UserUpdate(email="taken@example.com"),
        )

    assert exc.value.status_code == 409
    service.repository.update_user.assert_not_called()
