import os

import django
import pytest
from django.test import RequestFactory

from hirethon_template.users.models import User
from hirethon_template.users.tests.factories import UserFactory

# Configure Django BEFORE importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def admin_user(db) -> User:
    return User.objects.create_superuser(email="admin@example.com", password="testpass123")


@pytest.fixture
def rf() -> RequestFactory:
    return RequestFactory()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_api_client(user):
    from rest_framework.test import APIClient
    from rest_framework_simplejwt.tokens import RefreshToken

    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client
