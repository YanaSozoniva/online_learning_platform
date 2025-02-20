from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView, LessonListAPIView,
                             LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register("course", CourseViewSet, basename="course")

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lesson/create", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lesson/<int:pk>/detail", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lesson/<int:pk>/update", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/<int:pk>/delete", LessonDestroyAPIView.as_view(), name="lessons_delete"),
] + router.urls
