from rest_framework.viewsets import generics
from psycho_tests.models import Answers, Question, PsychoTest
from rest_framework.permissions import IsAuthenticated
from .serializers import QuestionsSerializer, AnswersSerializer, PsychoTestSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from django.http import HttpRequest, HttpResponse


class CreateQuestions(generics.ListCreateAPIView):
    """
    User can list and create one or many questions in one POST request.
    """
    serializer_class = QuestionsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()

    def create(self, request, *args, **kwargs) -> HttpResponse:
        if isinstance(request.data, list):
            data = request.data
        else:
            data = [request.data]

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class CreateAnswers(generics.ListCreateAPIView):
    """
    User can list and create one or many answers in one POST request.
    """
    serializer_class = AnswersSerializer
    permission_classes = [IsAuthenticated]
    queryset = Answers.objects.all()

    def create(self, request, *args, **kwargs) -> HttpResponse:
        if isinstance(request.data, list):
            data = request.data
        else:
            data = [request.data]

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)


class CreatePsychoTest(generics.ListCreateAPIView):
    """
    User can list all tests and create one test per POST request.
    """
    serializer_class = PsychoTestSerializer
    permission_classes = [IsAuthenticated]
    queryset = PsychoTest.objects.all()

    def create(self, request, *args, **kwargs) -> HttpResponse:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)
