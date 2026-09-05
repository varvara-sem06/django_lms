from django.contrib.auth import get_user_model
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Payment
from .permissions import IsOwnerOrReadOnly
from .serializers import (PaymentSerializer, UserRegisterSerializer,
                          UserSerializer)

User = get_user_model()


class UserRegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = []


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            if self.get_object() == self.request.user:
                return UserSerializer

            return PublicUserSerializer

        return UserSerializer


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )

    filterset_fields = (
        "course",
        "lesson",
        "payment_method",
    )

    ordering_fields = ("payment_date",)

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Moderators").exists():
            return Payment.objects.all()

        return Payment.objects.filter(user=user)


class PaymentListAPIView(ListAPIView):

    queryset = Payment.objects.all()

    serializer_class = PaymentSerializer


class PaymentListAPIView(ListAPIView):

    queryset = Payment.objects.all()

    serializer_class = PaymentSerializer

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )

    filterset_fields = (
        "course",
        "lesson",
        "payment_method",
    )

    ordering_fields = ("payment_date",)
