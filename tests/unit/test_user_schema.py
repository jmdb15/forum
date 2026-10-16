import pytest

from pydantic import ValidationError
from app.users.schema import UserCreate


def test_create_user_with_valid_data():
    user = UserCreate(
        first_name="John",
        last_name="Smith",
        email="johnsmith@example.com",
        password="Password123!",
        confirm_password="Password123!",
    )

    assert user.first_name == "John"
    assert user.email == "johnsmith@example.com"
    assert user.age is None


def test_create_user_with_invalid_data():
    with pytest.raises(ValidationError):
        user = UserCreate(
            first_name="John",
            last_name="Smith",
            email="johnsmith-invalid-email",
            password="Password123!",
            confirm_password="Password123!",
        )


def test_create_user_with_mismatched_passwords():
    with pytest.raises(
        ValidationError,
        match="Passwords do not match",    
    ):
        user = UserCreate(
            first_name="John",
            last_name="Smith",
            email="johnsmith@example.com",
            password="Password123!",
            confirm_password="Password123!.",
        )
