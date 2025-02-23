from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Добавление новых пользователей'

    def handle(self, *args, **kwargs):

        users = [
            {'email': 'test@test.ru', 'password': '123qwe456rty', 'is_active': True, 'is_superuser': False},
            {'email': 'user@test.ru', 'password': '123qwe456rty', 'is_active': True, 'is_superuser': False},
        ]

        for user_data in users:
            user, created = User.objects.get_or_create(**user_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added student: {user.email}'))
            else:
                self.stdout.write(self.style.WARNING(f'Student already exists: {user.email}'))
