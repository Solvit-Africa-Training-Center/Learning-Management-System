from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from api.models import CustomUser, Instructor, Course, Lesson

class LessonTest(APITestCase):
    def setUp(self):
 
        self.user = CustomUser.objects.create_user(
            username='phinona45',
            email='phinona45@example.com',
            first_name='Phinona',
            last_name='Doe',
            password='ngewe001@',
            role='Instructor'
        )
        self.instructor = Instructor.objects.create(user=self.user)

        self.course = Course.objects.create(
            course_name='Test Course',
            description='Test Course Description',
            amount=1000,
            instructor=self.instructor
        )


        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            instructor=self.instructor,
            course=self.course
        )

        
        self.client.force_authenticate(user=self.user)

    def test_create_lesson(self):
        response = self.client.post(
            reverse('lesson'),  
            {
                'title': 'New Lesson',
                'description': 'New Lesson Description',
                'course': self.course.id
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Lesson')
