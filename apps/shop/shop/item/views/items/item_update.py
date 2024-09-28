from drf_spectacular.utils import extend_schema
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import Request, Response

from shop.item.services.item import item_partial_update


class ItemPartialUpdateAPIView(GenericAPIView):
    class ItemUpdateSerializer(serializers.Serializer):
        name = serializers.CharField(min_length=2, max_length=128, required=False)
        description = serializers.CharField(allow_blank=True, max_length=128, required=False)
        net_cost = serializers.DecimalField(max_digits=12, decimal_places=3, required=False)
        tax_applicable = serializers.DecimalField(max_digits=4, decimal_places=2, required=False)
        reference = serializers.CharField(allow_blank=True, required=False)

    @extend_schema(request=ItemUpdateSerializer, responses=None)
    def patch(self, request: Request, item_id: str) -> Response:
        serializer = self.ItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item_partial_update(item_id=item_id, **serializer.validated_data)

        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
