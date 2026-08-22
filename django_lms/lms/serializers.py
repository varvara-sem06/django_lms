from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[validate_youtube_url]
    )
    

    class Meta:
        model = Lesson
        fields = (
            "id",
            "course",
            "name",
            "description",
            "preview",
            "video_url",
        )


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "preview",
            "description",
            "lessons_count",
            "lessons",
            "is_subscribed",
        )

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        return Subscription.objects.filter(
            user=request.user,
            course=obj
        ).exists()

    
