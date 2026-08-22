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
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Course, Lesson, Subscription
from .permissions import IsModeratorOrOwner
from .serializers import CourseSerializer, LessonSerializer
from .paginators import CourseLessonPagination


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination
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
    queryset = Lesson.objects.all()
    pagination_class = CourseLessonPagination
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


class CourseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)

        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            course=course,
        )

        return Response(
            {"subscribed":True},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
            )

    def delete(self, request, course_id):
        subscription = Subscription.objects.filter(
            user=request.user,
            course_id=course_id,
        ).first()

        if subscription:
            subscription.delete()

        return Response(
            {"subscribed": False},
            status=status.HTTP_204_NO_CONTENT,
        )
