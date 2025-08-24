from rest_framework import generics,permissions,viewsets
from rest_framework.response import Response
from rest_framework import status
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "message": "Student progression created successfull",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )





class CourseListView(generics.ListAPIView):
    queryset=Course.objects                  .all()
    serializer_class=CourseSerializer
    def get(self, request,*arg,**kwargs):
        serializer=CourseSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    