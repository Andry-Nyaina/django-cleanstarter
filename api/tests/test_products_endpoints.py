import pytest
from api.models import Product
from api.tests.conftest import *


def test_list_products(api_client, authenticated_user):
    api_client, user = authenticated_user
    api_client.force_authenticate(user=user)

    # prépare
    Product.objects.create(name="Product A", price=100)
    Product.objects.create(name="Product B", price=200)

    # action
    response = api_client.get("/api/products/")

    # vérifications
    assert response.status_code == 200
    assert len(response.data["data"]) == 2


def test_retrieve_product(api_client, authenticated_user):
    api_client, user = authenticated_user
    api_client.force_authenticate(user=user)

    product = Product.objects.create(name="Test", price=100)

    url = f"/api/products/{product.id}/"
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["data"]["name"] == "Test"

def test_update_product(api_client, authenticated_user):
    api_client, user = authenticated_user
    api_client.force_authenticate(user=user)

    product = Product.objects.create(name="Old", price=50)

    payload = {
        "name": "New",
        "price": 999
    }

    url = f"/api/products/{product.id}/"
    response = api_client.put(url, payload, format="json")

    assert response.status_code == 200
    assert response.data["data"]["name"] == "New"
    assert float(response.data["data"]["price"]) == 999

def test_delete_product(api_client, authenticated_user):
    api_client, user = authenticated_user
    api_client.force_authenticate(user=user)

    product = Product.objects.create(name="ToDelete", price=10)

    url = f"/api/products/{product.id}/"
    response = api_client.delete(url)

    assert response.status_code == 204
    assert Product.objects.count() == 0



