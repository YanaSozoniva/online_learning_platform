import re

from rest_framework.serializers import ValidationError


def validate_third_party_resources(value):
    """Проверка на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com"""
    url = re.compile(r"^(https?://)?(www\.)?youtube\.com/?$")
    if not bool(url.match(value)):
        raise ValidationError("Нельзя прикреплять ссылки на сторонние образовательные платформы или личные сайты!")
