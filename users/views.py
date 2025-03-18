from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from users.models import Payment, User
from users.permissions import IsUser
from users.serializers import PaymentSerializer, UserDetailSerializer, UserSerializer
from users.services import PaymentStripe


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return UserDetailSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = (
                IsUser,
                IsAuthenticated,
            )
        elif self.action == "retrieve":
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data["password"])
        user.save()


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["course", "lesson", "method_payment"]
    ordering_fields = ("data_payment",)


class PaymentCreateAPIView(generics.CreateAPIView):

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get("course")

        if course_id:
            payment.course = get_object_or_404(Course, pk=course_id)
            product = payment.course.name
        else:
            lesson_id = self.request.data.get("lesson")
            payment.lesson = get_object_or_404(Lesson, pk=lesson_id)
            product = payment.lesson.name

        product_id = PaymentStripe.create_stripe_product(product)
        amount = self.request.data.get("amount_payment")
        price = PaymentStripe.create_stripe_price(product_id, amount)
        session_id, session_url = PaymentStripe.create_stripe_session(price)
        payment.session_id = session_id
        payment.link = session_url
        payment.method_payment = "non_cash"
        payment.save()
