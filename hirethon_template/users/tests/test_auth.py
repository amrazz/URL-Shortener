import pytest
from django.urls import reverse
from rest_framework import status

from ..models import User


@pytest.mark.django_db
class TestUserRegistration:
    def test_user_registration(self, api_client):
        url = reverse("users:register")
        data = {
            "email": "new_user@example.com",
            "name": "Test User",
            "password": "SecurePass@123",
            "password2": "SecurePass@123",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["user"]["email"] == "new_user@example.com"
        assert response.data["user"]["name"] == "Test User"
        assert "tokens" in response.data
        assert "access" in response.data["tokens"]
        assert "refresh" in response.data["tokens"]
        assert "organization" in response.data

        user = User.objects.get(email="new_user@example.com")
        assert user.check_password("SecurePass@123")
        assert user.name == "Test User"

    def test_user_registration_password_mismatch(self, api_client):
        url = reverse("users:register")
        data = {
            "email": "new_user@example.com",
            "name": "Test User",
            "password": "SecurePass@123",
            "password2": "DifferentPass@123",
        }
        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data

    def test_user_registration_existing_email(self, api_client):
        User.objects.create_user(email="existing_user@example.com", name="Existing User", password="SecurePass@123")

        url = reverse("users:register")
        data = {
            "email": "existing_user@example.com",
            "name": "New User",
            "password": "SecurePass@123",
            "password2": "SecurePass@123",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_user_registration_missing_fields(self, api_client):
        url = reverse("users:register")
        data = {
            "email": "",
            "name": "",
            "password": "",
            "password2": "",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
        assert "name" in response.data
        assert "password" in response.data


@pytest.mark.django_db
class TestUserLogin:
    def test_user_login(self, api_client):
        User.objects.create_user(email="existing_user@example.com", name="Test User", password="SecurePass@123")

        url = reverse("users:login")
        data = {"email": "existing_user@example.com", "password": "SecurePass@123"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert "tokens" in response.data
        assert "access" in response.data["tokens"]
        assert "refresh" in response.data["tokens"]

    def test_user_login_invalid_credentials(self, api_client):
        url = reverse("users:login")
        data = {"email": "invalid_user@example.com", "password": "WrongPassword@123"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data

    def test_user_login_missing_fields(self, api_client):
        url = reverse("users:login")
        data = {"email": "", "password": ""}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data
        assert "password" in response.data

    def test_user_login_inactive_account(self, api_client):
        user = User.objects.create_user(
            email="inactive_user@example.com", name="Inactive User", password="SecurePass@123"
        )
        user.is_active = False
        user.save()

        url = reverse("users:login")
        data = {"email": "inactive_user@example.com", "password": "SecurePass@123"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "non_field_errors" in response.data
