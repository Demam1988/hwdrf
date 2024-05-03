from os import path

from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import (CourseViewSet, LessonCreateAPIView,
                             LessonDestroyAPIView, LessonListAPIView,
                             LessonRetriveAPIView, LessonUpdateAPIView, PaymentListAPIView, PaymentCreateAPIView)

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register('', CourseViewSet)

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(),
         name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(),
         name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetriveAPIView.as_view(),
         name='lesson_detail'),
    path('lesson/update/<int:pk>/',
         LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/',
         LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payments/', PaymentListAPIView.as_view(),
         name='payment_list'),
    path('payments/create/', PaymentCreateAPIView.as_view(),
         name='payment_create'),
]

urlpatterns += router.urls
