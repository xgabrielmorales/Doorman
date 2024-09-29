from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView, Request, Response

from shop.order.services.order import order_delete


class OrderDeleteAPIView(APIView):
    @extend_schema(request=None, responses=None)
    def delete(self, request: Request, order_id: int) -> Response:
        order_delete(order_id=order_id)
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
