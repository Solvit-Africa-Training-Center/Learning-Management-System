from rest_framework import serializers
from.models import (Course, Enrollment, Student, Instructor,Lesson,Choice,Question,Quiz)



class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Choice
        fields="__all__"



class QuestionSerializer(serializers.ModelSerializer):
    choices=ChoiceSerializer(many=True, required=True)
    class Meta:
        model=Question
        fields = ["id", "question_text", "choices"]

        

    def create(self, validated_data):
        choices_data= validated_data.pop("choices",[])
        question=Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question



class QuizSerializer(serializers.ModelSerializer):
    questions=QuestionSerializer(many=True, required=True)
    class Meta:
        model=Quiz
        fields=["id", "title", "lesson", "questions"]

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        quiz = Quiz.objects.create(**validated_data)
        for question_data in questions_data:
            QuestionSerializer.create(QuestionSerializer(), validated_data=question_data)
        return quiz


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        fields=["id", "title", "course", "description", "instructor"]






