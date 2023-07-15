from rest_framework import serializers
from psycho_tests.models import PsychoTest, Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class PsychoTestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = PsychoTest
        fields = '__all__'

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        answers_data = validated_data.pop('answers', [])

        psycho_test_instance = PsychoTest.objects.create(**validated_data)
        for question_data in questions_data:
            question_serializer = QuestionSerializer(data=question_data)
            question_serializer.is_valid(raise_exception=True)
            question_serializer.save()
            psycho_test_instance.questions.add(question_serializer.instance)

        for answer_data in answers_data:
            answer_data['psycho_test'] = psycho_test_instance.pk
            Answer.objects.create(**answer_data)

        return psycho_test_instance

