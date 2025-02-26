from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "method_payment"]
    ordering_fields = ("data_payment",)
