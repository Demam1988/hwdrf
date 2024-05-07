from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson, Payment, Subscription
from materials.services.create_pay import get_payment_link
from materials.validators import LinkValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkValidator(field="link")]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lesson = LessonSerializer(source="lessons", many=True, read_only=True)
    subscribed_users = SubscriptionSerializer(
        source="subscriptions", many=True, read_only=True
    )

    class Meta:
        model = Course
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    payment_url = SerializerMethodField()

    def get_payment_url(self, payment):

        return get_payment_link(payment)

    class Meta:
        model = Payment
        fields = "__all__"
