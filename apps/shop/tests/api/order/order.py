import random
from typing import Iterable
from urllib.parse import urlencode

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from shop.order.models import Order
from tests.factories.item import ItemFactory
from tests.factories.order import OrderFactory, OrderItemFactory

pytestmark = pytest.mark.django_db


class TestOrderCRUD:
    def test_list(self, client: APIClient):
        path = f"{reverse('orders:list')}?{urlencode(dict(order_by="id"))}"

        orders: Iterable[Order] = OrderFactory.create_batch(size=random.randint(1, 5))
        for order in orders:
            OrderItemFactory.create_batch(size=random.randint(1, 5), order=order)
            OrderItemFactory.create_batch(size=random.randint(1, 5), order=order, active=False)

        response: Response = client.get(path=path)

        assert response.status_code == status.HTTP_200_OK
        response_body = response.json()

        assert response_body["count"] == len(orders)

        expected_keys = (
            "gross_cost",
            "id",
            "net_cost",
            "number_items",
        )
        for key in expected_keys:
            key in response_body["results"][0]

    def test_detail(self, client: APIClient):
        order: Order = OrderFactory()
        OrderItemFactory.create_batch(size=random.randint(1, 5), order=order)
        OrderItemFactory.create_batch(size=random.randint(1, 5), order=order, active=False)

        path = f"{reverse('orders:detail', args=(order.id,))}"

        response = client.get(path=path)
        response_body = response.json()

        assert response.status_code == status.HTTP_200_OK

        expected_keys = ("gross_cost", "net_cost", "order_items")
        for key in expected_keys:
            assert key in response_body

    def test_create(self, client: APIClient):
        items = ItemFactory.create_batch(size=random.randint(1, 5))

        order_items: list[dict] = []
        for item in items:
            order_items.append(
                {
                    "item": item.id,
                    "quantity": random.randint(1, 10),
                },
            )

        path = reverse("orders:create")
        response = client.post(
            path=path,
            data={"order_items": order_items},
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        response_body = response.json()

        assert isinstance(response_body["id"], int)

    def test_delete(self, client: APIClient):
        item: Order = OrderFactory()

        path = f"{reverse('orders:delete', args=(item.id,))}"
        response = client.delete(path=path)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Order.objects.get(id=item.id).active is False
