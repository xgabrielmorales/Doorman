import json

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shop.item.models import Item
from tests.factories.item import ItemFactory

pytestmark = pytest.mark.django_db


class TestItemCRUD:
    def test_list(self, client: APIClient):
        path = f"{reverse('items:list')}"

        ItemFactory.create_batch(size=3)

        response = client.get(path=path)
        content = json.loads(response.content)

        assert response.status_code == status.HTTP_200_OK
        assert len(content["results"]) == 3

    def test_retrive(self, client: APIClient):
        item: Item = ItemFactory()

        path = f"{reverse('items:detail', args=(item.id,))}"

        expected_response = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "net_cost": item.net_cost,
            "tax_applicable": item.tax_applicable,
            "reference": item.reference,
        }

        response = client.get(path=path)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    def test_create(self, client: APIClient):
        item: Item = ItemFactory.build()

        path = reverse("items:create")

        response = client.post(
            path=path,
            data={
                "name": item.name,
                "description": item.description,
                "net_cost": item.net_cost,
                "tax_applicable": item.tax_applicable,
                "reference": item.reference,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        response_body = response.json()

        expected_response = {"name": item.name}
        response_content = {key: response_body[key] for key in expected_response.keys()}
        assert response_content == expected_response

        assert Item.objects.filter(id=response_body["id"]).exists() is True

    def test_partial_update(self, client: APIClient):
        item: Item = ItemFactory()
        new_item: Item = ItemFactory.build()

        path = f"{reverse('items:partial_update', args=(item.id,))}"

        response = client.patch(
            path=path,
            data={"name": new_item.name, "description": new_item.description},
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        item.refresh_from_db()

        assert item.name == new_item.name
        assert item.description == new_item.description

    def test_delete(self, client: APIClient):
        item = ItemFactory()

        path = f"{reverse('items:delete', args=(item.id,))}"

        response = client.delete(path=path)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Item.objects.get(id=item.id).active is False
