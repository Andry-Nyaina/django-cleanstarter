import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Product

@pytest.mark.django_db
def test_list_products():
    # 1) Préparer un utilisateur + token
    user = User.objects.create_user(username="test", password="pass123")
    client = APIClient()
    client.force_authenticate(user)

    # 2) Créer des produits en base
    Product.objects.create(name="P1", price=1000)
    Product.objects.create(name="P2", price=2000)

    # 3) Appeler l’endpoint
    response = client.get("/api/products/")

    # 4) Vérifier
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_create_product():
    user = User.objects.create_user(username="test", password="pass123")
    client = APIClient()
    client.force_authenticate(user)

    payload = {"name": "Laptop", "price": 3500}

    response = client.post("/api/products/", payload, format="json")

    assert response.status_code == 201
    assert response.data["message"] == "Produit créé avec succès"
    assert response.data["data"]["name"] == "Laptop"


@pytest.mark.django_db
def test_update_product():
    user = User.objects.create_user(username="test", password="pass123")
    client = APIClient()
    client.force_authenticate(user)

    product = Product.objects.create(name="Old", price=100)

    payload = {"name": "Updated", "price": 500}

    response = client.put(f"/api/products/{product.id}/", payload, format="json")

    assert response.status_code == 200
    assert response.data["data"]["name"] == "Updated"
    assert float(response.data["data"]["price"]) == 500


@pytest.mark.django_db
def test_delete_product():
    user = User.objects.create_user(username="test", password="pass123")
    client = APIClient()
    client.force_authenticate(user)

    product = Product.objects.create(name="DeleteMe", price=200)

    response = client.delete(f"/api/products/{product.id}/")

    assert response.status_code == 204
    assert Product.objects.count() == 0
