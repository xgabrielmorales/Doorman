from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F, Value as V

from shop.item.models import Item
from tests.common.models import BaseModelFieldTest


class BaseTestItem(BaseModelFieldTest):
    model = Item


class TestFieldItemName(BaseTestItem):
    field_name = "name"
    field_type = models.CharField


class TestFieldItemDescription(BaseTestItem):
    field_name = "description"
    field_type = models.TextField
    blank = True


class TestFieldItemGrossCost(BaseTestItem):
    field_name = "gross_cost"
    field_type = models.DecimalField
    validators = (MinValueValidator,)
    blank = False


class TestFieldItemNetCost(BaseTestItem):
    field_name = "net_cost"
    field_type = models.GeneratedField
    blank = True

    def test_generated_value(self):
        expected_expression = F("gross_cost") * (F("tax_applicable") + V(Decimal("1")))
        assert self.field.expression == expected_expression


class TestFieldItemTaxApplicable(BaseTestItem):
    field_name = "tax_applicable"
    field_type = models.DecimalField
    validators = (MaxValueValidator,)


class TestFieldItemReference(BaseTestItem):
    field_name = "reference"
    field_type = models.CharField
    blank = True
