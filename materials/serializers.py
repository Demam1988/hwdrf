from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

