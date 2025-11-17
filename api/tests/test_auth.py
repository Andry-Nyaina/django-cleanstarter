import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_user():
    client = APIClient()

    data = {
        "username": "TestUser",
        "email": "draken@example.com",
        "password": "test1234"
    }

    response = client.post("/api/register/", data, format="json")

    # 1. Le statut doit être 201 (créé)
    assert response.status_code == 201

    # 2. Vérifier que l'utilisateur est bien créé en DB
    assert User.objects.filter(username="TestUser").exists()

    # 3. Vérifier que le mot de passe est hashé (pas stocké en clair)
    user = User.objects.get(username="TestUser")
    assert user.check_password("test1234")

    # 4. Vérifier le format de réponse
    assert "message" in response.data


@pytest.mark.django_db
def test_login_success():
    # 1. Préparer un user
    user = User.objects.create_user(username="TestUser", password="test1234")

    client = APIClient()

    data = {
        "username": "TestUser",
        "password": "test1234"
    }

    response = client.post("/api/auth/login/", data, format="json")

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_wrong_password():
    User.objects.create_user(username="TestUser", password="test1234")

    client = APIClient()

    data = {
        "username": "TestUser",
        "password": "wrongpass"
    }

    response = client.post("/api/auth/login/", data, format="json")

    assert response.status_code == 401

