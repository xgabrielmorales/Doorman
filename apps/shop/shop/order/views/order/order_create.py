from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import Request, Response

from shop.api.utils import inline_serializer
from shop.item.models import Item
from shop.order.services.order import order_create


class OrderCreateAPIView(GenericAPIView):
    class OrderCreateSerializer(serializers.Serializer):
        order_items = inline_serializer(
            name="OrderItemCreateSerializer",
            fields={
                "item": serializers.PrimaryKeyRelatedField(
                    queryset=Item.objects.filter(active=True),
                ),
                "quantity": serializers.IntegerField(min_value=1),
            },
            many=True,
        )

    class OrderCreatedSerializer(serializers.Serializer):
        id = serializers.IntegerField()

    @extend_schema(
        request=OrderCreateSerializer,
        responses=OrderCreatedSerializer,
    )
    def post(self, request: Request) -> Response:
        serializer = self.OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = order_create(**serializer.validated_data)

        return Response(
            data=self.OrderCreatedSerializer(instance=order).data,
            status=status.HTTP_201_CREATED,
        )
