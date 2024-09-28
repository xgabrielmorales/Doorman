from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from shop.common.models import BaseModel
from shop.item.models import Item


class Order(BaseModel):
    gross_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
        db_comment="Cost before deductions and taxes.",
    )
    net_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
        db_comment="Cost after deductions and taxes.",
    )
    items = models.ManyToManyField(
        to=Item,
        through="OrderItem",
    )

    class Meta:
        db_table = "orders"


class OrderItem(BaseModel):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(Decimal("1"))],
        db_comment="Quantity of an item in an order.",
    )

    class Meta:
        db_table = "orders_items"
