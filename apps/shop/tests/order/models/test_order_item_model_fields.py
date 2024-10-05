from django.core.validators import MinValueValidator
from django.db import models

from shop.order.models import OrderItem
from tests.common.models import BaseModelFieldTest


class BaseTestOrderItem(BaseModelFieldTest):
    model = OrderItem


class TestFieldOrderItemItem(BaseTestOrderItem):
    field_name = "item"
    field_type = models.ForeignKey
    db_index = True


class TestFieldOrderItemOrder(BaseTestOrderItem):
    field_name = "order"
    field_type = models.ForeignKey
    db_index = True


class TestFieldOrderItemQuantity(BaseTestOrderItem):
    field_name = "quantity"
    field_type = models.IntegerField
    validators = (MinValueValidator,)
    default = 1
