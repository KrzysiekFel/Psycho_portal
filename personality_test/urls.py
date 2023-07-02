from django.urls import path
from .views import personality_test, PersonalityTestView, test_result

urlpatterns = [
    path('', personality_test, name='personality-test'),
    path('new/', PersonalityTestView.as_view(), name='test-create'),
    path('result/', test_result, name='test-result')
]
