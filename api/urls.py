from django.urls import path
from .views import CreateQuestions, CreateAnswers, CreatePsychoTest

urlpatterns = [
    path('create_questions/', CreateQuestions.as_view(), name='create-questions'),
    path('create_answers/', CreateAnswers.as_view(), name='create-answers'),
    path('create_psycho_test/', CreatePsychoTest.as_view(), name='create-psycho-test')
]
