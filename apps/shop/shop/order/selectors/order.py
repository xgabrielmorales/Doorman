import django_filters
from django.db.models import Count, Prefetch, Q, QuerySet

from shop.order.models import Order, OrderItem


class OrderListFilter(django_filters.FilterSet):
    gross_cost = django_filters.NumberFilter()
    net_cost = django_filters.NumberFilter()

    order_by = django_filters.OrderingFilter(
        fields=("gross_cost", "net_cost"),
    )


def order_list() -> QuerySet[Order]:
    return (
        Order.objects.filter(active=True)
        .annotate(number_items=Count("orderitem__item", filter=Q(orderitem__active=True)))
        .only("id", "gross_cost", "net_cost")
    )


def order_detail(*, order_id: int) -> QuerySet[Order]:
    order = (
        Order.objects.filter(id=order_id, active=True)
        .prefetch_related(
            Prefetch(
                lookup="orderitem_set",
                queryset=OrderItem.objects.filter(active=True),
            ),
        )
        .first()
    )

    if not order:
        raise Exception

    return order
