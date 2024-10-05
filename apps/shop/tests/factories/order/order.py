from factory import Faker, SubFactory, django, fuzzy

from shop.order.models import Order, OrderItem
from tests.factories.item import ItemFactory


class OrderFactory(django.DjangoModelFactory):
    class Meta:
        model = Order

    gross_cost = fuzzy.FuzzyDecimal(
        low=0.00,
        high=9999999999.99,
        precision=2,
    )
    net_cost = fuzzy.FuzzyDecimal(
        low=0.00,
        high=9999999999.99,
        precision=2,
    )


class OrderItemFactory(django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = SubFactory(OrderFactory)
    item = SubFactory(ItemFactory)
    quantity = Faker("random_int", min=1, max=99)
