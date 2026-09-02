from datetime import timedelta

from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Course, Lesson, Subscription
from .paginators import CourseLessonPagination
from .permissions import IsModeratorOrOwner
from .serializers import CourseSerializer, LessonSerializer
from .services import (create_checkout_session, create_stripe_price,
                       create_stripe_product, retrieve_checkout_session)
from .tasks import send_course_update


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CourseLessonPagination
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    @swagger_auto_schema(
        operation_summary="Список курсов",
        operation_description="Возвращает список всех курсов.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Создать курс",
        operation_description="Создает новый курс.",
        request_body=CourseSerializer,
        responses={201: CourseSerializer},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

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

    def perform_update(self, serializer):
        course = serializer.save()

        if timezone.now() - course.updated_at > timedelta(hours=4):
            send_course_update.delay(course.id)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    pagination_class = CourseLessonPagination
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    @swagger_auto_schema(
        operation_summary="Список уроков",
        operation_description="Возвращает список уроков.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="Получить урок",
        operation_description="Возвращает информацию об одном уроке.",
        responses={200: LessonSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LessonViewSet(ModelViewSet):

    def perform_update(self, serializer):
        lesson = serializer.save()

        course = lesson.course

        if timezone.now() - course.updated_at > timedelta(hours=4):
            send_course_update.delay(course.id)

        course.updated_at = timezone.now()
        course.save(update_fields=["updated_at"])


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    queryset = Lesson.objects.all()

    @swagger_auto_schema(
        operation_summary="Создать урок",
        request_body=LessonSerializer,
        responses={201: LessonSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @swagger_auto_schema(
        operation_summary="Обновить урок",
        request_body=LessonSerializer,
        responses={200: LessonSerializer},
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частично обновить урок",
        request_body=LessonSerializer,
        responses={200: LessonSerializer},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class LessonDestroyAPIView(DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsModeratorOrOwner,
    ]

    queryset = Lesson.objects.all()

    @swagger_auto_schema(
        operation_summary="Удалить урок",
        responses={204: "No Content"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name="Moderators").exists():
            raise PermissionDenied("Модераторы не могут удалять уроки.")

        instance.delete()


class CourseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Подписаться на урок",
        operation_description="Создает подписку пользователя на курс",
        responses={200: "Подписка уже существует.", 201: "Подписка создана."},
    )
    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)

        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            course=course,
        )

        return Response(
            {"subscribed": True},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        operation_summary="Отписаться от курса",
        operation_description="Удаляет подписку пользователя на курс",
        responses={204: "Подписка удалена."},
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


class CoursePaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Оплата курса",
        operation_description="Создает Stripe Checkout Session и возвращает ссылку на оплату.",
        responses={201: "Ссылка на оплату создана."},
    )
    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)

        product = create_stripe_product(course)

        price = create_stripe_price(
            product,
            course,
        )

        session = create_checkout_session(price)

        return Response(
            {
                "payment_url": session.url,
            },
            status=status.HTTP_201_CREATED,
        )


class CoursePaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Проверить статус оплаты",
        operation_description="Возвращает информацию о Stripe Checkout Session.",
    )
    def get(self, request, session_id):
        session = retrieve_checkout_session(session_id)

        return Response(
            {
                "id": session.id,
                "status": session.status,
                "payment_status": session.payment_status,
            },
            status=status.HTTP_200_OK,
        )
