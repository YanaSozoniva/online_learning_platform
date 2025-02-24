from django.urls import path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
] + router.urls
