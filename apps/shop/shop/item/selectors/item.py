import django_filters
from django.db.models import QuerySet

from shop.item.models import Item


class ItemListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    order_by = django_filters.OrderingFilter(
        fields=("id", "name", "net_cost", "tax_applicable"),
    )


def items_list(
    *,
    query_params: dict[str, str | int | float | bool],
) -> QuerySet[Item]:
    queryset = Item.objects.filter(active=True)
    filtered_queryset = ItemListFilter(data=query_params, queryset=queryset).qs

    return filtered_queryset


def item_detail(*, item_id: str | int) -> Item | None:
    item = Item.objects.filter(id=item_id, active=True).first()

    if not item:
        raise Exception

    return item
