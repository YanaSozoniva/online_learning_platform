from rest_framework import serializers

from materials.models import Course, Lesson
from materials.validators import validate_third_party_resources


class LessonSerializer(serializers.ModelSerializer):
    url_video = serializers.URLField(validators=[validate_third_party_resources])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons_in_course = serializers.SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = "__all__"
