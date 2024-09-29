from django.urls import include, path

from shop.order.views.order import (
    OrderCreateAPIView,
    OrderDeleteAPIView,
    OrderDetailAPIView,
    OrderListAPIView,
    OrderPartialUpdateAPIView,
)

app_name = "orders"

order_patters = [
    path("", OrderListAPIView.as_view(), name="list"),
    path("<int:order_id>", OrderDetailAPIView.as_view(), name="detail"),
    path("create/", OrderCreateAPIView.as_view(), name="create"),
    path("<int:order_id>/update", OrderPartialUpdateAPIView.as_view(), name="update"),
    path("<int:order_id>/delete", OrderDeleteAPIView.as_view(), name="delete"),
]

urlpatterns = [
    path("", include(order_patters), name="orders"),
]
