from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from .models import Payment
from .serializers import PaymentSerializer


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
