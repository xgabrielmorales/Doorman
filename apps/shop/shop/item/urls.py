from django.urls import include, path

from shop.item.views.items import (
    ItemCreateAPIView,
    ItemDeleteAPIView,
    ItemDetailAPIView,
    ItemListAPIView,
    ItemPartialUpdateAPIView,
)

app_name = "items"

item_patters = [
    path("", ItemListAPIView.as_view(), name="list"),
    path("<int:item_id>/", ItemDetailAPIView.as_view(), name="detail"),
    path("create/", ItemCreateAPIView.as_view(), name="create"),
    path("update/<int:item_id>", ItemPartialUpdateAPIView.as_view(), name="partial_update"),
    path("delete/<int:item_id>", ItemDeleteAPIView.as_view(), name="delete"),
]

urlpatterns = [
    path("", include(item_patters), name="items"),
]
