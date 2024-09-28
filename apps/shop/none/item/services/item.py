from decimal import Decimal

from django.db import transaction

from none.item.models import Item


@transaction.atomic
def item_create(
    *,
    name: str,
    description: str,
    net_cost: Decimal,
    tax_applicable: Decimal,
    reference: str,
) -> Item:
    item = Item(
        name=name,
        description=description,
        net_cost=net_cost,
        tax_applicable=tax_applicable,
        reference=reference,
    )
    item.full_clean()
    item.save()

    return item


@transaction.atomic
def item_delete(
    *,
    item_id: int,
) -> None:
    Item.objects.filter(id=item_id, active=True).update(active=False)


@transaction.atomic
def item_partial_update(
    *,
    item_id: int,
    name: str | None = None,
    description: str | None = None,
    net_cost: Decimal | None = None,
    tax_applicable: Decimal | None = None,
    reference: str | None = None,
) -> None:
    item = Item.objects.filter(id=item_id, active=True).first()

    if not item:
        raise Exception("Item not found.")

    item.name = name or item.name
    item.description = description or item.description
    item.net_cost = net_cost or item.net_cost
    item.tax_applicable = tax_applicable or item.tax_applicable
    item.reference = reference or item.reference

    item.full_clean()
    item.save()

    return item
