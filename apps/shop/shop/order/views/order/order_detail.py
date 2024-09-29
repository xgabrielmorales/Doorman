from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import Request, Response

from shop.api.utils import inline_serializer
from shop.order.models.order import Order
from shop.order.selectors.order import order_detail


class OrderDetailAPIView(GenericAPIView):
    class OrderDetailSerializer(serializers.Serializer):
        gross_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
        net_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
        order_items = inline_serializer(
            name="OrderItemDetailSErializer",
            fields={
                "item": inline_serializer(
                    name="OrderItemItemDetialSerializer",
                    fields={
                        "id": serializers.IntegerField(),
                        "name": serializers.CharField(),
                        "gross_cost": serializers.DecimalField(max_digits=12, decimal_places=2),
                        "net_cost": serializers.DecimalField(max_digits=12, decimal_places=2),
                        "tax_applicable": serializers.DecimalField(max_digits=12, decimal_places=2),
                    },
                ),
                "quantity": serializers.IntegerField(),
            },
            many=True,
            source="orderitem_set",
        )

    queryset = Order.objects.none()
    serializer_class = OrderDetailSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: OrderDetailSerializer,
        },
    )
    def get(self, request: Request, order_id: int) -> Response:
        order = order_detail(order_id=order_id)

        return Response(
            data=self.OrderDetailSerializer(instance=order).data,
            status=status.HTTP_200_OK,
        )
