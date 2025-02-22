from django.contrib.auth.models import AbstractUser, Permission, Group
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


class Payment(AbstractUser):
    CASH = "cash"
    NON_CASH = "non_cash"

    STATUS_CHOICES = [
        (CASH, "Наличные"),
        (NON_CASH, "Перевод на счет"),
    ]

    user = models.ManyToManyField(to=User)
    course = models.ManyToManyField(to=Course)
    lesson = models.ManyToManyField(to=Lesson)
    data_payment = models.DateField(verbose_name='дата оплаты')
    amount_payment = models.PositiveIntegerField(verbose_name='Сумма оплаты', default=0, help_text='Введите дату оплаты')
    method_payment = models.CharField(max_length=30, choices=STATUS_CHOICES,  blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='payment_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='payment_permissions')

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f'{self.user} - {self.course if self.course else self.lesson}'
