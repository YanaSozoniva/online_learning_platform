from celery import shared_task
from django.core.mail import send_mail

from config import settings


@shared_task
def send_info_about_course_update(course, email):
    """Отправляет пользователю сообщение об обновлении курса"""
    send_mail(
        "Обновление курса", f"Курс {course} обновлен. Можете продолжить обучение", settings.EMAIL_HOST_USER, [email]
    )
