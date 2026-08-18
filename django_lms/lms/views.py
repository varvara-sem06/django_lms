from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Course, Lesson
from .permissions import IsModeratorOrOwner
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Moderators").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name="Moderators").exists():
            raise PermissionDenied("Модераторы не могут создавать курсы.")

        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name="Moderators").exists():
            raise PermissionDenied("Модераторы не могут удалять курсы.")

        instance.delete()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    queryset = Lesson.objects.all()


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    queryset = Lesson.objects.all()

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name="Moderators").exists():
            raise PermissionDenied("Модераторы не могут создавать уроки.")

        serializer.save(owner=self.request.user)


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    queryset = Lesson.objects.all()


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    queryset = Lesson.objects.all()

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name="Moderators").exists():
            raise PermissionDenied("Модераторы не могут удалять уроки.")

        instance.delete()
