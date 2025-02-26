from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ("id", "payments", "email", "phone", "city", "is_active")
