from rest_framework import serializers
from .models import Enrollment, Course, Lesson

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'student', 'enrollment_date']
        read_only_fields = ['enrollment_date']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'course']
