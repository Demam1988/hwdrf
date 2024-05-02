from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Course, Lesson, Subscription
from .paginators import MyPaginator
from .serializers import CourseSerializer
from users.models import UserRoles



class CourseViewSet(ModelViewSet):
    """ ViewSet курса """
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    pagination_class = MyPaginator

    def get_queryset(self):
        """ Получаем queryset в зависимости от роли пользователя """

        if self.request.user.is_authenticated:
            if (self.request.user.is_superuser or self.request.user.is_staff
                    or self.request.user.role == UserRoles.MODERATOR):
                return Course.objects.all()

            return Course.objects.filter(owner=self.request.user)
        return []

    def perform_create(self, serializer):
        """ Сохраняем пользователя, добавившего курс """

        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        """ Обновление курса """

        updated_course = serializer.save()
        updated_course.owner = self.request.user
        updated_course.save()

    # def get_permissions(self):
    #     """ Получаем разрешения """
    #
    #     if self.request.method in ['CREATE', 'DELETE']:
    #         self.permission_classes = [IsOwner, ~IsModerator]
    #     else:
    #         self.permission_classes = [IsOwner, ]
    #     return super(CourseViewSet, self).get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """

    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class LessonListAPIView(generics.ListAPIView):
    """ Список уроков """

    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class LessonRetriveAPIView(generics.RetrieveAPIView):
    """ Детально об уроке """

    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Обновление урока """

    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]



