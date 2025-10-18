import pytest
from django.contrib.auth import get_user_model

from ..api.serializers import UserLoginSerializer, UserRegisterSerializer

User = get_user_model()


@pytest.mark.django_db
class TestUserRegisterSerializer:
    def test_valid_data(self):
        data = {
            "email": "new_user@example.com",
            "name": "New User",
            "password": "SecurePass@123",
            "password2": "SecurePass@123",
        }
        serializer = UserRegisterSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.email == data["email"]
        assert user.name == data["name"]  # Fixed assertion
        assert user.check_password(data["password"])

    def test_password_mismatch(self):
        data = {
            "email": "new_user@example.com",
            "name": "New User",
            "password": "SecurePass@123",
            "password2": "DifferentPass@123",
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_existing_email(self):
        User.objects.create_user(email="existing_user@example.com", name="Existing User", password="SecurePass@123")
        data = {
            "email": "existing_user@example.com",
            "name": "New User",
            "password": "SecurePass@123",
            "password2": "SecurePass@123",
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_missing_fields(self):
        data = {
            "email": "",
            "name": "",
            "password": "",
            "password2": "",
        }
        serializer = UserRegisterSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors
        assert "name" in serializer.errors
        assert "password" in serializer.errors


@pytest.mark.django_db
class TestUserLoginSerializer:
    def test_valid_data(self):
        user = User.objects.create_user(
            email="existing_user@example.com", name="Existing User", password="SecurePass@123"
        )
        data = {"email": "existing_user@example.com", "password": "SecurePass@123"}
        serializer = UserLoginSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data["user"].email == user.email

    def test_invalid_credentials(self):
        data = {"email": "non_existent_user@example.com", "password": "WrongPassword@123"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_inactive_user(self):
        user = User.objects.create_user(
            email="inactive_user@example.com", name="Inactive User", password="SecurePass@123"
        )
        user.is_active = False
        user.save()
        data = {"email": "inactive_user@example.com", "password": "SecurePass@123"}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "non_field_errors" in serializer.errors

    def test_missing_fields(self):
        data = {"email": "", "password": ""}
        serializer = UserLoginSerializer(data=data)
        assert not serializer.is_valid()
        assert "email" in serializer.errors
        assert "password" in serializer.errors
