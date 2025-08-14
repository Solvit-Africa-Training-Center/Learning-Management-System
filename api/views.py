from rest_framework import generics,permissions
from rest_framework.response import Response
from  rest_framework.exceptions import PermissionDenied
from .models import *
from .serialzers import *
from django.shortcuts import get_object_or_404


# Create your views here.



class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instructor=getattr(self.request.user, 'instructor', None)
        if not instructor:
            raise PermissionDenied("Only instructors can create lessons.")
        course=serializer.validated_data['course']

        if course.instructor !=instructor:
            raise PermissionDenied("You do not have permission to create lessons for this course.")

        serializer.save(instructor=instructor)



class QuizCreateView(generics.CreateAPIView):
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        instructor = getattr(self.request.user, 'instructor', None)
        if not instructor:
            raise PermissionDenied("Only instructors can create quizzes.")
        lesson = serializer.validated_data['lesson']
        if lesson.course.instructor != instructor:
            raise PermissionDenied("You do not have permission to create quizzes for this lesson come again.")

        serializer.save()

class EnrollnCourse(generics.CreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]