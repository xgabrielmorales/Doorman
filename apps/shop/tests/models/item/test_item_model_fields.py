from django.db import models

from shop.item.models import Item
from tests.models.common import BaseModelFieldTest
from django.core.validators import MinValueValidator


class BaseTestItem(BaseModelFieldTest):
    model = Item


class TestFieldItemName(BaseTestItem):
    field_name = "name"
    field_type = models.CharField


class TestFieldItemDescription(BaseTestItem):
    field_name = "description"
    field_type = models.TextField
    blank = True


class TestFieldItemNetCost(BaseTestItem):
    field_name = "net_cost"
    field_type = models.DecimalField
    validators = (MinValueValidator,)


class TestFieldItemTaxApplicable(BaseTestItem):
    field_name = "tax_applicable"
    field_type = models.DecimalField
    validators = (MinValueValidator,)


class TestFieldItemReference(BaseTestItem):
    field_name = "reference"
    field_type = models.CharField
    blank = True
