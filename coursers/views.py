from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Enrollment, Course, Lesson
from .serializers import EnrollmentSerializer, LessonSerializer
from rest_framework.response import Response
from rest_framework import status

class EnrollInCourseView(generics.CreateAPIView):
    """
    Student enrolls in a course if eligible.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        student = self.request.user.student
        if student.is_eligible_for_enrollment():
            serializer.save(student=student)
        else:
            raise PermissionError("You must pay or have sponsorship approved to enroll.")

class CourseContentView(generics.ListAPIView):
    """
    List lessons for a course if student is enrolled.
    """
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        student = self.request.user.student
        enrolled = Enrollment.objects.filter(student=student, course_id=course_id).exists()
        if not enrolled:
            return Lesson.objects.none()
        return Lesson.objects.filter(course_id=course_id)
