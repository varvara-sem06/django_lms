from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User

from .models import Course, Subscription


@shared_task
def send_course_update(course_id):
    course = Course.objects.get(id=course_id)

    subscriptions = Subscription.objects.filter(course=course)

    emails = [sub.user.email for sub in subscriptions]

    if emails:
        send_mail(
            subject=f"Курс обновлен: {course.title}",
            message=f"В курсе {course.title} появились новые материалы.",
            from_email=None,
            recipient_list=emails,
            fail_silently=False,
        )


@shared_task
def deactivate_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)

    users = User.objects.filter(
        last_login__lt=month_ago,
        is_active=True,
    )

    users.update(is_active=False)
