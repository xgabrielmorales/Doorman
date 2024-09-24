from rest_framework import status
from rest_framework.views import APIView, Request, Response
from drf_spectacular.utils import extend_schema

from none.item.services.item import item_delete


@extend_schema(responses=None, request=None)
class ItemDeleteAPIView(APIView):
    def delete(self, request: Request, item_id: int) -> Response:
        item_delete(item_id=item_id)
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)
