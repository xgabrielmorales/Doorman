from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import Request, Response

from shop.api.pagination import LimitOffsetPagination, get_paginated_response
from shop.order.models.order import Order
from shop.order.selectors.order import OrderListFilter, order_list


class OrderListAPIView(GenericAPIView):
    class OrderListSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        gross_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
        net_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
        number_items = serializers.IntegerField()

    queryset = Order.objects.none()
    filterset_class = OrderListFilter
    serializer_class = OrderListSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: OrderListSerializer(many=True),
        },
    )
    def get(self, request: Request) -> Response:
        orders = order_list()

        return get_paginated_response(
            pagination_class=LimitOffsetPagination,
            serializer_class=self.OrderListSerializer,
            queryset=orders,
            request=request,
            view=self,
        )
