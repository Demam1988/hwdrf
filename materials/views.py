from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter


from .models import Course, Lesson, Subscription, Payment
from .paginators import MyPaginator
from .permissions import IsOwner, IsModerator
from .serializers import CourseSerializer, PaymentSerializer
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

    def get_permissions(self):
        """ Получаем разрешения """

        if self.request.method in ['CREATE', 'DELETE']:
            self.permission_classes = [IsOwner, ~IsModerator]
        else:
            self.permission_classes = [IsOwner, ]
        return super(CourseViewSet, self).get_permissions()


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



