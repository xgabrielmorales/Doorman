from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import Request, Response

from shop.item.services.item import item_create


class ItemCreateAPIView(GenericAPIView):
    class ItemCreateSerializer(serializers.Serializer):
        name = serializers.CharField(min_length=2, max_length=128)
        description = serializers.CharField(allow_blank=True, max_length=128)
        net_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
        tax_applicable = serializers.DecimalField(max_digits=4, decimal_places=2)
        reference = serializers.CharField(allow_blank=True)

    class ItemCreatedSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()

    @extend_schema(
        request=ItemCreateSerializer,
        responses={
            status.HTTP_201_CREATED: ItemCreatedSerializer,
        },
    )
    def post(self, request: Request) -> Response:
        serializer = self.ItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = item_create(**serializer.validated_data)

        return Response(
            data=self.ItemCreatedSerializer(instance=item).data,
            status=status.HTTP_201_CREATED,
        )
