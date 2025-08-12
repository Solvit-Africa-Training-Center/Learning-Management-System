from django.urls import path
from .views import EnrollInCourseView, CourseContentView

urlpatterns = [
    path('enroll/', EnrollInCourseView.as_view(), name='enroll-course'),
    path('course/<int:course_id>/lessons/', CourseContentView.as_view(), name='course-lessons'),
]
