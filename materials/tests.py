from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson, Course, Subscription
from users.models import User, UserRoles


class EducationTestCase(APITestCase):
    def setUp(self):
        """Заполнение первичных данных"""

        self.user = User.objects.create(
            username="admin@test.com",
            email="admin@test.com",
            is_staff=True,
            is_superuser=True,
            is_active=True,
            role=UserRoles.MEMBER,
        )
        self.user.set_password("12345")
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title="test title course", description="test description course"
        )

        self.lesson = Lesson.objects.create(
            title="test title lesson",
            description="test description lesson",
            course=self.course,
            owner=self.user,
        )

    def test_lesson_retrieve(self):
        """Test retrieve a lesson"""

        response = self.client.get(
            reverse("education:lesson_detail", args=[self.lesson.pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_lesson_list(self):
        """Тест получения списка уроков"""

        response = self.client.get(reverse("education:lesson_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 5,
                        "title": "test title lesson",
                        "description": "test description lesson",
                        "picture": None,
                        "link": None,
                        "course": 4,
                        "owner": 4,
                    }
                ],
            },
        )

    def test_create_lesson(self):
        """Тест создания урока"""

        data = {
            "title": "test create lesson",
            "description": "test create description lesson",
            "course": 1,
        }

        response = self.client.post(reverse("education:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "title": "test create lesson",
                "description": "test create description lesson",
                "picture": None,
                "link": None,
                "course": 1,
                "owner": 1,
            },
        )

        self.assertEqual(2, Lesson.objects.all().count())

    def test_update_lesson(self):
        """Тест обновления урока"""

        data = {
            "title": "update test",
        }

        response = self.client.put(
            reverse("education:lesson_update", args=[self.lesson.pk]), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.lesson.refresh_from_db()

        self.assertEqual(self.lesson.title, "update test")

    def test_lesson_delete(self):
        """Тест удаления урока"""

        response = self.client.delete(
            reverse("education:lesson_delete", args=[self.lesson.pk])
        )

        self.assertFalse(Lesson.objects.filter(id=self.lesson.pk).exists())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_subscription(self):
        """Тест создания подписки"""

        data = {"user": self.user.pk, "course": self.course.pk}
        response = self.client.post(reverse("education:subscription_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_subscription(self):
        """Тест удаления подписки"""

        self.client.delete(
            reverse("education:subscription_delete", args=[self.course.id])
        )

        self.assertFalse(Subscription.objects.filter(id=self.course.id).exists())

    def tearDown(self):
        Course.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()
