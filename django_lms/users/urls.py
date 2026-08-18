from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentListAPIView, UserRegisterAPIView, UserViewSet

router = DefaultRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path(
        "payments/",
        PaymentListAPIView.as_view(),
        name="payments",
    ),
    path("", include(router.urls)),
]
