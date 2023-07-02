from django.urls import path
from .views import personality_test, PersonalityTestView, TestResultView

urlpatterns = [
    path('', personality_test, name='personality-test'),
    path('new/', PersonalityTestView.as_view(), name='test-create'),
    path('result/', TestResultView.as_view(), name='test-result')
]
