from django.db import models
import datetime
from accounts.models import CustomUser
# from courses.models import Student, Instructor, Course, Enrollment, Lesson, Quiz, Question, Choice

class Student(models.Model): 
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_number = models.CharField(max_length=255, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def generate_student_number(self):
        current_year = datetime.datetime.now().year
        first_letters = self.user.first_name[:2].upper() if self.user.first_name else 'XX'
        count = Student.objects.filter(student_number__startswith=f"{current_year}{first_letters}").count() + 1
        return f"{current_year}{first_letters}{str(count).zfill(3)}"

    def save(self, *args, **kwargs):
        if not self.student_number:
            self.student_number = self.generate_student_number()
        super().save(*args, **kwargs)


class Instructor(models.Model):  
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    instructor_number = models.CharField(max_length=255, primary_key=True, editable=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def generate_instructor_number(self):
        current_year = datetime.datetime.now().year
        first_letters = self.user.first_name[:2].upper() if self.user.first_name else 'XX'
        count = Instructor.objects.filter(instructor_number__startswith=f"{current_year}{first_letters}").count() + 1
        return f"{current_year}{first_letters}{str(count).zfill(3)}"

    def save(self, *args, **kwargs):
        if not self.instructor_number:
            self.instructor_number = self.generate_instructor_number()
        super().save(*args, **kwargs)


class Course(models.Model):  
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='courses')
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name
    # payment status
    def is_eligible_for_enrollment(self):
        return hasattr(self, 'payment_status') and self.payment_status.approved


class Enrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)


class Lesson(models.Model):
    instractor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='lessons',null=True, blank=True)
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    description = models.TextField()

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text
    
    # payment model
class PaymentOrSponsorship(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='payment_or_sponsorship')
    payment ='payment'
    SPOMSORSHIP = 'sponsorship'
    TYPE_CHOICES= [
        (payment, 'Payment'),
        (SPOMSORSHIP, 'Sponsorship'),]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=payment)
    document = models.FileField(upload_to='payments/', null=True, blank=True)
    approved = models.BooleanField(default=False)
    crereated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.get_type_display()}"
    def is_eligible(self):
        return self.approved
    


    



