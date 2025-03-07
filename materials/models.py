from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название курса", help_text="Введите название курса")
    preview = models.ImageField(
        verbose_name="Предварительный просмотр", upload_to="materials/course", null=True, blank=True
    )
    description = models.TextField(
        verbose_name="Описание курса", null=True, blank=True, help_text="Краткое описание курса"
    )

    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название урока", help_text="Введите название урока")
    preview = models.ImageField(
        verbose_name="Предварительный просмотр", upload_to="materials/lesson", null=True, blank=True
    )
    description = models.TextField(
        verbose_name="Описание урока", null=True, blank=True, help_text="Краткое описание урока"
    )
    url_video = models.URLField(
        verbose_name="Ссылка на видео",
        null=True,
        blank=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        blank=True,
        null=True,
        related_name="lessons",
    )
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
