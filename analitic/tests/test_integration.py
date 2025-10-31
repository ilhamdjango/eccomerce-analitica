import os
import django
import uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from analitic.models import Shop, ShopView, Product, ProductView, AnalyticsProduct

class ShopViewIntegrationTest(APITestCase):
    def test_create_shop_view_and_db_integration(self):
        external_id = uuid.uuid4()
        data = {
            "shop": {"external_id": str(external_id), "name": "Integrated Shop"}
        }
        url = reverse('shop-view-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['shop']['name'], "Integrated Shop")

        # DB yoxlaması
        shop = Shop.objects.get(external_id=external_id)
        shop_view = ShopView.objects.get(shop=shop)
        self.assertIsNotNone(shop_view)

class ProductViewIntegrationTest(APITestCase):
    def test_create_product_view_and_db_integration(self):
        external_id = uuid.uuid4()
        data = {
            "product": {"external_id": str(external_id), "name": "Integrated Product"}
        }
        url = reverse('product-view-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # DB yoxlaması
        product = Product.objects.get(external_id=external_id)
        product_view = ProductView.objects.get(product=product)
        self.assertIsNotNone(product_view)

class AnalyticsProductIntegrationTest(APITestCase):
    def test_create_analytics_product_full_flow(self):
        # Lazımi obyektləri yaradın
        shop_id = uuid.uuid4()
        product_id = uuid.uuid4()

        shop = Shop.objects.create(external_id=shop_id, name="Test Shop")
        product = Product.objects.create(external_id=product_id, name="Test Product", shop=shop)

        data = {
            "shop": str(shop_id),
            "product_variation": str(product_id),
            "count": 5,
            "original_price": 70,
            "sale_price": 100
        }
        url = reverse('analytics-product-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # DB yoxlaması
        analytics = AnalyticsProduct.objects.get(shop=shop, product_variation=product)
        self.assertEqual(analytics.count, 5)
