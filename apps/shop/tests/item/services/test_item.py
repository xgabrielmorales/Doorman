from decimal import Decimal

import pytest

from shop.item.models import Item
from shop.item.services.item import item_create, item_delete, item_partial_update
from tests.item.factories import ItemFactory


class TestItemCreate:
    @pytest.mark.django_db
    def test_create_item(self):
        fake_item = ItemFactory.build()

        item = item_create(
            name=fake_item.name,
            description=fake_item.description,
            gross_cost=fake_item.gross_cost,
            tax_applicable=fake_item.tax_applicable,
            reference=fake_item.reference,
        )

        assert isinstance(item, Item)
        assert isinstance(item.id, int)


class TestItemPartialUpdate:
    @pytest.mark.django_db
    def test_update_item(self):
        item: Item = ItemFactory()
        fake_item: ItemFactory = ItemFactory.build()

        item_partial_update(
            item_id=item.id,
            name=fake_item.name,
            description=fake_item.description,
            gross_cost=fake_item.gross_cost,
            tax_applicable=fake_item.tax_applicable,
            reference=fake_item.reference,
        )

        item.refresh_from_db()

        assert item.name == fake_item.name
        assert item.description == fake_item.description
        assert item.gross_cost == Decimal(str(fake_item.gross_cost))
        assert item.tax_applicable == Decimal(str(fake_item.tax_applicable))
        assert item.reference == fake_item.reference

    @pytest.mark.django_db
    def test_update_inactive_item(self):
        item: Item = ItemFactory()
        item.active = False
        item.save()

        fake_item = ItemFactory.build()

        with pytest.raises(Exception):
            item_partial_update(item_id=item.id, name=fake_item.name)


class TestItemDelete:
    @pytest.mark.django_db
    def test_delete_item(self):
        item: Item = ItemFactory()

        item_delete(item_id=item.id)

        assert Item.objects.filter(id=item.id).exists() is True

        item.refresh_from_db()
        assert item.active is False

    @pytest.mark.django_db
    def test_delete_inactive_item(self):
        item: Item = ItemFactory()
        item.active = False
        item.save()

        item_delete(item_id=item.id)

        Item.objects.filter(id=item.id).exists()

        item.refresh_from_db()
        assert item.active is False
