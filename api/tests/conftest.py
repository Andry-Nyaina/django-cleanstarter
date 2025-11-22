import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from api.models import Product 

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_user(api_client, db):
    user = User.objects.create_user(username="testuser", password="pass123")
    api_client.force_authenticate(user)
    return api_client, user

 
@pytest.fixture
def api_client():
    """APIClient sans authentification — réutilisable"""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Factory simple pour créer des users rapidement"""
    def _create_user(username="user", password="pass123", is_staff=False, is_superuser=False):
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()
        return user
    return _create_user


@pytest.fixture
def user(create_user):
    return create_user(username="normal", password="normal123", is_staff=False)


@pytest.fixture
def admin_user(create_user):
    return create_user(username="admin", password="admin123", is_staff=True)


@pytest.fixture
def auth_client(api_client, create_user):
    """
    Retourne une APIClient authentifié avec un user créé.
    Utilise un token JWT réel (pas force_authenticate).
    """
    user = create_user(username="authuser", password="authpass")
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(refresh.access_token)}")
    return api_client


@pytest.fixture
def auth_client_for_user(api_client, create_user):
    """
    Retourne une factory qui crée un user et renvoie un client authentifié pour ce user.
    Usage:
        client = auth_client_for_user(username="bob")
    """
    def _factory(username="userx", password="pwd123", is_staff=False):
        u = create_user(username=username, password=password, is_staff=is_staff)
        token = RefreshToken.for_user(u)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token.access_token)}")
        return api_client, u
    return _factory


@pytest.fixture
def product_factory(db):
    """Factory simple pour créer un product"""
    def _create_product(name="P", price=100):
        return Product.objects.create(name=name, price=price)
    return _create_product
