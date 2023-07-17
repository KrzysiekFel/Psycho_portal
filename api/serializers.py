from rest_framework import serializers
from psycho_tests.models import PsychoTest, Question, Answers
from typing import Type, List, Dict, Any


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = "__all__"


class PsychoTestSerializer(serializers.ModelSerializer):
    # questions = QuestionsSerializer(many=True)
    # answers = AnswersSerializer(many=True, read_only=True)

    class Meta:
        model = PsychoTest
        fields = "__all__"

    # def create(self, validated_data: Dict[str, Any]) -> PsychoTest:
    #     questions_data: List[Dict[str, str]] = validated_data.pop("questions", [])
    #     answers_data: List[Dict[str, str]] = validated_data.pop("answers", [])
    #
    #     psycho_test_instance = PsychoTest.objects.create(**validated_data)
    #     for question_data in questions_data:
    #         question_serializer = QuestionSerializer(data=question_data)
    #         question_serializer.is_valid(raise_exception=True)
    #         question_serializer.save()
    #         psycho_test_instance.questions.add(question_serializer.instance)
    #
    #     for answer_data in answers_data:
    #         answer_data["psycho_test"] = psycho_test_instance.pk
    #         Answers.objects.create(**answer_data)
    #
    #     return psycho_test_instance
