import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.mark.django_db
def test_user_list_permissions():
    admin = User.objects.create_superuser(username="admin", password="#Draken280403.")
    user = User.objects.create_user(username="abcd", password="abcd")

    client = APIClient()

    # --- ADMIN ---
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token_for_user(admin)}")
    response = client.get("/api/users/")
    assert response.status_code == 200

    # --- USER NORMAL ---
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token_for_user(user)}")
    response = client.get("/api/users/")
    assert response.status_code == 403


