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
    class Meta:
        model = PsychoTest
        fields = "__all__"

