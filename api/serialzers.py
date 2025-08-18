from rest_framework import serializers
from.models import (Course, Enrollment, Student, Instructor,Lesson,Choice,Question,Quiz, StudentProgress)




class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=["user", "student_number"]


class CourseSerializer(serializers.ModelSerializer):
      class Meta:
          model=Course
          fields=["id", "course_name", "description", "amount", "instructor", "enrolled_students"]
          extra_kwargs = {
             'id':{
                 'read_only':True
             }
          }


class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model=Enrollment
        fields=["id", "course", "student", "enrollment_date", "completed_date"]
        extra_kwargs={
            'id':{'read_only':True},
            'enrollment_date': {'read_only': True},
            'completed_date': {'read_only': True}
        }
    def validate(self,data):
        course=data.get('course')
        student=data.get('student')
        if Enrollment.objects.filter(course=course, student=student).exists():
            raise serializers.ValidationError("You are already enrolled in this course.")
        return data


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Choice
        fields="__all__"
        extra_kwargs = {
            'question': {'required': False, 'read_only': True}
        }



class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=True)

    class Meta:
        model = Question
        fields = ["id", "question_text","choices"]

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question





class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=True)
    
    class Meta:
        model = Quiz
        fields = ["id", "title", "lesson", "questions"]

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        quiz = Quiz.objects.create(**validated_data)
        
        for question_data in questions_data:
            choices_data = question_data.pop('choices', [])
            question = Question.objects.create(quiz=quiz, **question_data)
            
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)
                
        return quiz



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        fields=["id", "title", "course", "description","instructor"]





