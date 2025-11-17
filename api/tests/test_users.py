import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.mark.django_db
def test_user_list_permissions():
    admin = User.objects.create_superuser(username="admin", password="admin1234")
    user = User.objects.create_user(username="user", password="user1234")

    client = APIClient()

    # --- ADMIN ---
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token_for_user(admin)}")
    response = client.get("/api/users/")
    assert response.status_code == 200

    # --- USER NORMAL ---
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token_for_user(user)}")
    response = client.get("/api/users/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_retrieve_permissions():
    admin = User.objects.create_superuser(username="admin", password="admin123")
    user1 = User.objects.create_user(username="user1", password="user123")
    user2 = User.objects.create_user(username="user2", password="user123")

    client = APIClient()

    # ADMIN → peut voir user2
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token_for_user(admin)}")
    response = client.get(f"/api/users/{user2.id}/")
    assert response.status_code == 200

    # USER1 → peut voir son profil
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token_for_user(user1)}")
    response = client.get(f"/api/users/{user1.id}/")
    assert response.status_code == 200

    # USER1 → ne peut PAS voir user2
    response = client.get(f"/api/users/{user2.id}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_user_update_permissions():
    admin = User.objects.create_superuser(username="admin", password="admin123")
    user1 = User.objects.create_user(username="user1", password="user123")
    user2 = User.objects.create_user(username="user2", password="user123")

    client = APIClient()

    # USER1 → peut modifier son propre profil
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token_for_user(user1)}")
    response = client.patch(f"/api/users/{user1.id}/", {"email": "new@mail.com"}, format="json")
    assert response.status_code == 200

    # USER1 → NE PEUT PAS modifier user2
    response = client.patch(f"/api/users/{user2.id}/", {"email": "x@mail.com"}, format="json")
    assert response.status_code == 403

    # ADMIN → peut modifier user2
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {get_token_for_user(admin)}")
    response = client.patch(f"/api/users/{user2.id}/", {"email": "adminchange@mail.com"}, format="json")
    assert response.status_code == 200




