from django.core.management.base import BaseCommand
from users.models import User, Payment
from materials.models import Course, Lesson


class Command(BaseCommand):
    help = 'Добавление новых платежей'

    def handle(self, *args, **kwargs):

        course, _ = Course.objects.get_or_create(id=1)
        lesson, _ = Lesson.objects.get_or_create(id=3)
        user, _ = User.objects.get_or_create(id=4)

        payments = [
            {'user': user, 'course': course, 'data_payment': '2025-01-01', 'amount_payment': 1000, 'method_payment': Payment.CASH},
            {'user': user, 'lesson': lesson, 'data_payment': '2025-02-01', 'amount_payment': 2000, 'method_payment': Payment.NON_CASH},
        ]

        for payment_data in payments:
            payment, created = Payment.objects.get_or_create(**payment_data)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully added student: {payment.course if payment.course else payment.lesson}'))
            else:
                self.stdout.write(self.style.WARNING(f'Student already exists: {payment.course if payment.course else payment.lesson}'))
