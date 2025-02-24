from rest_framework.routers import DefaultRouter
from django.urls import path

from users.apps import UsersConfig
from users.views import UserViewSet, PaymentListAPIView

app_name = UsersConfig.name

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),

]+router.urls
