from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from shop.common.models import BaseModel


class Item(BaseModel):
    name = models.CharField(
        max_length=128,
        db_comment="Item name.",
    )
    description = models.TextField(
        blank=True,
        db_comment="Item description.",
    )
    gross_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        db_comment="Item cost before deductions and taxes.",
        validators=[MinValueValidator(Decimal("0"))],
    )
    tax_applicable = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0"))],
        db_comment="Taxes applicable to the item.",
    )
    reference = models.CharField(
        blank=True,
        max_length=128,
        db_comment="Item reference",
    )

    class Meta:
        db_table = "items"
