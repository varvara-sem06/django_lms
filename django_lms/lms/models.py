from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=25,
        verbose_name="Имя",
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
        verbose_name="урок"
        verbose_name_plural="уроки"
