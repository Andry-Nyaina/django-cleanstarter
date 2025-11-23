import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_products_unauthenticated_cannot_create(api_client):
    payload = {"name": "New", "price": 10}
    res = api_client.post("/api/products/", payload, format="json")
    assert res.status_code in (401, 403)  # 401 si JWT auth, 403 si autre config

@pytest.mark.django_db
def test_product_crud_with_authenticated_user(auth_client_for_user, product_factory):
    # client + user normal
    client, user = auth_client_for_user(username="alice", password="pw", is_staff=False)

    # CREATE
    res = client.post("/api/products/", {"name": "Prod1", "price": 50}, format="json")
    assert res.status_code == 201
    assert "message" in res.data and "data" in res.data

    prod_id = res.data["data"]["id"]

    # RETRIEVE
    res = client.get(f"/api/products/{prod_id}/")
    assert res.status_code == 200
    assert res.data["data"]["name"] == "Prod1"

    # UPDATE
    res = client.patch(f"/api/products/{prod_id}/", {"price": 60}, format="json")
    assert res.status_code == 200
    # price stored as decimal-string: on convertit pour assert
    assert float(res.data["data"]["price"]) == 60.0

    # DELETE
    res = client.delete(f"/api/products/{prod_id}/")
    assert res.status_code in (200, 204)


@pytest.mark.django_db
def test_user_list_only_admin_can_see(create_user, api_client, auth_client_for_user):
    # normal user
    client_normal, normal = auth_client_for_user(username="bob", password="b")
    response = client_normal.get("/api/users/")
    assert response.status_code == 403

    # admin user
    client_admin, admin = auth_client_for_user(username="adminx", password="a", is_staff=True)
    res = client_admin.get("/api/users/")
    assert res.status_code == 200
