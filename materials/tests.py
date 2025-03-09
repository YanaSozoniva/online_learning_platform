from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonsTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test@sky.pro")
        self.lesson = Lesson.objects.create(name="Test lesson", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {"name": "test", "description": "test", "owner": self.user.pk}
        response = self.client.post("/lesson/create", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тестирование вывода списка уроков"""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "url_video": None,
                    "name": self.lesson.name,
                    "preview": None,
                    "description": None,
                    "course": None,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.json(), result)

    def test_retrieve_lesson(self):
        """Тестирование вывода информации по уроку"""
        url = reverse("materials:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json().get("name"), self.lesson.name)


class SubscriptionTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="test@sky.pro")
        self.course = Course.objects.create(name="Test course")
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        """Тестирование активации подписки"""
        data = {"course": self.course.pk, "user": self.user}
        response = self.client.post("/subscription/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {"message": "подписка добавлена"})

    def test_subscription_delete(self):
        """Тестирование удаления подписки"""
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        data = {"course": self.course.pk, "user": self.user}
        response = self.client.post("/subscription/", data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), {"message": "подписка удалена"})
