from django.urls import path,include
from .views import *
from rest_framework import routers






urlpatterns=[
    path('lessons/',LessonCreateView.as_view(),name='lesson'),

    path('quizzes/',QuizCreateView.as_view(),name='quiz-list-create'),

]