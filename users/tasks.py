from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def block_user():
    today = timezone.now().date() - timedelta(days=30)
    users = User.objects.filter(is_active=True, last_login__lt=today)
    print(users)
    for user in users:
        user.is_active = False
        user.save()
        print(f"Пользователь {user.email} заблокирован, т.к. заходил последний раз более 30 дней назад: {user.last_login}")
