from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer

from rest_framework.viewsets import ViewSet


class CourseViewSet(ViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
