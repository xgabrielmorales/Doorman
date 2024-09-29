from django.core.validators import MinValueValidator
from django.db import models

from shop.order.models import Order
from tests.models.common import BaseModelFieldTest


class BaseTestOrder(BaseModelFieldTest):
    model = Order


class TestFieldOrderGrossCost(BaseTestOrder):
    field_name = "gross_cost"
    field_type = models.DecimalField
    validators = (MinValueValidator,)


class TestFieldOrderNetCost(BaseTestOrder):
    field_name = "net_cost"
    field_type = models.DecimalField
    validators = (MinValueValidator,)


class TestFieldOrderItems(BaseTestOrder):
    field_name = "items"
    field_type = models.ManyToManyField
