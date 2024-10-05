import random
from decimal import Decimal

import pytest

from shop.item.models import Item
from shop.order.models import Order, OrderItem
from shop.order.services.order import (
    calculate_order_price,
    order_create,
    order_delete,
    order_update,
)
from tests.item.factories import ItemFactory
from tests.order.factories import OrderFactory, OrderItemFactory


@pytest.fixture
def order_items_data():
    BATCH_SIZE = random.randint(1, 10)
    items = ItemFactory.create_batch(size=BATCH_SIZE)

    order_items = []
    total_net_cost, total_gross_cost = Decimal("0"), Decimal("0")
    for item in items:
        quantity = random.randint(1, 10)

        total_net_cost += item.net_cost * quantity
        total_gross_cost += item.gross_cost * quantity

        order_items.append({"item": item, "quantity": quantity})

    return {
        "order_items": order_items,
        "total_net_cost": total_net_cost,
        "total_gross_cost": total_gross_cost,
    }


@pytest.mark.django_db
def test_calcualte_order_values(order_items_data):
    order_items = order_items_data["order_items"]
    total_net_cost = order_items_data["total_net_cost"]
    total_gross_cost = order_items_data["total_gross_cost"]

    order_value = calculate_order_price(order_items=order_items)

    assert order_value["net_cost"] == total_net_cost
    assert order_value["gross_cost"] == total_gross_cost


class TestOrderCreate:
    @pytest.mark.django_db
    def test_create_order(self, order_items_data):
        order_items = order_items_data["order_items"]
        total_net_cost = order_items_data["total_net_cost"]
        total_gross_cost = order_items_data["total_gross_cost"]

        order = order_create(order_items=order_items)

        assert order.orderitem_set.count() == len(order_items)
        assert order.net_cost == total_net_cost
        assert order.gross_cost == total_gross_cost

    @pytest.mark.django_db
    def test_create_order_wihtout_items(self):
        with pytest.raises(Exception):
            order_create(order_items=[])


class TestOrderUpdate:
    @pytest.mark.django_db
    def test_update_order(self, order_items_data):
        created_order: Order = OrderFactory()
        created_order_items = OrderItemFactory.create_batch(size=3, order=created_order)

        total_net_cost = order_items_data["total_net_cost"]
        total_gross_cost = order_items_data["total_gross_cost"]
        order_items_to_update = order_items_data["order_items"]

        order_update(
            order_id=created_order.id,
            order_items=order_items_to_update,
        )

        created_order.refresh_from_db()
        assert created_order.orderitem_set.filter(active=True).count() == len(order_items_to_update)

        created_order_items_ids = [order_item.id for order_item in created_order_items]
        assert OrderItem.objects.filter(id__in=created_order_items_ids, active=True).count() == 0

        assert created_order.net_cost == total_net_cost
        assert created_order.gross_cost == total_gross_cost

    @pytest.mark.django_db
    def test_update_inactive_order(self):
        order: Order = OrderFactory(active=False)
        item: Item = ItemFactory()

        with pytest.raises(Exception):
            order_update(
                order_id=order.id,
                order_items={"item": item, "quantity": 5},
            )


class TestOrderDelete:
    @pytest.mark.django_db
    def test_delete_order(self):
        order: Order = OrderFactory()

        order_delete(order_id=order.id)

        assert Order.objects.filter(id=order.id).exists() is True

        order.refresh_from_db()
        assert order.active is False

    @pytest.mark.django_db
    def test_delete_inactive_order(self):
        order: Order = OrderFactory(active=False)
        order_delete(order_id=order.id)

        Order.objects.filter(id=order.id).exists()

        order.refresh_from_db()
        assert order.active is False
