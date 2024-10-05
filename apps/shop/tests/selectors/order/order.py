import random

import pytest
from pytest_django import DjangoAssertNumQueries

from shop.order.models import Order
from shop.order.selectors.order import order_detail, order_list
from tests.factories.order import OrderFactory, OrderItemFactory


class TestOrderDetail:
    @pytest.mark.django_db
    def test_order_detail(self, django_assert_num_queries: DjangoAssertNumQueries):
        created_order: Order = OrderFactory()
        OrderItemFactory.create_batch(
            size=random.randint(1, 5),
            order=created_order,
            active=False,
        )

        active_order_items = OrderItemFactory.create_batch(
            size=random.randint(1, 5),
            order=created_order,
        )
        active_items_ids = [order_item.item.id for order_item in active_order_items]

        with django_assert_num_queries(2):
            fetched_order = order_detail(order_id=created_order.id)

        assert created_order.id is fetched_order.id
        assert created_order.orderitem_set.count() != fetched_order.orderitem_set.count()

        fetched_items_ids = [item.id for item in fetched_order.orderitem_set.all()]
        assert active_items_ids == fetched_items_ids

    @pytest.mark.django_db
    def test_fetch_inactive_item(
        self,
        django_assert_num_queries: DjangoAssertNumQueries,
    ):
        created_order: Order = OrderFactory(active=False)

        with pytest.raises(Exception), django_assert_num_queries(2):
            order_detail(order_id=created_order.id)

    @pytest.mark.django_db
    def test_fetch_non_existent_item(
        self,
        django_assert_num_queries: DjangoAssertNumQueries,
    ):
        with pytest.raises(Exception), django_assert_num_queries(2):
            order_detail(order_id=999)


class TestOrderList:
    @pytest.mark.django_db
    def test_list_orders(
        self,
        django_assert_num_queries: DjangoAssertNumQueries,
    ):
        batch_size = random.randint(1, 5)

        created_orders: Order = OrderFactory.create_batch(size=batch_size)
        for created_order in created_orders:
            OrderItemFactory.create_batch(size=batch_size, order=created_order)
            OrderItemFactory.create_batch(size=batch_size, order=created_order, active=False)

        fetched_orders = order_list(query_params={"order_by": "id"})

        assert len(created_orders) == fetched_orders.count()

        for index in range(len(created_orders)):
            assert fetched_orders[index].number_items == batch_size
            assert (
                created_orders[index].orderitem_set.count()
                != fetched_orders[index].orderitem_set.count()
            )

    @pytest.mark.django_db
    def test_list_inactive_orders(self):
        OrderFactory(active=False)
        fetched_item = order_list(query_params={})
        assert 0 == fetched_item.count()

    @pytest.mark.django_db
    def test_list_inactive_order_items(self):
        BATCH_SIZE = 2

        created_order: Order = OrderFactory()
        OrderItemFactory.create_batch(size=BATCH_SIZE, order=created_order)
        OrderItemFactory.create_batch(size=BATCH_SIZE, order=created_order, active=False)

        fetched_items = order_list(query_params={})
        firsat_fetched_item = fetched_items.first()

        assert firsat_fetched_item.number_items == BATCH_SIZE
        assert firsat_fetched_item.orderitem_set.count() == BATCH_SIZE
