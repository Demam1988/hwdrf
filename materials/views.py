from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework import generics

from django_filters.rest_framework import DjangoFilterBackend

from .models import Course, Lesson, Payment, Subscription
from .paginators import MyPaginator
from .permissions import IsOwner, IsModerator
from .serializers import (CourseSerializer, LessonSerializer,
                          PaymentSerializer, SubscriptionSerializer)
from users.models import UserRoles
from users.tasks import check_last_login


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
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer, *args, **kwargs):
        check_last_login.delay(self.kwargs.get('pk'))
        super().perform_update(serializer)

    def get_permissions(self):
        """Получаем разрешения"""

        if self.action == 'create':
            self.permission_classes = [IsOwner, ~IsModerator]
        elif self.action == 'list':
            self.permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class SubscriptionListAPIView(generics.ListAPIView):
    """ Подписки список """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """ Создание подписки """

    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """ Удаление подписки """

    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated]


class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание урока """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonListAPIView(generics.ListAPIView):
    """ Список уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MyPaginator
    permission_classes = [IsAuthenticated]


class LessonRetriveAPIView(generics.RetrieveAPIView):
    """ Детально об уроке """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator | IsAdminUser]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Обновление урока """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator | IsAdminUser]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление урока """

    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsAdminUser]


class PaymentListAPIView(generics.ListAPIView):
    """ Список оплат """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('date_of_payment',)


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создание ссылки на оплату """

    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Привязка к пользователю """

        new_payment = serializer.save()
        new_payment.user = self.request.user
        new_payment.save()
