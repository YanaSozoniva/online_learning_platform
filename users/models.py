from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        null=True,
        blank=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        null=True,
        blank=True,
        help_text="Введите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        null=True,
        blank=True,
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    CASH = "cash"
    NON_CASH = "non_cash"

    STATUS_CHOICES = [
        (CASH, "Наличные"),
        (NON_CASH, "Перевод на счет"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments", blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="payments", blank=True, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="payments", blank=True, null=True)
    data_payment = models.DateField(verbose_name="Дата оплаты", auto_now=True)
    amount_payment = models.PositiveIntegerField(
        verbose_name="Сумма оплаты", default=0, help_text="Введите сумму оплаты"
    )
    method_payment = models.CharField(max_length=30, choices=STATUS_CHOICES, blank=True, null=True)
    session_id = models.CharField(
        max_length=255,
        verbose_name="Id сессии",
        null=True,
        blank=True,
        help_text="Укажите Id сессии",
    )
    link = models.URLField(
        max_length=400,
        verbose_name="Ссылка на оплату",
        null=True,
        blank=True,
        help_text="Укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user} - {self.course if self.course else self.lesson}"
