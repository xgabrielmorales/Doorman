from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import Request, Response

from shop.api.utils import inline_serializer
from shop.item.models import Item
from shop.order.services.order import order_update


class OrderPartialUpdateAPIView(GenericAPIView):
    class OrderPartialUpdateSerializer(serializers.Serializer):
        order_items = inline_serializer(
            name="OrderItemPartialUpdateSerializer",
            fields={
                "item": serializers.PrimaryKeyRelatedField(
                    queryset=Item.objects.filter(active=True),
                ),
                "quantity": serializers.IntegerField(min_value=1),
            },
            many=True,
        )

    @extend_schema(
        request=OrderPartialUpdateSerializer,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def patch(self, request: Request, order_id: int) -> Response:
        serializer = self.OrderPartialUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_update(order_id=order_id, **serializer.validated_data)

        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
