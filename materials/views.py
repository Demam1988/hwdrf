from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer


class CourseViewSet(ModelViewSet):
    """ ViewSet курса """
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer


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



