from django.urls import path
from .views import personality_test, new_test, test_result

urlpatterns = [
    path('', personality_test, name='personality-test'),
    path('new/', new_test, name='test-create'),
    path('result/', test_result, name='test-result')
]
