from django.contrib import admin
from .models import (Student,Instructor,Course,
                     Enrollment,Lesson,
                     Question,Quiz,
                     Choice)

# Register your models here.


@admin.register(Student)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ["student_number", "get_first_name", "get_last_name"]

    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'  
    get_first_name.short_description = 'First Name'       

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'
    get_last_name.short_description = 'Last Name'


@admin.register(Instructor)
class InstructorsAdmin(admin.ModelAdmin):
    list_display = ["instructor_number", "get_first_name", "get_last_name"]
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.admin_order_field = 'user__first_name'  

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.admin_order_field = 'user__last_name'
    get_last_name.short_description = 'Last Name'


@admin.register(Course)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ["course_name", "get_enrolled_students", "description", "amount"]

    def get_enrolled_students(self, obj):
        return ", ".join([str(student) for student in obj.enrolled_students.all()])
    get_enrolled_students.short_description = "Enrolled Students"



@admin.register(Enrollment)
class EnrollmentsAdmin(admin.ModelAdmin):
    list_display = ["student", "course","enrollment_date"]


@admin.register(Lesson)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ["title","course","description","instructor"]


@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ["question_text","quiz"]


@admin.register(Quiz)
class QuizzesAdmin(admin.ModelAdmin):
    list_display = ["title", "lesson"]

@admin.register(Choice)
class ChoicesAdmin(admin.ModelAdmin):
    list_display = ["choice_text", "question"]



       



