from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import Request, Response

from shop.api.pagination import LimitOffsetPagination, get_paginated_response
from shop.item.models import Item
from shop.item.selectors.item import ItemListFilter, items_list


class ItemListAPIView(GenericAPIView):
    class ItemListSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()
        gross_cost = serializers.DecimalField(max_digits=12, decimal_places=3)
        tax_applicable = serializers.DecimalField(max_digits=3, decimal_places=2)
        reference = serializers.CharField()

    queryset = Item.objects.none()
    filterset_class = ItemListFilter
    serializer_class = ItemListSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: ItemListSerializer(many=True),
        },
    )
    def get(self, request: Request) -> Response:
        items = items_list(query_params=request.query_params.dict())
        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=self.ItemListSerializer,
            queryset=items,
            request=request,
            view=self,
        )
