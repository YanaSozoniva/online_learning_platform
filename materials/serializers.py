from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_third_party_resources


class LessonSerializer(serializers.ModelSerializer):
    url_video = serializers.URLField(required=False, validators=[validate_third_party_resources])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons_in_course = serializers.SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    subscription_to_course = serializers.SerializerMethodField()

    def get_subscription_to_course(self, course):
        return Subscription.objects.filter(course=course).exists()

    class Meta:
        model = Course
        fields = "__all__"
