import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.models import Product

@pytest.mark.django_db
class TestProductsAPI:

    def setup_method(self):
        self.client = APIClient()

    def test_list_products(self):
        assert True  # temporaire

    def test_create_product(self):
        assert True  # temporaire

    def test_edit_product(self):
        assert True  # temporaire

    def test_delete_product(self):
        assert True  # temporaire
