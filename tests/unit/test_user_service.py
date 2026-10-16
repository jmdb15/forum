from datetime import date
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.users.schema import UserCreate, UserResponse
from app.users.service import UserService


@pytest.fixture
def user_data():
    return UserCreate(
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com",
        password="Password123!",
        confirm_password="Password123!",
    )

@pytest.fixture
def existing_user_data():
    return UserResponse(
        id="a13f8204-8b6b-43c5-b9ce-83e063278025",
        first_name="John",
        last_name="Doe",
        full_name="John Doe",
        email="johndoe@example.com",
        age=None,
        birthday=date(2001, 1, 1),
        is_active=True,
    )


@pytest.fixture
def user_service():
    service = UserService(db=Mock())
    service.repository = Mock()
    return service


def test_create_user_success(user_service, user_data):
    user_service.repository.exist_by_email.return_value = False
    user_service.repository.exist_by_name.return_value = False

    user_service.repository.create_user.side_effect = (
        lambda user: user
    )

    with patch(
        "app.users.service.hash_password",
        return_value="hashed-password",
    ):
        result = user_service.create_user(user_data)

    assert result.email == "johndoe@example.com"

    assert result.password == 'hashed-password'

    user_service.repository.create_user.assert_called_once()


def test_create_user_duplicate_email(user_service, user_data):
    user_service.repository.exist_by_email.return_value = True

    with pytest.raises(HTTPException) as exc:
        user_service.create_user(user_data)

    assert exc.value.status_code == 409

    user_service.repository.create_user.assert_not_called()


def test_list_users(user_service):
    expected_users = [
        Mock(first_name="John"),
        Mock(first_name="Jane"),
    ]

    user_service.repository.list_users.return_value = expected_users

    result = user_service.list_users()

    assert result == expected_users

    user_service.repository.list_users.assert_called_once_with()


def test_get_user_by_non_existing_id(user_service, existing_user_data):
    user_service.repository.get_user_by_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        user_service.get_user_by_id(existing_user_data.id)

    assert exc.value.detail == 'User ID does not exist'

def test_get_user_by_non_existing_id(user_service, existing_user_data):
    user_service.repository.get_user_by_id.return_value = existing_user_data

    result = user_service.get_user_by_id(existing_user_data.id)

    assert existing_user_data == result
    assert result.first_name == "John"
