from django.urls import path
from .views import personality_test, PersonalityTestView, TestResultView, CreateTestView, PsychoTestsListView

urlpatterns = [
    path('', PsychoTestsListView.as_view(), name='personality-tests'),
    path('create/', CreateTestView.as_view(), name='create-test'),


    # old to correct
    path('new/', PersonalityTestView.as_view(), name='test-create'),
    path('result/', TestResultView.as_view(), name='test-result'),

]
