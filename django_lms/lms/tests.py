from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription

User = get_user_model()


class LessonCRUDTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="12345")

        self.user2 = User.objects.create_user(email="user2@test.com", password="12345")

        self.course = Course.objects.create(name="Python", owner=self.user)

        self.lesson = Lesson.objects.create(
            course=self.course,
            owner=self.user,
            name="Lesson 1",
            video_url="https://www.youtube.com/watch?v=test",
        )

        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        response = self.client.get(reverse("lesson-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_lesson_create(self):
        data = {
            "course": self.course.id,
            "name": "New lesson",
            "description": "text",
            "video_url": "https://www.youtube.com/watch?v=123",
        }

        response = self.client.post(reverse("lesson-create"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_invalid_url(self):
        data = {
            "course": self.course.id,
            "name": "Bad lesson",
            "video_url": "https://udemy.com/course/python",
        }

        response = self.client.post(reverse("lesson-create"), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_update(self):
        data = {
            "course": self.course.id,
            "name": "Updated lesson",
            "video_url": "https://www.youtube.com/watch?v=777",
        }

        response = self.client.put(
            reverse("lesson-update", args=[self.lesson.id]), data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Updated lesson")

    def test_lesson_delete(self):
        response = self.client.delete(reverse("lesson-delete", args=[self.lesson.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="12345")

        self.course = Course.objects.create(name="Django", owner=self.user)

        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        response = self.client.post(reverse("course-subscribe", args=[self.course.id]))

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe(self):
        Subscription.objects.create(user=self.user, course=self.course)

        response = self.client.delete(
            reverse("course-subscribe", args=[self.course.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_course_has_subscription_field(self):
        Subscription.objects.create(user=self.user, course=self.course)

        response = self.client.get(reverse("course-detail", args=[self.course.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_subscribed"])
