from decimal import Decimal

from django.db import transaction

from shop.item.models import Item
from shop.order.models import Order, OrderItem


def calculate_order_price(
    order_items: list[dict[str, Item | int]],
) -> dict[str, Decimal]:
    gross_cost, net_cost = Decimal("0"), Decimal("0")
    for order_item in order_items:
        item, quantity = order_item["item"], order_item["quantity"]

        gross_cost += item.gross_cost * quantity
        net_cost += item.net_cost * quantity

    return {
        "gross_cost": gross_cost,
        "net_cost": net_cost,
    }


@transaction.atomic
def order_create(
    *,
    order_items: list[dict[str, Item | int]],
) -> Order:
    if not order_items:
        raise Exception

    order_price = calculate_order_price(order_items=order_items)
    gross_cost = order_price["gross_cost"]
    net_cost = order_price["net_cost"]

    order = Order(
        gross_cost=format(gross_cost, ".2f"),
        net_cost=format(net_cost, ".2f"),
    )
    order.full_clean()
    order.save()

    order_item_objs: list[OrderItem] = []
    for order_item in order_items:
        order_item_obj = OrderItem(
            item=order_item["item"],
            order=order,
            quantity=order_item["quantity"],
        )
        order_item_obj.full_clean()
        order_item_objs.append(order_item_obj)

    OrderItem.objects.bulk_create(order_item_objs)

    return order


@transaction.atomic
def order_update(
    *,
    order_id: int,
    order_items: list[dict[str, Item | int]],
):
    order = Order.objects.filter(id=order_id, active=True).first()

    if not order:
        raise Exception

    order_price = calculate_order_price(order_items=order_items)
    gross_cost = order_price["gross_cost"]
    net_cost = order_price["net_cost"]

    order.gross_cost = format(gross_cost, ".2f")
    order.net_cost = format(net_cost, ".2f")
    order.full_clean()
    order.save()

    order.orderitem_set.filter(active=True).update(active=False)

    order_item_objs: list[OrderItem] = []
    for order_item in order_items:
        order_item_obj = OrderItem(
            item=order_item["item"],
            order=order,
            quantity=order_item["quantity"],
        )
        order_item_obj.full_clean()
        order_item_objs.append(order_item_obj)

    OrderItem.objects.bulk_create(order_item_objs)


@transaction.atomic
def order_delete(
    *,
    order_id: int,
) -> None:
    Order.objects.filter(id=order_id, active=True).update(active=False)
