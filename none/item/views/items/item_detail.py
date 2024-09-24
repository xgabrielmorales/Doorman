from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.views import Request, Response

from none.item.selectors.item import item_detail


class ItemDetailAPIView(GenericAPIView):
    class ItemDetailSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        description = serializers.CharField()
        net_cost = serializers.DecimalField(max_digits=12, decimal_places=2)
        tax_applicable = serializers.DecimalField(max_digits=4, decimal_places=2)
        reference = serializers.CharField()

    @extend_schema(
        responses={
            status.HTTP_200_OK: ItemDetailSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Item no encontrado.",
                response=str,
            ),
        },
    )
    def get(self, request: Request, item_id: str) -> Response:
        item = item_detail(item_id=item_id)

        return Response(
            data=self.ItemDetailSerializer(instance=item).data,
            status=status.HTTP_200_OK,
        )
