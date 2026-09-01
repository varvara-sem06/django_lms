from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=25,
        verbose_name="Имя",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Владелец",
    )

    preview = models.ImageField(
        upload_to="courses/",
        blank=True,
        null=True,
        verbose_name="Превью",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Курс",
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Название",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Владелец",
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание",
    )

    preview = models.ImageField(
        upload_to="lessons/",
        blank=True,
        null=True,
        verbose_name="Превью",
    )

    video_url = models.URLField(
        verbose_name="Ссылка на видео",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="unique_user_course_subscription",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.course}"
